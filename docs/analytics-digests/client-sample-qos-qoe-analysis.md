# ClientSample analysis for QoS and QoE digests

Scope update: the user subsequently restricted analysis to base Client Monitor inputs and supplied real archives. See [the baseline-only evaluation, revised check contract and bug list](supplied-samples-evaluation.md). Observer-detected conclusions below are background from the earlier scope, not inputs to the revised proposal.

Review date: October 16, 2026. Internal research and proposed digest requirements; no dashboard or monitoring runtime changed.

## What the dashboard should help an engineer decide

The main unit should be a **client experience problem with evidence**, connected to its track, direction, possible contributing conditions, and other affected clients. Issue occurrences, call counts and mean scores are supporting measurements.

The investigation should answer:

1. Did this client have trouble receiving audio/video, producing media for others, or staying connected?
2. What was observed, how severe was it, and how much measured media was affected?
3. Was the likely contributing condition in capture, encoding, transport, delivery, assembly, decoding or playout?
4. Was this isolated to a receiver, shared across subscribers to one publisher, or correlated across independent calls?
5. Is the same problem becoming more common per eligible client or media exposure, by day and month?

QoS describes delivery and pipeline conditions. QoE evidence describes what was happening to the media presented to a client, or what could plausibly affect it. Neither is a subjective satisfaction measurement. A network warning is not automatically a media symptom, and the absence of a network warning does not establish a good experience.

## Evidence and baseline

This analysis traced actual serialization, live monitor calculations, detector update paths, issue lifecycle buffering, selected tests, and Observer correlation/summary collection. The accompanying [source audit](client-sample-source-audit.json) records field inventories, detector references, source hashes and six mechanically checked findings.

| Source | Inspected baseline | Meaning |
|---|---|---|
| Client Monitor JS | Clean local checkout `ecbb77277306c35b32ad0d275e193a9687bf764e`; package declares `4.11.0` | Source baseline, not a claim that this package is published or deployed |
| Client sample contract | `schemaVersion = "3.7.0"` in that checkout | Shape version does not establish detector/configuration parity |
| Observer JS | Clean local checkout `466ec13594ce151ef5d90dd4c6c35d498a7847ea` | Source baseline for correlation and summaries |
| Website reference | Previously documented pinned Client Monitor source `0f08bd5d…` | Historical comparison only; public documentation baseline has not been changed |

No production archive was supplied for this review. Two local replay fixtures were inspected structurally: `degrading-camera.jsonl` has 18 replay records over 85 seconds; `stuck-decoder.jsonl` has four over six seconds. They are replay inputs, not a representative sample population. Existing detector tests were read for edge-case intent, not executed. This does not validate live browser support, field coverage in your deployment, detector accuracy, or monthly prevalence.

## ClientSample contains several different kinds of evidence

### Raw snapshots

`peerConnections[]` groups browser/adapted raw reports. Their counters support interval calculations; gauges describe an instant or browser-specific recent window. They are not a sample-period average.

| Family | Useful QoS/QoE evidence | Important boundary |
|---|---|---|
| `inboundRtps[]` | Received/lost packets, jitter, bytes; receive/decode/render/drop counts; freeze/pause counters; audio concealment, time stretching, jitter buffer; processing and playout timestamps | Receiver evidence for a particular RTP stream; not the publisher's complete audience experience |
| `outboundRtps[]` | Sent bytes/packets; source links, simulcast IDs; encoded/sent frames, QP, encode cost; limitation durations, target bitrate and feedback | What this endpoint sent toward its immediate peer, commonly an SFU |
| `remoteInboundRtps[]` | Remote receiver reports about this endpoint's outbound RTP: loss, jitter, RTT | In an SFU deployment the receiver report typically describes publisher → SFU, not every subscriber's last-mile delivery |
| `remoteOutboundRtps[]` | Remote sender report counters and timestamps for inbound RTP | Supporting source-report evidence; not a complete end-to-end timing instrument |
| `mediaSources[]` | Capture frames/FPS/geometry; audio energy and duration; optional echo-cancellation statistics | Does not say whether a camera or microphone was supposed to be active unless context is available |
| `mediaPlayouts[]` | Synthesized audio duration/events, played duration, delay and sample count | A playout device/report can be shared by multiple tracks |
| `iceTransports[]`, `iceCandidatePairs[]`, `iceCandidates[]` | ICE/DTLS state, selected path, relay/protocol, connectivity checks, RTT, bandwidth estimates | Candidate existence is not selected-path use; successful ICE is not successful media delivery |
| `codecs[]` | Codec and format details, clock rate and channels | Necessary to interpret QP and other codec-dependent evidence |
| `dataChannels[]` | State, messages and bytes | Data-channel delivery evidence, not an audio/video experience metric |

