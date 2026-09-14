---
title: "Detectors"
description: "The detector taxonomy of client-monitor-js — five categories, 46 classes, 37 issue types"
lead: "A detector watches one thing, decides one question, and raises exactly one issue type"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 230
toc: true
---

"The call was bad" is not a diagnosis. The library ships **46 detector classes** raising **37 issue
types**, grouped into five categories, so that an engineer reading a failed session knows which of
four completely different investigations to start — and which facts to read alongside them.

```text
1  CONNECTIVITY          Can this endpoint establish and keep the path?
        │
        ▼
2  TRANSPORT QUALITY     The path exists — is it carrying traffic well enough?
        │
        ▼
3  PIPELINE DISRUPTION   Did the media chain stop, or do two components disagree?
        │
        ▼
4  PERCEIVED QUALITY     Is what the user actually sees and hears degraded?

        ┌───────────────────────────────────────────────────────────┐
        │  5  TELEMETRY   What is this session's shape, and what     │
        │                 changed about it?  (beside, not below)     │
        └───────────────────────────────────────────────────────────┘
```

**Categories 1–4 are ordered; category 5 sits beside them.** The arrows are the order to read a
failed session in: **start at the lowest category that raised an issue** and treat the rest as
consequences. They are not a dependency — nothing inside the library chains them.

{{< card-grid >}}
{{< link-card title="Connectivity" description="Nine classes across the five layers a connection climbs, plus the restart telemetry beside them." href="../detectors-connectivity/" >}}
{{< link-card title="Transport quality" description="Capacity, delay and delivery reliability on a path that already works." href="../detectors-transport-quality/" >}}
{{< link-card title="Pipeline disruption" description="Fifteen classes on the send and receive media chains — the boundary where progress stopped." href="../detectors-pipeline/" >}}
{{< link-card title="Perceived quality" description="What the participant actually sees and hears, and the proxies used to judge it." href="../detectors-perceived-quality/" >}}
{{< link-card title="Telemetry" description="The eight classes that record facts and never raise an issue." href="../detectors-telemetry/" >}}
{{< /card-grid >}}

## What decides the category

Not "where in the stack" — that cut fails, because the same place in the stack produces completely
different kinds of failure. The discriminator is **what the detection algorithm looks for**.

| | Question | Detection shape — reads like | Membership test |
|---|---|---|---|
| **1 Connectivity** | Can this endpoint establish and keep the communication path? | A stage's proof of progress is missing altogether: ICE never nominated a pair; DTLS never completed | The subject is the path itself, and the failure is a stage that never completed or stopped holding |
| **2 Transport quality** | The path is established and stable — is it carrying traffic well enough? | A continuously-measured property of a *working* path is bad: round trip above 300 ms for six seconds; loss above 5% | Every stage completed, and the path is still the reason the call is bad |
| **3 Pipeline disruption** | Did the media chain stop somewhere, or do two adjacent components disagree? | A monotonic counter went flat, or two adjacent ones disagree: frames encode, no packets leave | You can name the boundary at which progress stopped |
| **4 Perceived quality** | Is what the user sees and hears degraded, badly enough and long enough to matter? | A perceptual value is severely degraded and *stays* degraded | Everything is still running, and it is still bad |
| **5 Telemetry** | What is this session's shape, and what changed about it? | A fact changed, and no threshold on it would ever be right: the codec switched; the selected tuple moved | Would raising an issue here *ever* be the right thing to do? If no, it is telemetry |

That test is mechanically checkable, which is the point: ask whether a new detector watches for
something to **stop** (disruption) or for a number to **get bad and stay bad** (quality), and
whether the subject is the **path**, the **endpoint's media chain** or the **user's experience**.

**Category is not subject.** `IceTraversalDetector`, `IceRestartDetector` and
`IceRestartRecommendationDetector` are telemetry even though everything they read is a connectivity
fact: needing TURN is a cost rather than a fault, a path that moved once is a handover, and a
restart is what a healthy application *does* when the network changes underneath a call.

## The five design rules

### 1. One detector class raises exactly one issue type

A detector that would raise two different issues is two detectors. The reasons are practical:
`Detectors.update()` wraps each `update()` in its own try/catch, `disabled` and
`includeIssueInSample` are per detector, and several conditions in one class accumulate shared
state that couples them.

