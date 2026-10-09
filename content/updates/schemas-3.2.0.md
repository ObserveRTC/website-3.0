---
title: "Schema 3.2.0"
date: "2026-03-18"
draft: false
project: "Schemas"
version: "3.2.0"
summary: "Congestion feedback, video quality measurements, and structured quality-limitation durations."
sourceUrl: "https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md"
sourceLabel: "Read schema changelog on GitHub ↗"
---

## Added

- ECN and packet-accounting fields on inbound RTP stats:
  `packetsReceivedWithEct1`, `packetsReceivedWithCe`, `packetsReportedAsLost`,
  `packetsReportedAsLostButRecovered`.
- `packetsWithBleachedEct1Marking` to outbound RTP stats.
- `encodingIndex` to outbound RTP stats.
- `psnrSum` and `psnrMeasurements` (new `PsnrSum` record with `y`, `u`, `v`
  components) for video quality measurement.
- `frozen` state to `IceCandidatePairStats`.

## Changed

- `qualityLimitationDurations` restructured into a named
  `QualityLimitationDurations` record with `none`, `cpu`, `bandwidth` and
  `other` fields.
- Node 22 across the CI workflows.
- Protobuf handling reworked and dependencies updated; `CONTRIBUTING.md` added.

---

Source: [ObserveRTC schema changelog](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/CHANGELOG.md). Date follows the changelog’s schema-version date, rather than a GitHub release publication date.
