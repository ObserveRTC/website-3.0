# Baseline-only sample evaluation and revised digest/UI proposal

October 16, 2026. This supersedes the Observer-correlation scope and overview-first UI assumptions in earlier planning documents. It is a proposal and archive audit, not a deployed digest implementation.

## Scope agreed for this investigation

Use serialized raw ClientSample stat families and only event, metadata and issue types defined by base Client Monitor JS. Drop all `extensionStats`, custom event/metadata types, and all attachments for this baseline audit. Do not use custom room labels, version metadata, recording/upload telemetry or user-agent enrichment to explain QoS/QoE. Even an allowed type name is not authority for arbitrary custom payload fields; a production adapter must also project the verified base payload fields and nested structure.

Exclude Observer-generated detected conclusions. Mediasoup router reports and call-summary reports remain allowed separately as structural/lifecycle/context sources; none was supplied among these five files. Their possible future presence must not cause client findings to be double-counted.

All allowlists were derived from the clean local Client Monitor source at `ecbb77277306c35b32ad0d275e193a9687bf764e` (package declares 4.11.0; schema 3.7.0). The producer version/configuration of the uploaded archives is not established by that fact. No claims about a specific deployed release are inferred.

The read-only [audit script](audit-supplied-samples.py) creates [aggregate audit output](supplied-samples-baseline-audit.json). It does not copy source files, device labels, addresses, custom payload values or extension payloads into this repository. File hashes identify the inputs. The inventory includes field/type names for auditing exclusions; these names are not treated as quality evidence.

## What the actual archives show

All 1,472 JSON records parsed. Each file contains one client and one distinct call ID; all five call IDs differ. These are five partial call views, not five complete multi-client call archives. None contains `CLIENT_LEFT`.

| File alias / client prefix | UTC date | Records / observed span | Baseline evidence |
|---|---|---|---|
| A / 27b1ec80 | Oct 15 | 146 / 12m 53s | Outbound only; no sampled issue records; a fresh reported remote loss fraction reaches 40.625%; root score stays 5 |
| B / fd1603db | Oct 15 | 193 / 17m 11s | Outbound only; one keyed `dry-outbound-track` raise without a recorded resolution; root score stays 5 |
| C / fdc17746 | Sep 30 | 26 / 2m 05s | 6 recorded raises: congestion, uplink congestion, 3 transport-delay episodes, encoder bottleneck; no newly recorded completed video freezes in valid counter differences |
| D / 691b798a | Sep 29 | 440 / 36m 35s | 26 raises; 72 newly recorded completed video freezes totaling 74.497 video stream-seconds; capture, silence, congestion and delay findings |
| E / 172d5307 | Sep 29 | 667 / 55m 29s | 99 raises, including 73 decoder-overload and 10 encoder-bottleneck episodes; 2,767 newly recorded completed freezes totaling 762.893 video stream-seconds; synthesized playout delta 58.686 seconds across playout-report identities |

These totals subtract successive counters only within the same PC/family/stat identity and strictly increasing report timestamps. First observed cumulative totals are not treated as activity during the archive. Cumulative resets in A/B are excluded from ordinary differences and recorded as discontinuities. Stream-seconds are not unique client impairment seconds. Playout-report seconds are not added once per associated track, and the report does not infer whether distinct playout report IDs correspond to distinct physical devices.

The baseline filter excludes **5,529 extension entries, 1,704 custom events and 39 custom metadata records**. No custom issue types were present. Base `AUDIO_INPUT_DEVICE` metadata is present in A/B. No base `BROWSER`/OS metadata is present in these five files; custom `USER_AGENT_DATA` is excluded. Browser cohort charts would therefore be unsupported by this baseline-only dataset.

A/B have no inbound RTP/track/playout records. Their root score of 5 does not establish clean receiving quality. E's 73 decoder episodes and 762.893 recorded freeze seconds are substantial receiver evidence even while its typical network measurements are relatively modest. Raw media outcomes deserve their own checks rather than relying on network alarms or an overall score.