A detector may still carry a **payload discriminator** where one condition has two forms an
engineer would investigate the same way — `video-flow-disrupted`'s `state`,
`transport-loss-sustained`'s `direction`. The test: "nothing, but I would want to know which" is a
field; "an entirely different investigation" is a second detector.

### 2. Implementations stay deliberately simple

There is no shared base class and no helper for "accumulate a duration and raise past a threshold",
even though roughly half the detectors do exactly that. Duplicated straightforward bookkeeping is
preferred to a shared abstraction, so each file reads start to finish without reading any other.

**The one boundary: derived values live on the monitored object.** The monitor computes the fact;
the detector holds the opinion. `bitPerPixel`, `ewmaFps`, `fpsVolatility`, `timeStretchRate` and
the jitter-buffer delays live on `InboundRtpMonitor`; `avgInboundFractionLost`, `avgRttInSec` and
`ewmaRttInSec` on `PeerConnectionMonitor`; `sourceFps` and `rmsAudioLevel` on `MediaSourceMonitor`.
As of 4.9 **no detector re-derives a value the monitor also computes.**

### 3. Condition duration is measured in stats time

A detector measuring how long something has held accumulates the monitored object's **`deltaTime`**
— the difference between consecutive stats reports' timestamps — rather than wall-clock elapsed.
`Date.now()` survives for the issue lifecycle only (`raisedAt`, `durationInMs`, `resolvedAt`).

This matters most in exactly the conditions these detectors fire under. A saturated main thread or
a backgrounded tab makes collections run late; measured against the wall clock, a tab hidden for a
minute has "watched" a minute of failing gathering and stalled handshakes, and every duration
threshold crosses at once on the tick it comes back, on evidence nobody observed. It cuts the other
way too: a late collection means the condition held *longer* than one nominal period, and
`deltaTime` credits it with that.

Two documented exceptions measure the *instrument* rather than the call:
`CpuPerformanceDetector`'s `durationOfCollectingStatsInMs` signal, and `StatsGapDetector` entirely
— how late the library ran is exactly what the latter exists to measure.

### 4. One detector, one config block

Every detector reads a block keyed by its `name` in camelCase, and nothing else. Where two
detectors genuinely want the same tunable, **each carries its own copy with its own default** —
the duplication is the point, since two detectors asking different questions of the same
measurement should be able to disagree about where the line is.

```javascript
new ClientMonitor({
    pixelatedVideoDetector: { threshold: 0.03 },  // tune it
    codecChangeDetector: null,                    // or never construct it
});
```

A detector with nothing to tune still gets a key: `dtlsHandshakeFailedDetector`,
`iceConnectionFailedDetector` and `iceTraversalDetector` are typed `Record<string, never>` — `{}`
enables, `null` disables — because "nothing to tune" is not a reason to make a detector the one
nobody can switch off.

### 5. A detector never infers the raw stats it needs

*Adapters* make the stats spec-conformant, *monitors* derive facts from spec-conformant stats,
*detectors* threshold those facts. Compensating for a browser that omits a spec-required field
belongs in the adapter and nowhere else.

Reading a *different real measurement of the same traffic* is not inference and is fine:
`BlockedInboundMediaDetector` reads the far end's `deltaPacketsSent` off the remote-outbound report
to establish that media was sent at all. What the rule forbids is manufacturing the observation.
**A detector that guesses is worse than one that stays quiet**, because quiet is honest — which is
what `inputsUnavailable` exists to make it.

## Detectors are independent

Every detector reaches its verdict from raw observations alone. No built-in detector reads another
detector's issue, and registration order carries no meaning — so any detector may be disabled at
runtime, and a custom detector inserted anywhere, without side effects.

Two detectors firing at once for the same underlying cause is expected and fine: an overloaded
encoder and a frozen picture are two true observations, and **correlating them is the server's
job** — see [`observer-js`](/docs/observer-js/).

## When inputs are missing

A detector that stays quiet is saying one of two completely different things: *nothing is wrong*,
or *the browser did not report the stats I need*. From the outside those look identical, and a
dashboard counting issues reads the second as a healthy session.

```javascript
const d = pcMonitor.detectors.getByName('transport-delay-detector');
if (d?.inputsUnavailable) chart.markUnobserved();
```

`inputsUnavailable` is a public boolean on the fourteen classes that can compute it, set per tick
and only for missing **evidence**. A detector standing down because a track is paused or a sender
is muted is *not* unavailable — that is "not applicable", a different statement. **The flag changes
nothing about the verdict**; it only makes the silence legible.

