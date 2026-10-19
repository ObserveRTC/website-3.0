# WebRTC dashboard research and ObserveRTC digestion requirements

Research date: October 15, 2026. Internal planning analysis; no public site changes.

## Recommendation

Build an evidence pipeline that supports three questions: Is the service degrading? Who was affected? What evidence explains a reported call problem?

The valuable output is a searchable, comparable set of session facts and impairment intervals, backed by raw evidence. A collection of bitrate graphs alone cannot answer these questions.

Keep raw ClientSample archives, Observer findings, and final summaries. Add a versioned analytics digest with per-client/per-track interval measurements and mergeable aggregates. Keep the analytics implementation in the dashboard/ingestion deployment; the Hugo website does not need a database or analytics backend.

## Competitor capabilities

This is a public documentation and source review, not hands-on testing of authenticated vendor consoles. Availability can depend on plans, SDKs, and media topology. Vendor quality models are not interchangeable.

| Product | Publicly documented capabilities | Requirement to take from it |
|---|---|---|
| [Twilio Video Insights](https://www.twilio.com/docs/video/troubleshooting/insights) | Fleet room/participant usage and quality trends; browser/OS segmentation; issue tags; participant summaries; per-track publishing bitrate/loss/RTT graphs in 10-second intervals; aggregate receiving bitrate | Fleet → affected call → participant → track navigation; retain metric direction and interval |
| [Daily analytics](https://www.daily.co/products/enterprise-analytics/) | Session/participant/track metrics, client logs and REST access; enterprise BI; freeze and audio degradation views; network disruptions; CPU-related limitations; user timelines and issue clusters | Show experienced impairments alongside transport evidence, application logs, and cohort comparisons |
| [Agora Call Inspector](https://docs.agora.io/en/realtime-media/agora-analytics/build/explore-and-analyze-data/call-search) | Call search with duration, freeze-rate and user-count filters; call overview; user-specific metrics/events and experience investigation | Search by symptoms and impact, not only IDs; summarize large calls before showing every participant |
| [Vonage Inspector](https://developer.vonage.com/en/opentok/tools/inspector_doc) | Session diagnostics, users/errors/events, audio/video bitrate, loss, latency, codec, resolution and FPS; publisher/subscriber filters and chart zoom | Synchronized charts and events; distinguish publishing and receiving legs and SFU topology |
| [Vonage Insights](https://developer.vonage.com/en/opentok/guides/insights?source=opentok) | Project usage, quality distributions and error rates; location/endpoint filters; GraphQL access; connection/publish/subscribe failure analysis | Count attempted operations and outcomes separately from measured media quality |
| [LiveKit Cloud Analytics API](https://docs.livekit.io/deploy/admin/analytics-api/) | Sessions and participants; quality and bitrate histories, bandwidth, connection minutes and connection metadata | Expose digest facts through an API shared by dashboard and external reporting |
| [CyaraRTC](https://cyara.com/products/cyarartc/) | Browser-based testing, production monitoring, network/device diagnostics, quality analysis and alerts | Separate passive production analytics from active preflight/synthetic tests |
| [rtcStats](https://rtcstats.com/) | SDK/file ingestion; rates and quality estimates; cross-session facts; observations, deductions and session investigation; API and embedded viewer | Separate raw measurements, calculations, observations, and diagnostic hypotheses |

The former testRTC watchRTC URL currently redirects to CyaraRTC. Treat older watchRTC screenshots and callstats.io material as historical references unless independently verified. Do not infer current features or availability from them.

Twilio Voice Insights is also useful for warning lifecycle design: [SDK quality events](https://www.twilio.com/docs/voice/voice-insights/api/call/details-sdk-call-quality-events) expose raised and cleared warnings using repeated observations. Its telephony semantics and thresholds should not become universal video-call defaults.

## What ObserveRTC already offers

The website describes Stats Dashboard as an archive-based investigator for rooms, calls, participants, quality timelines, transport state, RTP and issues. Optional mediasoup router records supply additional SFU relationships. See [dashboard documentation](../content/docs/stats-dashboard/_index.md).

Local source reviewed:

- Observer: `/Users/riversidefm/src/observertc-observer-js/src/summaries/CallSummary.ts`, checkout HEAD `0c1befa79ced76b3e7a5ea33e50224b9b7d18f40`.
- Stats Dashboard: `/Users/riversidefm/src/observertc-stats`, checkout HEAD `323a1b28553758edafaa0abd0d4211c9e13de9ea`. This checkout includes uncommitted digest-related files; these are work in progress, not a released capability claim.
- Website sample inventory, metrics/formula reference, Observer detectors and SFU integration documentation.

The inspected Observer summary has opt-in `clients`, `issues`, `turnServers`, and `scores` sections. It carries lifecycle timestamps, bounded issues/client IDs, score min/max/median/sample count, and application enrichments in `attachments`. It does not contain per-track metric histories, impairment durations, participant minutes, cohort breakdowns, or attempted joins by default. Missing sections mean not collected. Caps and truncation must remain visible.

The dashboard work in progress reads a normalized/merged summary model, not exactly the Observer's raw summary type. Its digest already covers call counts, joins, call duration totals, issues, TURN clients, call-start buckets and worst calls. Preserve this normalization boundary; do not assume similarly named fields have identical semantics.

A current score rollup weights each call's representative score by score sample count. When that representative value is a median, this is a weighted mean of call medians. It is neither the fleet median nor the mean of the underlying score readings. Also, score sample count is not necessarily elapsed time. Label existing results precisely; use time exposure or mergeable distributions for new quality measures.

## What must be digested

“From samples” below means raw fields are present when the producer/browser supplies them; it does not guarantee coverage across producers or browsers. Many calculated live-monitor values are not serialized and must be recomputed. Track sample records contain only a limited projection.

| Dashboard question | Inputs | Digest output and limitation |
|---|---|---|
| How much is the product used? | Call lifecycle; client join/leave and stable IDs | Calls, participant sessions, call minutes, participant minutes, concurrency. Client IDs do not establish unique people |
| Can people join? | Application join attempts/results; ICE/DTLS transitions; first media events | Join success/failure, reasons, setup duration, first media delay, percentiles. Samples alone miss attempts before monitoring starts |
| Are calls stable? | Connection state transitions; signaling events; issue intervals | Reconnect/drop counts and disconnected seconds. Intentional leaves require application context |
| Is audio impaired? | Inbound RTP concealment/sample counters, discard counts, jitter-buffer counters, playout stats where emitted; mute/activity context | Concealment ratios, jitter-buffer delay, time stretching, affected seconds. Silence or zero energy alone does not prove failure |
| Does video freeze? | Inbound `freezeCount`, `totalFreezesDuration`, decoded/rendered/dropped frames, dimensions/FPS | Freeze counts/time, eligible stream seconds, frame rates and geometry changes; preserve unavailable coverage |
| Is video bandwidth constrained? | Outbound target/actual bitrate, `qualityLimitationReason`/durations; selected-pair available bitrate | Bandwidth-limited seconds and bitrate trends. Available bandwidth is an estimate, often shared at transport scope |
| Is the endpoint struggling? | Encode/decode duration and frame counts, CPU limitation durations; optional runtime telemetry | Encode/decode cost per frame, CPU-limited time. These do not measure OS-wide CPU utilization |
| Is the network degraded? | Inbound and remote-inbound loss/jitter, RTCP RTT, selected-pair ICE RTT | Directional interval loss, jitter distributions, RTT histories; identify measurement origin and freshness |
| Is TURN involved? | Transport → selected pair → candidates, relay URL/protocol; selection changes | Relay exposure, path changes, UDP/TCP distribution. Candidate presence alone does not prove selected relay use |
| Is one publisher affecting many receivers? | Resolved publisher/subscriber graph; aligned endpoint stats; Observer findings | Affected receivers, common onset, publisher evidence and confidence. SSRC equality alone is insufficient across SFUs |
| Is a release/browser/region worse? | Browser/OS/app/SDK version, declared region, SFU ID and metrics | Cohort denominators, affected participant-time, distributions and comparison periods. Persist metadata explicitly |
| What infrastructure is involved? | Mediasoup router records, signaling IDs, server metrics | SFU/transport correlations and hotspot ranking. Client samples do not provide server CPU, queue occupancy or authoritative egress billing |
| Did users notice? | Feedback event/rating and call/client association | Feedback distribution and correlations. A technical score is not measured user satisfaction |

Use [the ClientSample inventory](../content/docs/schema/clientsample.md) and [monitor formulas](../static/reference/monitor-fields-and-formulas.md) for exact fields and serialization. Use [Observer SFU integration](../content/docs/observer-js/sfu.md) for relationship requirements. [W3C WebRTC statistics](https://www.w3.org/TR/webrtc-stats/) defines browser statistics; actual availability still needs runtime verification.

## Calculation contract

1. Key time series by tenant, call, client instance, peer connection, stat ID and lifecycle epoch; attach track/encoding/transport relationships. Preserve changes rather than joining unrelated streams after reconnects or ID reuse.
2. Use each stat's own timestamp for counter deltas. Keep sample creation and ingestion timestamps separately. Remote reports may update more slowly than samples. Reject duplicate intervals and identify stale reports.
3. Missing data is unknown. Counter decreases may indicate resets or loss-estimate corrections; mark the interval and retain evidence. Do not turn every negative delta into a valid zero-loss observation. Bound interpolation and split at substantial gaps.
4. Store units and measurement scope. Jitter/RTT typically arrive in seconds; counters such as decode time and jitter-buffer delay are cumulative. ICE RTT is not RTCP RTT, one-way delay, or glass-to-glass latency.
5. Preserve transport and encoding scopes. Do not sum transport bytes with their RTP bytes. Sum outgoing simulcast layer traffic for sent-byte accounting, but never add layer resolutions or treat every encoding as a separate participant.
6. Build impaired intervals with explicit start/end, subject, evidence, threshold configuration, recovery policy, algorithm version, and unknown periods. Coalesce overlaps for participant-time impact while retaining individual stream evidence.
7. Store cohort denominators and coverage alongside every ratio. Report unknown separately from healthy. Preserve summary truncation, incomplete archives, open calls and unavailable detector/scoring coverage.
8. Separate observation from hypothesis. “Publisher fault suspected” should link the affected receivers and corroborating publisher evidence. It should not become an unqualified root-cause label.

Recommended derived formulas, evaluated only on valid intervals:

- Bitrate: `8 × Δbytes / Δseconds`, with byte scope documented.
- Inbound loss fraction: `Δlost / (Δreceived + Δlost)` when deltas are valid and denominator is positive. This proposed analytics definition permits all-loss intervals; it differs from a guarded expression in the reviewed Client Monitor implementation that requires positive received packets.
- Jitter-buffer delay: `1000 × ΔjitterBufferDelay / ΔjitterBufferEmittedCount`, denominator positive.
- Encode/decode cost: `1000 × ΔtotalEncodeOrDecodeTime / ΔframesEncodedOrDecoded`, denominator positive.
- Speech concealment proxy: `max(0, ΔconcealedSamples − ΔsilentConcealedSamples) / ΔtotalSamplesReceived`, when required inputs are available. Not an intelligibility measurement.
- Video freeze share: `ΔtotalFreezesDuration / eligibleObservedVideoSeconds`. State eligibility rules and field coverage; do not substitute full call duration for every stream.
- Participant impairment share: union of impairment intervals for that participant divided by eligible observed participant time. This avoids double counting simultaneous track faults.
- Join success: successful join attempts divided by eligible terminal attempts; report pending, canceled and unknown outcomes separately under an explicit policy.

Do not copy a competitor's thresholds blindly. Agora's documented freeze definitions vary by platform, and Twilio's cumulative video tags differ from its repeated-sample voice warnings. Retain native browser freeze observations separately from application-defined stalls. See [Agora's glossary](https://docportal.shengwang.cn/en/Agora%20Analytics/aa_call_search_terms) and the Twilio sources above.

## Proposed analytics artifacts

These are conceptual records, not existing ObserveRTC schema fields.

| Artifact | Minimum contents | Why it exists |
|---|---|---|
| Call facts | IDs, lifecycle, participant counts, failure outcomes, issue categories, coverage, source references | Fast call search and overview |
| Participant facts | Client instance and optional user association, join attempts/outcomes, durations, versions/cohorts, impairment exposure, score provenance | Support investigation and cohort analysis |
| Stream intervals | Direction, media kind, track/encoding links, timestamps, deltas/rates, geometry, limitations, validity | Recompute graphs and distributions without opening every raw record |
| Path intervals | Transport and selected-pair links, relay/protocol, RTT origin, changes, validity | Explain network and TURN changes |
| Findings | Scope, interval, severity, type, evidence, affected subjects, confidence, detector version | Correlated investigation and alerts |
| Period digest | Counts, exposure sums, numerator/denominator pairs, mergeable histograms/sketches, coverage, bounded worst-call references | Efficient day/month fleet queries |

Preserve raw archives for evidence and reprocessing. Persist normalization/algorithm versions and a source revision or watermark so rebuilt digests are explainable. Make recomputation idempotent and account for late arrivals and replacement summaries. Do not silently sum repeated multi-SFU observations of the same participant.

For each numeric metric retain valid count, observed duration, appropriate sum/weight, min/max and a mergeable distribution where quantiles matter. Never roll up percentiles by averaging percentiles. A capped worst-call list is useful navigation, not a population distribution.

Cross-midnight calls need two views: calls started in the period, and media/participant exposure occurring in the period. Split exposure at period boundaries. UTC storage buckets can remain canonical; local-day queries need boundary-aware interval data.

## Dashboard priorities

First, extend the current digest with data coverage, affected-call/participant counts, impairment seconds, issue categories, score provenance and accurate denominators. Keep call minutes separate from participant minutes, joins from unique users, and biggest-call peak from global concurrency.

Second, connect fleet cards and symptom filters to a call investigator. Its default view should show participant swimlanes with join/leave, disconnects, mute/pause context, audio concealment, video freezes and Observer findings. Selecting an interval should align network, RTP and encode/decode charts. Allow publisher/receiver comparison through resolved track links.

Third, add cohort comparisons by app release, browser/OS, declared region, SFU and selected TURN path, including sample sizes and unknown coverage. Alert on sustained population regressions and meaningful affected exposure; one low score should not page an operator by default.

Add active preflight tests, infrastructure metrics, user feedback and optional runtime instrumentation as separate inputs when needed. MOS-like scoring, AI-generated diagnosis, and estimated costs should follow validated evidence and clearly stated models.

## Completion criteria for the digestion design

- A support engineer can locate a call by ID or symptom and see who was affected, when, and which evidence supports a hypothesis.
- A fleet metric can be traced to numerator, denominator, coverage and source records.
- A day rolled into a month gives the same additive totals as direct processing; quantile approximation is explicit.
- Missing fields, stale RTCP, counter corrections/resets, sample gaps, simulcast, reconnects, late records, truncation and multi-SFU duplicates have explicit handling.
- Join failures before the first sample are represented through a separate attempt contract.
- Native C++ default scores are not presented as measured healthy quality; producer/version capability is retained.

This review did not run browser calls, benchmark ingestion, validate production archives, or exercise vendor consoles. Existing source and schema coverage establishes implementation candidates, not end-to-end tested support.
