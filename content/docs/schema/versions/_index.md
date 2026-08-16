---
title: "Version history"
description: "Browsable history of the ObserveRTC schema from 3.0.0 onward"
lead: "What changed in each schema release, field by field"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 230
toc: true
---

The schema version lives in `sources/version.txt` and is stamped into every generated artifact. The
three published packages — `@observertc/schemas`, `@observertc/samples-encoder` and
`@observertc/samples-decoder` — are versioned **in lockstep** with it by the generator.

**Current version: `3.3.0`**

## Timeline

| Version | Date | Headline | Wire-format impact |
|---|---|---|---|
| [3.3.0](./v3-3-0/) | 2026-08 | `key` on `ClientIssue`; TypeScript generator rewrite | ⚠️ `ClientIssue` field numbers shift |
| [3.2.0](./v3-2-0/) | 2026-03 | ECN / RFC 8888 counters, PSNR, structured quality-limitation durations | Additive |
| [3.1.0](./v3-1-0/) | 2025-06 | `BigInt` byte counters on outbound RTP | Encoder/decoder only |
| [3.0.0](./v3-0-0/) | 2025-06 | Complete rewrite of the schema | 🚨 Breaking vs 2.x |

## What changed between 3.0.0 and 3.3.0

Everything added since `3.0.0`, in one place. **No field was removed and no field was renamed**, so
a decoder that understands `3.3.0` reads every `3.x` sample — with the one wire-format caveat noted
under [3.3.0](./v3-3-0/).

### New records

| Record | Introduced | Where it is used |
|---|---|---|
| `PsnrSum` | 3.2.0 | `OutboundRtpStats.psnrSum` — per-plane PSNR (`y`, `u`, `v`) |
| `QualityLimitationDurations` | 3.2.0 | `OutboundRtpStats.qualityLimitationDurations` — was a loose map, now a named record with `none`, `cpu`, `bandwidth`, `other` |

### New fields

| Record | Field | Version | Purpose |
|---|---|---|---|
| `ClientIssue` | `key` | 3.3.0 | Ties an issue raise to its `<type>-resolved` companion |
| `InboundRtpStats` | `packetsReceivedWithEct1` | 3.2.0 | ECN — packets marked ECT(1) |
| `InboundRtpStats` | `packetsReceivedWithCe` | 3.2.0 | ECN — packets marked CE |
| `InboundRtpStats` | `packetsReportedAsLost` | 3.2.0 | RFC 8888 — reported with a zero R bit |
| `InboundRtpStats` | `packetsReportedAsLostButRecovered` | 3.2.0 | RFC 8888 — later recovered |
| `RemoteInboundRtpStats` | `packetsReceivedWithEct1` | 3.2.0 | ECN, remote side |
| `RemoteInboundRtpStats` | `packetsReceivedWithCe` | 3.2.0 | ECN, remote side |
| `RemoteInboundRtpStats` | `packetsReportedAsLost` | 3.2.0 | RFC 8888, remote side |
| `RemoteInboundRtpStats` | `packetsReportedAsLostButRecovered` | 3.2.0 | RFC 8888, remote side |
| `RemoteInboundRtpStats` | `packetsWithBleachedEct1Marking` | 3.2.0 | ECT(1) marking stripped by a middlebox |
| `OutboundRtpStats` | `encodingIndex` | 3.2.0 | Index of this encoding in the encodings array |
| `OutboundRtpStats` | `psnrSum` | 3.2.0 | Cumulative PSNR by plane |
| `OutboundRtpStats` | `psnrMeasurements` | 3.2.0 | Number of PSNR measurements |
| `OutboundRtpStats` | `packetsSentWithEct1` | 3.2.0 | ECN — packets sent marked ECT(1) |
| `IceTransportStats` | `ccfbMessagesSent` | 3.2.0 | Congestion Control Feedback messages sent |
| `IceTransportStats` | `ccfbMessagesReceived` | 3.2.0 | Congestion Control Feedback messages received |

### Type widenings

Several byte and packet counters moved from `int` to `long` in 3.2.0 so long calls at high bitrate
do not overflow, and outbound byte counters round-trip as `BigInt` through the encoder/decoder as
of 3.1.0.

### Documentation-only changes

`IceCandidatePairStats.state` gained documentation in 3.3.0 recording which
`RTCStatsIceCandidatePairState` symbols are no longer in the W3C spec — `new` (never standardised)
and `cancelled` (removed after
[w3c/webrtc-stats#66](https://github.com/w3c/webrtc-stats/issues/66)). **Both symbols are
retained**, so nothing about the wire format changed.

## How versioning works

| Change type | Version bump | Compatibility |
|---|---|---|
| Field addition at the end of its group | Minor | Additive; older decoders ignore it |
| Field addition **elsewhere** in its group | Minor | ⚠️ renumbers protobuf fields after it |
| Field removal | Major | Breaking |
| Type change | Major | Breaking |
| Documentation | Patch | Non-breaking |

{{< callout context="caution" title="Protobuf field numbers come from field order" icon="alert-triangle" >}}
The generator sorts fields — repeated, then required, then optional, each sorted by name — and
assigns protobuf numbers from that order. Inserting a field anywhere but the end of its group
renumbers every field after it, which breaks the wire format for decoders built against the older
schema.

This is why `3.3.0` carries a wire-format warning despite adding only one field. Always keep
`@observertc/samples-encoder` and `@observertc/samples-decoder` on the same version.
{{< /callout >}}

## Upgrading

{{< steps >}}
{{< step >}}Read the release page for every version you are skipping.{{< /step >}}
{{< step >}}Upgrade encoder and decoder **together** — they are released in lockstep for a reason.{{< /step >}}
{{< step >}}If you store encoded samples, decode with a version that matches what wrote them, or re-encode.{{< /step >}}
{{< step >}}Update your own processing for any new field you want to consume; nothing existing was removed.{{< /step >}}
{{< step >}}Deploy incrementally and watch for decode errors before switching writers over.{{< /step >}}
{{< /steps >}}

## Sources

- [`CHANGELOG.md`](https://github.com/observertc/schemas/blob/master/CHANGELOG.md) — the canonical history
- [`sources/version.txt`](https://github.com/observertc/schemas/blob/master/sources/version.txt) — the current version
- [`docs/GENERATOR.md`](https://github.com/observertc/schemas/blob/master/docs/GENERATOR.md) — how the generator assigns field numbers
- [`schemaList.md`](https://github.com/observertc/schemas/blob/master/schemaList.md) — the generated field-by-field reference
