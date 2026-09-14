---
title: "The event bus"
description: "The complete typed event catalogue and payload shapes"
lead: "Subscribe once on the Observer — every payload carries the ancestry from the observer down to the entity that raised it"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 320
toc: true
---

This is the primary API. **Subscribe on the `Observer` instance** — it is the single emitter for the
entire hierarchy. The `ObservedCall` / `ObservedClient` / `ObservedPeerConnection` objects are
`EventEmitter`s too, but those local events are reserved for internal lifecycle wiring; application
code uses the observer bus.

## Payload shape: ancestry + subject

Every event delivers exactly **one argument: a payload object**, always containing the ancestry from
the observer down to the entity that raised it, plus the event-specific subject.

```typescript
type ObserverEventBase           = { observer: Observer, context?: AcceptContext };
type ObservedCallScope           = ObserverEventBase   & { observedCall: ObservedCall };
type ObservedClientScope         = ObservedCallScope   & { observedClient: ObservedClient };
type ObservedPeerConnectionScope = ObservedClientScope & { observedPeerConnection: ObservedPeerConnection };
```

```typescript
observer.on('inbound-rtp-added', ({ observer, observedCall, observedClient, observedPeerConnection, observedInboundRtp }) => {
    // all five are present and correctly typed
});
```

`on` / `off` / `once` / `emit` are fully typed against the event map — the handler argument is
inferred from the event name. **You never walk the tree to attach a listener.**

## Observer level — scope `{ observer }`

| Event | Extra payload | Fires when |
|---|---|---|
| `observer-updated` | — | `observer.update()` ran |
| `observer-closed` | — | `observer.close()` |
| `sample-rejected` | `{ reason: 'observer-closed' \| 'missing-callId' \| 'missing-clientId', sample }` | a sample was dropped by `accept()` |
| `observer-issue` | `{ issue: ObserverIssue }` | `observer.addIssue(…)` — a cross-call / SFU-wide finding |
| `validation-ready` | `{ validator: string, report: ValidationReport }` | a [validator](../validators/) settled — **once per check**, not per tick |

## Mediasoup level — scope `{ observer, observedMediasoupRouter }`

| Event | Extra | Fires when |
|---|---|---|
| `mediasoup-router-added` | — | `observer.createObservedMediasoupRouter(…)` registered a router |
| `mediasoup-router-matched-with-peer-connection` | `{ observedCall, observedClient, observedPeerConnection }` | a newly added peer connection's id matched one of the router's WebRTC transport ids. **Opt-in** via `matchPeerConnectionByWebRtcTransportId: true` |
| `mediasoup-router-removed` | — | the underlying mediasoup router closed |

## Call level — scope `{ observer, observedCall }`

| Event | Extra | Fires when |
|---|---|---|
| `call-added` | — | a call is created |
| `call-updated` | `{ context? }` | `call.update()` ran |
| `call-closed` | — | the call closed |
| `call-empty` | — | the last client left |
| `call-not-empty` | — | the first client joined a previously-empty call |
| `call-issue` | `{ issue: CallIssue }` | `call.addIssue(…)` — a server-side detector finding |
| `call-summary` | `{ summary: CallSummary }` | the call is closing and a [summary](../call-summaries/) was configured. Emitted **inside** `close()`, while the call is still reachable |

## Client level — scope `{ observer, observedCall, observedClient }`

| Event | Extra | Fires when |
|---|---|---|
| `client-added` | — | a client is created |
| `client-sink-created` | `{ sink: ClientSampleSink }` | a per-client [sink](../sinks/) was created; fires right after `client-added` |
| `client-updated` | `{ sample, elapsedTimeInMs, context? }` | the client processed a sample |
| `client-closed` | — | the client closed |
| `client-joined` | — | the first `CLIENT_JOINED` event was seen |
| `client-left` | — | `CLIENT_LEFT` seen, or inferred on close |
| `client-rejoined` | `{ timestamp }` | a later `CLIENT_JOINED` after an earlier join |
| `client-issue` | `{ issue: ClientIssue }` | a client-reported issue arrived, or `client.addIssue(…)`. A keyed issue also opens an entry in `observedClient.activeIssues` |
| `client-issue-resolved` | `{ resolvedIssue: ResolvedActiveClientIssue }` | a stateful issue ended. Carries the finished interval — `durationInMs`, `resolvedBy` |
| `client-metadata` | `{ metaData: ClientMetaData }` | a client meta item arrived |
| `client-extension-stats` | `{ extensionStats: ExtensionStat }` | an app-defined extension stat arrived |
| `client-event` | `{ event: ClientEvent }` | any client event was processed |

