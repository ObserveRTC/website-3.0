---
title: "Detectors"
slug: "detectors"
description: "Cross-participant and cross-call detection in observer-js"
lead: "Ten built-in detectors that answer the questions no single browser can, plus the registry for running your own"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 324
toc: true
---

## The division of labour

The most important thing to understand about detection in `observer-js` is **what it deliberately
does not do**.

A client running [`client-monitor-js`](/docs/libraries/client-monitor-js/detectors/) already ships
detectors that decide *what is wrong with that endpoint* — `congestion`, `cpulimitation`,
`audio-concealment`, `freezed-video-track`, `keyframe-storm`, `video-decoder-overloaded`,
`stuck-decoder`, `ice-disconnected` and more. Those verdicts are better than anything re-derived
server-side, because they carry hysteresis and multi-signal confirmation:

- `audio-concealment` subtracts silent concealment — raw `concealedSamples` rises during ordinary
  silence, so a naive detector flags every quiet moment.
- `audio-jitter-buffer-stress` requires the buffer to be grown **and** NetEQ to be time-stretching;
  a grown buffer alone means NetEQ is *succeeding*.
- `ice-disconnected` only fires once `disconnected` has persisted, so the blips ICE heals on its
  own never surface.

{{< callout context="tip" title="The rule the whole design hangs on" icon="rocket" >}}
**If a condition is detectable on the client, the client's issue is the source of truth.**

`observer-js` adds only the cross-participant conclusion: *who else is in this state right now,
what do they have in common, and where in publisher → SFU → subscriber does the fault begin?*
{{< /callout >}}

## Nothing is created implicitly

A `new Observer()` has **zero detectors**. There is no detector configuration in `ObserverConfig`
and no default set.

{{< callout context="note" title="Why no defaults?" icon="info-circle" >}}
A detector nobody asked for is a detector nobody will act on. It costs time on every tick and
raises findings into a handler that was not written to expect them. Earlier versions auto-created
everything from a three-state config slot; the result was applications receiving finding types they
had never heard of.
{{< /callout >}}

## The wire format for client issues

From `client-monitor-js` **4.6.0** the whole issue lifecycle reaches the server. A stateful issue
arrives as two `clientIssues[]` entries sharing a `key`:

```text
raise:       { type: 'stuck-decoder',          key, payload,                                timestamp: raisedAt  }
resolution:  { type: 'stuck-decoder-resolved', key, payload: { raisedAt, comment, …final }, timestamp: resolvedAt }
```

The observer opens an entry in `observedClient.activeIssues` on the raise and closes it on the
matching key, emitting `client-issue-resolved` with the finished interval. Handled for you:

- the `-resolved` **suffix is stripped**, so both entries share one logical `type`;
- a **re-raise** of a live key refreshes the payload without restarting `raisedAt`;
- **keyless** entries are one-shot — reported via `client-issue`, never tracked;
- issues still open when a client closes are **force-resolved** (`resolvedBy: 'client-closed'`), and
  the registry expires stale entries, so a crashed participant cannot leave an issue open forever.

```typescript
observer.on("client-issue", ({ observedClient, issue }) => { /* opened, or one-shot */ });

observer.on("client-issue-resolved", ({ resolvedIssue }) => {
    resolvedIssue.type;          // 'stuck-decoder' — suffix stripped
    resolvedIssue.durationInMs;  // how long the episode lasted
    resolvedIssue.resolvedBy;    // 'client' | 'timeout' | 'client-closed'
});
```

{{< callout context="caution" title="client-monitor-js ≥ 4.6.0 is required" icon="alert-triangle" >}}
Every issue-driven detector depends on this format. There is no fallback that infers these
conditions from raw counters — the client decides better, and maintaining a worse second
implementation to be polite to old clients is how both end up wrong.
{{< /callout >}}

### Why intervals beat time windows

*"Several clients reported congestion in the last 10 seconds"* is a heuristic that has to guess
whether the symptoms are still happening. *"Several clients are congested **right now,
simultaneously**"* is ground truth, because the client says when the episode ends. Overlapping
intervals are far stronger evidence of a shared cause than near-in-time reports.

## `ActiveIssuesRegistry` — issues are pushed, not polled

A detector does not go looking for the issues it cares about. It implements `ActiveIssueTracker`
and registers for the types it consumes; the registry hands them over as they open and close.