The audited schema has 70 fields in `InboundRtpStats`, 43 in `OutboundRtpStats`, and nine in `MediaPlayoutStats`, including identity/timestamp/attachments fields. Field count is not capability count. Optional fields require actual emission and suitable interval support.

### Buffered issues and events

`clientIssues[]` carries discrete issue reports. Stateful raises and resolutions can reconstruct **detector episodes**, even if the raw snapshots are too coarse to reproduce the detector's decision.

`clientEvents[]` carries lifecycle and observations when integration/configuration supplies them. Examples include track addition/removal, mute/unmute, ICE/connection changes, producer/consumer pause/resume, codec/resolution/layer changes, tab visibility and collection gaps. An enum value alone does not guarantee every integration emits it.

`clientMetaItems[]` can supply browser/OS/engine/platform and capture-device/settings/error context. Metadata may be sent once and drained from the next sample. It needs a retained metadata timeline. `attachments` and `extensionStats` may carry application-defined facts; there is no universal implied app-version, room, location, topology or user identity contract.

### Scores at multiple scopes

Samples include scores/reasons at client, PC and inbound/outbound track scopes. Track records themselves contain only `id`, `kind`, `timestamp`, `attachments`, `score`, and `scoreReasons`. They do not serialize every track property or calculated metric.

Store the five quality dimensions separately when supported: transport/PC stability, received audio, received video, sent audio and sent video. A received-audio problem and an outbound-encoder problem mean different things even if they yield the same client score. The default client score combines dimensions nonlinearly; child score reasons do not automatically appear in root `scoreReasons`.

## Three levels of what can be digested

| Level | Definition | Suitable use |
|---|---|---|
| Recomputed measurement | Formula from fresh serialized fields with known identity and time | Loss, bitrate, decode cost, concealment ratio, counters and distributions |
| Recorded detector finding | A sampled issue emitted by the producer's live detector | Preserve actual detection policy and richer local context; count episodes and track their lifecycle |
| Correlated conclusion | Combine participants, relationships and temporal evidence | Publisher involvement, receiver isolation, delivery mismatch, population/infrastructure association |

These levels can corroborate one another. They must retain separate origins. A processor rule at a five-second cadence must not be presented as the same detector decision that ran locally every second.

## QoE-oriented findings

### Audio: separate short concealment, longer interruptions and output-device synthesis

| Question / family | Serialized evidence and existing issue | What to digest | Limit |
|---|---|---|---|
| Is received speech being reconstructed? | Inbound `concealedSamples`, `silentConcealedSamples`, `totalSamplesReceived`, optional `concealmentEvents`; `concealed-samples` | Non-silent concealment fraction, event rate, affected receiving clients, track identity and recorded episodes | Dense short concealment is different from a long silent dropout; do not collapse both into one audio score |
| Did longer audio interruptions occur? | `audio-interruption` issue payload contains `interruptionCount`, `interruptedMs`, average interruption and accumulator evidence | Recorded interruption episodes; retain initial/final observed counters as snapshots, not increments | Live `interruptionCount` and `totalInterruptionDuration` are not in this checkout's ClientSample serialization; raw replay cannot recover them |
| Did the output device synthesize audio? | `mediaPlayouts[].synthesizedSamplesDuration`, `synthesizedSamplesEvents`, `totalSamplesDuration`; `synthesized-audio` | Synthesized/played duration ratio and event count once per playout report; associated tracks and receiving client | Track issues may repeat the same device evidence. Never sum a shared device's duration once for each track |
| Is the jitter buffer under combined stress? | Target/actual jitter-buffer delay plus inserted/removed samples; `audio-jitter-buffer-stress` | Buffer delay, time-stretch fraction, simultaneous evidence and recorded episodes | Deep buffering alone can mean successful adaptation; stretching alone can reflect clock correction |
| Are audio and video out of sync? | `estimatedPlayoutTimestamp` on explicitly paired streams; `av-desync` payload identifies paired video, signed skew and direction | Audio-ahead/audio-behind findings, skew distribution and detector episodes | Raw sample does not universally preserve pairing or pause context; two arbitrary tracks cannot be compared |
| Was the intended microphone silent? | Source energy/duration; `silent-audio-source`; settings/device/context events where emitted | Digital silence vs below-threshold vs no-sample findings, device association and affected senders | Silence is not a fault without capture intent; local live detector has more context than track samples |
| Is the input a loopback source? | `loopback-audio-input` includes matched label pattern and capture context | Configuration-risk finding tied to source; suspected echo separately | Device label match does not prove audible echo |
| Is echo suspected across clients? | Observer `AUDIO_ECHO_SUSPECTED`, source/receiver levels, relationship/context evidence | Suspected source, affected relation, correlation/follow evidence, ambiguous direction | Not an acoustic recording or an objectively confirmed echo diagnosis |

