# Analytics digest contract, version 1

Status: proposed implementation contract, October 15, 2026. These are new analytics artifacts, not changes to ClientSample or Observer CallSummary. Both implementation prompts in this directory depend on this document. Changes to field meaning require a new major schema version and coordinated producer/consumer changes.

## Purpose

The processor turns archived samples, summaries and optional events into saved facts. The UI reads those facts to show fleet trends, find affected calls, and investigate a participant or stream. The UI does not recalculate counter deltas, classify impairments, merge Observer summaries, or read all raw archives to build its homepage.

Two persisted documents are the core contract:

- **Call digest:** one call's identity, coverage, participants, metric aggregates, findings and references to paginated detail.
- **Period digest:** one UTC day or month of counts, exposure, distributions and cohort breakdowns. It also references paginated call search results.

Large stream/path/timeline data is saved separately and loaded on demand. Source archives remain the evidence and reprocessing input. All IDs and keys are tenant-scoped. No UI-supplied storage key bypasses server authorization.

## Shared conventions

| Item | Contract |
|---|---|
| Time | UTC epoch milliseconds; intervals are half-open `[startAt, endAt)`. Durations in milliseconds unless the metric registry specifies otherwise |
| Ratios | Fractions from 0 to 1; UI may format as percentages. Never mix with 0–100 inputs |
| Numbers | Finite JSON numbers; counts and byte totals are nonnegative integers within JavaScript's safe-integer range. Overflow makes that measurement unavailable with a warning; never round silently |
| Unknown | Required nullable values use `null`, never zero or a sentinel such as `-1`. Optional sections are explicitly listed as unavailable in capabilities |
| Empty | `[]` means the collection was evaluated and is empty. A missing detail resource means unavailable, never an empty result |
| Identity | A participant is a client instance, not a unique human. A stream ID includes its lifecycle epoch; reconnects and reused stat IDs must not concatenate unrelated counters |
| Versioning | `schemaVersion: 1`; additive optional fields are allowed. Unknown fields are ignored. Unsupported major versions produce an explicit UI error |
| Calculation changes | `processorVersion` and `policyId` identify immutable calculation code/configuration. Incompatible policies/distributions cannot be silently combined |
| Evidence | References identify authorized logical source records, timestamps and stat IDs; never credentials or presigned URLs stored in the digest |
| Completeness | Source completeness, metric measurability and call lifecycle are separate states |

## Shared types

The following TypeScript is a descriptive serialization contract. Implement it once as a shared package or generated schema, with runtime JSON validation and fixtures used by both components. IDs shown as strings are opaque; do not derive semantics from their text.

```ts
type TimeRange = { startAt: number; endAt: number };
type Completeness = 'complete' | 'partial' | 'unknown';
type CapabilityState = 'available' | 'partial' | 'unavailable';
type Capability = { state: CapabilityState; reasons: string[] };
type Dimension =
  | 'browser' | 'browserMajorVersion' | 'os' | 'appVersion'
  | 'sdkVersion' | 'producer' | 'region' | 'sfuId' | 'turnServer';
type Subject = {
  kind: 'call' | 'participant' | 'stream' | 'transport';
  id: string;
};
type EvidenceRef = {
  sourceId: string;
  at: number | null;
  recordId: string | null;
  statId: string | null;
};
type ResourceRef = {
  resourceId: string;
  records: number;
};
type Provenance = {
  processorVersion: string;
  policyId: string;
  sourceRevision: string;
  generatedAt: number;
};
type Source = {
  sourceId: string;
  kind: 'client-samples' | 'observer-summary' | 'observer-events'
      | 'application-events' | 'router-samples';
  logicalKey: string;
  revision: string;
};
type Coverage = {
  completeness: Completeness;
  expectedSources: number | null;
  processedSources: number;
  rejectedRecords: number;
  duplicateRecords: number;
  gapDurationMs: number | null;
  truncated: boolean;
  warnings: string[];
};

// Metric registry fixes each metric's subject, direction, media and units.
// Identical metric IDs under different subjects never imply the same exposure.
type MetricAggregate = {
  metricId: string;
  status: 'measured' | 'partial' | 'unavailable';
  unavailableReasons: string[];
  validIntervals: number;
  eligibleDurationMs: number | null;
  measuredDurationMs: number;
  numerator: number | null;
  denominator: number | null;
  min: number | null;
  max: number | null;
  distribution: Histogram | null;
};
type Histogram = {
  definitionId: string;
  weights: number[];
};
type MetricDefinition = {
  metricId: string;
  label: string;
  unit: 'bps' | 'ms' | 'fps' | 'ratio' | 'bytes' | 'count';
  aggregation: 'ratio-of-sums' | 'duration-weighted-mean' | 'sum';
  histogram: null | {
    definitionId: string;
    upperBounds: number[];
    weightUnit: 'ms';
  };
};
type ImpairmentExposure = {
  category: 'audio' | 'video' | 'network' | 'connectivity' | 'any';
  assessedParticipantMs: number;
  impairedParticipantMs: number;
  unknownParticipantMs: number;
};
```

