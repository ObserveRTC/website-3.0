---
title: "Schema 3.4.0"
date: "2026-08-20T01:59:23Z"
draft: false
project: "Schemas"
version: "3.4.0"
summary: "JSON and protobuf delta codecs arrive; score reasons become a list and the old encoder packages are retired."
sourceUrl: "https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md"
sourceLabel: "Read schema changelog on GitHub ↗"
---

## Changed

- **`ClientSample.scoreReasons`** changed from an optional string to an optional array of strings (string[]). This allows multiple independent reasons to be attached to a calculated client score instead of encoding all score details into a single string value. Previous shape: `scoreReasons?: string | null;` New shape: `scoreReasons?: string[] | null;`  This is a schema and wire-format change, so producers and consumers should be updated to use the 3.4.0 generated schemas together.

## Added

- **`@observertc/samples-json-codec`** — the same delta codec over plain JSON,
  with **zero runtime dependencies** and a ~2.1 KB gzipped bundle (the protobuf
  codec is ~29.8 KB, since it carries the protobuf runtime and descriptor).
  - A delta is a `ClientSample` with the unchanged parts left out — nothing
    renamed, tagged or wrapped — so a message is readable in a log without a
    decoder, and a golden-fixture diff shows exactly which field started or
    stopped being sent.
  - Identical semantics to the protobuf codec: forward-fill, keyed collections,
    `reset()` as a keyframe, matching error codes. The two are interchangeable.
  - On the recorded test stream, JSON is 2.73× the protobuf payload raw and
    **1.41×** gzipped — so with `permessage-deflate` or any compressing
    transport the real cost is about 40%.
  - `NaN` and `Infinity` are rejected rather than silently serialised to `null`.
  - The decoder returns a sample it does not retain, so a pipeline that
    annotates samples in place cannot corrupt the stream.
  - Whole codec is two pure functions, a `diff` and a `merge` that are exact
    inverses, in under 300 lines. The only configuration is which arrays are
    keyed collections; a new schema field needs no change to it.
- Generator artifact `json-codec`. Unlike `protobuf-codec` it does not require
  `proto` — JSON is self-describing, so the package only needs the sample types.
  `npm run generate:codec` now produces both codecs.
- **`@observertc/samples-protobuf-codec`** — one package that both encodes plain
  `ClientSample`s into protobuf and decodes them back, replacing the separate
  `@observertc/samples-encoder` and `@observertc/samples-decoder`. Same wire
  idea as before: each message carries only what changed since the previous
  sample, over the all-optional `ClientSample` proto, where explicit presence is
  what "changed" means.
  - Dual ESM/`CommonJS` build with an `exports` map and full type declarations;
    no `Buffer` or other Node built-ins, so it runs in the browser that produces
    the samples.
  - `ProtobufCodecError` with a `code` (`MALFORMED_INPUT`, `STREAM_DESYNC`,
    `INVALID_VALUE`, `INVALID_OPTION`) and a `context.path` pointing at the
    offending value, plus a non-throwing `decoder.tryDecode()`.
  - `identifiers: { callId | clientId | peerConnectionId | trackId: 'utf8' | 'uuid' }`
    replaces the `*IsUuid` booleans. A value declared `uuid` that is not a UUID
    is now an error rather than a silent fallback.
  - `createClientSampleCodec()` builds both halves from one options object, so
    they cannot disagree about identifier packing.
  - `reset()` on either half is a keyframe: the next message is a full snapshot.
  - Silent by default — pass a `logger` to hear anything.
  - Regression suite (vitest) with byte-exact golden fixtures for two recorded
    streams, plus randomised streams checked against an independent forward-fill
    model.
- Generator artifact `protobuf-codec`, and `npm run generate:codec`. It emits
  only `src/generated/{samples,protobuf}.ts` into the new package: the codec
  reads the field list, scalar types and nesting off the protobuf descriptor at
  runtime, so a new schema field reaches the published codec without any new
  per-field code.

## Fixed

Behaviours the previous encoder/decoder pair got wrong, corrected in the new
package (the old packages are unchanged):

- `false` could never be transmitted. `BooleanToBooleanEncoder` skipped any
  falsy value, so `active`, `nominated` and `powerEfficientDecoder` could go
  `true` but never come back.
- An empty string could never be transmitted, for the same reason.
- Two entries of the same type in one sample's `clientEvents` lost the second
  one's `type`: all events shared one stateful field encoder.
- `ClientMetaData.timestamp` was dropped entirely on encode.
- `ClientMetaData.peerConnectionId` and `.trackId` ignored the uuid settings and
  were always written as utf8.
- `codecId`, `mid` and `transportId` used a one-time-pass encoder, so a value
  that legitimately changed mid-call was never re-sent. They are now ordinary
  delta fields.
- `attachments` was compared by reference, so an object rebuilt with identical
  content was re-sent on every sample. It is now compared by value.
- A decoder that joined a stream late returned a half-built sample; it now
  raises `STREAM_DESYNC`.

## Removed

- **`@observertc/samples-encoder` and `@observertc/samples-decoder` are
  deprecated and removed from this repository.** They stopped at 3.3.0 and will
  not be regenerated, versioned or published again. Their last generated
  sources are in git history at `cc8c7f8`.

  Version 3.3.0 stays installable from npm — removing the sources is not an
  unpublish. The wire format is unchanged, so either package still interoperates
  with `@observertc/samples-protobuf-codec`; the two ends of a stream can
  migrate independently.

  What went with them:
  - `npm-samples-encoder/` and `npm-samples-decoder/`.
  - The `encoder` and `decoder` generator artifacts, and
    `src/targets/codec-lib.ts`. `--only encoder` is now an unknown-artifact
    error.
  - `release-samples-encoder-lib.yaml` and `release-samples-decoder-lib.yaml`.

  The registry-side deprecation is a manual step, since it needs a publish
  token (see `docs/GENERATOR.md`). It matters more now that the READMEs are
  gone — the npm page still shows the last published README, which has no
  deprecation notice on it, so this warning is the only one consumers will see:

  ```sh
  npm deprecate "@observertc/samples-encoder@*" \
    "Deprecated - use @observertc/samples-protobuf-codec instead"
  npm deprecate "@observertc/samples-decoder@*" \
    "Deprecated - use @observertc/samples-protobuf-codec instead"
  ```

---

Source: [ObserveRTC schema changelog](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md). Date verified from the [schema version commit](https://github.com/ObserveRTC/schemas/commit/27f5438f3b610d698056ca292b6d4b56797528f3).
