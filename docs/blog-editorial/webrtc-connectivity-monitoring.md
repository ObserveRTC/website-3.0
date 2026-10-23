# Connectivity article: editorial and verification notes

Authoritative draft: `content/blog/webrtc-connectivity-monitoring.md`.
Status: unpublished (`draft: true`). No deployment, push, scheduling, analytics,
newsletter, existing-article, or automation changes are part of this work.

## Argument / section review order

1. Participant cannot join: establish the last demonstrated successful boundary.
2. Signaling: application evidence; no implemented signaling-delivery detector.
3. Gathering: empty inventory versus incomplete observation; traversal telemetry.
4. Checking: slow versus never established; worked corporate-network join.
5. DTLS: reported failure versus sustained waiting; worked handshake investigation.
6. Mid-call continuity: disconnected, failed, inbound asymmetry, path churn.
7. Recovery: recommendation, observed generation, ICE outcome, actual media return.
8. Integration: public API, full-block configuration, collection clocks, missing inputs.
9. Brief transport-quality next-post ending.

The piece is deliberately substantial to cover each implemented detector. Review
section by section before trimming behavior that affects operational interpretation.
All scenarios and measurements are hypothetical; no production incident is claimed.
Two original theme-aware SVGs illustrate evidence boundaries and recovery timing.

## Source baseline

Clean `/Users/riversidefm/src/client-monitor-js` working tree at
`ecbb77277306c35b32ad0d275e193a9687bf764e`; package.json version 4.11.0.
Inspected October 20, 2026. This is source/package metadata, not verification of
npm latest, an npm install, or production browser interoperability.

Read docs/DETECTOR_TAXONOMY.md, CONNECTIVITY_DETECTORS.md,
CONNECTION_DETECTORS.md, and relevant DETECTORS.md material. Contracts were checked
against all twelve Ice*/Dtls*/UnstableIce detector implementations and their tests,
ClientMonitor constructor defaults/config types, source/index exports,
SelectedIcePath, IceCandidatePairMonitor, IceTransportMonitor,
PeerConnectionMonitor, StatsGapDetector, native binding and README integration.

Taxonomy: nine Connectivity classes / eight issues; three nearby Telemetry
classes. No extra "connection lifecycle" diagnostic category was invented.
StatsGap is lifecycle telemetry. The blocked STUN/media trio is Transport Quality.

## Implementation takes precedence

The source docs contain statements that should not be copied as proven contracts:

- Empty candidates do not prove a device is offline; gathering state and policy matter.
- Host-only does not prove a STUN server was unreachable; absent relay does not prove TURN failed.
- Establishment failure stands down on nomination OR success, not both together.
  It does not require connectionState failed, or even connecting.
- ICE failure can fire on a never-working transport, despite continuity placement.
  Findings can overlap; the layers do not enforce global suppression.
- DTLS failure checks dtlsState directly, without proving ICE healthy first.
- ICE restart does not guarantee DTLS rekey or repair a failed DTLS transport.
- Candidate-pair byte deltas exclude connectivity checks; don't justify the stall
  detector by claiming consent responses must appear in these byte counters.
- Several reset branches don't close open issues. DTLS stall's fragment change
  resets its clock only. Stall losing outgoing traffic / inbound RTP resets its
  clock without resolution. Disconnected becoming failed stays open.
- A restart pending suppresses transport recommendations, not the separate
  never-established branch. Recommendations can recur; none performs a restart.
- The constructor replaces supplied detector config blocks; it does not deep-merge
  defaults. An omitted optional createEvent in an explicit block is falsy.
- Stats clocks can span gaps; docs' blanket claims that background sleep cannot
  contribute time are stronger than the timestamp-delta implementation supports.
- Generation counts are local observed counters; missing fragments conceal changes.
- Path kind uses the local candidate. A "direct" local classification doesn't
  establish that the remote endpoint isn't relayed.
- Closed peer connections cause several detectors to return early. Transport
  disappearance is resolved when observed during updates, not a blanket promise
  that every shutdown emits recovered issues.

These are editorial corrections to claims, not requested library fixes.

## External research

Primary contracts read via web:
- W3C WebRTC Recommendation (March 13, 2025): signaling, gathering, ICE/DTLS
  states, error 701, restartIce and negotiation behavior.
- W3C webrtc-stats: selectedCandidatePairId, candidate pair byte counters.
- RFC 8445: candidates, checks, nomination, restart credentials.
- RFC 8656: TURN allocation and authentication challenge context.
- RFC 5764: DTLS-SRTP key establishment.
- RFC 7675: consent freshness, distinct from media progress.

Practical first-party context, linked inline in article:
- BlogGeek.me, Handling WebRTC session disconnections: signaling/media distinction.
- rtcStats, WebRTC ICE failed: causes and how to diagnose it (August 20, 2026):
  inspect candidate-pair/check evidence. Did not copy its overly narrow statement
  that failed always means no pair ever passed a check.
- webrtcHacks, Power-up getStats for Client Monitoring: observation approach;
  explicitly distinguish its historical createClientMonitor API from current API.

No external article is used as the contract for today's detector APIs.

## Verification

- 12 detector suites, 153 tests passed using Jest --runInBand and a /private/tmp
  cache; includes threshold edges, missing inputs, reset and resolution cases.
- Extracted TypeScript article snippet compiled under strict/noEmit against
  current src/index exports and DOM types. No browser call or TURN service was run.
- Hugo draft build passed. Site check passed with zero broken local links/fragments;
  frontend service and tabs checks also passed without changing those features.
- Local reading preview: http://localhost:1313/blog/webrtc-connectivity-monitoring/.
- External article/spec pages were read; local checker doesn't validate every
  external URL or fragment, nor the GitHub availability of every pinned file.
- Normal production build passed; draft page absent and draft URL absent from
  generated HTML/XML/JSON/Markdown/text indexes. Final draft build and checks passed.
- Browser inspected desktop article and both figures across dark/light views;
  mobile prose at 390px had no document overflow. Figures were inspected at
  desktop width; mobile figure text was not separately visually verified.
- Preview remains open for review. Article is approximately 5,237 source words;
  site displays its rounded 25-minute reading label.

Runtime note: host Node is v26.0.0, while repository deployment targets Node 22.
No dependency install or lockfile change was made.

## October 23 editorial structure

Applied the author's case-first pattern across all twelve detector explanations:
human-readable scenario, detector subheading with pinned class source, a boxed
transition figure with short condition labels, and three mechanism paragraphs.
Kept event-only telemetry distinct from raised issues. Case 2 is titled
"taking the long way". The article now has fourteen numbered figures, each with
a text companion, including the original layer overview and recovery timeline.
Source contracts remain pinned to ecbb772; no newer API baseline was inferred.
The integration example and worked investigations remain outside the detector
case pattern. Draft build and site checks passed; event and issue figure layouts
were inspected in the browser. Earlier word-count/figure-count notes describe
the initial draft and are superseded by this structure.
