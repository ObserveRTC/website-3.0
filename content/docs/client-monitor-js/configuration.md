---
title: "Configuration"
description: "Every client-monitor-js option and detector block, with defaults"
lead: "65 keys: 46 detector blocks, four shared windows, and the basics"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 220
toc: true
---

`ClientMonitorConfig` is entirely optional — `new ClientMonitor()` runs on defaults. Every detector
reads a block **named after itself**, its `name` in camelCase, and reads nothing else.

{{< callout context="tip" title="The null / undefined / object rule" icon="rocket" >}}
- **Omit the key** (or pass `undefined`) → defaults applied.
- **Pass an object** → detector enabled with your overrides.
- **Pass `null`** → the detector is **not constructed at all** — no memory, no `update()` ticks.

`null` is not the same as `disabled: true`. The config entry decides whether the class exists;
`disabled` is a runtime flag on the instance.
{{< /callout >}}

## The basics

```javascript
const monitor = new ClientMonitor({
    clientId: "unique-client-id",
    callId: "unique-call-id",
    collectingPeriodInMs: 5000,   // default 5000
    samplingPeriodInMs: 5000,     // default 5000; keep it a multiple of the above

    // Integration settings
    integrateNavigatorMediaDevices: true,      // default true
    watchTabVisibility: true,                  // default true — off, `activeTab` stays true
    addClientJointEventOnCreated: true,        // default true
    addClientLeftEventOnClose: true,           // default true
    bufferingEventsForSamples: false,          // default false
    bufferClientSamplesUntilSubscriber: false, // default false — replay to the first listener
    logger: undefined,                         // default: warn/error to console, rest no-op

    // What leaves for the server. None of these change a score or an event.
    sendScoreReasonsToServer: true,             // false drops scoreReasons from samples
    sendResolvedIssuesToServer: true,           // false ships raises only, with no `key`
    sendIceTransportMetadataOnChangeOnly: true, // static ICE transport members on change only

    appData: { userId: "user-123", roomId: "room-456" },
});
```

{{< callout context="caution" title="Both periods default to 5000 as of 4.9" icon="alert-triangle" >}}
They were 2000 and 8000. `getStats()` is not free and the previous default paid for it two and a
half times over on every call. The two now match, so a sample is created on every collection and the
interval between samples cannot drift — the sampling period should always be a **multiple** of the
collecting period, and the monitor warns when it is not.

Every window and tick count in the library is measured in collections, so this default also makes
tick-counting detectors 2.5× slower to fire in wall-clock terms. Pass `collectingPeriodInMs: 2000`
to restore 4.8 timing throughout.
{{< /callout >}}

## Shared windows

Window sizes, shared by every detector bound to that level, so detectors judging the same thing
judge the same stretch of time. Counted **in values, not milliseconds**: N values span N−1
collecting intervals. These replaced the per-detector `durationInMs` keys in 4.9.

```javascript
{
    clientWindow:         { numberOfSamples: { detection: 3, recovery: 3 }, maxAllowedGapInMs: 20000 },
    inboundTrackWindow:   { numberOfSamples: { detection: 3, recovery: 3, flowDetection: 4, flowRecovery: 3 }, maxAllowedGapInMs: 20000 },
    outboundTrackWindow:  { numberOfSamples: { detection: 3, recovery: 3 }, maxAllowedGapInMs: 20000 },
    peerConnectionWindow: { numberOfSamples: { detection: 3, recovery: 3 }, maxAllowedGapInMs: 20000 },
}
```

Each window is published as `slicedWindow` on its monitor. A **recovery** slice is the stretch
*before* the detection window: a finding resolves only when both read healthy, which is what stops
a condition hovering at a threshold from turning one continuous fault into a stream of short
episodes.

## Connectivity detectors

```javascript
{
    iceReachabilityDetector: {
        thresholdInMs: 6000,          // grace for `new`/`connecting` with zero local candidates
    },
    iceTraversalDetector: {},         // telemetry, nothing to tune: `{}` enables, `null` disables
    icePathEstablishmentDetector: {
        thresholdInMs: 5000,          // how long `connecting` may last before it is reported
        createEvent: true,
    },
    iceEstablishmentFailedDetector: {
        thresholdInMs: 15000,         // well past the slow-establishment threshold, on purpose
    },
    dtlsHandshakeFailedDetector: {},  // `dtlsState: 'failed'` is terminal — no threshold
    dtlsHandshakeStalledDetector: {
        stalledThresholdInMs: 6000,   // ICE healthy but DTLS still new/connecting for this long
    },
    iceDisconnectedDetector: {
        disconnectedThresholdInMs: 5000,  // how long `disconnected` may self-heal
    },
    iceConnectionFailedDetector: {},  // ICE never self-heals from `failed`
    iceTransportStalledDetector: {
        transportStallThresholdInMs: 5000,  // sending but receiving nothing for this long
    },
    unstableIcePathDetector: {
        pathSwitchWindowInMs: 30000,  // window for counting selected-path switches
        pathSwitchThreshold: 3,       // switches in that window => unstable path
    },
    iceRestartDetector: {
        createEvent: true,
    },
    iceRestartRecommendationDetector: {
        createEvent: true,
        iceRestartRecommendationThresholdInMs: 10000, // per transport: disconnected / stalled
        iceRestartRecommendationCooldownInMs: 15000,  // min gap between those recommendations
        restartRecommendationThresholdInMs: 10000,    // per pc: never established at all
        restartRecommendationCooldownInMs: 15000,
    },
}
```

