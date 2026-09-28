---
slug: "general"
title: "Generation & versioning"
description: "Schema definitions are authoritative; generated types must follow them."
lead: "Schema definitions are authoritative; generated types must follow them."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 20
toc: true
---

Authoritative sources are `sources/samples/ClientSample.avsc` and `PeerConnectionSample.chunk.avsc`. The first defines the root and discrete records, the second the PC envelope, tracks and browser-stat families. Every field/type/default is in the [schema field reference](/docs/schema/clientsample/). Root includes timestamp, optional clientId/callId, attachments, score/reasons, PCs, events, issues, metadata and extensions. Optional at schema level does not imply accepted by Observer: Observer rejects missing clientId or callId.

`ClientIssue` is intentionally extensible by string type and payload, rather than a closed enum of detector issues; adding a new issue type usually does not require changing the Avro structure. New raw/stat fields do. `ClientMonitorIssues` is a local discriminated union for built-in issue handling, not the universal wire schema.

The generation path is `src/cli.ts` → `runPipeline()` → JSONC Avro loading/chunk expansion/validation → TypeScript, normalized Avro, Markdown, protobuf and npm targets. `src/config.ts` defines deliberate format overrides:

- Avro attachments are nullable string, but TypeScript exposes `Record<string,unknown>`.
- Payload is modeled with recursive AnyValue in Avro, exposed as Record in TS, and serialized as JSON string in protobuf.
- SFU extension payload is a specific string exception.
- Proto UUID-like identifier fields become bytes; timestamps become double; enum spelling overrides include candidate-pair in-progress variants.

Do not compare these representations with naive textual equivalence. Inspect [schemas/src/config.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/config.ts), [schemas/src/pipeline.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/pipeline.ts), [schemas/src/avro/source-loader.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/avro/source-loader.ts), [schemas/src/avro/chunk-registry.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/avro/chunk-registry.ts), [schemas/src/generators/typescript/generate.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/generators/typescript/generate.ts), [schemas/src/generators/protobuf/proto3-generator.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/generators/protobuf/proto3-generator.ts), [schemas/docs/GENERATOR.md](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/docs/GENERATOR.md).

Generated outputs appear under `outputs/typescript`, `outputs/avsc`, protobuf outputs and npm package source directories. observer-js's checked-in ClientSample.ts is byte-identical to the current generated TS; client-monitor's type field sets match but its file differs textually. Both advertise 3.7.0. Do not edit just one copied ClientSample file as if it were authoritative.

JSON/protobuf codec packages are stream-stateful. One encoder per client/receiver, ordered complete delivery, resets for reconnect/snapshot boundaries. Deltas are not complete ClientSamples. The website's current unordered unreliable channel cannot safely adopt delta encoding by simply replacing JSON.stringify with encode; establish delivery/recovery semantics first. [schemas/npm-samples-json-codec/src/ClientSampleEncoder.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/npm-samples-json-codec/src/ClientSampleEncoder.ts), [schemas/npm-samples-json-codec/src/ClientSampleDecoder.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/npm-samples-json-codec/src/ClientSampleDecoder.ts), [schemas/npm-samples-protobuf-codec/src/ClientSampleEncoder.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/npm-samples-protobuf-codec/src/ClientSampleEncoder.ts), [webrtc-observer.org/client/app.js](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/client/app.js).

[Exact source revisions](/docs/reference/versions/) · [Historical schema releases](/docs/schema/versions/)