`AVDesyncPlayoutDetector` is the clearest illustration: it needs a video track the application has
declared as this audio track's pair *and* an `estimatedPlayoutTimestamp` on both — a field Firefox
populates, Chrome exposes only when A/V sync is enabled internally, and Safari does not report at
all. Without the flag, an application that never declared a pairing and a fleet running mostly
Safari would both look exactly like a fleet with perfect lip sync.

## Issue, event, metric or attribute

Not every useful observation is a problem, and the fastest way to make a category worthless is to
fill it with things nobody can act on.

| | Meaning | Lifecycle | Example |
|---|---|---|---|
| **Issue** | A condition an engineer would act on differently from its neighbours | Raised, held, resolved | ≥3 selected-pair changes in 30 s |
| **Event** | Something happened, with a timestamp and a from/to | Fires once, gone | A candidate pair changed once; an ICE restart |
| **Metric** | A number useful trended, meaningless as a single reading | Sampled | `selectedCandidatePairChanges`; relay time share |
| **Attribute** | A property of the session, constant until it changes | On the sample, re-sent when it changes | The selected path is TURN/TLS; the codec in use |

The test every proposed issue must pass: **what does an engineer do differently after seeing this,
that they would not do for the issue next to it?** The damage a mis-filed issue does is not the
false alarm but the reflex — an issue firing on a third of a healthy fleet's sessions trains
operators to filter the whole category out.

## The full index

**46 classes, 37 issue types, 9 event-only classes.** One class, one issue type — so within each
table the class column and the issue column are the same list read twice. The config-key column is
one-to-one in both directions: passing `null` for one leaves exactly one class unregistered.

### Category 1 — Connectivity

**9 classes, 8 issue types**, all bound to `PeerConnectionMonitor`.
[Full reference →](../detectors-connectivity/)

| Class | `name` | Raises | Layer | Config key |
|---|---|---|---|---|
| `IceReachabilityDetector` | `ice-reachability-detector` | `no-available-ice-candidate` | 1 — Reachability | `iceReachabilityDetector` |
| `IcePathEstablishmentDetector` | `ice-path-establishment-detector` | *event only* — `ice-path-establishment-slow` | 3 — Path establishment | `icePathEstablishmentDetector` |
| `IceEstablishmentFailedDetector` | `ice-establishment-failed-detector` | `ice-establishment-failed` | 3 — Path establishment | `iceEstablishmentFailedDetector` |
| `DtlsHandshakeFailedDetector` | `dtls-handshake-failed-detector` | `dtls-handshake-failed` | 4 — Secure transport | `dtlsHandshakeFailedDetector` |
| `DtlsHandshakeStalledDetector` | `dtls-handshake-stalled-detector` | `dtls-handshake-stalled` | 4 — Secure transport | `dtlsHandshakeStalledDetector` |
| `IceDisconnectedDetector` | `ice-disconnected-detector` | `ice-disconnected` | 5 — Path continuity | `iceDisconnectedDetector` |
| `IceConnectionFailedDetector` | `ice-connection-failed-detector` | `ice-connection-failed` | 5 — Path continuity | `iceConnectionFailedDetector` |
| `IceTransportStalledDetector` | `ice-transport-stalled-detector` | `ice-transport-stalled` | 5 — Path continuity | `iceTransportStalledDetector` |
| `UnstableIcePathDetector` | `unstable-ice-path-detector` | `unstable-ice-path` | 5 — Path continuity | `unstableIcePathDetector` |

### Category 2 — Transport quality

**8 classes, 8 issue types**, all bound to `PeerConnectionMonitor`.
[Full reference →](../detectors-transport-quality/)

| Class | `name` | Raises | Sub-layer | Config key |
|---|---|---|---|---|
| `CongestionDetector` | `congestion-detector` | `congestion` *(deprecated)* | Capacity | `congestionDetector` |
| `UplinkCongestionDetector` | `uplink-congestion-detector` | `uplink-congestion` | Capacity | `uplinkCongestionDetector` |
| `DownlinkCongestionDetector` | `downlink-congestion-detector` | `downlink-congestion` | Capacity | `downlinkCongestionDetector` |
| `TransportDelayDetector` | `transport-delay-detector` | `transport-delay-degraded` | Delay | `transportDelayDetector` |
| `BlockedInboundMediaDetector` | `blocked-inbound-media-detector` | `blocked-inbound-media-transport` | Delivery reliability | `blockedInboundMediaDetector` |
| `BlockedOutboundMediaDetector` | `blocked-outbound-media-detector` | `blocked-outbound-media-transport` | Delivery reliability | `blockedOutboundMediaDetector` |
| `BlockedStunRequestsDetector` | `blocked-stun-requests-detector` | `blocked-stun-requests` | Delivery reliability | `blockedStunRequestsDetector` |
| `TransportLossDetector` | `transport-loss-detector` | `transport-loss-sustained` | Delivery reliability | `transportLossDetector` |

