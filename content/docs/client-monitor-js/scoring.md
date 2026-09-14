---
title: "Scoring"
description: "How the default 0–5 score is computed, what it charges, and how to replace it"
lead: "As of 4.9 the score is a reading of the open issues — the calculator forms no second opinion"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 250
toc: true
---

Scoring is **pluggable, and the library only defines the contract**:

```typescript
interface ScoreCalculator {
    update(): void;
}
```

`ClientMonitor.scoreCalculator` holds the implementation in use, `update()` is called once per
collection after the detectors have run, and `DefaultScoreCalculator` is assigned at construction so
a monitor scores something out of the box.

{{< callout context="caution" title="The default calculator is a reference implementation, not API" icon="alert-triangle" >}}
There is **no table of issue weights to import**, no config key that retunes a charge, and nothing
else in the library reads the scores it produces. Its numbers are internal. If its judgement does
not suit your application, replace it rather than work around it.

4.9 removed the last score internals that were reachable from outside the package:
`DefaultScoreCalculatorSubtractions`, `DefaultScoreCalculatorSubtractionReason`, the four
`…ScoreAppData` types, and the `VIDEO_QP_THRESHOLDS` / `VIDEO_QP_MAX` / `VideoQpThresholds` exports.
{{< /callout >}}

## The score scale

| Range | Meaning |
|---|---|
| `4.0 – 5.0` | good |
| `3.0 – 4.0` | fair |
| `2.0 – 3.0` | poor |
| `1.0 – 2.0` | bad |
| `0.0 – 1.0` | very bad |

Scores are recalculated on every stats collection, with **no smoothing window**: the published value
is this collection's verdict, not a mean of recent ones.

A score of `undefined` means *too few collections to judge yet*, which is a different statement from
`0` — and it is left out of every aggregate above it.

## The score is a reading of the issues

**As of 4.9 the charges are the open issues and the monitors' own published readings, and nothing
else.** Every monitor starts at `5.0`, the charges below are subtracted, and the result is clamped
at `0.0`. The calculator re-derives no threshold from raw stats: where a detector owns a verdict,
the calculator prices it and does not form a second opinion — so a fault is judged in one place and
**the score cannot disagree with the issue list an operator is looking at**.

This replaced the 4.7-era model, in which the calculator carried its own thresholds — jitter ramps,
per-codec quantizer tables — and could penalise a track no detector had flagged.

Two shapes of charge, and the difference matters when reading a score:

- **Gated on an open issue.** The charge applies only while the issue is open. What it is *worth*
  can still be a continuous reading, so `decoder-bottleneck` costs what the decoder actually fell
  behind by.
- **A continuous reading with no detector behind it.** `volatile-fps`, `dropped-video-frames`,
  `blocky-video`, `frozen-video`, `choppy-video`, `unstable-audio-playout`, `unstable-transport`,
  `downscaled-screenshare` and `high-deviation-from-target-bitrate` exist only in the calculator and
  are named for what they measure. They are what keep a merely mediocre call off a flat `5.0`, since
  a detector says nothing until its threshold is crossed.

A monitor holding no issues scores `5.0`, which is a real statement: its detectors ran and raised
nothing.

## The hierarchy — and the top level is not an average

1. **Every track** scores its own issues and readings into `calculatedScore`.
2. **Every peer connection** scores the state of its path into `calculatedStabilityScore` —
   deliberately not an average of its tracks, but a dimension in its own right.
3. **The client score** collapses five dimensions — the transport, and inbound and outbound audio
   and video — into one number.

Each dimension is the weighted mean of the monitors making it up, using each monitor's
`calculatedScore.weight` (`1` unless an application changes it). The five then combine as
**`5 − RMSE`**:

```text
                       ┌──────────────────────────
                       │  Σ (5 − Dimension_Score)²
Client Score  =  5  −  │  ────────────────────────
                      \│      count(Dimensions)
```

Squaring the distances is what makes one collapsed dimension cost more than the same shortfall
spread evenly, which is how a call is actually experienced: nobody whose video has died calls it
two-thirds fine because the audio and the path are still good. **`[5, 5, 0]` scores `2.11` where an
average would say `3.33`.**

**A dimension nothing reported is absent, not zero.** A call that sends no video is not a call whose
video is broken. `undefined` and `null` are dropped before the mean; with none left the client score
is `undefined`.

**The transport is one of the five, not a multiplier.** This replaced 4.8's model, in which a peer
connection scaled its tracks by `pcScore / 5`. A dead path now drags the call score hard without
silently zeroing tracks that raised nothing of their own — a track with no issues still reads `5.0`
while the call reads `1.46`. Both statements are true and kept separate on purpose.

## What each score is responsible for

> **A peer connection is scored for the state of the path. A track is scored for what the user
> perceived. Nothing is scored for both.**

Loss, delay and congestion are properties of the *transport* — every stream riding it shares them —
so they are charged once, there. Freezes, pixelation, invented speech and jitter-buffer stress
measure *damage the user experienced*, and are charged on the track.

The distinction is cause versus effect, and the two are not interchangeable:

