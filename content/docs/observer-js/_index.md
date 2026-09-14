---
title: "Observer"
linkTitle: "Observer"
description: "observer-js — server-side WebRTC session monitoring for Node.js"
lead: "Feed it getStats() snapshots and get back a live, queryable model of every call — plus one typed event stream to react to"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 300
toc: true
---

`@observertc/observer-js` is the server half of ObserveRTC. A WebRTC application — typically an SFU
or a stats backend — feeds it [`ClientSample`](/docs/schema/clientsample/) objects, and it maintains
an in-memory model of every call, participant, peer connection and media stream, derives
per-interval and cumulative metrics, and emits a single unified stream of typed events.

It answers the questions a browser structurally cannot: *who else is in this state right now, what
do they have in common, and where in publisher → SFU → subscriber does the fault begin?*

{{< callout context="note" title="Current version — 1.0.0" icon="info-circle" >}}
**`1.0.0` is the first stable release**, and the API described here follows semver from now on: a
breaking change means a 2.0.0. Node.js **≥ 22**, dual ESM + CommonJS from a single entry point.

Coming from a beta? Several things are gone rather than deprecated: the `updatePolicy` enum and the
pluggable `Updater`, detector configuration in `ObserverConfig`, auto-created detectors, and the
per-detector `registry` option. `ObservedInboundRtp.bitrate` is now **bits per second** (it was
1000× smaller than its outbound twin). See [what changed in 1.0](./migration-1-0/).
{{< /callout >}}

## Install

```bash
npm install @observertc/observer-js
```

```typescript
import { Observer, ClientSample, createJsonlFileSinkFactory } from "@observertc/observer-js";
```

The same import line works in ESM and CommonJS projects — in ESM it resolves to the `.mjs` build, in
CommonJS to the `.js` build, with type declarations for both.

