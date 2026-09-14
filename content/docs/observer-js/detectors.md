---
title: "Detectors"
description: "The ten built-ins, the issue registry, conclusions, and writing your own"
lead: "Every one of them correlates across the clients of a call or the calls of a fleet — because that is the only thing a server can do better than a browser"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 340
toc: true
---

`observer-js` ships **ten detectors**, each an opt-in extension you register explicitly. None are
created automatically.

{{< callout context="tip" title="The organising principle" icon="rocket" >}}
**If a condition is detectable on the client, the client's issue is the source of truth.**

`client-monitor-js` already decides *what is wrong with an endpoint*, with hysteresis and
multi-signal confirmation behind each verdict. `observer-js` never re-derives those verdicts from
raw counters. It answers the questions no browser can: *who else is in this state right now, what do
they have in common, and where in publisher → SFU → subscriber does the fault begin?*
{{< /callout >}}

## The division of labour

The most important thing to understand about detection in this library is **what it deliberately
does not do**. A client's verdicts are better than anything re-derived server-side, because they
carry hysteresis and multi-signal confirmation:

- `invented-speech` subtracts silent concealment — raw `concealedSamples` rises during ordinary
  silence, so a naive server-side detector would flag every quiet moment;
- `audio-jitter-buffer-stress` requires the buffer to be grown **and** NetEQ to be time-stretching —
  a grown buffer alone means NetEQ is *succeeding*;
- `ice-disconnected` only fires once `disconnected` has persisted, so the blips ICE heals on its own
  never surface.

### There is no ICE detector

ICE trouble is reported by the client as the keyed issues `ice-disconnected`,
`ice-connection-failed`, `ice-transport-stalled` and `unstable-ice-path`. An `IceDisruptionDetector`
used to re-derive that server-side from raw state transitions; it has been removed, because **the
server sees less and guesses more**. The client knows whether `disconnected` persisted or healed in
200 ms; the observer does not.

Correlating ICE trouble is now configuration, not a class:

```typescript
observer.addObserverDetector('observer-concurrent-issue-detector', {
    issueTypes: ['ice-disconnected', 'ice-connection-failed', 'ice-transport-stalled'],
});
```

## Registering them

**Nothing is created implicitly.** A `new Observer()` has zero detectors and there is no detector
configuration in `ObserverConfig` — an application says what it wants to watch, or it watches
nothing.

```typescript
const observer = new Observer({
    createRemoteTrackResolver: createDefaultMediasoupRemoteTrackResolverFactory(),
});

// observer-scoped (cross-call) — built immediately onto `observer.detectors`
observer.addObserverDetector('observer-concurrent-issue-detector', {
    issueTypes: ['congestion', 'ice-disconnected', 'ice-connection-failed'],
    minAffectedCalls: 3,
});
observer.addObserverDetector('turn-server-outage-detector', { minClientsAtPeak: 10 });

// call-scoped — recorded in `observer.callDetectorConfigs`, applied to every call created AFTER this
observer.addCallDetector('call-concurrent-issue-detector', {
    issueTypes: ['congestion', 'ice-disconnected'],
});

// one specific call
observedCall.addDetector('issue-fan-out-detector', { issueTypes: ['video-flow-disrupted'] });
```

Every `add*` is **chainable** — it returns the owning entity:

```typescript
observer
    .addObserverDetector('turn-server-health-detector')
    .addObserverDetector('turn-server-outage-detector', { minClientsAtPeak: 10 })
    .addValidator('remote-track-resolver');
```

Detectors are named by their kebab-case `NAME`, and **the name types the config** — an unknown name,
or a key that belongs to a different detector, will not compile. Each detector owns its defaults in
its own constructor, beside the doc explaining what each threshold means.

> **Why no defaults?** A detector nobody asked for is a detector nobody will act on. It costs time
> on every tick and raises findings into a handler that was not written to expect them. Earlier
> versions auto-created everything from a three-state config slot; the result was applications
> receiving finding types they had never heard of.

### Removing them

By **name**, on the entity — which removes *every* instance under that name:

```typescript
observer.removeObserverDetector('turn-server-outage-detector');   // → 1
observer.removeCallDetector('call-concurrent-issue-detector');    // stops it everywhere
observedCall.removeDetector('issue-fan-out-detector');            // this call only
```

By **instance**, through the registry — which is where instances live, since `add*` returns the
entity:

```typescript
observer
    .addObserverDetector('client-population-issue-detector', { issueTypes: ['cpulimitation'], groupBy: 'browser' })
    .addObserverDetector('client-population-issue-detector', { issueTypes: ['cpulimitation'], groupBy: 'operationSystem' });

const [byBrowser, byOs] = observer.detectors.getAll('client-population-issue-detector');

observer.detectors.remove(byOs);   // keeps the browser axis running
```

`Detectors` is a small collection: `instances` (a copy, in registration order), `listOfNames`,
`size`, `get(name)`, `getAll(name)`, `has(name)`, `add(detector)`, `remove(detector)`,
`removeByName(name)`, `clear()`, and it is iterable.

Two things worth knowing:

- **By name removes every instance under it**, not the first. A name can legitimately be registered
  more than once — `ClientPopulationIssueDetector` is meant to be added once per `groupBy` axis.
- **`removeCallDetector` affects calls already open, by default.** Otherwise whether a detector runs
  would depend on when a call happened to join, which is not a state anyone can reason about. Pass
  `{ includeOpenCalls: false }` to change only what future calls are built with.

Every removal path calls the detector's `close()`, so it unsubscribes from the issue registry and
drops any timers or bus listeners. **A detector removed without closing would keep being fed
matching issues for the life of the call** — invisible, unbounded, and it would still look healthy
if you inspected it.

## Issues are pushed, not polled

A detector does not go looking for the issues it cares about. It implements `ActiveIssueTracker` and
registers for the types it consumes; the registry hands them over as they open and close.

```typescript
observedCall.activeIssuesRegistry;   // this meeting
observer.activeIssuesRegistry;       // the fleet; every call's registry propagates into it

observer.activeIssuesRegistry.addIssueTracker('congestion', myDetector);
observer.activeIssuesRegistry.removeIssueTracker(myDetector);

registry.values();   // the open issues in this scope, oldest first
registry.size;
```

The cost of a detector is then proportional to the issues it actually receives, not to the number of
participants: **a healthy 500-client fleet does no per-tick work at all**, because nothing was
pushed.

{{< callout context="caution" title="There is no wildcard" icon="alert-triangle" >}}
A tracker names its types and sees nothing else. "Feed me everything and I'll work out what matters"
moves the decision from the application — which knows its client build and its issue vocabulary —
onto a detector that has to guess, and it makes the cost of a subscription unbounded and invisible.
If a detector should watch five types, list five types.
{{< /callout >}}

Onset spread is measured on the **observer clock**, never the client's. `raisedAt` comes from each
participant's own machine, and comparing those across clients makes clock skew look like a
synchronized infrastructure event.

## The built-in detectors

**🔗 marks detectors that require a [`RemoteTrackResolver`](../sfu/).** They reason about a published
track and its subscribers, so without the publisher↔subscriber links they see nothing and stay
**silent forever** — which looks exactly like "no problems found". Configure
`ObserverConfig.createRemoteTrackResolver`, and start the
[`remote-track-resolver` validator](../validators/) to prove it is wired.

| Detector | 🔗 | Scope | Raises |
|---|:--:|---|---|
| `CallConcurrentIssueDetector` | | call | `CONCURRENT_CLIENT_ISSUES`, `ISSUE_ONSET_BURST` |
| `ObserverConcurrentIssueDetector` | | **observer** | `CROSS_CALL_CONCURRENT_ISSUES`, `CROSS_CALL_ISSUE_ONSET_BURST` |
| `IssueFanOutDetector` | 🔗 | call | `PUBLISHED_TRACK_ISSUE_FAN_OUT`, `SINGLE_RECEIVER_ISSUE` |
| `PublisherFaultCorroborationDetector` | 🔗 | call | `CORROBORATED_PUBLISHER_FAULT` |
| `TrackDeliveryMismatchDetector` | 🔗 | call | `PUBLISHED_TRACK_NOT_DELIVERED`, `RECEIVER_TRACK_NOT_DELIVERED`, `PUBLISHER_TRACK_DRY` |
| `UnconsumedTrackDetector` | 🔗 | call | `UNCONSUMED_PUBLISHED_TRACK` |
| `ClientPopulationIssueDetector` | | **observer** | `CLIENT_POPULATION_ISSUE` |
| `SfuCongestionDetector` | | **observer** | `sfu-congestion` |
| `TurnServerHealthDetector` | | **observer** | `TURN_SERVER_DEGRADED` |
| `TurnServerOutageDetector` | | **observer** | `TURN_SERVER_OUTAGE` |

