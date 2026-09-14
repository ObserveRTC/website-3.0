---
title: "Transport quality detectors"
description: "Capacity, delay and delivery reliability on a path that already works"
lead: "The path exists, ICE is connected, DTLS completed — is it carrying traffic well enough?"
date: 2026-09-13T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 232
toc: true
---

This is the reference for **category 2**. It exists because "the network is bad" is four different
faults with four different fixes, and until 4.9.0 the library could only name one of them.

```text
Connectivity (the path exists and holds)
        │
        ▼
Capacity              can the path carry what we want to send?
Delay                 how long does a round trip take?
Delivery reliability  does what we send actually arrive — some of it, any of it?
Delivery stability    does it arrive evenly?
        │
        ▼
Perceived quality (what the user sees and hears)
```

**These four are not a ladder.** A path can be slow without being congested, congested without
losing packets, and lossy without being either. They are independent properties of the same object,
measured concurrently — which is what makes their co-firing worth reading.

**Membership.** A detector belongs here when every connectivity stage completed and continues to
hold — the candidate pair is `succeeded`, consent keeps passing, `iceConnectionState` reads
`connected` — and the path is *still* the reason the call is bad.

## Congestion is not loss, and neither is delay

The most useful distinction in this category, and the one an operator reading co-firing issues most
needs.

**Congestion is the path being narrower than what is being put on it.** On the sending side the
evidence is the browser's own bandwidth estimate collapsing while this endpoint is still trying to
use it. On the receiving side there is no estimate to read at all, and the evidence is what arrived
collapsing while the jitter buffer deepens. Nothing has necessarily been lost. The remedy is fewer
layers, a lower target, a smaller resolution — or a wider path.

**Loss is packets vanishing, whether or not anyone backed off.** A well-behaved congestion
controller produces a congested path with very little loss, precisely because it backed off before
the queue overflowed. A lossy wireless link produces loss with no congestion signal at all: the
estimator is happy, the encoder is unthrottled, and one packet in twenty is eaten by radio
interference. The remedy is retransmission, FEC, or a different link — not a lower bitrate.

**Delay is the round trip being long on a path that may be losing nothing.** A relay allocated on
the wrong continent gives a 400 ms round trip with zero loss and no bandwidth limitation
whatsoever; every packet arrives, and conversation still fails because turn-taking needs the round
trip to be short. No amount of encoder backoff helps.

**None of them consults another to decide.** That is what makes co-firing worth reading:
`uplink-congestion` and `transport-loss-sustained` together mean something specific — a path narrow
enough that the estimator noticed *and* overflowing anyway — that neither means alone.

## The grid

| Sub-layer | Class | Issue | Config key | Coverage |
|---|---|---|---|---|
| Capacity | `UplinkCongestionDetector` | `uplink-congestion` | `uplinkCongestionDetector` | Needs `candidate-pair.availableOutgoingBitrate` **and** `outbound-rtp.qualityLimitationReason` |
| Capacity | `DownlinkCongestionDetector` | `downlink-congestion` | `downlinkCongestionDetector` | Needs inbound video `jitterBufferDelay` / `jitterBufferEmittedCount` |
| Capacity | `CongestionDetector` *(deprecated)* | `congestion` | `congestionDetector` | Needs `qualityLimitationReason`; permanently silent on Firefox |
| Delay | `TransportDelayDetector` | `transport-delay-degraded` | `transportDelayDetector` | RTCP or ICE round trip — available everywhere |
| Delivery reliability | `TransportLossDetector` | `transport-loss-sustained` | `transportLossDetector` | Inbound everywhere; outbound needs `remote-inbound-rtp.packetsReceived` |
| Delivery reliability | `BlockedStunRequestsDetector` | `blocked-stun-requests` | `blockedStunRequestsDetector` | Needs the pair's `deltaResponsesReceived` |
| Delivery reliability | `BlockedOutboundMediaDetector` | `blocked-outbound-media-transport` | `blockedOutboundMediaDetector` | Needs our own `deltaPacketsSent` |
| Delivery reliability | `BlockedInboundMediaDetector` | `blocked-inbound-media-transport` | `blockedInboundMediaDetector` | Needs the remote-outbound report; **`null` by default** |

