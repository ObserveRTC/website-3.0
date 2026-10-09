---
title: "Client Monitor 4.5.0"
date: "2026-08-08T10:05:58Z"
draft: false
project: "Client Monitor"
version: "4.5.0"
summary: "Eleven new detectors, ICE connectivity and recovery signals, derived quality metrics, and correctness fixes."
releaseUrl: "https://github.com/ObserveRTC/client-monitor-js/releases/tag/4.5.0"
author: "balazskreith"
---
This release moves the library from collecting WebRTC stats toward *diagnosing* them. Eleven new detectors, a full ICE connectivity layer, and a broad set of derived metrics answer the two questions raw stats never do: **what did the user actually experience**, and **which component is responsible** — the network, the SFU, the device, or the application. No sampling-schema changes: everything new travels through the existing events and issues channels.

---

## ICE connectivity & recovery

**`IceConnectivityDetector`** watches runtime ICE health per ICE transport (a connection without BUNDLE has several, and they fail independently):

- `ice-disconnected` — raised only after `disconnected` persists past a threshold, so the transient blips ICE routinely self-heals never become issues; resolves with the episode duration.
- `ice-connection-failed` — raised immediately on `failed`, which is terminal for that ICE generation.
- `ice-transport-stalled` — deliberately narrow: still *sending* on a succeeded pair but receiving nothing, after inbound traffic had been seen. Silence in both directions is not reported, because it is indistinguishable from an idle connection.
- `unstable-ice-path` — the selected path keeps switching within a sliding window.

**ICE restart support.** The library reports *when* a restart is warranted; performing it stays with the application, which alone knows whether renegotiation is safe. `'ice-restart-recommended'` fires immediately on `failed` and after a threshold for persistent disconnects, stalls, or a connection that never finished establishing (tracked from `connectionState`, so a stuck DTLS handshake is covered too). It carries `reason`, `recommendationCount` and `iceGeneration` so applications can escalate to a rejoin after repeated failed attempts. Restarts themselves are inferred from ICE username-fragment changes and reported as `'ice-restart'` with an outcome of `detected`, `recovered` or `failed`.

**`SelectedIcePath`** is a live view of the transport's current network path (`peerConnectionMonitor.selectedIcePath`). It stores no copies — every getter reads through the linked candidate pair, so it can never disagree with the stats — and classifies path transitions (`initial-selection`, `direct-to-relay`, `relay-to-direct`, `relay-protocol-changed`, `turn-server-changed`, `path-changed`) into the `'ice-path-changed'` event and the `PEER_CONNECTION_ICE_PATH_CHANGED` client event. It also accumulates TURN usage facts: time spent per path kind, time to first relay, switch counts, and the relay share of total traffic. TURN usage is treated as an observation, not an error.

Path semantics now live on the monitors themselves — `IceCandidatePairMonitor` gained `usingTurn`, `usingTcp`, `relayProtocol`, `pathKind`, `turnUrl`, `turnServer`, `tuple` and a switch-stable `pathKey`; `IceCandidateMonitor` gained `isRelay`, `turnTransport`, `turnServer` and `addressFamily` — so every detector reads the same answer from one place.

## Audio quality as the user hears it

- **`AudioConcealmentDetector`** (`audio-concealment`) reports how the audio actually *sounded*, which packet loss does not: Opus + `NetEQ` conceal a great deal of loss inaudibly, and audio also degrades without dramatic loss. The rate counts **audible** concealment only — silent concealment is subtracted, since `concealedSamples` rises during ordinary silence and a raw-counter detector would flag every quiet moment of every call. Episodes are classified `bursty` (choppiness) vs `continuous` (dropouts). Thresholds align with industry voice-quality practice (>3% significant, >5% severe).
- **`JitterBufferStressDetector`** (`audio-jitter-buffer-stress`) fires only when the jitter buffer's target delay has grown **and** `NetEQ` is time-stretching audio. Either alone is the system working; together they are what the user hears.

## Video pipeline: freeze, repair, decode

