---
title: "Schema 3.6.0"
date: "2026-08-23T13:09:34Z"
draft: false
project: "Schemas"
version: "3.6.0"
summary: "Score reasons become a map of numeric contributions, with a corresponding protobuf wire change."
sourceUrl: "https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md"
sourceLabel: "Read schema changelog on GitHub ↗"
---

## Changed

- **`scoreReasons` is a map of contributions, not a list of labels.** `ClientSample.scoreReasons`, `PeerConnectionSample.scoreReasons`, `InboundTrackSample.scoreReasons` and `OutboundTrackSample.scoreReasons` changed from an optional array of strings to an optional map of doubles — `Record<string, number>` in the generated TypeScript (Avro: `["null", {"type": "map", "values": "double"}]`) — mapping each reason to how much it contributed to the calculated score. On the protobuf wire the field is now a real `map<string, double>`: the generator learned to emit proto3 maps for primitive-valued Avro maps (union-valued maps such as `payload` keep travelling as JSON strings), and a map field sorts with the repeated group so neighbouring field numbers are unchanged. Both codecs treat the field exactly as they treated the string array — written whole whenever present, never carried forward, an empty map meaning the same as an absent one. This is a schema and wire-format change, so producers and consumers should move to the 3.6.0 generated schemas together.

---

Source: [ObserveRTC schema changelog](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md). Date verified from the [schema version commit](https://github.com/ObserveRTC/schemas/commit/6be1d630a36547489e5bcf49ccc484f3a24938ff).
