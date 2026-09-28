---
slug: "detectors-perceived-quality"
title: "Perceived Quality detectors"
description: "Visible and audible degradation, including synchronization."
lead: "Visible and audible degradation, including synchronization."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 84
toc: true
---

| Class | Default / trigger | Recovery / evidence |
|---|---|---|
| [PixelatedVideoDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/PixelatedVideoDetector.ts#L75) | normalized QP≥0.62 for 8000 ms | QP<0.52; no QP/unknown codec/pause/end/screenshare stand down; **not bitPerPixel** |
| [InboundVideoFlowStateDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/InboundVideoFlowStateDetector.ts#L92) | shared flow slice: continuous/longest freeze≥2000 ms => frozen; ≥2 freezes => choppy | frozen clears on moving picture; choppy needs freeze-free recovery slice; mutually exclusive payload state |
| [InventedSpeechDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/InventedSpeechDetector.ts#L55) | bucket `clamp(bucket+(inventedRatio−0.05)×dtMs,0,400)`; full opens invented-speech | empty closes; pause/end discard; missing input marks unavailable |
| [AudioPlayoutSynthesisDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/AudioPlayoutSynthesisDetector.ts#L115) | synthesized duration / played duration>0.05 over track window | recovery ratio≤threshold; needs media-playout measurements; currently raises synthesized-audio |
| [JitterBufferStressDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/JitterBufferStressDetector.ts#L71) | target delay>200 ms AND stretch share>0.02 for 2 ticks | conjunction clears, track stand-downs; severity scales against 1000 ms and 0.15 |
| [AVDesyncPlayoutDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/AVDesyncPlayoutDetector.ts#L60) | explicitly paired audio/video playout timestamps; ahead≥90 ms or behind≥185 ms for 3000 ms | ahead<45 or behind<125; direction-aware hysteresis; missing pairing is unavailable |

Sources: [client-monitor-js/src/detectors/PixelatedVideoDetector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/PixelatedVideoDetector.ts), [client-monitor-js/src/detectors/AudioPlayoutSynthesisDetector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/AudioPlayoutSynthesisDetector.ts), [client-monitor-js/src/detectors/InventedSpeechDetector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/InventedSpeechDetector.ts).
