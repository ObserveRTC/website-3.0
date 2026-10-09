---
slug: "metrics"
title: "Metrics & missing values"
description: "Distinguish browser measurements, adapted stats and calculated values."
lead: "Distinguish browser measurements, adapted stats and calculated values."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 40
toc: true
---

Metrics help you explain what a client is sending, receiving, and playing. Start with the overview measurements, then follow the affected track or stream when something looks wrong. A missing measurement means the browser or current interval did not supply enough evidence; it does not mean the value is zero.

When interpreting a value, distinguish its origin: **browser stat**, **adapted/inferred stat**, **derived measurement**, **declared context**, **detector/score result**, **identity/lifecycle metadata**. Application-defined measurements belong to **application extensions**.

## Monitor ownership

The authoritative raw-stat families and exact field sets are in the schema inventory. Their monitor ownership is:

| Monitor | Browser report / content | Wire location under a `PeerConnectionSample` |
|---|---|---|
| `InboundRtpMonitor` | inbound-rtp: received/lost packets, jitter, received bytes, frame decode/render/freeze counters, jitter buffer, concealment, FEC/RTX, corruption | `inboundRtps[]` |
| `OutboundRtpMonitor` | outbound-rtp: sent packets/bytes, encoded frames, target bitrate, encode cost, QP, limitation durations, retransmission and feedback | `outboundRtps[]` |
| `RemoteInboundRtpMonitor` | remote-inbound-rtp: receiver-reported loss/jitter/RTT for local outbound stream | `remoteInboundRtps[]` |
| `RemoteOutboundRtpMonitor` | remote-outbound-rtp: sender reports for a local inbound stream | `remoteOutboundRtps[]` |
| `CodecMonitor` | codec identifiers, MIME type, clock rate, channels, FMTP, transport link | `codecs[]` |
| `MediaSourceMonitor` | media-source capture geometry/fps/frames and audio energy/duration | `mediaSources[]` |
| `MediaPlayoutMonitor` | media-playout synthesized audio duration/events, playout delay, sample totals | `mediaPlayouts[]` |
| `IceTransportMonitor` | transport: packets/bytes, ICE/DTLS state/roles, pair/certificate references, negotiated crypto | `iceTransports[]` |
| `IceCandidateMonitor` | local-candidate/remote-candidate addresses, ports, type, protocol, relay metadata | `iceCandidates[]` |
| `IceCandidatePairMonitor` | candidate-pair states, nomination, connectivity checks, RTT, throughput/BWE, endpoint refs | `iceCandidatePairs[]` |
| `CertificateMonitor` | certificate fingerprint/algorithm/base64 and issuer reference | `certificates[]` |
| `DataChannelMonitor` | data-channel state, label, protocol, identifier, messages/bytes | `dataChannels[]` |
| `PeerConnectionTransportMonitor` | peer-connection report: `dataChannelsOpened`/Closed | `peerConnectionTransports[]` |
| `InboundTrackMonitor` / `OutboundTrackMonitor` | `MediaStreamTrack` binding, context, aggregate/derived values; no matching browser track report assumed | `inboundTracks[]` / `outboundTracks[]`, limited projection |
| `PeerConnectionMonitor` | graph owner and aggregate, not the browser's peer-connection report | PC envelope |
| `ClientMonitor` | cross-PC aggregates, events, issues, extensions and score | `ClientSample` root |
| `ExtensionStatsMonitor` | application-defined payload, identity and freshness | `extensionStats[]` at root |
| `SelectedIcePath` | history/view over selected ICE tuple and its evidence | no dedicated sample record |

{{< details "Source references" >}}

