---
slug: "detectors-telemetry"
title: "Telemetry detectors"
description: "State changes and collection-health events."
lead: "State changes and collection-health events."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 85
toc: true
---

| Class | Observation | State / defaults |
|---|---|---|
| [IceTraversalDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceTraversalDetector.ts#L26) | selected tuple set changes | remembers tuple set; no first-observation change event; no issue |
| [IceRestartDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceRestartDetector.ts#L53) | local ICE username fragment changes, restart outcome | per-transport generation/pending state; createEvent true |
| [IceRestartRecommendationDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceRestartRecommendationDetector.ts#L87) | failed, disconnected/stalled≥10000 ms, or never-established≥10000 ms | cooldown 15000 ms; pending restart gates; recommendation event, does not itself restart ICE |
| [CaptureTrackMutedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CaptureTrackMutedDetector.ts#L28) | previously known unmuted→muted transition | track muted state; createEvent true; distinct from application mute |
| [CodecChangeDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CodecChangeDetector.ts#L26) | MIME/FMTP change | previous codec signature; first value establishes baseline |
| [VideoResolutionChangeDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/VideoResolutionChangeDetector.ts#L34) | positive frame width/height changes | prior geometry; includes direction and outbound limitation context |
| [SimulcastLayerDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/SimulcastLayerDetector.ts#L45) | set of actively sending layer keys changes | multiple encoding requirement; paused/end reset |
| [StatsGapDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/StatsGapDetector.ts#L34) | actual collection period >2×expected AND >5000 ms | prior collection start time; no issue, createEvent true |

Source files are preserved in the [detector implementation reference](/reference/detector-implementation-reference.md) and [client-monitor-js/docs/TELEMETRY_DETECTORS.md](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/docs/TELEMETRY_DETECTORS.md). Telemetry can have thresholds (StatsGap and restart recommendations); prose saying it has none is too broad.
