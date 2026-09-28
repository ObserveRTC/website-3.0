# ObserveRTC implementation map

Source snapshot: **28 September 2026**. This is an implementation reference for subsequent design and coding work, not a claim that the website, default branches and npm tags all expose the same release.

## How to use this reference

- This document explains ownership, lifecycle, formulas, wire boundaries, compatibility findings and where changes belong.
- [Monitor fields and formulas](monitor-fields-and-formulas.md) inventories the public properties/getters of every stable monitor, all direct `this.field` assignments, exact `createSample()` projections, and field calculations. Each entry links to a pinned source line. Assignments must be interpreted with their enclosing guards; they are not standalone mathematical definitions.
- [Detector reference](detector-implementation-reference.md) contains every released detector's exact configuration, state, inputs, comparisons, emissions and recovery implementation, plus server detectors. The concise condition index below makes these navigable.
- [Schema inventory](schema-field-inventory.md) enumerates authoritative nested Avro records and every field, type and default.
- [Searchable source atlas](source-atlas.html) includes the inspected repository snapshots, documentation, examples, generators and tests. Search a symbol or field, expand a file, and follow its pinned GitHub link. Source comments are preserved and can be wrong; the mismatch list distinguishes confirmed disagreements.
- [Machine-readable source index](source-index.json) contains classes, members, type declarations, assignments and exact source locations. [Verification results](verification-results.json) records the focused execution checks.

These references describe pinned source snapshots. Recheck commits before applying the map to newer versions. The appendices are generated inventories, not a claim of line-by-line manual verification or a full test-suite audit.

## Versions and local execution

| Component | Examined revision | Package/source version | Meaning |
|---|---|---|---|
| Client Monitor stable | `0f08bd5d110a4e9d53cf0486962e638c5b393c49` | 4.9.1 | `master`, npm `latest` |
| Observer | `b4a1ccb85468c94084a89ed2c007708c14ead551` | 1.0.0 | `master`, npm `latest` version 1.0.0 |
| Schemas | `eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17` | schema 3.7.0; generator package 3.0.0 | `sources/version.txt` is the schema version |
| Demo/site | `45c754f784e915c8b0c8f467e6edd3a178f8df64` | app 0.1.0 | Lockfile installs client 4.9.0 and observer 1.0.0-beta.23 |

Evidence: [client-monitor-js/package.json](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/package.json), [observer-js/package.json](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/package.json), [schemas/sources/version.txt](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/version.txt), [schemas/package.json](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/package.json), [webrtc-observer.org/package-lock.json](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/package-lock.json). npm metadata was fetched directly from the registry and saved under `work/`; tags describe the registry at inspection time. The prerelease tarball itself was not audited as a third implementation snapshot.

## End-to-end data ownership

```text
RTCPeerConnection or mediasoup-client Device/Transport
  → Sources / bindings → StatsCollector.getStats()
  → RTCStatsReport conversion → per-PC StatsAdapters
  → PeerConnectionMonitor dispatch by stats.type
  → raw-stat monitors, cross-reference graph, interval metrics
  → PC/ICE detectors; track windows and track detectors; client detectors
  → DefaultScoreCalculator
  → ClientMonitor.createSample() / each child's explicit createSample()
  → application transport (not built into ClientMonitor)
  → optional codec decode to a full ClientSample
  → Observer.accept(sample, context)
  → ObservedCall → ObservedClient → ObservedPeerConnection → entities
  → resolvers + aggregates + explicitly registered server detectors/validators
  → typed Observer bus; optional sinks; optional call summaries
```

