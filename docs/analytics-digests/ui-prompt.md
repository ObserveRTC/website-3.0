# Prompt: implement the analytics digest UI

Implement the ObserveRTC Stats Dashboard interface for the shared analytics digests. Work in the designated dashboard repository, preserving existing uncommitted work and following its repository instructions. The Hugo website is context, not the dashboard runtime. Reuse the dashboard's framework, styling, charts, navigation, API adapters and storage/security conventions.

Read the attached `digest-contract.md` first. It is the shared UI/processor contract. Read `webrtc-dashboard-research.md` for product rationale. Build the working interface, not just a mockup or plan. Existing local Digest/CallSummary shapes may require an explicit compatibility adapter; never silently reinterpret their scores, counts or missing values as the new contract.

## Establish the read boundary

Consume the shared runtime schemas/types, metric registry, policy descriptions and conformance fixtures produced for the processing component. If the processor is not available, build a fixture-backed adapter implementing exactly the same read operations, with a visible development data indicator. Keep fixture data out of production paths.

Use the existing authenticated server layer to access digest storage. Do not expose object storage credentials in browser code. Enforce tenant ownership and pinned revision/resource relationships on every route. Do not recalculate WebRTC counter deltas, detect impairment, merge summaries or scan raw call archives from the browser. Only presentation arithmetic explicitly defined by the contract—formatting, numerator/denominator division and histogram bucket interpretation—belongs in the UI.

## Implement the investigation flow

1. **Fleet overview:** day/month selection, UTC period boundaries clearly labeled, calls started, participant sessions started, observed participant minutes, call exposure minutes, join outcomes when available, category impairment exposure and source coverage. Explain the largest single-call peak rather than labeling it global concurrency. Distinguish verified empty periods, missing data and pending processing.
2. **Trends:** period buckets for usage and impairment. Preserve unavailable periods as gaps. Show measured exposure/denominators and unknown coverage in tooltips or accessible detail. Label ratios as percentages and durations consistently. No overall healthy score based on absent/default measurements.
3. **Affected calls:** show the processor's ranked worst-call list and a paginated searchable call list. Search by supported call/room/client identifiers, time range, impairment category and cohorts. Display affected participant time, assessed exposure, known call duration and completeness; link directly into the call investigator. Do not rank by a locally invented score.
4. **Cohorts:** show browser/OS/app/SDK/producer/region/SFU/TURN breakdowns supported by the response. Include unknown cohorts, denominators and sample/exposure size. Multiple filters require the server query; do not infer intersections from separate marginal aggregates. Do not imply causal regressions from small cohorts.
5. **Call overview:** lifecycle, participants, usage, category impairment exposure, issue categories, capabilities, coverage and freshness. Explain which facts came from samples versus selected summary sections. Summary-only calls remain usable with appropriate unavailable sections.
6. **Participant timeline:** load paginated detail lazily and show participant swimlanes with observed/missing intervals, connection states, relevant application events and findings. Align chart selection/zoom across participants and streams. Show uncertainty when events can only be localized to a sampling interval.
7. **Stream/path diagnostics:** separate inbound/outbound audio/video and individual encodings; show bitrate, loss, jitter, ICE versus RTCP RTT, freeze share, concealment, encode/decode cost and CPU/bandwidth limitation when measured. Display resolution/FPS changes, selected relay/protocol changes and resolved publisher/receiver comparisons. Never label per-stream average bitrate as total call bandwidth.
8. **Finding detail:** show affected subjects, interval, severity, origin, policy/algorithm, evidence and confidence. Distinguish observation from hypothesis. An unresolved finding is not proof of continuous impairment after the last valid evidence. Navigate to existing raw-evidence views through authorized server resolution when available.

## Presentation behavior

- Use the established ObserveRTC identity and accessible light/dark themes. Keep desktop and mobile navigation usable.
- Render measured zero as zero, unknown as unavailable, partial as partial. Explain why a capability is unavailable. Missing sections must never produce green healthy status.
- Provide separate loading, pending processing, missing digest, unsupported version, access denied, failed request, stale revision and empty-result states. Offer retry for failed reads without triggering processing implicitly.
- Pin a digest revision while reading its pages. On revision mismatch/expiration, offer a refresh and discard incompatible cached detail; never splice generations together.
- Describe each KPI in plain language through tooltips/help: subject, direction, units, numerator/denominator, coverage, measurement origin and policy. Approximate quantiles display bucket ranges or clear approximation labels.
- Preserve filters, time selection and navigation in URLs where practical. Avoid sensitive names in query strings. Support keyboard interactions, non-color status cues and accessible chart/table alternatives.
- Paginate and virtualize substantial detail lists. Abort obsolete requests, bound parallelism and prevent a slow participant read from blocking the whole overview. No unbounded browser fan-out across source objects.
- Do not invent costs, end-to-end latency, unique-human counts, measured user satisfaction or host CPU usage from these digests. Do not rebrand a native default score of 5 as measured quality.

## Verification and handoff

Use the shared fixtures to verify complete, impaired, partial, summary-only, native producer, unsupported-version and empty/pending cases. Test filter semantics, cursor/revision behavior, numerator/denominator formatting, unknown-versus-zero rendering, chart gaps, overlapping findings, midnight boundaries and server authorization. Inspect desktop/mobile layouts and both themes with actual fixture data. Do not add tests that merely duplicate trivial styling.

Deliver working routes/components/adapters, fixture mode, a field-to-screen mapping, screenshots or actual visual verification where available, and documented checks. Report any processor capabilities not yet available. Do not alter the shared schema to simplify a view without an explicit versioned contract update and updated producer fixtures.
