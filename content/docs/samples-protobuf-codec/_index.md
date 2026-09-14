---
title: "Protobuf Codec"
linkTitle: "Protobuf Codec"
description: "samples-protobuf-codec — protobuf delta codec for ObserveRTC ClientSamples"
lead: "Each message carries only the difference from the sample before it — which is where nearly all of the saving comes from"
date: 2026-09-13T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 400
toc: true
---

`@observertc/samples-protobuf-codec` encodes and decodes
[`ClientSample`](/docs/schema/clientsample/) objects over protobuf. It is a **delta** codec: each
message on the wire carries the difference between one sample and the one before it, because a
WebRTC stats sample is mostly identifiers, codec parameters and slow-moving counters that repeat
verbatim every tick.

{{< callout context="caution" title="This replaces samples-encoder and samples-decoder" icon="alert-triangle" >}}
`@observertc/samples-encoder` and `@observertc/samples-decoder` were the same codec split across two
published artefacts. They are **deprecated and removed from the schema repository**: they stopped at
`3.3.0` and will not be regenerated, versioned or published again.

Version `3.3.0` stays installable from npm — removing the sources is not an unpublish — and the wire
format is unchanged, so either package still interoperates with this one and **the two ends of a
stream can migrate independently**. See [migrating from the encoder / decoder
pair](#migrating-from-samples-encoder--samples-decoder).
{{< /callout >}}

## Install

```bash
npm install @observertc/samples-protobuf-codec
```

Ships both ESM and CommonJS builds with full type declarations. Node ≥ 20, and any modern browser —
nothing here touches `Buffer` or other Node built-ins, so it runs in the browser that produces the
samples.

It is generated in lockstep with the [schema](/docs/schema/), so the package version **is** the
schema version it speaks. `schemaVersion` is exported for asserting that at runtime.

## Usage

### Encoding, on the client

```typescript
import { ClientSampleEncoder } from '@observertc/samples-protobuf-codec';

const encoder = new ClientSampleEncoder({ clientId });

monitor.on('sample-created', ({ sample }) => {
    websocket.send(encoder.encode(sample));      // Uint8Array
});
```

For a text-only transport there is `encodeToBase64(sample)`.

### Decoding, on the server

```typescript
import { ClientSampleDecoder } from '@observertc/samples-protobuf-codec';

const decoder = new ClientSampleDecoder();

websocket.on('message', (bytes) => {
    const sample = decoder.decode(bytes);        // a complete ClientSample
    observer.accept(sample);
});
```

One decoder per connection, and it must see that connection's messages **in order**.

### Both halves at once

```typescript
import { createClientSampleCodec } from '@observertc/samples-protobuf-codec';

const codec = createClientSampleCodec({ clientId, identifiers: { clientId: 'uuid' } });
const sample = codec.decoder.decode(codec.encoder.encode(input));
```

Building both from one options object is the point: the encoder and the decoder have to agree about
identifier packing, and **the failure mode when they do not is mojibake rather than an error**.

## Streams are ordered and stateful

Message 5 says "jitter is now 12" and says nothing at all about the forty fields that did not move.
A decoder that has not seen messages 1–4 therefore cannot reconstruct sample 5 — and this package
tells you so, with a `STREAM_DESYNC` error, rather than handing back an object quietly missing its
`trackIdentifier`.

- **One decoder per encoder.** They are a pair.
- **The transport must be ordered and lossless.** A WebSocket or an HTTP/2 stream is fine. A
  datagram transport is not, unless you add your own ordering.
- **`reset()` is a keyframe.** Call it on both halves at the same point in the stream — after a
  reconnect, on a schedule, or whenever a new receiver needs to be able to join.

```typescript
encoder.reset();
const keyframe = encoder.encode(sample);
new ClientSampleDecoder().decode(keyframe);   // works
```

`clientId` is the one exception: it rides on **every** message, so a receiver can always attribute a
message without keeping routing state of its own.

### A field that stops being reported keeps its last value

A delta message says what changed. It has no way to say *"this field is gone"*, so the decoder
returns the running **forward-fill** of the stream: if sample 4 carries `jitter` and sample 5 does
not, decoded sample 5 still has sample 4's `jitter`.

That is almost always what you want from `getStats()` output, where a field missing from one tick
means the browser did not report it rather than that it became meaningless. It does mean the
decoder's output is *"everything known about this client so far"*, not *"exactly the object the
encoder was handed"*.

**Collection membership works the other way round: the newest sample defines it.** An RTP stream,
codec or candidate pair that stops appearing is understood to have left the call, and its state is
dropped on both sides — so if it comes back, it is re-sent in full.

## Identifiers: `utf8` or `uuid`

Identifier fields (`callId`, `clientId`, `peerConnectionId`, `trackId` / `trackIdentifier`) travel as
`bytes`. If yours really are UUIDs, packing them into their 16 significant bytes halves them:

```typescript
const options = {
    clientId,
    identifiers: {
        callId: 'uuid',
        clientId: 'uuid',
        peerConnectionId: 'uuid',
        trackId: 'uuid',
    },
} satisfies EncoderOptions;
```

The default is `utf8` for all of them, because ObserveRTC does not require callers to use UUIDs. **A
value configured as `uuid` that is not a UUID is an `INVALID_VALUE` error at encode time, not a
silent fallback** — which is the fix for the old `*IsUuid` boolean pair, where a mismatch produced
mangled ids and no error at all.

## Errors

Everything this package throws is a `ProtobufCodecError` with a `code` and a `context.path` pointing
at the offending value:

| `code` | Meaning |
|---|---|
| `MALFORMED_INPUT` | The bytes are not a `ClientSample` protobuf message |
| `STREAM_DESYNC` | The decoder has not seen enough of the stream to rebuild this sample |
| `INVALID_VALUE` | A value could not be converted between its plain and its wire form |
| `INVALID_OPTION` | The codec was configured with something it cannot honour |

```typescript
const result = decoder.tryDecode(bytes);
if (!result.ok) {
    metrics.increment('codec.decode_failed', { code: result.error.code });
    return;
}
```

The package writes nothing to `console` on its own. Pass a `logger` (anything with
`debug`/`info`/`warn`/`error`) if you want to hear about recoverable oddities.

A non-finite number anywhere inside a payload or `attachments` is rejected with `INVALID_VALUE` and
the path that reached it, rather than being silently turned into `null` by `JSON.stringify` — this
holds at any nesting depth. A `bigint` is rejected the same way, and a cycle is reported as
`MALFORMED_INPUT` rather than by exhausting the stack.

## API

| Export | What it is |
|---|---|
| `ClientSampleEncoder` | `encode`, `encodeToBase64`, `encodeToMessage`, `reset` |
| `ClientSampleDecoder` | `decode`, `decodeBase64`, `decodeFromMessage`, `tryDecode`, `reset` |
| `createClientSampleCodec` | Both halves from one options object |
| `ProtobufCodecError` | Every failure, with `code` and `context` |
| `ClientSample` and friends | The plain sample types, re-exported |
| `protobuf` | The generated protobuf bindings, namespaced |
| `schemaVersion`, `PROTO_PACKAGE` | What this build speaks |

`encodeToMessage` / `decodeFromMessage` work in protobuf messages rather than bytes, for when the
sample is going straight into another protobuf structure — or when you want to look at what a delta
actually contains.

## How it works

The codec keeps one small state machine per live thing in the call — the client, each peer
connection, each RTP stream, each ICE candidate pair — holding the last value seen for every field.
Encoding walks that tree and writes down only what moved; decoding walks the same tree and lays the
arriving values back over what it already had.

Two consequences worth knowing:

- **Collections are keyed, not positional.** Peer connections match on `peerConnectionId`, RTP
  streams on `ssrc`, everything else on `id`. The key is repeated on every message so entries stay
  matchable.
- **The field mapping is read from the protobuf descriptor at runtime.** Which fields exist, which
  are 64-bit, which are `bytes`, which nest — all of it comes off the descriptor rather than from
  hand-written per-field code, so **a field added upstream is carried by the codec without a line of
  new code**.

## Wire compatibility

The `.proto` is the all-optional variant of `ClientSample`, where explicit presence is what carries
"this field changed". **Field numbers are derived from the Avro schema and are part of the
contract.**

The test suite pins the actual bytes for two recorded streams. A change that alters them is a wire
break and needs a schema version bump — a round-trip test would not notice, because encode and
decode move together.

## Choosing between the two codecs

| | `samples-protobuf-codec` | [`samples-json-codec`](/docs/samples-json-codec/) |
|---|---:|---:|
| Runtime dependencies | `@bufbuild/protobuf` | **none** |
| Bundle, minified + gzip | ~29.8 KB | **~2.1 KB** |
| Payload, raw | 1× | 2.73× |
| Payload, gzipped | 1× | **1.41×** |
| Readable on the wire | no | yes |

Same delta semantics, same error codes, same API shape — **you can swap one for the other without
changing anything downstream.** Take protobuf when bytes on the wire are the binding constraint and
you cannot rely on transport compression.

## Migrating from samples-encoder / samples-decoder

| Old | New |
|---|---|
| Two packages, one per direction | One package, both directions |
| `new ClientSampleEncoder(clientId, settings)` | `new ClientSampleEncoder({ clientId, ...options })` |
| `encodeToBytes(sample)` | `encode(sample)` |
| `decodeFromBytes(bytes)` | `decode(bytes)` — or `tryDecode(bytes)` for the non-throwing form |
| `decodeFromBase64` / `encodeToBase64` | `decodeBase64` / `encodeToBase64` |
| `{ clientIdIsUuid: true, callIdIsUuid: true, … }` | `{ identifiers: { clientId: 'uuid', callId: 'uuid', … } }` |
| A decoder joining late returned a half-built sample | `STREAM_DESYNC` |
| Failures returned `undefined` | `ProtobufCodecError` with a `code` and a `context.path`, or `tryDecode()` |

Behaviours the old pair got wrong, corrected here:

- **`false` could never be transmitted.** The boolean encoder skipped any falsy value, so `active`,
  `nominated` and `powerEfficientDecoder` could go `true` but never come back. An empty string had
  the same problem.
- **Two entries of the same type in one sample's `clientEvents` lost the second one's `type`** — all
  events shared one stateful field encoder.
- **`ClientMetaData.timestamp` was dropped entirely on encode**, and its `peerConnectionId` /
  `trackId` ignored the uuid settings.
- **`codecId`, `mid` and `transportId` used a one-time-pass encoder**, so a value that legitimately
  changed mid-call was never re-sent. They are ordinary delta fields now.
- **`attachments` was compared by reference**, so an object rebuilt with identical content was
  re-sent on every sample. It is compared by value now.

## Resources

- [npm package](https://www.npmjs.com/package/@observertc/samples-protobuf-codec)
- [GitHub repository](https://github.com/observertc/schemas)
- [Schema](/docs/schema/) — what is being encoded
- [`samples-json-codec`](/docs/samples-json-codec/) — the same codec over JSON
