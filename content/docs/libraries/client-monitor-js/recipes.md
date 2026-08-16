---
title: "Recipes"
slug: "recipes"
description: "Worked integration patterns for client-monitor-js"
lead: "Complete, copy-ready patterns for dashboards, adaptive UX, production tuning and framework integration"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 318
toc: true
---

## Production monitoring pipeline

A configuration tuned for cost and signal quality rather than debugging resolution.

```javascript
import { ClientMonitor } from "@observertc/client-monitor-js";
import { ClientSampleEncoder } from "@observertc/samples-encoder";

// One encoder per client — it elides values that repeat between samples.
const encoder = new ClientSampleEncoder(session.participantId);

const monitor = new ClientMonitor({
    clientId: session.participantId,
    callId: session.roomId,

    collectingPeriodInMs: 3000,     // lower main-thread cost
    samplingPeriodInMs: 10000,      // less upload volume

    congestionDetector: { sensitivity: "low" },   // only strong evidence
    syntheticSamplesDetector: null,               // not acted on — don't build it

    appData: { appVersion: BUILD_VERSION },
});

monitor.attachments = {
    appVersion: BUILD_VERSION,
    region: session.region,
    tier: user.plan,
};

monitor.addSource(peerConnection);

// Ship telemetry.
monitor.on("sample-created", (sample) => {
    navigator.sendBeacon(`/api/samples/${session.participantId}`, encoder.encodeToBytes(sample));
});

// Route issues by how much you care.
monitor.on("issue", (issue) => {
    if (issue.type === "congestion" || issue.type === "cpulimitation") {
        alerting.notify(issue);
    } else {
        log.info("issue", issue.type, issue.payload);
    }
});

// Episode durations are the useful analytics event, not the raise.
monitor.on("issue-resolved", (resolved) => {
    analytics.track("quality_episode", {
        type: resolved.type,
        durationInMs: resolved.payload?.durationInMs,
    });
});

window.addEventListener("pagehide", () => monitor.close());
```

## In-call quality indicator

`activeIssues` is a live set, so rendering from it gives you an indicator that is correct by
construction — it clears itself when the detector resolves the issue.

```javascript
const SEVERITY = {
    congestion: "critical",
    cpulimitation: "critical",
    "dry-inbound-track": "critical",
    "dry-outbound-track": "critical",
    "freezed-video-track": "warning",
    "audio-desync": "warning",
    "inbound-video-playout-discrepancy": "warning",
};

monitor.on("stats-collected", () => {
    const active = monitor.getActiveIssuesByType();

    const worst = active.reduce((acc, issue) => {
        const level = SEVERITY[issue.type] ?? "info";
        return level === "critical" ? "critical" : acc === "critical" ? acc : level;
    }, "ok");

    ui.setNetworkIndicator({
        level: worst,
        score: monitor.score,
        detail: active.map((i) => i.type),
    });
});
```

## Adaptive behaviour

Reacting to detector verdicts inside the client is often the highest-value use of the library —
the fix happens before the user complains.

```javascript
monitor.on("issue", async (issue) => {
    switch (issue.type) {
        case "congestion": {
            // Shed the most expensive stream first.
            await screenShare?.pause();
            ui.toast("Network is congested — screen share paused");
            break;
        }
        case "cpulimitation": {
            // Reduce our own encoding cost.
            await sender.setParameters({
                ...sender.getParameters(),
                encodings: [{ maxBitrate: 300_000, scaleResolutionDownBy: 2 }],
            });
            break;
        }
        case "dry-outbound-track": {
            // Almost always a local capture problem.
            ui.promptDeviceCheck(issue.payload.trackId);
            break;
        }
    }
});

monitor.on("issue-resolved", async (resolved) => {
    if (resolved.type === "congestion") {
        await screenShare?.resume();
        ui.toast("Network recovered");
    }
});
```

## Real-time dashboard data

Everything a per-participant quality dashboard needs, computed once per tick.

```javascript
monitor.on("stats-collected", () => {
    const snapshot = {
        timestamp: Date.now(),
        score: monitor.score,
        scoreReasons: monitor.scoreReasons,

        bitrates: {
            sendingAudio: monitor.sendingAudioBitrate,
            sendingVideo: monitor.sendingVideoBitrate,
            receivingAudio: monitor.receivingAudioBitrate,
            receivingVideo: monitor.receivingVideoBitrate,
        },

        capacity: {
            availableIn: monitor.totalAvailableIncomingBitrate,
            availableOut: monitor.totalAvailableOutgoingBitrate,
        },

        rttMs: (monitor.avgRttInSec ?? 0) * 1000,

        connections: monitor.peerConnections.map((pc) => ({
            id: pc.peerConnectionId,
            iceState: pc.iceState,
            turn: pc.usingTURN,
            tcp: pc.usingTCP,
            rttMs: (pc.avgRttInSec ?? 0) * 1000,
            score: pc.calculatedStabilityScore?.value,
        })),

        tracks: monitor.tracks.map((t) => {
            const rtp = t.direction === "inbound" ? t.getInboundRtp() : t.getHighestLayer();
            return {
                id: t.track.id,
                kind: t.kind,
                direction: t.direction,
                bitrate: t.bitrate,
                fps: rtp?.ewmaFps,
                loss: t.fractionLost,
                score: t.score,
                label: t.attachments?.mediaType,
            };
        }),

        activeIssues: monitor.getActiveIssuesByType().map((i) => ({
            type: i.type,
            key: i.key,
            openForMs: Date.now() - i.raisedAt,
        })),
    };

    dashboard.push(snapshot);
});
```

