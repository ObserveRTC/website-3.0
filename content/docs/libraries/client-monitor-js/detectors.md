---
title: "Detectors"
slug: "detectors"
description: "Built-in anomaly detectors and how to write your own"
lead: "The seven detectors that ship with the library, what triggers them, and the registry API for controlling them"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 313
toc: true
---

A **detector** runs once per collecting period, looks at the derived metrics on the monitor it is
attached to, and raises or resolves an [issue](../events-and-issues/). Detectors live at the level
where the evidence is: freeze detection on an inbound video track, congestion on a peer
connection, CPU pressure at the client level.

{{< callout context="tip" title="Why detectors instead of raw thresholds" icon="rocket" >}}
Every built-in detector uses **hysteresis** — a threshold to turn on and a different, lower
threshold to turn off — and most require corroborating signals. That is what makes the resulting
issue worth alerting on: a single unlucky stats tick will not produce one, and the issue does not
flap on and off while the condition persists.
{{< /callout >}}

## Built-in detectors

### CongestionDetector

Network is being asked for more than it can deliver.

- **Attached to:** peer connection
- **Issue type:** `congestion` · **Event:** `'congestion'`
- **Triggers on:** available bandwidth (from the selected ICE candidate pair) falling below the
  sending/receiving bitrate, plus a sensitivity-specific corroborating signal
- **Resolves when:** the bandwidth limitation clears

```javascript
congestionDetector: {
    sensitivity: "medium",   // 'low' | 'medium' | 'high'
}
```

`sensitivity` controls how much corroboration is required before the issue is raised. `'low'`
raises only on strong, sustained evidence; `'high'` reacts faster and produces more issues.

Payload: `CongestionIssuePayload` — carries `peerConnectionId`, the available incoming/outgoing
bitrates, and (on resolution) `durationInMs`.

### CpuPerformanceDetector

The endpoint's CPU is the bottleneck, not the network.

- **Attached to:** client
- **Issue type:** `cpulimitation` · **Event:** `'cpulimitation'`
- **Triggers on:** any of —
  - an outbound RTP stream reporting `qualityLimitationReason === 'cpu'`
  - the **inbound decoded-to-received frames ratio** dropping below `alertOn` (frames arrive but
    the decoder cannot keep up)
  - stats collection itself taking longer than `highWatermark` (the main thread is saturated)

```javascript
cpuPerformanceDetector: {
    incomingDecodedFramesRatioThresholds: {
        alertOn: 0.7,          // alert when <70% of received frames get decoded
        alertOff: 0.85,        // clear once ≥85% are decoded again
        minReceivedFrames: 10, // ignore intervals with too few frames to judge
    },
    durationOfCollectingStatsThreshold: {
        lowWatermark: 5000,
        highWatermark: 10000,
    },
}
```

{{< callout context="note" title="Why not frame-rate volatility?" icon="info-circle" >}}
Earlier versions inferred decode-side CPU pressure from fps volatility. That false-triggered on
screen share, whose frame rate legitimately swings (15 → 1 fps when the shared content goes
static). The decoded/received ratio is robust to this: when fps drops legitimately, *received* and
*decoded* frames drop together and the ratio stays near 1.0. An alert only fires when frames are
received but not decoded.
{{< /callout >}}

### AudioDesyncDetector

Audio is being time-stretched to stay in sync with video.

- **Attached to:** inbound audio track
- **Issue type:** `audio-desync` · **Event:** `'audio-desync-track'`
- **Triggers on:** the fraction of accelerated/decelerated samples crossing the on-threshold
- **Resolves when:** it falls back below the off-threshold

```javascript
audioDesyncDetector: {
    fractionalCorrectionAlertOnThreshold: 0.1,
    fractionalCorrectionAlertOffThreshold: 0.05,
}
```

### FreezedVideoTrackDetector

Video stopped moving.