The current local concealment detector integrates excess non-silent concealment above a 5% allowance until a 400 ms bucket fills. It is not simply “any five-second interval above 5%.” The interruption detector integrates excess interrupted time above a 2% allowance until 500 ms accumulates. These are inspected defaults, not recommended production thresholds. Both depend on the producer's applied configuration.

A concrete consequence: a two-second audio dropout and a 25-second open issue are both possible in one episode because recovery drains the accumulator slowly. Report **measured interruption milliseconds**, **detector episode duration**, and **estimated affected experience** separately. Do not label all three “bad audio duration.”

### Video: distinguish continuity, sharpness and pipeline failure

| Question / family | Serialized evidence and existing issue | What to digest | Limit |
|---|---|---|---|
| Has the picture frozen or become choppy? | `framesRendered`/`framesDecoded`, `freezeCount`, `totalFreezesDuration`; `video-flow-disrupted` with `state: frozen/choppy` | Frozen vs choppy episode counts, affected receiving clients, reported completed-freeze count/time, measured coverage | Local detector uses separate flow windows and foreground/pause/screen-share guards; raw replay is conditional |
| Is the picture heavily compressed? | `qpSum`, decoded frames, codec; `pixelated-video` | Codec-specific mean QP/normalized-QP evidence and sustained recorded findings | Not a visual image-quality measurement; QP alone does not tell whether content was unreadable at its presented size |
| Are frames failing to reach presentation? | Received/rendered counters; `inbound-video-playout-discrepancy` | Frame skew/drop evidence, receiving track, foreground eligibility and episodes | Overlapping pipeline counters are not an exact per-frame queue; do not treat skew as guaranteed user-visible freeze time |
| Are packets arriving without complete frames? | RTP packets increase, assembled/received frames do not; `frame-assembly-stalled` | Assembly stall evidence, packets during stall, duration threshold and stream | Distinguish this from transport silence and from a complete-frame decoder stall |
| Are frames assembled but decoding not progressing? | Bytes/received frames/keyframe/PLI/decoded evidence; `stuck-decoder` with `variant` | Assembly/decode/unknown variant, elapsed stalled evidence and recovery attempts | A stuck picture is a symptom; hardware decoder defect is not proven |
| Is the decoder losing throughput? | Received, dropped, decoded frames; `decoder-bottleneck` | Accepted-frame supply vs decoded progress and recorded findings | Reviewed implementation subtracts dropped frames and handles burst catch-up; naïve decoded/received rates are not equivalent |
| Is decode cost too high for the frame budget? | Decode time, frames, FPS, low-loss condition; `video-decoder-overloaded` | Decode cost/frame, budget utilization, network quietness and affected receivers | This differs from the decoder-bottleneck throughput finding; CPU utilization is not measured |
| Did recovery requests fail to restore video? | PLI/keyframe/render evidence; `video-recovery-failed` | Recovery-failure findings, PLI count and stalled evidence | Feedback counts are not quality failures by themselves |
| Is the source producing fewer frames than intended? | Source frame deltas plus configured capture settings/context; `video-capture-bottleneck` | Expected vs produced FPS, source geometry and sender findings | Low source FPS without configured intent can be expected or content-dependent |
| Is encoding falling behind capture? | Source frame progress vs selected highest active encoding; `encoder-bottleneck` | Source/encoding shortfall, limitation reason and sender findings | Never sum encoded frames across simulcast layers and compare that sum with one capture stream |
| Did capture end unexpectedly? | `capture-source-lost`, optional event | One-shot loss report with track and device context | No resolved lifecycle by default; source end does not itself establish the user's intent |

The local flow detector distinguishes a stop from repeated shorter freezes. Pixelation uses codec-aware QP, with default raise/recovery 0.62/0.52 and an 8-second sustain. Local defaults are implementation evidence only. Unknown codec, screen-share exclusions and context-dependent scoring must remain explicit.

**Freeze timestamps require special care.** Browser freeze and pause durations are updated when a frame renders again; the counter's increase can describe time before the latest sampling interval. Consequently, `delta freeze duration / sample interval` is not always a valid bounded interval share. A long freeze can be recognized after midnight and relate to the preceding day. Keep event-accounting time separate from attributed experience time. Do not clamp an increment to the interval and silently lose duration. See the [W3C freeze/pause definitions](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-totalfreezesduration).