### What each adds that no endpoint can know

**`CallConcurrentIssueDetector`** — *who else in this meeting is in this state right now?* The
difference between "one person's Wi-Fi" and "this room is broken".

**`ObserverConcurrentIssueDetector`** — *is our infrastructure in trouble?* A **separate class**, not
the call one with a bigger denominator, because it is a different question with different gates. It
requires the group to span at least `minAffectedCalls` **independent calls** (default `2`) and
raises its own `CROSS_CALL_*` types. Without that gate, one thirty-person meeting where everyone is
congested clears every client threshold and pages you for a single bad room the call-scoped detector
already reported. Note there is deliberately **no participant ratio** at this scope: six broken
calls out of forty is a small share of all clients, and a ratio gate would hide exactly the event
you want.

**`IssueFanOutDetector`** — *does this issue follow one published source, or one receiver?*

**`PublisherFaultCorroborationDetector`** — *do **both ends** of one track agree the source is at
fault?* Fan-out sees one end and infers; this sees the publisher reporting `encoder-bottleneck`
about its own send path *while* its subscribers report `video-flow-disrupted` about receiving it. Two
independent parties, one conclusion, nothing left to deduce — hence the highest confidence in the
library. Run both: fan-out is broader and catches the case where the publisher is fine and the SFU's
forwarding is not.

**`ClientPopulationIssueDetector`** — *is this concentrated on one **kind of client**?* The one
correlation here that is neither per-call nor per-server. Every other observer-scoped detector
reasons "clients in unrelated calls share only the infrastructure, so it must be us" — right for
network symptoms, **wrong for endpoint ones**. `cpulimitation` across six unrelated calls is not an
SFU event; CPU is owned by the endpoint, so what those endpoints share is a browser version or a
client release. Groups by `browser` / `engine` / `platform` / `operationSystem` / `location`, one
axis per instance. **The gate is relative risk, not share**: "30% of Chrome 141 is unhappy" means
nothing if 30% of everyone is, and a share-based rule simply indicts whichever browser is most
popular.

**`SfuCongestionDetector`** — *is congestion spiking across the fleet right now?* Counts distinct
clients reporting congestion in **fixed wall-clock buckets** and compares each bucket against a
median+MAD baseline of the ones before it. Buckets rather than update ticks on purpose: the tick is
unevenly spaced and shorter than a client's sampling period, so counting on it compares windows of
different lengths and calls the difference a signal. Only add it when the observer's calls all come
from the **same SFU**.

**`TrackDeliveryMismatchDetector`** — *are the two ends of a track disagreeing?*

**`UnconsumedTrackDetector`** — *is anyone actually subscribed?* It reads the resolver's silence.

**`TurnServerHealthDetector`** — *does trouble cluster on one relay?*

**`TurnServerOutageDetector`** — covers the case the health detector structurally cannot. The health
detector groups clients by the server relaying them and asks how many report issues — it needs
clients *on* the server to ask. When a TURN server dies, allocation fails: existing sessions drop and
new clients never obtain a relay candidate through it, so they are never attributed to it at all.
**Degradation makes clients unhappy; an outage makes them disappear.** Absence is a dangerous signal,
so the **control group** is the heart of the design: a call ending, everyone leaving at 6pm, and a
fleet-wide network event all look identical to an outage. It refuses to blame a server unless
clients *not* relayed through it are demonstrably still connected (`requireControlGroup`, on by
default).

### Publisher → subscribers: the resolver links

The question a single browser can never answer is *"did **everyone** receiving Alice see the same
degradation?"*. The join is the publisher↔subscriber links maintained by a
[`RemoteTrackResolver`](../sfu/), and detectors walk them directly:

```typescript
outboundTrack.remoteInboundTracks;      // Set<ObservedInboundTrack> — every subscriber of this source
inboundTrack.remoteOutboundTrack;       // the publisher, or undefined if unlinked
inboundTrack.getInboundRtp();           // that receiver's RTP stats
observedCall.unconsumedOutboundTracks;  // published tracks with no subscriber at all
```

### `TrackDeliveryMismatchDetector` — resolving an ambiguous symptom

A dry track ("no bytes are arriving") is the clearest symptom there is and, on its own, completely
ambiguous. A receiver seeing silence cannot distinguish *the camera was switched off* from *the SFU
stopped forwarding* from *my own consumer wedged*.