- **Attached to:** inbound video track
- **Issue type:** `freezed-video-track` · **Event:** `'freezed-video-track'`
- **Triggers on:** the browser's `freezeCount` increasing
- **Resolves when:** no new freezes for one collection tick

```javascript
videoFreezesDetector: {}
```

### DryInboundTrackDetector / DryOutboundTrackDetector

A track that has stopped moving bytes in either direction.

- **Attached to:** inbound / outbound track
- **Issue types:** `dry-inbound-track`, `dry-outbound-track`
- **Triggers on:** byte counters flat for `thresholdInMs`
- **Resolves when:** bytes start flowing again

```javascript
dryInboundTrackDetector:  { thresholdInMs: 5000 },
dryOutboundTrackDetector: { thresholdInMs: 5000 },
```

A dry **outbound** track usually means a local capture problem — a camera taken by another app, a
muted device, an encoder that died. A dry **inbound** track is ambiguous from the browser alone;
[`observer-js`](/docs/libraries/observer-js/detectors/) resolves that ambiguity by joining the two
ends of the track server-side.

### PlayoutDiscrepancyDetector

Frames are arriving and decoding, but not reaching the screen.

- **Attached to:** inbound video track
- **Issue type:** `inbound-video-playout-discrepancy` · **Event:** `'inbound-video-playout-discrepancy'`
- **Triggers on:** `framesReceived - framesRendered > highSkewThreshold`
- **Resolves when:** the skew drops below `lowSkewThreshold`

```javascript
playoutDiscrepancyDetector: {
    lowSkewThreshold: 2,
    highSkewThreshold: 5,
}
```

Typical causes are a hidden or detached `<video>` element, a throttled background tab, or a
rendering pipeline that cannot keep up.

### SynthesizedSamplesDetector

The audio playout path is inventing samples to cover gaps.

- **Attached to:** media playout
- **Triggers on:** synthesized-sample duration exceeding the threshold

```javascript
syntheticSamplesDetector: {
    minSynthesizedSamplesDuration: 1000,
}
```

### LongPcConnectionEstablishmentDetector

ICE/DTLS negotiation is taking too long.

- **Attached to:** peer connection
- **Triggers on:** connection establishment exceeding `thresholdInMs`

```javascript
longPcConnectionEstablishmentDetector: {
    thresholdInMs: 5000,
}
```

Slow establishment is a strong early signal for firewall/TURN problems — it is visible before any
media flows at all.

## Which detector is attached where

```text
ClientMonitor
├── CpuPerformanceDetector
├── PeerConnectionMonitor
│   ├── CongestionDetector
│   └── LongPcConnectionEstablishmentDetector
├── InboundTrackMonitor
│   ├── AudioDesyncDetector            (audio)
│   ├── FreezedVideoTrackDetector      (video)
│   ├── PlayoutDiscrepancyDetector     (video)
│   └── DryInboundTrackDetector
├── OutboundTrackMonitor
│   └── DryOutboundTrackDetector
└── MediaPlayoutMonitor
    └── SynthesizedSamplesDetector
```

Each of these levels exposes its own `detectors` registry.

## The `Detectors` registry

`monitor.detectors`, `peerConnectionMonitor.detectors`, `inboundTrackMonitor.detectors`,
`outboundTrackMonitor.detectors` and `mediaPlayoutMonitor.detectors` are all instances of the same
small collection:

```typescript
// Inspection
detectors.size;                       // how many are attached
detectors.listOfNames;                // string[]
detectors.has(name);                  // boolean
detectors.getByName(name);            // Detector | undefined
detectors.getByName<CpuPerformanceDetector>("cpu-performance-detector");
detectors.find(pred);                 // first match
detectors.filter(pred);               // all matches
for (const d of detectors) { /* … */ }

// Mutation
detectors.add(detector);
detectors.remove(detector);
detectors.clear();

// Runtime toggle
detectors.disable(name);              // detector stays attached, update() is skipped
detectors.enable(name);
detectors.isEnabled(name);            // attached AND not disabled
detectors.disableAll();
detectors.enableAll();
```