The schemas describe the exchange contract; they are not another runtime processing stage. A raw JSON `ClientSample` can go directly to `Observer.accept()`. An encoded JSON delta or protobuf payload must be decoded first. The libraries do not prescribe HTTP, WebSocket, SCTP or storage. The demo uses an unordered, zero-retransmit mediasoup data channel, consumes it through a server DirectTransport, and persists JSONL via a sink. See [client-monitor-js/src/ClientMonitor.ts · collect](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L610), [client-monitor-js/src/monitors/PeerConnectionMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L614), [observer-js/src/Observer.ts · accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts#L710), [webrtc-observer.org/client/app.js](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/client/app.js), [webrtc-observer.org/src/call.ts](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/src/call.ts), [webrtc-observer.org/src/observer.ts](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/src/observer.ts).

**A sample is a projection, not a dump of every live monitor property.** Most calculated rates, detector severities, window state and declared context are not directly serialized. Raw counters, reference IDs, selected scores, attachments, buffered events/issues/meta/extensions are serialized. This is why an observer cannot reconstruct every client verdict merely by repeating calculations on slower samples.

## Client Monitor public API and graph

`src/index.ts` is the package export boundary. `ClientMonitor` is the root EventEmitter3-based API. Its core operations are:

| Need | Public surface |
|---|---|
| Attach instrumentation | `addSource(source, type?)`, `removeSource(source, type?)`; types: RTCPeerConnection, mediasoup device, mediasoup transport |
| Control updates | `collect()`, `setCollectingPeriod(ms)`, `setSamplingPeriod(ms)`, `createSample()`, `close()` |
| Identity / app-owned state | `clientId`, `callId`, `appData`, `attachments` |
| Traverse | `peerConnections`, `tracks`, `inboundRtps`, `outboundRtps`, remote RTP arrays, codecs, ICE entities, media sources/playouts, certificates, data channels; `getPeerConnectionMonitor`, `getTrackMonitor`, direction-specific getters |
| Declare intent | `setInboundTrackContext(trackId, context)`, `setOutboundTrackContext(trackId, context)`; pending context is applied when the track appears |
| Extend | `extensionStatsProviders`, `addExtensionStats`, `getExtensionStatsPayload`, `getExtensionStatsMonitor`; replaceable `scoreCalculator`; per-PC `statsAdapters`; scoped detector registries |
| Record | `addEvent`, `addIssue`, `raiseIssue`, `resolveIssue`, `addMetaData`, join/left event helpers |
| Subscribe | `on`, `once`, `off`, typed `ClientMonitorEvents`; convenience callback setters |

Sources: [client-monitor-js/src/index.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/index.ts), [client-monitor-js/src/ClientMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts), [client-monitor-js/docs/MONITOR_API.md](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/docs/MONITOR_API.md). Export nuances matter: `DefaultScoreCalculator` is exported as a **type** from the package root, despite being a runtime class internally; not every detector class is root-exported merely because its config type is.

The graph has ownership and cross-links:

- Client → peer connections, plus root extension monitors and client detector registry.
- PC → maps of codecs, inbound/outbound RTP, remote RTP, sources/playouts, data channels, ICE candidates/pairs/transports, certificates, peer-connection stats, inbound/outbound tracks.
- RTP → codec (`codecId`), ICE transport (`transportId`), counterpart remote report, track; outbound RTP → media source; inbound RTP → media playout.
- Track → actual MediaStreamTrack plus associated stream(s); outbound tracks can own several simulcast encodings, while an inbound track holds its inbound RTP monitor.
- ICE transport → selected pair; pair → local/remote candidates; `SelectedIcePath` tracks path identity, evidence and transitions. A PC may contain several transports; never assume one transport equals one PC.
- Track/PC issue registries forward toward the root registry. Ownership is not the same as the detector taxonomy.

References: [client-monitor-js/src/monitors/PeerConnectionMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts), [client-monitor-js/src/monitors/InboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts), [client-monitor-js/src/monitors/OutboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts), [client-monitor-js/src/monitors/InboundTrackMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts), [client-monitor-js/src/monitors/OutboundTrackMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts), [client-monitor-js/src/monitors/SelectedIcePath.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts), [client-monitor-js/src/utils/IssueRegistry.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/IssueRegistry.ts).

RTP monitor maps use SSRC in several lookup paths; stats-object IDs are not interchangeable with SSRC or MediaStreamTrack IDs. Preserve each identifier's role when adding fields or joining server entities. `visited` getters can consume/reset bookkeeping state; never read them from an inspector UI.

## Collection, adaptation and lifetime

1. `RtcPeerConnectionStatsCollector.getStats()` calls the real browser API; `convertRTCStatsReport()` keeps reports with id, timestamp and type. Mediasoup has its own collector and bindings. Bind a device before transports are created, or attach existing transports explicitly.
2. PC adapters run before dispatch. Chromium folds legacy fields and infers missing references. Safari additionally normalizes old data-channel IDs and pair-state spellings. Firefox can reconstruct a missing transport from its selected candidate pair, maintaining totals across pair changes. Inferred/reconstructed values must be labeled separately from browser-native measurements.
3. PC accept calculates `deltaTime` from successive maximum stats timestamps, resets PC aggregates, dispatches reports with a retry pass for unresolved ordering, updates references/path state, then runs PC and ICE-transport detectors.
4. Root collection aggregates PCs, feeds its window, updates tracks and their detectors, runs root detectors, updates scores, expires extension monitors, emits `stats-collected`, and possibly emits a sample.
5. Collection defaults to 5000 ms. Sampling defaults to 5000 ms and is collection-count-driven: `max(1, floor(samplingPeriod/collectingPeriod))`. A non-integral ratio warns and floors. Zero disables the relevant automatic mechanism. `createSample()` remains callable manually. A sample contains current stat snapshots and buffered discrete records; it is not a time average of all intervening monitor values.
6. `close()` tears down sources/timers, resolves lifecycle state, optionally records departure and emits a final sample before closing. Opt-in pre-subscriber buffering preserves samples until the first subscriber; it is off by default.
7. Stable 4.9.1 retains live track-associated RTP/source monitors over an omitted report and cleans up ended/pending tracks; the site's 4.9.0 dependency predates those fixes.

Sources: [client-monitor-js/src/collectors/RtcPeerConnectionStatsCollector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/collectors/RtcPeerConnectionStatsCollector.ts), [client-monitor-js/src/collectors/MediasoupTransportStatsCollector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/collectors/MediasoupTransportStatsCollector.ts), [client-monitor-js/src/adapters/ChromeStatsAdapter.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/adapters/ChromeStatsAdapter.ts), [client-monitor-js/src/adapters/FirefoxStatsAdapter.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/adapters/FirefoxStatsAdapter.ts), [client-monitor-js/src/adapters/SafariStatsAdapter.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/adapters/SafariStatsAdapter.ts), [client-monitor-js/src/monitors/PeerConnectionMonitor.ts · _acceptAdaptedStats](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L618), [client-monitor-js/src/ClientMonitor.ts · _setSamplingTick](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1219), [client-monitor-js/CHANGELOG.md](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/CHANGELOG.md).

## Field provenance and calculation rules

Use at least six origins in a future catalog: **browser stat**, **adapted/inferred stat**, **derived measurement**, **declared context**, **detector/score result**, **identity/lifecycle metadata**. A seventh useful presentation group is **application extension**.

The authoritative raw-stat families and exact field sets are in the schema inventory. Their monitor ownership is:

| Monitor | Browser report / content | Wire location under a PeerConnectionSample |
|---|---|---|
| InboundRtpMonitor | inbound-rtp: received/lost packets, jitter, received bytes, frame decode/render/freeze counters, jitter buffer, concealment, FEC/RTX, corruption | `inboundRtps[]` |
| OutboundRtpMonitor | outbound-rtp: sent packets/bytes, encoded frames, target bitrate, encode cost, QP, limitation durations, retransmission and feedback | `outboundRtps[]` |
| RemoteInboundRtpMonitor | remote-inbound-rtp: receiver-reported loss/jitter/RTT for local outbound stream | `remoteInboundRtps[]` |
| RemoteOutboundRtpMonitor | remote-outbound-rtp: sender reports for a local inbound stream | `remoteOutboundRtps[]` |
| CodecMonitor | codec identifiers, MIME type, clock rate, channels, FMTP, transport link | `codecs[]` |
| MediaSourceMonitor | media-source capture geometry/fps/frames and audio energy/duration | `mediaSources[]` |
| MediaPlayoutMonitor | media-playout synthesized audio duration/events, playout delay, sample totals | `mediaPlayouts[]` |
| IceTransportMonitor | transport: packets/bytes, ICE/DTLS state/roles, pair/certificate references, negotiated crypto | `iceTransports[]` |
| IceCandidateMonitor | local-candidate/remote-candidate addresses, ports, type, protocol, relay metadata | `iceCandidates[]` |
| IceCandidatePairMonitor | candidate-pair states, nomination, connectivity checks, RTT, throughput/BWE, endpoint refs | `iceCandidatePairs[]` |
| CertificateMonitor | certificate fingerprint/algorithm/base64 and issuer reference | `certificates[]` |
| DataChannelMonitor | data-channel state, label, protocol, identifier, messages/bytes | `dataChannels[]` |
| PeerConnectionTransportMonitor | peer-connection report: dataChannelsOpened/Closed | `peerConnectionTransports[]` |
| InboundTrackMonitor / OutboundTrackMonitor | MediaStreamTrack binding, context, aggregate/derived values; no matching browser track report assumed | `inboundTracks[]` / `outboundTracks[]`, limited projection |
| PeerConnectionMonitor | graph owner and aggregate, not the browser's peer-connection report | PC envelope |
| ClientMonitor | cross-PC aggregates, events, issues, extensions and score | ClientSample root |
| ExtensionStatsMonitor | application-defined payload, identity and freshness | `extensionStats[]` at root |
| SelectedIcePath | history/view over selected ICE tuple and its evidence | no dedicated sample record |

Source: [client-monitor-js/src/monitors/PeerConnectionMonitor.ts · createSample](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L924), [schemas/sources/samples/PeerConnectionSample.chunk.avsc](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc). The full field inventory is intentionally not reduced to the above examples.

### Core formulas

Let `Δx = positiveDelta(current, previous)`, `dtMs = current.timestamp − previous.timestamp`, `dt = dtMs/1000`. `positiveDelta` returns **undefined**, not zero, on missing inputs or a backwards counter. Each consumer may handle that differently; some explicitly coalesce to zero. Read the formula appendix for every assignment and its guards.

| Value | Implemented calculation / scope |
|---|---|
| RTP bitrate | `max(0, Δbytes × 8 / dt)` |
| RTP packet rate | `Δpackets / dt` |
| Outbound payloadBitrate | `max(0, (ΔbytesSent − ΔheaderBytesSent − (ΔretransmittedBytesSent ?? 0)) × 8 / dt)`; this is the implementation even if the field name invites a different byte accounting assumption |
| Inbound deltaFractionLost | `Δlost/(Δlost+Δreceived)` only when both deltas are present and both are positive; otherwise zero in that guarded block. This means all-loss/zero-received is not represented as 1 by this expression |
| Remote inbound deltaFractionLost | `Δlost/(Δlost+Δreceived)` when denominator >0, else 0; no-new-RTCP-report resets interval readings |
| BitPerPixel | `bitrate/(width × height × framesPerSecond)` with truthy geometry/fps/bitrate gates |
| Inbound avgFramesPerSec | mean of last at most 10 truthy browser FPS readings |
| fpsVolatility | mean absolute deviation of those FPS readings divided by their mean; deprecated |
| ewmaFps | existing EWMA ×0.9 + new FPS ×0.1; first/truthy-state handling matters |
| interFrameDelayVariation | `sqrt(max(0, ΔsquaredGap/N − (Δgap/N)²)) / (Δgap/N)`, N=`ΔframesDecoded`, N>1 |
| inventedSpeechRatio | `max(0, ΔconcealedSamples − (ΔsilentConcealedSamples ?? 0)) / ΔtotalSamplesReceived` |
| timeStretchRate | `((ΔinsertedSamplesForDeceleration ?? 0)+(ΔremovedSamplesForAcceleration ?? 0))/ΔtotalSamplesReceived`; a fraction, not per-second rate |
| concealmentEventRate | `ΔconcealmentEvents/dt` |
| discardRate | `ΔpacketsDiscarded/(ΔpacketsDiscarded+(ΔpacketsReceived ?? 0))`; zero if consumed count is zero |
| avgJitterBufferDelayInMs | `1000 × ΔjitterBufferDelay / ΔjitterBufferEmittedCount` |
| jitterBufferTargetDelayInMs | analogous target-delay delta / emitted count ×1000 |
| decodeTimePerFrameInMs | `1000 × ΔtotalDecodeTime / ΔframesDecoded` |
| avgEncodeTimePerFrameInMs | `1000 × ΔtotalEncodeTime / ΔframesEncoded` |
| avgQpPerFrame | ΔqpSum divided by decoded/encoded frames, depending on direction |
| normalizedQp | inbound average QP divided by codec scale from `qpScaleOf`, clamped 0..1; unknown codec => undefined |
| droppedFrameRatio / renderRatio | ΔframesDropped/ΔframesReceived; ΔframesRendered/ΔframesDecoded |
| frozenTimeRatio / pausedTimeRatio | ΔtotalFreezesDuration/dt; ΔtotalPausesDuration/dt |
| keyFrameRate, PLI/FIR/NACK rates | corresponding counter delta / dt |
| retransmissionRatio | retransmitted byte delta / total byte delta, capped at 1; zero/undefined behavior differs by direction |
| avgPacketSendDelayInMs | `1000 × ΔtotalPacketSendDelay/ΔpacketsSent` |
| qualityLimitationDurationShares | nonnegative deltas of none/cpu/bandwidth/other divided by sum of those deltas; undefined for no progress |
| source producedFps | nonnegative Δsource.frames/dt |
| source rmsAudioLevel | `sqrt(ΔtotalAudioEnergy/ΔtotalSamplesDuration)` when duration >0 |
| playoutDelayPerSampleInMs | `1000 × ΔtotalPlayoutDelay/ΔtotalSamplesCount` |
| synthesizedSamplesRatio | ΔsynthesizedSamplesDuration/ΔtotalSamplesDuration, with explicit fallback behavior in MediaPlayoutMonitor |
| ICE mean RTT | ΔtotalRoundTripTime/ΔresponsesReceived |
| RTCP mean RTT | ΔtotalRoundTripTime/ΔroundTripTimeMeasurements |

Sources: [client-monitor-js/src/utils/common.ts · positiveDelta](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/common.ts#L54), [client-monitor-js/src/monitors/InboundRtpMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L322), [client-monitor-js/src/monitors/OutboundRtpMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L174), [client-monitor-js/src/monitors/RemoteInboundRtpMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L97), [client-monitor-js/src/monitors/MediaSourceMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L82), [client-monitor-js/src/monitors/MediaPlayoutMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L72), [client-monitor-js/src/monitors/IceCandidatePairMonitor.ts · accept](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L95), [client-monitor-js/src/utils/quantizer.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/quantizer.ts).

PC sums distinguish audio/video/data-channel directions. Quality-loss averages include streams that actually carried relevant packets; missing measurement differs from zero loss. RTT paths are kept separate (`rtcpRttInSec`, `iceRttInSec`), with current RTT preferring RTCP and falling back to ICE. Root `avgRttInSec` averages PC values and returns -1 with no PCs. PC legacy loss sums and newer per-stream means are not interchangeable. See [client-monitor-js/src/monitors/PeerConnectionMonitor.ts · _updateTransportQualityAverages](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1253), [client-monitor-js/src/ClientMonitor.ts · collect](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L610).

`transportStability` is the normalized MOS-like value produced by `utils/transportStability.ts`: effective latency is RTT/2 + 2×jitter +10 ms; a piecewise latency impairment and 2.5×loss-percent reduce R; a cubic maps clamped R to MOS; normalized against this model's best/worst MOS. It requires all three measurements. It is not a direct measurement of user satisfaction or a selected-pair-switch counter. [client-monitor-js/src/utils/transportStability.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/transportStability.ts).

### Undefined, reset, suppression and nullification

There is no single universal nullification pass. The current code uses several distinct mechanisms:

- Missing raw inputs: InboundRtpMonitor explicitly replaces known fields, including undefined; several other monitors use Object.assign and can retain omitted properties. Derived assignments are conditional, so some previous derived values can remain. Do not promise universal freshness without checking the owner.
- Backwards counters: `positiveDelta` returns undefined; MediaPlayoutMonitor explicitly converts some such deltas to zero. Remote RTCP repeated/stale timestamps clear interval readings. Inbound repeated timestamps replace raw fields but return before recomputing derived values; outbound returns earlier.
- Shared windows: `SlicedWindow` uses null for unavailable totals, rejects repeated timestamps, resets across excessive gaps and requires full slices. N samples span N−1 intervals. Detection/recovery are different slices; inspect their configured offsets rather than assuming a trailing duration in milliseconds.
- Paused/ended/background/muted tracks: individual detectors stand down according to their own guards. There is no blanket rule that every detector handles every gate identically. Missing-input branches can preserve an open issue while publishing `inputsUnavailable`, whereas some detectors resolve it.
- Zero score: full-scale deductions clamp the affected component to zero. Connectivity issues are deliberately not charged again on the PC; dry-track issues can zero media components. There is no global “any network fault nullifies every score” rule.
- Aggregate absent dimensions: undefined/null dimensions are omitted from client RMSE; no measurable dimensions causes calculator early return, leaving the root's previous/default `score`, which starts at 5. This differs from documentation saying the root necessarily becomes undefined.
- Wire absence: undefined properties disappear under JSON serialization; Avro nullable fields and generated TS optional fields are separate representations. On-change ICE omissions must be retained by the receiver, but current observer code does not retain them (confirmed below).

Sources: [client-monitor-js/src/utils/SlicedWindow.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/SlicedWindow.ts), [client-monitor-js/src/monitors/InboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts), [client-monitor-js/src/monitors/OutboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts), [client-monitor-js/src/monitors/RemoteInboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts), [client-monitor-js/src/monitors/MediaPlayoutMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts), [client-monitor-js/src/scores/DefaultScoreCalculator.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/DefaultScoreCalculator.ts).

## Context, extensions, events and issues

Inbound context includes `contentType`, local `paused`, `remoteOutboundTrackPaused`, `linkedVideoTrackId`, `motionType`, `presentedResolution`, and `videoTag`. Outbound context includes `contentType` and `paused`; capture settings provide additional evidence. Context merges; passing a key with undefined clears it. Declared screen-share identity affects detectors; paired video identity is required for audio/video playout difference; rendered element size enables display magnification. None of these facts should be inferred merely from “video” or guessed from a different participant. [client-monitor-js/src/monitors/InboundTrackMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts), [client-monitor-js/src/monitors/OutboundTrackMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts), [client-monitor-js/src/ClientMonitor.ts · setInboundTrackContext](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1154).

`appData` is local arbitrary working state. `attachments` is the explicit serializable envelope. Track `createSample()` sends id, kind, timestamp, attachments, score and reasons; it does not automatically send the context object, HTML element, flags or all derived metrics. Put required backend application context into an appropriate serializable contract explicitly.

`addExtensionStats({type,payload,id?})` updates an id-keyed live ExtensionStatsMonitor independently of sampling. When automatic sampling is enabled or `bufferingEventsForSamples` is true, it also buffers `{type,payload}` and emits `extension-stats`. The optional monitor `id` is **not serialized** in that entry. Providers run during collect. The visited-based retention/expiry mechanism is local freshness, not persistent server storage. `getExtensionStatsPayload<T>` asserts T; it does not runtime-validate it. Observer emits `client-extension-stats`; it does not recreate the same client ExtensionStatsMonitor registry. [client-monitor-js/src/ClientMonitor.ts · addExtensionStats](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L983), [client-monitor-js/src/monitors/ExtensionStatsMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/ExtensionStatsMonitor.ts), [observer-js/src/ObservedClient.ts · addExtensionStats](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts#L570).

Events and issues are separate channels:

- Monitor events are local typed callbacks (`ClientMonitorEvents`) and may carry live monitor objects.
- `addEvent()` adds a serializable ClientEvent and emits `client-event` only when automatic sampling is enabled or `bufferingEventsForSamples` is true. The flag defaults to false, but automatic sampling defaults to enabled, so ordinary default operation still buffers events. With both disabled, `addEvent()` returns before buffering or emitting. Metadata and issue sample buffering use the same gate; local issue emission is independent. A detector's `createEvent` and a monitor event are not automatically the same switch.
- `addIssue()` is one-shot. Keyed `raiseIssue`/registry `raise` opens state, update changes live payload, resolve closes it. Local events are `issue`, `issue-updated`, `issue-resolved`.
- Stateful raises buffer `{type,payload,timestamp,key}` when allowed. Resolution buffers type `${type}-resolved`, the same key, resolution timestamp, and payload including raisedAt/comment. `sendResolvedIssuesToServer` defaults true; false omits keyed lifecycle shipping.
- `includeIssueInSample=false` preserves local detection but suppresses its issue records on the wire. Issue updates emit locally but `_updateIssue()` does not buffer a fresh issue entry each tick.
- Registry propagation preserves subject-specific keys; multiple tracks can hold the same issue type independently.

Sources: [client-monitor-js/src/ClientMonitorEvents.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitorEvents.ts), [client-monitor-js/src/ClientMonitorIssues.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitorIssues.ts), [client-monitor-js/src/utils/IssueRegistry.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/IssueRegistry.ts), [client-monitor-js/src/ClientMonitor.ts · _raiseIssue](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1260), [client-monitor-js/src/ClientMonitor.ts · _updateIssue](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1278), [client-monitor-js/src/ClientMonitor.ts · _resolveIssue](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1286).

## Detector configuration and complete condition index

Version 4.9.1 has **46 detector classes**. Class files, not historical table counts, define availability. Categories describe the condition being judged, not necessarily the registry/owner. `IceTraversal`, `IceRestart`, and `IceRestartRecommendation` are Telemetry even though their subject is connectivity. `IcePathEstablishment` is event-only Connectivity. `AudioPlayoutSynthesis` currently raises an issue despite stale event-only descriptions in stable taxonomy prose.

Each config key is lowerCamelCase class name; undefined selects the default object, null prevents registration, an object replaces that detector's default object. **Nested detector defaults are not deep-merged by ClientMonitor's `detectorDefault` helper.** Passing `{}` to a detector requiring thresholds can leave required values undefined; do not advertise `{}` as generic “use defaults.” Top-level type permits partial root config, not arbitrary partial nested configs. `BlockedInboundMediaDetector` is disabled by default because its evidence premise is not generally usable with browser RTCP mux. Deprecated `CongestionDetector` remains enabled by default.

Default shared windows: detection 3/recovery 3 values for client, PC, inbound and outbound tracks; inbound flow detection 4/flow recovery 3. Max allowed gap defaults to four times a positive collecting period (fallback period 5000 ms). Default flags: integrate media devices/watch visibility/join event/left event true; buffering events and pre-subscriber samples false; resolved issue shipping, score reason shipping and on-change ICE metadata true. See [client-monitor-js/src/ClientMonitor.ts · constructor](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L146), [client-monitor-js/src/ClientMonitorConfig.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitorConfig.ts), [client-monitor-js/src/detectors/Detectors.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/Detectors.ts).

The following summaries identify the main trigger and recovery. **Exact comparison operators, missing-input paths, state variables, payload types and event names are preserved per class in the detector reference.** A time threshold alone is insufficient to reproduce a detector.

### Connectivity

| Class | Default / trigger | Recovery / state |
|---|---|---|
| [IceReachabilityDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceReachabilityDetector.ts#L49) | gathering complete, no local candidates, never connected; failing state or 6000 ms wait | candidates appear, connected, or closed; remembers prior success |
| [IcePathEstablishmentDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IcePathEstablishmentDetector.ts#L43) | connection stays connecting ≥5000 ms; emits slow-stage event | resets outside connecting; event once per episode |
| [IceEstablishmentFailedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceEstablishmentFailedDetector.ts#L57) | candidates exist, no historical connected/succeeded/nominated path, sustained 15000 ms | established path or closed; distinguishes no-network from failed establishment |
| [DtlsHandshakeFailedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DtlsHandshakeFailedDetector.ts#L38) | dtlsState failed, immediate | connected or transport removed; per-transport raise map |
| [DtlsHandshakeStalledDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DtlsHandshakeStalledDetector.ts#L61) | DTLS new/connecting while real ICE evidence is healthy for 6000 ms | connected/failed/removal; generation and missing-evidence paths reset accumulation |
| [IceDisconnectedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceDisconnectedDetector.ts#L57) | per-transport disconnected for 5000 ms | connected/completed, ICE restart or removal |
| [IceConnectionFailedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceConnectionFailedDetector.ts#L51) | per-transport failed immediately | connected/completed, restart or removal |
| [IceTransportStalledDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceTransportStalledDetector.ts#L65) | succeeded connected path previously received data; sends but no inbound, expected inbound media, 5000 ms | inbound resumes, connectivity lost, restart/removal; send-only/paused situations gated |
| [UnstableIcePathDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/UnstableIcePathDetector.ts#L60) | at least 3 switches in 30000 ms observation window | completed quieter window or transport removal |

Each row links through its named class in [client-monitor-js/src/detectors/Detector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/Detector.ts) and the detector appendix; connectivity state machine context is in [client-monitor-js/src/monitors/SelectedIcePath.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts).

### Transport Quality

| Class | Default / trigger | Recovery / state |
|---|---|---|
| [CongestionDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CongestionDetector.ts#L77) | deprecated sensitivity medium; legacy RTT/loss/limitation heuristic | legacy congested flag and max-baseline bookkeeping; not interchangeable with directional detectors |
| [UplinkCongestionDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/UplinkCongestionDetector.ts#L95) | browser bandwidth-limited verdict AND severity≥0.65; severity = sqrt(BWE undershoot × pacer bloat); bloat saturates at 4×median | closes when browser stops reporting bandwidth limitation or send path stands down; decaying max and median baselines |
| [DownlinkCongestionDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DownlinkCongestionDetector.ts#L105) | inbound video; severity≥0.65 = sqrt(receive-bitrate undershoot × video jitter-buffer bloat), 4×median saturation | below half minSeverity (0.325 default), or no inbound video; separate baselines |
| [TransportDelayDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/TransportDelayDetector.ts#L70) | detection-window mean current RTT≥300 ms | recovery-window RTT<200 ms or no measurement; RTCP/ICE source retained |
| [TransportLossDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/TransportLossDetector.ts#L47) | max available inbound/outbound mean loss≥0.05 for 6000 ms | loss<0.01; hysteresis between thresholds |
| [BlockedStunRequestsDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/BlockedStunRequestsDetector.ts#L52) | succeeded pair sends requests/consent checks but no responses for 10000 ms | response arrives/path unverified/no request evidence; separate 10000 ms request timeout; issue is blocked-stun-requests, event remains blocked-transport |
| [BlockedOutboundMediaDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/BlockedOutboundMediaDetector.ts#L50) | actual outgoing RTP, STUN answers, fresh remote receiver reports stop for 10000 ms | reports resume, no sending or no usable path; absent RTCP is evidence with the other gates, not proof of a particular firewall |
| [BlockedInboundMediaDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/BlockedInboundMediaDetector.ts#L58) | **default null**; sender-report evidence advances while inbound media does not, for configured threshold | reception resumes/no sending or no usable path; enable only where evidence is meaningful |

Directional formulas and baseline update order: [client-monitor-js/src/detectors/UplinkCongestionDetector.ts · update](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/UplinkCongestionDetector.ts#L129), [client-monitor-js/src/detectors/DownlinkCongestionDetector.ts · update](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DownlinkCongestionDetector.ts#L138). The baseline is read before feeding the current observation; medians stop learning while an issue is open. These are not generic packet-loss thresholds.

### Pipeline Disruption

| Class | Default / trigger | Recovery / important gates |
|---|---|---|
| [CaptureSourceLostDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CaptureSourceLostDetector.ts#L40) | sourceEnded capture flag; one-shot capture-source-lost | one-shot, not a continuously resolved threshold episode |
| [SilentAudioSourceDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/SilentAudioSourceDetector.ts#L106) | live enabled unmuted microphone/device; RMS≤0.0001 for 60000 ms captured audio | RMS>0.0003 when raised; pause, screen share, lost input, ended source stand down |
| [VideoCaptureBottleneckDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/VideoCaptureBottleneckDetector.ts#L97) | `1 − producedFps/expectedCaptureFps >0.2` over shared detection slice | recovery slice within threshold; settings changes, screen share, inactive tab/muted/paused source stand down |
| [EncoderBottleneckDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/EncoderBottleneckDetector.ts#L113) | highest layer `1 − encodedFps/producedFps >0.3` | recovery slice within threshold; source/layer/config-change gates |
| [RtpSenderStalledDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/RtpSenderStalledDetector.ts#L51) | frames encode but no RTP packets leave for 4000 ms | packets resume, stream disappears or guarded state; per-SSRC state |
| [DryOutboundTrackDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DryOutboundTrackDetector.ts#L78) | active layer byte deltas sum to zero for 5000 ms | data resumes; pause/mute/end/encoder limitation/no active layer stand down |
| [TransportDemuxStalledDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/TransportDemuxStalledDetector.ts#L52) | transport receives ≥20000 bps while existing inbound RTP accounts for zero bytes, 4000 ms | RTP progress, missing transport or failed guards; per-transport state |
| [DryInboundTrackDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DryInboundTrackDetector.ts#L39) | incoming byte delta zero for 5000 ms | bytes resume, local/remote declared pause, ended track |
| [FrameAssemblyStalledDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/FrameAssemblyStalledDetector.ts#L44) | packets arrive, framesReceived flat; ≥20 packets and ≥3000 ms | complete frame arrives or stand-down gates |
| [DecoderBottleneckDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DecoderBottleneckDetector.ts#L126) | received frame supply≥5 fps, decoding shortfall>0.1 over shared window | recovery window catches up; dropped-frame and foreground/context gates distinguish causes |
| [DecoderPerformanceDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DecoderPerformanceDetector.ts#L73) | decode time >0.8×frame budget, ≥10 received frames, interval loss≤0.02, 2 ticks | decode keeps up, insufficient frames, loss dominates, ended/background |
| [StuckDecoderDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/StuckDecoderDetector.ts#L66) | no decoded frames with bitrate≥10000, ≥2 PLIs, elapsed≥max(4000 ms,15×RTT) | decoded frames return or source/context/foreground gates; records assembly evidence |
| [PlayoutDiscrepancyDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/PlayoutDiscrepancyDetector.ts#L63) | received-vs-rendered frame skew≥0.25 with ≥10 frames in detection window | skew<0.1 or stand-down; despite prose mentioning decode-to-render, inspect actual operands |
| [VideoRecoveryFailedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/VideoRecoveryFailedDetector.ts#L44) | stalled picture/keyframe recovery, ≥2 PLIs, ≥5000 ms | video recovery or guards; repair-loop diagnosis separate from perceptual freeze |
| [CpuPerformanceDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CpuPerformanceDetector.ts#L104) | measurable software encode/decode utilization at least 0.5 across client detection window | recovery below 0.4; background/no CPU-backed work/no measurement stand down |

Sources: named files under [client-monitor-js/src/detectors/Detectors.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/Detectors.ts), plus the full algorithms in the detector reference. Shared-window readiness and total-vs-delta choices are material to all capture/encoder/decoder comparisons.

### Perceived Quality

| Class | Default / trigger | Recovery / evidence |
|---|---|---|
| [PixelatedVideoDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/PixelatedVideoDetector.ts#L75) | normalized QP≥0.62 for 8000 ms | QP<0.52; no QP/unknown codec/pause/end/screenshare stand down; **not bitPerPixel** |
| [InboundVideoFlowStateDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/InboundVideoFlowStateDetector.ts#L92) | shared flow slice: continuous/longest freeze≥2000 ms => frozen; ≥2 freezes => choppy | frozen clears on moving picture; choppy needs freeze-free recovery slice; mutually exclusive payload state |
| [InventedSpeechDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/InventedSpeechDetector.ts#L55) | bucket `clamp(bucket+(inventedRatio−0.05)×dtMs,0,400)`; full opens invented-speech | empty closes; pause/end discard; missing input marks unavailable |
| [AudioPlayoutSynthesisDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/AudioPlayoutSynthesisDetector.ts#L115) | synthesized duration / played duration>0.05 over track window | recovery ratio≤threshold; needs media-playout measurements; currently raises synthesized-audio |
| [JitterBufferStressDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/JitterBufferStressDetector.ts#L71) | target delay>200 ms AND stretch share>0.02 for 2 ticks | conjunction clears, track stand-downs; severity scales against 1000 ms and 0.15 |
| [AVDesyncPlayoutDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/AVDesyncPlayoutDetector.ts#L60) | explicitly paired audio/video playout timestamps; ahead≥90 ms or behind≥185 ms for 3000 ms | ahead<45 or behind<125; direction-aware hysteresis; missing pairing is unavailable |

Sources: [client-monitor-js/src/detectors/PixelatedVideoDetector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/PixelatedVideoDetector.ts), [client-monitor-js/src/detectors/AudioPlayoutSynthesisDetector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/AudioPlayoutSynthesisDetector.ts), [client-monitor-js/src/detectors/InventedSpeechDetector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/InventedSpeechDetector.ts).

### Telemetry

| Class | Observation | State / defaults |
|---|---|---|
| [IceTraversalDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceTraversalDetector.ts#L26) | selected tuple set changes | remembers tuple set; no first-observation change event; no issue |
| [IceRestartDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceRestartDetector.ts#L53) | local ICE username fragment changes, restart outcome | per-transport generation/pending state; createEvent true |
| [IceRestartRecommendationDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceRestartRecommendationDetector.ts#L87) | failed, disconnected/stalled≥10000 ms, or never-established≥10000 ms | cooldown 15000 ms; pending restart gates; recommendation event, does not itself restart ICE |
| [CaptureTrackMutedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CaptureTrackMutedDetector.ts#L28) | previously known unmuted→muted transition | track muted state; createEvent true; distinct from application mute |
| [CodecChangeDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CodecChangeDetector.ts#L26) | MIME/FMTP change | previous codec signature; first value establishes baseline |
| [VideoResolutionChangeDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/VideoResolutionChangeDetector.ts#L34) | positive frame width/height changes | prior geometry; includes direction and outbound limitation context |
| [SimulcastLayerDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/SimulcastLayerDetector.ts#L45) | set of actively sending layer keys changes | multiple encoding requirement; paused/end reset |
| [StatsGapDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/StatsGapDetector.ts#L34) | actual collection period >2×expected AND >5000 ms | prior collection start time; no issue, createEvent true |

Source files are preserved in the detector reference and [client-monitor-js/docs/TELEMETRY_DETECTORS.md](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/docs/TELEMETRY_DETECTORS.md). Telemetry can have thresholds (StatsGap and restart recommendations); prose saying it has none is too broad.

## Scoring

`DefaultScoreCalculator.update()` computes PC stability, track scores, then client score. A component starts from 5 and subtracts applicable penalties, clamped at 0. Track weight and PC stability weight feed dimension means. Five dimensions are PC stability, inbound audio/video, outbound audio/video. Client score is:

```text
dimension = sum(componentScore × weight) / sum(weight)
client = roundTo2(clamp(5 − sqrt(mean((5 − dimension)²)), 0, 5))
```

Missing dimensions are excluded. `[5,5,0]` therefore gives 2.11, not arithmetic mean 3.33. The server's `DefaultCallScoreCalculator` is a **weighted arithmetic mean of client scores**, not the same RMSE rule. [client-monitor-js/src/scores/DefaultScoreCalculator.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/DefaultScoreCalculator.ts), [observer-js/src/scores/DefaultCallScoreCalculator.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/scores/DefaultCallScoreCalculator.ts).

Important costs include dry tracks/stuck decoder/frame-assembly stall at 5; PC sustained loss and delay at 2.5 each; directional congestion at 2.5×max(severity, configured minimum); PC continuous instability at `2×(1−transportStability)`; decoder bottleneck at 2×clamped degradation. Track-specific video/capture/encode/freeze/pixelation/audio costs and all continuous ramps are preserved in the source atlas and formula reference. Pixelation weight depends on displayed magnification: ≥1.5 =>1.5×, <0.75=>0.25×, otherwise1×. No presented size means ordinary weight, not suppression.

The calculator is **not issues-only**, despite its opening comment. It also charges continuous frame timing, frame drops, quantization, audio instability, target-bitrate deviation, screen-share downscale and transport stability. Continuous reason names are exposed only when their total exceeds 1 point, unless an issue is active; score reductions may exist with no published reasons. Root sample reasons are only root-owned reasons; the default RMSE adds no root reason, while the score event carries aggregated component reasons. `sampledScoreReasons()` copies the object and honors explicit false. Sources: [client-monitor-js/src/scores/DefaultScoreCalculator.ts · reasonsOf](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/DefaultScoreCalculator.ts#L298), [client-monitor-js/src/scores/utils.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/utils.ts), [client-monitor-js/src/ClientMonitor.ts · setScore](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L722).

## Schema contract and generation

Authoritative sources are `sources/samples/ClientSample.avsc` and `PeerConnectionSample.chunk.avsc`. The first defines the root and discrete records, the second the PC envelope, tracks and browser-stat families. Every field/type/default is in the schema appendix. Root includes timestamp, optional clientId/callId, attachments, score/reasons, PCs, events, issues, metadata and extensions. Optional at schema level does not imply accepted by Observer: Observer rejects missing clientId or callId.

`ClientIssue` is intentionally extensible by string type and payload, rather than a closed enum of detector issues; adding a new issue type usually does not require changing the Avro structure. New raw/stat fields do. `ClientMonitorIssues` is a local discriminated union for built-in issue handling, not the universal wire schema.

The generation path is `src/cli.ts` → `runPipeline()` → JSONC Avro loading/chunk expansion/validation → TypeScript, normalized Avro, Markdown, protobuf and npm targets. `src/config.ts` defines deliberate format overrides:

- Avro attachments are nullable string, but TypeScript exposes `Record<string,unknown>`.
- Payload is modeled with recursive AnyValue in Avro, exposed as Record in TS, and serialized as JSON string in protobuf.
- SFU extension payload is a specific string exception.
- Proto UUID-like identifier fields become bytes; timestamps become double; enum spelling overrides include candidate-pair in-progress variants.

Do not compare these representations with naive textual equivalence. Inspect [schemas/src/config.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/config.ts), [schemas/src/pipeline.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/pipeline.ts), [schemas/src/avro/source-loader.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/avro/source-loader.ts), [schemas/src/avro/chunk-registry.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/avro/chunk-registry.ts), [schemas/src/generators/typescript/generate.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/generators/typescript/generate.ts), [schemas/src/generators/protobuf/proto3-generator.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/src/generators/protobuf/proto3-generator.ts), [schemas/docs/GENERATOR.md](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/docs/GENERATOR.md).

Generated outputs appear under `outputs/typescript`, `outputs/avsc`, protobuf outputs and npm package source directories. observer-js's checked-in ClientSample.ts is byte-identical to the current generated TS; client-monitor's type field sets match but its file differs textually. Both advertise 3.7.0. Do not edit just one copied ClientSample file as if it were authoritative.

JSON/protobuf codec packages are stream-stateful. One encoder per client/receiver, ordered complete delivery, resets for reconnect/snapshot boundaries. Deltas are not complete ClientSamples. The website's current unordered unreliable channel cannot safely adopt delta encoding by simply replacing JSON.stringify with encode; establish delivery/recovery semantics first. [schemas/npm-samples-json-codec/src/ClientSampleEncoder.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/npm-samples-json-codec/src/ClientSampleEncoder.ts), [schemas/npm-samples-json-codec/src/ClientSampleDecoder.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/npm-samples-json-codec/src/ClientSampleDecoder.ts), [schemas/npm-samples-protobuf-codec/src/ClientSampleEncoder.ts](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/npm-samples-protobuf-codec/src/ClientSampleEncoder.ts), [webrtc-observer.org/client/app.js](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/client/app.js).

## Observer ingestion and reconstructed state

`Observer.accept(sample, context?)` is synchronous. The current implementation invokes acceptMiddlewares, validates nonempty call/client IDs, gets or creates a call/client and calls `ObservedClient.accept()`. It does not perform full Avro validation, automatic codec decoding or client-side detector execution. The middleware implementation has a reproduced drop/replacement bug described below.

`ObservedClient.accept` resets interval aggregates, normalizes score reason wire generations, merges pending injections, processes events/meta/issues/extensions, updates PCs, processes deferred events, sets attachments and sampled client score, emits update events, resets idle timeout and writes the final sample to a sink. Client-level bitrate uses **server wall-clock arrival interval**, so replaying historical samples rapidly is not equivalent to the browser stats cadence. Per-RTP entities retain their own stat processing rules. [observer-js/src/Observer.ts · accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts#L710), [observer-js/src/ObservedClient.ts · accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts#L217), [observer-js/src/common/utils.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/common/utils.ts).

PC accept handles the same stat families as its arrays, creates or updates `Observed*` entities, derives per-interval/cumulative counters, selects transports and cleans unvisited children. RTP maps commonly use SSRC, tracks use track ID, other objects use stat ID. Parent scopes are included on the central Observer bus; local emitters coordinate internals. State is live and removable; it is not a database. [observer-js/src/ObservedPeerConnection.ts · accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedPeerConnection.ts#L317), [observer-js/src/ObserverEvents.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObserverEvents.ts), [observer-js/src/ObservedInboundRtp.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedInboundRtp.ts), [observer-js/src/ObservedOutboundRtp.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedOutboundRtp.ts).

`ObservedClient.activeIssues` mirrors keyed client lifecycle records. A raise gets both client-clock `raisedAt` and server-clock `observedAt`; cross-client onset comparisons must use the latter. Same-key re-raise refreshes payload; keyless records are one-shot. A `-resolved` record retires the key and emits resolution. Client close resolves outstanding state. Registries propagate into call and observer scopes, enabling cross-client queries without walking every healthy client. [observer-js/src/issues/ObservedClientIssueRegistry.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/issues/ObservedClientIssueRegistry.ts), [observer-js/src/issues/ActiveIssuesRegistry.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/issues/ActiveIssuesRegistry.ts), [observer-js/src/ObservedClient.ts · addIssue](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts#L534).

Server defaults: automatic observer update on call updates, 60 s idle client timeout, 60 s empty-call timeout. Passing explicit undefined through config disables those timeout defaults because config is spread after defaults. Call summaries are absent unless configured. Detector registries start **empty**. Register observer-wide detectors with `addObserverDetector`, future-call detectors with `addCallDetector`, and an existing call's detector with `call.addDetector`. Removal semantics and duplicate-name instances differ from a unique-name client registry. [observer-js/src/Observer.ts · constructor](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts#L331), [observer-js/src/Observer.ts · addCallDetector](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts#L418), [observer-js/src/detectors/Detectors.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/Detectors.ts).

### Server detector and validator map

| Scope | Classes | Evidence / purpose |
|---|---|---|
| Call | CallConcurrentIssueDetector | active issue prevalence and onset bursts within one call |
| Call | IssueFanOutDetector | same publisher-associated failure appears across receivers |
| Call | PublisherFaultCorroborationDetector | publisher-side issues corroborated by receiver degradation/issues |
| Call | TrackDeliveryMismatchDetector | publisher/receiver delivery disagreement with resolved track links |
| Call | UnconsumedTrackDetector | outbound track has no known consumer after configured grace; requires a resolver |
| Observer | ObserverConcurrentIssueDetector | same issue spans independent calls / synchronized onsets |
| Observer | SfuCongestionDetector | correlated infrastructure/SFU degradation, consumes client issues |
| Observer | ClientPopulationIssueDetector | group client issues by browser/OS/location or supported axis |
| Observer | TurnServerHealthDetector | group current client findings around relays |
| Observer | TurnServerOutageDetector | detect relay outage patterns across clients |
| One-shot validation | SimulcastReceiverValidator | whether receivers select layers independently |
| One-shot validation | RemoteTrackResolverValidator | whether remote publisher/subscriber linkage can be established |
| One-shot validation | CodecConsistencyValidator | cross-end codec consistency / deployment behavior |

Exact configs/defaults, state and triggers for all server detector classes are in the detector reference. They live in detector constructors in this version; the obsolete AGENTS instructions about a nonexistent DetectorsConfig.ts are not the implementation. Validators run on observer updates until they decide or are cancelled, and publish typed reports; no observation is not proof of success. [observer-js/src/validators/Validators.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/validators/Validators.ts), [observer-js/src/validators/Validator.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/validators/Validator.ts), [observer-js/examples/detectors.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/examples/detectors.ts).

### Tracks, SFUs, sinks and extensions

`RemoteTrackResolver` connects publishers/subscribers across client boundaries. The mediasoup factory reads producerId/consumerId in track attachments. The P2P factory joins SSRC-derived identifiers and documents its single-encoding assumption. Generic SFUs need an explicit resolver factory based on their signaling IDs; schema IDs alone do not guarantee end-to-end association. [observer-js/src/resolvers/RemoteTrackResolver.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/resolvers/RemoteTrackResolver.ts), [observer-js/src/resolvers/RemoteTrackResolverFactories.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/resolvers/RemoteTrackResolverFactories.ts).

`ObservedMediasoupRouter` attaches to a real router and accumulates a separate `MediasoupRouterSample`; it observes server transports, producers/consumers and their lifecycle, and correlates a router's transport with client PCs. This is not the archived sfu-monitor-js API and not a ClientSample array. The application decides when to persist the growing router sample. The demo writes it beside call summaries and client streams, and injects routerId upon matching. [observer-js/src/ObservedMediasoupRouter.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedMediasoupRouter.ts), [observer-js/src/schema/MediasoupRouter.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/schema/MediasoupRouter.ts), [observer-js/examples/sfu-observer.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/examples/sfu-observer.ts), [webrtc-observer.org/src/observer.ts](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/src/observer.ts).

Sinks are per-client via `createClientSink`; built-ins are JSONL and in-memory. They persist the final injection-merged sample. During accept, `injectAttachment/Event/Issue/MetaData/ExtensionStat` affects the active sample immediately; between accepts it queues; close flushes pending data before sink teardown. A sink failure is logged, not a substitute for application persistence guarantees. [observer-js/src/sinks/ClientSampleSink.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/sinks/ClientSampleSink.ts), [observer-js/src/sinks/JsonlFileSink.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/sinks/JsonlFileSink.ts), [observer-js/src/sinks/InMemorySink.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/sinks/InMemorySink.ts), [observer-js/src/ObservedClient.ts · _flushPendingInjections](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts#L923).

Call summaries opt into sections (`clients`, `issues`, `turnServers`, `scores`) and optional event enrichers. Empty include defaults to no built-in sections, not “all.” Caps default to 500 issues/10000 client IDs; truncation is recorded. Collector bus subscriptions span the Observer rather than multiplying per call; final summary emits during call close. Client logger is supplied in ClientMonitor config; server uses its common logger API (`setObserverLogger` etc.). [observer-js/src/summaries/CallSummary.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/summaries/CallSummary.ts), [observer-js/src/summaries/CallSummaryCollector.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/summaries/CallSummaryCollector.ts), [observer-js/src/common/logger.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/common/logger.ts), [observer-js/docs/logging.md](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/docs/logging.md).

## Website audit and restructuring direction

The downloaded `webrtc-observer.org` repository is primarily an interactive diagnostics demo. Its design source is `design/Client Monitor.dc.html`; `tools/build-page.py` transforms it into committed `public/index.html`. Browser modules implement pipelines, catalog, scores, journal, sample viewer and hand-authored field/issue explanations. It is a plain JS/esbuild app, not a React site. Separately, `website-3.0` holds the project's documentation site and is relevant to informational content. Those are different products and should not silently be treated as one repository.

Catalog extraction reads **installed** `dist/monitors/*.d.ts`, `dist/ClientMonitor.d.ts`, and `dist/schema/ClientSample.d.ts`. It uses a hard-coded monitor/type map and regex parsing, includes only selected primitive types/getters, and classifies fields by schema membership. It also extracts monitor-event names. It does **not** derive formulas, units, detector configs, state machines, descriptions, or evidence relationships. Hand-authored explanations live in field-notes.js, issue-notes.js and pipeline modules. [webrtc-observer.org/tools/extract-monitors.py](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/tools/extract-monitors.py), [webrtc-observer.org/client/catalog.js](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/client/catalog.js), [webrtc-observer.org/client/field-notes.js](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/client/field-notes.js), [webrtc-observer.org/client/issue-notes.js](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/client/issue-notes.js), [webrtc-observer.org/client/pipeline.js](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/client/pipeline.js).

Confirmed issues:

| Finding | Why it matters / source of truth |
|---|---|
| Catalog generated from 4.9.0; stable is 4.9.1; next adds/renames audio detection | Show version/channel explicitly; never mix future docs into stable tooltips |
| Only 17 classes/555 primitive fields | Missing ExtensionStatsMonitor and SelectedIcePath; omits structured stats, contexts, arrays/maps and APIs |
| `clientId`, `closed`, `activeTab` labeled derived | These are identity/lifecycle/context, not calculated WebRTC measurements |
| Schema membership used as raw provenance | Firefox reconstructed transport and inferred IDs can share the same stat types; next raw Chromium extras are outside schema and would be falsely called derived |
| Pattern description says counter resets mean “no change” | positiveDelta yields undefined; zero would falsely suggest a stall |
| Pattern `*Rate` means per second | timeStretchRate/discardRate are fractions; naming cannot define units |
| Pattern `total*` means monotonic | available bandwidth totals are gauges, not counters; use explicit metadata |
| transportStability tooltip describes path changes and consent | actual calculation is RTT/jitter/loss MOS normalization |
| PC score tooltip says tracks contribute | getter is calculatedStabilityScore; track scores contribute separately to root dimensions |
| Root score tooltip says subtract weighted faults | actual aggregation is RMSE over dimension shortfalls |
| Uplink/downlink tooltips describe loss/jitter-based heuristics | current directional detectors use baseline undershoot and pacer/jitter-buffer bloat with distinct gating |
| Build does not regenerate catalog/page | an installed upgrade can leave a stale field/event catalog; generation belongs in a controlled build/check step |
| Automatic join on page load | Project documentation visitors are immediately put into demo behavior |

Visual inspection in the app's narrow browser pane reproduced clipped horizontal navigation and a 4+1 score-dimension grid with a large empty region. Source also uses fixed-width subgrids and many inline layout rules. This supports the reported ergonomic concern, but it is not a completed desktop/mobile breakpoint audit. The server's local loopback worked; no website content was rewritten.

Recommended structure preserving the visual language:

1. **Project overview**: one concise explanation, component/data-flow diagram, install entry points, links to client/server/schema references.
2. **Integrate**: browser, mediasoup, transport/backend, storage examples with version badges and copyable tested commands.
3. **Reference**: monitor graph, fields, detectors, events/issues, scoring and schema. Each field gets origin, unit, availability, formula, guards, wire projection and consumer links. Each detector gets inputs, defaults, raise/resolve, unsupported cases, event/issue shape and source.
4. **Live demo**: explicit Start, separate from reading documentation; stable page shell with consistent content alignment and a collapsible media panel.
5. **Migration/version notes**: released versions and 4.9.0→4.9.1 lifecycle fixes.

For the demo, replace the single long tab strip with a compact navigation group, use one shared content grid with `minmax(0,1fr)`, stack panels at explicit breakpoints, keep prose to a one-sentence explanation plus expandable detail, and avoid reflowing five dimensions into an accidental four-plus-one block. Preserve colors, typography, radii, chart style and spacing tokens; restructure page hierarchy and component layout. This is a proposal, not an implemented redesign.

## Confirmed documentation and implementation mismatches

1. **Delta reset semantics:** DERIVED_METRICS says zero; positiveDelta returns undefined. Source wins. Other consumers can explicitly coalesce; do not overgeneralize either direction.
2. **Outdated metric names:** DERIVED_METRICS examples use `InboundRtpMonitor.fractionLost`, `isFreezed`, and `OutboundRtpMonitor.encodeTimePerFrameInMs`; the current relevant names are deltaFractionLost/totalFractionLost, track flow state, and avgEncodeTimePerFrameInMs. See field inventory.
3. **Pixelation explanation:** ClientMonitorConfig prose still says bitPerPixel, while PixelatedVideoDetector uses normalizedQp. The site's exact tooltip must be version-checked separately from this stale config comment.
4. **Audio synthesis taxonomy:** stable taxonomy describes AudioPlayoutSynthesis as event-only/missing issue; actual constructor binds an InboundTrackMonitor and raises synthesized-audio using playout counters through that track.
5. **Scoring prose:** “open issues and nothing else,” “healthy/no issues always 5,” and root score becomes undefined with nothing measurable do not describe all actual paths. Continuous ramps and root early-return/default behavior contradict those statements.
6. **Observer AGENTS architecture:** references update-policy classes, IssueIndex, TrackDistributionAggregator, default detectors/DetectorsConfig.ts; current code instead has simplified update flow, ActiveIssuesRegistry, explicit registration and per-detector configs. Repository guidance is not a current API reference.
7. **Observer AcceptContext comment:** says merged into appData; actual factories can consume it at creation, and it is otherwise transient event context. Current changelog/config text correctly explains the distinction.
8. **Observer middleware contract — reproduced:** omitting next does not stop ingestion; throwing logs “dropping” but still ingests; next(newPayload) does not replace the object dispatched. `Observer.accept` proceeds after process(), and no final callback controls dispatch. The existing middleware tests cover ordering/mutation/removal, not these advertised cases.
9. **On-change ICE compatibility — reproduced:** client sends static ICE metadata first/on change by default; ObservedIceTransport.update assigns absent metadata to undefined. Thus roles, certificate IDs and crypto fields disappear on ordinary later samples. This needs a receiver-side retention contract or explicit sender setting, not documentation alone.
10. **Zero score history — reproduced:** ObservedClient accepts score 0, but `if (this.calculatedScore.value)` skips its cumulative score measurement count. Current instantaneous score remains 0; historical counters omit that measurement.
11. **Next vs schema:** next interruptionCount/totalInterruptionDuration are raw browser extras held locally, deliberately not schema 3.7.0 fields. Do not promise backend replay of the raw interruption counters from ClientSample.
12. **Site dependency mismatch:** installed lockfile is stable client 4.9.0 and observer beta.23, not the latest versions traced above.

Evidence: [client-monitor-js/docs/DERIVED_METRICS.md](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/docs/DERIVED_METRICS.md), [client-monitor-js/src/utils/common.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/common.ts), [client-monitor-js/src/ClientMonitorConfig.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitorConfig.ts), [client-monitor-js/src/detectors/AudioPlayoutSynthesisDetector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/AudioPlayoutSynthesisDetector.ts), [client-monitor-js/docs/DETECTOR_TAXONOMY.md](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/docs/DETECTOR_TAXONOMY.md), [client-monitor-js/src/scores/DefaultScoreCalculator.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/DefaultScoreCalculator.ts), [observer-js/AGENTS.md](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/AGENTS.md), [observer-js/src/Observer.ts · accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts#L710), [observer-js/src/common/Middleware.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/common/Middleware.ts), [observer-js/src/ObservedIceTransport.ts · update](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedIceTransport.ts#L53), [observer-js/src/ObservedClient.ts · accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts#L217). Reproduction outputs are saved separately. These findings were documented, not fixed.

## Other organization repositories

- **stats-dashboard**: current downstream consumer. `src/lib/s3.ts` resolves storage keys/listing/streams; API/routes and analysis code consume per-client JSONL plus call-summary and mediasoup-router artifacts. Its expected room/call/client layout is implemented by the demo's ObserverService uploads. Useful for schema evolution and replay compatibility, not an authority overriding schema definitions. [stats-dashboard/src/lib/s3.ts](https://github.com/ObserveRTC/stats-dashboard/blob/323a1b28553758edafaa0abd0d4211c9e13de9ea/src/lib/s3.ts), [stats-dashboard/README.md](https://github.com/ObserveRTC/stats-dashboard/blob/323a1b28553758edafaa0abd0d4211c9e13de9ea/README.md).
- **website-3.0**: current documentation content under `content/docs/client-monitor-js`, `observer-js`, and schema-related pages; useful material for a project website, with the same need for source-version checks. [website-3.0/content/docs/client-monitor-js/_index.md](https://github.com/ObserveRTC/website-3.0/blob/f5b4fb65a44eeaac7b17575569d413ba4c78d86c/content/docs/client-monitor-js/_index.md), [website-3.0/content/docs/observer-js/_index.md](https://github.com/ObserveRTC/website-3.0/blob/f5b4fb65a44eeaac7b17575569d413ba4c78d86c/content/docs/observer-js/_index.md).
- **full-stack-examples**: older Docker/service architecture; its mediasoup Monitor.ts uses createMediasoupMonitor/connect and older sender/storage APIs. Useful historical integration patterns, not copy/paste examples for current observer-js 1.0. [full-stack-examples/mediasoup-sfu/src/Monitor.ts](https://github.com/ObserveRTC/full-stack-examples/blob/26ec2d1ef87a6e0a576aa6bea1d453b9b089eb18/mediasoup-sfu/src/Monitor.ts), [full-stack-examples/docker-compose.yaml](https://github.com/ObserveRTC/full-stack-examples/blob/26ec2d1ef87a6e0a576aa6bea1d453b9b089eb18/docker-compose.yaml).
- **sfu-monitor-js**: archived, package 2.0.3 depends on old sample-schemas-js 2.2.1-rc.0, collector/storage/sampler design. Do not substitute it for current ObservedMediasoupRouter integration. [sfu-monitor-js/package.json](https://github.com/ObserveRTC/sfu-monitor-js/blob/6f1758976a89d4f31329a7f9caacec77b949ebeb/package.json), [sfu-monitor-js/src/SfuMonitorImpl.ts](https://github.com/ObserveRTC/sfu-monitor-js/blob/6f1758976a89d4f31329a7f9caacec77b949ebeb/src/SfuMonitorImpl.ts), [sfu-monitor-js/src/mediasoup/MediasoupCollector.ts](https://github.com/ObserveRTC/sfu-monitor-js/blob/6f1758976a89d4f31329a7f9caacec77b949ebeb/src/mediasoup/MediasoupCollector.ts).
- The organization inventory also exposed observer-service, getstats-lab, sample-reports, demo-app, and archived website/webextrapp/Node-RED repositories. They were triaged by metadata; their full code was not audited. They are not silently assumed current or compatible.

## Where future changes belong

| Change | Implementation and verification path |
|---|---|
| New browser field | W3C/schema definitions if appropriate → schema generation → synchronized generated types → owner monitor assignment + createSample → observer entity update → browser-availability tests |
| New local derived metric | owner monitor accept/update/getter; reset/missing/stale semantics; raw→derived unit/formula metadata; tests for counter reset, no progress and missing input; serialize only if backend needs the value itself |
| New client detector | Detector class with category/layer, config type, constructor defaults, correct owner registration, event payload/type, issue union, source tests/taxonomy test; independently define trigger/recovery and unavailable behavior |
| New score behavior | DefaultScoreCalculator and relevant monitor readings; component reasons and root aggregation kept distinct; verify absence/zero/continuous reason visibility |
| New schema field | authoritative Avro/chunk, source version/changelog, generator outputs/packages, both consumer copies, codec roundtrips and compatibility tests |
| New server entity behavior | appropriate Observed*.update/accept, ObserverEvents typed scope, lifecycle cleanup, metric reset semantics, focused source tests |
| New server detector | class + AvailableCallScope/ObserverScopeDetectorsConfigs + appropriate addDetector factory switch + index exports; explicit application registration |
| New structural validation | Validator + AvailableValidatorConfigs + Observer.addValidator switch; evidence-backed positive/negative/inconclusive behavior |
| New SFU integration | application signaling/attachments → RemoteTrackResolverFactory; optional server object observer; no guessed publisher linkage |
| Catalog changes | replace regex/schema-membership provenance with explicit/AST-backed metadata; derive docs from pinned package/source; generation check prevents drift |
| Site content/layout | design source + build-page generator + client modules; regenerate HTML/catalog and bundle, then check responsive layout and source facts |

Useful tests to extend: client `tests/monitors/DerivedFields.spec.ts`, `UnreportedRoundRecovery.spec.ts`, `EndedTrackStandDown.spec.ts`, `RemoteRtcpReportStaleness.spec.ts`, detector-specific specs and `DetectorTaxonomy.spec.ts`, scoring specs; observer `acceptMiddleware.spec.ts`, `issueLifecycle.spec.ts`, `payloadWireGenerations.spec.ts`, `injection.spec.ts`, `RemoteTrackResolver.spec.ts`, `mediasoupRouter.spec.ts`, `callSummary.spec.ts`; schema JSON/protobuf codec roundtrip/delta/nested-payload/error tests. The full library suites were not run during this analysis.
