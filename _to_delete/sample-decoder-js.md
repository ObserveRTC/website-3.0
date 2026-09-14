---
title: "samples-decoder"
slug: "sample-decoder-js"
description: "Binary decoding for ObserveRTC ClientSamples"
lead: "Restore an encoded ClientSample on the server, ready to hand to observer-js"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 340
toc: true
---

`@observertc/samples-decoder` is the server-side counterpart to
[`@observertc/samples-encoder`](../sample-encoder-js/). It restores a
[`ClientSample`](/docs/schema/clientsample/) from the protobuf representation, ready for
`observer.accept()` or your own storage.

**Current: `3.3.0`** — released in lockstep with the schema and the encoder.

```bash
npm install @observertc/samples-decoder
```

## Quick example

```typescript
import { ClientSampleDecoder } from "@observertc/samples-decoder";

// One decoder per client stream — see below.
const decoder = new ClientSampleDecoder();

const sample = decoder.decodeFromBytes(bytes);
if (sample) observer.accept(sample);
```

## The decoder is stateful — one per stream, in order

{{< callout context="caution" title="This is the thing to get right" icon="alert-triangle" >}}
The encoder omits values that have not changed since the previous sample — `clientId`, `callId`,
peer connection ids, track ids and repeated field values are written once and elided afterwards.
The decoder reconstructs them from what it has already seen.

Therefore:

- **One `ClientSampleDecoder` per client stream**, kept alive for the life of that stream.
- **Samples must arrive in order.** A decoder that missed the sample carrying an id will never
  learn it.
- **Do not share one decoder across clients**, and do not round-robin one client's samples across
  server instances that each hold their own decoder.

A shared or restarted decoder does not throw — it produces samples with missing or wrong ids,
which is much worse. If your transport cannot guarantee per-client ordering, use JSON.
{{< /callout >}}

### Keeping decoders per client

```typescript
const decoders = new Map<string, ClientSampleDecoder>();

function decoderFor(clientId: string) {
    let decoder = decoders.get(clientId);
    if (!decoder) {
        decoder = new ClientSampleDecoder({ clientIdIsUuid: true, callIdIsUuid: true });
        decoders.set(clientId, decoder);
    }
    return decoder;
}

// Release it when the client goes away, or the map grows forever.
observer.on("client-closed", ({ observedClient }) => {
    decoders.delete(observedClient.clientId);
});
```

Because the decoder needs a routing key before it has decoded the sample, carry the `clientId`
outside the payload — a URL path segment, a header, the WebSocket connection identity, or a queue
partition key.

## API

### `new ClientSampleDecoder(settings?)`

```typescript
type ClientSampleDecoderSettings = {
    callIdIsUuid?: boolean;             // default false
    clientIdIsUuid?: boolean;           // default false
    peerConnectionIdIsUuid?: boolean;   // default false
    trackIdIsUuid?: boolean;            // default false
};
```

{{< callout context="caution" title="These must match the encoder exactly" icon="alert-triangle" >}}
The `*IsUuid` flags change how ids are represented on the wire — 16 raw bytes instead of 36 text
characters. If the encoder sets a flag and the decoder does not (or vice versa), ids come back
mangled rather than erroring.
{{< /callout >}}

### Methods

| Method | Input | Pairs with |
|---|---|---|
| `decodeFromBytes(bytes: Uint8Array)` | Binary payload | `encodeToBytes` |
| `decodeFromBase64(base64: string)` | Text payload | `encodeToBase64` |
| `decodeFromProtobuf(message)` | A protobuf message you deserialised yourself | `encodeToProtobufSamples` |

All three return `ClientSample | undefined`. **They do not throw** — a malformed payload is logged
and `undefined` is returned, so a single bad message cannot take your ingestion path down.

```typescript
const sample = decoder.decodeFromBytes(bytes);
if (!sample) {
    metrics.increment("samples.decode_failed");
    return;
}
observer.accept(sample);
```

### Pluggable sub-decoders

If you replaced any encoder-side payload encoder, replace its counterpart here:

```typescript
decoder.clientEventDecoder = myEventDecoder;
decoder.clientIssueDecoder = myIssueDecoder;
decoder.clientMetaDataDecoder = myMetaDecoder;
decoder.extensionStatsDecoder = myExtensionStatsDecoder;
```

## Integration patterns

{{< tabs "decoder-transport" >}}
{{< tab "HTTP" >}}
```typescript
import express from "express";

app.post(
    "/api/samples/:clientId",
    express.raw({ type: "application/octet-stream", limit: "2mb" }),
    (req, res) => {
        const sample = decoderFor(req.params.clientId).decodeFromBytes(req.body);
        if (!sample) return res.sendStatus(400);

        observer.accept(sample, { receivedAt: Date.now() });
        res.sendStatus(202);
    },
);
```

Routing by `clientId` in the path is what lets you keep the right decoder — and, if you scale out,
what you shard on.
{{< /tab >}}
{{< tab "WebSocket" >}}
The natural fit: one connection is one client stream, ordered by construction.

```typescript
wss.on("connection", (ws) => {
    const decoder = new ClientSampleDecoder();

    ws.on("message", (data: Buffer) => {
        const sample = decoder.decodeFromBytes(new Uint8Array(data));
        if (sample) observer.accept(sample);
    });
});
```
{{< /tab >}}
{{< tab "Queue" >}}
```typescript
consumer.on("message", ({ key, value }) => {
    // Partition by clientId upstream so ordering is preserved per client.
    const sample = decoderFor(key).decodeFromBase64(value.payload);
    if (sample) observer.accept(sample);
});
```
{{< /tab >}}
{{< /tabs >}}

## Version compatibility

Keep `@observertc/samples-encoder` and `@observertc/samples-decoder` on the **same version**.
Protobuf field numbers derive from field order, so a schema release that inserts a field before an
existing one renumbers what follows.

`3.3.0` is such a release — adding `ClientIssue.key` moved `payload` from field 2 to 3 and
`timestamp` from 3 to 4. A `3.2.0` decoder reading a `3.3.0` sample misreads those fields.

See the [version history](/docs/schema/versions/v3-3-0/).

{{< callout context="note" title="3.3.0 also fixed a hard import failure" icon="info-circle" >}}
Before `3.3.0`, `ClientSampleDecoder` imported from a protobuf-es internal path that stopped
existing in v2, so requiring the package threw `ERR_PACKAGE_PATH_NOT_EXPORTED`. If you tried the
binary path earlier and it would not even load, that was this.
{{< /callout >}}

## Related

- [`@observertc/samples-encoder`](../sample-encoder-js/) — the other half
- [`observer-js`](../observer-js/) — hand it the decoded sample
- [Schema](/docs/schema/) — what is being decoded

[npm](https://www.npmjs.com/package/@observertc/samples-decoder) ·
[GitHub](https://github.com/observertc/schemas)
