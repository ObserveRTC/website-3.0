---
title: "What changed in 4.9"
description: "Upgrading client-monitor-js from 4.7 / 4.8 to 4.9"
lead: "27 detector classes became 46, every group config key was retired, and the default score calculator stopped forming a second opinion"
date: 2026-09-13T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 205
toc: true
---

`4.9.0` is the largest release the library has had. It is worth reading before upgrading, because
several changes **fail loudly** (a retired config key no longer type-checks) and a few change
behaviour **quietly** (the collection period is 2.5× longer by default, so tick-counted detectors
take 2.5× as long to fire).

{{< callout context="caution" title="The one-line summary" icon="alert-triangle" >}}
**One detector class raises exactly one issue type**, and each reads a config block named after
itself. Everything below follows from that rule, plus the score calculator being rewritten to read
the issues those detectors raised instead of re-deriving the same conditions from raw stats.
{{< /callout >}}

## Why the detector layer was rebuilt

Three concrete problems, all consequences of a class owning several findings:

- **One bad stats report cost four verdicts.** `Detectors.update()` wraps each detector in its own
  try/catch, so a class that owned four findings lost all four to one malformed report.
- **`disabled` and `includeIssueInSample` are per detector.** A config key covering a group could
  not silence one finding without silencing its neighbours — and nothing in the config said so.
- **Shared state coupled unrelated conditions.** A class holding several conditions accumulated
  state that tied them together, which is what made the ICE findings hard to separate.

## Breaking: detector classes split and renamed

Issue types are the public contract and were preserved wherever the condition survived. What
changed is **class names**, **detector `name` strings** and **config keys**.

| 4.8.0 | 4.9.0 | Issue type |
|---|---|---|
| `AudioConcealmentDetector` | `InventedSpeechDetector` | `audio-concealment` → `invented-speech` |
| `AudioDesyncDetector` | `AVDesyncPlayoutDetector` | `audio-desync` → `av-desync` |
| `BlockedTransportDetector` | `BlockedInboundMediaDetector`, `BlockedOutboundMediaDetector`, `BlockedStunRequestsDetector` | `blocked-transport` → `blocked-inbound-media-transport`, `blocked-outbound-media-transport`, `blocked-stun-requests` |
| `CaptureFailureDetector` | `CaptureSourceLostDetector`, `CaptureTrackMutedDetector`, `SilentAudioSourceDetector` | `capture-track-ended` → `capture-source-lost`; `silent-audio-source` unchanged; the muted class is event-only |
| `DtlsHandshakeDetector` | `DtlsHandshakeFailedDetector`, `DtlsHandshakeStalledDetector` | both types unchanged |
| `EncoderPerformanceDetector` | `EncoderBottleneckDetector` | `encoder-bottleneck`, unchanged |
| `FreezedVideoTrackDetector` | `InboundVideoFlowStateDetector`, `VideoRecoveryFailedDetector` | `freezed-video-track` → `video-flow-disrupted`; `video-recovery-failed` unchanged; **`keyframe-storm` dropped** |
| `IceConnectivityDetector` | `IceDisconnectedDetector`, `IceConnectionFailedDetector`, `IceTransportStalledDetector`, `UnstableIcePathDetector`, `IceRestartDetector`, `IceRestartRecommendationDetector` | all four issue types unchanged; the two restart classes are event-only |
| `IceTupleChangeDetector` | `IceTraversalDetector` | none (telemetry) |
| `InboundFrameSupplyDetector` | `DecoderBottleneckDetector` | `decoder-bottleneck`, unchanged |
| `LongPcConnectionEstablishment` | `IcePathEstablishmentDetector` | none |
| `MediaPipelineDetector` | `RtpSenderStalledDetector`, `TransportDemuxStalledDetector` | `media-pipeline-stalled` → `rtp-sender-stalled`, `transport-demux-stalled` |
| `NoAvailableIceCandidateDetector` | `IceReachabilityDetector` | `no-available-ice-candidate`, unchanged |
| `OutboundFrameSupplyDetector` | `VideoCaptureBottleneckDetector` | `capture-bottleneck` → `video-capture-bottleneck` |
| `SynthesizedSamplesDetector` | `AudioPlayoutSynthesisDetector` | none → `synthesized-audio` (the condition was event-only before) |

**New with no predecessor:** `FrameAssemblyStalledDetector`, `IceEstablishmentFailedDetector`,
`PixelatedVideoDetector`, `TransportDelayDetector`, `TransportLossDetector`,
`UplinkCongestionDetector`, `DownlinkCongestionDetector`.

**`keyframe-storm` is removed outright**, with no replacement.

