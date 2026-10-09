---
title: "Schema 3.7.0"
date: "2026-08-31T10:18:29Z"
draft: false
project: "Schemas"
version: "3.7.0"
summary: "Nested JSON payloads, unchanged codec bytes, and explicit validation of invalid opaque values."
sourceUrl: "https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md"
sourceLabel: "Read schema changelog on GitHub ↗"
---

## Changed

- **Payloads may nest.** `ClientEvent.payload`, `ClientIssue.payload`, `ClientMetaData.payload` and `ExtensionStat.payload` changed from a map of primitives to a free-form JSON object — `Record<string, unknown>` in the generated TypeScript, the same type `attachments` has had since it stopped being a string. A payload value may now be an object, an array, or any nesting of the two, so a caller with structured context (`{ device: { os: { name, version } } }`) no longer has to flatten it into dotted keys or stringify it into one field and parse it back on the far side.

  In Avro the map's values became `AnyValue`, a record that refers to itself through an `objectValue` map and an `arrayValue` array — the shape protobuf's `Struct`/`Value` uses, and the only way Avro can describe unbounded nesting, since a union cannot contain another union and only a *named* type can recurse. Treat it as documentation of what may appear rather than as an encoding: Avro tags its union branches in JSON, so the `.avsc` has not described the codecs' actual bytes since payloads stopped being strings in 3.5.0.

  **Wire format: unchanged.** Both codecs' golden fixtures are byte-identical to 3.6.0 apart from the recorded version string. On the protobuf wire a payload was already a JSON `string` (proto3 can express neither the old union-valued map nor the new one), so nesting costs it nothing. In the JSON codec a payload is an opaque object written whole whenever it changes and never carried forward, which is what made nesting free there too — diffing *into* a payload would need a way to say "this key was removed", which the format deliberately does not have. A 3.6.0 decoder reads a 3.7.0 stream and vice versa; only the TypeScript type moved.

  **Upgrading:** reading a payload value now needs narrowing. `payload.role` was `boolean | string | number` and is now `unknown`, so `String(payload.role)` or a type guard replaces a bare read. Writers need no change — everything that was valid before still is.

## Fixed

- **A non-finite number inside a payload or `attachments` no longer becomes `null` in silence.** Both codecs copied opaque values with `JSON.parse(JSON.stringify(v))`, which turns `NaN` and `Infinity` into `null` without complaint — exactly the corruption the top-level finite check has always rejected, but it only ever saw the top level of a record. With payloads able to nest, a `NaN` several levels down was newly easy to reach, so the encode path now walks an opaque value before copying it and reports the path that was wrong (`INVALID_VALUE`). A `bigint`, which previously escaped as a bare `TypeError` from inside the codec, is rejected the same way, and a cycle is reported as `MALFORMED_INPUT` rather than by exhausting the stack. Both codecs use the same codes for the same inputs. Values `JSON.stringify` drops harmlessly — functions, symbols, `undefined` — are still dropped, and a value with its own `toJSON`, such as a `Date`, still serialises itself.

## Internal

- TypeScript field-type overrides in the generator may now be scoped to one record, as `Record.field`, and a scoped key beats a bare one. The bare `payload` entry that gives the four client payloads their opaque type would otherwise also have caught `SfuExtensionStats.payload`, which is a genuine JSON string on the SFU wire; it keeps its `string` type through `['SfuExtensionStats.payload', 'string']`. Field names are not unique across the schema set, so the mechanism now says which one it means.

---

Source: [ObserveRTC schema changelog](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md). Date verified from the [schema version commit](https://github.com/ObserveRTC/schemas/commit/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17).
