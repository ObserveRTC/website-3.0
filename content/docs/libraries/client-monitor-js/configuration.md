---
title: "Configuration"
slug: "configuration"
description: "Every ClientMonitor configuration option with defaults"
lead: "The full ClientMonitorConfig surface — timing, integration flags, detector thresholds and application data"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 312
toc: true
---

Every option is optional. `new ClientMonitor()` with no arguments is valid and gives you sensible
defaults with all detectors enabled.

## The full object

```javascript
import { ClientMonitor } from "@observertc/client-monitor-js";

const monitor = new ClientMonitor({
    // ── Identity ────────────────────────────────────────────────────────────
    clientId: "unique-client-id",
    callId: "unique-call-id",

    // ── Timing ──────────────────────────────────────────────────────────────
    collectingPeriodInMs: 2000,   // default: 2000 — how often getStats() runs
    samplingPeriodInMs: 4000,     // no default — omit to disable automatic sampling

    // ── Integration flags ───────────────────────────────────────────────────
    integrateNavigatorMediaDevices: true,  // default: true
    addClientJointEventOnCreated: true,    // default: true
    addClientLeftEventOnClose: true,       // default: true
    bufferingEventsForSamples: false,      // default: false — required for manual sampling

    // ── Detectors ───────────────────────────────────────────────────────────
    audioDesyncDetector: {
        fractionalCorrectionAlertOnThreshold: 0.1,
        fractionalCorrectionAlertOffThreshold: 0.05,
    },
    congestionDetector: {
        sensitivity: "medium",              // 'low' | 'medium' | 'high'
    },
    cpuPerformanceDetector: {
        incomingDecodedFramesRatioThresholds: {
            alertOn: 0.7,
            alertOff: 0.85,
            minReceivedFrames: 10,
        },
        durationOfCollectingStatsThreshold: {
            lowWatermark: 5000,
            highWatermark: 10000,
        },
    },
    dryInboundTrackDetector:  { thresholdInMs: 5000 },
    dryOutboundTrackDetector: { thresholdInMs: 5000 },
    videoFreezesDetector: {},
    playoutDiscrepancyDetector: {
        lowSkewThreshold: 2,
        highSkewThreshold: 5,
    },
    syntheticSamplesDetector: {
        minSynthesizedSamplesDuration: 1000,
    },
    longPcConnectionEstablishmentDetector: {
        thresholdInMs: 5000,
    },

    // ── Logging ─────────────────────────────────────────────────────────────
    logger: myLogger,

    // ── Application data (never shipped in samples) ──────────────────────────
    appData: { userId: "user-123", roomId: "room-456" },
});
```

## Timing

| Option | Default | Meaning |
|---|---|---|
| `collectingPeriodInMs` | `2000` | How often `getStats()` is polled on every source. Drives all derived metrics, detectors and scores. |
| `samplingPeriodInMs` | *(none)* | How often a [`ClientSample`](/docs/schema/clientsample/) is created and `sample-created` fires. Omit it to disable automatic sampling. |

{{< callout context="tip" title="Choosing periods" icon="rocket" >}}
`collectingPeriodInMs` controls **resolution** — how quickly a detector can notice something.
`samplingPeriodInMs` controls **bandwidth** — how much telemetry you upload.

- Interactive debugging: `1000` / `2000`
- Default production: `2000` / `4000`
- High-scale, cost-sensitive: `3000` / `10000`

Sampling less often does not lose issues: events and issues are buffered between samples and all
of them ship in the next one.
{{< /callout >}}

Both can be changed while running:

```javascript
monitor.setCollectingPeriod(3000);
monitor.setSamplingPeriod(10000);
```

## Integration flags

| Option | Default | Effect |
|---|---|---|
| `integrateNavigatorMediaDevices` | `true` | Watches `navigator.mediaDevices` and records device lists / changes as client metadata. |
| `addClientJointEventOnCreated` | `true` | Emits a `CLIENT_JOINED` client event when the monitor is created. `observer-js` uses this to set `joinedAt`. |
| `addClientLeftEventOnClose` | `true` | Emits `CLIENT_LEFT` on `close()`. |
| `bufferingEventsForSamples` | `false` | Buffers events/issues even when automatic sampling is off. **Required if you call `createSample()` manually.** |

