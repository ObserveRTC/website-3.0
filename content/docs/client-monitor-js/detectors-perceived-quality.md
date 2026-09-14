---
title: "Perceived quality detectors"
description: "What the participant actually sees and hears, and the proxies used to judge it"
lead: "Nothing stopped. Every counter is advancing, every component agrees — and the call is still bad"
date: 2026-09-13T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 234
toc: true
---

This is the reference for **category 4**, asked from the participant's chair rather than the
engineer's. Nothing here says where the media chain broke, and nothing here has to.

```text
VISUAL    clarity        is the picture drawn with enough detail to read?
          smoothness     does it move at an even, adequate rate?
          continuity     is it moving at all?

AUDIO     clarity        is speech intelligible?            (no detector — deliberately)
          continuity     is the sound whole, or full of holes?
          naturalness    is what comes out of the speaker real audio, or invented?

BOTH      synchronization  do the picture and the voice agree in time?
          responsiveness   can the two people still take turns?
```

**These sub-layers are axes, not a ladder.** A picture can be perfectly smooth and unreadably
coarse; it can be sharp, steady and eleven seconds behind the voice; audio can be whole and
intelligible while the conversation is unusable because every turn arrives half a second late.

What they share is a **shape**, and the shape rather than the subject is what puts a detector here:
each watches a continuously-measured perceptual value and reports when it is severely degraded and
*stays* degraded. Every class is windowed, tick-counted or hysteretic — **users do not perceive
ticks.**

Every class binds to an **inbound** monitor, and that is not an accident: perception happens at the
receiver, and a sender-side detector reporting on the far end's experience would be guessing. The
one exception is `AudioPlayoutSynthesisDetector`, which binds to `MediaPlayoutMonitor` — playout
sits after the jitter buffer and is not per-track.

## The defining distinction: graded and sustained, not binary

The boundary with [pipeline disruption](../detectors-pipeline/) is the most confusing one in the
taxonomy, and the two categories routinely describe the same thirty seconds of the same call.

> Pipeline disruption asks **"where did progress stop?"** and its answer is binary and locatable.
> Perceived quality asks **"how bad is it, and for how long?"** and its answer is a threshold
> crossed and held.

A pipeline detector compares two monotonic counters either side of a named boundary; there is
nothing to average, because the finding is an equality with zero. A perceived-quality detector has
no boundary to name — everything is running — and the finding is that the *result* is bad: 0.012
bits per pixel, 8% of the last fifteen seconds of audio invented.

**Both can be right about the same call, and neither depends on the other.** `video-flow-disrupted`
and `stuck-decoder` are the standing example: one tells you the user's complaint is real, the other
tells you which component to open. Seeing only the freeze tells you the complaint is real and the
cause is somewhere you have not looked yet.

## What promoting a score reason to a detector changed

Until 4.9, three of the conditions here existed **only** as score penalties. `pixelated-video`,
`low-fps` and `volatile-fps` were score-reason keys computed inside `DefaultScoreCalculator`, and
that placement decided what could be done with them: a score reason cannot be raised, cannot be
resolved, has no duration, never reaches `activeIssues`, and is invisible to anything asking "what
is wrong with this session right now". A call that was blocky and juddery for four minutes produced
a low score and an empty issue list.

Promotion bought the whole lifecycle: a `raisedAt`, a `durationInMs`, a payload carrying the
evidence as it stood when the episode opened, a monitor event an application can act on live, and a
row in the sample a server can correlate. It also bought a stand-down policy — screen shares, paused
consumers, paused remote producers, backgrounded tabs — which a score penalty had no way to express.

The parallel implementations are gone with it. A condition is judged in exactly one place, here, and
the calculator's own thresholds, ramps and QP tables were removed.

## The grid