An ongoing stop may not yet appear in the completed-freeze total. Present both completed browser freeze measurements and detector stopped/choppy episodes, without summing their durations.

## QoS, connectivity and service evidence

| Family | What samples support | How it relates to client experience |
|---|---|---|
| Directional loss | Fresh inbound and remote-inbound packet counters; recorded `transport-loss-sustained` | Risk/condition; correlate with actual receiver continuity and recovery evidence |
| Round-trip delay | RTCP stream RTT and selected ICE path RTT, separately; `transport-delay-degraded` payload names origin | Conversation responsiveness evidence, not measured mouth-to-ear latency |
| Uplink congestion | Available outgoing bitrate, packet send delay, bandwidth-limitation evidence; `uplink-congestion` | Publisher delivery constraint; prioritize receivers actually affected |
| Downlink congestion | Receive throughput history, video jitter-buffer delay and recorded `downlink-congestion` | Receiver-side constraint hypothesis; application layer changes can also affect throughput |
| Legacy congestion | `congestion` | Compatibility finding; do not independently count the same period as a second new incident when directional findings describe it |
| Encoder limitation | `qualityLimitationDurations`, reason, resolution changes | CPU/bandwidth constrained operation; adaptation may preserve acceptable received media |
| Client codec processing pressure | Encode/decode time and hardware implementation evidence; `cpulimitation` | Local media processing estimate; not OS-wide CPU or memory telemetry |
| Setup and reachability | ICE/DTLS/path events and states; `no-available-ice-candidate`, `ice-establishment-failed`, `ice-connection-failed`, `dtls-handshake-failed`, `dtls-handshake-stalled`, `blocked-stun-requests` | Distinguish failure to establish from interruption of an existing media session |
| Connection interruption | `ice-disconnected`, transport state/event evidence | Connection evidence; use media progress to assess impact and avoid equating transient disconnection with a lost application call |
| RTP/transport progression | `ice-transport-stalled`, `rtp-sender-stalled`, `transport-demux-stalled`, `blocked-outbound-media-transport` | Localize where progress stops rather than labeling every zero-bitrate interval a network outage |
| Path stability/recovery | `unstable-ice-path`, restart events/recommendations, selected-pair changes | Supporting context. A direct-to-relay transition may be a successful recovery, not a new quality fault |
| Codec, resolution, layer, mute and pause changes | Buffered events and metadata when emitted | Explanatory context; do not automatically count these as incidents |
| Collection gaps and tab visibility | `STATS_COLLECTION_GAP`, `TAB_VISIBILITY_CHANGED`, repeated timestamps and archive gaps | Measurement/eligibility evidence. Collector delay is not proof of a network fault |

`blocked-inbound-media-transport` exists in the source, but its detector is disabled by default in this inspected baseline because its premise is unsuitable for browser RTCP multiplexing. A class/type in the package is not justification to make it a headline KPI.

A full application join-success denominator is still unavailable from samples alone. Failures before Client Monitor starts cannot appear in its archive. A peer-connection setup duration is a different metric from click-to-room-join or first-useful-media time.

## What can be calculated directly

Use differences from the same stat lifecycle and its own timestamp. Preserve raw units and explicit conversion. `dt` below is positive seconds; negative/missing/reset/corrected counters require classification, not blanket replacement with zero.

| Measurement | Calculation | Interpretive boundary |
|---|---|---|
| RTP throughput | `8 × delta bytes / dt` | Identify whether payload, header or retransmission bytes are included |
| Interval inbound loss | `delta lost / (delta lost + delta received)` with supported deltas and positive denominator | All-loss is possible; corrected loss estimates are not ordinary monotonic counters |
| Packet discard | `delta discarded / (delta discarded + delta received)` under the chosen documented model | Late/early discard is separate from packets never received |
| Non-silent concealment | `max(0, delta concealed − delta silentConcealed) / delta totalSamplesReceived` | Require both counters for a fully qualified measurement; the live code falls back to zero for missing silent concealment, which the digest should disclose rather than hide |
| Time stretching | `(delta inserted + delta removed) / delta totalSamplesReceived` | Fraction of samples, not events per second; missing subcounters are not measured zero |
| Jitter-buffer delay/target/minimum | `1000 × delta respective delay / delta emitted count` | Milliseconds per emitted sample/frame, not cumulative elapsed call delay |
| Audio RMS | `sqrt(delta totalAudioEnergy / delta totalSamplesDuration)` | Source/received signal energy; no recorded waveform or speech-content understanding |
| Playout synthesis | `delta synthesized duration / delta played duration` | Device-scoped shared evidence must be deduplicated |
| Encode/decode cost | `1000 × delta total time / delta frames` | Frame-weighted ratios; average compute cost is not total frame pipeline latency |
| Produced / encoded / decoded / rendered FPS | `delta respective frames / dt` | Use matching stage and stream; distinguish from browser's last-second FPS gauge |
| Mean QP | `delta qpSum / delta decodedOrEncodedFrames` | Codec units first, versioned normalization second |
| CPU/bandwidth-limited share | `delta relevant limitation duration / delta total limitation durations` | Encoder operation time; denominators can differ from fully eligible participant time |
| Mean RTT | `delta total RTT / delta RTT measurement count` | Measurement-weighted RTT where the fields support it; keep ICE/RTCP and stream direction separate |
| Interframe timing variation | Delta frame-gap moments using the relevant rendered-frame count and valid window | Check counting convention and source implementation; not a general jitter metric |