`Source.revision` is an immutable version ID or content hash, not just a mutable path. `sourceRevision` hashes the canonical input manifest plus policy identity. It changes on late records or corrected sources. `Coverage.gapDurationMs` is the union of missing time across participant instances, summed across participants; it is not a sum across every stream. Leave it null when expected cadence/exposure cannot be established. Warnings and reason codes are stable machine strings with a UI label map; unknown codes remain visible through a readable fallback.

An unavailable metric has null numerator/denominator/min/max/distribution and zero valid intervals/measured duration. Partial means at least some valid evidence exists but coverage or required inputs are incomplete. For a sum, `numerator` is the sum and `denominator` is null. For a ratio, both are accumulated in the registry's units. A measured zero is valid evidence. A zero denominator yields an unavailable display value, never a zero rate.

Histograms use immutable definitions distributed with the contract. `weights.length = upperBounds.length + 1`; buckets are `(-∞, b0]`, `(b0, b1]`, …, `(bn, +∞)`. Inputs outside the metric's legal domain are rejected before bucketing. Only identical definition IDs can be merged. Quantiles are approximate bucket ranges, not exact point estimates. Bounds and definitions must be committed with fixtures before either implementation is considered complete.

## Call digest

```ts
type CallDigest = {
  kind: 'call-digest';
  schemaVersion: 1;
  digestId: string;
  tenantId: string;
  callId: string;
  roomId: string | null;
  revision: string;
  provenance: Provenance;
  lifecycle: 'open' | 'closed' | 'unknown';
  range: TimeRange | null;
  coverage: Coverage;
  capabilities: Record<string, Capability>;
  sources: Source[];
  usage: {
    participantSessions: number | null;
    peakConcurrentParticipants: number | null;
    observedParticipantMs: number;
    connectedParticipantMs: number | null;
    callDurationMs: number | null;
  };
  joins: JoinAggregate;
  impairments: ImpairmentExposure[];
  metrics: MetricAggregate[];
  findingCounts: FindingCount[];
  participants: ResourceRef | null;
  streamDetails: ResourceRef | null;
  pathDetails: ResourceRef | null;
  timeline: ResourceRef | null;
  findings: ResourceRef | null;
};
type JoinAggregate = {
  status: CapabilityState;
  attempts: number | null;
  succeeded: number | null;
  failed: number | null;
  canceled: number | null;
  pending: number | null;
  unknown: number | null;
};
type FindingCount = {
  category: string;
  raised: number;
  activeAtEnd: number;
  truncated: boolean;
};
```

`revision` identifies this immutable output generation. `range` is the known call span, not the archive write time; it is null when lifecycle evidence cannot establish it. Summary finalization time is not call end time. Open calls are provisional even if all currently known files were processed. First/last observed samples may bound observed exposure, but do not establish authoritative join/leave times.

`participantSessions` counts deduplicated client lifecycle instances, never unique people or summed multi-SFU counts. `peakConcurrentParticipants` requires membership intervals; a summary's single-call peak can be used if authoritative for the whole call, but multiple SFU peaks cannot simply be summed. `observedParticipantMs` unions valid observation intervals per client instance and sums them; it is not participant count × call duration. `connectedParticipantMs` requires explicit connection-state evidence.

`joins` is unavailable without a versioned application attempt feed. Available counts partition attempts: succeeded + failed + canceled + pending + unknown = attempts. For the default success KPI, denominator is succeeded + failed. The UI shows canceled/pending/unknown beside it. A peer connection is not a join attempt.

Required capability keys: `usage`, `joinOutcomes`, `audio`, `video`, `network`, `connectivity`, `paths`, `topology`, `cohorts`, `scores`. Capabilities reflect measured evidence and producer support, not just schema field existence.

## Participant, stream, path, timeline and finding detail