| Sub-layer | Class | Issue | Config key | Coverage |
|---|---|---|---|---|
| Visual — clarity | `PixelatedVideoDetector` | `pixelated-video` | `pixelatedVideoDetector` | inbound video |
| Visual — smoothness | `InboundVideoFlowStateDetector` | `video-flow-disrupted` (`state: 'choppy'`) | `inboundVideoFlowStateDetector` | inbound video |
| Visual — continuity | `InboundVideoFlowStateDetector` | `video-flow-disrupted` (`state: 'frozen'`) | `inboundVideoFlowStateDetector` | inbound video |
| Audio — clarity | *(none)* | *(none — by design)* | — | **empty, deliberately** |
| Audio — continuity | `InventedSpeechDetector` | `invented-speech` | `inventedSpeechDetector` | inbound audio |
| Audio — naturalness | `AudioPlayoutSynthesisDetector` | `synthesized-audio` | `audioPlayoutSynthesisDetector` | media playout — **Chromium only** |
| Synchronization | `AVDesyncPlayoutDetector` | `av-desync` | `avDesyncPlayoutDetector` | inbound audio **paired with a declared video track** |
| Responsiveness | `JitterBufferStressDetector` | `audio-jitter-buffer-stress` | `jitterBufferStressDetector` | inbound audio |

**Six classes, six issue types.** Each video class is constructed only for video tracks and each
audio class only for audio ones.

{{< callout context="caution" title="Synchronization is covered, and frequently dark" icon="alert-triangle" >}}
Since 4.9 the sub-layer has a detector that measures the thing it is named after — the offset
between the two tracks' playout — rather than inferring it from repair work. But it measures nothing
unless the application declares which video track pairs with the audio track, **and** the browser
populates `estimatedPlayoutTimestamp` (Firefox does; Chrome only when A/V sync is enabled
internally; Safari not at all). On much of a real fleet this detector reports `inputsUnavailable`
rather than health. Read the two together or read neither.
{{< /callout >}}

## Where the arithmetic lives

The monitors compute; the detectors compare and time.

| Value | How it is derived | Read by |
|---|---|---|
| `bitPerPixel` | `bitrate / (frameWidth × frameHeight × framesPerSecond)` | `PixelatedVideoDetector` |
| `inventedSpeechRatio` | (Δ concealed − Δ silent concealed) ÷ Δ `totalSamplesReceived` | `InventedSpeechDetector` |
| `timeStretchRate` | (Δ inserted + Δ removed) ÷ Δ `totalSamplesReceived` | `JitterBufferStressDetector` |
| `jitterBufferTargetDelayInMs` | Δ `jitterBufferTargetDelay` ÷ Δ `jitterBufferEmittedCount`, ×1000 | `JitterBufferStressDetector` |
| `linkedVideoPlayoutDiffInMs` | this audio track's `estimatedPlayoutTimestamp` minus its linked video track's — **on `InboundTrackMonitor`** | `AVDesyncPlayoutDetector` |
| `displayMagnification` | `sqrt(presented area / decoded area)`, unbounded — **on `InboundTrackMonitor`** | `DefaultScoreCalculator` |
| `frameFlowState` | written *back* onto `InboundTrackMonitor` by the flow detector | `DefaultScoreCalculator` |

Two entries sit a level up on `InboundTrackMonitor` rather than on `InboundRtpMonitor`, each for a
stated reason: `linkedVideoPlayoutDiffInMs` is the library's only value computed from **two**
streams and neither RTP monitor owns the pair, and `displayMagnification` needs the
`presentedResolution` the application declared, which no RTP monitor has.

**Duration is stats time**, accumulated from `inboundRtp.deltaTime`. This category is where the rule
earns most of its keep, because a backgrounded tab or a saturated main thread is *itself* one of the
things that makes video look choppy. Two detectors count **collections** instead —
`InboundVideoFlowStateDetector` and `JitterBufferStressDetector`, both via `minConsecutiveTicks` —
which is a confidence floor rather than a persistence bar, and scales with `collectingPeriodInMs`.

## Visual — clarity

### `PixelatedVideoDetector` → `pixelated-video`

Video the viewer would call blocky or smeared: a picture drawn with too few bits for its size, for
long enough to be worth complaining about. Nothing has stalled — frames arrive, decode and render on
time — and the experience is still bad, which is the whole of this category in one condition.

```javascript
pixelatedVideoDetector: {
    threshold: 0.03,          // bits/pixel at or below which the picture is coarse
    recoveryThreshold: 0.05,  // strictly above this it resolves
    durationInMs: 8000,
}
```

The comparison runs the opposite way round from every transport measure in the library — **low is
bad** — so the hysteresis band runs *upward*. The defaults are reasoned from camera video typically
running 0.05–0.2 bits per pixel, with blocking artefacts usually visible below roughly 0.03.

