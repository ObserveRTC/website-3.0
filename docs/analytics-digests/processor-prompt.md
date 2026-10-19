# Prompt: implement the call processing and digest component

Implement a production-ready processing component that reads ObserveRTC call archives and saves call and UTC day/month analytics digests. Work in the ingestion/processing repository designated for this task. The ObserveRTC Hugo website is documentation context, not the runtime host.

Read the attached `digest-contract.md` first. It is the shared producer/UI contract. Read `webrtc-dashboard-research.md` for rationale. Implement the contract; do not substitute a summary of the research or stop at a design proposal. Preserve existing uncommitted work and follow repository instructions.

## Inspect before changing

Identify current sample contracts and producer versions, archive layout, raw/normalized Observer summary adapters, multi-SFU handling, scheduled jobs, storage clients, authentication boundaries and current digest work. Distinguish committed/released behavior from local work in progress. Existing types named Digest or CallSummary are not automatically this new contract.

Reuse the project's language, runtime, storage and scheduling conventions. Prefer a bounded-memory worker/CLI plus callable processing functions when no service infrastructure exists. Do not add a database, queue, framework or cloud dependency merely for convenience. Do not modify ClientSample or Observer CallSummary to force them into the analytics schema.

## Deliver the shared contract first

Create or consume a versioned shared contract package containing runtime schemas, generated/static types, metric registry, immutable histogram definitions, policy descriptions and conformance fixtures. Avoid separately maintained producer/UI copies. If package sharing is unavailable, check in an explicitly versioned artifact with a reproducible generation command and checksum.

Resolve the policy details required by the contract from actual source interfaces and available telemetry. Commit concrete units, legal ranges, histogram bounds, freshness/gap rules, lifecycle precedence, impairment/recovery rules and identity/deduplication rules. Document justified choices. Do not invent supported capabilities or raw fields; unavailable evidence produces unavailable outputs. Changes to the descriptive contract must be explicit and reflected in both implementation prompts/fixtures.

## Implement processing

1. Discover inputs through existing call indexes/manifests and adapters. Build an immutable source inventory using version IDs or content hashes. Support samples plus optional summaries, Observer events, application join events and router data. A summary-only call must produce an honest partial digest.
2. Normalize each input format once. Sort/reconcile out-of-order records within bounded limits. Deduplicate records and multi-SFU client observations using verified identities. Preserve provenance and uncertainty where overlap cannot be resolved. Never sum all per-SFU counts as if independent.
3. Build lifecycle-aware participant, track/encoding and transport identities. Reconstruct selected ICE paths using retained on-change metadata only when the producer's semantics support it. Link publishers/subscribers using verified signaling/resolver evidence. Leave unsupported relationships unknown.
4. Compute validated per-stat deltas and registry metrics using stat timestamps. Handle missing inputs, counter corrections/resets, stale remote reports, gaps, mute/pause context and simulcast. Do not treat missing as zero or carry stale observations indefinitely. Keep stream-time, participant-time and call-time separate.
5. Produce participant/stream/path facts, timeline records, observations/hypotheses and category impairment exposure. Do not infer precise freeze event boundaries from sampled cumulative counters. Record evidence and calculation policy for every finding.
6. Save the call digest and paginated detail resources. Bound resource size; stream large archives rather than loading a webinar's entire history into memory. Stable IDs and deterministic ordering are required.
7. Produce day/month digests from per-call contributions and attempt indexes, preserving period boundaries, late outcomes, exact call deduplication, coverage and cohort semantics. Keep internal contribution indexes as needed. Month processing must not sum daily distinct-call counts or active-at-end counts. No average-of-averages/medians/percentiles.
8. Publish immutable outputs before switching the current manifest. Support idempotent retries, late source arrivals, replacement summaries, backfill and call-to-period invalidation. Updating an existing contribution replaces it; it never adds the same call twice. Protect publication against concurrent workers with the storage system's supported conditional-write/locking mechanism.
9. Expose job state, input counts, rejected/duplicate records, processing failures, duration and output revision through existing observability conventions. A failed reprocess preserves the last valid revision. Do not log sensitive source contents or credentials.
10. Provide the contract's authorized read operations or a storage adapter that the existing API can consume. Do not put heavy archive processing on a UI read path.

## Verification and handoff

Add meaningful unit/integration tests using the shared fixtures. Verify retry determinism, concurrency-safe publication, late replacement invalidation, summary normalization, ratio math, rollover across midnight/month boundaries, incomplete periods, permissions and bounded resource handling. Use storage mocks for deterministic failure tests; state clearly whether real object storage was tested.

Deliver working code, migration/compatibility notes for any existing digests, schema/registry artifacts, a minimal runnable example, commands for processing one call and backfilling a period, and instructions for scheduling/reprocessing. Include a small fixture archive and its saved outputs so UI development can proceed without production data.

Report what was implemented, exact checks run, supported input versions, remaining unavailable capabilities and operational requirements. Do not deploy or alter production storage retention unless separately authorized.
