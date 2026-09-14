---
title: "Connectivity detectors"
description: "The five layers a WebRTC connection climbs, and the nine detectors that own them"
lead: "If a user cannot establish or maintain a working connection, where exactly did it fail?"
date: 2026-09-13T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 231
toc: true
---

This is the reference for **category 1**. It exists because the alternative is five issue types
that all mean approximately "ICE didn't work".

```text
Application / signaling      (not observable here)
        │
        ▼
1  Reachability              can we reach the ICE infrastructure at all?
        │
        ▼
2  Discovery / traversal     what candidates could we produce, and what path do they permit?
        │
        ▼
3  Path establishment        did any candidate pair actually win?
        │
        ▼
4  Secure transport          did DTLS complete on the path ICE found?
        │
        ▼
5  Path continuity           does the established path persist, and how much does it move?
```

**A layer begins where the previous layer's success is proven, and every issue belongs to the
*first* layer whose proof fails.** That single sentence is what keeps the taxonomy from collapsing:
a connection that never gathered a relay candidate is not a "path establishment" failure that
happens to have no candidates — it is a layer 1/2 failure, and layer 3 must stay quiet about it.

The layers are also the escalation order for an engineer reading a session: start at the lowest
layer that raised an issue, because everything above it is downstream.

## The grid

| Layer | Class | Issue | Config key |
|---|---|---|---|
| 1 Reachability | `IceReachabilityDetector` | `no-available-ice-candidate` | `iceReachabilityDetector` |
| 2 Discovery / traversal | `IceTraversalDetector` | *(none, by design)* | `iceTraversalDetector` |
| 3 Path establishment | `IcePathEstablishmentDetector` | *(event only)* | `icePathEstablishmentDetector` |
| 3 Path establishment | `IceEstablishmentFailedDetector` | `ice-establishment-failed` | `iceEstablishmentFailedDetector` |
| 4 Secure transport | `DtlsHandshakeFailedDetector` | `dtls-handshake-failed` | `dtlsHandshakeFailedDetector` |
| 4 Secure transport | `DtlsHandshakeStalledDetector` | `dtls-handshake-stalled` | `dtlsHandshakeStalledDetector` |
| 5 Path continuity | `IceDisconnectedDetector` | `ice-disconnected` | `iceDisconnectedDetector` |
| 5 Path continuity | `IceConnectionFailedDetector` | `ice-connection-failed` | `iceConnectionFailedDetector` |
| 5 Path continuity | `IceTransportStalledDetector` | `ice-transport-stalled` | `iceTransportStalledDetector` |
| 5 Path continuity | `UnstableIcePathDetector` | `unstable-ice-path` | `unstableIcePathDetector` |
| *(beside)* | `IceRestartDetector` | *(event only)* | `iceRestartDetector` |
| *(beside)* | `IceRestartRecommendationDetector` | *(event only)* | `iceRestartRecommendationDetector` |

Every class here binds to `PeerConnectionMonitor`. Turning a whole layer off means naming each of
its keys — which is the point of the 4.9 config model.

{{< callout context="note" title="There used to be a sixth layer" icon="info-circle" >}}
"Media flow", holding `BlockedTransportDetector`, has been retired. Every connectivity stage
completes and *holds* in that condition — the pair is `succeeded`, consent keeps passing, `iceState`
reads `connected` — and the path simply is not delivering. That is Transport Quality's membership
test word for word. The finding is now three classes; see
[transport quality](../detectors-transport-quality/).
{{< /callout >}}

## Layer 1 — Reachability

**Question.** Can the client reach the ICE infrastructure it was configured with?
**Ends when** gathering reports `complete`, or the connection gives up.

### `IceReachabilityDetector` → `no-available-ice-candidate`

ICE gathering produced **zero** local candidates: there was nothing to connect *with* — no
interface up, airplane mode, a VPN that tore down every route, or a network locked down so tightly
the sockets cannot bind.

Every other ICE issue describes a path that existed and stopped working; this one says no path was
ever possible. A healthy client gathers at least one host candidate within milliseconds, since any
interface that is up yields one even with no internet — so an empty candidate list is not a slow
start but an absent network.

Three guards, each ruling out a distinct false positive:

