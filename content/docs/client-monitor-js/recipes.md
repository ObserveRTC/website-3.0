---
title: "Recipes"
slug: "recipes"
description: "Worked integration patterns for client-monitor-js"
lead: "Copy-ready patterns for dashboards, adaptive UX, production tuning and framework integration"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 280
toc: true
---

## Production monitoring pipeline

Tuned for cost and signal quality rather than debugging resolution.

```javascript
import { ClientMonitor } from "@observertc/client-monitor-js";
import { ClientSampleEncoder } from "@observertc/samples-protobuf-codec";

// One encoder per client — it sends each sample as the delta from the previous one.
const encoder = new ClientSampleEncoder({ clientId: session.participantId });

const monitor = new ClientMonitor({
    clientId: session.participantId,
    callId: session.roomId,

    collectingPeriodInMs: 5000,     // the default; lower it to make detectors faster to judge
    samplingPeriodInMs: 10000,      // a multiple of the above — less upload volume

    congestionDetector: null,       // deprecated; take the two graded ones instead
    uplinkCongestionDetector: {},
    downlinkCongestionDetector: {},

    audioPlayoutSynthesisDetector: null,   // not acted on — don't build it

    appData: { appVersion: BUILD_VERSION },
});

monitor.attachments = {
    appVersion: BUILD_VERSION,
    region: session.region,
    tier: user.plan,
};

monitor.addSource(peerConnection);

// Ship telemetry.
monitor.on("sample-created", ({ sample }) => {
    navigator.sendBeacon(`/api/samples/${session.participantId}`, encoder.encode(sample));
});

// Route issues by how much you care.
monitor.on("issue", (issue) => {
    if (issue.type === "uplink-congestion" || issue.type === "cpulimitation") {
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

`activeIssues` is a live set, so rendering from it gives an indicator that is correct by
construction — it clears itself when the detector resolves the issue.

```javascript
const SEVERITY = {
    "uplink-congestion": "critical",
    "downlink-congestion": "critical",
    cpulimitation: "critical",
    "dry-inbound-track": "critical",
    "dry-outbound-track": "critical",
    "stuck-decoder": "critical",
    "video-flow-disrupted": "warning",
    "av-desync": "warning",
    "invented-speech": "warning",
    "pixelated-video": "warning",
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

Reacting to detector verdicts inside the client is often the highest-value use of the library — the
fix happens before the user complains.

```javascript
monitor.on("issue", async (issue) => {
    switch (issue.type) {
        case "uplink-congestion": {
            // The sending path is out of room — shed the most expensive stream first.
            await screenShare?.pause();
            ui.toast("Network is congested — screen share paused");
            break;
        }
        case "cpulimitation": {
            await sender.setParameters({
                ...sender.getParameters(),
                encodings: [{ maxBitrate: 300_000, scaleResolutionDownBy: 2 }],
            });
            break;
        }
        case "capture-source-lost": {
            // Terminal: the device is gone and the track will never produce another frame.
            ui.promptDeviceChange(issue.payload.trackId, issue.payload.deviceLabel);
            break;
        }
        case "silent-audio-source": {
            ui.toast("Your microphone is not picking anything up");
            break;
        }
        case "stuck-decoder": {
            // Per-consumer wedge — recreating the consumer is the documented remedy.
            if (issue.payload.variant === "decode") await recreateConsumer(issue.payload.trackId);
            break;
        }
    }
});

monitor.on("issue-resolved", async (resolved) => {
    if (resolved.type === "uplink-congestion") {
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
        cpuUtilization: monitor.cpuUtilization,

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
            congested: pc.congested,
            score: pc.calculatedStabilityScore?.value,
        })),

        tracks: monitor.tracks.map((t) => {
            const rtp = t.direction === "inbound" ? t.getInboundRtp() : t.highestLayer;
            return {
                id: t.track.id,
                kind: t.kind,
                direction: t.direction,
                bitrate: t.bitrate,
                fps: rtp?.ewmaFps,
                loss: t.fractionLost,
                flow: t.direction === "inbound" ? t.frameFlowState : undefined,
                score: t.calculatedScore?.value,
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

## Telling the library what the stats cannot say

Three declarations change what can be detected at all, rather than merely tuning it.

```javascript
// 1. Screen share. Nothing in getStats() reveals that an INBOUND track is a screen share,
//    and PixelatedVideoDetector refuses to judge one — a static slide legitimately spends
//    almost nothing per pixel. An undeclared screen share is judged as camera video.
monitor.setInboundTrackContext(remoteTrackId, { contentType: "screenshare" });

// Outbound is auto-detected from track.getSettings().displaySurface where the browser
// reports one; declare it where it does not. Declaring 'camera' on a genuinely moving
// captured surface opts it back into capture-bottleneck detection.
monitor.setOutboundTrackContext(screenTrack.id, { contentType: "camera" });

// 2. Lip sync. An SFU forwards audio and video as independent streams with no signalled
//    relationship, so AVDesyncPlayoutDetector reports inputsUnavailable until you pair them.
monitor.setInboundTrackContext(audioTrackId, { linkedVideoTrackId: videoTrackId });

// 3. Presented size. A blocky picture costs more full-screen than in a thumbnail.
monitor.setInboundTrackContext(remoteTrackId, { videoTag: videoElement });

// 4. Pauses. A receiver can be created ALREADY paused — a mediasoup consumer, for one — and
//    its stats appear a collection or more later, so this is declared rather than derived.
monitor.setInboundTrackContext(remoteTrackId, { paused: true });
```

Declarations **merge** and may be made before the track exists; the library applies them to
whichever peer connection first manifests the track.

## Tagging tracks for the server

```javascript
monitor.getTrackMonitor(camTrack.id).attachments    = { mediaType: "camera" };
monitor.getTrackMonitor(screenTrack.id).attachments = { mediaType: "screen-share" };

// mediasoup: what the default remote-track resolver reads server-side
monitor.getTrackMonitor(producer.track.id).attachments = { producerId: producer.id, direction: "send" };
monitor.getTrackMonitor(consumer.track.id).attachments = { consumerId: consumer.id, producerId: consumer.producerId, direction: "recv" };
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
            collectingPeriodInMs: 5000,
            samplingPeriodInMs: 5000,
            bufferClientSamplesUntilSubscriber: true,   // nothing is lost before the effect runs
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

        monitor.on("sample-created", ({ sample }) => {
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

The minimal server side, before you add [`observer-js`](/docs/observer-js/).

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
- Turn on logging — the library warns on sources it cannot poll.
{{< /details >}}

{{< details "`sample-created` never fires" >}}
- `samplingPeriodInMs` must be set for automatic sampling.
- Samples created before anything subscribed are dropped unless
  `bufferClientSamplesUntilSubscriber: true`.
- For manual `createSample()`, also set `bufferingEventsForSamples: true` — otherwise no client
  event is recorded at all between samples.
{{< /details >}}

{{< details "A detector never fires, or fires far later than expected" >}}
- Both periods default to **5000 ms** as of 4.9, and every window and tick count is measured in
  collections: `minConsecutiveTicks: 2` now covers 10 seconds, not 4. Set
  `collectingPeriodInMs: 2000` to restore 4.8 timing.
- Check `inputsUnavailable` on the detector — silence may mean "the browser reported nothing I
  need", not "nothing is wrong":
  ```javascript
  pcMonitor.detectors.getByName('transport-delay-detector')?.inputsUnavailable;
  ```
- `AVDesyncPlayoutDetector` measures nothing until `linkedVideoTrackId` is declared.
- `CongestionDetector` is permanently silent on Firefox — use the uplink/downlink pair.
{{< /details >}}

{{< details "`detectors.disable(...)` silences nothing" >}}
Lookup by `name` is exact and **there is no alias table** for the names retired in 4.9. A retired
name returns `false`. See [What changed in 4.9](../migration-4-9/#retired-detector-names), and
prefer `null` on the detector's config key when you want it never constructed at all.
{{< /details >}}

{{< details "Too many issues / noisy alerts" >}}
- Pass `null` for detectors you do not act on so they are never built.
- Raise the individual thresholds — every detector has a block of its own now, so tuning one can
  never retune a neighbour.
- Set `includeIssueInSample = false` on a detector to keep it running locally while keeping its
  findings out of the samples you upload.
- Alert on `issue-resolved` with a minimum `durationInMs` instead of on `issue` — short episodes
  are often not worth a page.
{{< /details >}}

{{< details "Scores look wrong for our product" >}}
The shipped calculator is a **reference implementation**, tuned for camera-based conferencing, and
19 of the 37 issue types carry no charge in it. Declare screen shares so they are judged
correctly, and if your product is audio-first or otherwise unusual, replace the calculator — see
[Scoring](../scoring/#writing-your-own).
{{< /details >}}

{{< details "High CPU from monitoring" >}}
- Increase `collectingPeriodInMs` — it drives `getStats()` and is the dominant cost, and it shrinks
  every window in the library at once.
- Watch `monitor.durationOfCollectingStatsInMs`: if it is large, the tab is saturated for reasons
  other than the monitor, and `cpulimitation` will be telling you so.
- Remove detectors you do not use with `null`.
- Keep stats adapters cheap; move expensive work into async extension stats providers.
{{< /details >}}

{{< details "Memory growth over long calls" >}}
Call `monitor.close()` when the call ends — it releases every monitor and auto-resolves open issues.
Remove your own event listeners too if the monitor outlives your component.
{{< /details >}}

## Frequently asked

**How often should stats be collected?**
The 5 s default suits most applications. Drop it to 1–2 s while debugging and you want a detector to
reach its verdict quickly — every window and tick count is measured in collections, so a shorter
period makes the whole library faster to judge at the cost of more `getStats()` calls.

**What is the difference between `collectingPeriodInMs` and `samplingPeriodInMs`?**
Collecting drives detection and metric resolution; sampling drives how much telemetry you upload.
Keep sampling a multiple of collecting, or the interval between samples drifts.

**How do I reduce bandwidth?**
Encode the samples — both codecs delta-encode against the previous sample, which is where nearly all
of the saving is. Beyond that, `sendScoreReasonsToServer: false` and
`sendResolvedIssuesToServer: false` drop the two optional parts of a sample without changing any
score.

**What is the performance impact?**
Typically under 1% CPU. The dominant cost is the periodic `getStats()` call.

**Does it work with React Native?**
It targets browsers with a standard WebRTC implementation. React Native needs WebRTC polyfills and
may hit platform-specific gaps.

**What happens when a peer connection closes?**
The monitor cleans up its monitors and emits the corresponding events. Nothing to do manually.
