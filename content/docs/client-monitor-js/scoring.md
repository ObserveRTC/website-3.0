---
slug: "scoring"
title: "Quality scores"
description: "Read the 0\u20135 component scores and understand how they aggregate."
lead: "Read the 0\u20135 component scores and understand how they aggregate."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 70
toc: true
---

`DefaultScoreCalculator.update()` computes PC stability, track scores, then client score. A component starts from 5 and subtracts applicable penalties, clamped at 0. Track weight and PC stability weight feed dimension means. Five dimensions are PC stability, inbound audio/video, outbound audio/video. Client score is:

```text
dimension = sum(componentScore × weight) / sum(weight)
client = roundTo2(clamp(5 − sqrt(mean((5 − dimension)²)), 0, 5))
```

Missing dimensions are excluded. `[5,5,0]` therefore gives 2.11, not arithmetic mean 3.33. The server's `DefaultCallScoreCalculator` is a **weighted arithmetic mean of client scores**, not the same RMSE rule. [client-monitor-js/src/scores/DefaultScoreCalculator.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/DefaultScoreCalculator.ts), [observer-js/src/scores/DefaultCallScoreCalculator.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/scores/DefaultCallScoreCalculator.ts).

Important costs include dry tracks/stuck decoder/frame-assembly stall at 5; PC sustained loss and delay at 2.5 each; directional congestion at 2.5×max(severity, configured minimum); PC continuous instability at `2×(1−transportStability)`; decoder bottleneck at 2×clamped degradation. Track-specific video/capture/encode/freeze/pixelation/audio costs and all continuous ramps are preserved in the [source atlas](/reference/source-atlas.html) and [formula reference](/reference/monitor-fields-and-formulas.md). Pixelation weight depends on displayed magnification: ≥1.5 =>1.5×, <0.75=>0.25×, otherwise1×. No presented size means ordinary weight, not suppression.

The calculator is **not issues-only**, despite its opening comment. It also charges continuous frame timing, frame drops, quantization, audio instability, target-bitrate deviation, screen-share downscale and transport stability. Continuous reason names are exposed only when their total exceeds 1 point, unless an issue is active; score reductions may exist with no published reasons. Root sample reasons are only root-owned reasons; the default RMSE adds no root reason, while the score event carries aggregated component reasons. `sampledScoreReasons()` copies the object and honors explicit false. Sources: [client-monitor-js/src/scores/DefaultScoreCalculator.ts · reasonsOf](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/DefaultScoreCalculator.ts#L298), [client-monitor-js/src/scores/utils.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/utils.ts), [client-monitor-js/src/ClientMonitor.ts · setScore](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L722).
