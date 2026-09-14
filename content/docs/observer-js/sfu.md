---
title: "SFU integration"
description: "Remote track resolution and mediasoup router observation"
lead: "Two independent opt-ins that happen to share a vendor name"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 360
toc: true
---

## Remote track resolution

In an SFU, one participant's **outbound** track is delivered to other participants as **inbound**
tracks — one publisher, many subscribers. Correlation is **opt-in per observer**: set
`ObserverConfig.createRemoteTrackResolver`, a factory invoked when each call is created that returns
the call's `RemoteTrackResolver` (or `undefined` for none).

```typescript
import { Observer, createDefaultMediasoupRemoteTrackResolverFactory } from '@observertc/observer-js';

const observer = new Observer({
    createRemoteTrackResolver: createDefaultMediasoupRemoteTrackResolverFactory(),
});

// later, given tracks — links are kept up to date as tracks come and go:
const source    = inboundTrack.remoteOutboundTrack;          // the publishing ObservedOutboundTrack
const receivers = [...outboundTrack.remoteInboundTracks];    // the subscribing ObservedInboundTrack[]
```

`RemoteTrackResolver` is a generic, strategy-driven class. It subscribes to the bus (filtered to its
call) and links tracks by **publisher id** — the link key — maintaining the links directly on the
tracks.

Two built-in factories ship:

| Factory | Publisher id | Subscriber id |
|---|---|---|
| `createDefaultMediasoupRemoteTrackResolverFactory()` | `attachments.producerId` | `attachments.consumerId` |
| `createP2pRemoteTrackResolverFactory()` | RTP **SSRC**, preserved end-to-end in p2p | — |

