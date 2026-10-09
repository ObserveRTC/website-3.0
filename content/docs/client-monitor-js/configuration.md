---
slug: "configuration"
title: "Configuration"
description: "Use verified defaults and complete detector overrides."
lead: "Use verified defaults and complete detector overrides."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 20
toc: true
---
Configuration controls how often the monitor reads statistics, which problems it detects, and what it includes in samples. Start with the defaults, then change settings for a concrete requirement: faster local feedback, less traffic, or a detector that needs different thresholds for your product.

## Configure a monitor

```javascript
const monitor = new ClientMonitor({
  clientId: 'participant-42',
  callId: 'room-123',
  collectingPeriodInMs: 1000,
  samplingPeriodInMs: 5000,
  congestionDetector: null,
});
```

This example collects every second, sends a sample every five seconds, and disables the deprecated congestion detector. It leaves the other detectors at their defaults. Faster collection increases the work done by `getStats()` and changes how much time a detection window covers.

## Identity and local application data

| Option | What it is for |
|---|---|
| `clientId` | Identify this monitored endpoint. Supply an application identifier when sending to Observer. |
| `callId` | Group this endpoint with other clients in the same call. Required for Observer ingestion. |
| `appData` | Keep application-owned working state locally. Use serializable `attachments` for data that should be sent. |
| `logger` | Route monitor diagnostics through your application logger. |

## Collection and sample settings

| Option | Default | What changes when you set it |
|---|---|---|
| `collectingPeriodInMs` | `5000` | Time between browser-stat updates. `0` disables automatic collection. |
| `samplingPeriodInMs` | `5000` | Requested interval for creating samples. Use a multiple of collection cadence; `0` disables automatic sampling. |
| `bufferingEventsForSamples` | `false` | Retain discrete records for manual samples when automatic sampling is off. |
| `bufferClientSamplesUntilSubscriber` | `false` | Keep samples until the first sample listener attaches. Prefer attaching listeners early. |

See [collection and sampling](/docs/client-monitor-js/sampling/) for manual collection and sample boundaries.

## Browser integration settings

| Option | Default | Purpose |
|---|---|---|
| `integrateNavigatorMediaDevices` | `true` | Follow media-device activity. Can also receive a `MediaDevices` instance. |
| `watchTabVisibility` | `true` | Track whether the tab is hidden so detectors can account for browser throttling. |
| `addClientJointEventOnCreated` | `true` | Record the client's join when the monitor is created. The API spelling is `Joint`. |
| `addClientLeftEventOnClose` | `true` | Record departure when the monitor closes. |

## Sample detail settings

| Option | Default | Purpose |
|---|---|---|
| `sendResolvedIssuesToServer` | `true` | Include keyed raises and resolutions so a backend can maintain active issue state. |
| `sendScoreReasonsToServer` | `true` | Include peer-connection and track penalty breakdowns. Scores remain available when disabled. |
| `sendSdpMetadataToServer` | `false` | Opt in to sending session descriptions as metadata, with ICE passwords redacted. SDP-derived monitor fields remain available when disabled. |
| `sendIceTransportMetadataOnChangeOnly` | `true` | Send mostly static transport metadata initially and on change rather than repeating it in every sample. |

## How detection windows work

A single bad measurement can be a brief fluctuation. Detection windows keep a recent sequence of measurements so detectors can judge sustained behavior. Recovery windows let them check whether a problem has settled before clearing it. These windows hold **collected values**, not outgoing samples.

With the default five-second collection interval, three values span two intervals, or about **10 seconds** between the oldest and newest value. Four values span about **15 seconds**. Collecting every second shortens those spans to two and three seconds. A detector can also use an independent time threshold or require other evidence, so these spans are not promises of an exact alert delay.

| Window option | Detection values | Recovery values | Applies to |
|---|---|---|---|
| `clientWindow` | 3 | 3 | Measurements of the overall client. |
| `peerConnectionWindow` | 3 | 3 | Measurements of an individual connection. |
| `outboundTrackWindow` | 3 | 3 | Sending/capture measurements for a track. |
| `inboundTrackWindow` | 3 | 3 | Receiving/playout measurements for a track. Also has `flowDetection: 4` and `flowRecovery: 3` for media-flow evaluation. |

