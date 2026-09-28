# Monitor fields and exact calculations
Generated from the TypeScript AST, not from README lists. Stable 4.9.1 is the main inventory. Schema membership alone is NOT a provenance test: attachments, identity, context, adapter reconstruction and detector outputs are distinct. Each assignment links to its full enclosing implementation; read its guards before using the expression. Assignments are an index, not a promise that every field is refreshed every tick.

## ClientMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L62)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `samplingSchemaVersion` | public static readonly samplingSchemaVersion = schemaVersion; | [L63](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L63) |
| `createdAt` | public readonly createdAt = Date.now(); | [L64](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L64) |
| `mappedPeerConnections` | public readonly mappedPeerConnections = new Map&lt;string, PeerConnectionMonitor&gt;(); | [L66](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L66) |
| `mappedExtensionStatsMonitors` | public readonly mappedExtensionStatsMonitors = new Map&lt;string, ExtensionStatsMonitor&gt;(); | [L67](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L67) |
| `detectors` | Detectors | [L68](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L68) |
| `clientEventPayloadProvider` | public readonly clientEventPayloadProvider = new ClientEventPayloadProvider(); | [L69](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L69) |
| `extensionStatsProviders` | public readonly extensionStatsProviders = new Set&lt;ExtensionStatProvider&gt;(); | [L70](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L70) |
| `activeIssues` | IssueRegistry | [L77](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L77) |
| `slicedWindow` | SlicedWindow&lt;
        ClientWindowValues,
        Record&lt;keyof ClientWindowConfig['numberOfSamples'], SliceConfig&gt;
    &gt; | [L84](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L84) |