## Evaluation of the proposed hierarchy

One canonical call digest is the right parent artifact. It should contain the call-level check results and a client-results map, plus references to larger evidence resources when needed. The client page is a projection of that same generation. There is no need for an independently calculated client digest that could disagree with its call page.

Recommended flow:

1. A completed-call trigger or lifecycle authority identifies the call to process. Do not infer completion from the final sample or an absent `CLIENT_LEFT`.
2. Process all available client archives for that call; optionally use provided router/summary context. Save `digests/calls/<callId>.json` within the authorized tenant/storage scope.
3. Daily processing discovers missing/stale days and reads call digests/contributions overlapping each day. Save `digests/daily-summaries/YYYY-MM-DD.json`.
4. Monthly processing reads daily contributions and the identity/provenance needed for exact rollups. Save `digests/monthly-summaries/YYYY-MM.json`.

The daily runner cannot discover a missing day's calls from that same missing daily summary. It needs a call digest index or call inventory. Checking only for missing files also misses corrected call digests: record input revisions and rebuild stale days/months. A month should not sum daily distinct calls/client counts without deduplication. Separate calls started in a period from calls contributing quality evidence in it.

The paths are implementation details. The essential contract is a persisted, versioned collection of **questions checked, their outcomes, the supporting measurements and their scope**.

## A check-result contract shared by call and client views

Each row should be an answerable diagnostic question, not just the name of a metric or an unqualified healthy label.

```typescript
type QualityCheckResult = {
  checkId: string;
  definitionVersion: string;
  question: string;
  category: 'received-audio' | 'received-video' | 'capture-send'
    | 'transport-connectivity' | 'timing-sync' | 'data-confidence';
  outcome: 'passed' | 'failed' | 'not-assessable' | 'not-applicable';
  basis: 'raw-measurement' | 'recorded-client-issue' | 'context-event';
  scope: { callId: string; clientId?: string; peerConnectionId?: string; trackId?: string };
  explanation: string;
  limitation?: string;
  // Defined, typed measurements with units. No arbitrary extension payloads.
  measurements: Array<{ metricId: string; value: number; unit: string }>;
  recordedEpisodeCount?: number;
  assessmentCoverage: { measuredMs?: number; eligibleMs?: number; reasonCodes: string[] };
  evidence: Array<{ sourceId: string; recordNumber: number; statId?: string; timestamp?: number }>;
  // An internal navigation intent, resolved by the UI, not arbitrary embedded HTML.
  destination: { section: string; clientId?: string; peerConnectionId?: string; trackId?: string };
};
```

These are proposed fields, not existing ClientSample fields. A separate check definition fixes the exact rule, required inputs, eligible context, source baseline and interpretation. `passed` means the named rule passed over stated observed evidence, not universally good QoE. For a recorded-issue-only check, no reported issue is not enough to pass a symptom question without assessment coverage. Unknown and inapplicable use neutral icons, never a green tick or red failure.

Call results roll up client results without changing their basis: fail if any in-scope client fails; pass only where the relevant assessment population is sufficient and all evaluated clients pass; otherwise remain partial/not-assessable. Always show counts such as “1 failed; 3 clients not supplied.” Positives remain visible when the call archive is partial.

Check validity and severity are separate. One measured dropped frame or synthesized sample may answer a strict measurement question, but is not automatically a severe user problem. Prefer a neutral measurement row under the relevant check when significance cannot be established.

## Sections and questions to include