- **The same loss does different damage to different tracks.** 2% loss is inaudible on an Opus
  stream with FEC and PLC, and very visible on video without it.
- **Damage happens without loss.** In a captured session, 754 of 772 intervals measured **zero**
  packet loss, and 31 of them still had audible invention above 0.5% — jitter-buffer underruns and
  late arrivals, not packets that never came.
- **A clean path can carry a broken track, and a bad path a fine one.** A camera that has stopped
  producing frames scores badly on a perfect network.

A degradation is attributed by *joining* the two, which a server can always do because they arrive
in the same sample: the track says what broke, the peer connection says whether the network explains
it.

## What the calculator charges

Costs are points out of `5.0`. "Issue" means the charge applies only while that issue is open;
"reading" means it is continuous and has no detector behind it.

### Inbound video track

| Charge | Gate | Cost |
|---|---|---|
| `dry-inbound-track` | issue | 5.0 |
| `stuck-decoder` | issue | 5.0 |
| `frame-assembly-stalled` | issue | 5.0 |
| `frozen-video` | reading — `frameFlowState === 'frozen'` | 5.0 |
| `choppy-video` | reading — `frameFlowState === 'choppy'` | 2.5 |
| `pixelated-video` | issue | `quantizationDegradation` × size weight × 2.5 |
| `decoder-bottleneck` | issue | `decodingDegradation` × 2 |
| `inbound-video-playout-discrepancy` | issue | `videoPlayoutSkew`, 0–1 |
| `video-decoder-overloaded` | issue | `decodeBudgetUtilization` ramped 0.8 → 1.0, 0–1 |
| `blocky-video` | reading — no `pixelated-video` open | `quantizationDegradation` × size weight, 0–1 |
| `volatile-fps` | reading — `interFrameDelayVariation` ramped 0.2 → 0.4 | 0–1 |
| `dropped-video-frames` | reading — `droppedFrameRatio` ramped 0.1 → 0.2 | 0–1 |

`volatile-fps` is skipped on screen share, which legitimately runs at a low and bursty frame rate.

### Inbound audio track

| Charge | Gate | Cost |
|---|---|---|
| `dry-inbound-track` | issue | 5.0 |
| `invented-speech` | issue | `inventedSpeechRatio`, 0–1 |
| `synthesized-audio` | issue | `synthesizedAudioRatio`, 0–1 |
| `audio-jitter-buffer-stress` | issue | `jitterBufferStressSeverity`, 0–1 |
| `unstable-audio-playout` | reading — no `invented-speech` open | `inventedSpeechSeverity` ramped 0.25 → 1.0, 0–1 |

`invented-speech` and `unstable-audio-playout` are the same measurement either side of the
detector's threshold, so they are mutually exclusive rather than additive.

### Outbound video track

| Charge | Gate | Cost |
|---|---|---|
| `dry-outbound-track` | issue | 5.0 |
| `video-capture-bottleneck` | issue | `videoCaptureDegradation` × 2 |
| `encoder-bottleneck` | issue | `videoEncodingDegradation` × 2 |
| `high-deviation-from-target-bitrate` | reading — camera only, shortfall against `targetBitrate` ramped 0.05 → 0.15 | 0–1 |
| `downscaled-screenshare` | reading — screen share only, encoded area below the captured surface ramped 0.5 → 0.75 | 0–1 |

The two readings are exclusive by content type: a screen share is judged on sharpness, because
downscaled text is unreadable, and a camera on whether the encoder reached the bitrate it was told
to.

### Outbound audio track

| Charge | Gate | Cost |
|---|---|---|
| `dry-outbound-track` | issue | 5.0 |
| `silent-audio-source` | issue | 5.0 |

### Peer connection

| Charge | Gate | Cost |
|---|---|---|
| `uplink-congestion` | issue | `max(uplinkVideoCongestionSeverity, minSeverity)` × 2.5 |
| `downlink-congestion` | issue | `max(downlinkVideoCongestionSeverity, minSeverity)` × 2.5 |
| `transport-loss-sustained` | issue | 2.5 |
| `transport-delay-degraded` | issue | 2.5 |
| `unstable-transport` | reading — `2 × (1 − transportStability)` | 0–2 |

Congestion is floored at the detector's own `minSeverity`, so a finding at the threshold still costs
what the threshold says it is worth.

### When a charge becomes a reason

A charge of `0` is **dropped rather than written**, because a reason sitting at zero reads as a
fault that was found and never resolved. `reasons` is assigned on every collection — never only the
bad ones — so a connection back at a clean `5.0` stops shipping last tick's keys.

Continuous readings alone have to come to more than one point before they are published: `reasons`
is read as what to act on, and a charge that did not move the score by a point is not that. The
score still carries it. Where a detector has raised, its reason is always published, even if the
continuous part came to nothing — so a verdict is never contradicted by an empty reason list.

## What it does not charge

**19 of the 37 issue types carry no charge in this calculator.** An unpriced issue is still raised,
still emitted and still shipped in the sample — it just does not move a score.