- [client-monitor-js/src/monitors/PeerConnectionMonitor.ts · createSample](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L924)
- [schemas/sources/samples/PeerConnectionSample.chunk.avsc](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

{{< /details >}}

The full field inventory is intentionally not reduced to the above examples.

## Core formulas

Let `Δx = positiveDelta(current, previous)`, `dtMs = current.timestamp − previous.timestamp`, `dt = dtMs/1000`. `positiveDelta` returns **undefined**, not zero, on missing inputs or a backwards counter. Each consumer may handle that differently; some explicitly coalesce to zero. Read the formula appendix for every assignment and its guards.

| Value | Implemented calculation / scope |
|---|---|
| RTP bitrate | `max(0, Δbytes × 8 / dt)` |
| RTP packet rate | `Δpackets / dt` |
| Outbound `payloadBitrate` | `max(0, (ΔbytesSent − ΔheaderBytesSent − (ΔretransmittedBytesSent ?? 0)) × 8 / dt)`; this is the implementation even if the field name invites a different byte accounting assumption |
| Inbound `deltaFractionLost` | `Δlost/(Δlost+Δreceived)` only when both deltas are present and both are positive; otherwise zero in that guarded block. This means all-loss/zero-received is not represented as 1 by this expression |
| Remote inbound `deltaFractionLost` | `Δlost/(Δlost+Δreceived)` when denominator >0, else 0; no-new-RTCP-report resets interval readings |
| `BitPerPixel` | `bitrate/(width × height × framesPerSecond)` with truthy geometry/fps/bitrate gates |
| Inbound `avgFramesPerSec` | mean of last at most 10 truthy browser FPS readings |
| `fpsVolatility` | mean absolute deviation of those FPS readings divided by their mean; deprecated |
| `ewmaFps` | existing EWMA ×0.9 + new FPS ×0.1; first/truthy-state handling matters |
| `interFrameDelayVariation` | `sqrt(max(0, ΔsquaredGap/N − (Δgap/N)²)) / (Δgap/N)`, N=`ΔframesDecoded`, N>1 |
| `inventedSpeechRatio` | `max(0, ΔconcealedSamples − (ΔsilentConcealedSamples ?? 0)) / ΔtotalSamplesReceived` |
| `timeStretchRate` | `((ΔinsertedSamplesForDeceleration ?? 0)+(ΔremovedSamplesForAcceleration ?? 0))/ΔtotalSamplesReceived`; a fraction, not per-second rate |
| `concealmentEventRate` | `ΔconcealmentEvents/dt` |
| `discardRate` | `ΔpacketsDiscarded/(ΔpacketsDiscarded+(ΔpacketsReceived ?? 0))`; zero if consumed count is zero |
| `avgJitterBufferDelayInMs` | `1000 × ΔjitterBufferDelay / ΔjitterBufferEmittedCount` |
| `jitterBufferTargetDelayInMs` | analogous target-delay delta / emitted count ×1000 |
| `decodeTimePerFrameInMs` | `1000 × ΔtotalDecodeTime / ΔframesDecoded` |
| `avgEncodeTimePerFrameInMs` | `1000 × ΔtotalEncodeTime / ΔframesEncoded` |
| `avgQpPerFrame` | ΔqpSum divided by decoded/encoded frames, depending on direction |
| `normalizedQp` | inbound average QP divided by codec scale from `qpScaleOf`, clamped 0..1; unknown codec => undefined |
| `droppedFrameRatio` / `renderRatio` | ΔframesDropped/ΔframesReceived; ΔframesRendered/ΔframesDecoded |
| `frozenTimeRatio` / `pausedTimeRatio` | ΔtotalFreezesDuration/dt; ΔtotalPausesDuration/dt |
| `keyFrameRate`, PLI/FIR/NACK rates | corresponding counter delta / dt |
| `retransmissionRatio` | retransmitted byte delta / total byte delta, capped at 1; zero/undefined behavior differs by direction |
| `avgPacketSendDelayInMs` | `1000 × ΔtotalPacketSendDelay/ΔpacketsSent` |
| `qualityLimitationDurationShares` | nonnegative deltas of none/cpu/bandwidth/other divided by sum of those deltas; undefined for no progress |
| source `producedFps` | nonnegative Δsource.frames/dt |
| source `rmsAudioLevel` | `sqrt(ΔtotalAudioEnergy/ΔtotalSamplesDuration)` when duration >0 |
| `playoutDelayPerSampleInMs` | `1000 × ΔtotalPlayoutDelay/ΔtotalSamplesCount` |
| `synthesizedSamplesRatio` | ΔsynthesizedSamplesDuration/ΔtotalSamplesDuration, with explicit fallback behavior in `MediaPlayoutMonitor` |
| ICE mean RTT | ΔtotalRoundTripTime/ΔresponsesReceived |
| RTCP mean RTT | ΔtotalRoundTripTime/ΔroundTripTimeMeasurements |

{{< details "Source references" >}}

- [client-monitor-js/src/utils/common.ts · positiveDelta](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/common.ts#L54)
- [client-monitor-js/src/monitors/InboundRtpMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L322)
- [client-monitor-js/src/monitors/OutboundRtpMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L174)
- [client-monitor-js/src/monitors/RemoteInboundRtpMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L97)
- [client-monitor-js/src/monitors/MediaSourceMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L82)
- [client-monitor-js/src/monitors/MediaPlayoutMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L72)
- [client-monitor-js/src/monitors/IceCandidatePairMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L95)
- [client-monitor-js/src/utils/quantizer.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/quantizer.ts)

{{< /details >}}

## Aggregates and transport stability

PC sums distinguish audio/video/data-channel directions. Quality-loss averages include streams that actually carried relevant packets; missing measurement differs from zero loss. RTT paths are kept separate (`rtcpRttInSec`, `iceRttInSec`), with current RTT preferring RTCP and falling back to ICE. Root `avgRttInSec` averages PC values and returns -1 with no PCs. PC legacy loss sums and newer per-stream means are not interchangeable.

{{< details "Source references" >}}

- [client-monitor-js/src/monitors/PeerConnectionMonitor.ts · _updateTransportQualityAverages](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1253)
- [client-monitor-js/src/ClientMonitor.ts · collect](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L610)

{{< /details >}}

`transportStability` is the normalized MOS-like value produced by `utils/transportStability.ts`: effective latency is RTT/2 + 2×jitter +10 ms; a piecewise latency impairment and 2.5×loss-percent reduce R; a cubic maps clamped R to MOS; normalized against this model's best/worst MOS. It requires all three measurements. It is not a direct measurement of user satisfaction or a selected-pair-switch counter. [client-monitor-js/src/utils/transportStability.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/transportStability.ts).

## Missing values and resets

There is no single universal nullification pass. The current code uses several distinct mechanisms:

- Missing raw inputs: `InboundRtpMonitor` explicitly replaces known fields, including undefined; several other monitors use `Object.assign` and can retain omitted properties. Derived assignments are conditional, so some previous derived values can remain. Do not promise universal freshness without checking the owner.
- Backwards counters: `positiveDelta` returns undefined; `MediaPlayoutMonitor` explicitly converts some such deltas to zero. Remote RTCP repeated/stale timestamps clear interval readings. Inbound repeated timestamps replace raw fields but return before recomputing derived values; outbound returns earlier.
- Shared windows: `SlicedWindow` uses null for unavailable totals, rejects repeated timestamps, resets across excessive gaps and requires full slices. N samples span N−1 intervals. Detection/recovery are different slices; inspect their configured offsets rather than assuming a trailing duration in milliseconds.
- Paused/ended/background/muted tracks: individual detectors stand down according to their own guards. There is no blanket rule that every detector handles every gate identically. Missing-input branches can preserve an open issue while publishing `inputsUnavailable`, whereas some detectors resolve it.
- Zero score: full-scale deductions clamp the affected component to zero. Connectivity issues are deliberately not charged again on the PC; dry-track issues can zero media components. There is no global “any network fault nullifies every score” rule.
- Aggregate absent dimensions: undefined/null dimensions are omitted from client RMSE; no measurable dimensions causes calculator early return, leaving the root's previous/default `score`, which starts at 5. This differs from documentation saying the root necessarily becomes undefined.
- Wire absence: undefined properties disappear under JSON serialization; Avro nullable fields and generated TS optional fields are separate representations. On-change ICE omissions must be retained by the receiver, but current observer code does not retain them ([known limitations](/docs/reference/known-differences/)).

{{< details "Source references" >}}

- [client-monitor-js/src/utils/SlicedWindow.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/SlicedWindow.ts)
- [client-monitor-js/src/monitors/InboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts)
- [client-monitor-js/src/monitors/OutboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts)
- [client-monitor-js/src/monitors/RemoteInboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts)
- [client-monitor-js/src/monitors/MediaPlayoutMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts)
- [client-monitor-js/src/scores/DefaultScoreCalculator.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/DefaultScoreCalculator.ts)

{{< /details >}}

[Browse the monitor catalog →](/docs/reference/monitor-catalog/)