### Common patterns

```javascript
// Silence one detector instance-wide.
monitor.detectors.disable("cpu-performance-detector");

// Silence congestion alerts across every peer connection.
for (const pc of monitor.mappedPeerConnections.values()) {
    pc.detectors.disable("congestion-detector");
}

// Turn a track-level detector off for a track your app knows is intentionally static.
inboundTrackMonitor.detectors.disable("freezed-video-track-detector");

// Suspend everything during a known-noisy state (e.g. a deliberate renegotiation), then restore.
monitor.detectors.disableAll();
// …later
monitor.detectors.enableAll();
```

{{< callout context="tip" title="Disable vs never construct" icon="rocket" >}}
`detectors.disable(name)` keeps the instance and its state, so re-enabling resumes cleanly — use
it for temporary suspension. Passing `null` in the [configuration](../configuration/) means the
detector is never built at all, which is what you want when you have decided your application does
not care about that condition.
{{< /callout >}}

## Writing a custom detector

A detector is any object with a `name` and an `update()` method. Implement `Detector`, raise
stateful issues with a key you control, and resolve them when the condition clears.

```typescript
import { Detector, ClientMonitor } from "@observertc/client-monitor-js";

class SilentMicDetector implements Detector {
    public readonly name = "silent-mic-detector";
    public disabled = false;               // honoured by Detectors.update()

    private startedAt?: number;
    private readonly key = "silent-mic";

    constructor(private readonly monitor: ClientMonitor) {}

    public update(): void {
        if (this.disabled) return;

        const mic = this.monitor.tracks.find(
            (t) => t.direction === "outbound" && t.kind === "audio",
        );
        if (!mic) return;

        const source = mic.getOutboundRtps()?.[0]?.getMediaSource();
        const silent = (source?.audioLevel ?? 1) < 0.001;

        if (silent && !this.startedAt) {
            this.startedAt = Date.now();
            this.monitor.raiseIssue(this.key, {
                type: "silent-mic",
                payload: { trackId: mic.track.id, audioLevel: source?.audioLevel },
            });
        } else if (!silent && this.startedAt) {
            this.monitor.resolveIssue(this.key, {
                comment: "audio level recovered",
                payload: { durationInMs: Date.now() - this.startedAt },
            });
            this.startedAt = undefined;
        }
    }
}

monitor.detectors.add(new SilentMicDetector(monitor));
```

Three conventions worth copying from the built-ins:

1. **`disabled` is a public field.** Check it at the top of `update()` so direct invocations behave
   the same as registry-driven ones.
2. **The detector owns the episode.** Track your own `startedAt` and enrich the resolution payload
   with `durationInMs` so consumers do not have to correlate raise and resolve themselves.
3. **Pick a stable key.** The built-in convention is `${type}-${scope}` — e.g.
   `congestion-pc-${peerConnectionId}`, `audio-desync-track-${trackId}`. One key per logical
   incident.

### Attaching to a lower level

Custom detectors do not have to live on the client. Attach one to each new peer connection or
track to get per-entity state for free:

```javascript
monitor.on("stats-collected", () => {
    for (const pc of monitor.peerConnections) {
        if (!pc.detectors.has("my-pc-detector")) {
            pc.detectors.add(new MyPcDetector(pc, monitor));
        }
    }
});
```

## Detector-specific events

Alongside the generic `'issue'` event, each built-in detector emits a named event once per
episode. Use these when you want to react to one specific condition without switching on `type`:

```javascript
monitor.on("congestion",                        (e) => { /* … */ });
monitor.on("cpulimitation",                     (e) => { /* … */ });
monitor.on("audio-desync-track",                (e) => { /* … */ });
monitor.on("freezed-video-track",               (e) => { /* … */ });
monitor.on("dry-inbound-track",                 (e) => { /* … */ });
monitor.on("dry-outbound-track",                (e) => { /* … */ });
monitor.on("inbound-video-playout-discrepancy", (e) => { /* … */ });
```
