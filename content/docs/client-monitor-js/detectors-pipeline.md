---
slug: "detectors-pipeline"
title: "Pipeline Disruption detectors"
description: "Capture, encoding, delivery, decoding and playout failures."
lead: "Capture, encoding, delivery, decoding and playout failures."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 83
toc: true
---

| Class | Default / trigger | Recovery / important gates |
|---|---|---|
| [CaptureSourceLostDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CaptureSourceLostDetector.ts#L40) | sourceEnded capture flag; one-shot capture-source-lost | one-shot, not a continuously resolved threshold episode |
| [SilentAudioSourceDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/SilentAudioSourceDetector.ts#L106) | live enabled unmuted microphone/device; RMS≤0.0001 for 60000 ms captured audio | RMS>0.0003 when raised; pause, screen share, lost input, ended source stand down |
| [VideoCaptureBottleneckDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/VideoCaptureBottleneckDetector.ts#L97) | `1 − producedFps/expectedCaptureFps >0.2` over shared detection slice | recovery slice within threshold; settings changes, screen share, inactive tab/muted/paused source stand down |
| [EncoderBottleneckDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/EncoderBottleneckDetector.ts#L113) | highest layer `1 − encodedFps/producedFps >0.3` | recovery slice within threshold; source/layer/config-change gates |
| [RtpSenderStalledDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/RtpSenderStalledDetector.ts#L51) | frames encode but no RTP packets leave for 4000 ms | packets resume, stream disappears or guarded state; per-SSRC state |
| [DryOutboundTrackDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DryOutboundTrackDetector.ts#L78) | active layer byte deltas sum to zero for 5000 ms | data resumes; pause/mute/end/encoder limitation/no active layer stand down |
| [TransportDemuxStalledDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/TransportDemuxStalledDetector.ts#L52) | transport receives ≥20000 bps while existing inbound RTP accounts for zero bytes, 4000 ms | RTP progress, missing transport or failed guards; per-transport state |
| [DryInboundTrackDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DryInboundTrackDetector.ts#L39) | incoming byte delta zero for 5000 ms | bytes resume, local/remote declared pause, ended track |
| [FrameAssemblyStalledDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/FrameAssemblyStalledDetector.ts#L44) | packets arrive, framesReceived flat; ≥20 packets and ≥3000 ms | complete frame arrives or stand-down gates |
| [DecoderBottleneckDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DecoderBottleneckDetector.ts#L126) | received frame supply≥5 fps, decoding shortfall>0.1 over shared window | recovery window catches up; dropped-frame and foreground/context gates distinguish causes |
| [DecoderPerformanceDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DecoderPerformanceDetector.ts#L73) | decode time >0.8×frame budget, ≥10 received frames, interval loss≤0.02, 2 ticks | decode keeps up, insufficient frames, loss dominates, ended/background |
| [StuckDecoderDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/StuckDecoderDetector.ts#L66) | no decoded frames with bitrate≥10000, ≥2 PLIs, elapsed≥max(4000 ms,15×RTT) | decoded frames return or source/context/foreground gates; records assembly evidence |
| [PlayoutDiscrepancyDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/PlayoutDiscrepancyDetector.ts#L63) | received-vs-rendered frame skew≥0.25 with ≥10 frames in detection window | skew<0.1 or stand-down; despite prose mentioning decode-to-render, inspect actual operands |
| [VideoRecoveryFailedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/VideoRecoveryFailedDetector.ts#L44) | stalled picture/keyframe recovery, ≥2 PLIs, ≥5000 ms | video recovery or guards; repair-loop diagnosis separate from perceptual freeze |
| [CpuPerformanceDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CpuPerformanceDetector.ts#L104) | measurable software encode/decode utilization at least 0.5 across client detection window | recovery below 0.4; background/no CPU-backed work/no measurement stand down |

Sources: named files under [client-monitor-js/src/detectors/Detectors.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/Detectors.ts), plus the full algorithms in the [detector implementation reference](/reference/detector-implementation-reference.md). Shared-window readiness and total-vs-delta choices are material to all capture/encoder/decoder comparisons.
