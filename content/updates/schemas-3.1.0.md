---
title: "Schema 3.1.0"
date: "2025-06-01"
draft: false
project: "Schemas"
version: "3.1.0"
summary: "BigInt encoding preserves large outbound byte counters; stale generated artifacts are removed."
sourceUrl: "https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md"
sourceLabel: "Read schema changelog on GitHub ↗"
---

## Changed

- Byte counters on outbound RTP are encoded and decoded as `BigInt`.
  `OutboundRtpEncoder` and `OutboundRtpDecoder` use `NumberToBigIntEncoder` /
  `BigIntToNumberDecoder` for bytes-sent and bytes-received fields, so values
  above `Number.MAX_SAFE_INTEGER` survive a round trip.

## Removed

- Stale generated proto, SQL and TypeScript outputs left over from the 2.x
  layout.

---

Source: [ObserveRTC schema changelog](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md). Date follows the changelog’s schema-version date, rather than a GitHub release publication date.