**Why bits per pixel rather than QP.** The obvious measure is the quantizer, and the library has it
(`avgQpPerFrame`). It is not used, for a plain reason: `qpSum` is **optional** in the specification,
absent on some codecs and implementations, and its scale differs between codecs — 127 for VP8, 255
for VP9 and AV1, 51 for H.264 and H.265. A QP threshold is therefore not a number at all, it is a
per-codec table. The score calculator maintained exactly that table until 4.9 and demonstrated the
failure mode: where the codec had no entry, or the browser reported no `qpSum`, the judgement
silently produced nothing — and nothing distinguished that from a picture that was fine.

**What that costs, and it is not small.** Bits per pixel is not a perceptual model. It knows nothing
about codec efficiency (AV1 at 0.02 bpp is a very different picture from VP8 at 0.02 bpp), nothing
about content (a static wall compresses to nearly nothing and looks perfect), and nothing about how
large the picture is on screen. The presented size is used by the *score*, not the detector — see
[Scoring](../scoring/).

**Screen shares are excluded, not re-thresholded.** A static slide legitimately spends almost
nothing per pixel and looks perfect. A second threshold for screen content would be an opinion about
content the library cannot verify. `isScreenShare` for an inbound track is **declared**:

```javascript
monitor.setInboundTrackContext(trackId, { contentType: 'screenshare' });
```

An undeclared screen share is judged as camera video and will raise. That is this category's most
likely false positive.

**What it does not claim.** Not *why* the picture is coarse — a congested uplink, a sender-side
encoder bottleneck, an SFU handing down a low simulcast layer and a deliberately low-bitrate stream
all look identical from here. Not that the viewer minds.

## Visual — smoothness and continuity

### `InboundVideoFlowStateDetector` → `video-flow-disrupted`

An inbound video track whose picture has stopped moving, or is moving badly — the freeze or judder
the person watching actually sees, with no claim about why. One class, one issue type, **two
states**.

**Why there is no separate `ChoppyVideoDetector`.** Both halves — a steady 8 fps that is
smooth-but-slow, and 25 fps swinging between 5 and 40 that is fast-but-lurching — are the same
complaint from the viewer ("it's juddery"), and they sit on a continuum with a full freeze rather
than beside it. Two issue types on one episode was noise. One type with a `state` of `frozen` or
`choppy` says it once — and the two verdicts are read from the same freeze counters over the same
window, so two classes would have had to agree tick by tick to avoid contradicting themselves.

A freeze starts when `freezeCount` advances and persists while nothing renders:

```text
frozen = 0 < newFreezes || (wasFrozen && deltaFramesRendered === 0)
```

The second clause is load-bearing: `freezeCount` counts freeze *starts*, so its delta alone would
declare a persistent freeze over after a single tick. The **state** is derived on the first frozen
tick, so the score reflects it immediately, while the **issue** waits for `minConsecutiveTicks`
consecutive frozen observations.

The payload is discriminated on `state`, because a freeze is one event with a length and choppiness
is several over a window:

| `state` | Payload |
|---|---|
| `frozen` | `observedFrozenTimeInMs` — how long the picture had been stopped when the finding was raised, a floor and never above the truth |
| `choppy` | `freezeCount`, `windowInMs` (the stretch they were counted over, in stats time) and `frozenRatio` |

`windowInMs` is stats time actually spanned, not the nominal collecting period, so a server can
judge severity as a frozen share of a *measured* window even when a collection ran late.

**Stand-downs swallow the counter.** A backgrounded tab, a paused consumer or a paused remote
producer set the last-seen freeze count to whatever the counter now reads, rather than skipping the
tick. Without that, a tab hidden for a minute would come back with `freezeCount` twenty higher and
the detector would replay a minute of browser throttling as a burst of freezes.

{{< callout context="caution" title="A recorded defect, not documented behaviour" icon="alert-triangle" >}}
All three stats adapters document `inbound-rtp.framesRendered` as *never emitted* — Chromium,
Firefox and WebKit alike — so `deltaFramesRendered === 0` is false everywhere and the persistence
clause cannot engage. What remains is `0 < newFreezes`: repeated freezing raises exactly as
intended, but a **single continuous freeze**, which increments the counter once and then holds, does
not. This is recorded as a defect rather than documented as behaviour; the fix is a persistence
signal that exists on real browsers.
{{< /callout >}}

