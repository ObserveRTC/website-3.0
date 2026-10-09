---
title: "Schema 3.5.0"
date: "2026-08-20T05:49:39Z"
draft: false
project: "Schemas"
version: "3.5.0"
summary: "Event, issue, metadata and extension payloads become records instead of pre-serialized strings."
sourceUrl: "https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md"
sourceLabel: "Read schema changelog on GitHub ↗"
---

## Changed

- **All payloads are records, not pre-serialised strings.** `ClientEvent.payload`, `ClientIssue.payload`, `ClientMetaData.payload` and `ExtensionStat.payload` changed from an optional string to an optional map of primitives — `Record<string, boolean | string | number>` in the generated TypeScript (Avro: `["null", {"type": "map", "values": ["boolean", "string", "double"]}]`, keeping the null-first optional convention). Producers no longer `JSON.stringify` every payload before buffering it, and consumers read payload fields directly instead of parsing a nested JSON document.

  **Why (measured, Node 22, realistic samples with 35–40 payloads):** a pre-stringified payload gets every quote escaped when the whole sample serialises, inflating the payload bytes by **~12%** on the wire; serialising the sample is **~18% faster** end to end (0.37ms → 0.30ms per sample) and the events portion alone **~54% faster** (0.042ms → 0.020ms), because each payload was previously walked twice — once by its own `JSON.stringify` at buffering time (30–40 calls per sample, now zero, along with their intermediate-string garbage) and once more character-by-character for escaping. Server-side decode saves ~3% (one parse instead of 1 + N) and payload fields become directly queryable without a second parse.

  **Codec impact:** on the protobuf wire the payload still travels as a JSON `string` (proto3 cannot express a union-valued map — same convention as `attachments`); the protobuf codec converts it through its JSON-fields mechanism, keyed on the field name, so all four payload fields are covered and protobuf field numbering is unchanged. The JSON codec needs no change: events, issues, meta items and extension stats are value lists written whole, and object values were already handled generically. The TypeScript generator learned to render union-valued Avro maps for this.

---

Source: [ObserveRTC schema changelog](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md). Date verified from the [schema version commit](https://github.com/ObserveRTC/schemas/commit/43bb02cec94e0ef77b6dc62456b6a30b72c8e74a).