Runtime dependencies: `@bufbuild/protobuf`, `events`, `uuid`. `mediasoup` is an **optional peer
dependency** (`>=3.11.0`), needed only for [router observation](./sfu/#mediasoup-router-observation).
No logger and no transport are bundled. This release ships `ClientSample` schema **3.7.0**.

## Sixty-second start

```typescript
import { Observer, ClientSample } from "@observertc/observer-js";

const observer = new Observer({
    closeCallIfEmptyForMs: 20_000,
    closeClientIfIdleForMs: 60_000,
});

// One bus. Every payload carries its full ancestry.
observer.on("call-added", ({ observedCall }) => {
    console.log("new call", observedCall.callId);
});

observer.on("client-issue", ({ observedClient, issue }) => {
    console.warn(`[${observedClient.clientId}] ${issue.type}`, issue.payload);
});

observer.on("client-issue-resolved", ({ resolvedIssue }) => {
    console.info(resolvedIssue.type, "lasted", resolvedIssue.durationInMs, "ms");
});

observer.on("peer-connection-updated", ({ observedClient, observedPeerConnection }) => {
    metrics.gauge("rtt_ms", observedPeerConnection.currentRttInMs, {
        client: observedClient.clientId,
    });
});

observer.on("sample-rejected", ({ reason }) => console.warn("dropped a sample:", reason));

// One ingestion method.
function onClientStats(sample: ClientSample) {
    observer.accept(sample, { studioVersion: "1.2.3" });
}

process.on("SIGINT", () => observer.close());
```

Entities are created lazily by id — you never pre-create a call or a client.

## The five ideas

{{< callout context="tip" title="If you read nothing else" icon="rocket" >}}
**One ingestion method. One event bus. Lazy entities. Warn, don't throw. Nothing implicit.**
Everything below is an elaboration of those five.
{{< /callout >}}

### 1. One ingestion method

```typescript
observer.accept(sample, context?);
```

`accept()` runs the global middleware chain, gets or creates the call and the client by id, fans the
sample out to each peer connection, updates every derived metric, runs detectors, and emits. There
is no second entry point, no queue to drain, and **no timer inside the library**.

### 2. One event bus

Subscribe on the `Observer`. Every payload is a single object carrying the ancestry from the
observer down to the entity that raised the event:

```typescript
observer.on("inbound-rtp-added", ({ observer, observedCall, observedClient, observedPeerConnection, observedInboundRtp }) => {
    // all five, correctly typed
});
```

You never walk the tree to attach a listener. [The event bus →](./event-bus/)

### 3. Lazy entities

```text
Observer
└── ObservedCall
    └── ObservedClient
        └── ObservedPeerConnection
            ├── ObservedInboundRtp / ObservedOutboundRtp
            ├── ObservedInboundTrack / ObservedOutboundTrack
            ├── ObservedRemoteInboundRtp / ObservedRemoteOutboundRtp
            ├── ObservedIceTransport / ObservedIceCandidate / ObservedIceCandidatePair
            ├── ObservedCodec / ObservedMediaSource / ObservedMediaPlayout
            ├── ObservedDataChannel / ObservedCertificate
            └── ObservedPeerConnectionTransport
```

Every node is created the first time it appears in a sample and garbage-collected when it stops
appearing. Entities that go idle auto-close on a timeout you configure. [Entities & API →](./entities/)

### 4. Warn, don't throw

Operational problems degrade rather than crash: `create*` returns `T | undefined`, a malformed
sample emits `sample-rejected`, a throwing middleware drops that one sample. **Guard the result of
`create*` / `getOrCreate*`.**

### 5. Nothing implicit

A `new Observer()` has **zero detectors**. There is no default detector set and no detector
configuration in `ObserverConfig` — an application says what it wants to watch, or it watches
nothing. A detector nobody asked for is a detector nobody will act on. [Detectors →](./detectors/)

## What the server sees that a client cannot

This is the whole reason the library exists. A client running
[`client-monitor-js`](/docs/client-monitor-js/) already decides *what is wrong with that endpoint*,
with hysteresis and multi-signal confirmation behind every verdict.

> **If a condition is detectable on the client, the client's issue is the source of truth.**

**`observer-js` does not repeat that work.** It correlates across participants:

{{< card-grid >}}
{{< link-card
  title="Is it the room or the person?"
  description="Several participants congested at the same moment is a different incident from one person's Wi-Fi — and only the server can tell them apart."
  href="./detectors/" >}}
{{< link-card
  title="Is it the publisher or the receiver?"
  description="Join a published track to every subscriber of it. If all of them see a freeze, the source or the forwarding path is at fault; if one does, it is that consumer."
  href="./sfu/" >}}
{{< link-card
  title="Is it our infrastructure?"
  description="The same symptom across independent calls shares no room, no publisher and no host — only the servers. That makes the finding conclusive."
  href="./detectors/" >}}
{{< link-card
  title="Is our deployment built correctly?"
  description="One-shot validators answer structural questions: does the SFU adapt layers per receiver, is everyone on the codec you think you negotiated."
  href="./validators/" >}}
{{< /card-grid >}}

### Issues arrive as intervals, not point-in-time reports

From `client-monitor-js` 4.6.0 the whole issue lifecycle reaches the server: a stateful issue arrives
as two `clientIssues[]` entries sharing a `key` — the raise, and a `<type>-resolved` companion. The
observer pairs them and emits `client-issue-resolved` with `durationInMs` and `resolvedBy`.

That turns *"several clients reported congestion in the last 10 seconds"* — a heuristic that has to
guess whether the symptoms are still happening — into *"several clients are congested **right now,
simultaneously**"*, which is ground truth. **Overlapping intervals are much stronger evidence of a
shared cause than near-in-time reports.**

## Extension points

| Point | What it does |
|---|---|
| **Accept middlewares** | Inspect, mutate or drop every sample before dispatch — route ids, redact, filter |
| **Detectors** | Cross-client and cross-call detection raising `call-issue` / `observer-issue` |
| **Validators** | One-shot structural checks that report once and remove themselves |
| **Call summaries** | The one record that outlives a call — who was in it, what was raised, how it scored |
| **Sinks** | Per-client persistence of every accepted sample (JSONL, in-memory, or your own) |
| **`RemoteTrackResolver`** | Publisher ↔ subscriber track correlation for any SFU topology |
| **mediasoup router observation** | The server's own ground truth, independent of client samples |
| **Injection API** | Merge application events, issues, metadata and attachments into a client's sample stream |
| **`appData` factories** | Populate application data at entity creation, with the accept context available |
| **Logger** | Route the library's logs into pino, winston, or nothing |

## Documentation map

{{< card-grid >}}
{{< link-card title="What changed in 1.0" description="Every break since the betas, and the migration for each." href="./migration-1-0/" >}}
{{< link-card title="Ingestion & lifecycle" description="accept(), middlewares, context vs appData, teardown, and when things update." href="./ingestion/" >}}
{{< link-card title="The event bus" description="The complete typed event catalogue and payload shapes." href="./event-bus/" >}}
{{< link-card title="Entities & API reference" description="Observer, call, client, peer connection — members, metrics and methods." href="./entities/" >}}
{{< link-card title="Detectors" description="The ten built-ins, the issue registry, conclusions, and writing your own." href="./detectors/" >}}
{{< link-card title="Validators" description="One-shot structural checks for simulcast, resolver wiring and codec consistency." href="./validators/" >}}
{{< link-card title="Call summaries" description="The record that outlives the call, and why it is configured at construction." href="./call-summaries/" >}}
{{< link-card title="SFU integration" description="Remote track resolution and mediasoup router observation." href="./sfu/" >}}
{{< link-card title="Sinks & injection" description="Persisting samples per client, injecting app data, and logging." href="./sinks/" >}}
{{< link-card title="Recipes" description="End-to-end patterns: HTTP ingestion, alerting, dashboards, archival." href="./recipes/" >}}
{{< /card-grid >}}

## Resources

- [npm package](https://www.npmjs.com/package/@observertc/observer-js)
- [GitHub repository](https://github.com/ObserveRTC/observer-js)
- [Client-side library](/docs/client-monitor-js/)
- [Schema definitions](/docs/schema/)