- Zero candidate rows count as evidence only once `iceGatheringState` reads `complete`. Before
  that they mean gathering is still running; where the field is absent they mean nothing was
  measured, which is not the same as "gathering produced nothing".
- Falling to `disconnected` / `failed` with zero candidates raises **immediately** — the browser
  has already given its verdict and the empty list explains it. Merely sitting in `new` /
  `connecting` has to outlast `thresholdInMs`, which keeps the detector off an un-negotiated peer
  connection.
- It never fires on a connection that once reached `connected`. Mid-call network loss is layer 5.

It cannot separate "no network" from "every candidate type forbidden by policy", and does not try:
operationally both mean this client cannot do WebRTC here.

```javascript
iceReachabilityDetector: {
    thresholdInMs: 6000,   // grace for `new`/`connecting` with zero local candidates
}
```

**User symptom.** Cannot join, or joins and then fails when relay would have been needed.

## Layer 2 — Discovery and traversal

**Question.** What kind of path do the gathered candidates permit, and what did the endpoint have
to use?

### `IceTraversalDetector` → events only

**Raises no issues, deliberately.** Needing TURN is not a fault; it is a cost. A relay path works,
and reporting it as a problem would train operators to ignore the layer.

It reports `ice-tuple-changed` when the selected local:remote tuple set changes, and the classified
`ice-path-changed` transitions `SelectedIcePath` produces — `direct-to-relay`, `relay-to-direct`,
`turn-server-changed`, `relay-protocol-changed`, `path-changed`. Establishment itself is not a
change: growing from an empty set is skipped, or every call would report a path move in its first
seconds.

The normalized path classification is `IcePathKind`: `direct`, `turn-udp`, `turn-tcp`, `turn-tls`,
`turn-unknown`. It is derived `candidateType`-first — a `relay` candidate is by definition obtained
from TURN — with `relayProtocol` as fallback, because a `srflx` candidate discovered *through* a
TURN server's STUN function also carries a `turn:` URL and would otherwise be misread as relay.

The path kind rides along on the payload of every issue that carries a candidate pair, so any
higher-layer issue reads as "…and it happened on a TURN/TLS path" without a separate signal.

`iceTraversalDetector: {}` enables it, `null` disables it — it has no tunables. (Before 4.9 it was
registered unconditionally and could only be silenced by name.)

## Layer 3 — Path establishment

**Question.** Did any candidate pair reach `succeeded` **and** `nominated`? Two classes, because
slow and failed are two claims.

### `IcePathEstablishmentDetector` → `ice-path-establishment-slow` (event)

Reports how long a peer connection has been trying to connect, and — the part that makes it
actionable — **which stage it is stuck in**. Nothing else in the library can answer that, because
`connectionState: 'connecting'` deliberately covers ICE gathering, ICE checking and the DTLS
handshake alike.

`stalledStage` is one of:

| Value | Meaning |
|---|---|
| `ice-gathering` | No transport exists yet |
| `ice-checking` | A transport is still negotiating connectivity |
| `dtls` | A transport's ICE side is done, the connection still is not `connected` |
| `unknown` | The stats give no verdict |

Where the browser reports no per-transport `iceState`, the selected pair being `succeeded` stands
in as proof the ICE side finished. The trigger is `connectionState` rather than any transport's ICE
state precisely because of that coverage: a connection whose DTLS handshake is hanging has every
transport reading `connected` while the call still does not work.

It re-arms on **any** exit from `connecting`, not only on `connected` — a retry that is also taking
too long is more interesting than the first attempt, not less. It raises no issue on purpose:
saying establishment is slow is not yet a claim that it failed.

```javascript
icePathEstablishmentDetector: {
    thresholdInMs: 5000,   // how long `connecting` may last before it is reported
    createEvent: true,     // also buffer the event into samples
}
```

### `IceEstablishmentFailedDetector` → `ice-establishment-failed`

The call that never connected — by a wide margin the most common connectivity failure a user
actually reports, and until 4.9 the one thing the library could not put in `activeIssues`. Layer 3
emitted an event when establishment dragged on, but an event is gone the moment it fires, so the
single most user-visible failure produced an empty issue list, which reads as a healthy call.

Three facts together, none sufficient alone:

1. **Local candidates exist** — so this is emphatically not the no-network case. Layer 1 owns that,
   and the two are mutually exclusive by construction.
2. **The peer connection has never reached `connected`** — so this is establishment failing rather
   than a working call that later broke.
3. **No candidate pair has ever been nominated or reached `succeeded`** — which separates "checks
   are still running and might yet win" from "nothing ever won". The nomination check is *latched*:
   a pair that won once is proof establishment got there, however it looks later.

All three must hold for the whole of `thresholdInMs`, accumulated from the peer connection's own
`deltaTime`. The default (15 s) sits well past `icePathEstablishmentDetector.thresholdInMs` (5 s)
on purpose — a connection that is merely slow has to be given time to stop being merely slow.

**The payload carries what was tried**, which is where the candidate types and the pair
`nominated` / `state` fields finally earn their place:

| `localCandidateCounts` shows | Reading |
|---|---|
| host only | Gathering never reached a STUN server |
| host + srflx, no relay | TURN was never configured or never answered — the most common cause of a call that fails only between certain networks |
| relay present, every pair `in-progress` or `failed` | The relay is unreachable, or the far end never answered the checks |

`candidatePairStates` is every distinct pair `state` seen, deduplicated and sorted. What it
deliberately does **not** claim is which side is at fault: every fact here is local, and a far end
that never sent an answer looks exactly like a far end whose candidates cannot be reached.

```javascript
iceEstablishmentFailedDetector: { thresholdInMs: 15000 }
```

**User symptom.** Cannot join the call.

## Layer 4 — Secure transport

**Question.** Did DTLS complete on the path ICE established? This layer separates "the network path
failed" from "the secure media transport never negotiated" — a certificate fingerprint mismatch,
DTLS version intolerance, or a middlebox that passes STUN but eats DTLS all used to present as a
generically slow `connecting`.

### `DtlsHandshakeFailedDetector` → `dtls-handshake-failed`

Raises on the first tick reporting `dtlsState: 'failed'`. There is nothing to wait for and nothing
to average: `failed` is the browser's terminal verdict on this key exchange, so there is no
maturity guard and no duration threshold, and the issue is raised once per transport rather than
once per tick.

Only a later `connected` resolves it — in practice an ICE restart re-ran the handshake and the new
generation succeeded. A transport dropping back to `new` / `connecting` after a restart is not yet
evidence of anything, so the issue stays open until one actually completes.

`dtlsHandshakeFailedDetector: {}` / `null` — `failed` is not a matter of degree, so there is
nothing to tune.

### `DtlsHandshakeStalledDetector` → `dtls-handshake-stalled`

Raises when the ICE side is **proven healthy** while `dtlsState` sits in `new` or `connecting` past
`stalledThresholdInMs`. This is the half with no verdict to read: a handshake being eaten by a
middlebox and one that is 300 ms from completing look identical in a single stats report, and only
duration separates them.

The payload's `iceEvidence` records which proof carried the finding — a finding resting on the
weaker one is worth less to whoever reads it:

| `iceEvidence` | Meaning |
|---|---|
| `transport-ice-state` | The transport reported `iceState` `connected` / `completed` |
| `selected-pair-succeeded` | No `iceState` reported (Safari, and the transport reconstructed for Firefox < 153); the selected pair being `succeeded` stood in |

The clock is stats time, and anything that ends the condition resets the accumulator: ICE health
lost, DTLS reaching `connected` or `failed`, a `closed` transport — and a changed ICE local
username fragment, since an ICE restart re-keys DTLS and the new generation deserves the full
threshold rather than inheriting the old one's.

A transport is never judged on its first observed tick: Firefox 153/154 report pre-negotiation
transport values that only 155 makes trustworthy. `dtlsState: 'closed'` is a shutdown, not a
failure, and is refused outright.

```javascript
dtlsHandshakeStalledDetector: { stalledThresholdInMs: 6000 }
```

**User symptom.** Appears stuck connecting even though the network path exists.

## Layer 5 — Path continuity

Four classes, one per finding, each keeping its own per-ICE-transport state — a peer connection
without BUNDLE has several transports and they fail independently. All four read the ICE local
username fragment themselves to notice a new generation rather than asking `IceRestartDetector`, so
none depends on another or on the order they run in.