```ts
type ParticipantDigest = {
  participantId: string;
  clientId: string;
  instanceId: string;
  displayName: string | null;
  // These membership ranges are empty if unavailable; capability says why.
  membership: TimeRange[];
  dimensions: Partial<Record<Dimension, string | null>>;
  capabilities: Record<string, Capability>;
  observedDurationMs: number;
  metrics: MetricAggregate[];
  impairments: ImpairmentExposure[];
};
type StreamDigest = {
  streamId: string;
  participantId: string;
  peerConnectionId: string;
  trackId: string | null;
  encodingId: string | null;
  direction: 'inbound' | 'outbound';
  mediaKind: 'audio' | 'video';
  epoch: string;
  publisherStreamId: string | null;
  relationshipSource: string | null;
  metrics: MetricAggregate[];
};
type PathDigest = {
  pathId: string;
  participantId: string;
  peerConnectionId: string;
  transportId: string;
  range: TimeRange;
  selectedCandidatePairId: string | null;
  relayed: boolean | null;
  relayServer: string | null;
  protocol: string | null;
  relayProtocol: string | null;
  evidence: EvidenceRef[];
};
type TimelineRecord = {
  recordId: string;
  subject: Subject;
  range: TimeRange;
  kind: 'measurement' | 'state' | 'event' | 'gap';
  metricId: string | null;
  value: number | null;
  // Valid only for measurement records; supports interpretable bucket values.
  numerator: number | null;
  denominator: number | null;
  state: string | null;
  validity: 'valid' | 'missing' | 'stale' | 'reset' | 'gap';
  evidence: EvidenceRef[];
};
type Finding = {
  findingId: string;
  category: string;
  type: string;
  severity: 'info' | 'warning' | 'critical';
  subject: Subject;
  affectedParticipantIds: string[];
  startedAt: number;
  resolvedAt: number | null;
  lastObservedAt: number;
  origin: 'client-detector' | 'observer-detector' | 'digest-rule';
  certainty: 'observation' | 'hypothesis';
  confidence: 'low' | 'medium' | 'high' | null;
  algorithmId: string;
  evidence: EvidenceRef[];
};
```

Time-varying dimensions such as selected TURN server, SFU, or changing app context must be represented through interval evidence and split cohort exposure. The participant's dimension map contains only invariant values; omit a changing dimension there. Unknown publisher relationships stay null; never join SFU tracks solely by equal SSRC.

Timeline measurements represent supported observation intervals, not fabricated exact occurrence times. Sampled cumulative freeze counters reveal freeze time within an interval, not exact freeze boundaries. Preserve that interval uncertainty. An event may use `startAt = endAt`; it adds no duration. State/gap records have null metric/numerator/denominator/value fields. Charts preserve gaps rather than interpolating through them.

An unresolved finding's `resolvedAt` stays null; exposure ends at last assessed evidence, not automatically at the query end. Ongoing detector state through unavailable inputs does not prove ongoing impairment. Native browser freeze duration remains a stream metric; it does not establish exact participant impairment intervals without suitable temporal evidence. Report assessed versus unknown exposure according to the named policy.

## Period digest

```ts
type PeriodDigest = {
  kind: 'period-digest';
  schemaVersion: 1;
  tenantId: string;
  period: 'day' | 'month';
  id: string; // YYYY-MM-DD or YYYY-MM, UTC
  range: TimeRange;
  revision: string;
  provenance: Provenance;
  completeness: Completeness;
  coverage: {
    indexedCalls: number;
    readableCallDigests: number;
    pendingCallDigests: number;
    failedCallDigests: number;
    unknownCallDigests: number;
    expectedChildPeriods: number;
    includedChildPeriods: number;
  };
  totals: {
    callsStarted: number;
    callsWithExposure: number;
    participantSessionsStarted: number;
    observedParticipantMs: number;
    connectedParticipantMs: number | null;
    callExposureMs: number;
    largestCallPeakParticipants: number | null;
  };
  joins: JoinAggregate;
  impairments: ImpairmentExposure[];
  metrics: MetricAggregate[];
  findingCounts: FindingCount[];
  cohorts: CohortAggregate[];
  buckets: PeriodBucket[];
  worstCalls: RankedCall[];
  callSearchResourceId: string;
};
type CohortAggregate = {
  dimension: Dimension;
  value: string | null;
  observedParticipantMs: number;
  impairments: ImpairmentExposure[];
  metrics: MetricAggregate[];
};
type PeriodBucket = {
  range: TimeRange;
  completeness: Completeness;
  callsStarted: number;
  observedParticipantMs: number;
  impairments: ImpairmentExposure[];
};
type RankedCall = {
  callId: string;
  roomId: string | null;
  digestRevision: string;
  startedAt: number | null;
  impairedParticipantMs: number;
  assessedParticipantMs: number;
  completeness: Completeness;
};
```

