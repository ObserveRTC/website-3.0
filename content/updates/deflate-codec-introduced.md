---
title: "Introducing the Deflate Codec"
date: "2026-10-13T20:23:47Z"
draft: false
project: "Deflate Codec"
summary: "Compact ClientSample streams through structural deltas, field-name dictionary coding, and per-message deflate compression. Thanks to Håvar Aambø Fosstveit for the contribution."
sourceUrl: "https://github.com/ObserveRTC/schemas/pull/44"
sourceLabel: "Read contribution on GitHub ↗"
---

## Smaller telemetry messages

The Deflate Codec adds another option for transporting ObserveRTC `ClientSample` streams. It combines a sample-specific structural diff, dictionary coding for repeated field names, and per-message deflate through the platform's `CompressionStream` and `DecompressionStream` APIs. No compression library is bundled as a runtime dependency.

Thanks to **Håvar Aambø Fosstveit** for contributing this codec and helping extend ObserveRTC's transport options.

## Built for a live sample stream

The first message is a snapshot; subsequent messages carry changes, including removal of fields and entries. Each compressed message can be sent as it arrives. Encoder and decoder state still depend on ordered, lossless delivery, so use a separate pair for each stream and coordinate resets at reconnect boundaries.

Encoding and decoding are asynchronous. Binary messages are supported directly, with base64 helpers for text-only transports. Decode the stream before passing its samples to Observer.

## Try it in your integration

```sh
npm install @observertc/samples-deflate-codec
```

The repository declares package version 3.7.0. Its README reports 831 bytes per sample on one recorded seven-hour call, compared with 9,489 bytes for raw JSON. Those figures describe that fixture, not a guarantee for other deployments.

Start with the [Deflate Codec guide](/docs/codecs/deflate/) for runtime requirements, usage, and stream boundaries, or [compare the codecs](/docs/codecs/).

---

Sources: [contribution #44](https://github.com/ObserveRTC/schemas/pull/44) and [codec README](https://github.com/ObserveRTC/schemas/blob/3f3ab4c5ee8d628e9665f81dff3aad591c167f17/npm-samples-deflate-codec/README.md). Date is the introducing commit's timestamp, October 13, 2026 at 20:23:47 UTC; this is a component introduction rather than a separately verified tagged release announcement.