- **`FreezedVideoTrackDetector`** now owns the whole freeze/repair domain. Freeze semantics were fixed — a freeze now persists until frames actually render again, so `isFreezed` means *currently frozen* and the issue's duration is the real episode length. Two new issues, gated by the `videoRecoveryDetector` config:
  - `keyframe-storm` — a sustained PLI rate. Self-reinforcing: keyframes are several times the size of delta frames, so a burst worsens exactly the congestion that caused it.
  - `video-recovery-failed` — PLIs going out repeatedly, the picture still frozen, keyframes not advancing: the repair request left the client and nothing came back, which points at forwarding rather than the first-hop network.
- **`DecoderPerformanceDetector`** (`video-decoder-overloaded`) blames the client only when frames demonstrably *arrived* — healthy receive rate, quiet loss — but decode time overran a budget derived from the stream's own frame rate, or frames were dropped after arrival. Carries `decoderImplementation` and `powerEfficientDecoder`, since a software decoder on a hardware-capable codec is the most actionable finding.
- **`StuckDecoderDetector`** (`stuck-decoder`) catches the per-consumer decode wedge: RTP bytes keep arriving while nothing decodes and PLIs fire continuously — the "frozen for minutes with gigabytes of dead traffic" failure that only recreating the consumer resolves. The wait is adaptive (`max(4s, 15 × RTT)`, at least 2 stuck collections), the bitrate floor separates it from a merely starved track, and the payload distinguishes an *assembly* wedge (no frame ever reassembled) from a *decode* wedge. The `'stuck-decoder'` event is the hook for the recreate-consumer mitigation.

## Send side: capture, encoder, CPU

- **`SourceEncoderBottleneckDetector`** splits "we are sending fewer frames than we should" into `capture-bottleneck` (the camera/OS never produced the frames) and `encoder-bottleneck` (the source was healthy; the encoder fell behind) by comparing the capture source's own frame production against the highest active encoding — a distinction invisible from RTP alone.
- **`CaptureFailureDetector`** raises `capture-track-ended` (device gone) and `silent-audio-source` (a live, unmuted microphone producing digital silence — the threshold is 30 s on purpose, since only duration separates a dead mic from a quiet person), and emits `'capture-track-muted'` when the OS or another app takes the device. Silence is judged on interval-integrated RMS, not the instantaneous `audioLevel` that reads zero between words.
- **`CpuPerformanceDetector`** gained sustained corroborators — encode time per frame against the stream's frame budget, and the share of the interval spent explicitly CPU-limited — catching pressure the flickery instantaneous `qualityLimitationReason` label misses.

## Observations (events, never issues)

Four detectors record context that is not a fault but is the missing column in most investigations:

- **`CodecChangeDetector`** → `CODEC_CHANGED` — which codec/profile is actually in use and when it changed (compares `sdpFmtpLine` too, so an H264 profile switch is caught).
- **`VideoResolutionChangeDetector`** → `VIDEO_RESOLUTION_CHANGED` — the adaptation ladder, classified `upgrade`/`downgrade`/`reshape`, carrying `qualityLimitationReason` on outbound tracks so encoder adaptation is never confused with an app-driven constraint change.
- **`SimulcastLayerDetector`** → `SIMULCAST_LAYER_CHANGED` — which layers are *actually sending bytes*; a layer marked active that sends nothing is the usual shape of a layer the encoder quietly gave up on.
- **`StatsGapDetector`** → `STATS_COLLECTION_GAP` — flags backgrounded-tab / sleep gaps in stats collection so the accumulated counters after the gap are not misread as a network spike.

## Derived metrics

All computed from fields the monitors already carried — no new collection:

- **Inbound RTP:** `concealmentRate`, `concealmentEventRate`, `timeStretchRate`, `avgJitterBufferDelayInMs`, `jitterBufferTargetDelayInMs`, `discardRate`, `decodeTimePerFrameInMs`, `dropRatio`, `renderRatio`, `keyFrameRate`, `pliRate`/`firRate`/`nackRate`, `retransmissionRatio`.
- **Outbound RTP:** `encodeTimePerFrameInMs`, `retransmissionRatio`, `retransmittedPacketRatio`, `avgQpPerFrame`, `avgPacketSendDelayInMs`, `keyFrameRate`, feedback rates, and `qualityLimitationDurationShares` — what the encoder spent *this interval* doing, in 0..1, unlike the lifetime accumulators.
- **Remote inbound:** `avgRoundTripTimeInSec` from the monotonic totals rather than the noisy last measurement.
- **ICE pair:** `avgRoundTripTimeInSec` from `totalRoundTripTime`/`responsesReceived` deltas.
- **Media source / playout:** `sourceFps`, `rmsAudioLevel`, `playoutDelayPerSampleInMs`, `synthesizedSamplesRatio`.

