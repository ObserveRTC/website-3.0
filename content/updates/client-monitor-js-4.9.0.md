---
title: "Client Monitor 4.9.0"
date: "2026-09-13T12:54:52Z"
draft: false
project: "Client Monitor"
version: "4.9.0"
summary: "Split and renamed detectors, configuration and event changes, revised scoring, and five-second collection and sampling defaults."
releaseUrl: "https://github.com/ObserveRTC/client-monitor-js/releases/tag/4.9.0"
author: "balazskreith"
---
The detector layer is rebuilt around one rule: **one detector class raises one issue type**. 27
detector classes became 46, 27 issue types became 37, and the score stopped re-deriving thresholds
from raw stats.

Three things drove it. A class that owned four findings lost all four to one malformed stats
report, because `Detectors.update()` wraps each detector in its own try/catch. `disabled` and
`includeIssueInSample` are per detector, so a config key covering a group could not silence one
finding without silencing its neighbours. And a class holding several conditions accumulated
shared state that coupled them.

Full reference: [docs/DETECTOR_TAXONOMY.md](https://github.com/ObserveRTC/client-monitor-js/blob/4.9.0/docs/DETECTOR_TAXONOMY.md).

## Breaking: detector classes split and renamed

| 4.8.0 | 4.9.0 | Issue type |
|---|---|---|
| `AudioConcealmentDetector` | `InventedSpeechDetector` | `audio-concealment` → `invented-speech` |
| `AudioDesyncDetector` | `AVDesyncPlayoutDetector` | `audio-desync` → `av-desync` |
| `BlockedTransportDetector` | `BlockedInboundMediaDetector`, `BlockedOutboundMediaDetector`, `BlockedStunRequestsDetector` | `blocked-transport` → `blocked-inbound-media-transport`, `blocked-outbound-media-transport`, `blocked-stun-requests` |
| `CaptureFailureDetector` | `CaptureSourceLostDetector`, `CaptureTrackMutedDetector`, `SilentAudioSourceDetector` | `capture-track-ended` → `capture-source-lost`; `silent-audio-source` unchanged; the muted class is event-only |
| `DtlsHandshakeDetector` | `DtlsHandshakeFailedDetector`, `DtlsHandshakeStalledDetector` | `dtls-handshake-failed`, `dtls-handshake-stalled`, both unchanged |
| `EncoderPerformanceDetector` | `EncoderBottleneckDetector` | `encoder-bottleneck`, unchanged |
| `FreezedVideoTrackDetector` | `InboundVideoFlowStateDetector`, `VideoRecoveryFailedDetector` | `freezed-video-track` → `video-flow-disrupted`; `video-recovery-failed` unchanged; `keyframe-storm` dropped |
| `IceConnectivityDetector` | `IceDisconnectedDetector`, `IceConnectionFailedDetector`, `IceTransportStalledDetector`, `UnstableIcePathDetector`, `IceRestartDetector`, `IceRestartRecommendationDetector` | `ice-disconnected`, `ice-connection-failed`, `ice-transport-stalled`, `unstable-ice-path`, all unchanged; the two restart classes are event-only |
| `IceTupleChangeDetector` | `IceTraversalDetector` | none (telemetry) |
| `InboundFrameSupplyDetector` | `DecoderBottleneckDetector` | `decoder-bottleneck`, unchanged |
| `LongPcConnectionEstablishment` | `IcePathEstablishmentDetector` | none |
| `MediaPipelineDetector` | `RtpSenderStalledDetector`, `TransportDemuxStalledDetector` | `media-pipeline-stalled` → `rtp-sender-stalled`, `transport-demux-stalled` |
| `NoAvailableIceCandidateDetector` | `IceReachabilityDetector` | `no-available-ice-candidate`, unchanged |
| `OutboundFrameSupplyDetector` | `VideoCaptureBottleneckDetector` | `capture-bottleneck` → `video-capture-bottleneck` |
| `SynthesizedSamplesDetector` | `AudioPlayoutSynthesisDetector` | none → `synthesized-audio` (the condition was event-only before) |

A split class has no alias: one that raised four issues cannot be aliased onto one that raises a
single one without lying about what it does. Import the part you meant.

**Also new**, with no predecessor: `FrameAssemblyStalledDetector`,
`IceEstablishmentFailedDetector`, `PixelatedVideoDetector`, `TransportDelayDetector`,
`TransportLossDetector`, `UplinkCongestionDetector`, `DownlinkCongestionDetector`.

`keyframe-storm` is removed outright, with no replacement.

## Breaking: one config block per detector

Every detector reads a block named after itself — its `name` in `camelCase`, so
`frame-assembly-stalled-detector` reads `frameAssemblyStalledDetector`. Keys that used to
construct a group of classes are gone, because a `null` intended to silence one finding silently
removed its neighbours: `audioConcealmentDetector`, `audioDesyncDetector`,
`blockedTransportDetector`, `captureFailureDetector`, `dtlsHandshakeDetector`,
`encoderPerformanceDetector`, `iceConnectivityDetector`, `inboundFrameSupplyDetector`,
`longPcConnectionEstablishmentDetector`, `mediaPipelineDetector`,
`noAvailableIceCandidateDetector`, `outboundFrameSupplyDetector`, `syntheticSamplesDetector`,
`videoFreezesDetector`, `videoRecoveryDetector`.

65 config keys: 46 detector blocks, one per class, plus the shared windows below and the basics. A
retired key fails to type-check.

## Breaking: collectingPeriodInMs defaults to 5000, samplingPeriodInMs to 5000

Was 2000 and 8000. `getStats()` is not free and the previous default paid for it two and a half
times over on every call; 5 seconds is where the cost stops being noticeable on a busy client. The
two now match, so a sample is created on every collection and the interval between samples cannot
drift — the sampling period should always be a multiple of the collecting period, and the monitor
warns when it is not.

**Tick-counting detectors are slower to fire at this default, deliberately unchanged.** A
threshold spelled as a number of consecutive collections now spans 2.5× the wall-clock time it
did — `minConsecutiveTicks: 2` covers 10 seconds rather than 4 — which buys confidence at the cost
of latency. Windows sized in values behave the same way: the default detection slice of 3 covers
10 seconds. Pass `collectingPeriodInMs: 2000` to restore the old timing throughout.

## Breaking: the default score calculator is a reading of the open issues

Scoring is pluggable and always was: the library defines `ScoreCalculator` (one
`update()`), `ClientMonitor.scoreCalculator` holds the implementation in use, and
`DefaultScoreCalculator` is the reference implementation assigned at construction. What
follows is that reference implementation changing its mind — its numbers are internal, so
an application that supplies its own calculator is unaffected.

`DefaultScoreCalculator` no longer re-derives anything from raw stats. Every monitor starts at
5.0 and is reduced by the findings its own detectors raised, read from that monitor's own
`IssueRegistry`, so a fault is judged in exactly one place and the score cannot disagree with the
issue list an operator is looking at.

A charge named after an issue type is applied only while that issue is open — what it is *worth*
can still be a continuous reading, so `decoder-bottleneck` costs what the decoder actually fell
behind by. A charge with no issue of that name is a continuous reading on its own:
`volatile-fps`, `dropped-video-frames`, `blocky-video`, `unstable-audio-playout` and
`unstable-transport` exist only here, and are named for what they measure. A reason that cost
nothing is not written at all — a key sitting at `0` reads as a fault that was found and never
resolved.

Connectivity issues are **deliberately not priced**. A path carrying nothing leaves nothing to
have an opinion about, and `dry-inbound-track` / `dry-outbound-track` already take the tracks
riding on it to zero; charging the connection as well would be the same fault counted twice.

**The client score is `5 − RMSE` across five dimensions** — the transport, and inbound and
outbound audio and video — which replaces 4.8.0's "the peer connection scales its tracks by
`pcScore / 5`". Each dimension is the weighted mean of the monitors making it up, and a dimension
nothing reported is *absent* rather than zero: a call that sends no video is not a call whose
video is broken. Squaring the distances is what makes one collapsed dimension cost more than the
same shortfall spread evenly — `[5, 5, 0]` scores `2.11` where an average would say `3.33`.

Removed with it: `DefaultScoreCalculatorInboundVideoTrackScoreAppData`,
`DefaultScoreCalculatorOutboundAudioTrackScoreAppData`,
`DefaultScoreCalculatorOutboundVideoTrackScoreAppData`,
`DefaultScoreCalculatorPeerConnectionScoreAppData`, `DefaultScoreCalculatorSubtractions`,
`DefaultScoreCalculatorSubtractionReason`, and the `VIDEO_QP_THRESHOLDS` / `VIDEO_QP_MAX` /
`VideoQpThresholds` exports — a blocky picture is now `PixelatedVideoDetector`'s verdict over
`InboundTrackMonitor.quantizationDegradation`, not the calculator's own model.

Those were the last score internals reachable from outside the package. Nothing replaces them:
there is no table of issue weights to import, and no config key that retunes a charge. Scoring
policy is changed by assigning your own `ScoreCalculator` to `ClientMonitor.scoreCalculator`,
which reads each monitor's `issues` registry and writes `calculatedScore` / `setScore()`.

## Breaking: retired events

`audio-concealment`, `audio-desync-track`, `capture-track-ended`, `freezed-video-track`,
`keyframe-storm`, `media-pipeline-stalled` and `too-long-pc-connection-establishment` no longer
exist. 68 events in total; the additions mirror the detector table above, plus
`ice-path-establishment-slow` and `capture-source-lost`.

On the wire, one `ClientEventTypes` member is renamed: **`CAPTURE_TRACK_ENDED` →
`CAPTURE_SOURCE_LOST`**, with `CaptureTrackEndedEventPayload` becoming
`CaptureSourceLostEventPayload`. A server matching on the event-type string has to accept the new
name. The sample schema itself is unchanged at **3.7.0**.

## Breaking: renamed and withdrawn monitor fields

The monitors were renamed alongside the detectors reading them, so a field named after a
withdrawn issue is gone too.

| 4.8.0 | 4.9.0 |
|---|---|
| `InboundRtpMonitor.concealmentRate` | `inventedSpeechRatio` |
| `InboundRtpMonitor.dropRatio` | `droppedFrameRatio` (this interval's share, not the call's) |
| `OutboundTrackMonitor.getHighestLayer()` | `highestLayer` |
| `PeerConnectionMonitor.attributeRtpToTransport()` | withdrawn; `hasInboundMedia` / `hasInboundVideo` / `hasOutboundMedia` answer what the detectors used it for |
| `PeerConnectionMonitor.highestSeenSendingBitrate`, `highestSeenReceivingBitrate`, `highestSeenAvailableOutgoingBitrate`, `highestSeenAvailableIncomingBitrate` | withdrawn; the congestion detectors hold their own `DecayingMaxEstimator`, which forgets |
| `InboundTrackMonitor.contentType`, `motionType`, `presentedResolution`, `videoTag`, `paused` | read-only getters over the declared context; write them with `setContext()` / `ClientMonitor.setInboundTrackContext()` |

## Deprecated: CongestionDetector

Still registered and still raising `congestion`, and still configured by `congestionDetector`.
It answers for both directions from one signal, which a receiver cannot support — Chrome computes
no incoming bandwidth estimate, so the old detector's incoming fields read zero there. Set
`congestionDetector: null` and listen for `uplink-congestion` / `downlink-congestion` instead.
Nothing else emits on the `congestion` event: the replacements each report on their own, with a
graded severity rather than one on/off verdict for the whole connection.

## Capacity: one detector per direction

`UplinkCongestionDetector` scores the sending path from two witnesses — how far the browser's
bandwidth estimate has fallen below the highest it recently reached, and how far pacer time per
packet sits above its own running median. `DownlinkCongestionDetector` scores the receiving path
from the arriving bitrate against its recent maximum, and the per-frame jitter buffer delay
against its median.

Each pair combines as a geometric mean, so a witness at its healthy level takes the severity to
zero rather than merely failing to add — which is what separates a path running out of room from
a sender that was asked for less. Two numbers are configurable per direction: `minSeverity`, how
deep the trouble has to be before it is reported, and `pacerBloatingSaturatesAt` /
`bufferBloatingSaturatesAt`, where the delay witness tops out as a multiple of the connection's
own median. Neither detector uses a recovery ratio against the old maximum, because nothing knows
what a narrowed path can carry now; the recent maximum decays instead, and fades faster for 30
seconds after an episode closes, since a path rarely gives back all of what one took.

## New: shared facts, shared windows, shared registries

- **`IssueRegistry`** — every monitor owns the issues raised against it, so a detector no longer
  reaches into a client-wide map and the score can read one monitor's findings directly.
  `PeerConnectionMonitor.issues`, `InboundTrackMonitor.issues`, `OutboundTrackMonitor.issues`.
- **`SlicedWindow`** — the rolling window several detectors had each implemented, done once, and
  shared by every detector on the same monitor so that detectors judging one track judge the same
  stretch of time. Sized per monitor level by `clientWindow`, `inboundTrackWindow`,
  `outboundTrackWindow` and `peerConnectionWindow`, which replace the per-detector `durationInMs`
  keys, and published as `slicedWindow` on each monitor.
- **`DecayingMaxEstimator`** — the largest value seen recently, where "recently" is a half-life
  rather than a window, decaying per second of stats time so applications collecting at different
  periods forget at the same rate.
- **`FrugalQuantileEstimator`** — a streaming quantile held in one number, for baselines of spiky
  signals where an EWMA settles far above the true median.

**`statsClockTime`** — every monitor now accumulates the measured gaps between collections, and
every window and duration in the library is aged on that clock rather than on `Date.now()`. A
late or skipped collection widens a window by the time the condition actually held; a backgrounded
tab cannot age a stall into an issue.

**`inputsUnavailable`** — a detector whose inputs the browser does not report says so, instead of
reading as a healthy path. This is the behaviour whose absence made a whole browser population
look like the best behaved on a fleet.

## New: monitor API

- **`bufferClientSamplesUntilSubscriber`** (default `false`) — samples created before anything
  listens for `'sample-created'` are buffered and replayed in creation order to the first
  subscriber, instead of being dropped. A monitor started before the transport is ready no longer
  loses the opening minute of a call.
- **`ExtensionStatsMonitor`** — application stats are folded into the monitor tree like any other:
  `ClientMonitor.getExtensionStatsMonitor()`, `getExtensionStatsPayload()` and
  `mappedExtensionStatsMonitors`.
- **`ClientMonitor.createdAt` / `uptimeInMs`** — how long this monitor has been running.
- **`ClientMonitor.cpuUtilization`** — the reading behind `cpulimitation`, published on every
  collection the detector could judge whether or not it raised.

## Fixed

| Fix | What was wrong |
|---|---|
| One-way media no longer reads as a fault | `blocked-transport` and `ice-transport-stalled` both assumed a peer connection carries media in both directions; an SFU publish transport does not, and both raised on healthy calls. Each now requires that return media was expected at all — at least one inbound RTP stream attributed to the transport |
| Data-channel bitrate accumulators reset each collection | they accumulated forever, so a 40 kbps signalling channel read as 9.7 Mbps after twenty minutes |
| RTCP round trip only counted when the report advances | `getStats()` keeps serving the last `remote-inbound-rtp` after the far end goes quiet, so the average converged on a measurement nobody had made recently |
| `postAdapt` no longer runs twice | every accumulator in `_acceptAdaptedStats` was applied twice per collection |
| The issue union matches what detectors raise | it declared `blocked-transport` and `capture-bottleneck`, which nothing raises, and omitted `blocked-stun-requests` and `video-capture-bottleneck`, which are raised — so `video-capture-bottleneck` also carried no score weight |

---

Source: [GitHub release 4.9.0](https://github.com/ObserveRTC/client-monitor-js/releases/tag/4.9.0). Published at 2026-09-13T12:54:52Z (UTC).