PSNR and corruption-probability fields exist in the serialized types but should be optional experimental evidence until actual producer support and semantics are checked. Do not present normalized QP as perceptual fidelity or PSNR as a user satisfaction score.

## Information that is lost or only conditionally available

1. **Intermediate collection states.** Samples are snapshots. A path or gauge can change and recover between samples. Buffered events can preserve some transitions; raw gauges cannot recover their exact extrema or duration.
2. **Audio interruption raw counters.** The monitor consumes Chromium extra fields but omits them from `InboundRtpStats` and `createSample()`. Recorded issue payloads can survive; sub-threshold interruption totals cannot reliably be recovered from those issue reports.
3. **Detector coverage/configuration.** There is no standard sampled inventory of enabled detectors, thresholds, `inputsUnavailable`, collection window geometry or config changes. No issue does not establish that the detector ran and judged the interval clean.
4. **Declared track context.** `setContext()` merges local context; `createSample()` does not serialize that context. Pause/content type, AV pairing and presentation size may be partially reconstructed from complete integration events, but not universally.
5. **Track/encoding association.** Inbound RTP has `trackIdentifier`. Outbound RTP reaches the track through `mediaSourceId → mediaSources.trackIdentifier`; if that relationship is absent, or a binding exists only in local integration state, do not invent a join.
6. **Issue updates.** `_updateIssue()` emits a local event but does not queue a new sampled issue. Initial and resolved payloads do not form a continuously sampled severity series.
7. **Metadata initial state.** Once-only metadata, first/on-change ICE metadata, or lifecycle records can be missing when capture starts late. Unknown initial state must remain unknown until established. The metadata type allows top-level association fields, but this `addMetaData()` path buffers only type, payload and timestamp; resolve associations from the actual emitted payload, not from optional type members that may never be written.
8. **Producer/version identity.** The exported schema version is not itself a mandatory root field in each sample. Library version, native-vs-JS support and detector/scoring policy need an archive manifest or declared metadata. Equal schema versions do not prove equal collection capability.
9. **SFU/room relationships and user intent.** Room ID, application session intent, publisher/subscriber mapping and deployment ownership are integration facts. `callId` and `clientId` themselves are optional in the type; archive identity needs explicit precedence/conflict handling.
10. **User satisfaction and exact output.** No waveform, visible presentation recording, verified audible speaker output, speech intelligibility, subjective rating or true end-to-end latency is provided by these counters.

## Reconstruct issue history correctly

Stateful raise records carry `type`, `key`, optional payload and timestamp. A matching `<type>-resolved` closes an episode. The same key can be reused in a later episode, so identity needs **client instance + key + raise occurrence**, not key alone. Track/PC IDs come from the payload where present; do not assume every issue has both.

Required parser behavior:

- A resolution is not a new occurrence. Count the raise once and preserve resolution/reason separately.
- Reassemble across sample boundaries and midnight. A raise and resolve can occur between raw snapshots yet both appear in the next buffered sample.
- One-shot reports have no required end time. Do not invent an interval for `capture-source-lost` or treat every report as active until call end.
- Unknown keys/custom issue types remain visible but do not get silently assigned built-in semantics.
- Preserve orphan resolution, missing raise, duplicate, open-at-archive-end, unknown sampling mode and out-of-order records.
- `sendResolvedIssuesToServer: false` suppresses keyed resolution tracking; `includeIssueInSample: false` can suppress a detector's output entirely. Local callbacks are independent of archived evidence.
- A close may be recovery, pause, end of track, backgrounding, unavailable input or forced client teardown. Use `endedReason` and a separate `recovered`/`stood-down`/`censored`/`unknown` outcome. A `-resolved` suffix is not enough to count successful recovery.
- Preserve raw raised/resolved timestamps and payload duration separately. They can use a wall clock while detector sustain uses stats time.