## Correctness fixes

- **RTT is no longer a blend.** `avgRttInSec` previously mixed RTCP round trips (media path) with ICE/STUN round trips (terminating at the SFU) in a ratio that changed as streams came and went — moving the value for non-network reasons and feeding a false-positive path in congestion detection. The two are now tracked separately with their own EWMAs; `avgRttInSec` prefers RTCP and falls back to ICE, never mixing the two in one tick. RTCP RTT is also now collected from `remote-inbound-rtp`, previously ignored, and ICE RTT is interval-averaged from the selected pair instead of reading a stale last STUN check.
- **Every delta is counter-reset safe.** SSRC reuse, ICE restarts and stats-object replacement reset cumulative counters; unguarded subtraction produced negative deltas that propagated into every derived rate. All monitors now clamp via one shared guard — and on remote-inbound reports this is not merely defensive, since `packetsLost` legitimately decreases when a late packet arrives.
- **`usingTURN` false positive** — two independent candidate scans could match *different* candidates; TURN is now decided per pair from the local candidate type.
- **`audioDesyncDetector` defaults matched their documentation** — the shipped 0.5/0.25 thresholds required half of all samples to be corrected before alerting, which effectively never fired; now 0.1/0.05.
- **A slow connection establishment after a failed attempt is reported again** — the detector previously armed only once per peer connection.
- **An ICE re-failure after a restart is reported** — a restart now closes the previous generation's issues instead of leaving stale state that silenced later findings.

## Calibration & performance

Detector defaults are calibrated for realistic deployments where stats collection runs at ~5 s (windows span several collections; tick-count requirements hold across 1–5 s periods) and validated against production telemetry — notably, the keyframe-storm threshold was lowered to 0.5 PLI/s because a real production storm ran at ~0.65 PLI/s, which the original threshold would have missed.

The hot paths were also tightened: shared delta helper instead of per-tick closures, running-sum sliding windows with hard caps, allocation-free layer lookup, single-pass detector loops. Measured cost: ~1.4 µs for the heaviest monitor update, ~0.2 µs per detector tick — negligible against `getStats()` itself.

## Configuration & migration

- Every new detector has a config block following the existing convention: omit for defaults, pass `null` to disable construction entirely, and flip the instance's `disabled` flag to silence it at runtime.
- New `ClientEventTypes`: `PEER_CONNECTION_ICE_PATH_CHANGED`, `ICE_RESTART`, `ICE_RESTART_RECOMMENDED`, `LONG_PC_CONNECTION_ESTABLISHMENT`, `EXCESSIVE_SYNTHESIZED_AUDIO`, `CODEC_CHANGED`, `VIDEO_RESOLUTION_CHANGED`, `SIMULCAST_LAYER_CHANGED`, `CAPTURE_TRACK_ENDED`, `CAPTURE_TRACK_MUTED`, `STATS_COLLECTION_GAP` — mirror these server-side if you switch on event types.
- New issue types are members of the `ClientMonitorIssue` discriminated union and recognized by `isClientMonitorIssue`.
- Behavior notes: `isFreezed` now means *currently frozen* (persists until rendering resumes) rather than "a freeze started this interval"; `avgRttInSec` may read slightly differently on SFU topologies now that it no longer blends measurement types; `audioDesyncDetector` will actually fire now.
- The sampling schema is unchanged — no server-side schema migration required.

---

Source: [GitHub release 4.5.0](https://github.com/ObserveRTC/client-monitor-js/releases/tag/4.5.0). Published at 2026-08-08T10:05:58Z (UTC).
