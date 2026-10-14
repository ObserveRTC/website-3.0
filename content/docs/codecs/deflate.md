---
title: "Deflate Codec"
slug: "deflate"
linkTitle: "Deflate Codec"
description: "Compress ClientSample streams with structural deltas, field dictionaries, and platform deflate."
lead: "Send compact binary telemetry without bundling a compression library."
draft: false
outputs: ["HTML", "Markdown"]
weight: 30
toc: false
---

The Deflate Codec (`@observertc/samples-deflate-codec`) compresses successive `ClientSample` records for live delivery. Use it when repeated fields and sample size matter, and your runtime supports `CompressionStream`, `DecompressionStream`, and `structuredClone`. The documented Node.js minimum is 20; browser deployments need those platform APIs.

## How it works

The first message is a complete snapshot. Later messages contain structural changes, with peer-connection list entries matched by `id`. A field-name dictionary replaces repeated names with integer codes. Each envelope is independently deflate-compressed into a binary message with a one-byte codec header.

Compression is per message, but reconstruction is stateful: a later delta still depends on earlier samples and dictionary entries. Removed fields and list entries are preserved as removals rather than silently carrying old values forward.

## Install and encode a sample

```sh
npm install @observertc/samples-deflate-codec
```

The following illustrates a round trip for an existing `sample` and its client identifier. In a real integration, the encoder runs at the sender and the decoder at the receiver:

```typescript
import {
  ClientSampleEncoder,
  ClientSampleDecoder,
} from '@observertc/samples-deflate-codec';

const encoder = new ClientSampleEncoder({ clientId });
const decoder = new ClientSampleDecoder();

const bytes = await encoder.encode(sample);
const decodedSample = await decoder.decode(bytes);
```

`encode()` and `decode()` are asynchronous. Process operations sequentially and preserve message order. `encodeToBase64()` and `decodeBase64()` support text-only transports. Decode to a complete sample before passing it to Observer; Observer does not accept compressed messages directly.

## Preserve stream state

- Keep one decoder per encoder/client stream.
- Use ordered, lossless delivery. An unreliable data channel is insufficient without your own recovery protocol.
- Reset both halves at the same stream boundary after reconnecting or starting a new receiver. The next encoded message is a snapshot.
- Treat decode failures as errors to investigate; do not continue as if the missing sample were successfully reconstructed.

`tryDecode()` returns a success/error result instead of throwing. `DeflateCodecError` exposes a code and context, including invalid input, unsupported options, or stream desynchronization. The decoded sample is independent of the decoder's retained state, so downstream mutation does not change that state.

## Choosing a codec

Choose [JSON Codec](/docs/codecs/json/) for readable delta messages, [Protobuf Codec](/docs/codecs/protobuf/) for its binary format, or Deflate Codec for dictionary-coded deltas with platform compression. Deflate has its own structural diff; it is not simply the JSON Codec with compression switched on. Measure your own streams before choosing a format.

The Deflate Codec package version is **3.7.0**. Package version, sample schema version, and wire-envelope version are separate contracts; do not assume identical version numbers mean interchangeable wire formats.

Sources: [usage and format](https://github.com/ObserveRTC/schemas/blob/3f3ab4c5ee8d628e9665f81dff3aad591c167f17/npm-samples-deflate-codec/README.md), [package and runtime requirements](https://github.com/ObserveRTC/schemas/blob/3f3ab4c5ee8d628e9665f81dff3aad591c167f17/npm-samples-deflate-codec/package.json), and [round-trip tests](https://github.com/ObserveRTC/schemas/blob/3f3ab4c5ee8d628e9665f81dff3aad591c167f17/npm-samples-deflate-codec/test/roundtrip.test.ts).
