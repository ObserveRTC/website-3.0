---
title: "Pipeline disruption detectors"
description: "The send and receive media chains, and the boundary each detector watches"
lead: "Did the media chain stop somewhere, or do two adjacent components disagree?"
date: 2026-09-13T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 233
toc: true
---

This is the reference for **category 3**, the largest at **15 classes and 15 issue types**. The
answer it is built to give is a **place**: the boundary where the upstream counter advanced and the
downstream one did not.

## The two chains

An endpoint runs two chains, and they are not each other's mirror image. They meet only at the
network, which belongs to neither.

```text
SEND
  capture device
        │  S1  is the device delivering the frames it was configured for?
        ▼
  frame supply
        │  S2  processing / constraints        (not observable — see below)
        ▼
  encoder input
        │  S3  is the encoder consuming what the source hands it?
        ▼
  encoder
        │  S4  do encoded frames become packets?
        ▼
  RTP sender
        │  S5  does anything at all go on the wire?
        ▼
  ══════ network ══════
```

```text
RECEIVE
  ══════ network ══════
        │
        ▼
  ICE transport
        │  R1  do arriving bytes reach an inbound RTP stream?
        ▼
  RTP receiver
        │  R2  is anything arriving on this track at all?
        ▼
  packets
        │  R3  do packets become complete frames?
        ▼
  frame assembly
        │  R4  do assembled frames become decoded pictures?
        ▼
  decoder
        │  R5  do decoded pictures get painted?
        ▼
  renderer

  beside R3–R5:  the repair loop — PLI out, keyframe back
```

Each arrow is a **boundary**, and each has a monotonic counter on either side. That is what makes a
disruption locatable rather than merely detectable: `framesEncoded` rising while `packetsSent` stays
flat is not "the call broke", it is a stage name to hand an engineer.

**The receive chain has more boundaries and more detectors**, because the receive side is where the
consequences of everything upstream — the far end's encoder, the SFU, the network — arrive with no
context. A sender knows what it meant to send; a receiver only knows what turned up.

## Boundary, not component

The membership test: *can you name the boundary at which progress stopped?* An ideal finding reads
as a comparison — "packets advanced, frames received did not" — never as a verdict about a
component's character. A boundary statement is falsifiable from the stats alone; a component verdict
imports a theory about which side is at fault, and the stats usually cannot tell.

{{< callout context="note" title="Three issue types still name a component" icon="info-circle" >}}
`encoder-bottleneck`, `decoder-bottleneck` and `video-decoder-overloaded` assert a component verdict
from boundary evidence. The boundary is real and measured; the component named on the *far* side is
an inference. An `encoder-bottleneck` on a machine running a background-blur transform is naming the
encoder for a stall upstream of it.

They are kept because the issue type is a public contract that `observer-js` and dashboards consume.
This is recorded as **naming debt with a known direction**: if they are ever renamed, it should be
toward the boundary (`encoder-frame-supply-shortfall` rather than `encoder-bottleneck`). That is
the same reasoning that split `media-pipeline-stalled` into `rtp-sender-stalled` and
`transport-demux-stalled` in 4.9.
{{< /callout >}}

## The grid