Use four distinct durations where available: (a) recorded detector-open time, (b) measured media impairment such as completed freeze/interruption duration, (c) digest-classified observation time, and (d) unknown time. Do not add or substitute them. Overlapping issue-open intervals can be unioned as **time with open findings**, but that is not automatically time with actual impaired media.

## Sender problems and receiver impact are different populations

Every finding should carry:

- **Reporting client:** endpoint whose sample or detector emitted the evidence.
- **Affected receiver(s):** endpoint(s) whose receiving media shows a relevant symptom.
- **Associated publisher:** verified source of the affected track, if resolved.
- **Suspected contributing domain:** capture, encoding, uplink, SFU/forwarding, downlink, assembly, decoder, playout, unknown.
- **Scope and support:** isolated, shared publisher, call-wide, cross-call or cohort-associated; evidence and uncertainty.

For example, a publisher's encoder fault is a local send-quality finding. If three linked receivers have frozen/choppy pictures, the digest should show one publisher-associated problem and three affected receivers. Four client issue records may support that problem, but neither four independent incidents nor one affected person is an adequate description.

Useful patterns supported by Observer source:

| Pattern | Evidence | Conclusion strength |
|---|---|---|
| One receiver affected, peers receiving the same track are not | Resolved links and contemporaneous receiving findings | Receiver-specific condition is more plausible; not proof of last-mile fault |
| Several receivers of one publisher affected | `IssueFanOutDetector` | Shared publisher/forwarding association; publisher itself may be healthy |
| Publisher send-path issue and multiple receiver symptoms coincide | `PublisherFaultCorroborationDetector` | Stronger two-sided corroboration of publisher involvement; unrelated simultaneous faults still need consideration |
| Publisher sending but linked receivers dry | `TrackDeliveryMismatchDetector` | Delivery mismatch; actual component attribution needs topology and context |
| Independent calls deteriorate together | Call/Observer concurrent issue detectors, SFU/relay context | Shared infrastructure hypothesis; avoid concluding a specific SFU solely from client symptoms |
| A browser/OS population has elevated issue prevalence vs controls | `ClientPopulationIssueDetector` | Cohort association with denominator/control evidence, not causal proof |

Observer detectors require registration; some require nonempty configured issue-type lists and a remote track resolver. Current source comments/examples in publisher corroboration still mention historical names such as `freezed-video-track` and `capture-bottleneck`; the inspected Client Monitor emits `video-flow-disrupted` and `video-capture-bottleneck`. Validate exact emitted tags in configurations. A detector configured against a historical name can remain silently uninformative.

The core CallSummary `issues` section collects **call-level** `call-issue` events. It is not automatically the complete ClientSample `clientIssues` history. Observer-wide findings also need their own archive feed. Keep these three streams separate and link them by evidence; do not count them as three independent impairments.

## Better digest requirements for day and month

### Use a quality lens, not one mutually exclusive whole-client status

A client can have poor received audio, clean received video, constrained sent video and unknown transport coverage in the same call. It can be both an affected receiver and a problematic sender. A single “good / QoS only / QoE” partition loses the information needed to investigate.

For each client session retain:

- Directional/media quality summaries: received audio, received video, sent audio, sent video, connectivity, with separate coverage.
- Recorded episodes by actual issue type and subtype (`frozen`, `choppy`, assembly/decode variant, AV direction).
- Recomputed measurements with units, valid denominators and uncertainty.
- Sender association and affected receiver references, without assuming impact.
- Source detector/configuration provenance where known; measurement capability independently from detector-reporting capability.
- Measured severity: worst sustained evidence, total measured impairment, longest supported episode, recurrence and recovery outcome. Never manufacture a common severity scale from incompatible payload fields.

### Aggregate each issue family independently

For every day/month and each issue family, retain:

| Digest field concept | Meaning |
|---|---|
| `reportingClientSessions` | Distinct sessions emitting the issue, deduplicated within that period |
| `affectedReceivingClientSessions` | Distinct receiver sessions with symptom evidence; separate from associated publishers |
| `assessableClientSessions` | Sessions meeting the named issue policy's minimum evidence/eligibility requirement |
| `knownPositiveClientSessions` | Positive evidence even if full-session assessability is unavailable |
| `unknownAssessmentClientSessions` | Ineligible or unassessable split by explicit reason, rather than all counted healthy |
| `affectedCalls` / `affectedRooms` | Distinct call/room identities containing the relevant evidence |
| `newEpisodes` / `ongoingEpisodes` / `recoveredEpisodes` | Lifecycle counts with explicit onset and period-boundary semantics |
| `openFindingMs` | Unioned detector-open time under named scope, excluding unsupported inferred end times |
| `measuredImpairment` | Typed measurement: frozen stream milliseconds, interrupted audio milliseconds, concealed sample count, etc.; never one generic duration |
| `mediaExposure` | Matched denominator: received-video stream time, audio samples/played duration, connected time, etc. |
| `severityDistribution` | Family-specific distributions and sample/exposure weights; versioned histogram definitions |
| `receiverFanOut` | Affected vs assessed subscribers for resolved published tracks, plus topology coverage |
| `corroboration` | Shared-publisher, single-receiver and cross-call findings with evidence references |
| `qualityScores` | Optional component/directional score distributions with measurement/policy provenance; no healthy fallback from missing support |