### `IceDisconnectedDetector` → `ice-disconnected`

A transport that has been `disconnected` long enough that it is no longer going to fix itself.
`disconnected` on its own is never worth an issue: it is what a browser says when consent checks
have missed for a moment, and a Wi-Fi roam, a brief radio dropout or a busy CPU produce it several
times in an ordinary call while ICE quietly recovers.

Only duration separates the blip from the outage — measured in stats time, so a late collection
credits the outage with the time it actually lasted rather than the time the library spent not
looking. A new ICE generation resolves the standing issue and restarts the clock. Falling from
`disconnected` into `failed` does **not** resolve it: that transport has not recovered, it has got
worse.

```javascript
iceDisconnectedDetector: { disconnectedThresholdInMs: 5000 }
```

### `IceConnectionFailedDetector` → `ice-connection-failed`

A transport the browser has given up on. `failed` is terminal for the ICE generation — the browser
will not retry candidates on its own — so the issue is raised on the first tick that reports it.

**The payload carries `everConnected`**, and that field is why this issue is worth reading rather
than just counting:

| `everConnected` | Meaning | Where to look |
|---|---|---|
| `false` | The path **never worked**: no candidate pair ever won | What was tried and what was reachable — symmetric NAT with no TURN, a firewall eating the checks, a TURN credential the client never got |
| `true` | The path **worked and was lost** | The network underneath — the interface changed, the NAT binding expired, the route died |

Seeing both `ice-establishment-failed` and an `everConnected: false` `ice-connection-failed` in one
session is coherent rather than contradictory: layer 5 is reporting the end of a story layer 3 was
already telling.

`iceConnectionFailedDetector: {}` / `null` — a terminal state has no threshold to tune.

### `IceTransportStalledDetector` → `ice-transport-stalled`

The quiet failure: every state still reads healthy — ICE `connected`, the selected pair
`succeeded`, no error anywhere — while the transport keeps sending and receives nothing back. No
state machine will ever report this; the only evidence is the asymmetry between what leaves and
what arrives.

Our own outbound traffic is what makes the expectation defensible: a live ICE path returns at least
STUN consent responses and RTCP for whatever we send. The mirror case — silence in **both**
directions — is deliberately not reportable, because it cannot be told apart from a legitimately
idle connection. That is why the payload's `direction` is `'inbound'` and only `'inbound'`.

Two guards keep it off paths where receiving nothing is the healthy state, and both are load
bearing: inbound traffic must have been seen on this transport before, and inbound RTP must be
attributed to this transport at all. A send-only publish transport — the ordinary shape of a
mediasoup uplink — receives only consent responses and RTCP in bursts seconds apart. *(Fixed in
4.9: before that, this detector and `blocked-transport` both raised on healthy one-way calls.)*

```javascript
iceTransportStalledDetector: { transportStallThresholdInMs: 5000 }
```

### `UnstableIcePathDetector` → `unstable-ice-path`

A transport whose selected path will not settle — a worse experience than a path that is simply
down. Each reselection is a fresh round of consent checks over a new tuple, so media stutters, the
encoder's bandwidth estimate is thrown away and rebuilt, and the call sounds broken while every
state field reports `connected` throughout. The usual causes: a device with two live interfaces
fighting over which one wins, a NAT rewriting bindings underneath a live flow, or a TURN allocation
that keeps being re-established.

Switches are counted as the **larger of two sources**, because neither alone is sufficient. Diffing
`selectedCandidatePairId` tick to tick is portable but blind to a flap that departs and returns
inside one collecting period. The browser's own `selectedCandidatePairChanges` delta sees exactly
those, but Safari does not report it and neither does Firefox before 155. The payload carries the
native count separately as `nativePairChanges`.

The window is **tumbling**, not sliding: each tick adds the transport's own `deltaTime`, and once
the accumulated time passes `pathSwitchWindowInMs` both counters reset.

The threshold is reasoned, not arbitrary: a legitimate handover produces one switch, occasionally
two. Consent checks run roughly every five seconds, so three or more switches inside thirty seconds
means no path survived even a few consent intervals — oscillation, not migration.