{{< callout context="note" title="A split class has no alias" icon="info-circle" >}}
`Detectors.getByName()` / `disable()` / `enable()` / `has()` lookup is **exact**, and there is no
alias table. A name that resolved to a class which became six could only ever have pointed at one
of them — `disable('ice-path-stability-detector')` would have kept "working" while quietly
governing a sixth of what it used to. It now returns `false` and silences nothing, which is an
answer you can act on.
{{< /callout >}}

### Retired detector names

| Retired name | What it became |
|---|---|
| `ice-path-stability-detector` / `ice-connectivity-detector` | `ice-disconnected-detector`, `ice-connection-failed-detector`, `ice-transport-stalled-detector`, `unstable-ice-path-detector`, `ice-restart-detector`, `ice-restart-recommendation-detector` |
| `dtls-handshake-detector` | `dtls-handshake-stalled-detector`, `dtls-handshake-failed-detector` |
| `capture-failure-detector` | `capture-source-lost-detector`, `silent-audio-source-detector`, `capture-track-muted-detector` |
| `media-pipeline-detector` | `rtp-sender-stalled-detector`, `transport-demux-stalled-detector` |
| `ice-tuple-change-detector` | `ice-traversal-detector` *(rename)* |
| `no-available-ice-candidate-detector` | `ice-reachability-detector` *(rename)* |
| `long-pc-connection-establishment-detector` | `ice-path-establishment-detector` *(rename)* |
| `audio-concealment-detector` | `invented-speech-detector` *(rename of a rewritten class)* |
| `audio-desync-detector` | `av-desync-playout-detector` *(a different detector — see below)* |
| `freezed-video-track-detector` | `inbound-video-flow-state-detector` |
| `blocked-transport-detector` | `blocked-inbound-media-detector`, `blocked-outbound-media-detector`, `blocked-stun-requests-detector` |
| `encoder-performance-detector` | `encoder-bottleneck-detector` *(rename)* |
| `synthesized-samples-detector` | `audio-playout-synthesis-detector` *(rename)* |
| `inbound-frame-supply-detector` | `decoder-bottleneck-detector` *(rename)* |
| `outbound-frame-supply-detector` | `video-capture-bottleneck-detector` *(rename)* |

## Breaking: one config block per detector

Every detector reads a block named after itself — its `name` in camelCase, so
`frame-assembly-stalled-detector` reads `frameAssemblyStalledDetector`. **No key is shared, and no
detector reads a neighbour's block.** 65 config keys in total: 46 detector blocks, the four shared
windows, and the basics.

A retired key **fails to type-check**. If one reaches the constructor anyway (plain JavaScript, or
a cast) it is ignored, and the detectors that used to read it run on their defaults — including a
`null` meant to disable them.

| Retired config key | What to use instead |
|---|---|
| `captureFailureDetector` | `captureSourceLostDetector`, `silentAudioSourceDetector`, `captureTrackMutedDetector` |
| `blockedTransportDetector` | `blockedInboundMediaDetector`, `blockedOutboundMediaDetector`, `blockedStunRequestsDetector` |
| `iceConnectivityDetector` / `icePathStabilityDetector` | `iceDisconnectedDetector`, `iceConnectionFailedDetector`, `iceTransportStalledDetector`, `unstableIcePathDetector`, `iceRestartDetector`, `iceRestartRecommendationDetector` |
| `dtlsHandshakeDetector` | `dtlsHandshakeStalledDetector`, `dtlsHandshakeFailedDetector` |
| `mediaPipelineDetector` | `rtpSenderStalledDetector`, `transportDemuxStalledDetector` |
| `encoderPerformanceDetector` | `encoderBottleneckDetector` *(rename)* |
| `longPcConnectionEstablishmentDetector` | `icePathEstablishmentDetector` *(replacement — it reports which setup stage is stuck)* |
| `noAvailableIceCandidateDetector` | `iceReachabilityDetector` *(rename)* |
| `videoRecoveryDetector` | `videoRecoveryFailedDetector` |
| `videoFreezesDetector` / `freezedVideoTrackDetector` | `inboundVideoFlowStateDetector` *(one detector for the frozen and choppy verdicts)* |
| `syntheticSamplesDetector` / `synthesizedSamplesDetector` | `audioPlayoutSynthesisDetector` *(rename; same fields)* |
| `audioConcealmentDetector` | `inventedSpeechDetector` *(rename — a different shape; none of the four old fields has an equivalent)* |
| `audioDesyncDetector` | `avDesyncPlayoutDetector` *(replacement — skew in milliseconds, not a correction fraction)* |
| `inboundFrameSupplyDetector` | `decoderBottleneckDetector` *(rename; same fields)* |
| `outboundFrameSupplyDetector` | `videoCaptureBottleneckDetector` *(rename; same fields)* |

