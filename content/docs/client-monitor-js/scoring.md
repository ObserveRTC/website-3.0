---
slug: "scoring"
title: "Quality scores"
description: "Read the 0\u20135 component scores and understand how they aggregate."
lead: "Read the 0\u20135 component scores and understand how they aggregate."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "Markdown"]
weight: 75
toc: true
---

## What a quality score tells you

A quality score summarizes the signals the monitor can observe on a scale from **0 to 5**. Higher values mean fewer measured penalties; lower values help you find clients and tracks that need attention. It is an engineering health indicator, not a guarantee of what a person hears or sees.

Use the score for an overview, then inspect the track metrics, active issues, and score reasons to explain a change. A healthy connection with unavailable browser measurements still has limited evidence, even if its score is high.

## Where scores are available

| Scope | What it summarizes |
|---|---|
| Peer connection | Stability and health of the transport used for media. |
| Inbound audio/video track | Media received and played by this client. |
| Outbound audio/video track | Media captured and sent by this client. |
| Client | Connection stability together with sending and receiving quality. |
| Call in Observer | A weighted average of the participating clients’ scores. |

## Why a bad track affects the overall score

The client calculator gives substantial weight to poor quality in any available dimension. For example, dimension scores of 5, 5, and 0 produce a client score of 2.11, rather than the arithmetic average of 3.33. This helps a severe problem remain visible even while other parts of a call work well. Dimensions with no data are excluded.

## How to use score reasons

Reasons identify penalties associated with a component. Read them alongside the relevant track or peer connection; the root sample does not automatically contain every child’s reasons. Setting `sendScoreReasonsToServer: false` reduces sample detail without turning off scores or the local `score` event.

A score can fall without an issue being raised. Some penalties follow continuous measurements, and small accumulated penalties may not publish a reason yet. Do not interpret an empty reasons list as proof that all media was perfect.

## Calculation reference

`DefaultScoreCalculator.update()` computes PC stability, track scores, then client score. A component starts from 5 and subtracts applicable penalties, clamped at 0. Track weight and PC stability weight feed dimension means. Five dimensions are PC stability, inbound audio/video, outbound audio/video. Client score is:

```text
dimension = sum(componentScore × weight) / sum(weight)
client = roundTo2(clamp(5 − sqrt(mean((5 − dimension)²)), 0, 5))
```

Missing dimensions are excluded. `[5,5,0]` therefore gives 2.11, not arithmetic mean 3.33. The server's `DefaultCallScoreCalculator` is a **weighted arithmetic mean of client scores**, not the same RMSE rule.

{{< details "Source references" >}}

- [client-monitor-js/src/scores/DefaultScoreCalculator.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/DefaultScoreCalculator.ts)
- [observer-js/src/scores/DefaultCallScoreCalculator.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/scores/DefaultCallScoreCalculator.ts)

{{< /details >}}

## Penalties

| Example evidence | Effect on the score |
|---|---|
| A dry track, stuck decoder, or stalled frame assembly | A severe penalty of 5 points for the affected component. |
| Sustained connection loss or delay | A penalty of 2.5 points for each condition. |
| Directional congestion | A penalty scaled by congestion severity. |
| Transport instability or decoder degradation | A continuous penalty that follows the measured degradation. |
| Pixelation | A penalty whose weight also depends on how much the video is magnified on screen. |

The calculator also evaluates capture, encoding, freezes, frame drops, and audio behavior. The [formula reference](/reference/monitor-fields-and-formulas.md) preserves the exact calculations for the documented baseline. Use component scores to locate the affected part of the pipeline rather than reading a client score as the diagnosis by itself.

## Detailed reason behavior

The calculator is **not issues-only**, despite its opening comment. It also charges continuous frame timing, frame drops, quantization, audio instability, target-bitrate deviation, screen-share downscale and transport stability. Continuous reason names are exposed only when their total exceeds 1 point, unless an issue is active; score reductions may exist with no published reasons. Root sample reasons are only root-owned reasons; the default RMSE adds no root reason, while the score event carries aggregated component reasons. `sampledScoreReasons()` copies the object and honors explicit false. Sources: [client-monitor-js/src/scores/DefaultScoreCalculator.ts · reasonsOf](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/DefaultScoreCalculator.ts#L298), [client-monitor-js/src/scores/utils.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/utils.ts), [client-monitor-js/src/ClientMonitor.ts · setScore](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L722).
