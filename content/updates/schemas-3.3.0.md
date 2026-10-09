---
title: "Schema 3.3.0"
date: "2026-08-09T11:17:16Z"
draft: false
project: "Schemas"
version: "3.3.0"
summary: "Issue lifecycle keys, a TypeScript generator rewrite, and repaired decoder imports."
sourceUrl: "https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md"
sourceLabel: "Read schema changelog on GitHub ↗"
---

## Added

- `key` field to `ClientIssue` in `ClientSample` — identifier of the related
  issue or resolution when one is provided.
- Documentation on `IceCandidatePairStats.state`, and source comments recording
  which `RTCStatsIceCandidatePairState` symbols are no longer in the W3C spec:
  `new` (never standardised) and `cancelled` (removed after
  [w3c/webrtc-stats#66](https://github.com/w3c/webrtc-stats/issues/66); last
  published in the 2016-12-14 Working Draft). Both symbols are retained for
  backward compatibility — no field or enum value was removed, so the wire
  format is unchanged.

> **Wire-format warning.** `ClientIssue` field numbers shift because protobuf
> numbering follows sorted field order: `payload` moves 2 → 3 and `timestamp`
> 3 → 4. A decoder built against 3.2.0 will misread these. See
> [`docs/GENERATOR.md`](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/docs/GENERATOR.md).

## Changed

- The generator was rewritten in TypeScript (`src/`, run with
  `npm run generate`). The legacy `index.js` and its root-level helpers were
  removed. Generated TypeScript, Avro and protobuf output is byte-identical to
  the previous implementation.
- `schemaVersion` is now exported from the `ClientSample` module only. It was
  previously emitted by every generated module, which made `src/index.ts`
  re-export the same name twice and broke `npm-samples-lib`'s build (TS2308).
  The package still exports `schemaVersion` from its entry point.
- Generated Markdown no longer runs a section heading onto the end of the
  preceding table row, and no longer prints `undefined` for enum fields that
  have no description.
- All packages moved to TypeScript 7 with `"module": "nodenext"`. Emit is still
  `CommonJS`; published entry points are unchanged.
- Dependencies refreshed: `avro-js` 1.12.1, `@bufbuild/buf` 1.72.0,
  `@bufbuild/protobuf` and `@bufbuild/protoc-gen-es` 2.13.0. Removed `argparse`,
  `json-schema-to-markdown`, `protobufjs` and `typedoc`, none of which were used.

## Fixed

- `@observertc/samples-decoder` could not be imported. `ClientSampleDecoder`
  imported `fromBinary` from `@bufbuild/protobuf/dist/cjs/from-binary`, a path
  that stopped existing in protobuf-es v2; requiring the package threw
  `ERR_PACKAGE_PATH_NOT_EXPORTED`. It now imports from the package root.

---

Source: [ObserveRTC schema changelog](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md). Date verified from the [schema version commit](https://github.com/ObserveRTC/schemas/commit/cc8c7f8072046108d88367fcb5e3bbf0182cf030).
