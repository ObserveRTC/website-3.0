---
title: "The event bus"
slug: "event-bus"
description: "The complete typed event catalogue of observer-js"
lead: "Subscribe once on the Observer — every payload carries its full ancestry"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 322
toc: true
---

This is the primary API. The `Observer` is the single emitter for the entire hierarchy.
`ObservedCall`, `ObservedClient` and `ObservedPeerConnection` are `EventEmitter`s too, but those
local events are reserved for internal teardown wiring — application code belongs on the bus.

## Payload shape

Every event delivers exactly **one argument**: an object containing the ancestry from the observer
down to the entity that raised it, plus any event-specific subject.

```typescript
type ObserverEventBase           = { observer: Observer; context?: AcceptContext };
type ObservedCallScope           = ObserverEventBase   & { observedCall: ObservedCall };
type ObservedClientScope         = ObservedCallScope   & { observedClient: ObservedClient };
type ObservedPeerConnectionScope = ObservedClientScope & { observedPeerConnection: ObservedPeerConnection };
```

So a peer-connection-level event hands you everything above it as well:

```typescript
observer.on("inbound-rtp-added", ({
    observer, observedCall, observedClient, observedPeerConnection, observedInboundRtp,
}) => {
    // all five present and typed
});
```

`on` / `off` / `once` / `emit` are fully typed against the event map — the handler argument is
inferred from the event name.

## Observer level

Scope `{ observer }`.

| Event | Extra payload | Fires when |
|---|---|---|
| `observer-updated` | — | `observer.update()` ran |
| `observer-closed` | — | `observer.close()` |
| `sample-rejected` | `{ reason: 'observer-closed' \| 'missing-callId' \| 'missing-clientId', sample }` | a sample was dropped by `accept()` |
| `observer-issue` | `{ issue: ObserverIssue }` | `observer.addIssue(...)` — a cross-call / SFU-wide finding |
| `validation-ready` | `{ validator: string, report: ValidationReport }` | a [validator](../validators/) settled — once per check, not per tick |

## Call level

Scope `{ observer, observedCall }`.

| Event | Extra | Fires when |
|---|---|---|
| `call-added` | — | a call is created |
| `call-updated` | `{ context? }` | `call.update()` ran |
| `call-closed` | — | the call closed |
| `call-empty` | — | the last client left |
| `call-not-empty` | — | the first client joined a previously-empty call |
| `call-issue` | `{ issue: ObserverIssue }` | `call.addIssue(...)` — a server-side detector finding |

## Client level

Scope `{ observer, observedCall, observedClient }`.

| Event | Extra | Fires when |
|---|---|---|
| `client-added` | — | a client is created |
| `client-sink-created` | `{ sink: ClientSampleSink }` | a per-client [sink](../sinks/) was created; fires right after `client-added` |
| `client-updated` | `{ sample, elapsedTimeInMs, context? }` | the client processed a sample |
| `client-closed` | — | the client closed |
| `client-joined` | — | first `CLIENT_JOINED` event seen |
| `client-left` | — | `CLIENT_LEFT` seen, or inferred on close |
| `client-rejoined` | `{ timestamp }` | a later `CLIENT_JOINED` after an earlier join |
| `client-issue` | `{ issue: ClientIssue }` | a client-reported issue arrived, or `client.addIssue(...)` |
| `client-issue-resolved` | `{ resolvedIssue: ResolvedActiveClientIssue }` | a stateful issue ended — carries `durationInMs` and `resolvedBy` |
| `client-metadata` | `{ metaData: ClientMetaData }` | a meta item arrived |
| `client-extension-stats` | `{ extensionStats: ExtensionStat }` | an app-defined extension stat arrived |
| `client-event` | `{ event: ClientEvent }` | any client event was processed |

{{< callout context="tip" title="client-issue-resolved is the one to build on" icon="rocket" >}}
`client-issue` tells you a symptom started. `client-issue-resolved` tells you the whole episode —
what it was, how long it lasted, and who closed it (`'client'`, `'timeout'` or `'client-closed'`).
Analytics and post-call reporting should be driven from the resolution, not the raise.
{{< /callout >}}

## Peer-connection level

Scope `{ observer, observedCall, observedClient, observedPeerConnection }`.