## Detector configuration: the three-state rule

Every detector slot in `ClientMonitorConfig` is typed `Config | null`, and the value you pass
decides whether the detector exists at all:

| You pass | Result |
|---|---|
| *(key omitted)* or `undefined` | Detector is constructed with its documented defaults |
| An object | Detector is constructed with your overrides merged in |
| `null` | Detector is **not constructed at all** — no instance, no per-tick work |

```javascript
const monitor = new ClientMonitor({
    congestionDetector: null,                    // never built
    videoFreezesDetector: {},                    // built with defaults
    dryInboundTrackDetector: { thresholdInMs: 10_000 },  // built with an override
    // cpuPerformanceDetector omitted             → built with defaults
});
```

Once constructed, a detector can also be silenced without being removed:

```javascript
monitor.detectors.disable("cpu-performance-detector");
monitor.detectors.enable("cpu-performance-detector");
monitor.detectors.disableAll();
```

See [Detectors](../detectors/) for the registry API and every threshold's meaning.

{{< callout context="caution" title="Removed in 4.3.0" icon="alert-triangle" >}}
`createIssue?: boolean` and `disabled?: boolean` were removed from every detector's config block.
Use `null` (do not construct) or the runtime `detector.disabled` flag instead.
{{< /callout >}}

## Detector thresholds at a glance

| Config key | Detector | Key thresholds |
|---|---|---|
| `audioDesyncDetector` | Audio desync | `fractionalCorrectionAlertOnThreshold` `0.1`, `fractionalCorrectionAlertOffThreshold` `0.05` |
| `congestionDetector` | Congestion | `sensitivity`: `'low'` \| `'medium'` \| `'high'` |
| `cpuPerformanceDetector` | CPU pressure | `incomingDecodedFramesRatioThresholds` `{ alertOn: 0.7, alertOff: 0.85, minReceivedFrames: 10 }`; `durationOfCollectingStatsThreshold` `{ lowWatermark: 5000, highWatermark: 10000 }` |
| `dryInboundTrackDetector` | Inbound track stalled | `thresholdInMs` `5000` |
| `dryOutboundTrackDetector` | Outbound track stalled | `thresholdInMs` `5000` |
| `videoFreezesDetector` | Video freeze | *(no thresholds — driven by `freezeCount`)* |
| `playoutDiscrepancyDetector` | Frames received but not rendered | `lowSkewThreshold` `2`, `highSkewThreshold` `5` |
| `syntheticSamplesDetector` | Audio being synthesized | `minSynthesizedSamplesDuration` `1000` |
| `longPcConnectionEstablishmentDetector` | Slow ICE/DTLS setup | `thresholdInMs` `5000` |

{{< callout context="caution" title="Migrating from ≤ 4.3.1" icon="alert-triangle" >}}
`cpuPerformanceDetector.fpsVolatilityThresholds` was **replaced** by
`incomingDecodedFramesRatioThresholds` in `4.3.2`. Frame-rate volatility false-triggered on screen
share, whose fps legitimately swings when the shared content goes static. If you still pass
`fpsVolatilityThresholds`, update your config.
{{< /callout >}}

## `appData` vs `attachments`

Two different bags, on every monitor object in the hierarchy, with opposite purposes:

| | `appData` | `attachments` |
|---|---|---|
| Included in `ClientSample` | **No** | **Yes** |
| Reaches your backend | No | Yes |
| Costs bandwidth / storage | No | Yes |
| Intended for | Local UI state, feature flags, runtime routing | Session identity, room context, A/B flags, custom metrics |

```javascript
// Local only.
trackMonitor.appData = { renderTargetId: "video-el-7", muteRequested: false };

// Shipped with every sample and readable server-side.
trackMonitor.attachments = { roomId: "room-456", role: "presenter", mediaType: "screen-share" };
```

Both exist on `ClientMonitor`, `PeerConnectionMonitor`, every track monitor, every RTP monitor and
every connection monitor.

## Minimal configurations

```javascript
// Only what you need to correlate samples.
const monitor = new ClientMonitor({ clientId: "my-client", collectingPeriodInMs: 1000 });

// Everything default — useful for local debugging with no backend.
const monitor = new ClientMonitor();
```