## Peer-connection level

Scope `{ observer, observedCall, observedClient, observedPeerConnection }`.

| Event | Extra | Notes |
|---|---|---|
| `peer-connection-added` / `-closed` | — | lifecycle of the PC |
| `peer-connection-updated` | `{ context? }` | the PC processed a sample |
| `ice-connection-state-changed` / `ice-gathering-state-changed` / `connection-state-changed` | `{ state: string }` | driven by client events |
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
The `*-updated` sub-stat events fire on **every peer-connection `accept()`** — per sample, per
stream. On a high-throughput server, subscribe only to what you need, or read fields off the
entities on `client-updated` / `call-updated` instead.
{{< /callout >}}

## Local lifecycle events

These remain on the individual entities rather than the bus, for teardown and coordination. You can
listen to them, but prefer the bus equivalents for application logic.

| Entity | Local events |
|---|---|
| `ObservedCall` | `update`, `newclient`, `empty`, `not-empty`, `close` |
| `ObservedClient` | `update` (`sample`, `elapsedTimeInMs`), `close`, `joined`, `left` |
| `ObservedPeerConnection` | `removed-inbound-track`, `removed-outbound-track`, `close` |

## Client issues: the lifecycle on the wire

From `client-monitor-js` 4.6.0 a stateful issue arrives as two `clientIssues[]` entries sharing a
`key`:

```text
raise:      { type: 'stuck-decoder',          key, payload,                                timestamp: raisedAt }
resolution: { type: 'stuck-decoder-resolved', key, payload: { raisedAt, comment, …final }, timestamp: resolvedAt }
```

The observer opens an entry in `observedClient.activeIssues` on the raise and closes it on the
matching key. Handled for you:

- the `-resolved` **suffix is stripped**, so both entries share one logical `type`;
- a **re-raise** of a live key refreshes the payload without restarting `raisedAt`;
- **keyless** entries are one-shot — reported via `client-issue`, never tracked;
- issues still open when a client closes are **force-resolved** (`resolvedBy: 'client-closed'`), and
  the registry expires stale entries.

```typescript
observer.on('client-issue', ({ observedClient, issue }) => { /* opened, or one-shot */ });

observer.on('client-issue-resolved', ({ resolvedIssue }) => {
    resolvedIssue.type;          // 'stuck-decoder' — suffix stripped
    resolvedIssue.durationInMs;  // how long the episode lasted
    resolvedIssue.resolvedBy;    // 'client' | 'timeout' | 'client-closed'
});

observedClient.activeIssues;     // the live per-client mirror, keyed by issue.key
```

{{< callout context="tip" title="Why intervals beat windows" icon="rocket" >}}
*"Several clients reported congestion in the last 10 seconds"* is a heuristic that has to guess
whether the symptoms are still happening. *"Several clients are congested **right now,
simultaneously**"* is ground truth, because the client says when the episode ends. Overlapping
intervals are far stronger evidence of a shared cause than near-in-time reports.
{{< /callout >}}

## Payload types on the wire

```typescript
type ClientEvent    = { type: string; payload?: Record<string, unknown>; timestamp?: number };
type ClientIssue    = { type: string; payload?: Record<string, unknown>; key?: string; timestamp?: number };
type ClientMetaData = { type: string; payload?: Record<string, unknown>; timestamp?: number };
type ExtensionStat  = { type: string; payload?: Record<string, unknown> };
```

`payload` fields are objects (schema **3.7.0**: free-form JSON, so a payload may nest objects and
arrays), and the library reads the ones it understands. **Older clients keep working**: a payload
from a pre-3.5.0 client arrives as a JSON string and is parsed on the way in, so a fleet running a
mix of client versions needs no coordination. Values inside a payload are `unknown`, so narrow
before use:

```typescript
if (typeof issue.payload?.trackId === 'string') { /* … */ }
```

**`ClientEventTypes`** (known `event.type` values): `CLIENT_JOINED`, `CLIENT_LEFT`,
`PEER_CONNECTION_OPENED` / `CLOSED` / `STATE_CHANGED`, `MEDIA_TRACK_ADDED` / `REMOVED` / `MUTED` /
`UNMUTED` / `RESUMED`, `ICE_GATHERING_STATE_CHANGED`, `ICE_CONNECTION_STATE_CHANGED`,
`DATA_CHANNEL_OPEN` / `CLOSED` / `ERROR`, `NEGOTIATION_NEEDED`, `SIGNALING_STATE_CHANGE`,
`ICE_CANDIDATE`, `ICE_CANDIDATE_ERROR`, and the mediasoup set `PRODUCER_*` / `CONSUMER_*` /
`DATA_PRODUCER_*` / `DATA_CONSUMER_*`.

**`ClientMetaTypes`**: `MEDIA_CONSTRAINT`, `MEDIA_DEVICE`, `MEDIA_DEVICES_SUPPORTED_CONSTRAINTS`,
`USER_MEDIA_ERROR`, `LOCAL_SDP`, `OPERATION_SYSTEM`, `ENGINE`, `PLATFORM`, `BROWSER`.

## A worked sample

Two consecutive samples from one participant of a mediasoup call show what actually flows through
`accept()`: a rich **join snapshot**, then lean **steady-state ticks**.

```jsonc
{
  "timestamp": 1780572332518,
  "callId":   "d3dbf2f5-…",
  "clientId": "c926983c-…",
  "score": 0,                                       // no quality measured yet on the join tick
  "attachments": { "displayName": "Guest", "roomId": "qq0iwfnd" },

  "clientEvents": [                                 // chronological lifecycle
    { "type": "CLIENT_JOINED",                 "timestamp": 1780572324515 },
    { "type": "PEER_CONNECTION_OPENED",        "timestamp": 1780572326790 },
    { "type": "ICE_GATHERING_STATE_CHANGED",   "timestamp": 1780572326811 },
    { "type": "PRODUCER_ADDED",                "timestamp": 1780572326821 },
    { "type": "MEDIA_TRACK_ADDED",             "timestamp": 1780572326821 }
  ],

  "clientMetaItems": [                              // environment & devices, one-off
    { "type": "USER_AGENT_DATA", "payload": { "…": "Chrome 148 / macOS" } },
    { "type": "MEDIA_DEVICE",    "payload": { "label": "BRIO 4K Stream Edition" } }
  ],

  "peerConnections": [
    { "peerConnectionId": "b81c8d9d-…", "outboundRtps": [ /* … */ ], "outboundTracks": [ /* … */ ] },
    { "peerConnectionId": "8635acb7-…", "peerConnectionTransports": [ /* … */ ] }
  ]
}
```

What `accept()` does with it, each step emitting on the bus with full ancestry:

{{< steps >}}
{{< step >}}lazily creates the `ObservedCall` → **`call-added`**;{{< /step >}}
{{< step >}}creates the `ObservedClient` → **`client-added`**, then **`client-joined`**;{{< /step >}}
{{< step >}}creates an `ObservedPeerConnection` per entry → **`peer-connection-added`** (×2 here);{{< /step >}}
{{< step >}}creates an `ObservedOutboundTrack` per track → **`outbound-track-added`**, plus the matching **`outbound-rtp-added`**;{{< /step >}}
{{< step >}}replays the device list as **`client-metadata`** and the lifecycle items as **`client-event`**, and finally emits **`client-updated`** for the whole tick.{{< /step >}}
{{< /steps >}}

`attachments.roomId` lands on `observedClient.attachments` — read it on `client-updated`, **not** at
creation.

The second sample, ~8 s later, carries the same ids, **no** new `clientEvents` or `clientMetaItems`,
and just refreshed stats. That is the shape of nearly every sample: the heavy join snapshot happens
once.
