---
title: "samples-encoder"
slug: "sample-encoder-js"
description: "Binary encoding for ObserveRTC ClientSamples"
lead: "Compress a ClientSample into the protobuf representation defined by the schema, before you upload it"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 330
toc: true
---

`@observertc/samples-encoder` encodes a [`ClientSample`](/docs/schema/clientsample/) into the
protobuf representation generated from the [schema](/docs/schema/). It is generated in lockstep
with the schema, so the encoder version **is** the schema version.

**Current: `3.3.0`**

```bash
npm install @observertc/samples-encoder
```

## Quick example

```javascript
import { ClientSampleEncoder } from "@observertc/samples-encoder";

// One encoder per client — the clientId is baked in.
const encoder = new ClientSampleEncoder(clientId);

monitor.on("sample-created", (sample) => {
    const bytes = encoder.encodeToBytes(sample);

    fetch("/api/samples", {
        method: "POST",
        headers: { "Content-Type": "application/octet-stream" },
        body: bytes,
    });
});
```

## The encoder is stateful — this matters

{{< callout context="caution" title="One encoder instance per client stream, and the decoder must match" icon="alert-triangle" >}}
The encoder does more than serialise. It is **delta-aware**: values that do not change between
samples — the `clientId`, the `callId`, peer connection ids, track ids, and any field whose value
repeats — are written **once** and omitted afterwards. That is where most of the size reduction
comes from.

The consequences:

- Create **one `ClientSampleEncoder` per client** and keep it for the life of that client's stream.
  A fresh encoder per sample throws away the benefit and produces larger output.
- The receiving side must use **one `ClientSampleDecoder` per stream**, fed the samples **in
  order**. A decoder that misses an earlier sample never learns the omitted values.
- Do not load-balance one client's samples across servers that each hold their own decoder unless
  you also route by client and preserve order.

If your transport cannot guarantee ordering per client, send JSON instead — the savings are not
worth silently corrupted ids.
{{< /callout >}}

## API

### `new ClientSampleEncoder(clientId, settings?)`

```typescript
type ClientSampleEncoderSettings = {
    callIdIsUuid?: boolean;             // default false
    clientIdIsUuid?: boolean;           // default false
    peerConnectionIdIsUuid?: boolean;   // default false
    trackIdIsUuid?: boolean;            // default false
};
```

The `*IsUuid` flags are a real optimisation: a UUID written as text is 36 bytes, and written as
bytes is 16. If your ids genuinely are UUIDs, turn the corresponding flag on — **and set the same
flags on the decoder**, or the ids come back wrong.

```javascript
const encoder = new ClientSampleEncoder(clientId, {
    clientIdIsUuid: true,
    callIdIsUuid: true,
    peerConnectionIdIsUuid: true,
    trackIdIsUuid: true,
});
```

### Methods

| Method | Returns | Use when |
|---|---|---|
| `encodeToBytes(sample)` | `Uint8Array` | Binary transports: `fetch` with `application/octet-stream`, WebSocket binary frames, a data channel |
| `encodeToBase64(sample)` | `string` | The payload must be text — JSON envelopes, log lines, some message queues |
| `encodeToProtobufSamples(sample)` | protobuf message | You want to serialise it yourself, or forward it into an existing protobuf pipeline |

### Pluggable sub-encoders

Payloads that are opaque to the schema — event, issue, metadata and extension-stat payloads, and
`attachments` — go through replaceable encoders, so you can compress your own payload shapes rather
than shipping JSON strings:

```javascript
encoder.clientEventEncoder = myEventEncoder;
encoder.clientIssueEncoder = myIssueEncoder;
encoder.clientMetaDataEncoder = myMetaEncoder;
encoder.extensionStatsEncoder = myExtensionStatsEncoder;
```

Each implements the exported `Encoder` interface, and each needs a matching decoder on the server.

## Sizing expectation

The saving depends heavily on your sample shape — how many peer connections, how many tracks, how
much you put in `attachments`. In practice the two large wins are the protobuf field encoding
itself and the delta/one-time-pass behaviour across a stream. Measure with your own traffic before
committing to a number:

```javascript
const json = JSON.stringify(sample).length;
const bin = encoder.encodeToBytes(sample).byteLength;
console.log(`${bin} / ${json} = ${((bin / json) * 100).toFixed(1)}%`);
```

Run that over a few minutes of a real call rather than on the first sample — the first one carries
the join snapshot and the not-yet-elided ids, so it is the least representative sample you will
ever encode.

## Integration patterns

{{< tabs "encoder-transport" >}}
{{< tab "HTTP" >}}
```javascript
const encoder = new ClientSampleEncoder(clientId);

monitor.on("sample-created", async (sample) => {
    await fetch("/api/samples", {
        method: "POST",
        headers: { "Content-Type": "application/octet-stream" },
        body: encoder.encodeToBytes(sample),
    });
});
```
{{< /tab >}}
{{< tab "WebSocket" >}}
Ordering is preserved per connection, which suits the stateful encoder well.

```javascript
const encoder = new ClientSampleEncoder(clientId);
const ws = new WebSocket("wss://analytics.example.com");

monitor.on("sample-created", (sample) => {
    if (ws.readyState !== WebSocket.OPEN) return;
    ws.send(encoder.encodeToBytes(sample));
});
```
{{< /tab >}}
{{< tab "Text envelope" >}}
```javascript
const encoder = new ClientSampleEncoder(clientId);

monitor.on("sample-created", (sample) => {
    queue.publish({
        clientId,
        seq: seq++,
        payload: encoder.encodeToBase64(sample),
    });
});
```

Carry a sequence number so the consumer can detect gaps — the decoder needs the samples in order.
{{< /tab >}}
{{< /tabs >}}

## Version compatibility

{{< callout context="caution" title="Encoder and decoder must be the same version" icon="alert-triangle" >}}
Protobuf field numbers are derived from field order, so a schema release that inserts a field
before an existing one renumbers everything after it. A mismatched pair can misread a sample
**without erroring**.

`3.3.0` is exactly such a release — `ClientIssue.payload` moved from field 2 to 3. See the
[version history](/docs/schema/versions/v3-3-0/).
{{< /callout >}}

## Related

- [`@observertc/samples-decoder`](../sample-decoder-js/) — the other half
- [`client-monitor-js`](../client-monitor-js/) — produces the samples
- [`observer-js`](../observer-js/) — consumes the decoded samples
- [Schema](/docs/schema/) — what is being encoded

[npm](https://www.npmjs.com/package/@observertc/samples-encoder) ·
[GitHub](https://github.com/observertc/schemas)