Daily buckets are 24 UTC hours; month buckets are its UTC days. `callsStarted` counts calls with a known start inside the period. `participantSessionsStarted` uses known membership starts. Exposure values are clipped to the period, including calls started earlier. A summary-only call's known span may support call exposure, but not inferred participant exposure. Mark partial populations rather than silently omitting unknown starts.

`callsWithExposure` counts each call with positive call/participant observation exposure once in this period. It must be deduplicated across days for a month; do not sum daily values. Likewise, monthly largest-call peak is the maximum, never a sum. Additive exposure and numerator/denominator fields sum. Joins are assigned to attempt start time; outcomes replace the prior result on reprocessing. Finding counts are assigned by raise time and deduplicated by stable finding identity. `activeAtEnd` is evaluated at the period boundary from known finding lifecycle and is not additive.

Monthly processing therefore needs a persisted call-contribution index (or exact identity set) to deduplicate call membership, update late outcomes and evaluate boundary state. An implementation that reads only anonymous daily totals cannot satisfy these semantics. Internal indexes are not UI payloads.

Cohort totals use exposure assigned to that dimension's value during each interval. Null is the unknown cohort, never discarded. Values of a single-valued dimension partition eligible exposure; multi-valued SFU participation must be assigned by an explicit path/ownership policy and must not duplicate overall participant time. Do not cross-combine dimensions from marginal cohort totals. Use a server query over call/participant contributions for combined filters. UI filters advertise which combinations are supported.

`worstCalls` contains at most 20 calls ordered by impaired participant milliseconds descending, then impairment share descending, then call ID ascending. Its exposure is clipped to this period. Use all-category union exposure, not a sum of categories. Calls with no assessed evidence are excluded and remain discoverable through missing-data filters. A period with no observed impairment has an empty ranking. The processor computes ranking; the UI does not substitute a score-based ranking.

Coverage counts classify indexed candidate calls into readable, pending, failed or unknown; their sum equals indexedCalls. A readable digest may itself be partial. Month child counts refer to expected/included UTC days; day child counts are 24 expected hours and the hours whose input inventory was successfully evaluated. A successfully evaluated empty bucket is zero; an unavailable bucket is identified through completeness/coverage and must not be presented as verified no traffic.

## Initial metric registry

Create these metric IDs exactly. Subject scope and media direction are part of identity. Call/period aggregates combine like metric IDs only. Durations from different stream subjects are stream-time and must be labeled accordingly; they are not participant-time. Counters are differenced once at stream/transport scope before aggregation.

| Metric ID | Unit | Numerator / denominator | Scope and interpretation |
|---|---|---|---|
| `audio.inbound.loss` / `video.inbound.loss` | ratio | lost packets / (lost + received packets) | Ratio of valid interval counter sums; all-loss intervals permitted |
| `audio.outbound.remoteLoss` / `video.outbound.remoteLoss` | ratio | receiver-reported lost / expected packets | Only fresh remote reports with supported counter evidence; do not manufacture denominator from unrelated sender counters |
| `audio.inbound.jitter` / `video.inbound.jitter` | ms | sum(value × supported duration ms) / supported duration ms | Time-weighted fresh observations |
| `transport.iceRtt` | ms | sum(value × supported duration ms) / supported duration ms | Selected ICE path only |
| `audio.outbound.rtcpRtt` / `video.outbound.rtcpRtt` | ms | sum(RTT ms × supported duration ms) / supported duration ms | Fresh RTCP evidence; never silently mix with ICE RTT |
| `audio.inbound.bitrate` / `video.inbound.bitrate` / `audio.outbound.bitrate` / `video.outbound.bitrate` | bps | 8000 × delta RTP bytes / interval duration ms | Per-stream/encoding bitrate; rollup is mean over stream-time, not total call bandwidth |
| `audio.inbound.speechConcealment` | ratio | max(0, concealed − silent concealed sample deltas) / received sample delta | Required counters must exist; missing silent concealment is not assumed zero |
| `audio.inbound.jitterBufferDelay` | ms | 1000 × jitter buffer delay delta in seconds / emitted count delta | Ratio of sums |
| `video.inbound.freezeShare` | ratio | freeze duration delta ms / eligible measured video stream ms | Browser freeze definition, not custom event-time reconstruction |
| `video.inbound.decodeTime` | ms | 1000 × total decode time delta seconds / decoded frame delta | Cost per decoded frame |
| `video.outbound.encodeTime` | ms | 1000 × total encode time delta seconds / encoded frame delta | Cost per encoded frame |
| `video.outbound.cpuLimitedShare` / `video.outbound.bandwidthLimitedShare` | ratio | relevant limitation duration delta ms / sum of limitation duration deltas ms | Measured encoder limitation, not host CPU utilization |
| `video.inbound.fps` | fps | sum(FPS × supported duration ms) / supported duration ms | Fresh browser FPS; geometry is timeline state |
| `transport.rtpBytesSent` / `transport.rtpBytesReceived` | bytes | sum unique RTP byte deltas / null | Despite transport namespace, derived from RTP families once per direction; excludes adding transport counters again; not billable bytes |