All four recommendation conditions live in one block, thresholds and cooldowns included. They are
its own rather than borrowed from the detectors that raise the corresponding issues, so disabling
those does not silence the recommendation — and it is normal to want the advice to wait longer than
the issue did. [Full reference →](../detectors-connectivity/)

## Transport quality detectors

```javascript
{
    uplinkCongestionDetector: {
        minSeverity: 0.65,            // how deep the trouble has to be, 0..1
    },                                // resolves on the browser's own verdict, not a ratio
    downlinkCongestionDetector: {
        minSeverity: 0.65,            // resolves when severity falls under half of it
    },
    congestionDetector: null,         // deprecated: one verdict for the whole connection
    transportDelayDetector: {
        thresholdInMs: 300,           // mean RTT at or above which the path counts as slow
        recoveryThresholdInMs: 200,   // RTT below which it resolves (hysteresis)
    },                                // the sustain is peerConnectionWindow, not a duration here
    blockedInboundMediaDetector: {},  // one instance per ICE transport
    blockedOutboundMediaDetector: {},
    blockedStunRequestsDetector: {},
    transportLossDetector: {
        threshold: 0.05,              // mean interval loss fraction (0..1), worse direction wins
        recoveryThreshold: 0.01,
        durationInMs: 6000,
    },
}
```

Round starting points, meant to be tuned against a real fleet. Only the delay threshold has an
external reference behind it (ITU-T G.114). [Full reference →](../detectors-transport-quality/)

## Pipeline disruption — the send chain

```javascript
{
    captureSourceLostDetector: {},    // the camera or mic went away under the track
    captureTrackMutedDetector: {},    // the OS or another app took it (telemetry)
    silentAudioSourceDetector: {
        silenceThresholdInMs: 60000,  // long on purpose: silence != a broken mic
        silenceRmsThreshold: 0.0001,  // interval-integrated RMS, not the flickery audioLevel
        recoveryRmsThreshold: 0.0003, // higher, so one dither blip cannot close a finding
    },
    videoCaptureBottleneckDetector: {
        produceDegradationThreshold: 0.2,  // camera more than 20% short of the configured fps
    },
    encoderBottleneckDetector: {
        encodeDegradationThreshold: 0.3,   // encoder leaving 30% of handed frames unencoded
    },
    rtpSenderStalledDetector: {
        thresholdInMs: 4000,          // frames encoding while no packet leaves, in stats time
    },
    dryOutboundTrackDetector: { thresholdInMs: 5000 },
}
```

Both frame-supply detectors average over the `detection` and `recovery` slices of
`outboundTrackWindow` rather than holding a window each, so the sustain and the hysteresis are
configured in one place.

## Pipeline disruption — the receive chain

```javascript
{
    transportDemuxStalledDetector: {
        thresholdInMs: 4000,                  // its own copy, not shared with the sender detector
        minTransportReceiveBitrateBps: 20000, // above this, incoming traffic must demux
    },
    dryInboundTrackDetector: { thresholdInMs: 5000 },
    frameAssemblyStalledDetector: {
        thresholdInMs: 3000,          // packets arriving with no frame completed, in stats time
        minPacketsReceived: 20,       // below this it is a trickle, not a stall
    },
    decoderBottleneckDetector: {
        decodeDegradationThreshold: 0.1,  // 10% of arriving frames left undecoded
        minReceivedFps: 5,                // too thin a stream to judge a decoder on
    },                                    // the span is inboundTrackWindow
    decoderPerformanceDetector: {
        decodeTimeBudgetRatio: 0.8,   // share of the per-frame budget decoding may use
        minFramesReceived: 10,
        quietLossThreshold: 0.02,     // above this, blame the network instead
        minConsecutiveTicks: 2,
    },
    stuckDecoderDetector: {
        thresholdInMs: 4000,   // floor; effective wait = max(this, rttMultiplier × RTT)
        rttMultiplier: 15,     // high-RTT paths get more time to recover legitimately
        minBitrate: 10000,     // bps below which this is a dry track, not a wedge
        minPliCount: 2,
    },
    playoutDiscrepancyDetector: {
        lowSkewRatio: 0.1,
        highSkewRatio: 0.25,
        minFramesReceived: 10,
    },
}
```