## Audio — clarity

**This sub-layer is empty, and the emptiness is a decision.**

Clarity for audio would mean intelligibility. That is the question users actually ask, it is the one
MOS-style estimators claim to answer, and **no client-side signal supports it.** The stats report
how much audio was concealed, how much was stretched, how deep the buffer ran and how loud the
signal was. None of those is a statement about intelligibility.

Two candidate routes were considered and rejected on the same ground:

- **A concealment-derived intelligibility score.** Concealment is *continuity*, already owned one
  sub-layer down as `invented-speech`. Recomputing it with a different threshold and calling the
  result clarity would be one condition wearing two names.
- **A published MOS model (E-model and relatives).** Calibrated for fixed-rate telephony codecs over
  networks with stationary loss. Applied to Opus with in-band FEC, DTX and NetEQ adapting
  continuously, they produce a number with a decimal point and no defensible relationship to what
  anyone heard. **A number nobody can verify is worse than an acknowledged gap**, because it will be
  trended, alerted on and believed.

## Audio — continuity

### `InventedSpeechDetector` → `invented-speech`

A listener being fed audio the sender never sent, for long enough to be the thing behind a "they
were breaking up" complaint. When packets are missing or late, NetEQ does not fall silent; it
fabricates audio from what came before so playout never stops. That is usually the right trade and
usually inaudible — which is exactly why packet loss is a poor proxy for how a call sounded. What
the listener hears is the fabrication, so that is what this measures.

**Only audible invention counts.** `concealedSamples` climbs through ordinary silence too, so
`silentConcealedSamples` is subtracted on the monitor before the ratio is formed:

```text
inventedSpeechRatio = max(0, ΔconcealedSamples − ΔsilentConcealedSamples)
                      ÷ ΔtotalSamplesReceived
```

That subtraction is what keeps every quiet moment of every call from reading as a fault.

```javascript
inventedSpeechDetector: {
    allowedInventedRatio: 0.05,  // RFC 7294 calls a second above 5% concealment severely concealed
    raiseAfterInventedMs: 400,   // invention beyond the allowance before the issue opens
}
```

**The accumulator is the whole of the detector's state.** Each tick contributes
`inventedSpeechRatio × deltaTime` milliseconds of invention and is credited
`allowedInventedRatio × deltaTime` of tolerance; the difference moves the accumulator, clamped
between zero and `raiseAfterInventedMs`. At the defaults that is 0.4 s of excess invention to open —
two seconds of audio at 25% invented — and, because the allowance is also the drain rate, about 8 s
of clean audio to close.

**It does not care how often you poll.** This is why the class was rewritten in 4.9. The previous
implementation classified each tick as bad or good and judged a ratio over a 15 s sliding window, so
a bad second inside a five-second collection was averaged down by five and the detector's
sensitivity moved with `collectingPeriodInMs`. Integrating a rate over elapsed time has no such
artefact.

**Brief pauses do not end an episode.** A clean tick drains only the allowance, so someone who
breaks up, pauses for breath and breaks up again keeps accumulating rather than starting over, while
genuinely recovered audio still closes the issue.

**Stand-downs discard the accumulator** rather than draining it: a paused consumer or remote
producer means nothing is being sent, so there is nothing to invent, and a paused stretch must not
leak into the next episode.

**What the accumulator cannot tell you** is the shape of what filled it: one second at 25% invented
and five seconds at 5% are both 200 ms of excess. That is the price of poll-independence.

## Audio — naturalness

### `AudioPlayoutSynthesisDetector` → `synthesized-audio`

Concealment audio the browser generated because the jitter buffer had nothing real left to play:
robotic, warbling or stretched speech. The signal is worth watching precisely because nothing
upstream reports it as a failure — concealment is the audio stack *succeeding* at keeping playback
continuous, so packet-level statistics can look unremarkable while the listener hears something
wrong.