| Section | Checks/questions and evidence |
|---|---|
| Received audio | Dense non-silent concealment? Recorded long interruptions? Excessive synthesized playout? Buffer delay plus time stretching? Dry inbound audio? Preserve duration/count distinctions |
| Received video | Completed freezes? Recorded frozen/choppy flow? Decoder overload? Assembly/decode stall? Failed keyframe recovery? Render discrepancy? Sustained quantizer degradation with codec/context? |
| Capture and sending | Capture falling behind configured FPS? Encoding falling behind source? Sender RTP stall/dry track? Capture source lost? Suspicious microphone silence? Loopback input risk? CPU/bandwidth limitation? |
| Transport and connectivity | ICE/DTLS establishment and failures? Disconnect evidence? Directional congestion? Reported/derived directional loss? RTT by source? Selected path changes/restarts? STUN/transport progression? |
| Timing and synchronization | Paired AV playout skew? Capture-to-render/end-to-end latency only if an explicit supported measurement exists; otherwise not assessable |
| Data confidence | Parse/identity consistency? Missing initial context? Repeated/stale reports? Counter discontinuities? Missing resolutions? Sampling/collector gaps? Unsupported detector/configuration coverage? |

Do not omit unavailable questions from the client page; show why they could not be answered. Useful explanations include “No received video in this archive,” “Pairing not declared,” “Interruption raw counters not serialized,” and “Missing assessment/configuration provenance.”

Every expanded result should show: what was checked; what was observed; why the rule passed/failed; what it does and does not establish; and an internal link to the exact audio/video/transport/event evidence section. Call and client pages reuse the same result objects.

Daily/monthly views summarize these check IDs with failed-client/call counts, assessed/unknown counts, observed measurement severity and recurrence. They lead into the same call/client results. They should not independently run browser-metric rules or invent another overall quality classification.

## Bugs and gaps verified in the inspected Client Monitor source

[Probe results](client-sample-bug-probes.json) were generated by [isolated synthetic execution](probe-client-sample-bugs.cjs) of unmodified source transpiled in memory. No browser, network or production ingestion was involved. These demonstrate source behavior; the producer versions of the supplied archives remain unknown.

| ID | Finding | Reproduction / consequence | Classification |
|---|---|---|---|
| B1 | All-loss inbound interval becomes zero loss | Received packets stay 100; lost goes 0→10. `deltaFractionLost` is 0, although supported interval fraction is 1. The PC aggregate also skips zero-received intervals | Confirmed calculation defect |
| B2 | Payload bitrate subtracts headers from an already payload-only byte counter | Over one second, delta bytes=1,000, headers=100, retransmissions=0: result 7,200 bps instead of 8,000 bps under standard RTP payload-byte semantics | Confirmed accounting defect relative to W3C byte definitions |
| B3 | Duplicate outbound report retains the previous elapsed interval | Repeating a report timestamp leaves `deltaTime=1000` from the previous interval instead of clearing the interval. Stateful consumers can repeatedly process old evidence | Confirmed freshness defect |
| B4 | Missing outbound raw fields can be re-emitted as old measurements | After `framesEncoded=10`, a later report omitting the field still produces `framesEncoded=10` in `createSample()` because `Object.assign` retains it | Confirmed sample freshness defect |
| B5 | Unavailable encode-cost calculation retains the preceding value | After measuring 100 ms/frame, a later report lacking the required counters leaves the old 100 ms/frame available | Confirmed derived freshness defect |
| B6 | Metadata association fields accepted by the type are discarded | `addMetaData({type, peerConnectionId, trackId, ssrc, payload, timestamp})` buffers type/payload/time but drops the top-level association fields | Confirmed API-to-sample projection defect; payload associations still survive if explicitly included there |
| G1 | Audio interruption counters are intentionally kept live-only | `totalInterruptionDuration=2` exists on the monitor but not its sample. Sample replay loses all sub-threshold interruption measurements | Serialization/analysis capability gap, not necessarily an unintended implementation bug |
| G2 | Remote receiver-reported loss is unavailable to the current interval aggregate when `packetsReceived` is missing | All supplied remote-inbound records omit `packetsReceived`, but all have `fractionLost`. A fresh reported fraction 0.2 yields undefined `deltaFractionLost` | Capability/aggregation gap. Preserve receiver-reported fraction as its own observation; do not invent a packet-weighted denominator |