```typescript
observedCall.activeIssuesRegistry;   // this meeting
observer.activeIssuesRegistry;       // the fleet; every call's registry propagates into it

observer.activeIssuesRegistry.addIssueTracker("congestion", myDetector);
observer.activeIssuesRegistry.removeIssueTracker(myDetector);

registry.values();   // open issues in this scope, oldest first
registry.size;
```

The cost of a detector is therefore proportional to the issues it actually receives, not to the
number of participants: a healthy 500-client fleet does no per-tick work at all, because nothing
was pushed.

{{< callout context="caution" title="There is no wildcard" icon="alert-triangle" >}}
A tracker names its types and sees nothing else. *"Feed me everything and I'll work out what
matters"* moves the decision from the application — which knows its client build and its issue
vocabulary — onto a detector that has to guess, and it makes the cost of a subscription unbounded
and invisible. If a detector should watch five types, list five types.
{{< /callout >}}

Onset spread is measured on the **observer clock**, never the client's. `raisedAt` comes from each
participant's own machine, and comparing those across clients makes clock skew look like a
synchronized infrastructure event.

## Registering detectors

```typescript
const observer = new Observer({
    createRemoteTrackResolver: createDefaultMediasoupRemoteTrackResolverFactory(),
});

// Observer-scoped (cross-call) — built immediately onto observer.detectors.
observer.addObserverDetector("observer-concurrent-issue-detector", {
    issueTypes: ["congestion", "ice-disconnected", "ice-connection-failed"],
    minAffectedCalls: 3,
});
observer.addObserverDetector("turn-server-outage-detector", { minClientsAtPeak: 10 });

// Call-scoped — recorded in observer.callDetectorConfigs, applied to every call created AFTER this.
observer.addCallDetector("call-concurrent-issue-detector", {
    issueTypes: ["congestion", "ice-disconnected"],
});

// One specific call.
observedCall.addDetector("issue-fan-out-detector", { issueTypes: ["freezed-video-track"] });
```

Every `add*` is **chainable**:

```typescript
observer
    .addObserverDetector("turn-server-health-detector")
    .addObserverDetector("turn-server-outage-detector", { minClientsAtPeak: 10 })
    .addValidator("remote-track-resolver");
```

Detectors are named by their kebab-case `NAME`, and **the name types the config** — an unknown name
or a key belonging to a different detector will not compile. Each detector owns its defaults in its
own constructor, beside the documentation for what each threshold means.

Issue-driven detectors that subscribe to an open-ended set of types take an explicit, non-empty
`issueTypes` (or `publisherIssueTypes` / `receiverIssueTypes`) — there is no "watch everything"
option. Detectors whose types are structural rather than a matter of taste name them individually
instead, with defaults: `TrackDeliveryMismatchDetector` takes `dryInboundIssueType` and
`dryOutboundIssueType`, defaulting to `'dry-inbound-track'` and `'dry-outbound-track'`.

Every threshold has a documented default. A few worth knowing:

| Detector | Notable defaults |
|---|---|
| `CallConcurrentIssueDetector` | `minClients: 3`, `minAffectedClients: 3`, `affectedRatioThreshold: 0.5`, `onsetBurstWindowInMs: 2000`, `cooldownMs: 60000` |
| `ObserverConcurrentIssueDetector` | `minAffectedCalls: 2` |
| `IssueFanOutDetector` | `minReceivers: 3`, `affectedRatioThreshold: 0.6`, `reportSingleReceiver: true` |
| `TrackDeliveryMismatchDetector` | `minReceivers: 2`, `allReceiversRatio: 1` |
| `UnconsumedTrackDetector` | `minUnconsumedDurationInMs: 30000`, `minBitrate: 50000` |
| `TurnServerOutageDetector` | `minClientsAtPeak: 5`, `lossRatioThreshold: 0.8`, `peakWindowMs: 120000`, `requireControlGroup: true`, `consecutiveTicks: 2`, `cooldownMs: 300000` |

### Removing them

By **name**, on the entity — which removes *every* instance under that name:

```typescript
observer.removeObserverDetector("turn-server-outage-detector");   // → 1
observer.removeCallDetector("call-concurrent-issue-detector");    // stops it everywhere
observedCall.removeDetector("issue-fan-out-detector");            // this call only
```

By **instance**, through the registry:

```typescript
observer
    .addObserverDetector("client-population-issue-detector", { issueTypes: ["cpulimitation"], groupBy: "browser" })
    .addObserverDetector("client-population-issue-detector", { issueTypes: ["cpulimitation"], groupBy: "operationSystem" });

const [byBrowser, byOs] = observer.detectors.getAll("client-population-issue-detector");

observer.detectors.remove(byOs);   // keeps the browser axis running
```

Two things worth knowing:

- **By name removes every instance under it**, not the first. A name can legitimately be registered
  more than once — `ClientPopulationIssueDetector` is meant to be added once per `groupBy` axis.
- **`removeCallDetector` affects open calls by default.** Otherwise whether a detector runs would
  depend on when a call happened to join. Pass `{ includeOpenCalls: false }` to change only future
  calls.

Every removal path calls the detector's `close()`, so it unsubscribes from the issue registry and
drops timers and bus listeners.

### The `Detectors` collection

```typescript
detectors.instances;          // a copy, in registration order
detectors.listOfNames;
detectors.size;
detectors.get(name);
detectors.getAll(name);
detectors.has(name);
detectors.add(detector);
detectors.remove(detector);
detectors.removeByName(name);
detectors.clear();
for (const detector of call.detectors) { /* … */ }
```

`instances` being a copy is deliberate: removing while iterating the live array would skip entries.

## The ten built-in detectors

🔗 marks detectors that require a [`RemoteTrackResolver`](../sfu/).

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

{{< callout context="caution" title="🔗 detectors are silent without a resolver" icon="alert-triangle" >}}
They reason about a published track and its subscribers. Without the publisher ↔ subscriber links
they see nothing and stay **silent forever** — which looks exactly like "no problems found".
Configure `ObserverConfig.createRemoteTrackResolver`, and run the
[`remote-track-resolver` validator](../validators/) to prove it is wired.
{{< /callout >}}

### What each one adds

**`CallConcurrentIssueDetector`** — *who else in this meeting is in this state right now?* The
difference between "one person's Wi-Fi" and "this room is broken". Gates on the participant ratio.

**`ObserverConcurrentIssueDetector`** — *is our infrastructure in trouble?* A separate class, not
the call one with a bigger denominator, because it is a different question with different gates. It
requires the group to span at least `minAffectedCalls` **independent calls** (default `2`) and
raises its own `CROSS_CALL_*` types. Without that gate, one thirty-person meeting where everyone is
congested clears every client threshold and pages you for a single bad room the call-scoped
detector already reported. There is deliberately **no participant ratio** at this scope: six broken
calls out of forty is a small share of all clients, and a ratio gate would hide exactly the event
you want.

**`IssueFanOutDetector`** — *does this issue follow one published source, or one receiver?*

**`PublisherFaultCorroborationDetector`** — *do **both ends** of one track agree the source is at
fault?* Fan-out sees one end and infers; this sees the publisher reporting `encoder-bottleneck`
about its own send path *while* its subscribers report `freezed-video-track` about receiving it.
Two independent parties, one conclusion — hence the highest confidence in the library. Run both:
fan-out is broader and catches the case where the publisher is fine and the SFU's forwarding is not.

**`ClientPopulationIssueDetector`** — *is this concentrated on one **kind of client**?* The one
correlation that is neither per-call nor per-server. Every other observer-scoped detector reasons
"clients in unrelated calls share only the infrastructure, so it must be us" — right for network
symptoms, **wrong for endpoint ones**. `cpulimitation` across six unrelated calls is not an SFU
event; CPU is owned by the endpoint, so what those endpoints share is a browser version or a client
release. Groups by `browser` / `engine` / `platform` / `operationSystem`, one axis per instance.
The gate is **relative risk**, not share: "30 % of Chrome 141 is unhappy" means nothing if 30 % of
everyone is, and a share-based rule simply indicts whichever browser is most popular.

**`SfuCongestionDetector`** — *is congestion spiking across the fleet right now?* Counts distinct
clients reporting congestion in fixed wall-clock buckets and compares each bucket against a
median + MAD baseline of the ones before it. Buckets rather than update ticks on purpose: the tick
is unevenly spaced and shorter than a client's sampling period, so counting on it compares windows
of different lengths and calls the difference a signal. Only add it when the observer's calls all
come from the **same SFU**.