```javascript
audioPlayoutSynthesisDetector: {
    synthesizedRatioThreshold: 0.05,  // share of what was played that was invented
    createEvent: true,                // also buffer EXCESSIVE_SYNTHESIZED_AUDIO into samples
}
```

It reads `MediaPlayoutMonitor.deltaSynthesizedSamplesDuration` and raises once the invented **share**
crosses the threshold — a share of what was played rather than a duration per collection, which is
what the earlier `minSynthesizedSamplesDuration: 0` got wrong: it reported on every tick that
concealed anything at all.

It is priced alongside `invented-speech` rather than on top of it: the two are the same fault seen
from two places — the stream that concealed, and the playout device that invented — so the pair is
weighted so one episode is not charged twice.

{{< callout context="note" title="Chromium only, and the spec is unsettled" icon="info-circle" >}}
`media-playout` reports do not exist on Firefox or WebKit — both adapters say so explicitly, and
neither substitutes a guess — so this detector runs on Chromium and is silent everywhere else. The
W3C statistics specification also marks `RTCAudioPlayoutStats` as a **feature at risk due to lack of
consensus**. A fleet-wide dashboard should not read its absence on Safari as health.
{{< /callout >}}

## Synchronization

### `AVDesyncPlayoutDetector` → `av-desync`

Lip sync: one participant's voice and their lips playing out at measurably different points in that
participant's own timeline. A viewer describes it as dubbing.

**This is the only detector in the library that compares two streams.** Synchronization is not a
property of a track at all: an audio track playing 200 ms behind the wall clock is perfectly fine if
the video is 200 ms behind too, and badly broken if the video is current.

```text
linkedVideoPlayoutDiffInMs = audio.estimatedPlayoutTimestamp
                           − video.estimatedPlayoutTimestamp
```

Positive means audio is **ahead** — playing content from later in the sender's timeline than the
picture is showing.

**Why the two values subtract directly.** `estimatedPlayoutTimestamp` is not a local clock reading:
the specification defines it as the **sender's NTP clock time** of the last playable sample or
frame, obtained by resolving the stream's RTP timestamps through the RTP-to-NTP mapping in that
sender's RTCP sender reports. Both tracks come from the same sender, so both values are already on
the same clock and their difference is the skew in milliseconds. No third quantity relates them.

**Which video track, and why the library will not guess:**

```javascript
monitor.setInboundTrackContext(audioTrack.id, { linkedVideoTrackId: videoTrack.id });
```

An SFU forwards each participant's audio and video as independent streams with no signalled
relationship; `MediaStream` grouping does not survive every topology; `trackIdentifier` says which
track, never whose. Pairing by arrival order is wrong the moment a participant joins mid-call, and
pairing by "the only video track" is wrong in any call with more than two people. **A wrong pairing
does not fail loudly** — it produces a confidently wrong number that looks exactly like a
measurement.

**The two directions are not symmetric, and that is the whole tuning.** Sound arrives after light
everywhere in the physical world — a metre of distance is three milliseconds of delay — and a
listener has spent a lifetime compensating. Audio *leading* the picture has no natural analogue.
ITU-R BT.1359-1 puts detectability at roughly +45 ms ahead and unacceptability at +90 ms, against
−125 ms and −185 ms behind.

```javascript
avDesyncPlayoutDetector: {
    audioAheadRaiseInMs: 90,
    audioAheadResolveInMs: 45,
    audioBehindRaiseInMs: 185,   // magnitudes, for audio lagging the picture
    audioBehindResolveInMs: 125,
    sustainForInMs: 3000,        // stats time past the threshold before raising
}
```

Thresholding the absolute skew against a single number would be either too strict on lag or too lax
on lead: at ±150 ms it would have to call both objectionable or neither, when in fact +150 ms is a
complaint and −150 ms is ordinary.

Three seconds is a deliberately long sustain for a value that can move sharply: the playout
timestamp is extrapolated between RTCP sender reports, which arrive on the order of every five
seconds, so the first readings after a track starts can swing while the mapping settles.

**What it does not claim.** Not that the viewer noticed. Not which side drifted. **Not desync that
begins during a freeze** — the specification allows `estimatedPlayoutTimestamp` to be extrapolated,
so a renderer that has stopped painting can keep reporting smooth playout, and this detector will
believe it. Seeing a freeze is the cue to distrust a clean sync reading over the same interval.