For B2, standard `bytesSent` excludes RTP header/padding; those are separately reported as `headerBytesSent`. Retransmitted payload is a subset of `bytesSent`. See [W3C RTP byte definitions](https://www.w3.org/TR/webrtc-stats/#dom-rtcsentrtpstreamstats-bytessent).

Source locations: [inbound loss guard](/Users/riversidefm/src/client-monitor-js/src/monitors/InboundRtpMonitor.ts:545), [outbound accept and byte accounting](/Users/riversidefm/src/client-monitor-js/src/monitors/OutboundRtpMonitor.ts:177), [metadata buffering](/Users/riversidefm/src/client-monitor-js/src/ClientMonitor.ts:996), [remote-inbound delta handling](/Users/riversidefm/src/client-monitor-js/src/monitors/RemoteInboundRtpMonitor.ts:104).

## Observed archive limitations that are not proven client bugs

- B's score remains 5 alongside a dry-outbound issue. This is a score/evidence inconsistency to investigate, not proof that the current JS score calculator produced it. A/B provide no component scores and no verified producer/scoring configuration.
- D/E contain substantial freeze evidence but no `video-flow-disrupted` issue. Detector enablement, source baseline, screen-share/foreground/pause context and historical rules are not established. Do not infer a confirmed detector miss from these files alone.
- Open issue raises at the archive end are right-censored. No final sample/client departure was supplied. They are not all unresolved production faults or failed recoveries.
- A/B contain backwards outbound counters across three encoding identities. These are epoch/reset boundaries, not valid negative traffic and not proven corruption.
- Repeated RTP/source/remote report timestamps are present. Repeated raw reports can be legitimate; reusing stale derived evidence as fresh is the defect.
- No exact call completion or full participant inventory is established by one client file. Call-level results must expose partial population coverage.

## UI proposal

Default the evaluation sketch to **Call Analytics → call → Quality checks**, because that is the workflow being designed. Keep Monthly Analytics and Daily Analytics at the top, and keep Load room directly accessible. The call page has a call/client scope selector and persistent links to check sections.

Use six grouped sections with expandable rows and four explicit outcomes: passed, finding/failed, not assessable and not applicable. On expansion, show the finding, its source and limitations, and a working jump to the relevant evidence panel. Selecting a client changes the scope, not the calculation. Monthly/daily pages summarize the same checks and open that same call result.

Use measured examples from the supplied files, but label the prototype as a local sample evaluation. Do not invent multi-client attendance, room metadata, browser cohorts, Observer conclusions or full-month statistics. “Load room” can demonstrate navigation, but the room identity of these files is not inferred from excluded attachments.

## Complete built-in issue-type coverage

The section catalog must retain every built-in issue type below, including unavailable and disabled-by-default checks. Related tags can share a user-facing question, but expanded details and the digest preserve the original type. Non-issue telemetry such as codec/resolution/mute/path changes supplies context rather than extra failures.

| Section | Built-in issue types |
|---|---|
| Received audio | `audio-interruption`, `audio-jitter-buffer-stress`, `concealed-samples`, `synthesized-audio` |
| Received video | `decoder-bottleneck`, `frame-assembly-stalled`, `inbound-video-playout-discrepancy`, `pixelated-video`, `stuck-decoder`, `video-decoder-overloaded`, `video-flow-disrupted`, `video-recovery-failed` |
| Capture and sending | `capture-source-lost`, `cpulimitation`, `dry-outbound-track`, `encoder-bottleneck`, `loopback-audio-input`, `rtp-sender-stalled`, `silent-audio-source`, `video-capture-bottleneck` |
| Transport and connectivity | `blocked-inbound-media-transport`, `blocked-outbound-media-transport`, `blocked-stun-requests`, `congestion`, `downlink-congestion`, `dtls-handshake-failed`, `dtls-handshake-stalled`, `ice-connection-failed`, `ice-disconnected`, `ice-establishment-failed`, `ice-transport-stalled`, `no-available-ice-candidate`, `transport-delay-degraded`, `transport-demux-stalled`, `transport-loss-sustained`, `unstable-ice-path`, `uplink-congestion` |
| Timing and synchronization | `av-desync` |
| Receiving media flow (audio or video) | `dry-inbound-track` |
