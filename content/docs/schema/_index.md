---
title: "Schema"
description: "The ObserveRTC schema — versioned, strongly typed monitoring data"
lead: "One contract shared by every ObserveRTC component, generated from Avro into TypeScript, protobuf and documentation"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 600
toc: true
---

The schema is the interface between everything in ObserveRTC. A client-side monitor produces a
[`ClientSample`](./clientsample/); a server-side observer consumes one; a storage layer persists
one. Because all three agree on the shape, none of them needs to know about the others.

**Current version: `3.7.0`** — see the [version history](./versions/) for what changed since
`3.0.0`.

## What it is, concretely

Avro schema files in `sources/samples/` are the single source of truth. A TypeScript generator reads
them and emits everything else:

| Output | Where it goes | Used by |
|---|---|---|
| TypeScript type definitions | `outputs/typescript/`, the sample-schemas package | Application code, both libraries |
| Protocol Buffers | `outputs/proto/` | The protobuf codec |
| Flattened Avro | `outputs/avsc/` | Schema registries, other languages |
| Markdown reference | `schemaList.md` | [This documentation](./clientsample/) |
| [Protobuf delta codec](/docs/samples-protobuf-codec/) | `@observertc/samples-protobuf-codec` | Browsers and servers, both directions |
| [JSON delta codec](/docs/samples-json-codec/) | `@observertc/samples-json-codec` | The same, zero-dependency |

Both codec packages are versioned **in lockstep** with the schema by the generator, so a package
version *is* the schema version it speaks. Each exports `schemaVersion` so a deployment can assert
that at runtime, and so do
[`client-monitor-js`](/docs/client-monitor-js/) (`ClientMonitor.samplingSchemaVersion`) and
[`observer-js`](/docs/observer-js/).

{{< callout context="caution" title="samples-encoder and samples-decoder are deprecated" icon="alert-triangle" >}}
They were the same codec split across two published artefacts, they stopped at `3.3.0`, and they
have been removed from the repository — they will not be regenerated, versioned or published again.

`3.3.0` stays installable from npm and its wire format is unchanged, so either package still
interoperates with `@observertc/samples-protobuf-codec` and **the two ends of a stream can migrate
independently.**
{{< /callout >}}

## Why a shared schema at all

{{< callout context="tip" title="The practical payoff" icon="rocket" >}}
Without a shared schema, every integration point is a private agreement: the client and the backend
negotiate a JSON shape, the backend and the warehouse negotiate a table, and each of them drifts
independently. Adding one WebRTC field means touching all of them.

With one, adding a field is a minor schema release, and the type definitions, protobuf encoding,
documentation, both codecs and both libraries update from the same edit.
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
  peer connection and track level. Since **3.6.0** `scoreReasons` is a `Record<string, number>`
  mapping each reason to how much it took off, rather than a list of labels.

## Payloads, and the three generations still on the wire

`ClientEvent.payload`, `ClientIssue.payload`, `ClientMetaData.payload` and `ExtensionStat.payload`
have been through three shapes, and a fleet is never on one client version:

| Generation | Payload shape |
|---|---|
| pre-3.5.0 | A pre-serialised JSON **string** |
| 3.5.0 – 3.6.0 | A flat record of primitives |
| **3.7.0** | Free-form JSON — a payload may nest objects and arrays |

`observer-js` passes an object through untouched and parses a string, so **nothing has to move in
step**. What 3.7.0 asks of a reader is narrowing: a payload value is `unknown`, so
`typeof payload.trackId === 'string'` replaces a bare read.

## Binary and JSON transport

```bash
npm install @observertc/samples-protobuf-codec   # smallest payload
npm install @observertc/samples-json-codec       # zero dependencies, ~2 KB, readable
```

```typescript
// Browser — one encoder per client, kept for the life of the stream.
import { ClientSampleEncoder } from '@observertc/samples-protobuf-codec';

const encoder = new ClientSampleEncoder({ clientId });
websocket.send(encoder.encode(sample));
```

```typescript
// Server — one decoder per client stream, fed in order.
import { ClientSampleDecoder } from '@observertc/samples-protobuf-codec';

const decoder = new ClientSampleDecoder();
observer.accept(decoder.decode(bytes));
```

{{< callout context="caution" title="Both codecs are delta codecs, and therefore stateful" icon="alert-triangle" >}}
Each message carries only what changed since the previous sample. So: **one encoder per client, one
decoder per client stream, fed in order**, over an ordered lossless transport. A decoder that has not
seen enough of the stream raises `STREAM_DESYNC` rather than handing back an object with missing ids,
and `reset()` on both halves is a keyframe.
{{< /callout >}}

## How versioning works

| Change type | Version bump | Compatibility |
|---|---|---|
| Field addition at the end of its group | Minor | Additive; older decoders ignore it |
| Field addition **elsewhere** in its group | Minor | ⚠️ renumbers protobuf fields after it |
| Field type change | Minor or major, depending on the wire | Producers and consumers should move together |
| Field removal | Major | Breaking |
| Documentation | Patch | Non-breaking |

{{< callout context="caution" title="Protobuf field numbers come from field order" icon="alert-triangle" >}}
The generator sorts fields — repeated, then required, then optional, each sorted by name — and
assigns protobuf numbers from that order. **Inserting a field anywhere but the end of its group
renumbers every field after it**, which breaks the wire format for decoders built against the older
schema. That is why `3.3.0` carries a wire-format warning despite adding only one field.
{{< /callout >}}

## Sections

{{< card-grid >}}
{{< link-card title="ClientSample reference" description="Every record and every field, generated from the 3.7.0 sources." href="./clientsample/" >}}
{{< link-card title="Version history" description="What changed in each release since 3.0.0, field by field." href="./versions/" >}}
{{< link-card title="Code generation & versioning" description="How the generator works, what it emits, and the versioning rules." href="./general/" >}}
{{< /card-grid >}}

## Repository

[github.com/observertc/schemas](https://github.com/observertc/schemas)
