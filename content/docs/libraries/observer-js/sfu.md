---
title: "SFU integration"
slug: "sfu"
description: "Remote track resolution and mediasoup router observation"
lead: "Linking a publisher's track to every subscriber of it, and observing the SFU's own ground truth"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 326
toc: true
---

In an SFU, one participant's **outbound** track is delivered to other participants as **inbound**
tracks — one publisher, many subscribers. Nothing in the raw stats says which inbound track carries
which published source. Establishing that link is what turns per-client symptoms into a verdict
about *where* the fault is.

There are two independent mechanisms here:

| | [Remote track resolution](#remote-track-resolution) | [mediasoup router observation](#mediasoup-router-observation) |
|---|---|---|
| Data source | The clients' own samples | The SFU's own `Router` object |
| SFU support | Any topology | mediasoup only |
| Enables | Four detectors and one validator | An independent server-side sample |
| Cost | Negligible | In-memory, grows with the meeting |

---

## Remote track resolution

Correlation is **opt-in per observer**: set `ObserverConfig.createRemoteTrackResolver`, a factory
invoked when each call is created that returns that call's `RemoteTrackResolver` (or `undefined`).

```typescript
import { Observer, createDefaultMediasoupRemoteTrackResolverFactory } from "@observertc/observer-js";

const observer = new Observer({
    createRemoteTrackResolver: createDefaultMediasoupRemoteTrackResolverFactory(),
});
```

`RemoteTrackResolver` subscribes to the bus, filtered to its call, and links tracks by **publisher
id** — maintaining the links directly on the track objects:

```typescript
const source    = inboundTrack.remoteOutboundTrack;          // the publishing ObservedOutboundTrack
const receivers = [...outboundTrack.remoteInboundTracks];    // the subscribing ObservedInboundTrack[]
const orphans   = observedCall.unconsumedOutboundTracks;     // published, nobody subscribed
```

Links are kept up to date as tracks come and go.

### Built-in factories

| Factory | Publisher key | Subscriber key |
|---|---|---|
| `createDefaultMediasoupRemoteTrackResolverFactory()` | `attachments.producerId` | `attachments.consumerId` |
| `createP2pRemoteTrackResolverFactory()` | RTP **SSRC** | SSRC — preserved end to end in P2P |

For the mediasoup factory, the client application puts `producerId` and `consumerId` (and
optionally `direction` and `label`) into the track `attachments`. See
[tagging tracks](/docs/libraries/client-monitor-js/integrations/#tagging-tracks-for-server-side-correlation).

### Any other topology

The publisher id is just whatever links a subscribed track to the published one. Supply your own
key resolvers:

```typescript
import { Observer, RemoteTrackResolver } from "@observertc/observer-js";

const observer = new Observer({
    createRemoteTrackResolver: (observedCall) =>
        new RemoteTrackResolver(observedCall, {
            resolveOutboundTrackPublisherId: (out) => out.attachments?.mediaId as string | undefined,
            resolveInboundTrackPublisherId:  (inb) => inb.attachments?.mediaId as string | undefined,
            resolveInboundTrackSubscriberId: (inb) => inb.attachments?.subId as string | undefined, // optional
        }),
});
```

### What the links unlock

{{< card-grid >}}
{{< link-card title="IssueFanOutDetector" description="Does this issue follow one published source, or one receiver?" href="../detectors/" >}}
{{< link-card title="PublisherFaultCorroborationDetector" description="Do both ends of one track independently agree the source is at fault?" href="../detectors/" >}}
{{< link-card title="TrackDeliveryMismatchDetector" description="Publisher sending but every receiver dry means the forwarding path — not the camera." href="../detectors/" >}}
{{< link-card title="UnconsumedTrackDetector" description="Uplink and SFU ingress spent on media nobody is receiving." href="../detectors/" >}}
{{< /card-grid >}}

{{< callout context="caution" title="Prove the wiring" icon="alert-triangle" >}}
A resolver pointed at the wrong `attachments` field produces **no links**, and every detector above
correctly stays silent — which is indistinguishable from a healthy deployment. Run the
[`remote-track-resolver` validator](../validators/#remotetrackresolvervalidator) at start-up.
{{< /callout >}}

---

## mediasoup router observation

Everything above is built from client-reported samples. When you run a
[mediasoup](https://mediasoup.org) SFU you also have the **server's own** ground truth — routers,
transports, producers, consumers and data channels with exact lifetimes and state transitions.

`ObservedMediasoupRouter` captures that into a **`MediasoupRouterSample`**, completely independent
of the client sample pipeline.

### The concept

You hand the observer a live mediasoup `Router`; it attaches to mediasoup's own `observer` API and
**passively tracks** the router's topology and lifecycle — no polling, no changes to your media
code:

- new transports (`webrtc` / `plain` / `pipe` / `direct`), their selected `tuple`, ICE/DTLS/SCTP
  state transitions and `connectedAt`
- producers (codec, SSRCs/RIDs, `pause`/`resume`) and consumers (`pause`/`resume`,
  `producerPaused`/`producerResumed`)
- data producers and data consumers
- `createdAt` / `closedAt` for every entity above

All of it lives in memory as `observedRouter.sample`, a plain object you own. The sample
**accumulates for the life of the router**: closed entities are kept with `closedAt` set, not
removed.

### Options

`observer.createObservedMediasoupRouter(settings)`

| Field | Type | Required | Meaning |
|---|---|---|---|
| `router` | `mediasoup.types.Router` | yes | the live router to observe |
| `appData` | `Record<string, unknown>` | no | application-owned bag on the `ObservedMediasoupRouter` |
| `attachments` | `Record<string, unknown>` | no | free-form data carried on `sample.attachments` |
| `matchPeerConnectionByWebRtcTransportId` | `boolean` | no | opt in to peer-connection matching. Omitted / `false` → the event never fires |

Returns the `ObservedMediasoupRouter`, or `undefined` if the observer is closed. A router with the
same id returns the existing instance (both warn).

Useful members: `.sample`, `.snapshot()`, `.appData`, `.attachments`,
`.webrtcTransportIds: Set<string>`, `.id`, `.close()`, plus typed accessors
`getTransportSample(id)`, `getProducerSample(id)`, `getConsumerSample(id)`,
`getDataProducerSample(id)`, `getDataConsumerSample(id)`.

### Ordering contract — observe the router first

{{< callout context="caution" title="Create it as early as the router exists" icon="alert-triangle" >}}
`ObservedMediasoupRouter` works purely by subscribing to mediasoup's `observer` API, so it can only
see events that happen **after** it is created. Matching is forward-only by design.

That is sufficient because the lifecycle ordering is guaranteed: a mediasoup transport is always
created on the server first, and only then can the client connect, produce/consume and start
shipping samples. So a `peer-connection-added` can never appear before its server-side WebRTC
transport has already been observed.

**Your responsibility:** call `createObservedMediasoupRouter(...)` before transports are added or
samples accepted. Register it later and those events are already in the past — the matches are
missed, silently.
{{< /callout >}}

### Matching peer connections — by event, not by storage

A mediasoup WebRTC transport and a client's `RTCPeerConnection` share the same id. When
`matchPeerConnectionByWebRtcTransportId: true`, the observer emits
`mediasoup-router-matched-with-peer-connection` for each matching peer connection — once per
participant's transport — and steps back. **It does not store the router on any entity.**

```typescript
observer.on("mediasoup-router-matched-with-peer-connection",
    ({ observedMediasoupRouter, observedCall, observedClient, observedPeerConnection }) => {
        (observedPeerConnection.appData ??= {}).routerId = observedMediasoupRouter.id;
        myStore.linkRouterToCall(observedCall.callId, observedMediasoupRouter.id);
    },
);
```

Why event-driven instead of stored on the call:

- **Loose coupling.** The call model stays about client telemetry; the SFU view lives on its own
  object and is associated only if and how *you* choose.
- **You own the association.** One router serves many peer connections across clients and calls,
  and the right place to keep that mapping is application-specific.
- **You own the sampling.** The router sample is plain in-memory state you read on your own terms.

### Enriching the router sample

Every entity — router, transport, producer, consumer, data producer, data consumer — has an
`attachments?: Record<string, unknown>` slot. Three ways to fill it, most declarative first.

{{< tabs "enrich" >}}
{{< tab "enrich" >}}
Mirror mediasoup's own `appData`. Runs once per entity at creation, before the corresponding event.

```typescript
observer.createObservedMediasoupRouter({
    router,
    enrich: {
        producer:  (producer)  => ({ participantId: producer.appData.participantId, purpose: producer.appData.purpose }),
        consumer:  (consumer)  => ({ subscriberId: consumer.appData.subscriberId }),
        transport: (transport) => ({ role: transport.appData.role }),
    },
});
```

A throwing enricher is caught and logged — it cannot take the router's bookkeeping down.
{{< /tab >}}
{{< tab "Lifecycle events" >}}
Each entity announces itself carrying **the live sample object** (not a copy) plus the mediasoup
object it came from. Mutating it in the handler is the intended pattern.

```typescript
observedRouter.on("producer-sample-added", ({ sample, producer, transport }) => {
    sample.attachments = { ...sample.attachments, participantId: lookup(producer.id) };
});

observedRouter.on("producer-sample-closed", ({ sample }) => {
    archive(sample);   // its closedAt is set
});
```

Events: `transport-sample-added` / `-closed`, `producer-sample-added` / `-closed`,
`consumer-sample-added` / `-closed`, `data-producer-sample-added` / `-closed`,
`data-consumer-sample-added` / `-closed`.
{{< /tab >}}
{{< tab "attachTo" >}}
When the knowledge arrives after the entity did — a signalling message, a database lookup that
resolved.

```typescript
observedRouter.attachTo(producerId, { participantId, joinedFrom: "mobile" });   // merges
```

Ids are unique across mediasoup entity kinds, so one method covers all of them. It returns `false`
for an unknown id rather than failing quietly, which matters when application events race the
mediasoup ones.
{{< /tab >}}
{{< /tabs >}}

### Building your own report

`observedRouter.sample` is **live** — arrays grow and `history` entries are appended as the router
runs, so a report built directly on it keeps changing after you think you are done. Use
`snapshot()` for a detached deep copy:

```typescript
const report = {
    ...observedRouter.snapshot(),   // never moves again
    generatedAt: Date.now(),
    region: process.env.REGION,
};
```

{{< callout context="note" title="Custom data belongs in attachments" icon="info-circle" >}}
The sample types do not carry a `Record<string, unknown>` index signature. That signature allowed
arbitrary top-level keys but also silently accepted typos on real fields and weakened autocomplete.
If you were assigning ad-hoc keys directly onto a sample object, move them into `attachments`.
{{< /callout >}}

### Memory and large meetings

{{< callout context="caution" title="Nothing is evicted for you" icon="alert-triangle" >}}
This is intentionally the simplest possible approach — everything is in memory, nothing is sampled
or evicted. That is fine for typical rooms, but the cost at scale is real:

- **Consumers grow as O(N²)** on a single flat router: with `N` participants each producing audio +
  video and consuming everyone else, the sample holds roughly `2·N·(N−1)` consumer records — about
  19 800 at `N` = 100.
- The sample is **cumulative** — closed entities and their `history` are retained — so it also
  grows with call duration and churn (renegotiation, simulcast layer changes, rejoins).

A 100-participant flat router can reach tens of megabytes and keep growing. There is **no built-in
sink, snapshotting or eviction, by design.** If you run large meetings, do your own sampling: on
your own cadence read `observedRouter.sample`, persist what you need, drop the rest, and close
routers you no longer track. (mediasoup typically shards routers across workers, which keeps any
one router small.)
{{< /callout >}}

```typescript
const timer = setInterval(() => persist(observedRouter.snapshot()), 10_000);

observer.on("mediasoup-router-removed", ({ observedMediasoupRouter }) => {
    clearInterval(timer);
    persist(observedMediasoupRouter.sample);   // final state, closedAt set
});
```

### End-to-end example

```typescript
import { Observer } from "@observertc/observer-js";
import type { ObservedMediasoupRouterScope, ObservedPeerConnectionScope } from "@observertc/observer-js";

const observer = new Observer();

// 1) Observe the SFU side FIRST — as early as the router exists.
const observedRouter = observer.createObservedMediasoupRouter({
    router,
    matchPeerConnectionByWebRtcTransportId: true,
    enrich: {
        producer: (p) => ({ participantId: p.appData.participantId }),
    },
});

// 2) Feed client samples as usual.
transport.on("sample", (sample) => observer.accept(sample));

// 3) Every peer connection whose id matches a router transport id fires this.
observer.on("mediasoup-router-matched-with-peer-connection",
    ({ observedMediasoupRouter, observedCall, observedPeerConnection }:
        ObservedMediasoupRouterScope & ObservedPeerConnectionScope) => {
        (observedPeerConnection.appData ??= {}).routerId = observedMediasoupRouter.id;
        myStore.linkRouterToCall(observedCall.callId, observedMediasoupRouter.id);
    },
);

// 4) The router closed — persist the final state, drop your reference.
observer.on("mediasoup-router-removed", ({ observedMediasoupRouter }: ObservedMediasoupRouterScope) => {
    persist(observedMediasoupRouter.sample);
});
```