Joining the two ends of the published track resolves it:

| Publisher | Subscribers | Verdict |
|---|---|---|
| sending | **all** dry | `PUBLISHED_TRACK_NOT_DELIVERED` — the forwarding path |
| sending | **some** dry | `RECEIVER_TRACK_NOT_DELIVERED` — those consumers (in mediasoup: recreate them) |
| dry | any dry | `PUBLISHER_TRACK_DRY` — the source stopped; **not** an SFU fault |

The publisher side is judged from both available signals: its own `dry-outbound-track` issue when the
client reports one, and the observed outbound RTP (`deltaPacketsSent`) as fallback and
corroboration. That combination is what makes the first row trustworthy — the server can state that
packets demonstrably left the publisher during the same interval in which every receiver got
nothing. This check needs **no mediasoup instrumentation at all**.

### `UnconsumedTrackDetector` — reading the resolver's silence

The one detector where the *absence* of links is the signal: a track still pushing packets whose
`remoteInboundTracks` set is empty — uplink and SFU ingress spent on media nobody receives. It waits
`minUnconsumedDurationInMs` first, since a gap between publishing and the first subscription is
normal at join time.

Note the trap it has to guard against, and why it checks `call.remoteTrackResolver` at runtime rather
than trusting a flag: **"no subscribers" and "no resolver configured" produce the identical
observation.** Without a resolver it would report every published track in the call as unconsumed.

## Grouping by place: the `location` axis

If your clients report coordinates, `ClientPopulationIssueDetector` can group by **where they are**
instead of what they run — which is the grouping network symptoms actually cluster by:

```typescript
observer.addObserverDetector('client-population-issue-detector', {
    issueTypes: ['congestion', 'ice-disconnected'],
    groupBy: 'location',
    locationPrecision: 3,   // geohash chars: 3 ≈ 156 km, 4 ≈ 39 km, 5 ≈ 5 km
    resolveClientLocation: (client) => client.attachments?.geo as { latitude: number; longitude: number },
});
```

**The client still owns "RTT jumped".** Absolute RTT is not comparable between clients — someone
200 ms away is *always* 200 ms away — so the only signal is deviation from that client's own
baseline, which is exactly what the client measures. The observer's contribution is the part no
endpoint can see: that many of the affected clients are **in the same place at the same time**.

Three things to know:

- **Cells, not radii.** The population is a geohash prefix. "Within N km" is a clustering problem —
  order-dependent, no stable group name, pairwise cost — and a detector needs the *same* group key
  on every tick for its cooldown and control group to mean anything. The cost is that a cell
  boundary can split two adjacent clients, which biases towards missing a finding rather than
  inventing one.
- **Only the cell key is reported.** `payload.population` is the geohash; coordinates never enter the
  issue. These payloads get archived into [call summaries](../call-summaries/), so that matters.
- **Geography is confounded with your topology.** The control group is "everyone outside this cell",
  which cannot separate *"the path into this region degraded"* from *"the SFU serving this region
  degraded"*. So the finding concludes `infrastructure` and points at `SfuCongestionDetector` /
  `TurnServerHealthDetector` rather than claiming an attribution it cannot support.

Coordinates are not in `ClientSample`, so `resolveClientLocation` is **required**; without it the
detector warns at construction and finds nothing, rather than quietly reporting no findings forever.

## `CallIssue` vs `ObserverIssue`

| | Raised by | Delivered as | `scope` |
|---|---|---|---|
| `CallIssue` | `observedCall.addIssue(…)` | `call-issue` | `'call'` |
| `ObserverIssue` | `observer.addIssue(…)` | `observer-issue` | `'observer'` |

Both share `IssueBase` — `type`, `timestamp`, `conclusion?`, `payload?` — and `Issue` is the union,
discriminated on `scope`.

```typescript
observer.on('call-issue', ({ observedCall, issue }) => {
    issue.scope;                    // 'call'
    observedCall.callId;            // the call — NOT repeated in the payload
    issue.conclusion?.faultDomain;
    issue.payload;                  // evidence only — no JSON.parse
});
```

`scope` is stamped by `addIssue` rather than asked of the detector: it is a fact about *where the
finding was raised*, which the entity knows and a detector should not have to restate.