```javascript
unstableIcePathDetector: {
    pathSwitchWindowInMs: 30000,
    pathSwitchThreshold: 3,
}
```

**User symptoms.** `ice-disconnected` / `ice-connection-failed`: audio and video suddenly stop.
`ice-transport-stalled`: the call looks connected and nothing arrives. `unstable-ice-path`:
intermittent freezes and reconnections.

## Restarts: the telemetry alongside the ladder

Two classes sit beside the ladder rather than on it. Neither raises an issue and neither ever will:
a restart is a fact about the connection, not a fault, and recommending one is advice rather than a
finding.

### `IceRestartDetector` → `ice-restart` (event)

Reports that a transport started a new ICE generation, and how it turned out. The evidence is a
changed ICE local username fragment — renegotiated per generation, and therefore the one field a
restart cannot leave alone. That is an inference, not a report: the browser exposes no "a restart
happened" signal, and stats cannot separate a restart the application asked for from one the
browser started itself. Firefox's transport report is reconstructed and carries no fragment, so the
detector falls back to the selected local candidate's `usernameFragment` and stays silent when
neither exists.

Three outcomes rather than one, because "a restart was attempted" and "the restart worked" are
different facts: `detected` when the fragment changes, then `recovered` or `failed` when the
generation reaches `connected`/`completed` or `failed`. A generation still checking has no outcome,
and none is invented for it.

### `IceRestartRecommendationDetector` → `ice-restart-recommended` (event)

The one place that says "restart ICE". It recommends and never performs: only the application knows
whether renegotiation is safe at this moment, whether the signalling channel is up, and what the
far end expects.

| `reason` | Scope | Waits for |
|---|---|---|
| `ice-failed` | per transport | Nothing — ICE never self-heals from `failed` |
| `ice-disconnected` | per transport | `iceRestartRecommendationThresholdInMs` |
| `transport-stalled` | per transport | `iceRestartRecommendationThresholdInMs` |
| `never-established` | per peer connection | `restartRecommendationThresholdInMs` |

Four conditions in one class is the documented exception to one-class-per-issue, and it is
legitimate: they produce one *event* type rather than four issue types, they answer one question —
*would starting ICE over help?* — and the rate limiting only means anything if it is shared. Two
detectors each politely waiting out their own cooldown produce twice the nagging.

Every verdict is reached from raw transport and connection state, never by asking the layer-5
detectors what they concluded; the stall condition and all its guards are written out a second time
in this class for exactly that reason. A restart already in flight suppresses recommendations until
it resolves. `recommendationCount` rising against a flat `iceGeneration` is what tells a reader the
advice is not being taken — or is not working.

```javascript
iceRestartRecommendationDetector: {
    createEvent: true,
    iceRestartRecommendationThresholdInMs: 10000,  // per transport: disconnected / stalled
    iceRestartRecommendationCooldownInMs: 15000,
    restartRecommendationThresholdInMs: 10000,     // per pc: never established at all
    restartRecommendationCooldownInMs: 15000,
}
```

{{< callout context="note" title="All four conditions live in one block now" icon="info-circle" >}}
Before 4.9 each half of this class was gated by a different neighbour's key, so an
`icePathEstablishmentDetector: null` meant to switch off the slow-establishment event also silenced
every `never-established` recommendation. Both halves now run whenever this key is set, and
`iceRestartRecommendationDetector: null` is the one way to silence any of it.
{{< /callout >}}

## What this model deliberately does not do

- **No `ConnectivityState` enum.** A single current state cannot represent a peer connection whose
  two transports are in different states. What the model provides instead is ordering.
- **No detector for what the monitor cannot see.** DNS resolution, signaling health, SFU
  reachability and captive portals are invisible to `getStats()`.
- **No issue for a working fallback.** TURN required, TURN/TCP and TURN/TLS fallback are events.
  They cost latency and loss resilience, and a fleet should count them — but a call that works is
  not a fault.
- **No per-server reachability finding.** Distinguishing an unreachable STUN server from a rejected
  TURN credential is genuinely valuable and the evidence exists in `icecandidateerror` verdicts. No
  detector consumes it today; it is recorded as a gap rather than documented as behaviour.
- **No duplication of the quality axis.** A connectivity detector that starts reasoning about
  quality has left its layer.