| Event | Extra | Notes |
|---|---|---|
| `peer-connection-added` / `-closed` | — | lifecycle of the PC |
| `peer-connection-updated` | `{ context? }` | the PC processed a sample |
| `ice-connection-state-changed` | `{ state }` | driven by client events |
| `ice-gathering-state-changed` | `{ state }` | |
| `connection-state-changed` | `{ state }` | |
| `inbound-track-added` / `-updated` / `-removed` / `-muted` / `-unmuted` | `{ observedInboundTrack }` | |
| `outbound-track-added` / `-updated` / `-removed` / `-muted` / `-unmuted` | `{ observedOutboundTrack }` | |
| `inbound-rtp-added` / `-updated` / `-removed` | `{ observedInboundRtp }` | `-updated` fires every tick |
| `outbound-rtp-added` / `-updated` / `-removed` | `{ observedOutboundRtp }` | `-updated` fires every tick |
| `remote-inbound-rtp-added` / `-updated` / `-removed` | `{ observedRemoteInboundRtp }` | |
| `remote-outbound-rtp-added` / `-updated` / `-removed` | `{ observedRemoteOutboundRtp }` | |
| `data-channel-added` / `-updated` / `-removed` | `{ observedDataChannel }` | |
| `ice-candidate-added` / `-updated` / `-removed` | `{ observedIceCandidate }` | |
| `ice-candidate-pair-added` / `-updated` / `-removed` | `{ observedIceCandidatePair }` | |
| `ice-transport-added` / `-updated` / `-removed` | `{ observedIceTransport }` | |
| `codec-added` / `-updated` / `-removed` | `{ observedCodec }` | |
| `media-source-added` / `-updated` / `-removed` | `{ observedMediaSource }` | |
| `media-playout-added` / `-updated` / `-removed` | `{ observedMediaPlayout }` | |
| `peer-connection-transport-added` / `-updated` / `-removed` | `{ observedPeerConnectionTransport }` | |
| `certificate-added` / `-updated` / `-removed` | `{ observedCertificate }` | |

{{< callout context="caution" title="Volume" icon="alert-triangle" >}}
The sub-stat `*-updated` events fire on **every peer-connection `accept()`, per stream**. At a
thousand participants that is tens of thousands of handler invocations per sampling period.

For high-throughput servers, subscribe only to what you need, or read fields off the entities on
`client-updated` / `call-updated` instead — one event per client per tick, with the whole tree
reachable from it.
{{< /callout >}}

## mediasoup level

Scope `{ observer, observedMediasoupRouter }`. See [SFU integration](../sfu/).

| Event | Extra | Fires when |
|---|---|---|
| `mediasoup-router-added` | — | `observer.createObservedMediasoupRouter(...)` registered a router |
| `mediasoup-router-matched-with-peer-connection` | `{ observedCall, observedClient, observedPeerConnection }` | a peer connection's id matched one of the router's WebRTC transport ids. **Opt-in** via `matchPeerConnectionByWebRtcTransportId: true` |
| `mediasoup-router-removed` | — | the underlying mediasoup router closed |

## Local lifecycle events

These stay on the individual entities, for teardown and coordination. You may listen to them, but
prefer the bus for application logic.

| Entity | Local events |
|---|---|
| `ObservedCall` | `update`, `newclient`, `empty`, `not-empty`, `close` |
| `ObservedClient` | `update` (`sample`, `elapsedTimeInMs`), `close`, `joined`, `left` |
| `ObservedPeerConnection` | `removed-inbound-track`, `removed-outbound-track`, `close` |

## Choosing a subscription strategy

{{< tabs "strategy" >}}
{{< tab "Low volume" >}}
Subscribe to what you need directly. Fine for hundreds of clients.

```typescript
observer.on("peer-connection-updated", ({ observedPeerConnection, observedClient }) => {
    metrics.gauge("rtt_ms", observedPeerConnection.currentRttInMs, { client: observedClient.clientId });
});
```
{{< /tab >}}
{{< tab "High volume" >}}
One event per client per tick; walk the tree yourself and emit only what you export.

```typescript
observer.on("client-updated", ({ observedClient }) => {
    let worstRtt = 0;
    for (const pc of observedClient.observedPeerConnections.values()) {
        worstRtt = Math.max(worstRtt, pc.currentRttInMs ?? 0);
    }
    metrics.gauge("client_worst_rtt_ms", worstRtt, { client: observedClient.clientId });
});
```
{{< /tab >}}
{{< tab "Incident-only" >}}
Ignore the metric firehose entirely and react to findings.

```typescript
observer.on("client-issue-resolved", ({ observedCall, observedClient, resolvedIssue }) => {
    incidents.record({
        callId: observedCall.callId,
        clientId: observedClient.clientId,
        type: resolvedIssue.type,
        durationInMs: resolvedIssue.durationInMs,
        resolvedBy: resolvedIssue.resolvedBy,
    });
});

observer.on("call-issue",     ({ issue }) => alerting.page(issue));
observer.on("observer-issue", ({ issue }) => alerting.page(issue));
```
{{< /tab >}}
{{< /tabs >}}