| Boundary | Class | Issue type | Config key | Coverage |
|---|---|---|---|---|
| Send — the source | `CaptureSourceLostDetector` | `capture-source-lost` | `captureSourceLostDetector` | Audio + video, outbound track; reads the track object, not stats |
| Send — the source | `SilentAudioSourceDetector` | `silent-audio-source` | `silentAudioSourceDetector` | Audio only, outbound track |
| S1 capture → frame supply | `VideoCaptureBottleneckDetector` | `video-capture-bottleneck` | `videoCaptureBottleneckDetector` | Video only; screen shares refused; needs `getSettings().frameRate` |
| **S2 processing → encoder input** | *(none — no browser stat exists)* | — | — | **Unwatched by design of the stats, not by choice** |
| S3 frames → encoder | `EncoderBottleneckDetector` | `encoder-bottleneck` | `encoderBottleneckDetector` | Video only; highest active layer only |
| S4 encoder → RTP sender | `RtpSenderStalledDetector` | `rtp-sender-stalled` | `rtpSenderStalledDetector` | Video in practice — per ssrc; audio has no frame counter |
| S5 RTP sender → wire | `DryOutboundTrackDetector` | `dry-outbound-track` | `dryOutboundTrackDetector` | Audio + video, outbound track |
| R1 transport → RTP streams | `TransportDemuxStalledDetector` | `transport-demux-stalled` | `transportDemuxStalledDetector` | Per ICE transport; **blind on Firefox** |
| R2 wire → track | `DryInboundTrackDetector` | `dry-inbound-track` | `dryInboundTrackDetector` | Audio + video, inbound track |
| R3 packets → frames | `FrameAssemblyStalledDetector` | `frame-assembly-stalled` | `frameAssemblyStalledDetector` | Video only; needs `framesReceived` |
| R4 frames → decoder | `DecoderBottleneckDetector` | `decoder-bottleneck` | `decoderBottleneckDetector` | Video only, inbound track |
| R4 frames → decoder | `DecoderPerformanceDetector` | `video-decoder-overloaded` | `decoderPerformanceDetector` | Video only; needs a loss reading to proceed |
| R4 frames → decoder | `StuckDecoderDetector` | `stuck-decoder` | `stuckDecoderDetector` | Video only; the binary case |
| R5 decoder → renderer | `PlayoutDiscrepancyDetector` | `inbound-video-playout-discrepancy` | `playoutDiscrepancyDetector` | Video only; evidence spans R4+R5 |
| Repair loop | `VideoRecoveryFailedDetector` | `video-recovery-failed` | `videoRecoveryFailedDetector` | Video only, inbound track |
| The machine | `CpuPerformanceDetector` | `cpulimitation` | `cpuPerformanceDetector` | Client monitor singleton; spans every peer connection |

## What every stall clock shares