**The payload is evidence and nothing else.** It no longer repeats `type`, `scope`, or the `callId`
already carried by the event, and `conclusion` was lifted out of it to a first-class field. A payload
that restates its own envelope invites the two to disagree — and they did, because nothing kept them
in step. `payload` is always an object; use `issuePayloadAsString(issue)` at a boundary that
genuinely needs text.

## Conclusions

Every issue-driven finding carries a `conclusion` — the interpretation step, so the person reading
the alert does not have to perform it. It sits **beside** the evidence, not inside it:

```jsonc
{
  "type": "CROSS_CALL_ISSUE_ONSET_BURST",
  "scope": "observer",
  "timestamp": 1739812345678,
  "conclusion": {
    "faultDomain": "infrastructure",
    "summary": "network congestion is open across independent calls at the same time — 6 of 40 calls (11/300 clients)",
    "recommendation": "check SFU egress bandwidth and host network saturation before looking at any single participant",
    "confidence": 0.85
  },
  "payload": {
    "issueType": "congestion",
    "calls": 40, "affectedCalls": 6,
    "perCall": [ { "callId": "…", "affectedClients": 4, "totalClients": 9 } ]
  }
}
```

`faultDomain` is one of `infrastructure`, `call`, `published-track`, `endpoint`,
`client-population` or `unknown`, and **it comes from the spread, not the issue type** — congestion
in one call is a meeting problem, congestion in six calls is a server problem, and the client
reported the identical symptom in both.

{{< callout context="note" title="One case inverts the usual reading" icon="info-circle" >}}
**`cpulimitation` spread across many independent calls concludes `client-population`, not
`infrastructure`.** Endpoint CPU is owned by the endpoint, so breadth there points at what those
endpoints share — a recent client release, a browser version, shared VDI hardware — and paging the
SFU on-call would be wrong. The conclusion table encodes that so nobody has to rediscover it during
an incident.
{{< /callout >}}

Unknown issue types (your own custom client detectors) still produce a structurally valid conclusion
from the spread alone; they just get generic wording.

Two functions are exported, one per scope: `concludeCallIssue()` and `concludeObserverIssue()`. They
are separate because a detector already knows its scope, and a single generic function forced every
caller to pass the other scope's fields as placeholders.

## Cost

Detectors run inside `call.update()`, on your event loop. Two things keep their cost off the
participant axis:

- **Issues are pushed, not polled.** An `update()` that finds `size === 0` — the overwhelmingly
  common case — costs one comparison, whatever the participant count.
- **So are unconsumed tracks.** `observedCall.unconsumedOutboundTracks` is maintained by the
  resolver as tracks gain and lose subscribers, so `UnconsumedTrackDetector` reads a set that is
  normally empty instead of walking every published track (529 µs → 65 µs per tick at 1,200 tracks).
- **Track lookups start from the affected minority.** A detector resolving an issue to its published
  track searches the *reporting client's* peer connections (typically one or two), not the call.

At 20 calls × 12 participants (2,640 subscriptions) the whole detector pass costs ~1.3 ms per tick.

## Writing your own

```typescript
import { Observer, Detector } from '@observertc/observer-js';

class MyCrossClientDetector implements Detector {
    readonly name = 'my-detector';

    constructor(private readonly call: ObservedCall) {}

    update() {                                   // called on every call.update()
        // …inspect this.call.observedClients across participants…
        if (/* a condition only visible server-side */ false) {
            this.call.addIssue({
                type: this.name,
                payload: { /* evidence */ },
                timestamp: Date.now(),
            });
            // → emitted on the bus as 'call-issue'
        }
    }
}

const observer = new Observer();
observer.on('call-added', ({ observedCall }) => {
    observedCall.detectors.add(new MyCrossClientDetector(observedCall));
});
observer.on('call-issue', ({ observedCall, issue }) => { /* react */ });
```

An observer-scoped detector is the same shape, added to `observer.detectors` and raising through
`observer.addIssue(…)`:

```typescript
observer.detectors.add({
    name: 'sfu-wide-degradation',
    update: () => {
        const degraded = [...observer.observedCalls.values()].filter(isDegraded);

        if (observer.numberOfCalls > 3 && degraded.length / observer.numberOfCalls > 0.6) {
            observer.addIssue({ type: 'SFU_WIDE_QUALITY_DEGRADATION', timestamp: Date.now() });
        }
    },
});
```

**Do not re-implement client-detectable signals.** If the condition can be seen in the browser, it
belongs in a `client-monitor-js` detector, where the evidence is better.
