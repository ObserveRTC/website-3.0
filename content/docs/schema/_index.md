---
title: "Schema"
description: "The ObserveRTC schema — versioned, strongly typed monitoring data"
lead: "One contract shared by every ObserveRTC component, generated from Avro into TypeScript, protobuf and documentation"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 200
toc: true
---

The schema is the interface between everything in ObserveRTC. A client-side monitor produces a
[`ClientSample`](./clientsample/); a server-side observer consumes one; a storage layer persists
one. Because all three agree on the shape, none of them needs to know about the others.

**Current version: `3.3.0`** — see the [version history](./versions/) for what changed since
`3.0.0`.

## What it is, concretely

Avro schema files in `sources/samples/` are the single source of truth. A TypeScript generator
reads them and emits everything else:

| Output | Where it goes | Used by |
|---|---|---|
| TypeScript type definitions | `outputs/typescript/`, `@observertc/schemas` | Application code, both libraries |
| Protocol Buffers | `outputs/proto/` | Binary transport |
| Flattened Avro | `outputs/avsc/` | Schema registries, other languages |
| Markdown reference | `schemaList.md` | Documentation |
| Binary encoder | `@observertc/samples-encoder` | Browsers, before upload |
| Binary decoder | `@observertc/samples-decoder` | Servers, on ingest |

All three npm packages are versioned **in lockstep** with the schema version.

## Why a shared schema at all

{{< callout context="tip" title="The practical payoff" icon="rocket" >}}
Without a shared schema, every integration point is a private agreement: the client and the backend
negotiate a JSON shape, the backend and the warehouse negotiate a table, and each of them drifts
independently. Adding one WebRTC field means touching all of them.

With one, adding a field is a minor schema release, and the type definitions, protobuf encoding,
documentation and both libraries update from the same edit.
{{< /callout >}}

## The shape

```text
ClientSample
├─ timestamp, callId, clientId, score, scoreReasons, attachments
├─ peerConnections[]  (PeerConnectionSample)
│   └─ fifteen arrays mirroring the W3C getStats() dictionaries
├─ clientEvents[]      — things that happened
├─ clientIssues[]      — problem states, raised and resolved
├─ clientMetaItems[]   — devices, browser, OS, SDP
└─ extensionStats[]    — your own application metrics
```

Three conventions run through every record:

- **`timestamp` + `id`** — collection time and the browser's own identifier, so records correlate
  across samples.
- **`attachments`** — a free-form slot on every record. This is how an SSRC becomes "Alice's screen
  share", and how a server can link a publisher to its subscribers.
- **`score` + `scoreReasons`** — computed 0–5 quality with a machine-readable breakdown, at client,
  peer connection and track level.

## Installation

```bash
npm install @observertc/schemas
```

```typescript
import { ClientSample, PeerConnectionSample, schemaVersion } from "@observertc/schemas";

console.log(schemaVersion);   // "3.3.0"
```

Both libraries re-export these types, so you usually do not need the package directly:

```typescript
import { ClientSample } from "@observertc/observer-js";
```

## Binary transport

```bash
npm install @observertc/samples-encoder    # client side
npm install @observertc/samples-decoder    # server side
```

```typescript
// Browser — one encoder per client, kept for the life of the stream.
import { ClientSampleEncoder } from "@observertc/samples-encoder";

const encoder = new ClientSampleEncoder(clientId);

await fetch(`/api/samples/${clientId}`, {
    method: "POST",
    headers: { "Content-Type": "application/octet-stream" },
    body: encoder.encodeToBytes(sample),
});
```

```typescript
// Server — one decoder per client stream, fed in order.
import { ClientSampleDecoder } from "@observertc/samples-decoder";

const decoder = new ClientSampleDecoder();

const sample = decoder.decodeFromBytes(bytes);
if (sample) observer.accept(sample);
```

{{< callout context="caution" title="Both sides are stateful" icon="alert-triangle" >}}
The encoder elides values that have not changed since the previous sample, so **one encoder per
client** and **one decoder per client stream, fed in order**. A shared or restarted decoder does
not throw — it produces samples with missing ids. See
[samples-encoder](/docs/libraries/sample-encoder-js/).
{{< /callout >}}

{{< callout context="caution" title="Keep encoder and decoder on the same version" icon="alert-triangle" >}}
Protobuf field numbers are derived from field order, so inserting a field anywhere but the end of
its group renumbers everything after it. A decoder built against an older schema can misread a
newer sample without erroring. See [3.3.0](./versions/v3-3-0/) for a concrete case.
{{< /callout >}}

## Sections

{{< card-grid >}}
{{< link-card title="ClientSample reference" description="Every record and every field, generated from the 3.3.0 sources." href="./clientsample/" >}}
{{< link-card title="Version history" description="What changed in 3.1.0, 3.2.0 and 3.3.0, field by field." href="./versions/" >}}
{{< link-card title="Code generation & versioning" description="How the generator works, what it emits, and the versioning rules." href="./general/" >}}
{{< /card-grid >}}

## Repository

[github.com/observertc/schemas](https://github.com/observertc/schemas)