For the mediasoup factory, the application puts `producerId` / `consumerId` (and optionally
`direction`, `label`) into the track `attachments` — see
[tagging tracks](/docs/client-monitor-js/integrations/#tagging-tracks-for-server-side-correlation).

### Any other topology

The publisher id is just whatever links a subscribed track to the published one:

```typescript
import { Observer, RemoteTrackResolver } from '@observertc/observer-js';

const observer = new Observer({
    createRemoteTrackResolver: (observedCall) => new RemoteTrackResolver(observedCall, {
        resolveOutboundTrackPublisherId: (out) => out.attachments?.mediaId as string | undefined,
        resolveInboundTrackPublisherId:  (inb) => inb.attachments?.mediaId as string | undefined,
        resolveInboundTrackSubscriberId: (inb) => inb.attachments?.subId as string | undefined, // optional
    }),
});
```

### Backing a strategy with your own mapping

The three resolvers are plain functions returning a link key, so they can read a table your own
report already maintains rather than something the client attached. The only requirement is a key
**visible on both sides**. SSRC is the useful one, because it needs no client cooperation at all —
mediasoup knows each consumer's `rtpParameters.encodings[].ssrc` server-side, and the subscriber's
inbound RTP reports the same value:

```typescript
// your own table, filled where you already create consumers
const ssrcToProducerId = new Map<number, string>();

const observer = new Observer({
    createRemoteTrackResolver: (observedCall) => new RemoteTrackResolver(observedCall, {
        resolveOutboundTrackPublisherId: (out) => out.attachments?.producerId as string | undefined,
        resolveInboundTrackPublisherId:  (inb) => {
            const ssrc = inb.getInboundRtp()?.ssrc;
            return ssrc === undefined ? undefined : ssrcToProducerId.get(ssrc);
        },
    }),
});
```

{{< callout context="tip" title="A key that arrives late still links" icon="rocket" >}}
A track announces itself once, but its `attachments` are replaced on every sample and a table like
the one above is inherently racy against sample arrival. Tracks whose key does not resolve at first
sight are **held and retried on their own `*-track-updated`** — exactly when new stats arrive for
them — so a key that appears on the second sample links then, rather than being lost for the track's
lifetime.

`resolver.pendingTrackCounts` reports how many are still waiting; in a healthy setup it is
`{ inbound: 0, outbound: 0 }`. *(Before 1.0 resolution was one-shot, and an unresolvable track was
invisible for its whole life.)*
{{< /callout >}}

If a strategy resolves *nothing* the failure is quiet — "no subscribers" and "no links resolved" look
identical from the outside. That is what the
[`remote-track-resolver` validator](../validators/#remotetrackresolvervalidator) is for; run it once
in staging after wiring up a custom strategy.

### Resolution stands alone

Track resolution and mediasoup router observation are two **independent** opt-ins. Nothing in
`RemoteTrackResolver` reads `ObservedMediasoupRouter`, and nothing in `ObservedMediasoupRouter`
touches calls, clients or tracks.

So if your application already builds its own per-router report and you only want the detectors that
need publisher↔subscriber links, set `createRemoteTrackResolver` and simply never call
`observer.createObservedMediasoupRouter(…)`. No `MediasoupRouterSample` is created, nothing
accumulates, and these keep working: `UnconsumedTrackDetector`,
`PublisherFaultCorroborationDetector`, `TrackDeliveryMismatchDetector`, `IssueFanOutDetector`,
`RemoteTrackResolverValidator` and `SimulcastReceiverValidator`.

## Mediasoup router observation

Everything above is built from the **client-reported** `ClientSample`. When you run a
[mediasoup](https://mediasoup.org) SFU you also have the **server's own** ground truth — its routers,
transports, producers, consumers and data channels, with exact lifetimes and state transitions.

You hand the observer a live mediasoup `Router`; it attaches to mediasoup's own `observer` API and
from then on **passively tracks** the router's topology and lifecycle, with no polling and no changes
to your media code:

- new transports (`webrtc` / `plain` / `pipe` / `direct`), their selected `tuple`, ICE/DTLS/SCTP
  state transitions and `connectedAt`;
- producers (codec, SSRCs/RIDs, pause/resume) and consumers (pause/resume,
  `producerPaused` / `producerResumed`);
- data producers and data consumers;
- `createdAt` / `closedAt` for every entity above.

All of it lives in memory in a single `MediasoupRouterSample` exposed as `observedRouter.sample`. The
sample **accumulates for the life of the router**: closed transports, producers and consumers are
kept with their `closedAt` set, not removed.

### Options

```typescript
const observedRouter = observer.createObservedMediasoupRouter({
    router,                                          // the live mediasoup Router
    matchPeerConnectionByWebRtcTransportId: true,    // opt in to peer-connection matching
    appData: { /* application-owned bag */ },
    attachments: { /* carried on sample.attachments */ },
});
```

| Field | Required | Meaning |
|---|---|---|
| `router` | yes | The live router to observe; `.id` and the sample's `routerId` come from `router.id` |
| `matchPeerConnectionByWebRtcTransportId` | no | Emit `mediasoup-router-matched-with-peer-connection` for each peer connection whose id matches one of the router's WebRTC transport ids. Omitted or `false` → no matching, and the event never fires |
| `appData` | no | Application-owned bag on the `ObservedMediasoupRouter` |
| `attachments` | no | Free-form data carried on `sample.attachments` |

Useful members on the returned object: `.sample`, `.appData`, `.attachments`,
`.webrtcTransportIds: Set<string>`, `.id`, `.snapshot()`, `.close()`.

{{< callout context="caution" title="Memory & large meetings" icon="alert-triangle" >}}
This is intentionally the **simplest** approach — everything lives in memory and nothing is sampled
or evicted for you.

- **Consumers grow as O(N²)** on a single flat router: with `N` participants each producing audio +
  video and consuming everyone else, the sample holds roughly `2·N·(N−1)` consumer records (≈19,800
  for N = 100).
- The sample is **cumulative**, so it also grows with call duration and churn.

A 100-participant flat router can reach tens of MB and keep growing. There is **no built-in sink,
snapshotting or eviction, by design.** If you run large meetings, sample it yourself: read
`observedRouter.sample` on your own cadence, persist what you need, and close routers you no longer
track. (mediasoup also typically shards routers across workers, which keeps any one router small.)
{{< /callout >}}

### Annotating the sample

Every entity has an `attachments?: Record<string, unknown>` slot, and there are three ways to fill
it, from most declarative to most ad-hoc.

**1. `enrich` — mirror mediasoup's own `appData`.** Runs once per entity at creation, before the
corresponding event:

```typescript
observer.createObservedMediasoupRouter({
    router,
    enrich: {
        producer: (producer) => ({ participantId: producer.appData.participantId, purpose: producer.appData.purpose }),
        consumer: (consumer) => ({ subscriberId: consumer.appData.subscriberId }),
        transport: (transport) => ({ role: transport.appData.role }),
    },
});
```

A throwing enricher is caught and logged — it cannot take the router's bookkeeping down with it.

**2. Lifecycle events — enrich on the fly.** Each entity announces itself as `<entity>-sample-added`
and `<entity>-sample-closed`, carrying **the live sample object** (not a copy) plus the mediasoup
object it came from. Mutating it in the handler is the intended pattern:

```typescript
observedRouter.on('producer-sample-added', ({ sample, producer, transport }) => {
    sample.attachments = { ...sample.attachments, participantId: lookup(producer.id) };
});

observedRouter.on('producer-sample-closed', ({ sample }) => archive(sample));   // closedAt is set
```

Events: `transport-sample-added` / `-closed`, `producer-sample-added` / `-closed`,
`consumer-sample-added` / `-closed`, `data-producer-sample-added` / `-closed`,
`data-consumer-sample-added` / `-closed`.

**3. `attachTo(id, attachments)` — annotate later, from anywhere**, when the knowledge arrives after
the entity did:

```typescript
observedRouter.attachTo(producerId, { participantId, joinedFrom: 'mobile' });   // merges
```

Ids are unique across mediasoup entity kinds, so one method covers all of them. It returns `false`
for an unknown id rather than failing quietly. Typed accessors index the *same* objects the arrays
hold, so a lookup is O(1): `getTransportSample(id)`, `getProducerSample(id)`, `getConsumerSample(id)`,
`getDataProducerSample(id)`, `getDataConsumerSample(id)`.

### Building your own report

`observedRouter.sample` is live — arrays grow and `history` entries are appended as the router runs,
so a report built directly on it keeps changing after you think you are done. Use **`snapshot()`**
for a detached deep copy:

```typescript
const report = {
    ...observedRouter.snapshot(),        // never moves again
    generatedAt: Date.now(),
    region: process.env.REGION,
};
```

### Matching peer connections — by event, not by storage

A mediasoup WebRTC transport and a client's `RTCPeerConnection` share the same id, so whenever an
observed peer connection's id matches one of the router's WebRTC transport ids, that is a match.

**The observer does not store the router (or its sample) on any entity.** Instead it emits
`mediasoup-router-matched-with-peer-connection` for every matching peer connection and steps back —
*your application* decides what the pairing means. The payload carries the full ancestry.

```typescript
observer.on('mediasoup-router-matched-with-peer-connection',
    ({ observedMediasoupRouter, observedCall, observedPeerConnection }) => {
        (observedPeerConnection.appData ??= {}).routerId = observedMediasoupRouter.id;
        myStore.linkRouterToCall(observedCall.callId, observedMediasoupRouter.id);
    },
);

observer.on('mediasoup-router-removed', ({ observedMediasoupRouter }) => {
    persist(observedMediasoupRouter.sample);   // its closedAt is set
});
```

Why event-driven rather than stored on the call:

- **Loose coupling.** The call model stays about client telemetry; the SFU view lives on its own
  object and is associated only if and how *you* choose.
- **You own the association.** One router serves many peer connections, across clients and calls,
  and the right place to keep that mapping is application-specific.
- **You own the sampling.** The router sample is plain in-memory state you read on your own terms.

### Ordering contract — observe the router first

Matching is **forward-only by design**, and that is sufficient because the lifecycle ordering is
guaranteed rather than racy:

- `ObservedMediasoupRouter` works purely by subscribing to mediasoup's `observer` API, so it can only
  see events that happen *after* it is created.
- A mediasoup transport is always created **on the server first**; only then can the client connect
  to it, produce or consume, and begin shipping samples.

So by the time a `peer-connection-added` fires, the router has already recorded that transport's id
in `webrtcTransportIds`, and a single forward-looking listener catches every match.

{{< callout context="caution" title="Your responsibility" icon="alert-triangle" >}}
Call `createObservedMediasoupRouter(…)` **as early as the router exists** — before transports are
added or samples are accepted. If you register the router *after* its transports are created or after
the client's first sample, those events are already in the past and the corresponding matches are
missed. The observer deliberately does not look backwards.
{{< /callout >}}
