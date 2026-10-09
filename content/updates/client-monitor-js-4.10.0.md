---
title: "Client Monitor 4.10.0"
date: "2026-10-04T16:53:02Z"
draft: false
project: "Client Monitor"
version: "4.10.0"
summary: "Loopback audio detection, SDP monitoring, audio input metadata, and changes to audio concealment and interruption detection."
releaseUrl: "https://github.com/ObserveRTC/client-monitor-js/releases/tag/4.10.0"
author: "balazskreith"
---
## LoopbackAudioInputDetector — loopback-audio-input

A new Pipeline Disruption detector on outbound audio tracks. It raises `loopback-audio-input` when the
capture device's label names a loopback of the machine's own output (`Monitor of …` on
`PulseAudio`/`PipeWire`, `Stereo Mix` / `Wave Out Mix` / `What U Hear` on Windows). The far end hears
itself on such a call while every stat looks healthy. A label never changes, so each track is judged
once and the detector then removes itself from the track's registry. Config: `loopbackAudioInputDetector.labelPatterns`,
defaulting to `DEFAULT_LOOPBACK_AUDIO_INPUT_LABEL_PATTERNS`. Track attribute:
`OutboundTrackMonitor.loopbackAudioInput`.

## AUDIO_INPUT_DEVICE client metadata

Each outbound audio track now sends one `AUDIO_INPUT_DEVICE` meta item when it is first monitored:
`{ peerConnectionId, trackId, label, deviceId?, groupId? }`. It reaches the server whichever source
binding created the track, unlike `MEDIA_TRACK_ADDED`. `ClientMetaTypes` and `AudioInputDevice` are now
exported.

## New: session descriptions — SdpMonitor

`ClientMonitor.acceptLocalDescription(peerConnectionId, description)` and
`acceptRemoteDescription(...)` hand an applied description to the peer connection's new
`PeerConnectionMonitor.sdp` (`SdpMonitor`, which has the same two methods). Each accepted
description is added to the sample as `LOCAL_SDP` / new `REMOTE_SDP` metadata, payload
`{ peerConnectionId, type, sdp }` with `a=ice-pwd` redacted; identical repeats and rollbacks are
ignored.

What it reads is published on `PeerConnectionMonitor`: `negotiationRole`, `dtlsRole`,
`remoteIceLite`, `localIceLite`, `bundled`, `negotiatedAudioCodecs`, `negotiatedVideoCodecs`,
`sendingAudioDtx`, `receivingAudioDtx`, `sendingAudioInbandFec`, `receivingAudioInbandFec`,
`audioRedNegotiated`, `sendingSimulcast`; per media section on
`sdp.negotiatedMediaSections`. The parser (`parseSdp`) is exported. No new dependency.

Sources feed it automatically: `RtcPeerConnectionBinding` and `MediasoupTransportBinding` read the
connection's descriptions when bound and on every `signalingstatechange`. The mediasoup binding
reaches the connection through mediasoup-client's private `transport.handler._pc`
(`peerConnectionOfTransport`); a handler without one is monitored as before, without SDP.

## Breaking: InventedSpeechDetector renamed to ConcealedSamplesDetector

"Concealed samples" is the term audio engineers recognise — it is what the W3C stats
(`concealedSamples`, `silentConcealedSamples`) and `NetEQ` call it. "Invented speech" also
overstated what the detector sees; see the next section. Straight rename, same algorithm,
**no aliases** for any of the old names.

| 4.9.x | 4.10.0 |
|---|---|
| `InventedSpeechDetector` / `invented-speech-detector` | `ConcealedSamplesDetector` / `concealed-samples-detector` |
| issue type and monitor event `invented-speech` | `concealed-samples` |
| config `inventedSpeechDetector` | `concealedSamplesDetector` |
| `allowedInventedRatio`, `raiseAfterInventedMs` | `allowedConcealedRatio`, `raiseAfterConcealedMs` |
| `InboundRtpMonitor.inventedSpeechRatio` | `nonSilentConcealedRatio` |
| payload `inventedSpeechRatio`, `excessInventedMs` | `nonSilentConcealedRatio`, `excessConcealedMs` |
| `InboundTrackMonitor.inventedSpeechSeverity` | `concealedSamplesSeverity` |
| `DefaultScoreCalculator.INVENTED_SPEECH_ACTIVATION` / `_SATURATION` | `CONCEALED_SAMPLES_ACTIVATION` / `_SATURATION` |
| score reason `invented-speech` | `concealed-samples` |
| `InventedSpeechIssuePayload`, `InventedSpeechEventPayload`, `InventedSpeechDetectorConfig` | `ConcealedSamples…` |

The issue payload gains `concealmentEventRate`, so a few longer gaps can be told from
constant micro-concealment.

## Why the old detector could not see dropouts

`NetEQ` fades concealment out: the mute slope steepens on the 3rd and 7th consecutive expand,
and the output reaches zero after roughly 60–120 ms. From then on libwebrtc counts every
concealed sample as `silentConcealedSamples` — the same bucket as DTX comfort noise, which
the detector has to subtract. So each concealment event adds at most ~100 ms to the ratio
however long the gap lasts, and a two-second dropout was nearly invisible. What the detector
actually finds is **frequent short gaps** (choppy audio), and it is now documented as such.

## New: AudioInterruptionDetector — audio-interruption

Reports dropouts of 150 ms and longer, from Chromium's non-standard `inbound-rtp`
`interruptionCount` / `totalInterruptionDuration` (libwebrtc counts every concealment event
of at least 150 ms, silent part included). Same leaky-accumulator shape as its sibling:
`allowedInterruptedRatio: 0.02`, `raiseAfterInterruptedMs: 500`. The interruption that ends
when a paused stream resumes is discarded. Chromium only; elsewhere it reports
`inputsUnavailable`. Config `audioInterruptionDetector`, monitor event `audio-interruption`,
charged in `DefaultScoreCalculator` as `audioInterruptionSeverity × AUDIO_INTERRUPTION_MAX_CHARGE` (2).

New on `InboundRtpMonitor`: `interruptionCount`, `totalInterruptionDuration`,
`deltaInterruptionCount`, `deltaTotalInterruptionDurationInMs`. They are not added to the
sample schema.

---

Source: [GitHub release 4.10.0](https://github.com/ObserveRTC/client-monitor-js/releases/tag/4.10.0). Published at 2026-10-04T16:53:02Z (UTC).