Positive evidence remains a positive finding even when the denominator cannot be trusted. Show “12 clients reported; assessment coverage unknown” instead of silently calculating “12 / all clients” as a valid failure rate.

Monthly unique sessions/calls/rooms must be deduplicated from identity-bearing contributions, not added from daily distinct counts. Define sessions with evidence occurring in the period separately from sessions started in the period. Episodes crossing midnight contribute open time to each relevant day, onset only to their start day, and resolution outcome only where it occurs. Do not use discovery time as onset time when backlog arrives.

Counters updated on completed events need a different accounting policy from exact lifecycle timestamps. Where exact cross-boundary allocation is not supported, store reporting-period totals and an attribution-uncertainty marker. Never proportionally spread a freeze across days and describe it as exact.

Cohort comparisons need issue-specific assessability, platform, producer, policy and direction. A browser that does not emit a required stat must not appear healthier because its detector is blind. Show both absolute affected counts and rates with matched denominator; compare configurations and traffic mix before interpreting a regression.

## Worked example: why raw issue totals are inadequate

Consider one publisher and three receivers in the same call. The publisher emits `encoder-bottleneck`; two receivers emit `video-flow-disrupted` with `state: choppy`; a third has usable continuous video evidence. One of the two affected receivers also emits `audio-jitter-buffer-stress`.

A useful digest says:

- Two receiving client sessions have video symptom evidence; one also has audio buffer-stress evidence. Do not add those populations into three distinct affected clients.
- One publishing client has a production constraint. Do not classify it as a third client with a confirmed received-video symptom.
- Four client issue episodes support this investigation, but the common publisher relationship can group some into one problem cluster. Grouping does not erase the raw episode records.
- The receiver denominator is three only if the third receiver's relevant evaluation coverage is known. If that receiver merely emitted no issue, report two known positives with uncertain assessment coverage.
- Publisher corroboration is available only if links, configured type lists and temporal evidence support it. Otherwise retain a shared-source association as a hypothesis.
- Two completed freeze increments totaling six stream-seconds do not establish six participant-seconds, particularly if the receivers' freezes overlap or actual timing is unknown.

Suppose this call crosses midnight. Its session identity belongs once in the monthly distinct-session set; each day includes only its supported exposure and relevant issue overlap. An episode raised on day one and resolved on day two is one episode, not two. A third-party rule grouping it into a correlated finding must not add another measured freeze to the media totals.

## What this changes in the proposed dashboard

The previous sketch improves access but still compresses the analysis too far:

- “Clients with QoE symptoms” hides whether people could hear, see or stay connected, and whether the issue concerns their own reception or the media they publish.
- A single whole-session classification masks mixed quality and partial evidence. Replace it with directional/media summaries and per-family assessability.
- The issue table needs affected receivers, reporting senders, severity evidence, recurrence, recovery and cross-client spread. Occurrence count alone is a weak prioritizer.
- “CPU limitation” and “packet loss” belong beside the media symptom they help explain. They should not compete with “frozen picture” as equivalent end-user outcomes.
- Monthly analytics should identify recurring quality patterns and cohort changes. Daily analytics should identify onset clusters and allow hour → room → call drilldown.
- Keep the front-page room loader. A quality report must not obstruct the direct support workflow.

A more suitable first screen would have three quality areas—**Audio experience**, **Video experience**, **Connection continuity**—with an **Issues to investigate** list beneath them. Each area reports affected receivers, issue-specific measurable population, dominant symptoms and meaningful measured severity. Sending constraints and transport conditions appear as corroborating evidence, with an explicit separate view for technical QoS. This is a recommendation from source capabilities, not a final layout specification.

## Prioritized collection and processing work

### Can be delivered from sufficiently complete existing samples