Two field moves worth checking for:

- `icePathEstablishmentDetector.restartRecommendationThresholdInMs` / `.restartRecommendationCooldownInMs`
  now live on `iceRestartRecommendationDetector`, which holds all four recommendation conditions.
- `EncoderBottleneckDetector` reads its own `encoderBottleneckDetector.encodeDegradationThreshold`
  (default `0.3`) rather than borrowing the capture detector's threshold.

Three detectors that had **no key at all** gained one, so each can now be disabled individually:
`dtlsHandshakeFailedDetector`, `iceConnectionFailedDetector` and `iceTraversalDetector`. All three
carry no tunables — `{}` enables, `null` disables.

## Breaking: default periods are 5000 / 5000

Was `collectingPeriodInMs: 2000` and `samplingPeriodInMs: 8000`. `getStats()` is not free, and the
previous default paid for it two and a half times over on every call. The two now match, so a
sample is created on every collection and the interval between samples cannot drift — the sampling
period should always be a multiple of the collecting period, and the monitor warns when it is not.

{{< callout context="caution" title="Tick-counting detectors are slower to fire, deliberately" icon="alert-triangle" >}}
A threshold spelled as a number of consecutive collections now spans 2.5× the wall-clock time it
did: `minConsecutiveTicks: 2` covers 10 seconds rather than 4. Windows sized in values behave the
same way — the default detection slice of 3 covers 10 seconds. That buys confidence at the cost of
latency. Pass `collectingPeriodInMs: 2000` to restore the old timing throughout.
{{< /callout >}}

## Breaking: the default score calculator is a reading of the open issues

Scoring was always pluggable: the library defines `ScoreCalculator` (one `update()`),
`ClientMonitor.scoreCalculator` holds the implementation in use, and `DefaultScoreCalculator` is
the reference implementation assigned at construction. What changed is that reference
implementation. An application supplying its own calculator is unaffected.

- **It no longer re-derives anything from raw stats.** Every monitor starts at 5.0 and is reduced
  by the findings its own detectors raised, read from that monitor's `IssueRegistry`. A fault is
  judged in exactly one place, so the score cannot disagree with the issue list an operator is
  looking at.
- **Six conditions that existed twice are now single.** `pixelated-video`, `low-fps`,
  `volatile-fps`, `high-rtt`, `high-jitter` and `high-packetloss` used to be computed by the
  calculator with its own thresholds *while* detectors derived the same conditions with theirs.
  (`high-jitter` has no detector successor and was dropped rather than replaced.)
- **The client score is `5 − RMSE` across five dimensions** — the transport, and inbound and
  outbound audio and video — replacing 4.8's "the peer connection scales its tracks by
  `pcScore / 5`". A dimension nothing reported is *absent*, not zero. `[5, 5, 0]` scores `2.11`
  where an average would say `3.33`.
- **Connectivity issues are deliberately not priced.** A path carrying nothing leaves nothing to
  have an opinion about, and `dry-inbound-track` / `dry-outbound-track` already take the tracks
  riding on it to zero.

**Removed exports:** `DefaultScoreCalculatorInboundVideoTrackScoreAppData`,
`DefaultScoreCalculatorOutboundAudioTrackScoreAppData`,
`DefaultScoreCalculatorOutboundVideoTrackScoreAppData`,
`DefaultScoreCalculatorPeerConnectionScoreAppData`, `DefaultScoreCalculatorSubtractions`,
`DefaultScoreCalculatorSubtractionReason`, `VIDEO_QP_THRESHOLDS`, `VIDEO_QP_MAX` and
`VideoQpThresholds`. Nothing replaces them: there is no table of issue weights to import and no
config key that retunes a charge. Scoring policy is changed by assigning your own
`ScoreCalculator`. See [Scoring](./scoring/).

## Deprecated: `CongestionDetector`

Still registered, still raising `congestion`, still configured by `congestionDetector`. It answers
for both directions from one signal, which a receiver cannot support — Chrome computes no incoming
bandwidth estimate, so the old detector's incoming fields read zero there.

```javascript
new ClientMonitor({
    congestionDetector: null,          // stop the one-verdict-per-connection detector
    uplinkCongestionDetector: {},      // and take the two graded ones instead
    downlinkCongestionDetector: {},
});
```

