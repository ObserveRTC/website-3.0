---
title: "Ingestion & lifecycle"
slug: "ingestion"
description: "accept(), middlewares, context, entity creation and update cadence"
lead: "How a ClientSample becomes entity state, and what controls when metrics are recomputed"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 321
toc: true
---

## `observer.accept(sample, context?)`

The single entry point. In order, it:

{{< steps >}}
{{< step >}}Drops the sample and emits `sample-rejected` if the observer is closed.{{< /step >}}
{{< step >}}Runs it through the [accept-middleware chain](#accept-middlewares), in registration order.{{< /step >}}
{{< step >}}Drops it and emits `sample-rejected` if `callId` or `clientId` is missing.{{< /step >}}
{{< step >}}Gets or lazily creates the `ObservedCall` and `ObservedClient`.{{< /step >}}
{{< step >}}Delegates to `client.accept(sample, context)`, which fans out to each `ObservedPeerConnection.accept(pcSample, context)`.{{< /step >}}
{{< step >}}Rolls metrics up peer connection → client → call → observer, running detectors and emitting events as it goes.{{< /step >}}
{{< /steps >}}

```text
client getStats()  ──►  ClientSample  ──►  observer.accept(sample, ctx?)
                                               │
              ┌────────────────────────────────┘
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
                                          events emitted on the Observer bus  ──►  your handlers
```

Sub-entities that stop appearing in samples are garbage-collected by a mark-and-sweep on each
`ObservedPeerConnection.accept()`, emitting the corresponding `*-removed` events.

## Accept middlewares

`observer.addAcceptMiddleware(...)` registers functions that run on **every** sample, before it
reaches any call or client. Each receives `{ sample, context }`, may mutate either, and calls
`next(payload)` to continue.

{{< callout context="caution" title="Not calling next() drops the sample" icon="alert-triangle" >}}
Nothing is created, no event fires. That is the intended way to filter. A middleware that throws is
caught and warned — the sample is dropped, `accept()` never crashes.
{{< /callout >}}

```typescript
import { Observer, AcceptMiddleware } from "@observertc/observer-js";

const observer = new Observer();

// Derive ids from the application's own attachments, before dispatch.
const route: AcceptMiddleware = ({ sample }, next) => {
    sample.callId   ??= sample.attachments?.roomId as string;
    sample.clientId ??= sample.attachments?.peerId as string;
    next({ sample });
};

// Redact anything you must not persist.
const redact: AcceptMiddleware = (payload, next) => {
    delete payload.sample.attachments?.email;
    next(payload);
};

// Drop blocklisted clients entirely.
const filter: AcceptMiddleware = (payload, next) => {
    if (blocked.has(payload.sample.clientId)) return;   // no next() ⇒ dropped
    next(payload);
};

observer.addAcceptMiddleware(route, redact, filter);
observer.removeAcceptMiddleware(route);
```

When no middleware is registered, `accept()` dispatches directly with no overhead.

## `context` vs `appData`

These are deliberately different, and confusing them is the most common integration mistake.

| | `appData` | `context` |
|---|---|---|
| Owner | The application | The application |
| Set at | Entity creation (`settings.appData` or a factory) | Every `accept()` call |
| Stored | Yes, on the entity | **No** — discarded after the update |
| Changed by the library | Never | n/a |
| Reaches | Anywhere you hold the entity | Only the `*-updated` events that this `accept()` triggers |

```typescript
type AcceptContext = Record<string, unknown>;

observer.accept(sample, { requestId, ingestNode: "eu-1", receivedAt: Date.now() });

observer.on("client-updated", ({ observedClient, sample, context }) => {
    tracing.record(context?.requestId, observedClient.clientId);
});
```

`client-updated` and `peer-connection-updated` carry the exact context of that sample.
`call-updated` carries the context of the client `accept()` that drove it, and is absent for
teardown-driven call updates.

### `appData` factories

Rather than pre-creating entities just to enrich them, register a factory once. It runs in the
entity's constructor whenever one is created without an explicit `settings.appData` — including
the lazy creation inside `accept()`.

```typescript
const observer = new Observer({
    createCallAppData:   ({ callId })                 => ({ callId, startedAt: Date.now(), region: "eu" }),
    createClientAppData: ({ clientId, observedCall }) => ({ clientId, region: observedCall.appData.region }),
});
```

The client factory receives the already-created parent call, so it can derive fields from it.

{{< callout context="note" title="attachments arrive with the first sample, not at creation" icon="info-circle" >}}
`observedClient.attachments` (things like `roomId` and `displayName` the client put on the sample)
is populated from the first `accept()`, **after** the entity was created. Read it on
`client-updated`, not in a creation-time hook.
{{< /callout >}}

## Get-or-create helpers

If you want to create and configure entities before or without samples:

```typescript
const call   = observer.getOrCreateObservedCall({ callId, appData });      // ObservedCall | undefined
const client = call?.getOrCreateObservedClient({ clientId, appData });     // ObservedClient | undefined
```

- `getOrCreate*` returns the existing instance if the id is known.
- `create*` returns the **existing** instance and warns if the id already exists.
- Both return `undefined` (and warn) when the parent is closed.

**Guard the result.** This is the library's error-handling philosophy in practice — see
[below](#error-handling).

## Automatic teardown

```typescript
const observer = new Observer({
    closeClientIfIdleForMs: 60_000,   // a client with no sample for this long auto-closes
    closeCallIfEmptyForMs: 20_000,    // a call with zero clients for this long auto-closes
});
```

Both are also settable per entity via `ObservedCallSettings.closeCallIfEmptyForMs` and
`ObservedClientSettings.closeClientIfIdleForMs`.

Closing cascades downward — call → clients → peer connections → sub-stats — unsubscribing
listeners and emitting `*-closed` and `*-removed` events. Sinks are `end()`ed, open client issues
are force-resolved with `resolvedBy: 'client-closed'`, and running validators are cancelled.

{{< callout context="tip" title="Set both" icon="rocket" >}}
Without these, a crashed participant leaves a client object alive forever and its open issues
never close, which quietly poisons every cross-client detector. The registry does expire stale
issue entries as a backstop, but idle timeouts are the real fix.
{{< /callout >}}

## When things update

"Update" means: recompute aggregated metrics, run the detectors, emit the `*-updated` event at that
level. Updates are **event-driven — there is no built-in timer.**

> A call is updated when any of its clients is updated. The observer is updated when any of its
> calls is updated.

Composed, the observer updates exactly when any client anywhere updates. Two booleans, both
defaulting to `true`, let you break a link in that chain:

| Setting | Where | Effect when `false` |
|---|---|---|
| `autoUpdateOnClientUpdate` | `ObservedCallSettings` | the call updates only when you call `call.update()` |
| `autoUpdateOnCallUpdate` | `ObserverConfig` | the observer updates only when you call `observer.update()` |

An application that wants a fixed cadence sets both to `false` and drives updates itself:

```typescript
const observer = new Observer({ autoUpdateOnCallUpdate: false });

setInterval(() => observer.update(), 5_000);
```

{{< callout context="caution" title="Observer-scoped detectors run nowhere else" icon="alert-triangle" >}}
Observer-scoped [detectors](../detectors/) and [validators](../validators/) run only inside
`observer.update()`. If you disable auto-update and never call `update()`, they never run.
{{< /callout >}}

{{< callout context="note" title="Removed in the 1.0.0 line" icon="info-circle" >}}
The `updatePolicy` / `defaultCallUpdatePolicy` enums (`'update-on-any-…'`,
`'update-when-all-…'`, `'update-on-interval'`) and the pluggable `Updater` are gone.
"Update when all clients have updated" sounds appealing and deadlocks on the first client that
stops sending — one silent participant froze the whole call's aggregation until it timed out.
{{< /callout >}}

## Error handling

The library **warns and degrades; it does not throw** on operational problems:

| Situation | Behaviour |
|---|---|
| `createObservedCall` / `createObservedClient` on a closed parent | warn, return `undefined` |
| Duplicate id | warn, return the **existing** instance |
| `accept()` on a closed client | warn, no-op |
| Sample missing `callId` / `clientId` | `sample-rejected` with `reason: 'missing-callId' \| 'missing-clientId'` |
| Observer closed | `sample-rejected` with `reason: 'observer-closed'` |
| Middleware throws | warn, drop that sample |
| Sink `write` / `end` throws | caught, surfaced on the sink's `error` event |

```typescript
observer.on("sample-rejected", ({ reason, sample }) => {
    metrics.increment("observer.sample_rejected", { reason });
    if (reason !== "observer-closed") deadLetter.write(sample);
});
```

## A worked sample

What a real first sample looks like and what `accept()` does with it. This is one participant
joining an SFU call:

```jsonc
{
  "timestamp": 1780572332518,
  "callId":   "d3dbf2f5-79be-4cb8-9d43-fb404f07ef27",
  "clientId": "c926983c-4468-4046-ae8c-a9cabe1a1868",
  "score": 0,
  "attachments": { "displayName": "Guest", "roomId": "qq0iwfnd" },

  "clientEvents": [
    { "type": "CLIENT_JOINED",                 "timestamp": 1780572324515 },
    { "type": "PEER_CONNECTION_OPENED",        "timestamp": 1780572326790 },
    { "type": "ICE_GATHERING_STATE_CHANGED",   "timestamp": 1780572326811 },
    { "type": "PEER_CONNECTION_STATE_CHANGED", "timestamp": 1780572326812 },
    { "type": "PRODUCER_ADDED",                "timestamp": 1780572326821 },
    { "type": "MEDIA_TRACK_ADDED",             "timestamp": 1780572326821 },
    { "type": "PEER_CONNECTION_STATE_CHANGED", "timestamp": 1780572326827 }
  ],

  "clientMetaItems": [
    { "type": "USER_AGENT_DATA", "payload": "{…Chrome 148 / macOS…}" },
    { "type": "MEDIA_DEVICE",    "payload": "{…\"BRIO 4K Stream Edition\"…}" }
  ],

  "peerConnections": [
    {
      "peerConnectionId": "b81c8d9d-…",
      "outboundRtps":      [ /* audio + video */ ],
      "outboundTracks":    [ /* mic + camera */ ],
      "remoteInboundRtps": [ /* RTCP feedback from the SFU */ ],
      "codecs": [], "iceTransports": [], "iceCandidatePairs": [], "dataChannels": []
    },
    { "peerConnectionId": "8635acb7-…", "peerConnectionTransports": [] }
  ]
}
```

In order, this emits: `call-added` → `client-added` → `client-joined` →
`peer-connection-added` (×2) → `outbound-track-added` and `outbound-rtp-added` per track →
`client-metadata` per device item → `client-event` per lifecycle item → `client-updated`.

Every subsequent sample is much leaner: the same ids, no new events or metadata, just refreshed
`peerConnections` stats. Those ticks refresh metrics and fire the `*-updated` events; the heavy
join snapshot happens once.