`maxAllowedGapInMs` defaults to four times a positive collection interval (20 seconds at the normal cadence). A gap larger than this prevents stale measurements from being treated as a continuous run. Think of a laptop waking from sleep: measurements before sleep should not be joined to the first measurement after wake as if the call had been continuously observed.

```javascript
const monitor = new ClientMonitor({
  collectingPeriodInMs: 1000,
  inboundTrackWindow: {
    numberOfSamples: {
      detection: 3,
      recovery: 3,
      flowDetection: 4,
      flowRecovery: 3,
    },
    maxAllowedGapInMs: 4000,
  },
});
```

Supply the complete window object when overriding it. Tune against real sessions: shorter windows respond sooner but can react to transient fluctuations; longer windows need more evidence and react later.

## Enable, disable, or tune a detector

| Supplied value | Result |
|---|---|
| Omitted or `undefined` | Use the built-in configuration. |
| `null` | Disable this detector. |
| Configuration object | Replace its default object with your object. |

Nested objects are not deep-merged. Copy the complete detector configuration before changing a threshold; `{}` is only appropriate when that detector has no required tunables. `BlockedInboundMediaDetector` is off by default because its evidence is not generally available with browser RTCP multiplexing. The deprecated `CongestionDetector` remains enabled by default in 4.10.1.

## Detector option reference

The table below lists every detector option and its complete default settings in **Client Monitor 4.10.1**. Values ending in `InMs` are milliseconds; ratios are fractions unless the detector guide states otherwise. Use the [detector catalog](/docs/client-monitor-js/detectors/) to understand the evidence before tuning a number. Newer installed versions can add or change options; their TypeScript configuration is the authority for that version.