The initial histogram definitions below are part of this proposed contract. All use duration weights in milliseconds and reject negative/nonfinite observations. Ratios additionally reject values above 1. They apply to valid interval values, not lifetime averages.

| Definition ID | Metrics | Inclusive upper bounds |
|---|---|---|
| `ratio-v1` | All ratio metrics | `[0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1]` |
| `delay-ms-v1` | All ms metrics | `[0, 1, 2, 5, 10, 20, 50, 100, 200, 300, 500, 1000, 2000]` |
| `bitrate-bps-v1` | All bps metrics | `[0, 10000, 25000, 50000, 100000, 250000, 500000, 1000000, 2500000, 5000000, 10000000, 25000000]` |
| `fps-v1` | FPS metrics | `[0, 1, 5, 10, 15, 24, 30, 60, 90, 120]` |

Byte-sum metrics have no histogram. These bounds are display/aggregation choices, not quality thresholds. All delay and FPS metrics use `duration-weighted-mean`; byte totals use `sum`; remaining metrics use `ratio-of-sums`. For min/max, retain the extrema of valid interval values, never extrema of cumulative counters. Ratio histograms use per-interval ratios with duration weights; their quantiles describe interval experience while their main value remains ratio-of-sums. A ratio-of-sums and a time-weighted mean of interval ratios can differ.

No default overall score is required in v1. Existing Observer score min/max/median can be shown as explicitly labeled source-summary metadata through a future additive section; they cannot be fed into fleet means/percentiles. A default native C++ score of 5 is not measured healthy quality.

## Input and impairment policies

The processor must commit a versioned policy fixture defining max supported sampling gap, fresh-report rules, mute/pause eligibility, impairment triggers/recovery, precedence of authoritative lifecycle sources, deduplication identity, clock-skew tolerance and cohort attribution. There are no hidden defaults. The following is a proposed initial policy, `conservative-v1`, for development and fixture interoperability; it is not an empirically validated quality model:

- Maximum supported interval is 10,000 ms. Longer gaps contribute no interpolated measurements. Repeated timestamps add no exposure. Remote metrics require an advanced report timestamp; they are not carried into later unchanged reports. No cross-client clock correction is invented; reject cross-client temporal correlation when measured clock uncertainty exceeds 1,000 ms or cannot be bounded.
- Explicit application membership/outcome events take precedence for application lifecycle; verified Observer lifecycle follows. Sample bounds establish observation only. Conflicting authoritative sources produce partial coverage and a conflict warning.
- A known muted, disabled, ended or intentionally paused track is ineligible for impairment evaluation. Missing context is recorded; lack of media alone never proves failure. Successfully measured network metrics remain visible while a media track is muted.
- Default impairment exposure uses interval classifications, not persistent inferred episodes: audio concealment ratio above 0.05; browser video freeze duration delta above zero; network loss above 0.05 or RTCP/ICE RTT above 400 ms; explicitly disconnected/failed connection state. Each category requires its own valid inputs. A valid negative interval ends that interval classification; no hysteresis or hidden recovery delay. Findings emitted by existing detectors retain their own lifecycle/policy instead of being relabeled as these digest rules.
- A nonzero cumulative freeze-duration delta is a video impairment observation for that sampling interval, but does not classify the entire interval as impaired participant time. Without exact temporal support it contributes measured stream freeze time and an uncertain observation; participant impairment duration for that evidence remains unknown. The same restriction applies to reconstructing exact impairment duration from concealment ratios. Exact state intervals and suitably timestamped detector evidence may support participant-time classification; state their source and temporal resolution.
- Multi-SFU records require verified identity and matching record/report timestamps for deduplication. When observations overlap but differ, retain source evidence, select using a committed deterministic source-precedence rule, and mark partial/conflicting coverage. Do not add them. Region means declared application/deployment region, not an inferred IP location. Multi-SFU/TURN cohort exposure uses a verified serving path; ambiguous intervals go to the unknown cohort.