- Parse and deduplicate keyed issue episodes, including subtype and resolution outcome.
- Compute packet/byte/frame/energy/limitation metrics and native freeze totals with correct scope and timing.
- Reconstruct supported lifecycle, metadata, codec/layer/path timelines.
- Preserve component/directional score histories and available child reasons.
- Build issue-family day/month contributions and searchable room/call/client references.
- Present recorded evidence with honest unknown coverage, without claiming exact replay or complete assessability.

### Requires explicit serialization or integration additions for stronger claims

1. A versioned producer/capture manifest: producer/version, schema version, collection/sample cadence, algorithm/config hash and enabled issue reporting.
2. A detector assessment timeline: evaluated/no issue, positive, unavailable, disabled and ineligible, with reason. Absence of positive issue reports cannot substitute for this.
3. Versioned track context changes: content type, pauses, pairing, intended capture parameters and presentation context. Use semantic data, never serialize DOM objects.
4. Raw interruption counters in a supported schema/extension contract if population-wide dropout metrics are wanted, including events below detector thresholds.
5. Periodic/final episode evidence snapshots when severity progression or interruption totals are needed; current local updates are not continuously archived. Snapshots need identity/revision so they are not added as fresh events.
6. Verified publisher/subscriber and SFU ownership relationships, with their validity intervals.
7. Persisted Observer call-level and observer-wide findings, distinct from client issues and summaries.
8. Application attempt/outcome and feedback events only for the metrics that actually require them; these are separate from WebRTC media quality.

### Validate against real archives before setting production quality policies

Measure field presence by producer/browser, actual sample gaps and cadence, available issue types, raise/resolve pairing completeness, context coverage, shared playout IDs, track mapping coverage, native score availability, clock alignment and truncated capture boundaries. Trace a small set of known user complaints through the whole chain. Calibrate thresholds using those examples instead of substituting one generic 5%/400 ms policy for existing detectors.

The earlier descriptive digest contract is a draft. Before implementation or further UI commitment, revise its generic impairment-time model, fixed policy assumptions, per-family eligibility, event-accounting time, sender/receiver roles and recorded-vs-recomputed origin to reflect these findings. Existing implementations of that draft need a compatibility review rather than silent semantic changes.

## Source map

- [Client sample serialization and buffering](/Users/riversidefm/src/client-monitor-js/src/ClientMonitor.ts:788)
- [Serialized field types](/Users/riversidefm/src/client-monitor-js/src/schema/ClientSample.ts:1)
- [Issue type union](/Users/riversidefm/src/client-monitor-js/src/ClientMonitorIssues.ts:1)
- [Issue registry and resolution semantics](/Users/riversidefm/src/client-monitor-js/src/utils/IssueRegistry.ts:1)
- [Inbound RTP counters and extras](/Users/riversidefm/src/client-monitor-js/src/monitors/InboundRtpMonitor.ts:385)
- [Inbound track context](/Users/riversidefm/src/client-monitor-js/src/monitors/InboundTrackMonitor.ts:35)
- [Outbound track context](/Users/riversidefm/src/client-monitor-js/src/monitors/OutboundTrackMonitor.ts:25)
- [Concealment detector](/Users/riversidefm/src/client-monitor-js/src/detectors/ConcealedSamplesDetector.ts:1)
- [Audio interruption detector](/Users/riversidefm/src/client-monitor-js/src/detectors/AudioInterruptionDetector.ts:1)
- [Audio synthesis and shared-device semantics](/Users/riversidefm/src/client-monitor-js/src/detectors/AudioPlayoutSynthesisDetector.ts:1)
- [Flow-state detector](/Users/riversidefm/src/client-monitor-js/src/detectors/InboundVideoFlowStateDetector.ts:1)
- [Pixelation detector](/Users/riversidefm/src/client-monitor-js/src/detectors/PixelatedVideoDetector.ts:1)
- [AV playout detector](/Users/riversidefm/src/client-monitor-js/src/detectors/AVDesyncPlayoutDetector.ts:1)
- [Scoring implementation](/Users/riversidefm/src/client-monitor-js/src/scores/DefaultScoreCalculator.ts:1)
- [Core summary issue subscription](/Users/riversidefm/src/observertc-observer-js/src/summaries/CallSummaryCollector.ts:166)
- [Publisher corroboration and configured type lists](/Users/riversidefm/src/observertc-observer-js/src/detectors/PublisherFaultCorroborationDetector.ts:1)
- [Delivery mismatch](/Users/riversidefm/src/observertc-observer-js/src/detectors/TrackDeliveryMismatchDetector.ts:1)
- [Population analysis](/Users/riversidefm/src/observertc-observer-js/src/detectors/ClientPopulationIssueDetector.ts:1)
- [W3C published WebRTC statistics definitions](https://www.w3.org/TR/webrtc-stats/)