### Category 3 — Pipeline disruption

**15 classes, 15 issue types** — the largest category.
[Full reference →](../detectors-pipeline/)

| Class | `name` | Raises | Boundary | Config key |
|---|---|---|---|---|
| `CpuPerformanceDetector` | `cpu-performance-detector` | `cpulimitation` | Across both chains — the machine | `cpuPerformanceDetector` |
| `VideoRecoveryFailedDetector` | `video-recovery-failed-detector` | `video-recovery-failed` | Beside the receive chain — the repair loop | `videoRecoveryFailedDetector` |
| `PlayoutDiscrepancyDetector` | `playout-discrepancy-detector` | `inbound-video-playout-discrepancy` | Receive — decoder to renderer | `playoutDiscrepancyDetector` |
| `DecoderBottleneckDetector` | `decoder-bottleneck-detector` | `decoder-bottleneck` | Receive — frames to decoder | `decoderBottleneckDetector` |
| `DecoderPerformanceDetector` | `decoder-performance-detector` | `video-decoder-overloaded` | Receive — frames to decoder | `decoderPerformanceDetector` |
| `StuckDecoderDetector` | `stuck-decoder-detector` | `stuck-decoder` | Receive — frames to decoder | `stuckDecoderDetector` |
| `FrameAssemblyStalledDetector` | `frame-assembly-stalled-detector` | `frame-assembly-stalled` | Receive — packets to frames | `frameAssemblyStalledDetector` |
| `DryInboundTrackDetector` | `dry-inbound-track-detector` | `dry-inbound-track` | Receive — the wire to the track | `dryInboundTrackDetector` |
| `TransportDemuxStalledDetector` | `transport-demux-stalled-detector` | `transport-demux-stalled` | Receive — transport to RTP streams | `transportDemuxStalledDetector` |
| `DryOutboundTrackDetector` | `dry-outbound-track-detector` | `dry-outbound-track` | Send — RTP sender to the wire | `dryOutboundTrackDetector` |
| `VideoCaptureBottleneckDetector` | `video-capture-bottleneck-detector` | `video-capture-bottleneck` | Send — capture to frame supply | `videoCaptureBottleneckDetector` |
| `RtpSenderStalledDetector` | `rtp-sender-stalled-detector` | `rtp-sender-stalled` | Send — encoder to RTP sender | `rtpSenderStalledDetector` |
| `EncoderBottleneckDetector` | `encoder-bottleneck-detector` | `encoder-bottleneck` | Send — frames to encoder | `encoderBottleneckDetector` |
| `CaptureSourceLostDetector` | `capture-source-lost-detector` | `capture-source-lost` | Send — the source | `captureSourceLostDetector` |
| `SilentAudioSourceDetector` | `silent-audio-source-detector` | `silent-audio-source` | Send — the source | `silentAudioSourceDetector` |

### Category 4 — Perceived quality

**6 classes, 6 issue types.** All bind to `InboundTrackMonitor` except
`AudioPlayoutSynthesisDetector`, which binds to `MediaPlayoutMonitor` — perception happens at the
receiver, so a sender-side detector reporting the far end's experience would be guessing.
[Full reference →](../detectors-perceived-quality/)

| Class | `name` | Raises | Sub-layer | Config key |
|---|---|---|---|---|
| `InventedSpeechDetector` | `invented-speech-detector` | `invented-speech` | Audio — continuity | `inventedSpeechDetector` |
| `AudioPlayoutSynthesisDetector` | `audio-playout-synthesis-detector` | `synthesized-audio` | Audio — naturalness | `audioPlayoutSynthesisDetector` |
| `JitterBufferStressDetector` | `jitter-buffer-stress-detector` | `audio-jitter-buffer-stress` | Responsiveness | `jitterBufferStressDetector` |
| `AVDesyncPlayoutDetector` | `av-desync-playout-detector` | `av-desync` | Synchronization | `avDesyncPlayoutDetector` |
| `PixelatedVideoDetector` | `pixelated-video-detector` | `pixelated-video` | Visual — clarity | `pixelatedVideoDetector` |
| `InboundVideoFlowStateDetector` | `inbound-video-flow-state-detector` | `video-flow-disrupted` | Visual — continuity | `inboundVideoFlowStateDetector` |