Every class binds to `PeerConnectionMonitor`, except the three `Blocked*` classes, which live on
`IceTransportMonitor.detectors` — one instance judges one transport, because a peer connection
without BUNDLE has several and they can be blocked independently.

## Where the numbers come from

`PeerConnectionMonitor` owns the arithmetic; the detectors own the opinion.

| Value | Meaning |
|---|---|
| `avgRttInSec` | `rtcpRttInSec ?? iceRttInSec` — the RTCP round trip when remote reports exist, the ICE/STUN one otherwise |
| `avgInboundFractionLost` | Mean interval loss fraction over inbound streams that received packets this tick |
| `avgOutboundFractionLost` | Mean interval loss fraction the far end reported for the streams we send |
| `avgPacketSendDelayInMs` | Mean pacer queue time per packet, Δ`totalPacketSendDelay` over Δ`packetsSent` |
| `avgInboundVideoJitterBufferDelayInMs` | Mean time a video frame spent in the jitter buffer this tick |
| `availableOutgoingBitrate` | Summed over the selected pairs that reported one, `undefined` where none did |
| `qualityLimitationReason` | The most limiting reason across the streams that sent anything — streams that sent nothing do not vote |
| `deltaTime` | Milliseconds between this stats collection and the previous one, from the reports' own timestamps |

{{< callout context="caution" title="The averages exclude streams that carried nothing" icon="alert-triangle" >}}
Any inbound stream whose `deltaPacketsReceived` is zero or absent is skipped, and when no stream
qualifies the average is `undefined` rather than `0`. A call with eight muted tracks and one
bleeding one would otherwise average to a ninth of the real loss and read as healthy. Every
detector reading these values stands down on `undefined` and says so through `inputsUnavailable`.
{{< /callout >}}

## The threshold-and-stats-clock shape

`TransportLossDetector` has this shape (delay moved onto the shared window in 4.9). It reads one
value, compares it against a **raise threshold** and a **recovery threshold**, and accumulates time
above the raise threshold in **stats time** until a **duration** is satisfied:

```text
value < recoveryThreshold             → accumulator = 0, resolve any standing issue
recoveryThreshold ≤ value < threshold → hold whatever state exists
threshold ≤ value                     → accumulator += deltaTime; raise at durationInMs
```

**The gap between the two thresholds is a hold zone.** A call parked exactly on the line would flap
the issue open and shut on every collection if one number governed both directions, and a dashboard
would show twenty episodes for one continuously mediocre network. Nothing accumulates in the band,
and nothing resolves in it.

The accumulator is cleared **only** by falling below the recovery threshold, so a path that
oscillates between the band and above the raise threshold keeps its accumulated time across the
dips and eventually raises. `sustainedForInMs` is therefore time spent above the threshold, not
necessarily one unbroken stretch of it.

**The defaults are round numbers meant to be tuned.** Only the delay threshold has an external
reference behind it (ITU-T G.114 puts one-way "generally acceptable" at 150 ms, and turn-taking
starts to break down around a 300 ms round trip).

## Capacity

Two detectors, one per direction, because the evidence is not the same evidence. The sending side
can read the browser's own bandwidth estimate; the receiving side has none to read and has to
rebuild the verdict from what arrived.

### `UplinkCongestionDetector` → `uplink-congestion`

`qualityLimitationReason === 'bandwidth'` decides *whether* this is congestion; two witnesses
decide *how deep*, and each is already a fraction of this connection's own normal, so neither needs
a scale to be configured:

- **`undershoot`** — how far `availableOutgoingBitrate` has fallen below the highest it recently
  reached. The maximum is a **decaying** one: it fades on a half-life of about three minutes of
  stats time rather than dropping out of a window.
- **`pacerBloating`** — how far `avgPacketSendDelayInMs` sits above its own running median, with
  four times the median as the top of the scale and a 1 ms noise floor under the baseline.

They combine as a **geometric mean**, so a witness at its healthy level takes the severity to zero
rather than merely failing to add: a path narrowing with the pacer empty is an encoder that was
asked for less — a muted camera, a replaced track, a screen share of a still slide — and a pacer
filling on an unchanged path is a hiccup.

The anchor change was measured, not argued. Against a loopback call throttled to 500 kbit on
Chromium 141:

| Signal | Healthy | Throttled | Verdict |
|---|---|---|---|
| `qualityLimitationReason === 'bandwidth'` | true | true | precision 0.53 — useless alone |
| `availableOutgoingBitrate` | 1161 kbps | ~400, recovering to 1025 | tracks cleanly |
| `packetsDiscardedOnSend` | 0 | 0 throughout | a socket-error counter, not congestion |

**How it recovers.** When the browser stops reporting a bandwidth limitation, and on nothing else.
There is no recovery threshold on any bitrate, because nothing knows what the path can carry after
it narrows — a link that settles at half its old capacity has recovered, and a ratio against its
old maximum would hold the finding open for the rest of the call.

```javascript
uplinkCongestionDetector: {
    minSeverity: 0.65,   // how deep the trouble has to be, 0..1
}
```

**What it does not claim.** Not that packets were lost. Not that the round trip is long. Not where
the narrow part of the path is. Nothing about the receiving direction, and nothing about what the
far end sees.

### `DownlinkCongestionDetector` → `downlink-congestion`

**Why it cannot read an estimate.** `availableIncomingBitrate` is specified, and on Chrome it is
not zero but *absent* — structurally, because Chrome's congestion control is send-side, so the
estimate for your downlink is computed at the far end's sender and never reaches you.

Two witnesses, same shape as the uplink:

- **`undershoot`** — how far `receivingBitrate` has fallen below its recent decaying maximum.
- **`bufferBloating`** — how far `avgInboundVideoJitterBufferDelayInMs` sits above its own running
  median, with four times the median as the top of the scale and a 10 ms noise floor.

Combined as a geometric mean, which is what separates a far end that was *asked* for less
(undershoot with the buffer flat) from a path running out of room.

**Nothing gates on `qualityLimitationReason`**, unlike the uplink detector: that verdict describes
this endpoint's *encoder*, so reading it would make a receive-only connection — a webinar attendee,
a spectator — permanently blind, which is the population most in need of a downlink verdict.

**How it recovers.** When the severity falls back under half of `minSeverity`; the gap is the
hysteresis. The maximum keeps being fed while a finding is open and an episode cannot inflate it,
so a link that settles at half its former bandwidth is compared against what it now has and the
undershoot returns to zero on its own.

**The baselines.** The maximum takes every collection; the median takes only collections with no
finding open, because a sustained bloat would drag it up and talk the episode out of existence.
Both are read *before* the collection under judgement joins them, so a collection cannot move its
own baseline.

**The faster fade after an episode.** Both capacity detectors carry it: for 30 seconds of stats
time after a finding closes, the recent maximum decays on a ~34 second half-life instead of three
minutes. A path that lost capacity rarely gives all of it back, and without this a second dip
arriving inside that window is scored against a peak the path no longer reaches.

```javascript
downlinkCongestionDetector: {
    minSeverity: 0.65,
}
```

**The neighbour it must not echo.** `JitterBufferStressDetector` also reads a jitter buffer under
strain. It is audio, per track, and reports what the listener hears; this is video, per connection,
reports capacity, and counts the buffer only when the bitrate has already collapsed underneath it.
If the two are ever found firing on the same episodes, this one has not earned its place.