| Not charged | Why |
|---|---|
| `ice-connection-failed`, `ice-disconnected`, `ice-establishment-failed`, `ice-transport-stalled`, `no-available-ice-candidate`, `unstable-ice-path`, `dtls-handshake-failed`, `dtls-handshake-stalled` | **Deliberate.** A path carrying nothing leaves nothing to have an opinion about, and the tracks riding on it go dry — `dry-inbound-track` and `dry-outbound-track` already take their dimensions to zero. Charging the connection too would be the same fault counted twice, in the one situation where there is no media to judge |
| `congestion` | **Deliberate.** The deprecated detector raises it for the same episode `uplink-congestion` / `downlink-congestion` cover, so pricing it would charge one episode twice |
| `capture-source-lost`, `rtp-sender-stalled`, `transport-demux-stalled`, `video-recovery-failed`, `av-desync`, `cpulimitation`, `blocked-inbound-media-transport`, `blocked-outbound-media-transport`, `blocked-stun-requests` | **Not deliberate** as far as the code says — these are findings a reference implementation would be expected to price. Treat their absence as a gap in this implementation rather than a statement that they do not matter |

A deployment that cares about any of the second group should price it in its own calculator rather
than wait for this one to.

## Pixelation and the presented size

`PixelatedVideoDetector` decides *whether* the picture is blocky, which is a fact about the stream
and the same everywhere. How much that *matters* is a fact about this client: the same stream is a
thumbnail in one layout and full-screen in the next.

**`InboundTrackMonitor.displayMagnification`** says how magnified it is — the linear factor
`sqrt(presented area / decoded area)`, reported raw, taken from the *areas* so a 16:9 frame
letterboxed into a square tile is not read as magnification on width alone. It is `undefined` — not
`1` — when nothing declared a presented size: "nobody measured" and "painted at its decoded size"
are different facts.

| `displayMagnification` | Multiplier |
|---|---|
| ≥ 1.5 | **×1.5** |
| 0.75 – 1.5 | ×1.0 |
| < 0.75 | **×0.25** |
| `undefined` | ×1.0 |

Deliberately asymmetric: blown up, the blocks are what the viewer complains about; in a thumbnail
nobody can see them. The size only ever *weighs* a finding and never becomes one.

### Declaring the presented size

In **device pixels**, either directly or by handing over the element:

```typescript
monitor.setInboundTrackContext(trackId, { presentedResolution: { width: 1280, height: 720 } });
monitor.setInboundTrackContext(trackId, { videoTag });   // re-measured every tick
```

The `videoTag` route measures the element's **layout box** (`clientWidth`/`clientHeight` ×
`devicePixelRatio`), never `videoWidth`/`videoHeight` — those are the *intrinsic* decoded size, the
same number the stats already report, so measuring with them would make every magnification exactly
1. It fits the frame's aspect ratio into that box as `object-fit: contain` does; an application
using `object-fit: cover` should declare `presentedResolution` itself.

## Where the reasons surface

`scoreReasons` is keyed by issue type wherever an issue is behind the charge, and by the name of the
reading otherwise. The value is the points that charge took off.

```typescript
monitor.on('score', ({ clientScore, currentReasons }) => {
    ui.setCallQuality(clientScore);        // 0.0–5.0, undefined until it settles
    console.log('what cost the score:', currentReasons);
});

monitor.scoreReasons;                                  // this entity's own reasons
monitor.peerConnections[0].calculatedStabilityScore;   // { value, reasons, weight }
monitor.tracks[0].calculatedScore;
```

The samples carry `scoreReasons` per entity as `Record<string, number>` (schema 3.6.0 made it a map
of contributions rather than a list of labels). Set `sendScoreReasonsToServer: false` to drop them
from the wire without changing any score.

## Writing your own

Assign it, and the monitor calls your `update()` from the next collection on. Nothing else has to
change: the monitors publish the same facts either way.

```typescript
monitor.scoreCalculator = {
    update() {
        for (const pc of monitor.mappedPeerConnections.values()) {
            const lossy = pc.issues.hasType('transport-loss-sustained');

            pc.calculatedStabilityScore.value = lossy ? 2.5 : 5.0;
            pc.calculatedStabilityScore.reasons = lossy ? { lossy_path: 2.5 } : undefined;
        }

        for (const track of monitor.tracks) {
            track.calculatedScore.value = track.issues.size === 0 ? 5.0 : 3.0;
        }

        monitor.setScore(myClientScore);
    },
};
```

**What you read.** Each monitor's `issues` registry — `hasType(type)`, `getByType(type)`,
`getFirstPayloadByType(type)`, `size` — plus any derived field the monitor publishes. Detector
payloads reached through the registry carry the measurements behind a finding.

**What you write.** `calculatedScore.value` and `.reasons` on the track monitors,
`calculatedStabilityScore` on the peer connections, and
`ClientMonitor.setScore(score, ownReasons?, aggregatedReasons?)` for the call. Leave `value` as
`undefined` to mean "not judged yet". Reason keys are yours to name; they ship verbatim in the
sample.

**Retuning when a fault is raised at all** is a different job, and is an edit to that detector's
config rather than to any calculator — see [Configuration](../configuration/). The two are
independent: the detector config decides whether the issue exists, the calculator decides what it
costs.