`uplink-congestion` and `downlink-congestion` each score their direction from two independent
witnesses combined as a geometric mean, and report a graded `severity` rather than one on/off
verdict for the whole connection. See
[Transport quality detectors](./detectors-transport-quality/).

## Breaking: retired events

`audio-concealment`, `audio-desync-track`, `capture-track-ended`, `freezed-video-track`,
`keyframe-storm`, `media-pipeline-stalled` and `too-long-pc-connection-establishment` no longer
exist. 68 events in total; the additions mirror the detector table above, plus
`ice-path-establishment-slow` and `capture-source-lost`.

**On the wire, one `ClientEventTypes` member is renamed:** `CAPTURE_TRACK_ENDED` →
`CAPTURE_SOURCE_LOST`, with `CaptureTrackEndedEventPayload` becoming
`CaptureSourceLostEventPayload`. A server matching on the event-type string has to accept the new
name. The sample schema itself is unchanged at **3.7.0**.

## Breaking: renamed and withdrawn monitor fields

| 4.8.0 | 4.9.0 |
|---|---|
| `InboundRtpMonitor.concealmentRate` | `inventedSpeechRatio` |
| `InboundRtpMonitor.dropRatio` | `droppedFrameRatio` (this interval's share, not the call's) |
| `OutboundTrackMonitor.getHighestLayer()` | `highestLayer` |
| `PeerConnectionMonitor.attributeRtpToTransport()` | withdrawn — `hasInboundMedia` / `hasInboundVideo` / `hasOutboundMedia` answer what the detectors used it for |
| `PeerConnectionMonitor.highestSeen*Bitrate` (four fields) | withdrawn — the congestion detectors hold their own `DecayingMaxEstimator`, which forgets |
| `InboundTrackMonitor.contentType`, `motionType`, `presentedResolution`, `videoTag`, `paused` | read-only getters over the declared context; write them with `setContext()` / `ClientMonitor.setInboundTrackContext()` |

## Two detectors measure something genuinely different now

**`audio-concealment` → `invented-speech`.** The finding is the share of audio that was
*invented*, not the share of samples that were concealed. The old detector summed per-tick ratios
over a sliding window, which is not the ratio of the sums; the new one integrates a rate over
elapsed time and reads `inventedSpeechRatio` off the monitor. The monitor event, the payload type
and the score reason moved with the name.

**`audio-desync` → `av-desync`.** A replacement, not a rename. The old detector inferred lip sync
from NetEQ's accelerate and preemptive-expand counters — which measure jitter-buffer adaptation,
and because sync logic corrects drift by *raising* NetEQ's target delay, tended to fire on the
correction rather than the fault. The new one measures the offset between the two tracks'
`estimatedPlayoutTimestamp` directly, in milliseconds of skew. Nothing about the old thresholds
carries over, and it needs a piece of context the old one did not:

```javascript
// Without this the detector reports inputsUnavailable — an SFU forwards audio and
// video as independent streams with no signalled relationship.
monitor.setInboundTrackContext(audioTrackId, { linkedVideoTrackId: videoTrackId });
```

## New in 4.9

### Shared facts, shared windows, shared registries

- **`IssueRegistry`** — every monitor owns the issues raised against it, so a detector no longer
  reaches into a client-wide map and the score reads one monitor's findings directly:
  `PeerConnectionMonitor.issues`, `InboundTrackMonitor.issues`, `OutboundTrackMonitor.issues`, with
  `hasType()`, `getByType()`, `getFirstPayloadByType()`.
- **`SlicedWindow`** — the rolling window several detectors had each implemented, done once and
  shared by every detector on the same monitor, so detectors judging one track judge the same
  stretch of time. Sized by `clientWindow`, `inboundTrackWindow`, `outboundTrackWindow` and
  `peerConnectionWindow`, which replace the per-detector `durationInMs` keys.
- **`DecayingMaxEstimator`** — the largest value seen recently, where "recently" is a half-life
  rather than a window, decaying per second of *stats* time so applications collecting at different
  periods forget at the same rate.
- **`FrugalQuantileEstimator`** — a streaming quantile held in one number, for baselines of spiky
  signals where an EWMA settles far above the true median.

### `statsClockTime` — every duration is stats time

Every monitor accumulates the measured gaps between collections, and every window and duration in
the library is aged on that clock rather than on `Date.now()`. A late or skipped collection widens
a window by the time the condition actually held; a backgrounded tab cannot age a stall into an
issue.

### `inputsUnavailable` — silence you can read

A detector whose inputs the browser does not report says so, instead of reading as a healthy path.
Fourteen of the 46 classes set it. This is the behaviour whose absence made a whole browser
population look like the best behaved on a fleet.