This deliberately leaves some participant impairment duration unknown even when stream degradation is measured. The UI must still expose stream metrics and findings. A later policy may add validated temporal estimation, with an explicit policy ID and uncertainty semantics. Before production, confirm or revise the proposed policy against actual telemetry and desired sensitivity; update shared fixtures with every change. If a definition cannot be supported by available fields, mark that capability unavailable.

Each participant's assessed impairment time is a union of intervals where the policy could evaluate the category. Impaired time is the union of positive classifications within assessed time. Unknown time is eligible observed participant time outside assessed time. For `any`, impaired is the union of known positive categories; assessed is that positive union plus intervals where every applicable enabled category could be evaluated and none was impaired. Thus a known positive remains affected even if another category is unknown. Disabled/non-applicable categories are declared in capabilities/policy. Category durations overlap and must not be added together.

Application join input must have a versioned adapter with stable `attemptId`, tenant/call/client association when available, attempt start, outcome timestamp, outcome enum, and reason code. Define handling of attempts with no assigned call yet through a tenant-level attempt index; do not invent a synthetic successful call. Such attempts contribute to period joins but not call counts. Application/SFU context and feedback are optional inputs, never inferred facts.

## Storage and read boundary

Use existing deployment storage configuration, with independent logical roots for analytics and source archives. Recommended logical layout:

```text
<tenant>/analytics/v1/calls/<call-key>/manifest.json
<tenant>/analytics/v1/calls/<call-key>/revisions/<revision>/digest.json
<tenant>/analytics/v1/calls/<call-key>/revisions/<revision>/details/<resource-id>/<page>.json
<tenant>/analytics/v1/periods/<day-or-month>/<period-id>/manifest.json
<tenant>/analytics/v1/periods/<day-or-month>/<period-id>/revisions/<revision>/digest.json
```

Encode keys safely and independently from display names. Manifests contain schema version, current revision, digest location and provenance. Write immutable details/digest first, validate, then publish the manifest atomically. A reader pins revision for all detail pages. Failed processing preserves the previous usable revision and exposes job failure separately. Garbage collection of old revisions is a separate retention policy and must respect active readers.

The server read adapter exposes these logical operations; route spelling follows the host application's conventions:

- Get call digest by tenant and call identity.
- Get period digest by tenant, period and ID.
- Read detail by authorized resource ID, pinned digest revision and opaque cursor.
- Search calls by time range, call/room/client identity, impairment category and declared supported cohort filters; return rows referencing a call digest revision.
- Get the shared metric registry and policy descriptions by immutable ID.

Pages return `{ revision, items, nextCursor }`; `nextCursor: null` ends pagination. Search rows return call/room IDs, digest revision, known start/end, observed participant time, all-category impairment exposure and completeness. Search ordering and tie-breakers must be deterministic. Bound pages to 100 records by default, 500 maximum; the server may use smaller pages. Cursors bind filters, tenant and revision/snapshot. Reject mismatched/expired cursors explicitly.

Read states are `ready`, `pending`, `not-found`, `unsupported-version`, `failed`, and `forbidden`. An empty ready digest differs from a pending job. A stale usable revision may remain ready with a separate freshness warning. No credentials or source object URLs are exposed by default. Follow the existing server authentication and tenant isolation model.

## Required conformance fixtures

Use one shared fixture set for producer and UI: complete healthy call; impaired call with overlapping categories; all-loss interval; missing metric family; stale RTCP; reset/corrected counter; long sample gap; muted track; simulcast; reconnect with ID reuse; multi-SFU duplicate sources; summary-only call; absent/truncated summary sections; native producer without scoring coverage; open call; failed attempt before samples; late outcome/replacement summary; call crossing midnight/month boundary; incomplete period; revision mismatch; unsupported version; empty evaluated period.

Validate identical call/day/month results after retries and replacements, correct ratio-of-sums, no average-of-medians, unknown distinct from zero, and period deduplication. Compare direct period processing to rollups for additive quantities and histogram buckets. Quantiles remain labeled approximations. Schema, registry and fixture conformance is the handoff gate between the two implementations.