Eleven of the classes measure how long a boundary has been broken, and every one accumulates the
**monitored object's own `deltaTime`** rather than wall-clock elapsed. This category is where
[design rule 3](../detectors/#3-condition-duration-is-measured-in-stats-time) earns its keep most
obviously, because the conditions these detectors fire under are precisely the conditions that make
collections run late: a wedged decoder, a saturated encoder and a main thread too busy to run the
collector arrive together.

The clocks read the `deltaTime` of the object whose counters are being compared — `mediaSource` for
capture, `outboundRtp` for the sender, `transport` for the demux, `inboundRtp` for everything on the
receive side — which is what keeps each detector's numerator and denominator on one clock.

**The one deliberate exception is inside `CpuPerformanceDetector`**: its
`durationOfCollectingStatsInMs` signal is wall clock, because the thing it measures *is* wall clock.

## Send — the source

### `CaptureSourceLostDetector` → `capture-source-lost`

The capture device behind an outbound track went away: `track.readyState` turned `ended`. A webcam
unplugged, a Bluetooth headset that dropped its link, a screen share the user stopped from the
browser's own bar, a virtual camera whose application quit.

**It reads no stats at all**, and that is the point: none of these events leaves a trace in RTP. The
`outbound-rtp` entry survives, the counters simply stop advancing, and every detector above reads a
track that has gone quiet with no way to say why. The track object is the only place the reason is
written down.

There are no thresholds. `ended` is terminal by specification, so a duration threshold would measure
how long a fact stayed true. Raised exactly once per track, and **nothing ever resolves it** — the
only issue in this category with no resolve path. Payload: `peerConnectionId`, `trackId`, `kind`,
`deviceLabel`.

**No stand-downs, deliberately.** It is not conditioned on the sender being live or unpaused: a
device unplugged during a pause is a fact about the device, and an application about to resume onto
a device that no longer exists is exactly who needs to be told.

### `SilentAudioSourceDetector` → `silent-audio-source`

A microphone that is live, unmuted, enabled — and dutifully capturing digital silence. The failure
is invisible everywhere else in the stats: the encoder runs, packets flow at the usual rate, the
transport is healthy, and the call is perfect except that nobody can hear this person. It is the
"you're on mute" that muting does not explain.

It reads `mediaSource.rmsAudioLevel` — `sqrt(deltaTotalAudioEnergy / deltaSamplesDuration)`, the
level integrated over the interval — deliberately **not** the instantaneous `audioLevel`, which
reads zero between words and would fire on every pause for breath.

```javascript
silentAudioSourceDetector: {
    silenceThresholdInMs: 60000,   // long on purpose: silence != a broken mic
    silenceRmsThreshold: 0.0001,   // interval-integrated RMS
    recoveryRmsThreshold: 0.0003,  // higher, so one dither blip cannot close a finding
}
```

**The minute is not timidity.** A microphone capturing nothing and a person who is simply not
talking are the same measurement, and only duration separates them. A threshold in single-digit
seconds would file every listener in every meeting as a broken capture device.

**The dead band between the two RMS thresholds** exists because the raise threshold sits in empty
space between digital silence and a real noise floor: a source hovering just under it crosses by a
dither bit and crosses back. A captured call showed one doing exactly that — four raises and three
resolutions in eight minutes on an unchanging source.

**It judges microphones only.** A track marked as screen share resolves with `screen share audio,
not a microphone`; a track whose settings name no capture device resolves with `no capture device,
not a microphone`. The second is what catches display-capture audio, since `contentType` is
auto-detected from `getSettings().displaySurface` — a *video* track setting.

## Send — capture to frame supply (S1)

### `VideoCaptureBottleneckDetector` → `video-capture-bottleneck`

A camera degrading in place: a driver struggling, another application contending for the device,
thermal throttling. The track reports itself `live` and unmuted throughout while the far end's
picture turns stuttery.

It compares `mediaSource.sourceFps` against the `frameRate` in the track's own `getSettings()`.
`sourceFps` is the raw frame counter differenced against measured elapsed time — **never**
`mediaSource.framesPerSecond`, which the browser has already smoothed and which hides exactly the
stutter being looked for.

**Averaging over a window rather than thresholding each tick is the whole design.** A camera that is
failing rather than merely busy produces starving intervals interleaved with healthy ones — 150
frames in one 5-second tick, then 132, then 150, then 97 — so tick by tick most of it looks fine and
per-tick thresholding never reaches it, while the average reads well under the configured rate.

```javascript
videoCaptureBottleneckDetector: {
    produceDegradationThreshold: 0.2,  // camera more than 20% short of the configured fps
}
// the detection and recovery spans come from outboundTrackWindow
```

One threshold read over **two windows**: a shortfall across the detection window raises, and the
issue resolves only once the *recovery* window — the stretch immediately before it — comes back
under the same line. A camera hovering at the threshold therefore cannot turn one continuous fault
into a stream of short episodes.

`produceDegradation` in the payload is the **depth** of the finding, measured from the raise line
rather than from the configured rate, so it asks the same question at any threshold: a camera just
over the line reports near `0`, one delivering nothing reports `1`.

**Stand-downs.** A backgrounded tab, a paused sender, a track that is not live/unmuted/enabled, and
**screen shares**, which are refused outright — a screen share's frame rate is content-driven, and
an application capturing a genuinely moving surface can opt in with
`setOutboundTrackContext(trackId, { contentType: 'camera' })`. Each stand-down closes the window,
and the first tick after one only reopens it without contributing: that tick's `deltaTime` spans the
stretch that was deliberately not judged.

**False positives.** A `frameRate: 60` constraint on a 30 fps webcam produces a permanent finding.
The detector has no way to tell an unmet constraint from a degrading device, and does not try.

## Send — processing to encoder input (S2)

**Nothing watches this boundary, because no browser statistic sits on it.**
`RTCMediaSourceStats.frames` counts what the source produced; `framesEncoded` counts what came out
of the encoder. There is no counter in between. A transform that drops every other frame and an
encoder that encodes every other frame are, in `getStats()`, the same two numbers.

The consequence is stated plainly: **S2's failures are attributed to S3.** The honest reading of an
`encoder-bottleneck` is "something between the capture source and the encoder's output could not
keep up". An application that inserts processing and wants this boundary observable has to
instrument it itself.

## Send — frames to encoder (S3)

### `EncoderBottleneckDetector` → `encoder-bottleneck`

Given a capture source that is delivering, is the encoder keeping up with it? It reads two frame
counters off `OutboundTrackMonitor.slicedWindow` — frames the media source produced, frames the
highest active layer encoded, measured across the same stretch.

```javascript
encoderBottleneckDetector: {
    encodeDegradationThreshold: 0.3,   // encoder leaving 30% of handed frames unencoded
}
```

| | |
|---|---|
| Raise | more than `encodeDegradationThreshold` of the frames handed over left unencoded across the detection window |
| Update | every later collection still short of it updates the open issue rather than opening another |
| Resolve | the recovery window — the stretch *before* the detection window — is back within the threshold |

**The comparison is always against what the source actually delivered**, never the configured frame
rate, so a starving camera cannot make the encoder look guilty: handed nothing, it has nothing to
answer for. Screen shares are judged like any other track here — their frame rate follows the
content, and the encoder is still expected to keep up with whatever it is given. (That asymmetry is
deliberate: screen shares never raise `video-capture-bottleneck` and always remain judgeable for
`encoder-bottleneck`.)

{{< callout context="tip" title="Independence, worked once" icon="rocket" >}}
The "is the source short?" test is made here from the two raw readings, and deliberately **not** by
consulting `VideoCaptureBottleneckDetector`'s issue — which is what this class used to do. Reading
another detector's conclusion made the verdict depend on two things that have nothing to do with the
encoder: whether that detector was registered at all (`videoCaptureBottleneckDetector: null` and
this one starts blaming the encoder for a starving camera, silently), and the order the two were
constructed in. The two still agree on defaults **because they read the same two numbers**.
{{< /callout >}}

**There is deliberately no CPU signal here.** `CpuPerformanceDetector` already raises `cpulimitation`
from codec utilization. Folding a CPU reading in as well would make the two correlate
*tautologically* — one measurement reported twice, which is exactly what co-firing as independent
evidence is supposed to rule out.

The layer is chosen by `OutboundTrackMonitor.highestLayer`: the single outbound RTP where there is
one, otherwise the one with the highest bitrate — returning nothing when several layers are present
and none reports a bitrate, standing the detector down rather than picking arbitrarily.

## Send — encoder to RTP sender (S4)

### `RtpSenderStalledDetector` → `rtp-sender-stalled`

`deltaFramesEncoded > 0` while `deltaPacketsSent === 0` on one ssrc. **An encoded frame always
packetizes**, so a sustained violation is a wedged sender or pacer. Seen in the wild after
`replaceTrack` races and simulcast reconfigurations, where the encoder happily keeps running against
a sender that will never transmit again.

This is the cleanest boundary statement in the category: the issue type names the stage, so a reader
learns where the break is from `type` alone rather than from a discriminator inside a payload.

```javascript
rtpSenderStalledDetector: {
    thresholdInMs: 4000,   // frames encoding while no packet leaves, in stats time
}
```

State is kept **per ssrc**, because simulcast layers wedge one at a time. An ssrc that disappears
from the stats resolves with `outbound rtp is gone` rather than leaving an issue open forever.

**Why the innocent explanations cannot produce this signature.** Congestion, resolution adaptation
and a paused sender would all have stopped the *encoder*. The condition requires `framesEncoded` to
be rising, which is what makes silence on the wire anomalous rather than expected — and why this
detector needs none of the bitrate floors its receive-side twin carries.

**Coverage, stated honestly.** `framesEncoded` is a video counter, so **this boundary is unwatched
for audio**; the equivalent audio failure surfaces one stage later as `dry-outbound-track`.

## Send — RTP sender to the wire (S5)

### `DryOutboundTrackDetector` → `dry-outbound-track`

Zero bytes sent, tick after tick. **It is the one failure the local user cannot see for themselves**,
because their own preview keeps rendering from the capture stream and looks perfect.

```javascript
dryOutboundTrackDetector: { thresholdInMs: 5000 }
```

**It reports only silence the browser has not already explained.** An encoder held back by
`bandwidth` or `cpu` has stopped because it was told to, and that pressure is already reported by
`uplink-congestion` and `cpulimitation`. Either reason on any layer the sender is driving stands the
detector down. `other` does not: that is the browser declining to say why, which is not an
explanation.

**It judges the track, not one of its layers.** A simulcast track is sent over several RTP streams
and the sender moves between them constantly. The dry test is the **sum** of `deltaBytesSent` across
the layers, with `active: false` layers left out rather than counted as silence. Reading a single
stream instead reported a 640×360 camera as dry for fourteen minutes of a captured call while the
layer beside it sent a hundred kilobytes every collection.

`dryForInMs` and `durationInMs` are different quantities: how long the fault had lasted *before* it
was reported, and how long the report stayed open.

**What it does not claim.** Why nothing is leaving. Read `capture-source-lost`,
`video-capture-bottleneck`, `encoder-bottleneck` and `rtp-sender-stalled` first — the lowest
boundary that fired is the diagnosis, and `dry-outbound-track` on its own means none of them could
name it.

## Receive — transport to RTP streams (R1)

### `TransportDemuxStalledDetector` → `transport-demux-stalled`

The transport receiving at a media-level rate while every inbound RTP attributed to it reports zero
bytes. Packets are arriving that never reach a stream — which is what an SSRC mismatch after
renegotiation looks like from inside the browser, or a consumer created against a producer that is
already gone. **It is worth naming precisely because everything else looks healthy**: the transport
counters keep climbing, ICE is connected, no quality detector has anything to measure, and the
picture is simply never there.

```javascript
transportDemuxStalledDetector: {
    thresholdInMs: 4000,
    minTransportReceiveBitrateBps: 20000,  // above this, incoming traffic must demux
}
```

**Two guards, each ruling out a different false positive.** The bitrate floor rules out RTCP and
STUN consent explaining the arriving bytes. The at-least-one-inbound-RTP requirement rules out
**send-only transports** — the ordinary shape of an SFU publish transport has nothing to demux into
by design.

{{< callout context="caution" title="Blind on Firefox, and it says so" icon="alert-triangle" >}}
The upstream half of the comparison is `transport.receivingBitrate`, derived solely from
`RTCTransportStats.bytesReceived`, which **Firefox still does not populate as of 153**. There the
detector is permanently inert — it cannot tell an SSRC mismatch from a perfectly demuxing call. This
is one of the two cases `inputsUnavailable` was introduced for: the flag is set on exactly the tick
the detector would otherwise have judged, and a dashboard counting issues without counting it reads
every Firefox session as healthy on this boundary.
{{< /callout >}}

**`suspectedIssueTypes` is gone.** The predecessor annotated every `media-pipeline-stalled` payload
with the other issue types active on the peer connection. It read as helpful and was structurally
wrong three ways: it made one detector's output a function of every other detector's verdicts, it
made the output depend on the order detectors ran in, and it duplicated — badly and locally — work
the server is positioned to do properly. **Detection is not correlation.**

## Receive — the wire to the track (R2)

### `DryInboundTrackDetector` → `dry-inbound-track`

Media having stopped arriving — not degraded, not concealed, but *nothing*. This is "their video is
frozen" and "I cannot hear them" at their most literal, and it catches the transmission failures
that leave every quality detector quiet precisely because nothing is left to measure.

```javascript
dryInboundTrackDetector: { thresholdInMs: 5000 }
```

**Two kinds of deliberate silence, and it names which one it saw.** The resolve comment
distinguishes `consumer paused` — *this leg* is paused, a local opt-out, everyone else may be
receiving the producer fine — from `remote track paused`, where nobody is receiving it.

**Its relationship with `FrameAssemblyStalledDetector`: adjacent, not overlapping.**

| | `dry-inbound-track` | `frame-assembly-stalled` |
|---|---|---|
| Question | Is anything arriving? | Is what arrives becoming pictures? |
| Requires | `deltaBytesReceived === 0` | `deltaPacketsReceived > 0` |
| Reading | The sender, the SFU or the path stopped | The stream is being delivered and reassembly is failing |

They are **mutually exclusive by construction**, not by suppression, so neither needs a guard
against the other and neither reads the other's state.

## Receive — packets to frames (R3)

### `FrameAssemblyStalledDetector` → `frame-assembly-stalled`

**New in 4.9**, and the class that closed the last unwatched boundary on the receive side.
`packetsReceived` keeps advancing and `framesReceived` does not: RTP is being delivered and no
complete picture is being made from it. Either every frame is missing pieces, or the depacketizer
has lost the stream.

**Why the boundary was worth naming.** Before this class existed, the condition surfaced as
`stuck-decoder` — which points at the decoder for something that happened **before the decoder ever
saw a frame**. An engineer reading `stuck-decoder` reasonably investigates the codec, the hardware
path, the implementation string. Naming the wrong stage is worse than naming none, because it spends
the reader's time in the wrong place.

```javascript
frameAssemblyStalledDetector: {
    thresholdInMs: 3000,      // packets arriving with no frame completed, in stats time
    minPacketsReceived: 20,   // below this it is a trickle, not a stall
}
```

**Both bars must be cleared.** The packet floor is what separates a stall from a trickle — twenty
packets arriving with no frame out of them is a stream being delivered and not assembled, whereas
three packets is noise.

**How it and `StuckDecoderDetector` relate, without depending on each other:**

| | `frame-assembly-stalled` | `stuck-decoder` |
|---|---|---|
| Requires | Packets arriving, `deltaFramesReceived === 0` | `deltaFramesDecoded === 0`, `bitrate ≥ minBitrate` |
| Also requires | ≥ 20 packets, ≥ 3 s stats time | ≥ 2 PLIs, ≥ `max(4 s, 15 × RTT)` |
| Claim | Reassembly is producing nothing | Decoding is producing nothing, and repair was asked for |
| Fix it points at | The stream: loss inside every frame, a codec or depacketizer mismatch | Recreating the consumer |

The longer wait and the PLI evidence make `stuck-decoder` the slower of the two to raise on a shared
cause, which is the right ordering: the assembly statement is the more specific one and should be
the one a reader sees first.

## Receive — frames to decoder (R4)

Three classes on one boundary looks like duplication and is not. They differ in the *shape* of the
failure each can see, and each shape has a different fix:

| Class | Failure shape | Evidence | Verdict unit |
|---|---|---|---|
| `DecoderBottleneckDetector` | Graded shortfall, sustained | Decoded fps vs received fps over a window | A ratio over the inbound track window |
| `DecoderPerformanceDetector` | Decoding is expensive or lossy | Decode time per frame, frames dropped after arrival | Consecutive ticks |
| `StuckDecoderDetector` | Binary wedge | Nothing decodes at all, with RTP still flowing | `max(4 s, 15 × RTT)` and PLIs |

### `DecoderBottleneckDetector` → `decoder-bottleneck`

The receive-side counterpart of `video-capture-bottleneck`: frames arrived and the decoder did not
turn enough of them into pictures. The user sees video that judders or runs behind the audio while
the network is delivering perfectly well.

```javascript
decoderBottleneckDetector: {
    decodeDegradationThreshold: 0.1,  // 10% of arriving frames left undecoded
    minReceivedFps: 5,                // too thin a stream to judge a decoder on
}
// the span is inboundTrackWindow
```

**The bar is the measured arrival rate, never the sender's intent.** Frames that never arrived are
the network's story, told by `video-flow-disrupted` and the peer connection's loss reasons — so a
stream throttled to 5 fps that decodes cleanly is silent here.

`minReceivedFps` is not a substituted baseline; it only refuses a ratio taken over a handful of
frames.

### `DecoderPerformanceDetector` → `video-decoder-overloaded`

The client failing to decode what it was sent, measured by what decoding **cost** rather than by how
many frames went missing. It exists to make network-versus-client attribution possible at all:
frames missing because they never arrived and frames missing because the machine could not decode
them look identical in a frame-rate chart, and the two have opposite fixes.

Three gates before any symptom counts:

| Gate | Default | Stand-down comment |
|---|---|---|
| `minFramesReceived` frames in the interval | **10** | `not enough frames to evaluate` |
| A loss reading exists at all | — | `no loss reading; cannot clear the network` |
| Loss at or below `quietLossThreshold` | **0.02** | `loss dominates; not a decoder problem` |

The middle gate is the subtle one and it is right: **an absent measurement cannot exonerate the
network**, so a missing `deltaFractionLost` stands the detector down rather than letting it proceed
on an assumption.

```javascript
decoderPerformanceDetector: {
    decodeTimeBudgetRatio: 0.8,  // share of the per-frame budget decoding may use
    minFramesReceived: 10,
    quietLossThreshold: 0.02,
    minConsecutiveTicks: 2,
}
```

Past the gates, one symptom qualifies a tick: decode time per frame above `decodeTimeBudgetRatio` of
the budget the stream's own frame rate implies (`1000 / fps` — 33 ms at 30 fps, 66 ms at 15 fps).
The ratio is published either way as `InboundTrackMonitor.decodeBudgetUtilization`, so a decoder at
0.7 of its budget is distinguishable from one nobody measured.

**The overlap with `DecoderBottleneckDetector` is real, deliberate and kept:**

- `decoder-bottleneck` alone — frames are going missing across a sustained window and decoding is
  not visibly expensive. A supply-side or scheduling problem: the decode thread is not getting run.
- `video-decoder-overloaded` alone — decoding is expensive on this machine right now, without the
  sustained average having moved yet. The earlier, more specific warning, pointing at hardware
  acceleration, the codec, or a machine under load.
- Both — the unambiguous case, and two independent measurements agreeing is worth more than either.

### `StuckDecoderDetector` → `stuck-decoder`

The wedge: RTP keeps arriving and **no frame ever decodes again**. A corrupt or incomplete frame
breaks the decode chain, PLIs go out and keyframes may even be produced upstream, yet this consumer
never assembles a usable frame — until the track is recreated. It is a per-consumer fault, so
another consumer of the same producer keeps playing normally and only this client can see it.

```javascript
stuckDecoderDetector: {
    thresholdInMs: 4000,   // floor; effective wait = max(this, rttMultiplier × RTT)
    rttMultiplier: 15,     // high-RTT paths get more time to recover legitimately
    minBitrate: 10000,     // bps below which this is a dry track, not a wedge
    minPliCount: 2,
}
```

The wait scales with round trip because a wedge never self-heals, so it only has to outlast a
*legitimate* PLI → keyframe recovery — whose cost scales with RTT rather than being a fixed number
of seconds. The PLI requirement is independent evidence: the browser asking for repair confirms it
considers itself stuck.

**The `variant` discriminator**, set at raise time:

| `variant` | Condition | Reading |
|---|---|---|
| `decode` | Frames were assembled during the stretch | Assembly works, decoding does not — the wedge this issue is named for |
| `assembly` | No frame was ever assembled | The break is upstream — `frame-assembly-stalled` names it |
| `unknown` | The browser reports no `framesReceived` | No verdict is invented |

The `stuck-decoder` **monitor event is the hook for the application-side mitigation** — recreating
the consumer — which is the one place in this category where an issue names a specific remedy.

A tick with **no** reported `bitrate` holds the accumulated state rather than resetting it: the
distinction between "measured as low" and "not measured" is made deliberately.

## Receive — decoder to renderer (R5)

### `PlayoutDiscrepancyDetector` → `inbound-video-playout-discrepancy`

Video that arrives perfectly well over the network and never reaches the screen. The viewer sees a
frozen or stuttering tile while every network statistic reads healthy.

```javascript
playoutDiscrepancyDetector: {
    lowSkewRatio: 0.1,
    highSkewRatio: 0.25,
    minFramesReceived: 10,
}
```

`frameSkew = deltaFramesReceived − deltaFramesRendered`, and `skewRatio = frameSkew /
deltaFramesReceived`. An episode opens at `highSkewRatio` and closes only once the ratio falls below
`lowSkewRatio`.

**A ratio rather than a raw count, deliberately.** Five frames of skew is 8% of a 2-second interval
at 30 fps and 3% of a 5-second one, so a raw frame count would mean a different thing at every
collecting period and every frame rate.

**A boundary imprecision, recorded.** The comparison spans **decoding as well as painting**: a
decoder that is not decoding produces the same skew as a renderer that is not painting. The strict
R5 comparison exists and is already computed — `InboundRtpMonitor.renderRatio` — and nothing
thresholds on it. Tightening onto `renderRatio` would make the boundary exact at the cost of missing
frames that vanish between assembly and decode. The current arrangement is the wider net; the
imprecision is stated rather than papered over.

## Beside the receive chain — the repair loop

### `VideoRecoveryFailedDetector` → `video-recovery-failed`

Keyframes were requested, repeatedly, over a sustained stretch, and none arrived. A freeze that
repairs itself in a second is a lossy first hop; a freeze where PLI after PLI leaves the client and
`keyFramesDecoded` never moves points **past** the first hop — at forwarding, at a consumer wired to
a producer that is gone, at an encoder on the far side that stopped producing keyframes. **This is
the one issue in the category worth waking an SFU operator for.**

```javascript
videoRecoveryFailedDetector: {
    recoveryFailedThresholdInMs: 5000,  // stalled with PLIs out for this long
    recoveryFailedMinPliCount: 2,       // proof we actually asked for repair
}
```

The clock only starts once a keyframe has actually been asked for — a stall with no PLI in sight is
a real problem but a *different* one, since nothing was requested and so nothing failed to come back.

**Independence, worked twice.** The stall condition is derived here from raw counters
(`deltaFramesRendered === 0 && deltaKeyFramesDecoded === 0`) and deliberately **not** from
`InboundTrackMonitor.frameFlowState`, which is another detector's conclusion — a verdict resting on
that would die silently when `inboundVideoFlowStateDetector: null` is set, and would inherit
judgement calls made for a different question.

**Stand-downs behave differently here**: a backgrounded tab or either end being paused stands the
detector down **for the tick without resetting the counters**. The condition being measured is a
property of the stream that a pause does not undo.

## Across both chains — the machine

### `CpuPerformanceDetector` → `cpulimitation`

The documented exception in the category. Everything else is filed at a boundary; this one is filed
at a **cause**. Its evidence is entirely boundary evidence — the encoder shedding, decoded-versus-
received frames falling, encode time overrunning the per-frame budget, the stats loop itself running
late — but `cpulimitation` names *why* rather than *where*, and a saturated CPU shows up at S3 and
R4 simultaneously, which is the shape of a cause rather than a stage.

**Why it is kept here rather than triggering a sixth category.** A "Resource" category would need
exactly one member and would immediately become the place every hard-to-classify detector goes. The
library has one such gravity well in its history already: connectivity layer 6, retired in 4.9. One
strained member is cheaper than a category that attracts everything hard to classify.

**The measurement is utilization, over a window.** Codec time per unit of stats time, summed across
the video streams, where `0.25` means a quarter of the stretch was spent inside a codec. Summed
rather than averaged, so three simulcast layers busy half the time each read `1.5`.
`encoderUtilization` and `decoderUtilization` combine with `min()`, so codec work on one side alone
is a busy *stream* and work on both at once is a busy *machine*.

```javascript
cpuPerformanceDetector: {
    utilizationThreshold: 0.15,   // both halves of the pipeline, over clientWindow's detection slice
}
```

The sustain **is** the detection slice of `clientWindow`, which is why this detector counts no
duration of its own. `ClientMonitor.cpuUtilization` is published on every judgeable collection,
whether or not it raised.

**It is not CPU time.** `totalEncodeTime` is elapsed time inside the codec call, so a hardware codec
waiting on the GPU would count in full. Streams naming an off-CPU implementation, or flagged
`powerEfficient`, are left out as each collection's delta is taken.

**Deliberately not gated on `qualityLimitationReason === 'cpu'`.** Chrome's precedence is
`bandwidth > cpu > none`, so a machine that is both would report `bandwidth` and the gate would close
exactly where both problems are real.

**Stand-downs.** A backgrounded tab refuses judgement entirely and resolves any open alert —
throttled timers stretch the interval and read as an idle machine. A wholly hardware pipeline, or no
video at all, sets `inputsUnavailable` rather than reading as healthy.

## Reading a session

Read a session by starting at the **lowest boundary in the chain that fired**, because everything
above it is downstream of that break.

| Chain | Boundary | Issue type | Level |
|---|---|---|---|
| Send | the source | `capture-source-lost` | Outbound track |
| Send | the source | `silent-audio-source` | Outbound track |
| Send | S1 capture → frames | `video-capture-bottleneck` | Outbound track |
| Send | S2 processing | *(unwatched — no stat exists)* | — |
| Send | S3 frames → encoder | `encoder-bottleneck` | Outbound track |
| Send | S4 encoder → sender | `rtp-sender-stalled` | Peer connection, per ssrc |
| Send | S5 sender → wire | `dry-outbound-track` | Outbound track |
| Receive | R1 transport → streams | `transport-demux-stalled` | Peer connection, per transport |
| Receive | R2 wire → track | `dry-inbound-track` | Inbound track |
| Receive | R3 packets → frames | `frame-assembly-stalled` | Inbound track |
| Receive | R4 frames → decoder | `decoder-bottleneck` | Inbound track |
| Receive | R4 frames → decoder | `video-decoder-overloaded` | Inbound track |
| Receive | R4 frames → decoder | `stuck-decoder` | Inbound track |
| Receive | R5 decoder → renderer | `inbound-video-playout-discrepancy` | Inbound track |
| Both | repair loop | `video-recovery-failed` | Inbound track |
| Both | the machine | `cpulimitation` | Client monitor |

`media-pipeline-stalled` is not in this table and has no alias: it became `rtp-sender-stalled` and
`transport-demux-stalled` in 4.9, and one type cannot alias onto two.