### Category 5 — Telemetry

**8 classes, 0 issue types.** [Full reference →](../detectors-telemetry/)

| Class | `name` | Emits | Sub-layer | Config key |
|---|---|---|---|---|
| `CaptureTrackMutedDetector` | `capture-track-muted-detector` | `capture-track-muted` | Lifecycle | `captureTrackMutedDetector` |
| `StatsGapDetector` | `stats-gap-detector` | `stats-collection-gap` | Lifecycle | `statsGapDetector` |
| `CodecChangeDetector` | `codec-change-detector` | `codec-changed` | Media | `codecChangeDetector` |
| `SimulcastLayerDetector` | `simulcast-layer-detector` | `simulcast-layer-changed` | Media | `simulcastLayerDetector` |
| `VideoResolutionChangeDetector` | `video-resolution-change-detector` | `video-resolution-changed` | Media | `videoResolutionChangeDetector` |
| `IceRestartDetector` | `ice-restart-detector` | `ice-restart` | Transport | `iceRestartDetector` |
| `IceRestartRecommendationDetector` | `ice-restart-recommendation-detector` | `ice-restart-recommended` | Transport | `iceRestartRecommendationDetector` |
| `IceTraversalDetector` | `ice-traversal-detector` | `ice-tuple-changed` | Transport | `iceTraversalDetector` |

## Controlling detectors at runtime

Every layer's registry — `monitor.detectors`, `pcMonitor.detectors`, `inboundTrackMonitor.detectors`,
`outboundTrackMonitor.detectors`, `mediaPlayoutMonitor.detectors` — offers:

```typescript
// Inspection
detectors.size;
detectors.listOfNames;
detectors.has(name);
detectors.getByName<CpuPerformanceDetector>('cpu-performance-detector');
detectors.find(pred);  detectors.filter(pred);
for (const d of detectors) { /* … */ }

// Mutation
detectors.add(detector);  detectors.remove(detector);  detectors.clear();

// Runtime toggle
detectors.disable(name);  detectors.enable(name);  detectors.isEnabled(name);
detectors.disableAll();   detectors.enableAll();
```

Issue-raising detectors also expose `includeIssueInSample = true` — set it to `false` to keep a
detector running locally (events, `activeIssues`) while excluding its issues from the samples
shipped to the server.

## Writing your own

A custom detector implements `Detector`: a `name`, a public `disabled` flag, and an `update()`
called once per collection.

```typescript
import { Detector, ClientMonitor, InboundTrackMonitor } from '@observertc/client-monitor-js';

class UnexpectedMicMuteDetector implements Detector {
    public readonly name = 'unexpected-mic-mute-detector';
    public disabled = false;

    private readonly issueKey: string;

    constructor(
        private readonly track: InboundTrackMonitor,
        private readonly participantId: string,
        private readonly clientMonitor: ClientMonitor,
    ) {
        this.issueKey = `unexpected-mic-mute-track-${track.track.id}`;
    }

    update() {
        if (this.disabled) return;

        const wantsAudio = !this.track.track.muted;
        const receiving = (this.track.getInboundRtp()?.deltaBytesReceived ?? 0) > 0;
        const misbehaving = wantsAudio && !receiving;

        if (misbehaving && !this.clientMonitor.isIssueActive(this.issueKey)) {
            this.clientMonitor.raiseIssue(this.issueKey, {
                type: 'unexpected-mic-mute',
                payload: { participantId: this.participantId },
            });
        } else if (!misbehaving && this.clientMonitor.isIssueActive(this.issueKey)) {
            this.clientMonitor.resolveIssue(this.issueKey, { comment: 'mic unmuted' });
        }
    }
}

inboundTrackMonitor.detectors.add(
    new UnexpectedMicMuteDetector(inboundTrackMonitor, participantId, monitor),
);
```

Follow the five rules above and your detector behaves like a built-in one: age durations on the
monitor's `deltaTime`, read facts off the monitor rather than re-deriving them, and never consult
another detector's verdict.