## Distinguishing screen share from camera

Tag tracks with `attachments`, then use the tag both locally and server-side.

```javascript
const camTrack = await getCameraTrack();
const screenTrack = await getDisplayTrack();

monitor.getTrackMonitor(camTrack.id).attachments    = { mediaType: "camera" };
monitor.getTrackMonitor(screenTrack.id).attachments = { mediaType: "screen-share" };
```

Two things follow from this. The default score calculator already skips bitrate-deviation and
volatility penalties when `track.contentHint === 'screen'`, so set the content hint as well:

```javascript
screenTrack.contentHint = "detail";   // or "text" / "motion"
```

And you can suppress detectors that do not make sense for that content:

```javascript
const screenMonitor = monitor.getTrackMonitor(screenTrack.id);
screenMonitor.detectors.disable("freezed-video-track-detector");   // a static slide is not a freeze
```

## React

```jsx
import { useEffect, useRef, useState } from "react";
import { ClientMonitor } from "@observertc/client-monitor-js";

export function useClientMonitor(peerConnection, { clientId, callId }) {
    const monitorRef = useRef(null);
    const [quality, setQuality] = useState({ score: 5, issues: [] });

    useEffect(() => {
        if (!peerConnection) return;

        const monitor = new ClientMonitor({
            clientId,
            callId,
            collectingPeriodInMs: 2000,
            samplingPeriodInMs: 8000,
        });
        monitorRef.current = monitor;
        monitor.addSource(peerConnection);

        monitor.on("stats-collected", () => {
            setQuality({
                score: monitor.score ?? 5,
                rttMs: (monitor.avgRttInSec ?? 0) * 1000,
                issues: monitor.getActiveIssuesByType().map((i) => i.type),
            });
        });

        monitor.on("sample-created", (sample) => {
            fetch("/api/samples", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(sample),
            }).catch(() => {});
        });

        return () => {
            monitor.close();
            monitorRef.current = null;
        };
    }, [peerConnection, clientId, callId]);

    return { quality, monitor: monitorRef };
}
```

## Express endpoint for samples

The minimal server side, before you add [`observer-js`](/docs/libraries/observer-js/).

```javascript
import express from "express";

const app = express();
app.use(express.json({ limit: "2mb" }));

app.post("/api/samples", (req, res) => {
    const sample = req.body;
    if (!sample?.clientId || !sample?.callId) return res.sendStatus(400);

    store.append(sample);           // your archive
    observer.accept(sample);        // live analysis

    res.sendStatus(200);
});
```

## Troubleshooting

{{< details "No stats are being collected" >}}
- Confirm a source was added: `monitor.peerConnections.length > 0`.
- For mediasoup, transports created **before** `addSource(device)` must be added manually.
- Check the peer connection is not already closed when you add it.
- Turn on logging (`logger: console`) — the library warns on sources it cannot poll.
{{< /details >}}

{{< details "`sample-created` never fires" >}}
- `samplingPeriodInMs` must be set for automatic sampling. It has no default.
- For manual `createSample()`, you must also set `bufferingEventsForSamples: true`.
{{< /details >}}

{{< details "Too many issues / noisy alerts" >}}
- Lower `congestionDetector.sensitivity` to `'low'`.
- Raise `dryInboundTrackDetector.thresholdInMs` / `dryOutboundTrackDetector.thresholdInMs`.
- Pass `null` for detectors you do not act on so they are never built.
- Alert on `issue-resolved` with a minimum `durationInMs` instead of on `issue` — short episodes
  are often not worth a page.
{{< /details >}}

{{< details "Scores look wrong for our product" >}}
The default model is tuned for camera-based conferencing. Set `contentHint` on screen-share
tracks, and if your product is audio-first or otherwise unusual, replace the calculator — see
[Scoring](../scoring/).
{{< /details >}}

{{< details "High CPU from monitoring" >}}
- Increase `collectingPeriodInMs` — this is the dominant cost, because it drives `getStats()`.
- Watch `monitor.durationOfCollectingStatsInMs`: if it is large, the tab is saturated for reasons
  other than the monitor, and `cpulimitation` will be telling you so.
- Remove detectors you do not use with `null`.
- Keep stats adapters cheap; move expensive work into async extension stats providers.
{{< /details >}}

{{< details "Memory growth over long calls" >}}
Call `monitor.close()` when the call ends — it releases every monitor and auto-resolves open
issues. Remove your own event listeners too if the monitor outlives your component.
{{< /details >}}

## Frequently asked

**How often should stats be collected?**
The 2 s default suits most applications. Use 1 s while debugging, 3–5 s at high scale.

**What is the difference between `collectingPeriodInMs` and `samplingPeriodInMs`?**
Collecting drives detection and metric resolution; sampling drives how much telemetry you upload.

**What is the performance impact?**
Typically under 1 % CPU. The dominant cost is the periodic `getStats()` call, which is why the
period is configurable.

**Does it work with React Native?**
It targets browsers with a standard WebRTC implementation. React Native needs WebRTC polyfills and
may hit platform-specific gaps.

**How do I handle multiple peer connections?**
Add each one as a source. Client-level metrics aggregate automatically.

**What happens when a peer connection closes?**
The monitor cleans up its monitors and emits the corresponding events. Nothing to do manually.