### The `congestion` event, and the deprecated detector

Two issue types, because two questions answered from two sets of evidence are two findings. But "is
this connection capacity-limited at all" is a fair thing to want in one word, so both detectors also
emit a **`congestion` event**, discriminated on `direction`, carrying the whole payload of whichever
fired. `PeerConnectionMonitor.congested` is the same reading as an attribute —
`uplinkCongested || downlinkCongested`, read-only, because a single writable boolean could not say
which direction it meant.

The convenience stops at the event. Neither detector raises a combined *issue*: an issue is a
condition with a start and an end, and the two directions start and end independently.

{{< callout context="caution" title="CongestionDetector is deprecated" icon="alert-triangle" >}}
The `congestion` **issue** type is raised by `CongestionDetector` alone, kept only so integrations
built against it keep working. It answers for both directions from one signal, which a receiver
cannot support, and it is permanently silent on Firefox — its anchor
`outbound-rtp.qualityLimitationReason` is among the values `FirefoxStatsAdapter` deliberately leaves
absent, and this is the one transport-quality detector that does **not** set `inputsUnavailable`, so
that silence is indistinguishable from a healthy path.

Set `congestionDetector: null` and take `uplink-congestion` / `downlink-congestion` instead. The
shipped score calculator ignores `congestion` so the same episode is never charged twice.
{{< /callout >}}

## Delay

### `TransportDelayDetector` → `transport-delay-degraded`

A path that works and takes too long: the round trip stays high enough, for long enough, that
conversation stops being conversation and becomes turn-taking.

**The signal** is the mean round trip over `PeerConnectionMonitor.slicedWindow`:
`totalRoundTripTime` divided by the number of measurements that produced it, across a span the
window states in milliseconds. A single inflated RTT sample is common and means nothing — one
retransmission, one scheduling hiccup, one RTCP report that sat in a queue.

**Why it is no longer `ewmaRttInSec`.** That EWMA has a fixed α of 0.1, so its memory is set by how
often stats are collected: roughly a minute at a five-second collecting period, under half that at
two. A `durationInMs` written against one cadence meant something else on another. A window states
its span in milliseconds and means the same thing everywhere — which is why this detector no longer
counts a duration of its own. **The sustain *is* the detection window**, configured under
`peerConnectionWindow`.

**RTCP is preferred over ICE per reading, not once per call.** The two span different paths and are
held as separate totals that are never summed. Each reading picks RTCP when RTCP measurements moved
within the window and ICE otherwise, so an RTCP stream that stops being reported produces no RTCP
reading and the detector falls back. The chosen source travels with the issue as `rttSource`.

```javascript
transportDelayDetector: {
    thresholdInMs: 300,           // mean RTT at or above which the path counts as slow
    recoveryThresholdInMs: 200,   // the recovery window must read below this to resolve
}
// the sustain is peerConnectionWindow, not a duration here
```

**False positives.** The measurement is a mean across selected candidate pairs and across
RTCP-reporting streams, so a peer connection without BUNDLE, or one talking to two destinations at
very different distances, produces a mean that describes neither. Relay paths — TURN/TCP and
TURN/TLS especially — legitimately add tens of milliseconds and can sit near a 300 ms threshold
while working exactly as designed.

{{< callout context="caution" title="It is not end-to-end latency" icon="alert-triangle" >}}
In an SFU topology the ICE round trip is measured to whatever terminates ICE — the SFU — and the
RTCP round trip spans the media path to whatever originates the RTCP reports, which in most SFU
deployments is also the SFU. Either way this is a **half-path** measurement, blind to the far leg: a
150 ms reading here is perfectly compatible with a listener 400 ms away. An application presenting
this number to a user as "latency" is overstating what was measured.
{{< /callout >}}

## Delivery reliability

