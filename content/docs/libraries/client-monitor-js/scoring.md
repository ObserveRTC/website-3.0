---
title: "Quality scoring"
slug: "scoring"
description: "How the 0–5 quality score is calculated and how to replace it"
lead: "A single number per client, per peer connection and per track — with a machine-readable explanation of every penalty"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 315
toc: true
---

Every collecting tick the monitor recomputes a **score** between `0.0` (worst) and `5.0` (best)
for each track, each peer connection and the client as a whole, plus a `scoreReasons` object that
attributes the loss to named causes.

```javascript
monitor.on("score", ({ clientScore, scoreReasons }) => {
    // clientScore: 3.2
    // scoreReasons: { "high-rtt": 1.0, "high-packetloss": 0.8 }
});

monitor.score;                              // current client score
monitor.scoreReasons;                       // current breakdown
peerConnectionMonitor.calculatedStabilityScore;
trackMonitor.calculatedScore;
```

Scores also travel in every [`ClientSample`](/docs/schema/clientsample/) — at client, peer
connection and track level — so a server can aggregate them without recomputing anything.

{{< callout context="tip" title="What a score is for" icon="rocket" >}}
A score is a **ranking device**, not a physical measurement. It is what you chart over time, sort
sessions by, and alert on when a percentile drops. When you need to know *what* was wrong, read
the `scoreReasons` or the [issues](../events-and-issues/) — that is what they are for.
{{< /callout >}}

## The default model

`DefaultScoreCalculator` computes the client score as a weighted average over peer connections,
where each peer connection's contribution is its own stability score modulated by the quality of
the tracks running over it.

```text
Client Score  =  Σ(PC_Score × PC_Weight) / Σ(PC_Weight)

PC_Score      =  Track_Score_Avg × PC_Stability_Score
```

### Peer connection stability

Driven by round-trip time and packet loss on that connection.

| Condition | Penalty |
|---|---|
| RTT 150–300 ms | −1.0 |
| RTT > 300 ms | −2.0 |
| Packet loss 1–5 % | −1.0 |
| Packet loss 5–20 % | −2.0 |
| Packet loss > 20 % | −5.0 |

### Inbound audio track

Logarithmic bitrate normalisation with exponential decay for loss:

```javascript
normalizedBitrate = log10(max(bitrate, MIN_AUDIO_BITRATE) / MIN_AUDIO_BITRATE) / NORMALIZATION_FACTOR;
lossPenalty       = exp(-packetLoss / 2);
score             = min(MAX_SCORE, 5 * normalizedBitrate * lossPenalty);
```

The logarithm matters: the difference between 8 kbps and 16 kbps is enormous perceptually, while
the difference between 48 and 56 kbps is not. A linear model would rank those wrongly.

### Inbound video track

Penalised for frame-rate volatility, dropped frames and frame corruption.

### Outbound audio track

Same shape as inbound, computed from the sending bitrate and the packet loss the **remote** peer
reports back over RTCP.

### Outbound video track

Penalised for deviation from the target bitrate, CPU limitation, and bitrate volatility.

{{< callout context="note" title="Screen share is scored differently" icon="info-circle" >}}
When `track.contentHint === 'screen'`, bitrate-deviation and volatility penalties are skipped.
Screen share traffic is legitimately spiky — near zero on a static slide, a burst on a scroll — and
scoring it like camera video produces a permanently bad number for a perfectly good stream.
{{< /callout >}}

## Score reasons

`scoreReasons` maps a cause name to the number of points it removed:

```javascript
monitor.on("score", ({ clientScore, scoreReasons }) => {
    console.log(clientScore);   // 1.2
    console.log(scoreReasons);
    // {
    //   "high-rtt": 1.0,
    //   "high-packetloss": 2.0,
    //   "cpu-limitation": 2.0,
    //   "dropped-video-frames": 1.0
    // }
});
```

Because it is a plain object of numbers, it aggregates cleanly: sum the reasons across a call to
see what actually cost your users quality this week.

## Replacing the calculator

Assign any object implementing `ScoreCalculator` to `monitor.scoreCalculator`. Its `update()` is
called once per collecting tick, after metrics are derived and detectors have run.

```typescript
interface ScoreCalculator {
    update(): void;
    encodeClientScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
    encodePeerConnectionScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
    encodeInboundAudioScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
    encodeInboundVideoScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
    encodeOutboundAudioScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
    encodeOutboundVideoScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
}
```

The `encode*` methods control how reasons are serialised into the sample's string
`scoreReasons` fields — override them if you want a compact format instead of JSON.

### A worked replacement

```javascript
import { ScoreCalculator } from "@observertc/client-monitor-js";

class CustomScoreCalculator {
    constructor(clientMonitor) {
        this.clientMonitor = clientMonitor;
    }

    update() {
        for (const pc of this.clientMonitor.peerConnections) this.scorePeerConnection(pc);
        for (const track of this.clientMonitor.tracks) this.scoreTrack(track);
        this.scoreClient();
    }

    scorePeerConnection(pcMonitor) {
        const rttMs = (pcMonitor.avgRttInSec ?? 0) * 1000;
        const fractionLost = pcMonitor.inboundRtps
            .reduce((acc, rtp) => acc + (rtp.fractionLost ?? 0), 0);

        let score = 5.0;
        const reasons = {};

        if (rttMs > 200) { score -= 1.5; reasons["custom-high-rtt"] = 1.5; }
        if (fractionLost > 0.02) { score -= 2.0; reasons["custom-packet-loss"] = 2.0; }

        pcMonitor.calculatedStabilityScore.value = Math.max(0, score);
        pcMonitor.calculatedStabilityScore.reasons = reasons;
    }

    scoreTrack(trackMonitor) {
        let score = 5.0;
        const reasons = {};

        if (trackMonitor.direction === "inbound" && trackMonitor.kind === "video") {
            const fps = trackMonitor.getInboundRtp()?.ewmaFps ?? 0;
            if (fps < 15) { score -= 2.0; reasons["low-fps"] = 2.0; }
        }

        trackMonitor.calculatedScore.value = Math.max(0, score);
        trackMonitor.calculatedScore.reasons = reasons;
    }

    scoreClient() {
        let total = 0, weight = 0;
        const combined = {};

        for (const pc of this.clientMonitor.peerConnections) {
            const s = pc.calculatedStabilityScore;
            if (s.value === undefined) continue;
            total += s.value;
            weight += 1;
            Object.assign(combined, s.reasons ?? {});
        }

        this.clientMonitor.setScore(weight > 0 ? total / weight : 5.0, combined);
    }

    encodeClientScoreReasons(reasons) {
        return JSON.stringify(reasons ?? {});
    }
}

monitor.scoreCalculator = new CustomScoreCalculator(monitor);
```

### When to replace it

- **Your product has a dominant modality.** An audio-first product should not lose points for
  video frame drops; a screen-share product cares about text legibility, not frame rate.
- **You have ground truth.** If you collect user-reported quality ratings, fit the model to them —
  a score that correlates with what users actually say is worth far more than a generic one.
- **You need stability over sensitivity.** Aggressive per-tick scoring produces noisy charts. Add
  smoothing in your own calculator rather than post-processing downstream.

## Setting the score directly

If your quality signal comes from somewhere else entirely — a media-quality model, a user
thumbs-down, a server-side measurement pushed back to the client — set it and skip the calculator:

```javascript
monitor.setScore(2.5, { "user-reported-bad": 2.5 });
```

The value ships in the next sample like any computed score.
