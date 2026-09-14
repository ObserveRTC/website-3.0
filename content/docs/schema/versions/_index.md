---
title: "Version history"
description: "Browsable history of the ObserveRTC schema from 3.0.0 onward"
lead: "What changed in each schema release, field by field"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 630
toc: true
---

The schema version lives in `sources/version.txt` and is stamped into every generated artifact. The
published packages — the sample-schemas types, [`@observertc/samples-protobuf-codec`](/docs/samples-protobuf-codec/)
and [`@observertc/samples-json-codec`](/docs/samples-json-codec/) — are versioned **in lockstep**
with it by the generator.

**Current version: `3.7.0`**

## Timeline

| Version | Date | Headline | Wire-format impact |
|---|---|---|---|
| [3.7.0](./v3-7-0/) | 2026-08 | Payloads may **nest** — free-form JSON instead of a map of primitives | None — byte-identical to 3.6.0 |
| [3.6.0](./v3-6-0/) | 2026-08 | `scoreReasons` becomes a map of contributions | ⚠️ `scoreReasons` becomes a protobuf `map` |
| [3.5.0](./v3-5-0/) | 2026-08 | Payloads become records, not pre-serialised strings | ⚠️ Payload representation changes |
| [3.4.0](./v3-4-0/) | 2026-08 | `scoreReasons` becomes a `string[]`; **both delta codecs arrive** | ⚠️ `scoreReasons` changes shape |
| [3.3.0](./v3-3-0/) | 2026-08 | `key` on `ClientIssue`; TypeScript generator rewrite | ⚠️ `ClientIssue` field numbers shift |
| [3.2.0](./v3-2-0/) | 2026-03 | ECN / RFC 8888 counters, PSNR, structured quality-limitation durations | Additive |
| [3.1.0](./v3-1-0/) | 2025-06 | `BigInt` byte counters on outbound RTP | Encoder/decoder only |
| [3.0.0](./v3-0-0/) | 2025-06 | Complete rewrite of the schema | 🚨 Breaking vs 2.x |

## What changed between 3.0.0 and 3.7.0

**No field was ever removed and no field was renamed**, so a decoder that understands `3.7.0` reads
every `3.x` sample structurally. What did change — twice — is the *type* of a small set of fields.

### New records

| Record | Introduced | Where it is used |
|---|---|---|
| `PsnrSum` | 3.2.0 | `OutboundRtpStats.psnrSum` — per-plane PSNR (`y`, `u`, `v`) |
| `QualityLimitationDurations` | 3.2.0 | `OutboundRtpStats.qualityLimitationDurations` — was a loose map, now a named record with `none`, `cpu`, `bandwidth`, `other` |
| `AnyValue` | 3.7.0 | The Avro description of a nestable payload value — documentation of what may appear, not an encoding |

### New fields

| Record | Field | Version | Purpose |
|---|---|---|---|
| `ClientIssue` | `key` | 3.3.0 | Ties an issue raise to its `<type>-resolved` companion |
| `InboundRtpStats` | `packetsReceivedWithEct1` | 3.2.0 | ECN — packets marked ECT(1) |
| `InboundRtpStats` | `packetsReceivedWithCe` | 3.2.0 | ECN — packets marked CE |
| `InboundRtpStats` | `packetsReportedAsLost` | 3.2.0 | RFC 8888 — reported with a zero R bit |
| `InboundRtpStats` | `packetsReportedAsLostButRecovered` | 3.2.0 | RFC 8888 — later recovered |
| `RemoteInboundRtpStats` | `packetsReceivedWithEct1`, `packetsReceivedWithCe`, `packetsReportedAsLost`, `packetsReportedAsLostButRecovered` | 3.2.0 | The same, remote side |
| `RemoteInboundRtpStats` | `packetsWithBleachedEct1Marking` | 3.2.0 | ECT(1) marking stripped by a middlebox |
| `OutboundRtpStats` | `encodingIndex` | 3.2.0 | Index of this encoding in the encodings array |
| `OutboundRtpStats` | `psnrSum`, `psnrMeasurements` | 3.2.0 | Cumulative PSNR by plane, and how many measurements |
| `OutboundRtpStats` | `packetsSentWithEct1` | 3.2.0 | ECN — packets sent marked ECT(1) |
| `IceTransportStats` | `ccfbMessagesSent`, `ccfbMessagesReceived` | 3.2.0 | Congestion Control Feedback messages |

### Type changes

| Field(s) | Version | From → to |
|---|---|---|
| Outbound byte counters | 3.1.0 | round-trip as `BigInt` through the codecs |
| Several byte and packet counters | 3.2.0 | `int` → `long`, so long calls at high bitrate do not overflow |
| `ClientSample.scoreReasons` | 3.4.0 | `string` → `string[]` |
| `scoreReasons` on every record that has it | 3.6.0 | `string[]` → **`Record<string, number>`** — each reason mapped to how much it contributed |
| The four `payload` fields | 3.5.0 | pre-serialised **string** → record of primitives |
| The four `payload` fields | 3.7.0 | record of primitives → **free-form JSON** (`Record<string, unknown>`) |

### Documentation-only changes

`IceCandidatePairStats.state` gained documentation in 3.3.0 recording which
`RTCStatsIceCandidatePairState` symbols are no longer in the W3C spec — `new` (never standardised)
and `cancelled` (removed after
[w3c/webrtc-stats#66](https://github.com/w3c/webrtc-stats/issues/66)). **Both symbols are
retained**, so nothing about the wire format changed.

## Upgrading

{{< steps >}}
{{< step >}}Read the release page for every version you are skipping.{{< /step >}}
{{< step >}}Upgrade both halves of a codec **together** — they are released in lockstep for a reason, and a mismatched pair can misread a sample without erroring.{{< /step >}}
{{< step >}}Check whether the versions you are crossing changed a *type*: 3.4.0, 3.5.0 and 3.6.0 each did, and producers and consumers should move together across those.{{< /step >}}
{{< step >}}If you store encoded samples, decode with a version that matches what wrote them, or re-encode.{{< /step >}}
{{< step >}}Update your own processing for any new field you want to consume; nothing existing was removed.{{< /step >}}
{{< step >}}Deploy incrementally and watch for decode errors before switching writers over.{{< /step >}}
{{< /steps >}}

{{< callout context="tip" title="Reading a mixed fleet" icon="rocket" >}}
`observer-js` accepts all three payload generations on the same `accept()` call — every payload it
reads goes through a parser that passes an object through untouched and parses a string, and a
legacy `string[]` of score reasons is folded into the record shape with a magnitude of `0`. So you
can upgrade clients gradually without coordinating the server.
{{< /callout >}}

## Sources

- [`CHANGELOG.md`](https://github.com/observertc/schemas/blob/master/CHANGELOG.md) — the canonical history
- [`sources/version.txt`](https://github.com/observertc/schemas/blob/master/sources/version.txt) — the current version
- [`docs/GENERATOR.md`](https://github.com/observertc/schemas/blob/master/docs/GENERATOR.md) — how the generator assigns field numbers
- [`schemaList.md`](https://github.com/observertc/schemas/blob/master/schemaList.md) — the generated field-by-field reference