Two kinds of finding, and the pairing is the point: `transport-loss-sustained` is a path dropping a
*share* of what crosses it, and the `blocked-*` issues are a path dropping *all* of one kind of
traffic for a reason that is policy rather than capacity.

### `TransportLossDetector` → `transport-loss-sustained`

The path is up, the path is stable, and packets are simply not all arriving. Loss has always been
*visible* to the library — it gated the old congestion detector's low-sensitivity mode and it stands
`DecoderPerformanceDetector` down — but until 4.9 nothing could raise it, resolve it, or count it.

Both directions are watched with one threshold and **whichever is worse is reported**, as one issue
type with `direction` in the payload, because the engineer's next step is the same either way. An
exact tie breaks towards `inbound`.

Where one direction is absent the other is still judged: a publish-only peer connection has no
inbound RTP, so the outbound mean carries the verdict alone. `inputsUnavailable` is set only when
**both** are absent.

```javascript
transportLossDetector: {
    threshold: 0.05,          // mean interval loss fraction (0..1), worse direction wins
    recoveryThreshold: 0.01,
    durationInMs: 6000,
}
```

**False positives.** *Loss at low packet rates is noisy.* An audio stream at 50 packets per second
contributes 100 packets to a two-second interval, so a single lost packet is 1% and three are 3%.
There is no minimum packet count in this detector, and the six-second duration is the only thing
standing between it and that noise — which is why the duration matters more here than the threshold
does.

The mean across streams is also a real simplification: nine healthy streams and one at 40% average
to 4% and raise nothing, while the one stream is unusable. This detector is a statement about the
*path*; per-stream loss is a different question.

**Coverage.** Inbound loss works everywhere. The outbound half needs both `packetsLost` and
`packetsReceived` on `remote-inbound-rtp`, and WebKit has never filled
`remote-inbound-rtp.packetsReceived` (through Safari 26) — so on Safari this detector judges the
inbound direction alone, without setting `inputsUnavailable`, because one direction genuinely was
measured. A Safari session reporting `direction: 'inbound'` should not be read as evidence that the
send path was fine.

### The blocked-media detectors

The signature of a firewall — or any policy middlebox — that lets ICE and STUN through while
blocking the media itself: the candidate pair is `succeeded`, consent checks keep passing,
`iceConnectionState` reads `connected`, and the call carries nothing.

**Why nothing else can see it.** STUN consent responses count into the candidate pair's
`bytesReceived`, so the pair never looks dry and `IceTransportStalledDetector`'s inbound-stall check
never fires. The dry-track detectors watch producer-side `outbound-rtp` counters, which keep
advancing because the encoder is doing its job perfectly well. The gap between "STUN says the path
is alive" and "no media traverses it" is visible only to something comparing those two facts.

#### `BlockedStunRequestsDetector` → `blocked-stun-requests`

The path stopped answering while this endpoint was still asking.

| Gate | Config | Default | Why |
|---|---|---|---|
| The pair reached `succeeded` first | — | — | A path that never answered is ordinary establishment failure |
| We are still asking | `requestsSentTimeoutInMs` | `10000` | Consent counts as well as connectivity checks — after nomination, consent is the only STUN still leaving |
| Nothing is answering | `responseReceivedTimeoutInMs` | `10000` | Consent runs roughly every 5 s, so the window comfortably exceeds one interval |

Payload: `silentForMs`, `requestsSent`, `currentRoundTripTime`, `pathKind`. While the finding is
open the transport is marked `blocked`. This detector emits the **`blocked-transport` event** — the
older name, kept; the issue of that name is gone.

#### `BlockedOutboundMediaDetector` → `blocked-outbound-media-transport`

We sent and nothing got through. Requires at least one outbound RTP stream reporting
`deltaPacketsSent`, and raises once packets have been handed over with none leaving for
`thresholdInMs` (default `10000`). Payload: `packetsSent`, `blockedForMs`, `pathKind`.

#### `BlockedInboundMediaDetector` → `blocked-inbound-media-transport`