| Option | Default settings |
|---|---|
| `iceReachabilityDetector` | `thresholdInMs: 6000` |
| `iceTraversalDetector` | `No thresholds` |
| `icePathEstablishmentDetector` | `thresholdInMs: 5000`; `createEvent: true` |
| `iceEstablishmentFailedDetector` | `thresholdInMs: 15000` |
| `dtlsHandshakeFailedDetector` | `No thresholds` |
| `dtlsHandshakeStalledDetector` | `stalledThresholdInMs: 6000` |
| `iceDisconnectedDetector` | `disconnectedThresholdInMs: 5000` |
| `iceConnectionFailedDetector` | `No thresholds` |
| `iceTransportStalledDetector` | `transportStallThresholdInMs: 5000` |
| `unstableIcePathDetector` | `pathSwitchWindowInMs: 30000`; `pathSwitchThreshold: 3` |
| `iceRestartDetector` | `createEvent: true` |
| `iceRestartRecommendationDetector` | `createEvent: true`; `iceRestartRecommendationThresholdInMs: 10000`; `iceRestartRecommendationCooldownInMs: 15000`; `restartRecommendationThresholdInMs: 10000`; `restartRecommendationCooldownInMs: 15000` |
| `congestionDetector` | `sensitivity: 'medium' as const` |
| `uplinkCongestionDetector` | `minSeverity: 0.65`; `pacerBloatingSaturatesAt: 4` |
| `downlinkCongestionDetector` | `minSeverity: 0.65`; `bufferBloatingSaturatesAt: 4` |
| `transportDelayDetector` | `thresholdInMs: 300`; `recoveryThresholdInMs: 200` |
| `transportLossDetector` | `threshold: 0.05`; `recoveryThreshold: 0.01`; `durationInMs: 6000` |
| `blockedStunRequestsDetector` | `responseReceivedTimeoutInMs: 10000`; `requestsSentTimeoutInMs: 10000` |
| `blockedOutboundMediaDetector` | `thresholdInMs: 10000` |
| `blockedInboundMediaDetector` | `null` |
| `captureSourceLostDetector` | `createEvent: true` |
| `silentAudioSourceDetector` | `silenceThresholdInMs: 60000`; `silenceRmsThreshold: 0.0001`; `recoveryRmsThreshold: 0.0003` |
| `loopbackAudioInputDetector` | Built-in loopback-device label patterns; see the [release configuration source](https://github.com/ObserveRTC/client-monitor-js/blob/4ae541eac3305d1cc779ff6dd703211e837a7f7b/src/ClientMonitor.ts) for the array |
| `videoCaptureBottleneckDetector` | `produceDegradationThreshold: 0.2` |
| `encoderBottleneckDetector` | `encodeDegradationThreshold: 0.3` |
| `rtpSenderStalledDetector` | `thresholdInMs: 4000` |
| `dryOutboundTrackDetector` | `thresholdInMs: 5000` |
| `transportDemuxStalledDetector` | `thresholdInMs: 4000`; `minTransportReceiveBitrateBps: 20000` |
| `dryInboundTrackDetector` | `thresholdInMs: 5000` |
| `frameAssemblyStalledDetector` | `thresholdInMs: 3000`; `minPacketsReceived: 20` |
| `decoderBottleneckDetector` | `decodeDegradationThreshold: 0.1`; `minReceivedFps: 5` |
| `decoderPerformanceDetector` | `decodeTimeBudgetRatio: 0.8`; `minFramesReceived: 10`; `quietLossThreshold: 0.02`; `minConsecutiveTicks: 2` |
| `stuckDecoderDetector` | `thresholdInMs: 4000`; `rttMultiplier: 15`; `minBitrate: 10000`; `minPliCount: 2` |
| `playoutDiscrepancyDetector` | `lowSkewRatio: 0.1`; `highSkewRatio: 0.25`; `minFramesReceived: 10` |
| `videoRecoveryFailedDetector` | `recoveryFailedThresholdInMs: 5000`; `recoveryFailedMinPliCount: 2` |
| `cpuPerformanceDetector` | `utilizationThreshold: 0.5`; `recoveryThreshold: 0.4` |
| `pixelatedVideoDetector` | `threshold: 0.62`; `recoveryThreshold: 0.52`; `durationInMs: 8000` |
| `inboundVideoFlowStateDetector` | `frozenAfterInMs: 2000`; `minFreezeCountForChoppy: 2` |
| `concealedSamplesDetector` | `allowedConcealedRatio: 0.05`; `raiseAfterConcealedMs: 400` |
| `audioInterruptionDetector` | `allowedInterruptedRatio: 0.02`; `raiseAfterInterruptedMs: 500` |
| `audioPlayoutSynthesisDetector` | `synthesizedRatioThreshold: 0.05`; `createEvent: true` |
| `avDesyncPlayoutDetector` | `audioAheadRaiseInMs: 90`; `audioAheadResolveInMs: 45`; `audioBehindRaiseInMs: 185`; `audioBehindResolveInMs: 125`; `sustainForInMs: 3000` |
| `jitterBufferStressDetector` | `targetDelayThresholdInMs: 200`; `timeStretchThreshold: 0.02`; `minConsecutiveTicks: 2`; `unbearableTargetDelayInMs: 1000`; `unbearableTimeStretchRate: 0.15` |
| `captureTrackMutedDetector` | `createEvent: true` |
| `codecChangeDetector` | `createEvent: true` |
| `videoResolutionChangeDetector` | `createEvent: true` |
| `simulcastLayerDetector` | `createEvent: true` |
| `statsGapDetector` | `gapRatioThreshold: 2`; `minGapInMs: 5000`; `createEvent: true` |

[Detailed detector types and implementation evidence](/reference/detector-implementation-reference.md).

Sources: [ClientMonitor constructor](https://github.com/ObserveRTC/client-monitor-js/blob/4ae541eac3305d1cc779ff6dd703211e837a7f7b/src/ClientMonitor.ts), [ClientMonitorConfig](https://github.com/ObserveRTC/client-monitor-js/blob/4ae541eac3305d1cc779ff6dd703211e837a7f7b/src/ClientMonitorConfig.ts), [Detectors](https://github.com/ObserveRTC/client-monitor-js/blob/4ae541eac3305d1cc779ff6dd703211e837a7f7b/src/detectors/Detectors.ts).
