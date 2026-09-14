---
title: "Ingestion & lifecycle"
description: "accept(), middlewares, context vs appData, teardown, and when things update"
lead: "One entry point, one optional context object, and an update model that is structural rather than configurable"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 310
toc: true
---

## The data flow

```text
client getStats()  ──►  ClientSample  ──►  observer.accept(sample, ctx?)
                                               │
              ┌────────────────────────────────┘
              ▼
   accept middlewares (global, in order)
              │
              ▼
   get-or-create ObservedCall ──► get-or-create ObservedClient ──► client.accept(sample, ctx)
                                                                        │
                                              per peerConnections[] in the sample
                                                                        ▼
                                              get-or-create ObservedPeerConnection
                                              .accept(pcSample, ctx) updates all sub-stats,
                                              derives deltas/bitrates/RTT, correlates remote RTP
                                                                        │
                          metrics roll up: PeerConnection → Client → Call → Observer
                                                                        │
                                          events emitted on the Observer bus
```

## `observer.accept(sample, context?)`

The single entry point. It:

{{< steps >}}
{{< step >}}drops the sample and emits `sample-rejected` if the observer is closed;{{< /step >}}
{{< step >}}runs it through the global accept-middleware chain;{{< /step >}}
{{< step >}}drops it and emits `sample-rejected` if `callId` or `clientId` is missing;{{< /step >}}
{{< step >}}gets or lazily creates the `ObservedCall` and `ObservedClient`;{{< /step >}}
{{< step >}}delegates to `client.accept(sample, context)`, which fans out to each peer connection.{{< /step >}}
{{< /steps >}}

Sub-entities that stop appearing in samples are garbage-collected by a "visited" mark-and-sweep on
each `ObservedPeerConnection.accept()`, emitting the corresponding `*-removed` events.

## Accept middlewares

`observer.addAcceptMiddleware(...)` registers middlewares run on **every** sample inside `accept()`,
in order, **before** the sample is dispatched to any call or client. Each gets a
`{ sample, context }` payload; it can inspect or mutate either, then call `next(payload)` to
continue.

```typescript
import { Observer, AcceptMiddleware } from '@observertc/observer-js';

const observer = new Observer();

// Derive callId/clientId from the app's own attachment, before dispatch.
const route: AcceptMiddleware = ({ sample }, next) => {
    sample.callId ??= sample.attachments?.roomId as string;
    sample.clientId ??= sample.attachments?.peerId as string;
    next({ sample });
};

// Drop samples from a blocklisted client — never dispatched.
const filter: AcceptMiddleware = (payload, next) => {
    if (blocked.has(payload.sample.clientId)) return;   // no next() => dropped
    next(payload);
};

observer.addAcceptMiddleware(route, filter);
observer.removeAcceptMiddleware(route);
```

**Not calling `next` drops the sample** — nothing is created and no event fires. A throwing
middleware is caught and warns (the sample is dropped) rather than crashing `accept()`. When no
middleware is registered, `accept()` dispatches directly with no overhead.

## `context` versus `appData`

```typescript
type AcceptContext = Record<string, unknown>;
```

A single optional object threaded down the whole accept chain. It is **transient request-scoped
data**, never written to `appData` and not stored on any entity.

| | `appData` | `context` |
|---|---|---|
| Set | At creation (`settings.appData` or a factory), or by the app on `*-added` | Per `accept()`, may differ every time |
| Lives | On the entity, for its lifetime | Through this one accept, then discarded |
| Owned by | The application — the library never changes it | The caller |
| Reaches | Anything holding the entity | The `*-updated` events this accept triggers |

`client-updated` and `peer-connection-updated` carry the exact context of that sample;
`call-updated` carries the context of the client `accept()` that drove the call update (absent for
interval- or teardown-driven updates).

### `appData` factories

Instead of pre-creating an entity just to enrich its `appData`, register a factory once. It runs
whenever the entity is created without an explicit `settings.appData` — including lazily inside
`accept()` — and **receives the accept context that caused the creation**:

```typescript
const observer = new Observer({
    createCallAppData:   ({ callId, acceptCtx })      => ({ callId, startedAt: Date.now(), tenant: acceptCtx?.tenant }),
    createClientAppData: ({ clientId, observedCall }) => ({ clientId, tenant: observedCall.appData.tenant }),
});

observer.accept(sample, { tenant: 'acme' });
```

That is what lets an accept middleware resolve something once — a tenant, a trace id — and have it
land in `appData` at birth, instead of every factory re-deriving it from the sample. `appData` stays
application-owned: the context is *offered* to the factory, never written across by the library.

The client factory receives the already-created parent `observedCall`, so it can derive fields from
it.

## Get-or-create helpers

```typescript
const call = observer.getOrCreateObservedCall({ callId, appData }, acceptCtx?);
const client = call?.getOrCreateObservedClient({ clientId, appData }, acceptCtx?);
```

These return `undefined` (and warn) when the parent is closed. `createObservedCall` /
`createObservedClient` return the **existing** instance (and warn) if the id already exists.

{{< callout context="caution" title="Guard the result" icon="alert-triangle" >}}
The library **warns and degrades; it does not throw** on operational problems, so every `create*` and
`getOrCreate*` returns `T | undefined`.
{{< /callout >}}

## When things update

"Update" means *recompute aggregated metrics, run the detectors, and emit the `*-updated` event* at
that level. Updates are **event-driven** — there is no built-in timer.

> **A call is updated when any of its clients is updated. The observer is updated when any of its
> calls is updated.** Composed: the observer is updated exactly when any client anywhere is updated.

| Setting | Where | Effect when `false` |
|---|---|---|
| `autoUpdateOnClientUpdate` | `ObservedCallSettings` | the call updates only when you call `call.update()` |
| `autoUpdateOnCallUpdate` | `ObserverConfig` | the observer updates only when you call `observer.update()` |

```typescript
const observer = new Observer({ autoUpdateOnCallUpdate: false });
setInterval(() => observer.update(), 5_000);
```

{{< callout context="caution" title="Observer-scoped detectors and validators run nowhere else" icon="alert-triangle" >}}
If the observer never updates, they never run.
{{< /callout >}}

The `updatePolicy` / `defaultCallUpdatePolicy` enum and the pluggable `Updater` are **gone** in
1.0. "When all clients have updated" sounds appealing and deadlocks on the first client that stops
sending — one silent participant froze the whole call's aggregation until it timed out.

## Automatic teardown

```typescript
new Observer({
    closeClientIfIdleForMs: 60_000,   // a client with no sample for this long auto-closes
    closeCallIfEmptyForMs: 20_000,    // a call with zero clients for this long auto-closes
});
```

Closing cascades down (call → clients → peer connections → sub-stats), unsubscribing listeners and
emitting the `*-closed` / `*-removed` events.

{{< callout context="caution" title="These two timeouts have non-obvious failure modes" icon="alert-triangle" >}}
**Too low a client timeout re-creates a paused participant as a *new* client**, restarting its
detectors and splitting one person into two in any summary. **Too low a call timeout splits one
meeting into several calls**, each emitting its own `call-summary`.
{{< /callout >}}

Issues still open when a client closes are force-resolved with `resolvedBy: 'client-closed'`, and
the registry additionally expires stale entries — so a crashed participant cannot leave an issue
"active" forever.

## Error-handling philosophy

The library **warns and degrades; it does not throw** on operational problems:

| Condition | What happens |
|---|---|
| `createObservedCall` / `createObservedClient` on a closed parent | warn + return `undefined` |
| Duplicate id | warn + return the **existing** instance |
| `accept()` on a closed client | warn + no-op |
| Sample missing `callId` / `clientId`, or observer closed | `sample-rejected` event |
| A throwing accept middleware | warn + drop that sample |
| A throwing summary enricher | logged and skipped — a summary is a side-channel |

`sample-rejected` carries `reason: 'observer-closed' | 'missing-callId' | 'missing-clientId'` and the
sample itself, so a rejected sample is observable rather than silent.