## Pipeline disruption — the repair loop and the machine

```javascript
{
    videoRecoveryFailedDetector: {
        recoveryFailedThresholdInMs: 5000,  // stalled with PLIs out for this long
        recoveryFailedMinPliCount: 2,       // proof we actually asked for repair
    },
    cpuPerformanceDetector: {
        utilizationThreshold: 0.15,   // both halves of the pipeline, over clientWindow
    },
}
```

[Full reference →](../detectors-pipeline/)

## Perceived quality detectors

```javascript
{
    pixelatedVideoDetector: {
        threshold: 0.03,              // bits/pixel at or below which the picture is coarse
        recoveryThreshold: 0.05,      // above this it resolves
        durationInMs: 8000,
    },
    inboundVideoFlowStateDetector: {},  // both verdicts measured over inboundTrackWindow
    inventedSpeechDetector: {
        allowedInventedRatio: 0.05,   // RFC 7294: above 5% concealment is severely concealed
        raiseAfterInventedMs: 400,    // invention beyond the allowance before the issue opens
    },
    audioPlayoutSynthesisDetector: {
        synthesizedRatioThreshold: 0.05,  // share of what was played that was invented
        createEvent: true,
    },
    avDesyncPlayoutDetector: {
        // Asymmetric on purpose: audio ahead of the picture is far more
        // objectionable than audio behind it (ITU-R BT.1359-1).
        audioAheadRaiseInMs: 90,
        audioAheadResolveInMs: 45,
        audioBehindRaiseInMs: 185,    // magnitudes, for audio lagging the picture
        audioBehindResolveInMs: 125,
        sustainForInMs: 3000,         // stats time past the threshold before raising
    },
    jitterBufferStressDetector: {
        targetDelayThresholdInMs: 200,
        timeStretchThreshold: 0.02,
        minConsecutiveTicks: 2,
    },
}
```

[Full reference →](../detectors-perceived-quality/)

## Telemetry detectors

These emit events and never raise issues.

```javascript
{
    captureTrackMutedDetector: { createEvent: true },
    codecChangeDetector: { createEvent: true },
    videoResolutionChangeDetector: { createEvent: true },
    simulcastLayerDetector: { createEvent: true },
    statsGapDetector: {
        gapRatioThreshold: 2,  // multiple of collectingPeriodInMs that counts as a gap
        minGapInMs: 5000,      // a single missed short tick is jitter, not a gap
        createEvent: true,
    },
}
```

[Full reference →](../detectors-telemetry/)

## Switching detectors off

```javascript
// Never construct them: one key, one detector.
new ClientMonitor({
    congestionDetector: null,
    avDesyncPlayoutDetector: null,
    cpuPerformanceDetector: null,
});
```

Because every detector has a key of its own, `null` removes **exactly one** class. Turning off what
used to be a group means naming each of its members' keys — see
[What changed in 4.9](../migration-4-9/#breaking-one-config-block-per-detector).

At runtime, every built-in detector exposes a public `disabled` boolean and every registry exposes
`disable(name)` / `enable(name)`. Issue-raising detectors also expose `includeIssueInSample`, which
keeps a detector running locally while excluding its issues from the samples shipped to the server.

## Typing a block

Each detector file exports `<ClassName>Config`, and the package root re-exports it beside the class:

```typescript
import type { StuckDecoderDetectorConfig } from '@observertc/client-monitor-js';

const stuckDecoder: StuckDecoderDetectorConfig = { minPliCount: 3 };
```

`ClientMonitorConfig` declares each key as `<ClassName>Config | null`, so a retired key **fails to
type-check** rather than being silently ignored.

## Minimal configurations

```javascript
// Faster verdicts while debugging — every window and tick count shrinks with it.
const monitor = new ClientMonitor({ clientId: "my-client", collectingPeriodInMs: 1000 });

// Everything on defaults.
const monitor = new ClientMonitor();
```

```javascript
// Optimised for many tracks on a modest machine.
const monitor = new ClientMonitor({
    collectingPeriodInMs: 10000,
    samplingPeriodInMs: 10000,
    cpuPerformanceDetector: null,
    avDesyncPlayoutDetector: null,
    sendScoreReasonsToServer: false,   // keeps reasons off the wire without changing any score
});
```