The far end sent and nothing arrived. It rests on the remote-outbound report's `deltaPacketsSent`
to establish that anything was sent at all. **This is the one class in the library not registered
unless its key is supplied** — it only fires where RTCP survives whatever killed the media, which
`rtcp-mux` makes rare.

The asymmetry is the reason: sending, the client holds both halves — it produced the bytes and it
reads what the transport put on the wire. Receiving, it holds one half. A dry return path with no
remote report to lean on is [`dry-inbound-track`](../detectors-pipeline/)'s finding, not this one's.

**Nothing is gated on media having flowed successfully first.** A blocked transport is normally
blocked from its first packet: the user is behind a corporate firewall, nothing gets out, and
reloading puts them behind the same wall. Any bar of the form "it was carrying media and then
stopped" would switch the detector off in exactly the case it exists to explain.

**Coverage, and why these set `inputsUnavailable`.** The transport send bitrate has a substitute —
Firefox still does not populate `RTCTransportStats.bytesSent` as of 153, so the detector falls back
to the selected pair's own `deltaBytesSent` over the transport's measured `deltaTime`, which is a
different real measurement of the same traffic. **The consent counter has no substitute, and none is
invented**: `responsesReceived` reached Firefox only in 142, and without it there is no telling a
firewall from a dead path, so the transport is not judged at all. Note `deltaResponsesReceived === 0`
is a *reported fact* and the detector sees fine; only `undefined` is blindness.

## Delivery stability

**No detector answers it at this layer, and that is deliberate.** A `TransportJitterDetector`
reading `avgInboundJitterInMs` against an absolute threshold existed briefly during 4.9 development
and was removed before release:

- **It was not independent evidence.** Its intended pairing was with `JitterBufferStressDetector`,
  but NetEQ's `jitterBufferTargetDelay` *is* the receiver's response to inter-arrival jitter, so the
  two move together by construction. Their agreement is an echo, not a second opinion.
- **The averaged input loses its meaning.** `avgInboundJitterInMs` is an unweighted mean over every
  inbound stream, audio and video together. Video inter-arrival jitter is inflated by frame bursting,
  so one video stream can carry the mean past an absolute threshold on a path whose audio is arriving
  perfectly.
- **Both halves were already covered on self-relative baselines** — `JitterBufferStressDetector` for
  the listener, `DownlinkCongestionDetector`'s `bufferBloating` witness for the viewer.

`PeerConnectionMonitor.avgInboundJitterInMs` stays public for applications that want the number.
What is gone is the opinion about it — and with it a flat `0.5` subtraction from a connection score
for a condition two detectors already price by severity.

## What this model deliberately does not do

- **No composite "network quality" verdict.** A composite would have to weigh four independent
  measurements against each other, and the weighting that is right for a conversational audio call
  is wrong for a screen share.
- **No detector consults another.** Where two need the same input they read the raw value, not each
  other's conclusion.
- **No per-track transport issue.** The subject is the path; per-stream numbers are on the inbound
  RTP monitors for anything that wants them.
- **No congestion detector that works without the browser's verdict.** It could in principle be
  inferred from a rising round trip and a falling send rate, but the inference is much weaker than
  the estimator's own report and would produce a detector whose behaviour differed by browser in
  ways consumers could not see.

## The neighbours

**Below: connectivity.** Everything here presupposes the path exists. When a session raises both a
connectivity issue and a transport-quality one, read the connectivity issue first.

**Above: perceived quality.** The clearest pairing in the taxonomy is `transport-loss-sustained` and
`invented-speech` — one measures packets not arriving, on the peer connection; the other measures
the jitter buffer fabricating audio to cover what did not arrive, on one inbound audio track. They
are not a chain, and that is the point: cause and symptom confirmed by two separate measurements is
evidence, whereas a symptom detector that only fires when a cause detector already fired adds
nothing.