**`TrackDeliveryMismatchDetector`** — *are the two ends of a track disagreeing?* See
[below](#trackdeliverymismatchdetector-in-detail).

**`UnconsumedTrackDetector`** — *is anyone actually subscribed?* A track still pushing packets
whose `remoteInboundTracks` set is empty — uplink and SFU ingress spent on media nobody receives.
It waits `minUnconsumedDurationInMs` first, since a gap between publishing and the first
subscription is normal at join time. It checks `call.remoteTrackResolver` at runtime, because "no
subscribers" and "no resolver configured" produce the identical observation.

**`TurnServerHealthDetector`** — *does trouble cluster on one relay?*

**`TurnServerOutageDetector`** — covers the case the health detector structurally cannot. The
health detector groups clients by the server relaying them and asks how many report issues — it
needs clients *on* the server to ask. When a TURN server dies, allocation fails: existing sessions
drop and new clients never obtain a relay candidate through it, so they are never attributed to it
at all. Its population goes to zero and the health detector falls silent for the worst possible
reason.

{{< callout context="tip" title="Degradation makes clients unhappy; an outage makes them disappear" icon="rocket" >}}
Absence is a dangerous signal, so the **control group** is the heart of `TurnServerOutageDetector`:
a call ending, everyone leaving at 6 pm, and a fleet-wide network event all look identical to an
outage. It refuses to blame a server unless clients *not* relayed through it are demonstrably still
connected (`requireControlGroup`, on by default).
{{< /callout >}}

### There is no ICE detector

ICE trouble is reported by `client-monitor-js` ≥ 4.6.0 as the keyed issues `ice-disconnected`,
`ice-connection-failed`, `ice-transport-stalled` and `unstable-ice-path`, each with hysteresis and
multi-signal confirmation behind it. An `IceDisruptionDetector` used to re-derive that server-side
from raw state transitions; it was removed, because the server sees less and guesses more. The
client knows whether `disconnected` persisted or healed in 200 ms; the observer does not.

Correlating ICE trouble is now configuration, not a class:

```typescript
observer.addObserverDetector("observer-concurrent-issue-detector", {
    issueTypes: ["ice-disconnected", "ice-connection-failed", "ice-transport-stalled"],
});
```

### `TrackDeliveryMismatchDetector` in detail

A dry track ("no bytes are arriving") is the clearest symptom there is and, on its own, completely
ambiguous. A receiver seeing silence cannot distinguish *the camera was switched off* from *the SFU
stopped forwarding* from *my own consumer wedged* — all three look identical from the browser.

Joining the two ends of the published track resolves it:

| Publisher | Subscribers | Verdict |
|---|---|---|
| sending | **all** dry | `PUBLISHED_TRACK_NOT_DELIVERED` — the forwarding path |
| sending | **some** dry | `RECEIVER_TRACK_NOT_DELIVERED` — those consumers (in mediasoup: recreate them) |
| dry | any dry | `PUBLISHER_TRACK_DRY` — the source stopped; **not** an SFU fault |

The publisher side is judged from both available signals: its own `dry-outbound-track` issue when
the client reports one, and the observed outbound RTP (`deltaPacketsSent`) as fallback and
corroboration. That combination is what makes the first row trustworthy — the server can state that
packets demonstrably left the publisher during the same interval in which every receiver got
nothing.

This needs **no mediasoup instrumentation at all** — the clients' own dry-track verdicts plus the
resolver links are sufficient.

## Findings and conclusions

Server-raised findings are `ObserverIssue`:

```typescript
type ObserverIssue = {
    type: string;
    timestamp: number;
    payload?: string | Record<string, unknown>;
};
```

{{< callout context="caution" title="The payload is the object" icon="alert-triangle" >}}
Do **not** `JSON.parse` it. A server-raised finding is delivered to an in-process handler, so
there is nothing to serialise for. (`ClientIssue`, the type on samples, keeps its string payload —
that one really is a wire format.)

```typescript
observer.on("call-issue", ({ issue }) => {
    issue.payload;                 // the object
    issuePayloadOf(issue);         // if you want to accept a string payload too
    issuePayloadAsString(issue);   // only at an edge that needs text
});
```
{{< /callout >}}

### Conclusions

Every issue-driven finding carries a `conclusion` — the interpretation step, so the person reading
the alert does not have to perform it:

```jsonc
{
  "type": "CROSS_CALL_ISSUE_ONSET_BURST",
  "issueType": "congestion",
  "calls": 40, "affectedCalls": 6,
  "perCall": [ { "callId": "…", "affectedClients": 4, "totalClients": 9 } ],
  "conclusion": {
    "faultDomain": "infrastructure",
    "summary": "network congestion is open across independent calls at the same time — 6 of 40 calls (11/300 clients)",
    "recommendation": "check SFU egress bandwidth and host network saturation before looking at any single participant",
    "confidence": 0.85
  }
}
```

`faultDomain` is one of `infrastructure`, `call`, `published-track`, `endpoint`,
`client-population` or `unknown`, and it comes from the **spread**, not the issue type — congestion
in one call is a meeting problem, congestion in six calls is a server problem, and the client
reported the identical symptom in both.

{{< callout context="note" title="The case that inverts the usual reading" icon="info-circle" >}}
**`cpu-limitation` spread across many independent calls concludes `client-population`, not
`infrastructure`.** Endpoint CPU is owned by the endpoint, so breadth there points at what those
endpoints share — a recent client release, a browser version, shared VDI hardware — and paging the
SFU on-call would be wrong. The conclusion table encodes that so nobody has to rediscover it during
an incident.
{{< /callout >}}

Unknown issue types (your own custom client detectors) still produce a structurally valid
conclusion from the spread alone; they just get generic wording.

Two functions are exported, one per scope: `concludeCallIssue()` and `concludeObserverIssue()`.

## Writing your own detector

A detector is any object with a `name` and an `update()`, called on every `call.update()` (call
scope) or `observer.update()` (observer scope).

```typescript
import { Observer, Detector } from "@observertc/observer-js";

class MyCrossClientDetector implements Detector {
    readonly name = "my-detector";

    constructor(private readonly call: ObservedCall) {}

    update() {
        // …inspect this.call.observedClients across participants…
        if (/* a condition only visible server-side */ false) {
            this.call.addIssue({
                type: this.name,
                payload: { /* … */ },
                timestamp: Date.now(),
            });
            // → emitted on the bus as 'call-issue'
        }
    }
}

const observer = new Observer();
observer.on("call-added", ({ observedCall }) => {
    observedCall.detectors.add(new MyCrossClientDetector(observedCall));
});
observer.on("call-issue", ({ observedCall, issue }) => { /* react */ });
```

An observer-scoped one, inline:

```typescript
observer.detectors.add({
    name: "sfu-wide-degradation",
    update: () => {
        const degraded = [...observer.observedCalls.values()].filter(isDegraded);

        if (observer.numberOfCalls > 3 && degraded.length / observer.numberOfCalls > 0.6) {
            observer.addIssue({ type: "SFU_WIDE_QUALITY_DEGRADATION", timestamp: Date.now() });
        }
    },
});

observer.on("observer-issue", ({ issue }) => alerting.page(issue));
```

To consume client issues rather than poll entities, implement `ActiveIssueTracker` and register
your types on the [registry](#activeissuesregistry--issues-are-pushed-not-polled).

## Cost

Detectors run inside `call.update()`, on your event loop. Two things keep their cost off the
participant axis:

- **Issues are pushed, not polled.** A detector holds only what the registry handed it, so an
  `update()` that finds `size === 0` — the overwhelmingly common case — costs one comparison,
  whatever the participant count.
- **So are unconsumed tracks.** `observedCall.unconsumedOutboundTracks` is maintained by the
  resolver as tracks gain and lose subscribers, so `UnconsumedTrackDetector` reads a normally-empty
  set instead of walking every published track (529 µs → 65 µs per tick at 1 200 tracks).
- **Track lookups start from the affected minority.** A detector resolving an issue to its
  published track searches the *reporting client's* peer connections, not the whole call.

At 20 calls × 12 participants (2 640 subscriptions) the whole detector pass costs roughly **1.3 ms
per tick**. `yarn bench` in the repository prints a per-detector breakdown for your own shape.

## Worked examples

The repository ships two runnable examples:

- [`examples/detectors.ts`](https://github.com/ObserveRTC/observer-js/blob/master/examples/detectors.ts)
  (`yarn example:detectors`) — one scenario per detector: the question it answers, its full config,
  the synthetic traffic that makes it fire, and the finding with its conclusion. It asserts every
  expected finding, so it doubles as a smoke test.
- [`examples/sfu-observer.ts`](https://github.com/ObserveRTC/observer-js/blob/master/examples/sfu-observer.ts)
  (`yarn example`) — the end-to-end tour: ingest → correlate → react, with the mediasoup wiring
  alongside.