{{< callout context="note" title="What replaced what" icon="info-circle" >}}
Until 4.9 this sub-layer held `AudioDesyncDetector`, which read NetEQ's accelerate and
preemptive-expand counters and called the result desync. Those counters measure the jitter buffer
time-stretching audio to reach its target delay — buffer health, not synchronisation. Worse, the one
real coupling runs backwards: when a browser's A/V sync logic detects drift it *raises* NetEQ's
target delay, so sustained deceleration is frequently the sync **correction** working. The old
detector fired on the repair. Nothing of that measurement survives, and no tuning carries over — the
old thresholds were dimensionless fractions of samples, the new ones are milliseconds of skew. The
signal itself is not lost: `JitterBufferStressDetector` reads it as `timeStretchRate`, under a name
that says what it is.
{{< /callout >}}

## Responsiveness

### `JitterBufferStressDetector` → `audio-jitter-buffer-stress`

An audio jitter buffer fighting the network and losing. The user-visible failure is conversation
that has gone latent and slightly warped — voices sped up or dragged out, replies landing on top of
each other — rather than the dropouts `invented-speech` covers. The two are complements: invented
speech is what the buffer does when it has already run dry, and this is the buffer straining before
it gets there.

**Both conditions are required, because either alone is benign:**

| Signal alone | What it actually means |
|---|---|
| Deep `jitterBufferTargetDelayInMs` | NetEQ is **succeeding** — it bought latency to hide jitter, and the user hears nothing wrong |
| Raised `timeStretchRate` | Ordinary clock-drift correction between two devices whose sample clocks disagree |

It is the two *together* — the buffer already deep and still having to warp audio to keep up — that
a listener hears. For the same reason a tick missing **either** field is skipped rather than judged
on the other: half the evidence is worse than none.

```javascript
jitterBufferStressDetector: {
    targetDelayThresholdInMs: 200,
    timeStretchThreshold: 0.02,
    minConsecutiveTicks: 2,
}
```

**Why this is genuine conversational latency, and why RTT does not capture it.**
`transport-delay-degraded` measures the round trip on the path. The delay a participant experiences
before they can reply is that, *plus* however long the receiver deliberately holds audio before
playing it. The jitter buffer's target delay is the second term, it is often the largest, and it is
invisible to any transport measurement: a path with a flat 40 ms RTT and a receiver holding 400 ms
produces a conversation nobody can take turns in while every network metric reads healthy.

**And why end-to-end conversational delay is deliberately not measured.** The number an operator
wants is mouth-to-ear. This endpoint can see its own receive-side terms and nothing else. Publishing
a total assembled from the terms we happen to have would produce a figure that is confidently wrong,
that nobody can verify, and that would be trended and alerted on precisely because it looks like the
number everyone wanted.

**False positives.** An application that deliberately raises the buffer (`jitterBufferMinimumDelay`,
`playoutDelayHint`) gets a deep target delay by configuration; this class does not read the
minimum-delay field, so a deep buffer chosen on purpose plus 2% ordinary clock correction satisfies
both conditions.

## How this category relates to its neighbours

Co-firing is **independent evidence, never a chain**. Nothing here waits for, checks, or is
suppressed by anything in the other categories.

- **Against connectivity.** Perceived-quality issues on a call that also raised `unstable-ice-path`
  say the reselections are audible; on a call that raised nothing they say the path is fine and
  something else is wrong.
- **Against transport quality.** `invented-speech` with `transport-loss-sustained` is loss the
  listener heard; `transport-loss-sustained` without it is loss Opus successfully hid — a different
  and much less urgent finding. `invented-speech` *without* loss points at the buffer rather than
  the wire.
- **Against pipeline disruption.** `video-flow-disrupted` with `stuck-decoder` names the component;
  alone it means the freeze is real and the break is upstream of anything this endpoint can see.
- **Against telemetry.** `video-resolution-changed` beside `pixelated-video` is usually the whole
  story — the SFU dropped a layer — and neither says so alone. `stats-collection-gap` beside
  anything here is a warning about the *measurement*: after a gap the next interval's rates are
  fiction.

Correlating any of these is the server's job, where the whole session is visible — see
[`observer-js`](/docs/observer-js/).