| `scoreCalculator` | ScoreCalculator | [L89](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L89) |
| `logger` | Logger | [L90](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L90) |
| `closed` | public closed = false; | [L91](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L91) |
| `lastSampledAt` | public lastSampledAt = 0; | [L92](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L92) |
| `lastCollectingStatsAt` | public lastCollectingStatsAt = 0; | [L93](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L93) |
| `cpuPerformanceAlertOn` | public cpuPerformanceAlertOn = false; | [L95](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L95) |
| `cpuUtilization` | number | [L102](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L102) |
| `activeTab` | public activeTab = true; | [L110](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L110) |
| `sendingAudioBitrate` | public sendingAudioBitrate = -1; | [L112](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L112) |
| `sendingVideoBitrate` | public sendingVideoBitrate = -1; | [L113](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L113) |
| `receivingAudioBitrate` | public receivingAudioBitrate = -1; | [L114](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L114) |
| `receivingVideoBitrate` | public receivingVideoBitrate = -1; | [L115](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L115) |
| `totalAvailableIncomingBitrate` | public totalAvailableIncomingBitrate = -1; | [L116](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L116) |
| `totalAvailableOutgoingBitrate` | public totalAvailableOutgoingBitrate = -1; | [L117](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L117) |
| `avgRttInSec` | public avgRttInSec = -1; | [L119](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L119) |
| `score` | public score = 5.0; | [L120](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L120) |
| `scoreReasons` | Record&lt;string, number&gt; | [L121](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L121) |
| `durationOfCollectingStatsInMs` | public durationOfCollectingStatsInMs = 0; | [L136](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L136) |
| `config` | AppliedClientMonitorConfig&lt;AppData&gt; | [L137](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L137) |
| `attachments` | Record&lt;string, unknown&gt; | [L144](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L144) |
| `clientId` | public get clientId() { return this.config.clientId; } | [L498](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L498) |
| `callId` | public get callId() { return this.config.callId; } | [L503](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L503) |
| `appData` | AppData | [L508](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L508) |
| `uptimeInMs` | public get uptimeInMs() { | [L521](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L521) |
| `browser` | public get browser() { | [L546](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L546) |
| `peerConnections` | public get peerConnections() { | [L1076](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1076) |
| `codecs` | public get codecs() { | [L1080](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1080) |
| `inboundRtps` | public get inboundRtps() { | [L1084](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1084) |
| `outboundRtps` | public get outboundRtps() { | [L1088](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1088) |
| `remoteInboundRtps` | public get remoteInboundRtps() { | [L1092](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1092) |
| `remoteOutboundRtps` | public get remoteOutboundRtps() { | [L1096](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1096) |
| `mediaSources` | public get mediaSources() { | [L1100](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1100) |
| `mediaPlayouts` | public get mediaPlayouts() { | [L1104](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1104) |
| `dataChannels` | public get dataChannels() { | [L1108](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1108) |
| `iceCandidatePairs` | public get iceCandidatePairs() { | [L1112](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1112) |
| `iceCandidates` | public get iceCandidates() { | [L1116](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1116) |
| `iceTransports` | public get iceTransports() { | [L1120](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1120) |
| `certificates` | public get certificates() { | [L1124](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1124) |
| `tracks` | TrackMonitor[] | [L1128](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1128) |

### Assignment and formula index

- **logger** [L152](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L152): `this.logger = monitorConfig.logger ?? createLogger()`
- **config** [L165](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L165): `this.config = { ...monitorConfig, collectingPeriodInMs: monitorConfig.collectingPeriodInMs ?? 5000, samplingPeriodInMs: monitorConfig.samplingPeriodInMs ?? 5000, integrateNavigatorMediaDevices: monitorConfig.integrateNavigatorMediaDevices ?? true, watchTabVisibility: monitorConfig.watchTabVisibility ?? true, addClientJointEventOnCreated: monitorConfig.addClientJointEventOnCreated ?? true, addClientLeftEventOnClose: monitorConfig.addClientLeftEventOnClose ?? true, // The slices are counted in values, not milliseconds, so that a slice asked for N // values holds N at any collecting period and is readable at any cadence. What varies // is the stretch those values span: N values span N-1 intervals, so at the default // 5000ms period a slice of 2 covers 5s and one of 4 covers 15s. 'maxAllowedGapInMs' // tolerates a couple of late or missed collections and treats anything longer as a // blackout worth starting again after. outboundTrackWindow: monitorConfig.outboundTrackWindow ?? { numberOfSamples: { detection: 3, recovery: 3, }, maxAllowedGapInMs: collectingPeriodInMs * 4, }, inboundTrackWindow: monitorConfig.inboundTrackWindow ?? { numberOfSamples: { detection: 3, recovery: 3, flowDetection: 4, flowRecovery: 3, }, maxAllowedGapInMs: collectingPeriodInMs * 4, }, peerConnectionWindow: monitorConfig.peerConnectionWindow ?? { numberOfSamples: { detection: 3, recovery: 3, }, maxAllowedGapInMs: collectingPeriodInMs * 4, }, clientWindow: monitorConfig.clientWindow ?? { numberOfSamples: { detection: 3, recovery: 3, }, maxAllowedGapInMs: collectingPeriodInMs * 4, }, // Detector defaults, one entry per detector, grouped as in // 'ClientMonitorConfig' so the two files read side by side. // Connectivity — layer 1: reachability. iceReachabilityDetector: detectorDefault(monitorConfig.iceReachabilityDetector, { thresholdInMs: 6000, }), // Layer 2 — traversal. Telemetry, nothing to tune. iceTraversalDetector: detectorDefault(monitorConfig.iceTraversalDetector, {}), // Layer 3 — path establishment: slow, then demonstrably failed. icePathEstablishmentDetector: detectorDefault(monitorConfig.icePathEstablishmentDetector, { thresholdInMs: 5000, createEvent: true, }), iceEstablishmentFailedDetector: detectorDefault(monitorConfig.iceEstablishmentFailedDetector, { thresholdInMs: 15000, }), // Layer 4 — secure transport. 'failed' is terminal, so no threshold. dtlsHandshakeFailedDetector: detectorDefault(monitorConfig.dtlsHandshakeFailedDetector, {}), dtlsHandshakeStalledDetector: detectorDefault(monitorConfig.dtlsHandshakeStalledDetector, { stalledThresholdInMs: 6000, }), // Layer 5 — path continuity: down, finished, delivering nothing, // or never settling. iceDisconnectedDetector: detectorDefault(monitorConfig.iceDisconnectedDetector, { disconnectedThresholdInMs: 5000, }), iceConnectionFailedDetector: detectorDefault(monitorConfig.iceConnectionFailedDetector, {}), iceTransportStalledDetector: detectorDefault(monitorConfig.iceTransportStalledDetector, { transportStallThresholdInMs: 5000, }), unstableIcePathDetector: detectorDefault(monitorConfig.unstableIcePathDetector, { pathSwitchWindowInMs: 30000, pathSwitchThreshold: 3, }), // Connectivity telemetry. Recommendation thresholds sit wider than // the issue thresholds beside them, on purpose. iceRestartDetector: detectorDefault(monitorConfig.iceRestartDetector, { createEvent: true, }), iceRestartRecommendationDetector: detectorDefault(monitorConfig.iceRestartRecommendationDetector, { createEvent: true, iceRestartRecommendationThresholdInMs: 10000, iceRestartRecommendationCooldownInMs: 15000, restartRecommendationThresholdInMs: 10000, restartRecommendationCooldownInMs: 15000, }), // Transport Quality — the properties of a working path. These // thresholds are starting points, meant to be tuned against a fleet. // Deprecated, on by default so integrations built against the 'congestion' event keep // working. Set to 'null' once nothing depends on it. congestionDetector: detectorDefault(monitorConfig.congestionDetector, { sensitivity: 'medium' as const, }), uplinkCongestionDetector: detectorDefault(monitorConfig.uplinkCongestionDetector, { minSeverity: 0.65, // Four times the connection's own median pacer delay tops the scale. pacerBloatingSaturatesAt: 4, }), downlinkCongestionDetector: detectorDefault(monitorConfig.downlinkCongestionDetector, { minSeverity: 0.65, // Four times the connection's own median jitter buffer delay tops the scale. bufferBloatingSaturatesAt: 4, }), transportDelayDetector: detectorDefault(monitorConfig.transportDelayDetector, { // ~300ms round trip is where turn-taking starts to break down. thresholdInMs: 300, recoveryThresholdInMs: 200, // The sustain lives in 'peerConnectionWindow', not here. }), transportLossDetector: detectorDefault(monitorConfig.transportLossDetector, { threshold: 0.05, recoveryThreshold: 0.01, durationInMs: 6000, }), blockedStunRequestsDetector: detectorDefault(monitorConfig.blockedStunRequestsDetector, { responseReceivedTimeoutInMs: 10000, requestsSentTimeoutInMs: 10000, }), blockedOutboundMediaDetector: detectorDefault(monitorConfig.blockedOutboundMediaDetector, { thresholdInMs: 10000, }), // Defaults to 'null': its premise fails wherever rtcp-mux is in // force, which is every browser. See 'ClientMonitorConfig'. blockedInboundMediaDetector: detectorDefault(monitorConfig.blockedInboundMediaDetector, null), // Pipeline Disruption — the send chain, from the capture device to // the wire. captureSourceLostDetector: detectorDefault(monitorConfig.captureSourceLostDetector, { createEvent: true, }), silentAudioSourceDetector: detectorDefault(monitorConfig.silentAudioSourceDetector, { silenceThresholdInMs: 60000, silenceRmsThreshold: 0.0001, recoveryRmsThreshold: 0.0003, }), videoCaptureBottleneckDetector: detectorDefault(monitorConfig.videoCaptureBottleneckDetector, { produceDegradationThreshold: 0.2, }), encoderBottleneckDetector: detectorDefault(monitorConfig.encoderBottleneckDetector, { encodeDegradationThreshold: 0.3, }), rtpSenderStalledDetector: detectorDefault(monitorConfig.rtpSenderStalledDetector, { thresholdInMs: 4000, }), dryOutboundTrackDetector: detectorDefault(monitorConfig.dryOutboundTrackDetector, { thresholdInMs: 5000, }), // Pipeline Disruption — the receive chain, from the transport to the // renderer. transportDemuxStalledDetector: detectorDefault(monitorConfig.transportDemuxStalledDetector, { thresholdInMs: 4000, minTransportReceiveBitrateBps: 20000, }), dryInboundTrackDetector: detectorDefault(monitorConfig.dryInboundTrackDetector, { thresholdInMs: 5000, }), frameAssemblyStalledDetector: detectorDefault(monitorConfig.frameAssemblyStalledDetector, { thresholdInMs: 3000, minPacketsReceived: 20, }), decoderBottleneckDetector: detectorDefault(monitorConfig.decoderBottleneckDetector, { // 0.1 is the old decodeFpsRatioThreshold of 0.9, read as a shortfall. decodeDegradationThreshold: 0.1, minReceivedFps: 5, }), decoderPerformanceDetector: detectorDefault(monitorConfig.decoderPerformanceDetector, { decodeTimeBudgetRatio: 0.8, minFramesReceived: 10, quietLossThreshold: 0.02, minConsecutiveTicks: 2, }), stuckDecoderDetector: detectorDefault(monitorConfig.stuckDecoderDetector, { thresholdInMs: 4000, rttMultiplier: 15, minBitrate: 10000, minPliCount: 2, }), playoutDiscrepancyDetector: detectorDefault(monitorConfig.playoutDiscrepancyDetector, { lowSkewRatio: 0.1, highSkewRatio: 0.25, minFramesReceived: 10, }), // Pipeline Disruption — the repair loop beside the receive chain, and // the machine behind both chains. videoRecoveryFailedDetector: detectorDefault(monitorConfig.videoRecoveryFailedDetector, { recoveryFailedThresholdInMs: 5000, recoveryFailedMinPliCount: 2, }), cpuPerformanceDetector: detectorDefault(monitorConfig.cpuPerformanceDetector, { utilizationThreshold: 0.5, recoveryThreshold: 0.4, }), // Perceived Quality — how the picture and the sound come across. pixelatedVideoDetector: detectorDefault(monitorConfig.pixelatedVideoDetector, { // Fractions of the codec's own quantizer scale, so one pair covers every codec. // 0.62 is a mean quantizer of 79 on VP8 and 32 on H.264, either of which is // visibly coarse; 0.52 is 66 and 27, which is not. Starting points to calibrate // against a fleet, not findings. threshold: 0.62, recoveryThreshold: 0.52, durationInMs: 8000, }), inboundVideoFlowStateDetector: detectorDefault(monitorConfig.inboundVideoFlowStateDetector, { frozenAfterInMs: 2000, minFreezeCountForChoppy: 2, // The stretch both verdicts are measured over is the track's shared window, not a // duration here: see 'inboundTrackWindow'. }), inventedSpeechDetector: detectorDefault(monitorConfig.inventedSpeechDetector, { // Share of concealed audio tolerated before it counts against the budget. allowedInventedRatio: 0.05, // Invented audio beyond the allowance, in ms, that opens the issue. raiseAfterInventedMs: 400, }), audioPlayoutSynthesisDetector: detectorDefault(monitorConfig.audioPlayoutSynthesisDetector, { // A share of what was played, not a duration per collection. The previous // 'minSynthesizedSamplesDuration: 0' reported on every tick that concealed anything // at all, and its unit was seconds while the config documented milliseconds. synthesizedRatioThreshold: 0.05, createEvent: true, }), // Raise at the acceptability limits, resolve back inside the // detectability ones; audio behind video is forgiven further. avDesyncPlayoutDetector: detectorDefault(monitorConfig.avDesyncPlayoutDetector, { audioAheadRaiseInMs: 90, audioAheadResolveInMs: 45, audioBehindRaiseInMs: 185, audioBehindResolveInMs: 125, sustainForInMs: 3000, }), jitterBufferStressDetector: detectorDefault(monitorConfig.jitterBufferStressDetector, { targetDelayThresholdInMs: 200, timeStretchThreshold: 0.02, minConsecutiveTicks: 2, // Severity scale only, and absolute rather than relative to the thresholds above: // a second of buffering makes conversation impossible, and a seventh of the samples // warped is badly distorted speech. The thresholds land near 0.16 on that scale. unbearableTargetDelayInMs: 1000, unbearableTimeStretchRate: 0.15, }), // Telemetry — facts about the session, not faults. captureTrackMutedDetector: detectorDefault(monitorConfig.captureTrackMutedDetector, { createEvent: true, }), codecChangeDetector: detectorDefault(monitorConfig.codecChangeDetector, { createEvent: true, }), videoResolutionChangeDetector: detectorDefault(monitorConfig.videoResolutionChangeDetector, { createEvent: true, }), simulcastLayerDetector: detectorDefault(monitorConfig.simulcastLayerDetector, { createEvent: true, }), statsGapDetector: detectorDefault(monitorConfig.statsGapDetector, { gapRatioThreshold: 2, minGapInMs: 5000, createEvent: true, }), bufferingEventsForSamples: monitorConfig.bufferingEventsForSamples ?? false, bufferClientSamplesUntilSubscriber: monitorConfig.bufferClientSamplesUntilSubscriber ?? false, sendResolvedIssuesToServer: monitorConfig.sendResolvedIssuesToServer ?? true, sendScoreReasonsToServer: monitorConfig.sendScoreReasonsToServer ?? true, sendIceTransportMetadataOnChangeOnly: monitorConfig.sendIceTransportMetadataOnChangeOnly ?? true, appData: monitorConfig.appData ?? {} as AppData, }`
- **slicedWindow** [L437](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L437): `this.slicedWindow = new SlicedWindow({ maxAllowedGapInMs: this.config.clientWindow.maxAllowedGapInMs, totals: { totalVideoEncodeTimeInMs: null, totalVideoDecodeTimeInMs: null, }, slices: { detection: { numberOfSamples: this.config.clientWindow.numberOfSamples.detection, }, recovery: { numberOfSamples: this.config.clientWindow.numberOfSamples.recovery, offset: this.config.clientWindow.numberOfSamples.detection, }, }, })`
- **scoreCalculator** [L455](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L455): `this.scoreCalculator = new DefaultScoreCalculator(this)`
- **activeIssues** [L482](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L482): `this.activeIssues = new IssueRegistry({ notify: (issue) => this.addIssue(issue), raise: (input) => this._raiseIssue(input), update: (input) => this._updateIssue(input), resolve: (input) => this._resolveIssue(input), })`
- **detectors** [L489](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L489): `this.detectors = new Detectors()`
- **config.clientId** [L500](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L500): `this.config.clientId = clientId`
- **config.callId** [L505](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L505): `this.config.callId = callId`
- **config.appData** [L509](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L509): `this.config.appData = appData`
- **closed** [L580](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L580): `this.closed = true`
- **lastCollectingStatsAt** [L617](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L617): `this.lastCollectingStatsAt = Date.now()`
- **sendingAudioBitrate** [L640](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L640): `this.sendingAudioBitrate = this.peerConnections.reduce((acc, peerConnection) => acc + (peerConnection.sendingAudioBitrate ?? 0), 0)`
- **sendingVideoBitrate** [L641](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L641): `this.sendingVideoBitrate = this.peerConnections.reduce((acc, peerConnection) => acc + (peerConnection.sendingVideoBitrate ?? 0), 0)`
- **receivingAudioBitrate** [L642](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L642): `this.receivingAudioBitrate = this.peerConnections.reduce((acc, peerConnection) => acc + (peerConnection.receivingAudioBitrate ?? 0), 0)`
- **receivingVideoBitrate** [L643](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L643): `this.receivingVideoBitrate = this.peerConnections.reduce((acc, peerConnection) => acc + (peerConnection.receivingVideoBitrate ?? 0), 0)`
- **totalAvailableIncomingBitrate** [L644](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L644): `this.totalAvailableIncomingBitrate = this.peerConnections.reduce((acc, peerConnection) => acc + (peerConnection.totalAvailableIncomingBitrate ?? 0), 0)`
- **totalAvailableOutgoingBitrate** [L645](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L645): `this.totalAvailableOutgoingBitrate = this.peerConnections.reduce((acc, peerConnection) => acc + (peerConnection.totalAvailableOutgoingBitrate ?? 0), 0)`
- **avgRttInSec** [L647](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L647): `this.avgRttInSec = 0 < this.peerConnections.length ? this.peerConnections.reduce((acc, peerConnection) => acc + (peerConnection.avgRttInSec ?? 0), 0) / this.peerConnections.length : -1`
- **durationOfCollectingStatsInMs** [L650](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L650): `this.durationOfCollectingStatsInMs = Date.now() - this.lastCollectingStatsAt`
- **score** [L729](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L729): `this.score = score`
- **scoreReasons** [L730](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L730): `this.scoreReasons = ownReasons`
- **lastSampledAt** [L764](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L764): `this.lastSampledAt = timestamp`
- **config.collectingPeriodInMs** [L1200](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1200): `this.config.collectingPeriodInMs = collectingPeriodInMs`
- **config.samplingPeriodInMs** [L1214](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1214): `this.config.samplingPeriodInMs = samplingPeriodInMs`

### Exact wire projection
```ts
public createSample(): ClientSample | undefined {
        if (this.closed) return;

        const clientSample: ClientSample = {
            clientId: this.clientId,
            timestamp: Date.now(),
            callId: this.callId,
            attachments: this.attachments,
            peerConnections: this.peerConnections.map(peerConnection => peerConnection.createSample()),
            clientEvents: this._clientEvents,
            clientMetaItems: this._clientMetaItems,
            clientIssues: this._clientIssues,
            extensionStats: this._extensionStats,
            score: this.score,
            // The client's own reasons only; the aggregate lives on the 'score' event.
            scoreReasons: sampledScoreReasons(this.scoreReasons, this.config.sendScoreReasonsToServer),
        };
        this._clientEvents = [];
        this._clientMetaItems = [];
        this._clientIssues = [];
        this._extensionStats = [];

        const timestamp = Date.now();
        if (!clientSample) {
            return;
        }
        this.lastSampledAt = timestamp;

        if (this._bufferedClientSamples) {
            if (this.listenerCount('sample-created') === 0) {
                this._bufferedClientSamples.push(clientSample);
            } else {
                this._flushBufferedClientSamples();
            }
        }

        this.emit('sample-created', {
            clientMonitor: this,
            sample: clientSample
        });

        return clientSample;
    }
```

## CertificateMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L4)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `timestamp` | number | [L7](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L7) |
| `id` | string | [L8](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L8) |
| `fingerprint` | string  /  undefined | [L9](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L9) |
| `fingerprintAlgorithm` | string  /  undefined | [L10](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L10) |
| `base64Certificate` | string  /  undefined | [L11](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L11) |
| `issuerCertificateId` | string  /  undefined | [L12](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L12) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L17](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L17) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L22](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L22) |
| `visited` | boolean | [L35](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L35) |

### Assignment and formula index

- **id** [L28](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L28): `this.id = options.id`
- **timestamp** [L29](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CertificateMonitor.ts#L29): `this.timestamp = options.timestamp`

### Exact wire projection
```ts
public createSample(): CertificateStats {
		return {
			id: this.id,
			timestamp: this.timestamp,
			fingerprint: this.fingerprint,
			fingerprintAlgorithm: this.fingerprintAlgorithm,
			base64Certificate: this.base64Certificate,
			issuerCertificateId: this.issuerCertificateId,
			attachments: this.attachments,
		};
	}
```

## CodecMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L4)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `timestamp` | number | [L7](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L7) |
| `id` | string | [L8](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L8) |
| `payloadType` | number | [L9](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L9) |
| `transportId` | string | [L10](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L10) |
| `mimeType` | string | [L11](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L11) |
| `clockRate` | number  /  undefined | [L12](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L12) |
| `channels` | number  /  undefined | [L13](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L13) |
| `sdpFmtpLine` | string  /  undefined | [L14](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L14) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L19](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L19) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L24](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L24) |
| `visited` | boolean | [L37](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L37) |

### Assignment and formula index

- **id** [L30](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L30): `this.id = options.id`
- **timestamp** [L31](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L31): `this.timestamp = options.timestamp`
- **mimeType** [L32](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/CodecMonitor.ts#L32): `this.mimeType = options.mimeType`

### Exact wire projection
```ts
public createSample(): CodecStats {
		return {
			id: this.id,
			timestamp: this.timestamp,
			payloadType: this.payloadType,
			transportId: this.transportId,
			mimeType: this.mimeType,
			clockRate: this.clockRate,
			channels: this.channels,
			sdpFmtpLine: this.sdpFmtpLine,
			attachments: this.attachments,
		};
	}
```

## DataChannelMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L5)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `timestamp` | number | [L8](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L8) |
| `id` | string | [L9](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L9) |
| `label` | string  /  undefined | [L10](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L10) |
| `protocol` | string  /  undefined | [L11](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L11) |
| `dataChannelIdentifier` | number  /  undefined | [L12](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L12) |
| `state` | string  /  undefined | [L13](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L13) |
| `messagesSent` | number  /  undefined | [L14](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L14) |
| `bytesSent` | number  /  undefined | [L15](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L15) |
| `messagesReceived` | number  /  undefined | [L16](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L16) |
| `bytesReceived` | number  /  undefined | [L17](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L17) |
| `deltaBytesSent` | number  /  undefined | [L19](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L19) |
| `deltaBytesReceived` | number  /  undefined | [L20](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L20) |
| `sendingBitrate` | number  /  undefined | [L22](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L22) |
| `receivingBitrate` | number  /  undefined | [L23](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L23) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L25](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L25) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L27](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L27) |
| `visited` | boolean | [L45](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L45) |

### Assignment and formula index

- **id** [L33](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L33): `this.id = options.id`
- **timestamp** [L34](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L34): `this.timestamp = options.timestamp`
- **deltaBytesReceived** [L63](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L63): `this.deltaBytesReceived = positiveDelta(stats.bytesReceived, this.bytesReceived)`
- **deltaBytesSent** [L64](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L64): `this.deltaBytesSent = positiveDelta(stats.bytesSent, this.bytesSent)`
- **sendingBitrate** [L67](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L67): `this.sendingBitrate = Math.max(0, this.deltaBytesSent * 8 / elapsedInSec)`
- **receivingBitrate** [L71](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/DataChannelMonitor.ts#L71): `this.receivingBitrate = Math.max(0, this.deltaBytesReceived * 8 / elapsedInSec)`

### Exact wire projection
```ts
public createSample(): DataChannelStats {
		return {
			id: this.id,
			timestamp: this.timestamp,
			label: this.label,
			protocol: this.protocol,
			dataChannelIdentifier: this.dataChannelIdentifier,
			state: this.state,
			messagesSent: this.messagesSent,
			bytesSent: this.bytesSent,
			messagesReceived: this.messagesReceived,
			bytesReceived: this.bytesReceived,
			attachments: this.attachments,
		};
	}
```

## ExtensionStatsMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/ExtensionStatsMonitor.ts#L12)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `visited` | public visited = true; | [L17](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/ExtensionStatsMonitor.ts#L17) |
| `payload` | Record&lt;string, unknown&gt; | [L20](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/ExtensionStatsMonitor.ts#L20) |
| `timestamp` | public timestamp = Date.now(); | [L23](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/ExtensionStatsMonitor.ts#L23) |

### Assignment and formula index

- **visited** [L34](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/ExtensionStatsMonitor.ts#L34): `this.visited = true`
- **payload** [L35](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/ExtensionStatsMonitor.ts#L35): `this.payload = payload`
- **timestamp** [L36](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/ExtensionStatsMonitor.ts#L36): `this.timestamp = Date.now()`

## IceCandidateMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L12)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `timestamp` | number | [L15](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L15) |
| `id` | string | [L16](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L16) |
| `transportId` | string  /  undefined | [L17](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L17) |
| `address` | string  /  undefined | [L18](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L18) |
| `port` | number  /  undefined | [L19](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L19) |
| `protocol` | string  /  undefined | [L20](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L20) |
| `candidateType` | string  /  undefined | [L21](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L21) |
| `priority` | number  /  undefined | [L22](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L22) |
| `url` | string  /  undefined | [L23](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L23) |
| `relayProtocol` | string  /  undefined | [L24](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L24) |
| `foundation` | string  /  undefined | [L25](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L25) |
| `relatedAddress` | string  /  undefined | [L26](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L26) |
| `relatedPort` | number  /  undefined | [L27](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L27) |
| `usernameFragment` | string  /  undefined | [L28](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L28) |
| `tcpType` | string  /  undefined | [L29](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L29) |
| `direction` | 'local'  /  'remote' | [L32](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L32) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L35](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L35) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L37](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L37) |
| `visited` | boolean | [L49](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L49) |
| `isRelay` | boolean | [L80](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L80) |
| `turnTransport` | IceRelayProtocol  /  undefined | [L85](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L85) |
| `turnServer` | string  /  undefined | [L100](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L100) |
| `addressFamily` | IceAddressFamily  /  undefined | [L108](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L108) |

### Assignment and formula index

- **id** [L43](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L43): `this.id = options.id`
- **timestamp** [L44](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidateMonitor.ts#L44): `this.timestamp = options.timestamp`

### Exact wire projection
```ts
public createSample(): IceCandidateStats {
		return {
			id: this.id,
			timestamp: this.timestamp,
			transportId: this.transportId,
			address: this.address,
			port: this.port,
			protocol: this.protocol,
			candidateType: this.candidateType,
			priority: this.priority,
			url: this.url,
			relayProtocol: this.relayProtocol,
			foundation: this.foundation,
			relatedAddress: this.relatedAddress,
			relatedPort: this.relatedPort,
			usernameFragment: this.usernameFragment,
			tcpType: this.tcpType,
			attachments: this.attachments,
		};
	}
```

## IceCandidatePairMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L15)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `id` | string | [L18](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L18) |
| `timestamp` | number | [L19](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L19) |
| `transportId` | string  /  undefined | [L20](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L20) |
| `localCandidateId` | string  /  undefined | [L21](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L21) |
| `remoteCandidateId` | string  /  undefined | [L22](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L22) |
| `state` | &quot;new&quot;  /  &quot;in-progress&quot;  /  &quot;failed&quot;  /  &quot;waiting&quot;  /  &quot;succeeded&quot;  /  undefined | [L23](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L23) |
| `nominated` | boolean  /  undefined | [L24](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L24) |
| `packetsSent` | number  /  undefined | [L25](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L25) |
| `packetsReceived` | number  /  undefined | [L26](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L26) |
| `bytesSent` | number  /  undefined | [L27](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L27) |
| `bytesReceived` | number  /  undefined | [L28](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L28) |
| `lastPacketSentTimestamp` | number  /  undefined | [L29](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L29) |
| `lastPacketReceivedTimestamp` | number  /  undefined | [L30](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L30) |
| `totalRoundTripTime` | number  /  undefined | [L31](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L31) |
| `currentRoundTripTime` | number  /  undefined | [L32](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L32) |
| `availableOutgoingBitrate` | number  /  undefined | [L33](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L33) |
| `availableIncomingBitrate` | number  /  undefined | [L34](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L34) |
| `requestsReceived` | number  /  undefined | [L35](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L35) |
| `requestsSent` | number  /  undefined | [L36](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L36) |
| `responsesReceived` | number  /  undefined | [L37](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L37) |
| `responsesSent` | number  /  undefined | [L38](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L38) |
| `consentRequestsSent` | number  /  undefined | [L39](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L39) |
| `packetsDiscardedOnSend` | number  /  undefined | [L40](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L40) |
| `bytesDiscardedOnSend` | number  /  undefined | [L41](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L41) |
| `deltaPacketsSent` | number  /  undefined | [L43](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L43) |
| `deltaPacketsReceived` | number  /  undefined | [L44](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L44) |
| `deltaBytesSent` | number  /  undefined | [L45](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L45) |
| `deltaBytesReceived` | number  /  undefined | [L46](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L46) |
| `deltaTotalRoundTripTime` | number  /  undefined | [L47](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L47) |
| `deltaRequestsSent` | number  /  undefined | [L48](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L48) |
| `deltaConsentRequestsSent` | number  /  undefined | [L53](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L53) |
| `deltaResponsesReceived` | number  /  undefined | [L54](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L54) |
| `deltaPacketsDiscardedOnSend` | number  /  undefined | [L59](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L59) |
| `deltaBytesDiscardedOnSend` | number  /  undefined | [L61](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L61) |
| `deltaTime` | number  /  undefined | [L64](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L64) |
| `avgRoundTripTimeInSec` | number  /  undefined | [L70](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L70) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L73](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L73) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L75](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L75) |
| `visited` | boolean | [L87](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L87) |
| `statsClockTime` | public statsClockTime = 0; | [L136](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L136) |
| `pathKey` | string | [L159](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L159) |
| `usingTurn` | boolean | [L164](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L164) |
| `usingTcp` | boolean | [L172](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L172) |
| `relayProtocol` | IceRelayProtocol  /  undefined | [L177](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L177) |
| `turnUrl` | string  /  undefined | [L182](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L182) |
| `turnServer` | string  /  undefined | [L187](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L187) |
| `pathKind` | IcePathKind | [L191](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L191) |
| `tuple` | string | [L207](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L207) |

### Assignment and formula index

- **id** [L81](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L81): `this.id = options.id`
- **timestamp** [L82](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L82): `this.timestamp = options.timestamp`
- **deltaTime** [L102](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L102): `this.deltaTime = elapsedInMs`
- **statsClockTime** [L103](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L103): `this.statsClockTime += elapsedInMs`
- **deltaPacketsSent** [L106](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L106): `this.deltaPacketsSent = positiveDelta(stats.packetsSent, this.packetsSent)`
- **deltaPacketsReceived** [L107](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L107): `this.deltaPacketsReceived = positiveDelta(stats.packetsReceived, this.packetsReceived)`
- **deltaBytesSent** [L108](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L108): `this.deltaBytesSent = positiveDelta(stats.bytesSent, this.bytesSent)`
- **deltaBytesReceived** [L109](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L109): `this.deltaBytesReceived = positiveDelta(stats.bytesReceived, this.bytesReceived)`
- **deltaTotalRoundTripTime** [L111](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L111): `this.deltaTotalRoundTripTime = positiveDelta(stats.totalRoundTripTime, this.totalRoundTripTime)`
- **deltaResponsesReceived** [L112](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L112): `this.deltaResponsesReceived = positiveDelta(stats.responsesReceived, this.responsesReceived)`
- **deltaRequestsSent** [L113](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L113): `this.deltaRequestsSent = positiveDelta(stats.requestsSent, this.requestsSent)`
- **deltaConsentRequestsSent** [L114](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L114): `this.deltaConsentRequestsSent = positiveDelta(stats.consentRequestsSent, this.consentRequestsSent)`
- **deltaPacketsDiscardedOnSend** [L115](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L115): `this.deltaPacketsDiscardedOnSend = positiveDelta(stats.packetsDiscardedOnSend, this.packetsDiscardedOnSend)`
- **deltaBytesDiscardedOnSend** [L116](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L116): `this.deltaBytesDiscardedOnSend = positiveDelta(stats.bytesDiscardedOnSend, this.bytesDiscardedOnSend)`
- **avgRoundTripTimeInSec** [L117](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L117): `this.avgRoundTripTimeInSec = this.deltaTotalRoundTripTime !== undefined && this.deltaResponsesReceived !== undefined && this.deltaResponsesReceived > 0 ? this.deltaTotalRoundTripTime / this.deltaResponsesReceived : undefined`
- **availableOutgoingBitrate** [L127](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L127): `this.availableOutgoingBitrate = stats.availableOutgoingBitrate`
- **availableIncomingBitrate** [L128](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceCandidatePairMonitor.ts#L128): `this.availableIncomingBitrate = stats.availableIncomingBitrate`

### Exact wire projection
```ts
public createSample(): IceCandidatePairStats {
		return {
			id: this.id,
			timestamp: this.timestamp,
			transportId: this.transportId,
			localCandidateId: this.localCandidateId,
			remoteCandidateId: this.remoteCandidateId,
			state: this.state,
			nominated: this.nominated,
			packetsSent: this.packetsSent,
			packetsReceived: this.packetsReceived,
			bytesSent: this.bytesSent,
			bytesReceived: this.bytesReceived,
			lastPacketSentTimestamp: this.lastPacketSentTimestamp,
			lastPacketReceivedTimestamp: this.lastPacketReceivedTimestamp,
			totalRoundTripTime: this.totalRoundTripTime,
			currentRoundTripTime: this.currentRoundTripTime,
			availableOutgoingBitrate: this.availableOutgoingBitrate,
			availableIncomingBitrate: this.availableIncomingBitrate,
			requestsReceived: this.requestsReceived,
			requestsSent: this.requestsSent,
			responsesReceived: this.responsesReceived,
			responsesSent: this.responsesSent,
			consentRequestsSent: this.consentRequestsSent,
			packetsDiscardedOnSend: this.packetsDiscardedOnSend,
			bytesDiscardedOnSend: this.bytesDiscardedOnSend,
			attachments: this.attachments,
		};
	}
```

## IceTransportMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L17)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `detectors` | Detectors | [L24](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L24) |
| `issues` | IssueRegistry&lt;IceTransportIssues&gt; | [L31](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L31) |
| `timestamp` | number | [L33](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L33) |
| `id` | string | [L34](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L34) |
| `packetsSent` | number  /  undefined | [L35](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L35) |
| `packetsReceived` | number  /  undefined | [L36](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L36) |
| `bytesSent` | number  /  undefined | [L37](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L37) |
| `bytesReceived` | number  /  undefined | [L38](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L38) |
| `iceRole` | string  /  undefined | [L39](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L39) |
| `iceLocalUsernameFragment` | string  /  undefined | [L40](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L40) |
| `dtlsState` | string  /  undefined | [L41](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L41) |
| `iceState` | string  /  undefined | [L42](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L42) |
| `selectedCandidatePairId` | string  /  undefined | [L43](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L43) |
| `localCertificateId` | string  /  undefined | [L44](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L44) |
| `remoteCertificateId` | string  /  undefined | [L45](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L45) |
| `tlsVersion` | string  /  undefined | [L46](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L46) |
| `dtlsCipher` | string  /  undefined | [L47](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L47) |
| `dtlsRole` | string  /  undefined | [L48](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L48) |
| `srtpCipher` | string  /  undefined | [L49](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L49) |
| `selectedCandidatePairChanges` | number  /  undefined | [L50](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L50) |
| `ccfbMessagesSent` | number  /  undefined | [L51](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L51) |
| `ccfbMessagesReceived` | number  /  undefined | [L52](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L52) |
| `deltaPacketsSent` | number  /  undefined | [L54](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L54) |
| `deltaPacketsReceived` | number  /  undefined | [L55](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L55) |
| `deltaBytesSent` | number  /  undefined | [L56](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L56) |
| `deltaBytesReceived` | number  /  undefined | [L57](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L57) |
| `sendingBitrate` | number  /  undefined | [L58](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L58) |
| `receivingBitrate` | number  /  undefined | [L59](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L59) |
| `deltaSelectedCandidatePairChanges` | number  /  undefined | [L64](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L64) |
| `deltaTime` | number  /  undefined | [L67](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L67) |
| `everConnected` | everConnected = false; | [L73](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L73) |
| `blocked` | public blocked = false; | [L80](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L80) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L83](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L83) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L85](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L85) |
| `visited` | boolean | [L106](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L106) |
| `statsClockTime` | public statsClockTime = 0; | [L119](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L119) |

### Assignment and formula index

- **id** [L91](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L91): `this.id = options.id`
- **timestamp** [L92](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L92): `this.timestamp = options.timestamp`
- **issues** [L96](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L96): `this.issues = new IssueRegistry<IceTransportIssues>( this._peerConnection.issues.asSink, )`
- **detectors** [L99](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L99): `this.detectors = new Detectors()`
- **deltaTime** [L157](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L157): `this.deltaTime = elapsedInMs`
- **statsClockTime** [L158](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L158): `this.statsClockTime += elapsedInMs`
- **everConnected** [L161](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L161): `this.everConnected = true`
- **deltaPacketsSent** [L165](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L165): `this.deltaPacketsSent = stats.packetsSent - this.packetsSent`
- **deltaPacketsSent** [L167](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L167): `this.deltaPacketsSent = undefined`
- **deltaPacketsReceived** [L170](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L170): `this.deltaPacketsReceived = stats.packetsReceived - this.packetsReceived`
- **deltaPacketsReceived** [L172](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L172): `this.deltaPacketsReceived = undefined`
- **deltaBytesSent** [L175](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L175): `this.deltaBytesSent = stats.bytesSent - this.bytesSent`
- **sendingBitrate** [L176](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L176): `this.sendingBitrate = (this.deltaBytesSent * 8) / elapsedInSec`
- **deltaBytesSent** [L178](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L178): `this.deltaBytesSent = undefined`
- **sendingBitrate** [L179](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L179): `this.sendingBitrate = undefined`
- **deltaBytesReceived** [L182](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L182): `this.deltaBytesReceived = stats.bytesReceived - this.bytesReceived`
- **receivingBitrate** [L183](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L183): `this.receivingBitrate = (this.deltaBytesReceived * 8) / elapsedInSec`
- **deltaBytesReceived** [L185](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L185): `this.deltaBytesReceived = undefined`
- **receivingBitrate** [L186](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L186): `this.receivingBitrate = undefined`
- **deltaSelectedCandidatePairChanges** [L191](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/IceTransportMonitor.ts#L191): `this.deltaSelectedCandidatePairChanges = this.selectedCandidatePairId !== undefined ? positiveDelta(stats.selectedCandidatePairChanges, this.selectedCandidatePairChanges) : undefined`

### Exact wire projection
```ts
public createSample(): IceTransportStats {
		// Constant after the handshake, so emitted in the first sample and again only on change
		// (the ufrag changes exactly at an ICE restart).
		const staticMetadata: Pick<IceTransportStats,
			'iceRole' | 'iceLocalUsernameFragment' | 'localCertificateId' | 'remoteCertificateId'
			| 'tlsVersion' | 'dtlsCipher' | 'dtlsRole' | 'srtpCipher'> = {
			iceRole: this.iceRole,
			iceLocalUsernameFragment: this.iceLocalUsernameFragment,
			localCertificateId: this.localCertificateId,
			remoteCertificateId: this.remoteCertificateId,
			tlsVersion: this.tlsVersion,
			dtlsCipher: this.dtlsCipher,
			dtlsRole: this.dtlsRole,
			srtpCipher: this.srtpCipher,
		};

		let sampledStaticMetadata: typeof staticMetadata | undefined = staticMetadata;

		if (this._peerConnection.parent.config.sendIceTransportMetadataOnChangeOnly) {
			const fingerprint = [
				this.iceRole, this.iceLocalUsernameFragment, this.localCertificateId, this.remoteCertificateId,
				this.tlsVersion, this.dtlsCipher, this.dtlsRole, this.srtpCipher,
			].join('|');

			if (this._sampledStaticMetadataFingerprint === fingerprint) {
				sampledStaticMetadata = undefined;
			} else {
				this._sampledStaticMetadataFingerprint = fingerprint;
			}
		}

		return {
			id: this.id,
			timestamp: this.timestamp,
			packetsSent: this.packetsSent,
			packetsReceived: this.packetsReceived,
			bytesSent: this.bytesSent,
			bytesReceived: this.bytesReceived,
			dtlsState: this.dtlsState,
			iceState: this.iceState,
			selectedCandidatePairId: this.selectedCandidatePairId,
			selectedCandidatePairChanges: this.selectedCandidatePairChanges,
			ccfbMessagesSent: this.ccfbMessagesSent,
			ccfbMessagesReceived: this.ccfbMessagesReceived,
			attachments: this.attachments,
			...(sampledStaticMetadata ?? {}),
		};
	}
```

## InboundRtpMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L8)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `addedAt` | public addedAt = Date.now(); | [L12](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L12) |
| `timestamp` | number | [L15](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L15) |
| `id` | string | [L16](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L16) |
| `ssrc` | number | [L17](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L17) |
| `kind` | MediaKind | [L18](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L18) |
| `trackIdentifier` | string | [L19](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L19) |
| `transportId` | string  /  undefined | [L20](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L20) |
| `codecId` | string  /  undefined | [L21](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L21) |
| `packetsReceived` | number  /  undefined | [L22](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L22) |
| `packetsReceivedWithEct1` | number  /  undefined | [L23](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L23) |
| `packetsReceivedWithCe` | number  /  undefined | [L24](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L24) |
| `packetsReportedAsLost` | number  /  undefined | [L25](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L25) |
| `packetsReportedAsLostButRecovered` | number  /  undefined | [L26](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L26) |
| `packetsLost` | number  /  undefined | [L27](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L27) |
| `jitter` | number  /  undefined | [L28](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L28) |
| `mid` | string  /  undefined | [L29](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L29) |
| `remoteId` | string  /  undefined | [L30](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L30) |
| `framesDecoded` | number  /  undefined | [L31](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L31) |
| `keyFramesDecoded` | number  /  undefined | [L32](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L32) |
| `framesRendered` | number  /  undefined | [L33](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L33) |
| `framesDropped` | number  /  undefined | [L34](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L34) |
| `frameWidth` | number  /  undefined | [L35](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L35) |
| `frameHeight` | number  /  undefined | [L36](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L36) |
| `framesPerSecond` | number  /  undefined | [L37](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L37) |
| `qpSum` | number  /  undefined | [L38](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L38) |
| `totalDecodeTime` | number  /  undefined | [L39](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L39) |
| `totalInterFrameDelay` | number  /  undefined | [L40](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L40) |
| `totalSquaredInterFrameDelay` | number  /  undefined | [L41](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L41) |
| `pauseCount` | number  /  undefined | [L42](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L42) |
| `totalPausesDuration` | number  /  undefined | [L43](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L43) |
| `freezeCount` | number  /  undefined | [L44](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L44) |
| `totalFreezesDuration` | number  /  undefined | [L45](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L45) |
| `lastPacketReceivedTimestamp` | number  /  undefined | [L46](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L46) |
| `headerBytesReceived` | number  /  undefined | [L47](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L47) |
| `packetsDiscarded` | number  /  undefined | [L48](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L48) |
| `fecBytesReceived` | number  /  undefined | [L49](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L49) |
| `fecPacketsReceived` | number  /  undefined | [L50](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L50) |
| `fecPacketsDiscarded` | number  /  undefined | [L51](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L51) |
| `bytesReceived` | number  /  undefined | [L52](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L52) |
| `nackCount` | number  /  undefined | [L53](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L53) |
| `firCount` | number  /  undefined | [L54](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L54) |
| `pliCount` | number  /  undefined | [L55](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L55) |
| `totalProcessingDelay` | number  /  undefined | [L56](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L56) |
| `estimatedPlayoutTimestamp` | number  /  undefined | [L57](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L57) |
| `jitterBufferDelay` | number  /  undefined | [L58](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L58) |
| `jitterBufferTargetDelay` | number  /  undefined | [L59](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L59) |
| `jitterBufferEmittedCount` | number  /  undefined | [L60](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L60) |
| `jitterBufferMinimumDelay` | number  /  undefined | [L61](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L61) |
| `totalSamplesReceived` | number  /  undefined | [L62](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L62) |
| `concealedSamples` | number  /  undefined | [L63](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L63) |
| `silentConcealedSamples` | number  /  undefined | [L64](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L64) |
| `concealmentEvents` | number  /  undefined | [L65](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L65) |
| `insertedSamplesForDeceleration` | number  /  undefined | [L66](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L66) |
| `removedSamplesForAcceleration` | number  /  undefined | [L67](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L67) |
| `audioLevel` | number  /  undefined | [L68](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L68) |
| `totalAudioEnergy` | number  /  undefined | [L69](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L69) |
| `totalSamplesDuration` | number  /  undefined | [L70](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L70) |
| `framesReceived` | number  /  undefined | [L71](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L71) |
| `decoderImplementation` | string  /  undefined | [L72](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L72) |
| `playoutId` | string  /  undefined | [L73](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L73) |
| `powerEfficientDecoder` | boolean  /  undefined | [L74](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L74) |
| `framesAssembledFromMultiplePackets` | number  /  undefined | [L75](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L75) |
| `totalAssemblyTime` | number  /  undefined | [L76](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L76) |
| `retransmittedPacketsReceived` | number  /  undefined | [L77](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L77) |
| `retransmittedBytesReceived` | number  /  undefined | [L78](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L78) |
| `rtxSsrc` | number  /  undefined | [L79](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L79) |
| `fecSsrc` | number  /  undefined | [L80](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L80) |
| `totalCorruptionProbability` | number  /  undefined | [L81](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L81) |
| `totalSquaredCorruptionProbability` | number  /  undefined | [L82](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L82) |
| `corruptionMeasurements` | number  /  undefined | [L83](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L83) |
| `bitrate` | number | [L86](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L86) |
| `avgFramesPerSec` | number | [L87](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L87) |
| `fpsVolatility` | number | [L97](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L97) |
| `lastNFramesPerSec` | number[] | [L98](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L98) |
| `receivingAudioSamples` | number | [L99](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L99) |
| `totalFractionLost` | number | [L100](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L100) |
| `bitPerPixel` | number | [L101](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L101) |
| `packetRate` | number  /  undefined | [L102](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L102) |
| `ewmaFps` | number | [L103](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L103) |
| `deltaPacketsLost` | number | [L105](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L105) |
| `deltaPacketsReceived` | number | [L106](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L106) |
| `deltaBytesReceived` | number | [L107](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L107) |
| `deltaJitterBufferDelay` | number | [L108](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L108) |
| `deltaCorruptionProbability` | number | [L109](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L109) |
| `deltaFractionLost` | number | [L110](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L110) |
| `deltaFramesDecoded` | number | [L111](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L111) |
| `deltaQpSum` | number  /  undefined | [L112](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L112) |
| `avgQpPerFrame` | number  /  undefined | [L114](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L114) |
| `normalizedQp` | number  /  undefined | [L132](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L132) |
| `deltaFramesReceived` | number | [L133](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L133) |
| `deltaFramesRendered` | number | [L134](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L134) |
| `deltaTime` | number | [L135](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L135) |
| `deltaTotalSamplesReceived` | number | [L138](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L138) |
| `deltaConcealedSamples` | number | [L139](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L139) |
| `deltaSilentConcealedSamples` | number | [L140](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L140) |
| `deltaConcealmentEvents` | number | [L141](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L141) |
| `deltaInsertedSamplesForDeceleration` | number | [L142](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L142) |
| `deltaRemovedSamplesForAcceleration` | number | [L143](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L143) |
| `deltaPacketsDiscarded` | number | [L144](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L144) |
| `deltaJitterBufferEmittedCount` | number | [L145](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L145) |
| `deltaJitterBufferTargetDelay` | number | [L146](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L146) |
| `inventedSpeechRatio` | number | [L152](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L152) |
| `concealmentEventRate` | number | [L153](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L153) |
| `timeStretchRate` | number | [L155](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L155) |
| `avgJitterBufferDelayInMs` | number | [L156](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L156) |
| `jitterBufferTargetDelayInMs` | number | [L157](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L157) |
| `discardRate` | number | [L158](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L158) |
| `deltaFramesDropped` | number | [L161](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L161) |
| `deltaKeyFramesDecoded` | number | [L162](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L162) |
| `deltaTotalDecodeTime` | number | [L163](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L163) |
| `deltaTotalFreezesDuration` | number | [L164](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L164) |
| `deltaFreezeCount` | number | [L166](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L166) |
| `frozenTimeRatio` | number | [L171](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L171) |
| `deltaPauseCount` | number | [L177](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L177) |
| `deltaTotalPausesDuration` | number | [L178](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L178) |
| `pausedTimeRatio` | number | [L180](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L180) |
| `deltaTotalInterFrameDelay` | number | [L181](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L181) |
| `deltaTotalSquaredInterFrameDelay` | number | [L182](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L182) |
| `avgInterFrameDelayInMs` | number | [L184](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L184) |
| `interFrameDelayVariation` | number | [L191](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L191) |
| `deltaPliCount` | number | [L192](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L192) |
| `deltaFirCount` | number | [L193](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L193) |
| `deltaNackCount` | number | [L194](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L194) |
| `deltaRetransmittedBytesReceived` | number | [L195](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L195) |
| `deltaRetransmittedPacketsReceived` | number | [L196](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L196) |
| `retransmissionRatio` | number | [L198](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L198) |
| `decodeTimePerFrameInMs` | number | [L199](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L199) |
| `droppedFrameRatio` | number | [L200](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L200) |
| `renderRatio` | number | [L201](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L201) |
| `keyFrameRate` | number | [L202](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L202) |
| `pliRate` | number | [L203](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L203) |
| `firRate` | number | [L204](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L204) |
| `nackRate` | number | [L205](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L205) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L208](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L208) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L210](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L210) |
| `visited` | boolean | [L303](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L303) |
| `statsClockTime` | public statsClockTime = 0; | [L316](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L316) |

### Assignment and formula index

- **id** [L216](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L216): `this.id = options.id`
- **timestamp** [L217](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L217): `this.timestamp = options.timestamp`
- **ssrc** [L218](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L218): `this.ssrc = options.ssrc`
- **kind** [L219](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L219): `this.kind = options.kind as MediaKind`
- **trackIdentifier** [L220](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L220): `this.trackIdentifier = options.trackIdentifier`
- **timestamp** [L230](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L230): `this.timestamp = stats.timestamp`
- **id** [L231](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L231): `this.id = stats.id`
- **ssrc** [L232](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L232): `this.ssrc = stats.ssrc`
- **kind** [L233](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L233): `this.kind = stats.kind as MediaKind`
- **trackIdentifier** [L234](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L234): `this.trackIdentifier = stats.trackIdentifier`
- **transportId** [L236](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L236): `this.transportId = stats.transportId`
- **codecId** [L237](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L237): `this.codecId = stats.codecId`
- **packetsReceived** [L238](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L238): `this.packetsReceived = stats.packetsReceived`
- **packetsReceivedWithEct1** [L239](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L239): `this.packetsReceivedWithEct1 = stats.packetsReceivedWithEct1`
- **packetsReceivedWithCe** [L240](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L240): `this.packetsReceivedWithCe = stats.packetsReceivedWithCe`
- **packetsReportedAsLost** [L241](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L241): `this.packetsReportedAsLost = stats.packetsReportedAsLost`
- **packetsReportedAsLostButRecovered** [L242](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L242): `this.packetsReportedAsLostButRecovered = stats.packetsReportedAsLostButRecovered`
- **packetsLost** [L243](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L243): `this.packetsLost = stats.packetsLost`
- **jitter** [L244](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L244): `this.jitter = stats.jitter`
- **mid** [L245](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L245): `this.mid = stats.mid`
- **remoteId** [L246](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L246): `this.remoteId = stats.remoteId`
- **framesDecoded** [L247](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L247): `this.framesDecoded = stats.framesDecoded`
- **keyFramesDecoded** [L248](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L248): `this.keyFramesDecoded = stats.keyFramesDecoded`
- **framesRendered** [L249](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L249): `this.framesRendered = stats.framesRendered`
- **framesDropped** [L250](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L250): `this.framesDropped = stats.framesDropped`
- **frameWidth** [L251](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L251): `this.frameWidth = stats.frameWidth`
- **frameHeight** [L252](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L252): `this.frameHeight = stats.frameHeight`
- **framesPerSecond** [L253](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L253): `this.framesPerSecond = stats.framesPerSecond`
- **qpSum** [L254](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L254): `this.qpSum = stats.qpSum`
- **totalDecodeTime** [L255](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L255): `this.totalDecodeTime = stats.totalDecodeTime`
- **totalInterFrameDelay** [L256](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L256): `this.totalInterFrameDelay = stats.totalInterFrameDelay`
- **totalSquaredInterFrameDelay** [L257](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L257): `this.totalSquaredInterFrameDelay = stats.totalSquaredInterFrameDelay`
- **pauseCount** [L258](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L258): `this.pauseCount = stats.pauseCount`
- **totalPausesDuration** [L259](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L259): `this.totalPausesDuration = stats.totalPausesDuration`
- **freezeCount** [L260](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L260): `this.freezeCount = stats.freezeCount`
- **totalFreezesDuration** [L261](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L261): `this.totalFreezesDuration = stats.totalFreezesDuration`
- **lastPacketReceivedTimestamp** [L262](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L262): `this.lastPacketReceivedTimestamp = stats.lastPacketReceivedTimestamp`
- **headerBytesReceived** [L263](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L263): `this.headerBytesReceived = stats.headerBytesReceived`
- **packetsDiscarded** [L264](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L264): `this.packetsDiscarded = stats.packetsDiscarded`
- **fecBytesReceived** [L265](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L265): `this.fecBytesReceived = stats.fecBytesReceived`
- **fecPacketsReceived** [L266](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L266): `this.fecPacketsReceived = stats.fecPacketsReceived`
- **fecPacketsDiscarded** [L267](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L267): `this.fecPacketsDiscarded = stats.fecPacketsDiscarded`
- **bytesReceived** [L268](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L268): `this.bytesReceived = stats.bytesReceived`
- **nackCount** [L269](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L269): `this.nackCount = stats.nackCount`
- **firCount** [L270](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L270): `this.firCount = stats.firCount`
- **pliCount** [L271](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L271): `this.pliCount = stats.pliCount`
- **totalProcessingDelay** [L272](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L272): `this.totalProcessingDelay = stats.totalProcessingDelay`
- **estimatedPlayoutTimestamp** [L273](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L273): `this.estimatedPlayoutTimestamp = stats.estimatedPlayoutTimestamp`
- **jitterBufferDelay** [L274](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L274): `this.jitterBufferDelay = stats.jitterBufferDelay`
- **jitterBufferTargetDelay** [L275](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L275): `this.jitterBufferTargetDelay = stats.jitterBufferTargetDelay`
- **jitterBufferEmittedCount** [L276](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L276): `this.jitterBufferEmittedCount = stats.jitterBufferEmittedCount`
- **jitterBufferMinimumDelay** [L277](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L277): `this.jitterBufferMinimumDelay = stats.jitterBufferMinimumDelay`
- **totalSamplesReceived** [L278](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L278): `this.totalSamplesReceived = stats.totalSamplesReceived`
- **concealedSamples** [L279](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L279): `this.concealedSamples = stats.concealedSamples`
- **silentConcealedSamples** [L280](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L280): `this.silentConcealedSamples = stats.silentConcealedSamples`
- **concealmentEvents** [L281](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L281): `this.concealmentEvents = stats.concealmentEvents`
- **insertedSamplesForDeceleration** [L282](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L282): `this.insertedSamplesForDeceleration = stats.insertedSamplesForDeceleration`
- **removedSamplesForAcceleration** [L283](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L283): `this.removedSamplesForAcceleration = stats.removedSamplesForAcceleration`
- **audioLevel** [L284](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L284): `this.audioLevel = stats.audioLevel`
- **totalAudioEnergy** [L285](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L285): `this.totalAudioEnergy = stats.totalAudioEnergy`
- **totalSamplesDuration** [L286](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L286): `this.totalSamplesDuration = stats.totalSamplesDuration`
- **framesReceived** [L287](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L287): `this.framesReceived = stats.framesReceived`
- **decoderImplementation** [L288](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L288): `this.decoderImplementation = stats.decoderImplementation`
- **playoutId** [L289](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L289): `this.playoutId = stats.playoutId`
- **powerEfficientDecoder** [L290](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L290): `this.powerEfficientDecoder = stats.powerEfficientDecoder`
- **framesAssembledFromMultiplePackets** [L291](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L291): `this.framesAssembledFromMultiplePackets = stats.framesAssembledFromMultiplePackets`
- **totalAssemblyTime** [L292](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L292): `this.totalAssemblyTime = stats.totalAssemblyTime`
- **retransmittedPacketsReceived** [L293](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L293): `this.retransmittedPacketsReceived = stats.retransmittedPacketsReceived`
- **retransmittedBytesReceived** [L294](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L294): `this.retransmittedBytesReceived = stats.retransmittedBytesReceived`
- **rtxSsrc** [L295](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L295): `this.rtxSsrc = stats.rtxSsrc`
- **fecSsrc** [L296](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L296): `this.fecSsrc = stats.fecSsrc`
- **totalCorruptionProbability** [L297](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L297): `this.totalCorruptionProbability = stats.totalCorruptionProbability`
- **totalSquaredCorruptionProbability** [L298](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L298): `this.totalSquaredCorruptionProbability = stats.totalSquaredCorruptionProbability`
- **corruptionMeasurements** [L299](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L299): `this.corruptionMeasurements = stats.corruptionMeasurements`
- **attachments** [L300](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L300): `this.attachments = stats.attachments`
- **deltaTotalSamplesReceived** [L337](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L337): `this.deltaTotalSamplesReceived = positiveDelta(stats.totalSamplesReceived, this.totalSamplesReceived)`
- **receivingAudioSamples** [L339](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L339): `this.receivingAudioSamples = this.deltaTotalSamplesReceived`
- **deltaBytesReceived** [L342](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L342): `this.deltaBytesReceived = positiveDelta(stats.bytesReceived, this.bytesReceived)`
- **bitrate** [L344](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L344): `this.bitrate = this.deltaBytesReceived === undefined ? undefined : Math.max(0, this.deltaBytesReceived * 8 / elapsedInSec)`
- **deltaPacketsLost** [L349](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L349): `this.deltaPacketsLost = positiveDelta(stats.packetsLost, this.packetsLost)`
- **deltaPacketsReceived** [L352](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L352): `this.deltaPacketsReceived = positiveDelta(stats.packetsReceived, this.packetsReceived)`
- **packetRate** [L353](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L353): `this.packetRate = this.deltaPacketsReceived === undefined ? undefined : this.deltaPacketsReceived / elapsedInSec`
- **deltaConcealedSamples** [L359](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L359): `this.deltaConcealedSamples = positiveDelta(stats.concealedSamples, this.concealedSamples)`
- **deltaSilentConcealedSamples** [L360](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L360): `this.deltaSilentConcealedSamples = positiveDelta(stats.silentConcealedSamples, this.silentConcealedSamples)`
- **deltaConcealmentEvents** [L361](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L361): `this.deltaConcealmentEvents = positiveDelta(stats.concealmentEvents, this.concealmentEvents)`
- **deltaInsertedSamplesForDeceleration** [L362](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L362): `this.deltaInsertedSamplesForDeceleration = positiveDelta(stats.insertedSamplesForDeceleration, this.insertedSamplesForDeceleration)`
- **deltaRemovedSamplesForAcceleration** [L363](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L363): `this.deltaRemovedSamplesForAcceleration = positiveDelta(stats.removedSamplesForAcceleration, this.removedSamplesForAcceleration)`
- **deltaPacketsDiscarded** [L364](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L364): `this.deltaPacketsDiscarded = positiveDelta(stats.packetsDiscarded, this.packetsDiscarded)`
- **deltaJitterBufferEmittedCount** [L365](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L365): `this.deltaJitterBufferEmittedCount = positiveDelta(stats.jitterBufferEmittedCount, this.jitterBufferEmittedCount)`
- **inventedSpeechRatio** [L371](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L371): `this.inventedSpeechRatio = invented / (this.deltaTotalSamplesReceived as number)`
- **inventedSpeechRatio** [L373](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L373): `this.inventedSpeechRatio = undefined`
- **concealmentEventRate** [L375](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L375): `this.concealmentEventRate = this.deltaConcealmentEvents !== undefined ? this.deltaConcealmentEvents / elapsedInSec : undefined`
- **timeStretchRate** [L381](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L381): `this.timeStretchRate = stretched / (this.deltaTotalSamplesReceived as number)`
- **timeStretchRate** [L383](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L383): `this.timeStretchRate = undefined`
- **discardRate** [L389](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L389): `this.discardRate = 0 < consumed ? this.deltaPacketsDiscarded / consumed : 0`
- **deltaCorruptionProbability** [L398](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L398): `this.deltaCorruptionProbability = Math.max( 0, deltaCorruption / deltaMeasurements )`
- **deltaJitterBufferDelay** [L404](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L404): `this.deltaJitterBufferDelay = positiveDelta(stats.jitterBufferDelay, this.jitterBufferDelay)`
- **deltaFramesDecoded** [L405](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L405): `this.deltaFramesDecoded = positiveDelta(stats.framesDecoded, this.framesDecoded)`
- **deltaFramesReceived** [L406](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L406): `this.deltaFramesReceived = positiveDelta(stats.framesReceived, this.framesReceived)`
- **deltaFramesRendered** [L407](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L407): `this.deltaFramesRendered = positiveDelta(stats.framesRendered, this.framesRendered)`
- **deltaFramesDropped** [L408](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L408): `this.deltaFramesDropped = positiveDelta(stats.framesDropped, this.framesDropped)`
- **deltaKeyFramesDecoded** [L409](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L409): `this.deltaKeyFramesDecoded = positiveDelta(stats.keyFramesDecoded, this.keyFramesDecoded)`
- **deltaQpSum** [L410](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L410): `this.deltaQpSum = positiveDelta(stats.qpSum, this.qpSum)`
- **avgQpPerFrame** [L413](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L413): `this.avgQpPerFrame = this.deltaQpSum / this.deltaFramesDecoded`
- **avgQpPerFrame** [L415](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L415): `this.avgQpPerFrame = undefined`
- **normalizedQp** [L418](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L418): `this.normalizedQp = this._deriveNormalizedQp()`
- **deltaTotalDecodeTime** [L419](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L419): `this.deltaTotalDecodeTime = positiveDelta(stats.totalDecodeTime, this.totalDecodeTime)`
- **deltaTotalFreezesDuration** [L420](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L420): `this.deltaTotalFreezesDuration = positiveDelta(stats.totalFreezesDuration, this.totalFreezesDuration)`
- **deltaFreezeCount** [L421](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L421): `this.deltaFreezeCount = positiveDelta(stats.freezeCount, this.freezeCount)`
- **frozenTimeRatio** [L422](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L422): `this.frozenTimeRatio = this.deltaTotalFreezesDuration !== undefined && 0 < elapsedInSec ? this.deltaTotalFreezesDuration / elapsedInSec : undefined`
- **deltaPauseCount** [L425](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L425): `this.deltaPauseCount = positiveDelta(stats.pauseCount, this.pauseCount)`
- **deltaTotalPausesDuration** [L426](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L426): `this.deltaTotalPausesDuration = positiveDelta(stats.totalPausesDuration, this.totalPausesDuration)`
- **pausedTimeRatio** [L427](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L427): `this.pausedTimeRatio = this.deltaTotalPausesDuration !== undefined && 0 < elapsedInSec ? this.deltaTotalPausesDuration / elapsedInSec : undefined`
- **deltaTotalInterFrameDelay** [L430](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L430): `this.deltaTotalInterFrameDelay = positiveDelta(stats.totalInterFrameDelay, this.totalInterFrameDelay)`
- **deltaTotalSquaredInterFrameDelay** [L431](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L431): `this.deltaTotalSquaredInterFrameDelay = positiveDelta(stats.totalSquaredInterFrameDelay, this.totalSquaredInterFrameDelay)`
- **avgInterFrameDelayInMs** [L446](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L446): `this.avgInterFrameDelayInMs = mean * 1000`
- **interFrameDelayVariation** [L447](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L447): `this.interFrameDelayVariation = 0 < mean ? Math.sqrt(variance) / mean : undefined`
- **avgInterFrameDelayInMs** [L449](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L449): `this.avgInterFrameDelayInMs = undefined`
- **interFrameDelayVariation** [L450](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L450): `this.interFrameDelayVariation = undefined`
- **deltaPliCount** [L452](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L452): `this.deltaPliCount = positiveDelta(stats.pliCount, this.pliCount)`
- **deltaFirCount** [L453](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L453): `this.deltaFirCount = positiveDelta(stats.firCount, this.firCount)`
- **deltaNackCount** [L454](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L454): `this.deltaNackCount = positiveDelta(stats.nackCount, this.nackCount)`
- **deltaRetransmittedBytesReceived** [L455](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L455): `this.deltaRetransmittedBytesReceived = positiveDelta(stats.retransmittedBytesReceived, this.retransmittedBytesReceived)`
- **deltaRetransmittedPacketsReceived** [L456](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L456): `this.deltaRetransmittedPacketsReceived = positiveDelta(stats.retransmittedPacketsReceived, this.retransmittedPacketsReceived)`
- **retransmissionRatio** [L458](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L458): `this.retransmissionRatio = this.deltaRetransmittedBytesReceived !== undefined && 0 < (this.deltaBytesReceived ?? 0) ? Math.min(1, this.deltaRetransmittedBytesReceived / (this.deltaBytesReceived as number)) : undefined`
- **avgJitterBufferDelayInMs** [L462](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L462): `this.avgJitterBufferDelayInMs = 0 < (this.deltaJitterBufferEmittedCount ?? 0) && this.deltaJitterBufferDelay !== undefined ? (this.deltaJitterBufferDelay / (this.deltaJitterBufferEmittedCount as number)) * 1000 : undefined`
- **deltaJitterBufferTargetDelay** [L465](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L465): `this.deltaJitterBufferTargetDelay = positiveDelta(stats.jitterBufferTargetDelay, this.jitterBufferTargetDelay)`
- **jitterBufferTargetDelayInMs** [L466](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L466): `this.jitterBufferTargetDelayInMs = 0 < (this.deltaJitterBufferEmittedCount ?? 0) && this.deltaJitterBufferTargetDelay !== undefined ? (this.deltaJitterBufferTargetDelay / (this.deltaJitterBufferEmittedCount as number)) * 1000 : undefined`
- **decodeTimePerFrameInMs** [L471](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L471): `this.decodeTimePerFrameInMs = 0 < (this.deltaFramesDecoded ?? 0) && this.deltaTotalDecodeTime !== undefined ? (this.deltaTotalDecodeTime / (this.deltaFramesDecoded as number)) * 1000 : undefined`
- **droppedFrameRatio** [L473](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L473): `this.droppedFrameRatio = 0 < (this.deltaFramesReceived ?? 0) && this.deltaFramesDropped !== undefined ? this.deltaFramesDropped / (this.deltaFramesReceived as number) : undefined`
- **renderRatio** [L475](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L475): `this.renderRatio = 0 < (this.deltaFramesDecoded ?? 0) && this.deltaFramesRendered !== undefined ? this.deltaFramesRendered / (this.deltaFramesDecoded as number) : undefined`
- **keyFrameRate** [L477](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L477): `this.keyFrameRate = this.deltaKeyFramesDecoded !== undefined ? this.deltaKeyFramesDecoded / elapsedInSec : undefined`
- **pliRate** [L478](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L478): `this.pliRate = this.deltaPliCount !== undefined ? this.deltaPliCount / elapsedInSec : undefined`
- **firRate** [L479](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L479): `this.firRate = this.deltaFirCount !== undefined ? this.deltaFirCount / elapsedInSec : undefined`
- **nackRate** [L480](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L480): `this.nackRate = this.deltaNackCount !== undefined ? this.deltaNackCount / elapsedInSec : undefined`
- **deltaTime** [L481](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L481): `this.deltaTime = elapsedInMs`
- **statsClockTime** [L482](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L482): `this.statsClockTime += elapsedInMs`
- **avgFramesPerSec** [L496](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L496): `this.avgFramesPerSec = avgFramesPerSec`
- **fpsVolatility** [L497](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L497): `this.fpsVolatility = avgDiff / avgFramesPerSec`
- **bitPerPixel** [L500](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L500): `this.bitPerPixel = this.bitrate / (this.frameWidth * this.frameHeight * this.framesPerSecond)`
- **totalFractionLost** [L505](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L505): `this.totalFractionLost = 0 < this.packetsReceived && 0 < this.packetsLost ? (this.packetsLost) / (this.packetsLost + this.packetsReceived) : 0.0`
- **deltaFractionLost** [L509](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L509): `this.deltaFractionLost = 0 < this.deltaPacketsReceived && 0 < this.deltaPacketsLost ? (this.deltaPacketsLost) / (this.deltaPacketsLost + this.deltaPacketsReceived) : 0.0`
- **ewmaFps** [L513](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts#L513): `this.ewmaFps = this.ewmaFps ? 0.9 * this.ewmaFps + 0.1 * this.framesPerSecond : this.framesPerSecond`

### Exact wire projection
```ts
public createSample(): InboundRtpStats {
		return {
			timestamp: this.timestamp,
			id: this.id,
			ssrc: this.ssrc,
			kind: this.kind,
			trackIdentifier: this.trackIdentifier,
			transportId: this.transportId,
			codecId: this.codecId,
			packetsReceived: this.packetsReceived,
			packetsReceivedWithEct1: this.packetsReceivedWithEct1,
			packetsReceivedWithCe: this.packetsReceivedWithCe,
			packetsReportedAsLost: this.packetsReportedAsLost,
			packetsReportedAsLostButRecovered: this.packetsReportedAsLostButRecovered,
			packetsLost: this.packetsLost,
			jitter: this.jitter,
			mid: this.mid,
			remoteId: this.remoteId,
			framesDecoded: this.framesDecoded,
			keyFramesDecoded: this.keyFramesDecoded,
			framesRendered: this.framesRendered,
			framesDropped: this.framesDropped,
			frameWidth: this.frameWidth,
			frameHeight: this.frameHeight,
			framesPerSecond: this.framesPerSecond,
			qpSum: this.qpSum,
			totalDecodeTime: this.totalDecodeTime,
			totalInterFrameDelay: this.totalInterFrameDelay,
			totalSquaredInterFrameDelay: this.totalSquaredInterFrameDelay,
			pauseCount: this.pauseCount,
			totalPausesDuration: this.totalPausesDuration,
			freezeCount: this.freezeCount,
			totalFreezesDuration: this.totalFreezesDuration,
			lastPacketReceivedTimestamp: this.lastPacketReceivedTimestamp,
			headerBytesReceived: this.headerBytesReceived,
			packetsDiscarded: this.packetsDiscarded,
			fecBytesReceived: this.fecBytesReceived,
			fecPacketsReceived: this.fecPacketsReceived,
			fecPacketsDiscarded: this.fecPacketsDiscarded,
			bytesReceived: this.bytesReceived,
			nackCount: this.nackCount,
			firCount: this.firCount,
			pliCount: this.pliCount,
			totalProcessingDelay: this.totalProcessingDelay,
			estimatedPlayoutTimestamp: this.estimatedPlayoutTimestamp,
			jitterBufferDelay: this.jitterBufferDelay,
			jitterBufferTargetDelay: this.jitterBufferTargetDelay,
			jitterBufferEmittedCount: this.jitterBufferEmittedCount,
			jitterBufferMinimumDelay: this.jitterBufferMinimumDelay,
			totalSamplesReceived: this.totalSamplesReceived,
			concealedSamples: this.concealedSamples,
			silentConcealedSamples: this.silentConcealedSamples,
			concealmentEvents: this.concealmentEvents,
			insertedSamplesForDeceleration: this.insertedSamplesForDeceleration,
			removedSamplesForAcceleration: this.removedSamplesForAcceleration,
			audioLevel: this.audioLevel,
			totalAudioEnergy: this.totalAudioEnergy,
			totalSamplesDuration: this.totalSamplesDuration,
			framesReceived: this.framesReceived,
			decoderImplementation: this.decoderImplementation,
			playoutId: this.playoutId,
			powerEfficientDecoder: this.powerEfficientDecoder,
			framesAssembledFromMultiplePackets: this.framesAssembledFromMultiplePackets,
			totalAssemblyTime: this.totalAssemblyTime,
			retransmittedPacketsReceived: this.retransmittedPacketsReceived,
			retransmittedBytesReceived: this.retransmittedBytesReceived,
			rtxSsrc: this.rtxSsrc,
			fecSsrc: this.fecSsrc,
			totalCorruptionProbability: this.totalCorruptionProbability,
			totalSquaredCorruptionProbability: this.totalSquaredCorruptionProbability,
			corruptionMeasurements: this.corruptionMeasurements,
			attachments: this.attachments,
		}
	}
```

## InboundTrackMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L181)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `CLEAN_QP_RATIO` | public static CLEAN_QP_RATIO = 0.5; | [L189](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L189) |
| `COARSE_QP_RATIO` | public static COARSE_QP_RATIO = 0.8; | [L190](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L190) |
| `direction` | public readonly direction = 'inbound'; | [L192](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L192) |
| `detectors` | Detectors | [L193](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L193) |
| `issues` | IssueRegistry&lt;InboundTrackIssues&gt; | [L199](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L199) |
| `slicedWindow` | SlicedWindow&lt;
		InboundTrackWindowValues,
		// A slice for every stretch the config sizes, so the names are declared once. Only the
		// names matter here: how many samples each covers, and where it sits, are runtime.
		Record&lt;keyof InboundTrackWindowConfig['numberOfSamples'], SliceConfig&gt;
	&gt; | [L210](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L210) |
| `dtxMode` | public dtxMode = false; | [L218](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L218) |
| `paused` | boolean | [L229](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L229) |
| `remoteOutboundTrackPaused` | boolean | [L237](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L237) |
| `contentType` | TrackContentType  /  undefined | [L244](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L244) |
| `linkedVideoTrackId` | string  /  undefined | [L247](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L247) |
| `motionType` | VideoMotionType  /  undefined | [L250](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L250) |
| `presentedResolution` | { width: number, height: number }  /  undefined | [L253](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L253) |
| `videoTag` | HTMLVideoElement  /  undefined | [L256](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L256) |
| `linkedVideoPlayoutDiffInMs` | number | [L266](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L266) |
| `displayMagnification` | number | [L272](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L272) |
| `frameFlowState` | InboundVideoFlowState | [L283](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L283) |
| `degradedFrameSupply` | boolean | [L300](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L300) |
| `decodingDegradation` | number | [L308](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L308) |
| `quantizationDegradation` | number | [L345](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L345) |
| `synthesizedAudioRatio` | number | [L348](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L348) |
| `jitterBufferStressSeverity` | number | [L351](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L351) |
| `videoPlayoutSkew` | number | [L367](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L367) |
| `decodeBudgetUtilization` | number | [L370](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L370) |
| `inventedSpeechSeverity` | number | [L373](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L373) |
| `overloadedDecoder` | boolean | [L376](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L376) |
| `dry` | boolean | [L379](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L379) |
| `stalledFrameAssembly` | boolean | [L382](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L382) |
| `playoutDiscrepancy` | boolean | [L385](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L385) |
| `stuckedDecoder` | boolean | [L388](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L388) |
| `failedVideoRecovery` | boolean | [L391](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L391) |
| `calculatedScore` | CalculatedScore | [L393](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L393) |
| `score` | public get score() { | [L398](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L398) |
| `scoreReasons` | public get scoreReasons() { | [L402](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L402) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L407](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L407) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L409](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L409) |
| `isScreenShare` | public get isScreenShare() { | [L531](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L531) |
| `readyState` | MediaStreamTrack['readyState'] | [L560](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L560) |
| `kind` | public get kind() { | [L568](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L568) |
| `bitrate` | public get bitrate() { | [L572](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L572) |
| `jitter` | public get jitter() { | [L576](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L576) |
| `fractionLost` | public get fractionLost() { | [L580](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L580) |

### Assignment and formula index

- **attachments** [L416](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L416): `this.attachments = attachments`
- **issues** [L420](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L420): `this.issues = new IssueRegistry<InboundTrackIssues>( this.getPeerConnection().parent.activeIssues.asSink, )`
- **slicedWindow** [L427](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L427): `this.slicedWindow = new SlicedWindow({ maxAllowedGapInMs: windowConfig.maxAllowedGapInMs, totals: INBOUND_TRACK_WINDOW_VALUES, // Each recovery slice sits at its own detection slice's size, so it covers the stretch // that ends where that detection stretch begins. The two pairs are independent: a // detector reads one pair or the other, never one half of each. slices: { detection: { numberOfSamples: windowConfig.numberOfSamples.detection, }, recovery: { numberOfSamples: windowConfig.numberOfSamples.recovery, offset: windowConfig.numberOfSamples.detection, }, flowDetection: { numberOfSamples: windowConfig.numberOfSamples.flowDetection, }, flowRecovery: { numberOfSamples: windowConfig.numberOfSamples.flowRecovery, offset: windowConfig.numberOfSamples.flowDetection, }, }, })`
- **detectors** [L450](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L450): `this.detectors = new Detectors()`
- **quantizationDegradation** [L613](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L613): `this.quantizationDegradation = normalizedQp === undefined || coarse <= clean ? undefined : clamp((normalizedQp - clean) / (coarse - clean), 0, 1)`
- **displayMagnification** [L656](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L656): `this.displayMagnification = presented && 0 < presented.width && 0 < presented.height && decodedWidth && decodedHeight ? Math.sqrt((presented.width * presented.height) / (decodedWidth * decodedHeight)) : undefined`
- **linkedVideoPlayoutDiffInMs** [L665](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L665): `this.linkedVideoPlayoutDiffInMs = undefined`
- **linkedVideoPlayoutDiffInMs** [L675](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts#L675): `this.linkedVideoPlayoutDiffInMs = audioPlayout - videoPlayout`

### Exact wire projection
```ts
public createSample(): InboundTrackSample {
			return {
				id: this.track.id,
				kind: this.track.kind,
				timestamp: Date.now(),
				attachments: this.attachments,
				score: this.score,
				scoreReasons: sampledScoreReasons(
					this.calculatedScore.reasons,
					this.getPeerConnection()?.parent.config.sendScoreReasonsToServer,
				),
			};
		}
```

## MediaPlayoutMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L7)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `detectors` | public readonly detectors = new Detectors(); | [L14](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L14) |
| `timestamp` | number | [L16](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L16) |
| `id` | string | [L17](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L17) |
| `kind` | MediaKind | [L18](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L18) |
| `synthesizedSamplesDuration` | number  /  undefined | [L19](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L19) |
| `synthesizedSamplesEvents` | number  /  undefined | [L20](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L20) |
| `totalSamplesDuration` | number  /  undefined | [L21](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L21) |
| `totalPlayoutDelay` | number  /  undefined | [L22](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L22) |
| `totalSamplesCount` | number  /  undefined | [L23](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L23) |
| `deltaSynthesizedSamplesDuration` | public deltaSynthesizedSamplesDuration = 0; | [L25](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L25) |
| `deltaSamplesDuration` | public deltaSamplesDuration = 0; | [L26](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L26) |
| `deltaSynthesizedSamplesEvents` | number  /  undefined | [L27](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L27) |
| `deltaTotalPlayoutDelay` | number  /  undefined | [L28](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L28) |
| `deltaSamplesCount` | number  /  undefined | [L29](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L29) |
| `deltaTime` | number  /  undefined | [L32](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L32) |
| `playoutDelayPerSampleInMs` | number  /  undefined | [L36](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L36) |
| `synthesizedSamplesRatio` | number  /  undefined | [L39](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L39) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L41](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L41) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L43](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L43) |
| `visited` | boolean | [L57](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L57) |
| `statsClockTime` | public statsClockTime = 0; | [L66](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L66) |

### Assignment and formula index

- **id** [L49](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L49): `this.id = options.id`
- **timestamp** [L50](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L50): `this.timestamp = options.timestamp`
- **kind** [L51](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L51): `this.kind = options.kind as MediaKind`
- **deltaTime** [L79](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L79): `this.deltaTime = elapsedInMs`
- **statsClockTime** [L80](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L80): `this.statsClockTime += elapsedInMs`
- **deltaSynthesizedSamplesDuration** [L81](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L81): `this.deltaSynthesizedSamplesDuration = positiveDelta(stats.synthesizedSamplesDuration, this.synthesizedSamplesDuration) ?? 0`
- **deltaSamplesDuration** [L82](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L82): `this.deltaSamplesDuration = positiveDelta(stats.totalSamplesDuration, this.totalSamplesDuration) ?? 0`
- **deltaSynthesizedSamplesEvents** [L83](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L83): `this.deltaSynthesizedSamplesEvents = positiveDelta(stats.synthesizedSamplesEvents, this.synthesizedSamplesEvents)`
- **deltaTotalPlayoutDelay** [L84](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L84): `this.deltaTotalPlayoutDelay = positiveDelta(stats.totalPlayoutDelay, this.totalPlayoutDelay)`
- **deltaSamplesCount** [L85](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L85): `this.deltaSamplesCount = positiveDelta(stats.totalSamplesCount, this.totalSamplesCount)`
- **playoutDelayPerSampleInMs** [L89](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L89): `this.playoutDelayPerSampleInMs = (this.deltaTotalPlayoutDelay * 1000) / this.deltaSamplesCount`
- **playoutDelayPerSampleInMs** [L91](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L91): `this.playoutDelayPerSampleInMs = undefined`
- **synthesizedSamplesRatio** [L94](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaPlayoutMonitor.ts#L94): `this.synthesizedSamplesRatio = this.deltaSamplesDuration > 0 ? Math.min(1, this.deltaSynthesizedSamplesDuration / this.deltaSamplesDuration) : 0`

### Exact wire projection
```ts
public createSample(): MediaPlayoutStats {
		return {
			id: this.id,
			timestamp: this.timestamp,
			kind: this.kind,
			synthesizedSamplesDuration: this.synthesizedSamplesDuration,
			synthesizedSamplesEvents: this.synthesizedSamplesEvents,
			totalSamplesDuration: this.totalSamplesDuration,
			totalPlayoutDelay: this.totalPlayoutDelay,
			totalSamplesCount: this.totalSamplesCount,
			attachments: this.attachments,
		};
	}
```

## MediaSourceMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L6)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `timestamp` | number | [L9](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L9) |
| `id` | string | [L10](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L10) |
| `kind` | MediaKind | [L11](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L11) |
| `audioLevel` | number  /  undefined | [L12](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L12) |
| `trackIdentifier` | string | [L13](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L13) |
| `totalAudioEnergy` | number  /  undefined | [L14](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L14) |
| `totalSamplesDuration` | number  /  undefined | [L15](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L15) |
| `echoReturnLoss` | number  /  undefined | [L16](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L16) |
| `echoReturnLossEnhancement` | number  /  undefined | [L17](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L17) |
| `width` | number  /  undefined | [L18](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L18) |
| `height` | number  /  undefined | [L19](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L19) |
| `frames` | number  /  undefined | [L20](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L20) |
| `framesPerSecond` | number  /  undefined | [L21](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L21) |
| `deltaFrames` | number  /  undefined | [L24](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L24) |
| `deltaTotalAudioEnergy` | number  /  undefined | [L25](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L25) |
| `deltaSamplesDuration` | number  /  undefined | [L26](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L26) |
| `deltaTime` | number  /  undefined | [L29](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L29) |
| `producedFps` | number  /  undefined | [L33](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L33) |
| `rmsAudioLevel` | number  /  undefined | [L39](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L39) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L42](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L42) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L44](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L44) |
| `visited` | boolean | [L58](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L58) |
| `statsClockTime` | public statsClockTime = 0; | [L67](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L67) |

### Assignment and formula index

- **id** [L50](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L50): `this.id = options.id`
- **timestamp** [L51](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L51): `this.timestamp = options.timestamp`
- **kind** [L52](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L52): `this.kind = options.kind as MediaKind`
- **deltaTime** [L89](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L89): `this.deltaTime = elapsedInMs`
- **statsClockTime** [L90](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L90): `this.statsClockTime += elapsedInMs`
- **deltaFrames** [L93](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L93): `this.deltaFrames = positiveDelta(stats.frames, this.frames)`
- **deltaTotalAudioEnergy** [L94](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L94): `this.deltaTotalAudioEnergy = positiveDelta(stats.totalAudioEnergy, this.totalAudioEnergy)`
- **deltaSamplesDuration** [L95](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L95): `this.deltaSamplesDuration = positiveDelta(stats.totalSamplesDuration, this.totalSamplesDuration)`
- **producedFps** [L103](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L103): `this.producedFps = framesDelta !== undefined && 0 <= framesDelta ? framesDelta / elapsedInSec : undefined`
- **rmsAudioLevel** [L107](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/MediaSourceMonitor.ts#L107): `this.rmsAudioLevel = this.deltaTotalAudioEnergy !== undefined && this.deltaSamplesDuration !== undefined && this.deltaSamplesDuration > 0 ? Math.sqrt(this.deltaTotalAudioEnergy / this.deltaSamplesDuration) : undefined`

### Exact wire projection
```ts
public createSample(): MediaSourceStats {
		return {
			id: this.id,
			timestamp: this.timestamp,
			kind: this.kind,
			audioLevel: this.audioLevel,
			trackIdentifier: this.trackIdentifier,
			totalAudioEnergy: this.totalAudioEnergy,
			totalSamplesDuration: this.totalSamplesDuration,
			echoReturnLoss: this.echoReturnLoss,
			echoReturnLossEnhancement: this.echoReturnLossEnhancement,
			width: this.width,
			height: this.height,
			frames: this.frames,
			framesPerSecond: this.framesPerSecond,
			attachments: this.attachments,
		};
	}
```

## OutboundRtpMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L6)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `timestamp` | number | [L9](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L9) |
| `id` | string | [L10](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L10) |
| `ssrc` | number | [L11](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L11) |
| `kind` | MediaKind | [L12](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L12) |
| `qualityLimitationDurations` | QualityLimitationDurations | [L13](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L13) |
| `transportId` | string  /  undefined | [L14](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L14) |
| `codecId` | string  /  undefined | [L15](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L15) |
| `packetsSent` | number  /  undefined | [L16](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L16) |
| `bytesSent` | number  /  undefined | [L17](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L17) |
| `mid` | string  /  undefined | [L18](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L18) |
| `mediaSourceId` | string  /  undefined | [L19](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L19) |
| `remoteId` | string  /  undefined | [L20](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L20) |
| `rid` | string  /  undefined | [L21](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L21) |
| `encodingIndex` | number  /  undefined | [L22](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L22) |
| `headerBytesSent` | number  /  undefined | [L23](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L23) |
| `retransmittedPacketsSent` | number  /  undefined | [L24](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L24) |
| `retransmittedBytesSent` | number  /  undefined | [L25](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L25) |
| `rtxSsrc` | number  /  undefined | [L26](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L26) |
| `targetBitrate` | number  /  undefined | [L27](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L27) |
| `totalEncodedBytesTarget` | number  /  undefined | [L28](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L28) |
| `frameWidth` | number  /  undefined | [L29](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L29) |
| `frameHeight` | number  /  undefined | [L30](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L30) |
| `framesPerSecond` | number  /  undefined | [L31](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L31) |
| `framesSent` | number  /  undefined | [L32](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L32) |
| `hugeFramesSent` | number  /  undefined | [L33](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L33) |
| `framesEncoded` | number  /  undefined | [L34](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L34) |
| `keyFramesEncoded` | number  /  undefined | [L35](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L35) |
| `qpSum` | number  /  undefined | [L36](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L36) |
| `psnrSum` | PsnrSum  /  undefined | [L37](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L37) |
| `psnrMeasurements` | number  /  undefined | [L38](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L38) |
| `totalEncodeTime` | number  /  undefined | [L39](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L39) |
| `totalPacketSendDelay` | number  /  undefined | [L40](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L40) |
| `qualityLimitationReason` | string  /  undefined | [L41](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L41) |
| `qualityLimitationResolutionChanges` | number  /  undefined | [L42](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L42) |
| `nackCount` | number  /  undefined | [L43](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L43) |
| `firCount` | number  /  undefined | [L44](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L44) |
| `pliCount` | number  /  undefined | [L45](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L45) |
| `encoderImplementation` | string  /  undefined | [L46](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L46) |
| `powerEfficientEncoder` | boolean  /  undefined | [L47](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L47) |
| `active` | boolean  /  undefined | [L48](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L48) |
| `scalabilityMode` | string  /  undefined | [L49](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L49) |
| `packetsSentWithEct1` | number  /  undefined | [L50](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L50) |
| `bitrate` | number  /  undefined | [L53](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L53) |
| `payloadBitrate` | number  /  undefined | [L54](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L54) |
| `packetRate` | number  /  undefined | [L55](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L55) |
| `bitPerPixel` | number  /  undefined | [L56](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L56) |
| `deltaPacketsSent` | number  /  undefined | [L58](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L58) |
| `deltaBytesSent` | number  /  undefined | [L59](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L59) |
| `deltaHeaderBytesSent` | number  /  undefined | [L60](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L60) |
| `deltaRetransmittedPacketsSent` | number  /  undefined | [L61](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L61) |
| `deltaRetransmittedBytesSent` | number  /  undefined | [L62](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L62) |
| `deltaFramesSent` | number  /  undefined | [L63](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L63) |
| `deltaFramesEncoded` | number  /  undefined | [L64](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L64) |
| `deltaKeyFramesEncoded` | number  /  undefined | [L65](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L65) |
| `deltaHugeFramesSent` | number  /  undefined | [L66](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L66) |
| `deltaEncodeTime` | number  /  undefined | [L67](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L67) |
| `deltaPacketSendDelay` | number  /  undefined | [L68](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L68) |
| `deltaQpSum` | number  /  undefined | [L69](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L69) |
| `deltaNackCount` | number  /  undefined | [L70](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L70) |
| `deltaFirCount` | number  /  undefined | [L71](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L71) |
| `deltaPliCount` | number  /  undefined | [L72](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L72) |
| `deltaTime` | number  /  undefined | [L75](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L75) |
| `avgEncodeTimePerFrameInMs` | number  /  undefined | [L78](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L78) |
| `retransmissionRatio` | number  /  undefined | [L81](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L81) |
| `retransmittedPacketRatio` | number  /  undefined | [L84](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L84) |
| `avgQpPerFrame` | number  /  undefined | [L87](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L87) |
| `avgPacketSendDelayInMs` | number  /  undefined | [L90](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L90) |
| `keyFrameRate` | number  /  undefined | [L93](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L93) |
| `nackRate` | number  /  undefined | [L96](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L96) |
| `pliRate` | number  /  undefined | [L97](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L97) |
| `firRate` | number  /  undefined | [L98](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L98) |
| `qualityLimitationDurationShares` | {
		none: number;
		cpu: number;
		bandwidth: number;
		other: number;
	}  /  undefined | [L101](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L101) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L109](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L109) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L111](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L111) |
| `visited` | boolean | [L125](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L125) |
| `trackIdentifier` | public get trackIdentifier() { | [L133](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L133) |
| `statsClockTime` | public statsClockTime = 0; | [L142](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L142) |

### Assignment and formula index

- **id** [L117](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L117): `this.id = options.id`
- **timestamp** [L118](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L118): `this.timestamp = options.timestamp`
- **ssrc** [L119](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L119): `this.ssrc = options.ssrc`
- **kind** [L120](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L120): `this.kind = options.kind as MediaKind`
- **deltaTime** [L181](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L181): `this.deltaTime = elapsedInMs`
- **statsClockTime** [L182](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L182): `this.statsClockTime += elapsedInMs`
- **deltaPacketsSent** [L185](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L185): `this.deltaPacketsSent = positiveDelta(stats.packetsSent, this.packetsSent)`
- **packetRate** [L187](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L187): `this.packetRate = this.deltaPacketsSent / elapsedInSec`
- **deltaBytesSent** [L190](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L190): `this.deltaBytesSent = positiveDelta(stats.bytesSent, this.bytesSent)`
- **deltaHeaderBytesSent** [L191](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L191): `this.deltaHeaderBytesSent = positiveDelta(stats.headerBytesSent, this.headerBytesSent)`
- **deltaRetransmittedBytesSent** [L192](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L192): `this.deltaRetransmittedBytesSent = positiveDelta(stats.retransmittedBytesSent, this.retransmittedBytesSent)`
- **deltaRetransmittedPacketsSent** [L193](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L193): `this.deltaRetransmittedPacketsSent = positiveDelta(stats.retransmittedPacketsSent, this.retransmittedPacketsSent)`
- **bitrate** [L196](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L196): `this.bitrate = Math.max(0, this.deltaBytesSent * 8 / elapsedInSec)`
- **payloadBitrate** [L201](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L201): `this.payloadBitrate = Math.max(0, payloadBytesSent * 8 / elapsedInSec)`
- **retransmissionRatio** [L204](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L204): `this.retransmissionRatio = this.deltaBytesSent > 0 && this.deltaRetransmittedBytesSent !== undefined ? Math.min(1, this.deltaRetransmittedBytesSent / this.deltaBytesSent) : 0`
- **retransmittedPacketRatio** [L210](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L210): `this.retransmittedPacketRatio = this.deltaPacketsSent > 0 ? Math.min(1, this.deltaRetransmittedPacketsSent / this.deltaPacketsSent) : 0`
- **deltaFramesSent** [L215](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L215): `this.deltaFramesSent = positiveDelta(stats.framesSent, this.framesSent)`
- **deltaFramesEncoded** [L216](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L216): `this.deltaFramesEncoded = positiveDelta(stats.framesEncoded, this.framesEncoded)`
- **deltaKeyFramesEncoded** [L217](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L217): `this.deltaKeyFramesEncoded = positiveDelta(stats.keyFramesEncoded, this.keyFramesEncoded)`
- **deltaHugeFramesSent** [L218](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L218): `this.deltaHugeFramesSent = positiveDelta(stats.hugeFramesSent, this.hugeFramesSent)`
- **deltaEncodeTime** [L219](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L219): `this.deltaEncodeTime = positiveDelta(stats.totalEncodeTime, this.totalEncodeTime)`
- **deltaPacketSendDelay** [L220](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L220): `this.deltaPacketSendDelay = positiveDelta(stats.totalPacketSendDelay, this.totalPacketSendDelay)`
- **deltaQpSum** [L221](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L221): `this.deltaQpSum = positiveDelta(stats.qpSum, this.qpSum)`
- **deltaNackCount** [L222](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L222): `this.deltaNackCount = positiveDelta(stats.nackCount, this.nackCount)`
- **deltaFirCount** [L223](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L223): `this.deltaFirCount = positiveDelta(stats.firCount, this.firCount)`
- **deltaPliCount** [L224](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L224): `this.deltaPliCount = positiveDelta(stats.pliCount, this.pliCount)`
- **avgEncodeTimePerFrameInMs** [L229](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L229): `this.avgEncodeTimePerFrameInMs = (this.deltaEncodeTime * 1000) / this.deltaFramesEncoded`
- **avgQpPerFrame** [L232](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L232): `this.avgQpPerFrame = this.deltaQpSum / this.deltaFramesEncoded`
- **avgPacketSendDelayInMs** [L238](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L238): `this.avgPacketSendDelayInMs = (this.deltaPacketSendDelay * 1000) / this.deltaPacketsSent`
- **keyFrameRate** [L242](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L242): `this.keyFrameRate = this.deltaKeyFramesEncoded / elapsedInSec`
- **nackRate** [L245](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L245): `this.nackRate = this.deltaNackCount / elapsedInSec`
- **pliRate** [L248](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L248): `this.pliRate = this.deltaPliCount / elapsedInSec`
- **firRate** [L251](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L251): `this.firRate = this.deltaFirCount / elapsedInSec`
- **qualityLimitationDurationShares** [L254](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L254): `this.qualityLimitationDurationShares = this._calculateQualityLimitationShares( this.qualityLimitationDurations, stats.qualityLimitationDurations, )`
- **bitPerPixel** [L262](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts#L262): `this.bitPerPixel = this.bitrate / (this.frameHeight * this.frameWidth * this.framesPerSecond)`

### Exact wire projection
```ts
public createSample(): OutboundRtpStats {
		return {
			timestamp: this.timestamp,
			id: this.id,
			ssrc: this.ssrc,
			kind: this.kind,
			qualityLimitationDurations: this.qualityLimitationDurations,
			transportId: this.transportId,
			codecId: this.codecId,
			packetsSent: this.packetsSent,
			bytesSent: this.bytesSent,
			mid: this.mid,
			mediaSourceId: this.mediaSourceId,
			remoteId: this.remoteId,
			rid: this.rid,
			encodingIndex: this.encodingIndex,
			headerBytesSent: this.headerBytesSent,
			retransmittedPacketsSent: this.retransmittedPacketsSent,
			retransmittedBytesSent: this.retransmittedBytesSent,
			rtxSsrc: this.rtxSsrc,
			targetBitrate: this.targetBitrate,
			totalEncodedBytesTarget: this.totalEncodedBytesTarget,
			frameWidth: this.frameWidth,
			frameHeight: this.frameHeight,
			framesPerSecond: this.framesPerSecond,
			framesSent: this.framesSent,
			hugeFramesSent: this.hugeFramesSent,
			framesEncoded: this.framesEncoded,
			keyFramesEncoded: this.keyFramesEncoded,
			qpSum: this.qpSum,
			psnrSum: this.psnrSum,
			psnrMeasurements: this.psnrMeasurements,
			totalEncodeTime: this.totalEncodeTime,
			totalPacketSendDelay: this.totalPacketSendDelay,
			qualityLimitationReason: this.qualityLimitationReason,
			qualityLimitationResolutionChanges: this.qualityLimitationResolutionChanges,
			nackCount: this.nackCount,
			firCount: this.firCount,
			pliCount: this.pliCount,
			encoderImplementation: this.encoderImplementation,
			powerEfficientEncoder: this.powerEfficientEncoder,
			active: this.active,
			scalabilityMode: this.scalabilityMode,
			packetsSentWithEct1: this.packetsSentWithEct1,
			attachments: this.attachments,
		};
	}
```

## OutboundTrackMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L90)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `direction` | public readonly direction = 'outbound'; | [L91](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L91) |
| `detectors` | Detectors | [L92](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L92) |
| `issues` | IssueRegistry&lt;OutboundTrackIssues&gt; | [L93](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L93) |
| `slicedWindow` | SlicedWindow&lt;
		OutboundTrackWindowValues,
		// A slice for every stretch the config sizes, so the names are declared once. Only the
		// names matter here: how many samples each covers, and where it sits, are runtime.
		Record&lt;keyof OutboundTrackWindowConfig['numberOfSamples'], SliceConfig&gt;
	&gt; | [L102](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L102) |
| `bitrate` | number | [L119](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L119) |
| `jitter` | number | [L120](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L120) |
| `fractionLost` | number | [L121](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L121) |
| `sendingPacketRate` | number | [L122](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L122) |
| `remoteReceivedPacketRate` | number | [L123](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L123) |
| `sourceEnded` | public sourceEnded = false; | [L130](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L130) |
| `mappedOutboundRtps` | public readonly mappedOutboundRtps = new Map&lt;number, OutboundRtpMonitor&gt;(); | [L131](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L131) |
| `paused` | boolean | [L145](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L145) |
| `settings` | MediaTrackSettings | [L164](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L164) |
| `videoCaptureSettingsChanged` | boolean | [L167](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L167) |
| `degradedVideoCapture` | boolean | [L173](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L173) |
| `videoCaptureDegradation` | number | [L181](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L181) |
| `degradedEncodingPerformance` | boolean | [L184](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L184) |
| `videoEncodingDegradation` | number | [L187](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L187) |
| `dry` | boolean | [L190](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L190) |
| `silentAudioSource` | boolean | [L193](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L193) |
| `lostCaptureSource` | boolean | [L199](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L199) |
| `contentType` | TrackContentType  /  undefined | [L209](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L209) |
| `calculatedScore` | CalculatedScore | [L213](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L213) |
| `score` | public get score() { | [L218](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L218) |
| `scoreReasons` | public get scoreReasons() { | [L222](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L222) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L227](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L227) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L229](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L229) |
| `kind` | public get kind() { | [L316](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L316) |
| `isScreenShare` | public get isScreenShare() { | [L321](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L321) |
| `readyState` | MediaStreamTrack['readyState'] | [L325](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L325) |
| `highestLayer` | OutboundRtpMonitor | [L343](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L343) |

### Assignment and formula index

- **attachments** [L236](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L236): `this.attachments = attachments`
- **detectors** [L237](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L237): `this.detectors = new Detectors()`
- **issues** [L238](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L238): `this.issues = new IssueRegistry<OutboundTrackIssues>( this.getPeerConnection().parent.activeIssues.asSink )`
- **slicedWindow** [L288](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L288): `this.slicedWindow = new SlicedWindow({ maxAllowedGapInMs: windowConfig.maxAllowedGapInMs, totals: { highestLayerTotalEncodedFrames: null, mediaSourceTotalProducedFrames: null, }, slices: { detection: { numberOfSamples: windowConfig.numberOfSamples.detection, }, recovery: { numberOfSamples: windowConfig.numberOfSamples.recovery, offset: windowConfig.numberOfSamples.detection, } } })`
- **bitrate** [L348](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L348): `this.bitrate = 0`
- **jitter** [L349](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L349): `this.jitter = 0`
- **fractionLost** [L350](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L350): `this.fractionLost = 0`
- **sendingPacketRate** [L351](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L351): `this.sendingPacketRate = 0`
- **remoteReceivedPacketRate** [L352](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L352): `this.remoteReceivedPacketRate = 0`
- **highestLayer** [L353](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L353): `this.highestLayer = undefined`
- **bitrate** [L356](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L356): `this.bitrate += outboundRtp.bitrate ?? 0`
- **jitter** [L357](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L357): `this.jitter += outboundRtp.getRemoteInboundRtp()?.jitter ?? 0`
- **fractionLost** [L358](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L358): `this.fractionLost += outboundRtp.getRemoteInboundRtp()?.deltaFractionLost ?? 0`
- **sendingPacketRate** [L359](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L359): `this.sendingPacketRate += outboundRtp.packetRate ?? 0`
- **remoteReceivedPacketRate** [L360](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L360): `this.remoteReceivedPacketRate += outboundRtp.getRemoteInboundRtp()?.packetRate ?? 0`
- **highestLayer** [L364](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L364): `this.highestLayer = outboundRtp`
- **highestLayer** [L367](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L367): `this.highestLayer = outboundRtp`
- **settings** [L402](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L402): `this.settings = settings ? { ...settings } : undefined`
- **settings** [L405](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L405): `this.settings = undefined`
- **videoCaptureSettingsChanged** [L408](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts#L408): `this.videoCaptureSettingsChanged = previous === undefined ? undefined : previous.frameRate !== this.settings?.frameRate || previous.width !== this.settings?.width || previous.height !== this.settings?.height`

### Exact wire projection
```ts
public createSample(): OutboundTrackSample {
		return {
			id: this.track.id,
			kind: this.kind,
			timestamp: Date.now(),
			attachments: this.attachments,
			score: this.score,
			scoreReasons: sampledScoreReasons(
				this.calculatedScore.reasons,
				this.getPeerConnection()?.parent.config.sendScoreReasonsToServer,
			),
		};
	}
```

## PeerConnectionMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L163)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `statsAdapters` | StatsAdapters | [L171](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L171) |
| `detectors` | Detectors | [L173](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L173) |
| `issues` | IssueRegistry&lt;PeerConnectionIssues&gt; | [L180](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L180) |
| `mappedCodecMonitors` | public readonly mappedCodecMonitors = new Map&lt;string, CodecMonitor&gt;(); | [L181](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L181) |
| `mappedInboundRtpMonitors` | public readonly mappedInboundRtpMonitors = new Map&lt;number, InboundRtpMonitor&gt;(); | [L182](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L182) |
| `mappedRemoteOutboundRtpMonitors` | public readonly mappedRemoteOutboundRtpMonitors = new Map&lt;number, RemoteOutboundRtpMonitor&gt;(); | [L183](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L183) |
| `mappedOutboundRtpMonitors` | public readonly mappedOutboundRtpMonitors = new Map&lt;number, OutboundRtpMonitor&gt;(); | [L184](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L184) |
| `mappedDataChannelMonitors` | public readonly mappedDataChannelMonitors = new Map&lt;string, DataChannelMonitor&gt;(); | [L185](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L185) |
| `mappedRemoteInboundRtpMonitors` | public readonly mappedRemoteInboundRtpMonitors = new Map&lt;number, RemoteInboundRtpMonitor&gt;(); | [L186](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L186) |
| `mappedMediaSourceMonitors` | public readonly mappedMediaSourceMonitors = new Map&lt;string, MediaSourceMonitor&gt;(); | [L187](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L187) |
| `mappedMediaPlayoutMonitors` | public readonly mappedMediaPlayoutMonitors = new Map&lt;string, MediaPlayoutMonitor&gt;(); | [L188](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L188) |
| `mappedPeerConnectionTransportMonitors` | public readonly mappedPeerConnectionTransportMonitors = new Map&lt;string, PeerConnectionTransportMonitor&gt;(); | [L189](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L189) |
| `mappedIceTransportMonitors` | public readonly mappedIceTransportMonitors = new Map&lt;string, IceTransportMonitor&gt;(); | [L190](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L190) |
| `mappedIceCandidateMonitors` | public readonly mappedIceCandidateMonitors = new Map&lt;string, IceCandidateMonitor&gt;(); | [L191](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L191) |
| `mappedIceCandidatePairMonitors` | public readonly mappedIceCandidatePairMonitors = new Map&lt;string, IceCandidatePairMonitor&gt;(); | [L192](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L192) |
| `mappedCertificateMonitors` | public readonly mappedCertificateMonitors = new Map&lt;string, CertificateMonitor&gt;(); | [L193](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L193) |
| `mappedSelectedIcePaths` | public readonly mappedSelectedIcePaths = new Map&lt;string, SelectedIcePath&gt;(); | [L195](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L195) |
| `mappedInboundTracks` | public readonly mappedInboundTracks = new Map&lt;string, InboundTrackMonitor&gt;(); | [L202](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L202) |
| `mappedOutboundTracks` | public readonly mappedOutboundTracks = new Map&lt;string, OutboundTrackMonitor&gt;(); | [L203](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L203) |
| `closed` | public closed = false; | [L209](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L209) |
| `sendingAudioBitrate` | public sendingAudioBitrate = 0; | [L212](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L212) |
| `sendingVideoBitrate` | public sendingVideoBitrate = 0; | [L213](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L213) |
| `receivingAudioBitrate` | public receivingAudioBitrate = 0; | [L214](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L214) |
| `receivingVideoBitrate` | public receivingVideoBitrate = 0; | [L215](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L215) |
| `dataChannelSendingBitrate` | public dataChannelSendingBitrate = 0; | [L216](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L216) |
| `dataChannelReceivingBitrate` | public dataChannelReceivingBitrate = 0; | [L217](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L217) |
| `outboundFractionLost` | public outboundFractionLost = 0.0; | [L219](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L219) |
| `inboundFractionalLost` | public inboundFractionalLost = 0.0; | [L220](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L220) |
| `avgInboundFractionLost` | number | [L228](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L228) |
| `avgOutboundFractionLost` | number | [L231](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L231) |
| `avgInboundJitterInMs` | number | [L234](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L234) |
| `transportStability` | number | [L251](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L251) |
| `deltaTime` | number  /  undefined | [L258](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L258) |
| `statsClockTime` | public statsClockTime = 0; | [L265](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L265) |
| `slicedWindow` | SlicedWindow&lt;
		PeerConnectionWindowValues,
		// A slice for every stretch the config sizes, so the names are declared once. Only the
		// names matter here: how many samples each covers, and where it sits, are runtime.
		Record&lt;keyof PeerConnectionWindowConfig['numberOfSamples'], SliceConfig&gt;
	&gt; | [L286](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L286) |
| `totalInboundPacketsLost` | number | [L296](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L296) |
| `totalInboundPacketsReceived` | number | [L297](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L297) |
| `totalOutboundPacketsSent` | number | [L298](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L298) |
| `totalOutboundPacketsReceived` | number | [L299](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L299) |
| `totalOutboundPacketsLost` | number | [L300](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L300) |
| `totalDataChannelBytesSent` | number | [L301](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L301) |
| `totalDataChannelBytesReceived` | number | [L302](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L302) |
| `totalSentAudioBytes` | number | [L303](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L303) |
| `totalSentVideoBytes` | number | [L304](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L304) |
| `totalReceivedAudioBytes` | number | [L305](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L305) |
| `totalReceivedVideoBytes` | number | [L306](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L306) |
| `totalVideoEncodeTimeInMs` | number | [L307](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L307) |
| `totalVideoDecodeTimeInMs` | number | [L308](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L308) |
| `totalAvailableIncomingBitrate` | number | [L309](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L309) |
| `totalAvailableOutgoingBitrate` | number | [L310](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L310) |
| `totalPacketSendDelayInSec` | number | [L311](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L311) |
| `deltaInboundPacketsLost` | number | [L314](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L314) |
| `deltaInboundPacketsReceived` | number | [L315](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L315) |
| `deltaOutboundPacketsSent` | number | [L316](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L316) |
| `deltaOutboundPacketsReceived` | number | [L317](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L317) |
| `deltaOutboundPacketsLost` | number | [L318](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L318) |
| `deltaAudioBytesSent` | number | [L319](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L319) |
| `deltaVideoBytesSent` | number | [L320](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L320) |
| `deltaAudioBytesReceived` | number | [L321](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L321) |
| `deltaVideoBytesReceived` | number | [L322](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L322) |
| `deltaDataChannelBytesReceived` | number | [L323](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L323) |
| `deltaDataChannelBytesSent` | number | [L324](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L324) |
| `deltaPacketSendDelayInSec` | number | [L325](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L325) |
| `deltaVideoPacketsSent` | number | [L327](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L327) |
| `deltaVideoEncodeTimeInMs` | number | [L334](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L334) |
| `deltaVideoDecodeTimeInMs` | number | [L335](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L335) |
| `avgPacketSendDelayInMs` | number | [L342](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L342) |
| `deltaInboundVideoJitterBufferDelayInSec` | number | [L345](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L345) |
| `deltaInboundVideoJitterBufferEmittedCount` | number | [L346](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L346) |
| `avgInboundVideoJitterBufferDelayInMs` | number | [L356](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L356) |
| `uplinkCongested` | public uplinkCongested = false; | [L363](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L363) |
| `uplinkVideoCongestionSeverity` | number | [L364](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L364) |
| `downlinkCongested` | public downlinkCongested = false; | [L365](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L365) |
| `downlinkVideoCongestionSeverity` | number | [L366](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L366) |
| `cpulimited` | public cpulimited = false; | [L368](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L368) |
| `stalledRtpSender` | boolean | [L382](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L382) |
| `stalledTransportDemux` | boolean | [L385](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L385) |
| `hasInboundMedia` | public hasInboundMedia = false; | [L387](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L387) |
| `hasOutboundMedia` | public hasOutboundMedia = false; | [L388](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L388) |
| `hasInboundVideo` | public hasInboundVideo = false; | [L395](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L395) |
| `qualityLimitationReason` | PeerConnectionQualityLimitationReason | [L402](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L402) |
| `iceRttInSec` | number | [L408](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L408) |
| `ewmaIceRttInSec` | number | [L409](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L409) |
| `rtcpRttInSec` | number | [L412](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L412) |
| `ewmaRtcpRttInSec` | number | [L413](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L413) |
| `connectingStartedAt` | number | [L414](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L414) |
| `connectedAt` | number | [L415](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L415) |
| `iceState` | W3C.RtcIceTransportState | [L417](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L417) |
| `iceGatheringState` | string | [L420](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L420) |
| `usingTURN` | boolean | [L422](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L422) |
| `usingTCP` | boolean | [L423](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L423) |
| `calculatedStabilityScore` | CalculatedScore | [L424](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L424) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L430](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L430) |
| `avgRttInSec` | number  /  undefined | [L541](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L541) |
| `ewmaRttInSec` | number  /  undefined | [L546](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L546) |
| `score` | public get score() { | [L550](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L550) |
| `scoreReasons` | public get scoreReasons() { | [L554](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L554) |
| `congested` | public congested = false; | [L565](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L565) |
| `receivingBitrate` | public get receivingBitrate() { | [L567](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L567) |
| `sendingBitrate` | public get sendingBitrate() { | [L571](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L571) |
| `tracks` | public get tracks() { | [L575](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L575) |
| `codecs` | public get codecs() { | [L985](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L985) |
| `inboundRtps` | public get inboundRtps() { | [L989](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L989) |
| `remoteOutboundRtps` | public get remoteOutboundRtps() { | [L1042](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1042) |
| `outboundRtps` | public get outboundRtps() { | [L1046](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1046) |
| `remoteInboundRtps` | public get remoteInboundRtps() { | [L1050](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1050) |
| `mediaSources` | public get mediaSources() { | [L1054](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1054) |
| `mediaPlayouts` | public get mediaPlayouts() { | [L1058](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1058) |
| `dataChannels` | public get dataChannels() { | [L1062](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1062) |
| `peerConnectionTransports` | public get peerConnectionTransports() { | [L1066](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1066) |
| `iceTransports` | public get iceTransports() { | [L1070](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1070) |
| `iceCandidates` | public get iceCandidates() { | [L1074](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1074) |
| `localIceCandidates` | public get localIceCandidates() { | [L1079](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1079) |
| `iceCandidatePairs` | public get iceCandidatePairs() { | [L1083](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1083) |
| `certificates` | public get certificates() { | [L1087](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1087) |
| `selectedIcePaths` | public get selectedIcePaths() { | [L1091](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1091) |
| `selectedIcePath` | SelectedIcePath  /  undefined | [L1099](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1099) |
| `blockedTransport` | boolean | [L1110](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1110) |
| `selectedIceCandidatePairs` | public get selectedIceCandidatePairs() { | [L1118](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1118) |
| `connectionState` | public get connectionState() { | [L1164](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1164) |

### Assignment and formula index

- **statsAdapters** [L440](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L440): `this.statsAdapters = new StatsAdapters(logger)`
- **issues** [L441](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L441): `this.issues = new IssueRegistry<PeerConnectionIssues>(parent.activeIssues.asSink)`
- **slicedWindow** [L446](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L446): `this.slicedWindow = new SlicedWindow({ maxAllowedGapInMs: windowConfig.maxAllowedGapInMs, totals: PEER_CONNECTION_WINDOW_VALUES, slices: { detection: { numberOfSamples: windowConfig.numberOfSamples.detection, }, recovery: { numberOfSamples: windowConfig.numberOfSamples.recovery, offset: windowConfig.numberOfSamples.detection, }, }, })`
- **detectors** [L459](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L459): `this.detectors = new Detectors()`
- **deltaTime** [L632](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L632): `this.deltaTime = timeDelta !== undefined && 0 < timeDelta ? timeDelta : undefined`
- **statsClockTime** [L633](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L633): `this.statsClockTime += this.deltaTime ?? 0`
- **deltaVideoBytesSent** [L642](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L642): `this.deltaVideoBytesSent = undefined`
- **deltaAudioBytesSent** [L643](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L643): `this.deltaAudioBytesSent = undefined`
- **deltaVideoBytesReceived** [L644](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L644): `this.deltaVideoBytesReceived = undefined`
- **deltaAudioBytesReceived** [L645](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L645): `this.deltaAudioBytesReceived = undefined`
- **deltaDataChannelBytesReceived** [L646](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L646): `this.deltaDataChannelBytesReceived = undefined`
- **deltaDataChannelBytesSent** [L647](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L647): `this.deltaDataChannelBytesSent = undefined`
- **deltaOutboundPacketsLost** [L648](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L648): `this.deltaOutboundPacketsLost = undefined`
- **deltaOutboundPacketsReceived** [L649](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L649): `this.deltaOutboundPacketsReceived = undefined`
- **deltaOutboundPacketsSent** [L650](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L650): `this.deltaOutboundPacketsSent = undefined`
- **deltaInboundPacketsLost** [L651](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L651): `this.deltaInboundPacketsLost = undefined`
- **deltaInboundPacketsReceived** [L652](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L652): `this.deltaInboundPacketsReceived = undefined`
- **deltaPacketSendDelayInSec** [L653](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L653): `this.deltaPacketSendDelayInSec = undefined`
- **deltaInboundVideoJitterBufferDelayInSec** [L654](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L654): `this.deltaInboundVideoJitterBufferDelayInSec = undefined`
- **deltaInboundVideoJitterBufferEmittedCount** [L655](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L655): `this.deltaInboundVideoJitterBufferEmittedCount = undefined`
- **avgInboundVideoJitterBufferDelayInMs** [L656](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L656): `this.avgInboundVideoJitterBufferDelayInMs = undefined`
- **deltaVideoPacketsSent** [L657](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L657): `this.deltaVideoPacketsSent = undefined`
- **deltaVideoEncodeTimeInMs** [L658](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L658): `this.deltaVideoEncodeTimeInMs = undefined`
- **deltaVideoDecodeTimeInMs** [L659](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L659): `this.deltaVideoDecodeTimeInMs = undefined`
- **avgPacketSendDelayInMs** [L660](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L660): `this.avgPacketSendDelayInMs = undefined`
- **sendingAudioBitrate** [L662](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L662): `this.sendingAudioBitrate = 0`
- **sendingVideoBitrate** [L663](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L663): `this.sendingVideoBitrate = 0`
- **receivingAudioBitrate** [L664](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L664): `this.receivingAudioBitrate = 0`
- **receivingVideoBitrate** [L665](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L665): `this.receivingVideoBitrate = 0`
- **dataChannelSendingBitrate** [L666](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L666): `this.dataChannelSendingBitrate = 0`
- **dataChannelReceivingBitrate** [L667](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L667): `this.dataChannelReceivingBitrate = 0`
- **outboundFractionLost** [L668](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L668): `this.outboundFractionLost = 0`
- **inboundFractionalLost** [L669](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L669): `this.inboundFractionalLost = 0`
- **totalAvailableIncomingBitrate** [L670](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L670): `this.totalAvailableIncomingBitrate = undefined`
- **totalAvailableOutgoingBitrate** [L671](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L671): `this.totalAvailableOutgoingBitrate = undefined`
- **qualityLimitationReason** [L672](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L672): `this.qualityLimitationReason = undefined`
- **hasInboundMedia** [L673](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L673): `this.hasInboundMedia = false`
- **hasOutboundMedia** [L674](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L674): `this.hasOutboundMedia = false`
- **hasInboundVideo** [L675](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L675): `this.hasInboundVideo = false`
- **receivingAudioBitrate** [L689](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L689): `this.receivingAudioBitrate += monitor?.bitrate ?? 0`
- **deltaAudioBytesReceived** [L690](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L690): `this.deltaAudioBytesReceived = accumulatedValue(this.deltaAudioBytesReceived, monitor?.deltaBytesReceived)`
- **hasInboundMedia** [L691](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L691): `this.hasInboundMedia = true`
- **receivingVideoBitrate** [L694](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L694): `this.receivingVideoBitrate += monitor?.bitrate ?? 0`
- **deltaVideoBytesReceived** [L695](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L695): `this.deltaVideoBytesReceived = accumulatedValue(this.deltaVideoBytesReceived, monitor?.deltaBytesReceived)`
- **hasInboundMedia** [L696](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L696): `this.hasInboundMedia = true`
- **hasInboundVideo** [L697](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L697): `this.hasInboundVideo = true`
- **deltaVideoDecodeTimeInMs** [L700](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L700): `this.deltaVideoDecodeTimeInMs = accumulatedValue( this.deltaVideoDecodeTimeInMs, monitor.deltaTotalDecodeTime === undefined ? undefined : monitor.deltaTotalDecodeTime * 1000, )`
- **deltaInboundVideoJitterBufferDelayInSec** [L712](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L712): `this.deltaInboundVideoJitterBufferDelayInSec = accumulatedValue( this.deltaInboundVideoJitterBufferDelayInSec, monitor?.deltaJitterBufferDelay, )`
- **deltaInboundVideoJitterBufferEmittedCount** [L716](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L716): `this.deltaInboundVideoJitterBufferEmittedCount = accumulatedValue( this.deltaInboundVideoJitterBufferEmittedCount, monitor?.deltaJitterBufferEmittedCount, )`
- **inboundFractionalLost** [L725](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L725): `this.inboundFractionalLost += monitor?.deltaFractionLost ?? 0.0`
- **deltaInboundPacketsLost** [L726](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L726): `this.deltaInboundPacketsLost = accumulatedValue(this.deltaInboundPacketsLost, monitor?.deltaPacketsLost)`
- **deltaInboundPacketsReceived** [L727](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L727): `this.deltaInboundPacketsReceived = accumulatedValue(this.deltaInboundPacketsReceived, monitor?.deltaPacketsReceived)`
- **sendingAudioBitrate** [L745](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L745): `this.sendingAudioBitrate += monitor?.bitrate ?? 0`
- **deltaAudioBytesSent** [L746](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L746): `this.deltaAudioBytesSent = accumulatedValue(this.deltaAudioBytesSent, monitor?.deltaBytesSent)`
- **hasOutboundMedia** [L747](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L747): `this.hasOutboundMedia = true`
- **sendingVideoBitrate** [L750](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L750): `this.sendingVideoBitrate += monitor?.bitrate ?? 0`
- **deltaVideoBytesSent** [L751](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L751): `this.deltaVideoBytesSent = accumulatedValue(this.deltaVideoBytesSent, monitor?.deltaBytesSent)`
- **deltaVideoEncodeTimeInMs** [L754](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L754): `this.deltaVideoEncodeTimeInMs = accumulatedValue( this.deltaVideoEncodeTimeInMs, monitor.deltaEncodeTime === undefined ? undefined : monitor.deltaEncodeTime * 1000, )`
- **totalPacketSendDelayInSec** [L761](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L761): `this.totalPacketSendDelayInSec = accumulatedValue(this.totalPacketSendDelayInSec, monitor?.deltaPacketSendDelay)`
- **deltaPacketSendDelayInSec** [L762](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L762): `this.deltaPacketSendDelayInSec = accumulatedValue(this.deltaPacketSendDelayInSec, monitor?.deltaPacketSendDelay)`
- **deltaVideoPacketsSent** [L763](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L763): `this.deltaVideoPacketsSent = accumulatedValue(this.deltaVideoPacketsSent, monitor?.deltaPacketsSent)`
- **hasOutboundMedia** [L764](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L764): `this.hasOutboundMedia = true`
- **deltaOutboundPacketsSent** [L767](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L767): `this.deltaOutboundPacketsSent = accumulatedValue(this.deltaOutboundPacketsSent, monitor?.deltaPacketsSent)`
- **outboundFractionLost** [L786](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L786): `this.outboundFractionLost += monitor?.deltaFractionLost ?? 0.0`
- **deltaOutboundPacketsLost** [L787](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L787): `this.deltaOutboundPacketsLost = accumulatedValue(this.deltaOutboundPacketsLost, monitor?.deltaPacketsLost)`
- **deltaOutboundPacketsReceived** [L788](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L788): `this.deltaOutboundPacketsReceived = accumulatedValue(this.deltaOutboundPacketsReceived, monitor?.deltaPacketsReceived)`
- **deltaDataChannelBytesSent** [L795](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L795): `this.deltaDataChannelBytesSent = accumulatedValue(this.deltaDataChannelBytesSent, monitor?.deltaBytesSent)`
- **deltaDataChannelBytesReceived** [L796](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L796): `this.deltaDataChannelBytesReceived = accumulatedValue(this.deltaDataChannelBytesReceived, monitor?.deltaBytesReceived)`
- **dataChannelSendingBitrate** [L797](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L797): `this.dataChannelSendingBitrate += monitor?.sendingBitrate ?? 0`
- **dataChannelReceivingBitrate** [L798](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L798): `this.dataChannelReceivingBitrate += monitor?.receivingBitrate ?? 0`
- **rtcpRttInSec** [L846](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L846): `this.rtcpRttInSec = rtcpRttMeasurementsInS.reduce((acc, rtt) => acc + rtt, 0) / rtcpRttMeasurementsInS.length`
- **ewmaRtcpRttInSec** [L847](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L847): `this.ewmaRtcpRttInSec = this.ewmaRtcpRttInSec !== undefined ? (this.rtcpRttInSec * 0.1) + (this.ewmaRtcpRttInSec * 0.9) : this.rtcpRttInSec`
- **totalAvailableIncomingBitrate** [L856](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L856): `this.totalAvailableIncomingBitrate = accumulatedValue(this.totalAvailableIncomingBitrate, selectedPair.availableIncomingBitrate)`
- **totalAvailableOutgoingBitrate** [L857](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L857): `this.totalAvailableOutgoingBitrate = accumulatedValue(this.totalAvailableOutgoingBitrate, selectedPair.availableOutgoingBitrate)`
- **iceRttInSec** [L868](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L868): `this.iceRttInSec = iceRttMeasurementsInS.reduce((acc, rtt) => acc + rtt, 0) / iceRttMeasurementsInS.length`
- **ewmaIceRttInSec** [L869](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L869): `this.ewmaIceRttInSec = this.ewmaIceRttInSec !== undefined ? (this.iceRttInSec * 0.1) + (this.ewmaIceRttInSec * 0.9) : this.iceRttInSec`
- **usingTCP** [L876](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L876): `this.usingTCP = selectedIceCandidatePairs.some(pair => pair.usingTcp)`
- **usingTURN** [L877](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L877): `this.usingTURN = selectedIceCandidatePairs.some(pair => pair.usingTurn)`
- **iceState** [L879](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L879): `this.iceState = this._mostSevereIceState()`
- **avgPacketSendDelayInMs** [L883](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L883): `this.avgPacketSendDelayInMs = this.deltaPacketSendDelayInSec !== undefined && this.deltaVideoPacketsSent !== undefined && this.deltaVideoPacketsSent > 0 ? (this.deltaPacketSendDelayInSec * 1000) / this.deltaVideoPacketsSent : undefined`
- **avgInboundVideoJitterBufferDelayInMs** [L891](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L891): `this.avgInboundVideoJitterBufferDelayInMs = this.deltaInboundVideoJitterBufferDelayInSec !== undefined && this.deltaInboundVideoJitterBufferEmittedCount !== undefined && this.deltaInboundVideoJitterBufferEmittedCount > 0 ? (this.deltaInboundVideoJitterBufferDelayInSec * 1000) / this.deltaInboundVideoJitterBufferEmittedCount : undefined`
- **totalDataChannelBytesReceived** [L897](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L897): `this.totalDataChannelBytesReceived = accumulatedValue(this.totalDataChannelBytesReceived, this.deltaDataChannelBytesReceived)`
- **totalDataChannelBytesSent** [L898](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L898): `this.totalDataChannelBytesSent = accumulatedValue(this.totalDataChannelBytesSent, this.deltaDataChannelBytesSent)`
- **totalSentAudioBytes** [L899](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L899): `this.totalSentAudioBytes = accumulatedValue(this.totalSentAudioBytes, this.deltaAudioBytesSent)`
- **totalSentVideoBytes** [L900](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L900): `this.totalSentVideoBytes = accumulatedValue(this.totalSentVideoBytes, this.deltaVideoBytesSent)`
- **totalReceivedAudioBytes** [L901](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L901): `this.totalReceivedAudioBytes = accumulatedValue(this.totalReceivedAudioBytes, this.deltaAudioBytesReceived)`
- **totalReceivedVideoBytes** [L902](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L902): `this.totalReceivedVideoBytes = accumulatedValue(this.totalReceivedVideoBytes, this.deltaVideoBytesReceived)`
- **totalVideoEncodeTimeInMs** [L903](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L903): `this.totalVideoEncodeTimeInMs = accumulatedValue(this.totalVideoEncodeTimeInMs, this.deltaVideoEncodeTimeInMs)`
- **totalVideoDecodeTimeInMs** [L904](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L904): `this.totalVideoDecodeTimeInMs = accumulatedValue(this.totalVideoDecodeTimeInMs, this.deltaVideoDecodeTimeInMs)`
- **totalOutboundPacketsSent** [L905](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L905): `this.totalOutboundPacketsSent = accumulatedValue(this.totalOutboundPacketsSent, this.deltaOutboundPacketsSent)`
- **totalOutboundPacketsReceived** [L906](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L906): `this.totalOutboundPacketsReceived = accumulatedValue(this.totalOutboundPacketsReceived, this.deltaOutboundPacketsReceived)`
- **totalOutboundPacketsLost** [L907](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L907): `this.totalOutboundPacketsLost = accumulatedValue(this.totalOutboundPacketsLost, this.deltaOutboundPacketsLost)`
- **totalInboundPacketsLost** [L908](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L908): `this.totalInboundPacketsLost = accumulatedValue(this.totalInboundPacketsLost, this.deltaInboundPacketsLost)`
- **totalInboundPacketsReceived** [L909](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L909): `this.totalInboundPacketsReceived = accumulatedValue(this.totalInboundPacketsReceived, this.deltaInboundPacketsReceived)`
- **connectingStartedAt** [L1155](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1155): `this.connectingStartedAt = Date.now()`
- **connectedAt** [L1157](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1157): `this.connectedAt = Date.now()`
- **connectingStartedAt** [L1159](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1159): `this.connectingStartedAt = undefined`
- **connectedAt** [L1160](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1160): `this.connectedAt = undefined`
- **qualityLimitationReason** [L1213](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1213): `this.qualityLimitationReason = newReason`
- **qualityLimitationReason** [L1221](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1221): `this.qualityLimitationReason = newReason`
- **transportStability** [L1241](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1241): `this.transportStability = rttInSec === undefined || jitterInMs === undefined || lossFraction === undefined ? undefined : transportStability({ rttInMs: rttInSec * 1000, jitterInMs, packetLossPercent: Math.max( this.avgInboundFractionLost ?? 0, this.avgOutboundFractionLost ?? 0, ) * 100, })`
- **avgInboundFractionLost** [L1272](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1272): `this.avgInboundFractionLost = 0 < lossCount ? lossSum / lossCount : undefined`
- **avgInboundJitterInMs** [L1273](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1273): `this.avgInboundJitterInMs = 0 < jitterCount ? jitterSum / jitterCount : undefined`
- **avgOutboundFractionLost** [L1285](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1285): `this.avgOutboundFractionLost = 0 < outboundLossCount ? outboundLossSum / outboundLossCount : undefined`
- **closed** [L1426](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L1426): `this.closed = true`

### Exact wire projection
```ts
public createSample(): PeerConnectionSample {
		return {
			peerConnectionId: this.peerConnectionId,

			attachments: this.attachments,

			codecs: this.codecs.map(codec => codec.createSample()),
			inboundRtps: this.inboundRtps.map(inboundRtp => inboundRtp.createSample()),
			remoteOutboundRtps: this.remoteOutboundRtps.map(remoteOutboundRtp => remoteOutboundRtp.createSample()),
			outboundRtps: this.outboundRtps.map(outboundRtp => outboundRtp.createSample()),
			remoteInboundRtps: this.remoteInboundRtps.map(remoteInboundRtp => remoteInboundRtp.createSample()),
			mediaSources: this.mediaSources.map(mediaSource => mediaSource.createSample()),
			mediaPlayouts: this.mediaPlayouts.map(mediaPlayout => mediaPlayout.createSample()),
			peerConnectionTransports: this.peerConnectionTransports.map(peerConnectionTransport => peerConnectionTransport.createSample()),
			dataChannels: this.dataChannels.map(dataChannel => dataChannel.createSample()),
			iceTransports: this.iceTransports.map(iceTransport => iceTransport.createSample()),
			iceCandidates: this.iceCandidates.map(iceCandidate => iceCandidate.createSample()),
			iceCandidatePairs: this.iceCandidatePairs.map(iceCandidatePair => iceCandidatePair.createSample()),
			certificates: this.certificates.map(certificate => certificate.createSample()),
			inboundTracks: [ ...this.mappedInboundTracks.values() ].map(inboundTrack => inboundTrack.createSample()),
			outboundTracks: [ ...this.mappedOutboundTracks.values() ].map(outboundTrack => outboundTrack.createSample()),
			score: this.score,
			scoreReasons: sampledScoreReasons(this.calculatedStabilityScore.reasons, this.parent.config.sendScoreReasonsToServer)
		}
	}
```

## PeerConnectionTransportMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionTransportMonitor.ts#L4)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `timestamp` | number | [L7](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionTransportMonitor.ts#L7) |
| `id` | string | [L8](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionTransportMonitor.ts#L8) |
| `dataChannelsOpened` | number | [L9](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionTransportMonitor.ts#L9) |
| `dataChannelsClosed` | number | [L10](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionTransportMonitor.ts#L10) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L16](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionTransportMonitor.ts#L16) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L21](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionTransportMonitor.ts#L21) |
| `visited` | boolean | [L33](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionTransportMonitor.ts#L33) |

### Assignment and formula index

- **id** [L27](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionTransportMonitor.ts#L27): `this.id = options.id`
- **timestamp** [L28](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionTransportMonitor.ts#L28): `this.timestamp = options.timestamp`

### Exact wire projection
```ts
public createSample(): PeerConnectionTransportStats {
		return {
			id: this.id,
			timestamp: this.timestamp,
			dataChannelsOpened: this.dataChannelsOpened,
			dataChannelsClosed: this.dataChannelsClosed,
			attachments: this.attachments,
		};
	}
```

## RemoteInboundRtpMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L5)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `timestamp` | number | [L8](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L8) |
| `id` | string | [L9](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L9) |
| `ssrc` | number | [L10](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L10) |
| `kind` | string | [L11](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L11) |
| `transportId` | string  /  undefined | [L12](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L12) |
| `codecId` | string  /  undefined | [L13](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L13) |
| `packetsReceived` | number  /  undefined | [L14](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L14) |
| `packetsReceivedWithEct1` | number  /  undefined | [L15](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L15) |
| `packetsReceivedWithCe` | number  /  undefined | [L16](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L16) |
| `packetsReportedAsLost` | number  /  undefined | [L17](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L17) |
| `packetsReportedAsLostButRecovered` | number  /  undefined | [L18](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L18) |
| `packetsLost` | number  /  undefined | [L19](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L19) |
| `jitter` | number  /  undefined | [L20](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L20) |
| `localId` | string  /  undefined | [L21](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L21) |
| `roundTripTime` | number  /  undefined | [L22](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L22) |
| `totalRoundTripTime` | number  /  undefined | [L23](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L23) |
| `fractionLost` | number  /  undefined | [L24](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L24) |
| `roundTripTimeMeasurements` | number  /  undefined | [L25](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L25) |
| `packetsWithBleachedEct1Marking` | number  /  undefined | [L26](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L26) |
| `packetRate` | number | [L29](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L29) |
| `deltaPacketsLost` | number | [L31](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L31) |
| `deltaPacketsReceived` | number | [L32](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L32) |
| `deltaFractionLost` | number | [L33](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L33) |
| `avgRoundTripTimeInSec` | number | [L39](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L39) |
| `deltaTotalRoundTripTime` | number | [L41](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L41) |
| `deltaRoundTripTimeMeasurements` | number | [L42](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L42) |
| `deltaTime` | number  /  undefined | [L45](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L45) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L49](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L49) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L51](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L51) |
| `visited` | boolean | [L66](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L66) |
| `statsClockTime` | public statsClockTime = 0; | [L75](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L75) |

### Assignment and formula index

- **id** [L57](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L57): `this.id = options.id`
- **timestamp** [L58](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L58): `this.timestamp = options.timestamp`
- **ssrc** [L59](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L59): `this.ssrc = options.ssrc`
- **kind** [L60](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L60): `this.kind = options.kind`
- **deltaTime** [L105](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L105): `this.deltaTime = 0`
- **deltaPacketsReceived** [L106](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L106): `this.deltaPacketsReceived = undefined`
- **deltaPacketsLost** [L107](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L107): `this.deltaPacketsLost = undefined`
- **deltaFractionLost** [L108](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L108): `this.deltaFractionLost = undefined`
- **deltaTotalRoundTripTime** [L109](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L109): `this.deltaTotalRoundTripTime = undefined`
- **deltaRoundTripTimeMeasurements** [L110](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L110): `this.deltaRoundTripTimeMeasurements = undefined`
- **avgRoundTripTimeInSec** [L111](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L111): `this.avgRoundTripTimeInSec = undefined`
- **packetRate** [L112](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L112): `this.packetRate = undefined`
- **deltaTime** [L117](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L117): `this.deltaTime = elapsedInMs`
- **statsClockTime** [L118](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L118): `this.statsClockTime += elapsedInMs`
- **deltaPacketsReceived** [L121](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L121): `this.deltaPacketsReceived = positiveDelta(stats.packetsReceived, this.packetsReceived)`
- **packetRate** [L123](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L123): `this.packetRate = this.deltaPacketsReceived / elapsedInSeconds`
- **deltaPacketsLost** [L126](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L126): `this.deltaPacketsLost = positiveDelta(stats.packetsLost, this.packetsLost)`
- **deltaTotalRoundTripTime** [L127](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L127): `this.deltaTotalRoundTripTime = positiveDelta(stats.totalRoundTripTime, this.totalRoundTripTime)`
- **deltaRoundTripTimeMeasurements** [L128](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L128): `this.deltaRoundTripTimeMeasurements = positiveDelta(stats.roundTripTimeMeasurements, this.roundTripTimeMeasurements)`
- **avgRoundTripTimeInSec** [L130](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L130): `this.avgRoundTripTimeInSec = this.deltaTotalRoundTripTime !== undefined && this.deltaRoundTripTimeMeasurements !== undefined && this.deltaRoundTripTimeMeasurements > 0 ? this.deltaTotalRoundTripTime / this.deltaRoundTripTimeMeasurements : undefined`
- **deltaFractionLost** [L138](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteInboundRtpMonitor.ts#L138): `this.deltaFractionLost = totalDelta > 0 ? this.deltaPacketsLost / totalDelta : 0.0`

### Exact wire projection
```ts
public createSample(): RemoteInboundRtpStats {
		return {
			timestamp: this.timestamp,
			id: this.id,
			ssrc: this.ssrc,
			kind: this.kind,
			transportId: this.transportId,
			codecId: this.codecId,
			packetsReceived: this.packetsReceived,
			packetsReceivedWithEct1: this.packetsReceivedWithEct1,
			packetsReceivedWithCe: this.packetsReceivedWithCe,
			packetsReportedAsLost: this.packetsReportedAsLost,
			packetsReportedAsLostButRecovered: this.packetsReportedAsLostButRecovered,
			packetsLost: this.packetsLost,
			jitter: this.jitter,
			localId: this.localId,
			roundTripTime: this.roundTripTime,
			totalRoundTripTime: this.totalRoundTripTime,
			fractionLost: this.fractionLost,
			roundTripTimeMeasurements: this.roundTripTimeMeasurements,
			packetsWithBleachedEct1Marking: this.packetsWithBleachedEct1Marking,

			attachments: this.attachments,
		};
	}
```

## RemoteOutboundRtpMonitor
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L5)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `timestamp` | number | [L8](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L8) |
| `id` | string | [L9](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L9) |
| `ssrc` | number | [L10](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L10) |
| `kind` | string | [L11](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L11) |
| `transportId` | string  /  undefined | [L12](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L12) |
| `codecId` | string  /  undefined | [L13](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L13) |
| `packetsSent` | number  /  undefined | [L14](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L14) |
| `bytesSent` | number  /  undefined | [L15](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L15) |
| `deltaPacketsSent` | number  /  undefined | [L18](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L18) |
| `deltaBytesSent` | number  /  undefined | [L19](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L19) |
| `localId` | string  /  undefined | [L20](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L20) |
| `remoteTimestamp` | number  /  undefined | [L21](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L21) |
| `reportsSent` | number  /  undefined | [L22](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L22) |
| `roundTripTime` | number  /  undefined | [L23](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L23) |
| `totalRoundTripTime` | number  /  undefined | [L24](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L24) |
| `roundTripTimeMeasurements` | number  /  undefined | [L25](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L25) |
| `bitrate` | number  /  undefined | [L28](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L28) |
| `deltaTime` | number  /  undefined | [L31](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L31) |
| `attachments` | Record&lt;string, unknown&gt;  /  undefined | [L36](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L36) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L38](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L38) |
| `visited` | boolean | [L52](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L52) |
| `statsClockTime` | public statsClockTime = 0; | [L61](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L61) |

### Assignment and formula index

- **id** [L44](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L44): `this.id = options.id`
- **timestamp** [L45](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L45): `this.timestamp = options.timestamp`
- **ssrc** [L46](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L46): `this.ssrc = options.ssrc`
- **kind** [L47](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L47): `this.kind = options.kind`
- **deltaTime** [L91](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L91): `this.deltaTime = 0`
- **deltaPacketsSent** [L92](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L92): `this.deltaPacketsSent = undefined`
- **deltaBytesSent** [L93](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L93): `this.deltaBytesSent = undefined`
- **deltaTime** [L98](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L98): `this.deltaTime = elapsedInMs`
- **statsClockTime** [L99](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L99): `this.statsClockTime += elapsedInMs`
- **deltaPacketsSent** [L100](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L100): `this.deltaPacketsSent = positiveDelta(stats.packetsSent, this.packetsSent)`
- **deltaBytesSent** [L101](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/RemoteOutboundRtpMonitor.ts#L101): `this.deltaBytesSent = positiveDelta(stats.bytesSent, this.bytesSent)`

### Exact wire projection
```ts
public createSample(): RemoteOutboundRtpStats {
		return {
			id: this.id,
			timestamp: this.timestamp,
			ssrc: this.ssrc,
			kind: this.kind,
			transportId: this.transportId,
			codecId: this.codecId,
			packetsSent: this.packetsSent,
			bytesSent: this.bytesSent,
			localId: this.localId,
			remoteTimestamp: this.remoteTimestamp,
			reportsSent: this.reportsSent,
			roundTripTime: this.roundTripTime,
			totalRoundTripTime: this.totalRoundTripTime,
			roundTripTimeMeasurements: this.roundTripTimeMeasurements,
			attachments: this.attachments,
		};
	}
```

## SelectedIcePath
[Source](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L86)

| Public field / getter | Type or declaration | Source |
|---|---|---|
| `createdAt` | public readonly createdAt = Date.now(); | [L88](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L88) |
| `updatedAt` | public updatedAt = Date.now(); | [L89](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L89) |
| `closed` | public closed = false; | [L90](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L90) |
| `durations` | IcePathDurations | [L93](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L93) |
| `pathSwitches` | public pathSwitches = 0; | [L95](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L95) |
| `directToRelaySwitches` | public directToRelaySwitches = 0; | [L96](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L96) |
| `relayToDirectSwitches` | public relayToDirectSwitches = 0; | [L97](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L97) |
| `relayProtocolSwitches` | public relayProtocolSwitches = 0; | [L98](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L98) |
| `turnServerSwitches` | public turnServerSwitches = 0; | [L99](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L99) |
| `firstRelaySelectedAt` | number | [L102](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L102) |
| `lastSwitchedAt` | number | [L103](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L103) |
| `totalBytesSent` | public totalBytesSent = 0; | [L105](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L105) |
| `totalBytesReceived` | public totalBytesReceived = 0; | [L106](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L106) |
| `totalPacketsSent` | public totalPacketsSent = 0; | [L107](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L107) |
| `totalPacketsReceived` | public totalPacketsReceived = 0; | [L108](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L108) |
| `relayBytesSent` | public relayBytesSent = 0; | [L111](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L111) |
| `relayBytesReceived` | public relayBytesReceived = 0; | [L112](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L112) |
| `relayPacketsSent` | public relayPacketsSent = 0; | [L113](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L113) |
| `relayPacketsReceived` | public relayPacketsReceived = 0; | [L114](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L114) |
| `appData` | Record&lt;string, unknown&gt;  /  undefined | [L126](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L126) |
| `pair` | IceCandidatePairMonitor | [L149](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L149) |
| `localCandidate` | public get localCandidate() { | [L153](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L153) |
| `remoteCandidate` | public get remoteCandidate() { | [L157](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L157) |
| `iceTransport` | public get iceTransport() { | [L161](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L161) |
| `pairId` | public get pairId() { | [L167](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L167) |
| `transportId` | public get transportId() { | [L171](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L171) |
| `kind` | IcePathKind | [L175](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L175) |
| `usingTurn` | boolean | [L179](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L179) |
| `usingTcp` | boolean | [L183](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L183) |
| `relayProtocol` | public get relayProtocol() { | [L187](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L187) |
| `turnUrl` | public get turnUrl() { | [L191](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L191) |
| `turnServer` | public get turnServer() { | [L195](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L195) |
| `tuple` | public get tuple() { | [L199](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L199) |
| `protocol` | public get protocol() { | [L203](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L203) |
| `localCandidateType` | public get localCandidateType() { | [L207](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L207) |
| `remoteCandidateType` | public get remoteCandidateType() { | [L211](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L211) |
| `localAddress` | public get localAddress() { | [L215](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L215) |
| `localPort` | public get localPort() { | [L219](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L219) |
| `localAddressFamily` | public get localAddressFamily() { | [L223](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L223) |
| `remoteAddress` | public get remoteAddress() { | [L227](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L227) |
| `remotePort` | public get remotePort() { | [L231](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L231) |
| `remoteAddressFamily` | public get remoteAddressFamily() { | [L235](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L235) |
| `currentRoundTripTime` | public get currentRoundTripTime() { | [L239](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L239) |
| `state` | public get state() { | [L243](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L243) |
| `durationInMs` | number | [L250](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L250) |
| `relayDurationInMs` | number | [L255](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L255) |
| `timeToFirstRelayInMs` | number  /  undefined | [L266](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L266) |
| `relayBytesRatio` | number  /  undefined | [L271](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L271) |

### Assignment and formula index

- **firstRelaySelectedAt** [L139](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L139): `this.firstRelaySelectedAt = this.createdAt`
- **durations[previousKind]** [L311](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L311): `this.durations[previousKind] += Math.max(0, now - this._kindSince)`
- **updatedAt** [L314](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L314): `this.updatedAt = now`
- **firstRelaySelectedAt** [L323](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L323): `this.firstRelaySelectedAt = now`
- **lastSwitchedAt** [L340](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L340): `this.lastSwitchedAt = now`
- **closed** [L370](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L370): `this.closed = true`
- **durations[this._kind]** [L372](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L372): `this.durations[this._kind] += Math.max(0, Date.now() - this._kindSince)`
- **totalBytesSent** [L384](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L384): `this.totalBytesSent += bytesSent`
- **totalBytesReceived** [L385](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L385): `this.totalBytesReceived += bytesReceived`
- **totalPacketsSent** [L386](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L386): `this.totalPacketsSent += packetsSent`
- **totalPacketsReceived** [L387](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L387): `this.totalPacketsReceived += packetsReceived`
- **relayBytesSent** [L391](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L391): `this.relayBytesSent += bytesSent`
- **relayBytesReceived** [L392](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L392): `this.relayBytesReceived += bytesReceived`
- **relayPacketsSent** [L393](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L393): `this.relayPacketsSent += packetsSent`
- **relayPacketsReceived** [L394](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts#L394): `this.relayPacketsReceived += packetsReceived`