```javascript
const d = pcMonitor.detectors.getByName('transport-delay-detector');
d?.inputsUnavailable;   // true = "nothing was observed", not "nothing is wrong"
```

### Monitor API additions

- **`bufferClientSamplesUntilSubscriber`** (default `false`) — samples created before anything
  listens for `'sample-created'` are buffered and replayed in creation order to the first
  subscriber, so a monitor started before the transport is ready no longer loses the opening minute
  of a call.
- **`ExtensionStatsMonitor`** — application stats fold into the monitor tree like any other:
  `getExtensionStatsMonitor()`, `getExtensionStatsPayload()`, `mappedExtensionStatsMonitors`.
- **`ClientMonitor.createdAt` / `uptimeInMs`** — how long this monitor has been running.
- **`ClientMonitor.cpuUtilization`** — the reading behind `cpulimitation`, published on every
  collection the detector could judge, whether or not it raised.

## Fixed in 4.9

| Fix | What was wrong |
|---|---|
| One-way media no longer reads as a fault | `blocked-transport` and `ice-transport-stalled` both assumed a peer connection carries media in both directions; an SFU publish transport does not, and both raised on healthy calls. Each now requires that return media was expected at all |
| Data-channel bitrate accumulators reset each collection | They accumulated forever, so a 40 kbps signalling channel read as 9.7 Mbps after twenty minutes |
| RTCP round trip only counted when the report advances | `getStats()` keeps serving the last `remote-inbound-rtp` after the far end goes quiet, so the average converged on a measurement nobody had made recently |
| `postAdapt` no longer runs twice | Every accumulator in `_acceptAdaptedStats` was applied twice per collection |
| The issue union matches what detectors raise | It declared `blocked-transport` and `capture-bottleneck`, which nothing raises, and omitted `blocked-stun-requests` and `video-capture-bottleneck`, which are |

## What 4.8 brought, if you are coming from 4.7

4.8.0 was the transport-observability release, and it moved the wire format to schema **3.7.0**:

- **Payloads may nest.** `ClientEvent`, `ClientIssue`, `ClientMetaData` and `ExtensionStat`
  payloads accept nested structures, not only flat records of primitives. `ClientPayloadValue` is
  removed.
- **`PEER_CONNECTION_ICE_PATH_CHANGED` carries structured `from` / `to`.** Consumers that used to
  `JSON.parse` those fields must read them as objects.
- **`IceTransportStats` static members ship on change only** — `iceRole`,
  `iceLocalUsernameFragment`, the certificate ids, `tlsVersion`, `dtlsCipher`, `dtlsRole`,
  `srtpCipher`. **Absence means "unchanged", not "unknown"**; keep the last seen value per
  transport id, or set `sendIceTransportMetadataOnChangeOnly: false`.
- **DTLS handshake failure got an owner** — `dtls-handshake-failed` and `dtls-handshake-stalled`
  (4.9 split that class into the two detectors that raise them).
- **One attribution rule for RTP → transport**, and a complete traversal graph: `getIceTransport()`
  and `getSelectedCandidatePair()` on all four RTP monitors.
- **Selected-pair churn is counted from the browser** where it reports it, so a flap that departs
  and returns inside one collecting period is no longer invisible.

## Upgrade checklist

{{< steps >}}
{{< step >}}Search your config for any key in the retired table above and replace it with the specific detector blocks you meant. TypeScript will find them for you.{{< /step >}}
{{< step >}}Search for `detectors.disable(` / `getByName(` and update every retired `name` string — these fail silently, not at compile time.{{< /step >}}
{{< step >}}Decide on the collection period: keep the new 5000 default and accept slower verdicts, or set `collectingPeriodInMs: 2000` to keep 4.8 timing.{{< /step >}}
{{< step >}}Update any server-side allow-list of issue types: `audio-concealment`, `audio-desync`, `capture-track-ended`, `freezed-video-track`, `keyframe-storm`, `media-pipeline-stalled`, `capture-bottleneck` and `blocked-transport` are gone as issue types.{{< /step >}}
{{< step >}}Rename `CAPTURE_TRACK_ENDED` to `CAPTURE_SOURCE_LOST` wherever a server matches on the event type.{{< /step >}}
{{< step >}}If you imported anything from the old score internals, move that logic into your own `ScoreCalculator`.{{< /step >}}
{{< step >}}Declare `linkedVideoTrackId` on inbound audio tracks if you want lip-sync detection at all.{{< /step >}}
{{< step >}}Switch `congestionDetector: null` and enable the uplink / downlink pair.{{< /step >}}
{{< /steps >}}
