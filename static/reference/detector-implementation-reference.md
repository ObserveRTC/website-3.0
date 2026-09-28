# Detector implementation reference
All stable and next detector implementations are indexed here. Every entry contains the exact state, input guards, threshold comparisons, emission payloads, and recovery code. Defaults live in ClientMonitor.constructor, reproduced below, rather than independently inside these detector classes. This reference preserves source comments as evidence, not as independently verified assertions.

## client-monitor-js
### Configuration defaults
```ts
public constructor(
        config?: Partial<ClientMonitorConfig<AppData>>,
    ) {
        super();
        const monitorConfig = config ?? {};

        this.logger = monitorConfig.logger ?? createLogger();

        // Defaults are applied only when the user did not specify the key
        // (undefined). Explicit `null` means "disable this detector entirely"
        // and is preserved — the corresponding detector won't be instantiated.
        const detectorDefault = <T>(value: T | null | undefined, fallback: T): T | null =>
            value === undefined ? fallback : value;

        const collectingPeriodInMs = 0 < (monitorConfig.collectingPeriodInMs ?? 0)
            ? monitorConfig.collectingPeriodInMs as number
            : 5000;


        this.config = {
            ...monitorConfig,
            collectingPeriodInMs: monitorConfig.collectingPeriodInMs ?? 5000,
            samplingPeriodInMs: monitorConfig.samplingPeriodInMs ?? 5000,

            integrateNavigatorMediaDevices: monitorConfig.integrateNavigatorMediaDevices ?? true,
            watchTabVisibility: monitorConfig.watchTabVisibility ?? true,
            addClientJointEventOnCreated: monitorConfig.addClientJointEventOnCreated ?? true,
            addClientLeftEventOnClose: monitorConfig.addClientLeftEventOnClose ?? true,
            // The slices are counted in values, not milliseconds, so that a slice asked for N
            // values holds N at any collecting period and is readable at any cadence. What varies
            // is the stretch those values span: N values span N-1 intervals, so at the default
            // 5000ms period a slice of 2 covers 5s and one of 4 covers 15s. `maxAllowedGapInMs`
            // tolerates a couple of late or missed collections and treats anything longer as a
            // blackout worth starting again after.
            outboundTrackWindow: monitorConfig.outboundTrackWindow ?? {
                numberOfSamples: {
                    detection: 3,
                    recovery: 3,
                },
                maxAllowedGapInMs: collectingPeriodInMs * 4,
            },
            inboundTrackWindow: monitorConfig.inboundTrackWindow ?? {
                numberOfSamples: {
                    detection: 3,
                    recovery: 3,
                    flowDetection: 4,
                    flowRecovery: 3,
                },
                maxAllowedGapInMs: collectingPeriodInMs * 4,
            },
            peerConnectionWindow: monitorConfig.peerConnectionWindow ?? {
                numberOfSamples: {
                    detection: 3,
                    recovery: 3,
                },
                maxAllowedGapInMs: collectingPeriodInMs * 4,
            },
            clientWindow: monitorConfig.clientWindow ?? {
                numberOfSamples: {
                    detection: 3,
                    recovery: 3,
                },
                maxAllowedGapInMs: collectingPeriodInMs * 4,
            },
            // Detector defaults, one entry per detector, grouped as in
            // `ClientMonitorConfig` so the two files read side by side.

            // Connectivity — layer 1: reachability.
            iceReachabilityDetector: detectorDefault(monitorConfig.iceReachabilityDetector, {
                thresholdInMs: 6000,
            }),
            // Layer 2 — traversal. Telemetry, nothing to tune.
            iceTraversalDetector: detectorDefault(monitorConfig.iceTraversalDetector, {}),
            // Layer 3 — path establishment: slow, then demonstrably failed.
            icePathEstablishmentDetector: detectorDefault(monitorConfig.icePathEstablishmentDetector, {
                thresholdInMs: 5000,
                createEvent: true,
            }),
            iceEstablishmentFailedDetector: detectorDefault(monitorConfig.iceEstablishmentFailedDetector, {
                thresholdInMs: 15000,
            }),
            // Layer 4 — secure transport. `failed` is terminal, so no threshold.
            dtlsHandshakeFailedDetector: detectorDefault(monitorConfig.dtlsHandshakeFailedDetector, {}),
            dtlsHandshakeStalledDetector: detectorDefault(monitorConfig.dtlsHandshakeStalledDetector, {
                stalledThresholdInMs: 6000,
            }),
            // Layer 5 — path continuity: down, finished, delivering nothing,
            // or never settling.
            iceDisconnectedDetector: detectorDefault(monitorConfig.iceDisconnectedDetector, {
                disconnectedThresholdInMs: 5000,
            }),
            iceConnectionFailedDetector: detectorDefault(monitorConfig.iceConnectionFailedDetector, {}),
            iceTransportStalledDetector: detectorDefault(monitorConfig.iceTransportStalledDetector, {
                transportStallThresholdInMs: 5000,
            }),
            unstableIcePathDetector: detectorDefault(monitorConfig.unstableIcePathDetector, {
                pathSwitchWindowInMs: 30000,
                pathSwitchThreshold: 3,
            }),
            // Connectivity telemetry. Recommendation thresholds sit wider than
            // the issue thresholds beside them, on purpose.
            iceRestartDetector: detectorDefault(monitorConfig.iceRestartDetector, {
                createEvent: true,
            }),
            iceRestartRecommendationDetector: detectorDefault(monitorConfig.iceRestartRecommendationDetector, {
                createEvent: true,
                iceRestartRecommendationThresholdInMs: 10000,
                iceRestartRecommendationCooldownInMs: 15000,
                restartRecommendationThresholdInMs: 10000,
                restartRecommendationCooldownInMs: 15000,
            }),
            // Transport Quality — the properties of a working path. These
            // thresholds are starting points, meant to be tuned against a fleet.
            // Deprecated, on by default so integrations built against the `congestion` event keep
            // working. Set to `null` once nothing depends on it.
            congestionDetector: detectorDefault(monitorConfig.congestionDetector, {
                sensitivity: 'medium' as const,
            }),
            uplinkCongestionDetector: detectorDefault(monitorConfig.uplinkCongestionDetector, {
                minSeverity: 0.65,
                // Four times the connection's own median pacer delay tops the scale.
                pacerBloatingSaturatesAt: 4,
            }),
            downlinkCongestionDetector: detectorDefault(monitorConfig.downlinkCongestionDetector, {
                minSeverity: 0.65,
                // Four times the connection's own median jitter buffer delay tops the scale.
                bufferBloatingSaturatesAt: 4,
            }),
            transportDelayDetector: detectorDefault(monitorConfig.transportDelayDetector, {
                // ~300ms round trip is where turn-taking starts to break down.
                thresholdInMs: 300,
                recoveryThresholdInMs: 200,
                // The sustain lives in `peerConnectionWindow`, not here.
            }),
            transportLossDetector: detectorDefault(monitorConfig.transportLossDetector, {
                threshold: 0.05,
                recoveryThreshold: 0.01,
                durationInMs: 6000,
            }),
            blockedStunRequestsDetector: detectorDefault(monitorConfig.blockedStunRequestsDetector, {
                responseReceivedTimeoutInMs: 10000,
                requestsSentTimeoutInMs: 10000,
            }),
            blockedOutboundMediaDetector: detectorDefault(monitorConfig.blockedOutboundMediaDetector, {
                thresholdInMs: 10000,
            }),
            // Defaults to `null`: its premise fails wherever rtcp-mux is in
            // force, which is every browser. See `ClientMonitorConfig`.
            blockedInboundMediaDetector: detectorDefault(monitorConfig.blockedInboundMediaDetector, null),
            // Pipeline Disruption — the send chain, from the capture device to
            // the wire.
            captureSourceLostDetector: detectorDefault(monitorConfig.captureSourceLostDetector, {
                createEvent: true,
            }),
            silentAudioSourceDetector: detectorDefault(monitorConfig.silentAudioSourceDetector, {
                silenceThresholdInMs: 60000,
                silenceRmsThreshold: 0.0001,
                recoveryRmsThreshold: 0.0003,
            }),
            videoCaptureBottleneckDetector: detectorDefault(monitorConfig.videoCaptureBottleneckDetector, {
                produceDegradationThreshold: 0.2,
            }),
            encoderBottleneckDetector: detectorDefault(monitorConfig.encoderBottleneckDetector, {
                encodeDegradationThreshold: 0.3,
            }),
            rtpSenderStalledDetector: detectorDefault(monitorConfig.rtpSenderStalledDetector, {
                thresholdInMs: 4000,
            }),
            dryOutboundTrackDetector: detectorDefault(monitorConfig.dryOutboundTrackDetector, {
                thresholdInMs: 5000,
            }),
            // Pipeline Disruption — the receive chain, from the transport to the
            // renderer.
            transportDemuxStalledDetector: detectorDefault(monitorConfig.transportDemuxStalledDetector, {
                thresholdInMs: 4000,
                minTransportReceiveBitrateBps: 20000,
            }),
            dryInboundTrackDetector: detectorDefault(monitorConfig.dryInboundTrackDetector, {
                thresholdInMs: 5000,
            }),
            frameAssemblyStalledDetector: detectorDefault(monitorConfig.frameAssemblyStalledDetector, {
                thresholdInMs: 3000,
                minPacketsReceived: 20,
            }),
            decoderBottleneckDetector: detectorDefault(monitorConfig.decoderBottleneckDetector, {
                // 0.1 is the old decodeFpsRatioThreshold of 0.9, read as a shortfall.
                decodeDegradationThreshold: 0.1,
                minReceivedFps: 5,
            }),
            decoderPerformanceDetector: detectorDefault(monitorConfig.decoderPerformanceDetector, {
                decodeTimeBudgetRatio: 0.8,
                minFramesReceived: 10,
                quietLossThreshold: 0.02,
                minConsecutiveTicks: 2,
            }),
            stuckDecoderDetector: detectorDefault(monitorConfig.stuckDecoderDetector, {
                thresholdInMs: 4000,
                rttMultiplier: 15,
                minBitrate: 10000,
                minPliCount: 2,
            }),
            playoutDiscrepancyDetector: detectorDefault(monitorConfig.playoutDiscrepancyDetector, {
                lowSkewRatio: 0.1,
                highSkewRatio: 0.25,
                minFramesReceived: 10,
            }),
            // Pipeline Disruption — the repair loop beside the receive chain, and
            // the machine behind both chains.
            videoRecoveryFailedDetector: detectorDefault(monitorConfig.videoRecoveryFailedDetector, {
                recoveryFailedThresholdInMs: 5000,
                recoveryFailedMinPliCount: 2,
            }),
            cpuPerformanceDetector: detectorDefault(monitorConfig.cpuPerformanceDetector, {
                utilizationThreshold: 0.5,
                recoveryThreshold: 0.4,
            }),
            // Perceived Quality — how the picture and the sound come across.
            pixelatedVideoDetector: detectorDefault(monitorConfig.pixelatedVideoDetector, {
                // Fractions of the codec's own quantizer scale, so one pair covers every codec.
                // 0.62 is a mean quantizer of 79 on VP8 and 32 on H.264, either of which is
                // visibly coarse; 0.52 is 66 and 27, which is not. Starting points to calibrate
                // against a fleet, not findings.
                threshold: 0.62,
                recoveryThreshold: 0.52,
                durationInMs: 8000,
            }),
            inboundVideoFlowStateDetector: detectorDefault(monitorConfig.inboundVideoFlowStateDetector, {
                frozenAfterInMs: 2000,
                minFreezeCountForChoppy: 2,
                // The stretch both verdicts are measured over is the track's shared window, not a
                // duration here: see `inboundTrackWindow`.
            }),
            inventedSpeechDetector: detectorDefault(monitorConfig.inventedSpeechDetector, {
                // Share of concealed audio tolerated before it counts against the budget.
                allowedInventedRatio: 0.05,
                // Invented audio beyond the allowance, in ms, that opens the issue.
                raiseAfterInventedMs: 400,
            }),
            audioPlayoutSynthesisDetector: detectorDefault(monitorConfig.audioPlayoutSynthesisDetector, {
                // A share of what was played, not a duration per collection. The previous
                // `minSynthesizedSamplesDuration: 0` reported on every tick that concealed anything
                // at all, and its unit was seconds while the config documented milliseconds.
                synthesizedRatioThreshold: 0.05,
                createEvent: true,
            }),
            // Raise at the acceptability limits, resolve back inside the
            // detectability ones; audio behind video is forgiven further.
            avDesyncPlayoutDetector: detectorDefault(monitorConfig.avDesyncPlayoutDetector, {
                audioAheadRaiseInMs: 90,
                audioAheadResolveInMs: 45,
                audioBehindRaiseInMs: 185,
                audioBehindResolveInMs: 125,
                sustainForInMs: 3000,
            }),
            jitterBufferStressDetector: detectorDefault(monitorConfig.jitterBufferStressDetector, {
                targetDelayThresholdInMs: 200,
                timeStretchThreshold: 0.02,
                minConsecutiveTicks: 2,
                // Severity scale only, and absolute rather than relative to the thresholds above:
                // a second of buffering makes conversation impossible, and a seventh of the samples
                // warped is badly distorted speech. The thresholds land near 0.16 on that scale.
                unbearableTargetDelayInMs: 1000,
                unbearableTimeStretchRate: 0.15,
            }),
            // Telemetry — facts about the session, not faults.
            captureTrackMutedDetector: detectorDefault(monitorConfig.captureTrackMutedDetector, {
                createEvent: true,
            }),
            codecChangeDetector: detectorDefault(monitorConfig.codecChangeDetector, {
                createEvent: true,
            }),
            videoResolutionChangeDetector: detectorDefault(monitorConfig.videoResolutionChangeDetector, {
                createEvent: true,
            }),
            simulcastLayerDetector: detectorDefault(monitorConfig.simulcastLayerDetector, {
                createEvent: true,
            }),
            statsGapDetector: detectorDefault(monitorConfig.statsGapDetector, {
                gapRatioThreshold: 2,
                minGapInMs: 5000,
                createEvent: true,
            }),

            bufferingEventsForSamples: monitorConfig.bufferingEventsForSamples ?? false,
            bufferClientSamplesUntilSubscriber: monitorConfig.bufferClientSamplesUntilSubscriber ?? false,
            sendResolvedIssuesToServer: monitorConfig.sendResolvedIssuesToServer ?? true,
            sendScoreReasonsToServer: monitorConfig.sendScoreReasonsToServer ?? true,
            sendIceTransportMetadataOnChangeOnly: monitorConfig.sendIceTransportMetadataOnChangeOnly ?? true,
            appData: monitorConfig.appData ?? {} as AppData,
        }

        this.slicedWindow = new SlicedWindow({
            maxAllowedGapInMs: this.config.clientWindow.maxAllowedGapInMs,
            totals: {
                totalVideoEncodeTimeInMs: null,
                totalVideoDecodeTimeInMs: null,
            },
            slices: {
                detection: {
                    numberOfSamples: this.config.clientWindow.numberOfSamples.detection,
                },
                recovery: {
                    numberOfSamples: this.config.clientWindow.numberOfSamples.recovery,
                    offset: this.config.clientWindow.numberOfSamples.detection,
                },
            },
        });

        this._sources = new Sources(this, this.logger);
        this.scoreCalculator = new DefaultScoreCalculator(this);
        this.setCollectingPeriod(this.config.collectingPeriodInMs);
        if (this.config.samplingPeriodInMs) {
            this.setSamplingPeriod(this.config.samplingPeriodInMs);
        }

        if (this.config.addClientJointEventOnCreated === true) {
            this.addClientJoinEvent();
        }
        if (this.config.integrateNavigatorMediaDevices) {
            this._sources.watchNavigatorMediaDevices();
        }
        if (this.config.watchTabVisibility) {
            this._sources.watchTabVisibility();
        }
        if (this.config.bufferClientSamplesUntilSubscriber) {
            this._bufferedClientSamples = [];
        }
        try {
            this._sources.fetchUserAgentData();
        } catch (err) {
            this.logger.error(`[${MODULE_NAME}]:`, 'Failed to fetch user agent data', err);
        }

        // The terminal registry, built before any detector so a detector's constructor can
        // reach it. Its uplink is not another registry but the sink that emits the events and
        // buffers entries into the ClientSample — which is what makes this the end of the chain.
        this.activeIssues = new IssueRegistry({
            notify: (issue) => this.addIssue(issue),
            raise: (input) => this._raiseIssue(input),
            update: (input) => this._updateIssue(input),
            resolve: (input) => this._resolveIssue(input),
        });

        this.detectors = new Detectors();
        if (this.config.cpuPerformanceDetector !== null) {
            this.detectors.add(new CpuPerformanceDetector(this));
        }
        if (this.config.statsGapDetector !== null) {
            this.detectors.add(new StatsGapDetector(this));
        }
    }
```
### AVDesyncPlayoutDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/AVDesyncPlayoutDetector.ts#L60)
Category: Perceived Quality
```ts
import { Detector } from "./Detector";
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";

/** Which way the two tracks have drifted apart. */
export type AVDesyncDirection = 'audio-ahead' | 'audio-behind';

export type AVDesyncPlayoutIssuePayload = {
	peerConnectionId: string;
	trackId: string;
	/** The video track this audio track was compared against. */
	linkedVideoTrackId: string;
	/** Signed skew in milliseconds: positive means audio is ahead of video. */
	playoutDiffInMs: number;
	direction: AVDesyncDirection;
	/** How long the skew stayed past the raise threshold, from stats timestamps. */
	sustainedForInMs: number;
	durationInMs?: number;
}

export type AVDesyncPlayoutDetectorConfig = {
	/**
	 * Raise and resolve thresholds per direction, in ms. Audio ahead is far less forgivable than
	 * audio behind, so each direction gets its own pair.
	 */
	audioAheadRaiseInMs: number;
	audioAheadResolveInMs: number;
	audioBehindRaiseInMs: number;
	audioBehindResolveInMs: number;

	/** Stats time the skew must hold past the raise threshold before opening, in ms. */
	sustainForInMs: number;
}

/**
 * Reports a speaker's voice and their lips coming apart — one participant's audio and video playing
 * out at measurably different points in the sender's timeline. Use it to tell lip-sync drift apart
 * from either track simply being late or stuttering on its own.
 *
 * A finding usually means the two tracks were buffered differently on the way here: one path
 * degraded while the other did not, or the audio buffer grew to cover jitter while video kept
 * rendering. The sign says which is ahead, which is what tells a lagging picture from lagging sound.
 *
 * It subtracts the two tracks' `estimatedPlayoutTimestamp` values, which are both already on the
 * sender's NTP clock and so compare directly. The pairing is the application's to declare through
 * `linkedVideoTrackId`; until it does, the detector measures nothing and says so through
 * `inputsUnavailable`, since a guessed pairing would give a confidently wrong number. Each direction
 * has its own raise and resolve thresholds, and the payload names which one fired.
 *
 * `estimatedPlayoutTimestamp` is thinly implemented and extrapolated between sender reports, so this
 * says nothing about desync that begins during a freeze, and reports `inputsUnavailable` rather than
 * health where the browser omits it.
 *
 * Issue raised: `av-desync`. Monitor event: `av-desync`.
 * Config: `avDesyncPlayoutDetector`.
 *
 * Category: Perceived Quality
 * Layer: Synchronization
 *
 */
export class AVDesyncPlayoutDetector implements Detector {
	public static readonly ISSUE_TYPE = 'av-desync';
	public readonly name = 'av-desync-playout-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	private readonly issueKey: string;
	private _sustainedForInMs = 0;
	private _raised = false;
	private _startedAt?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this.issueKey = `${AVDesyncPlayoutDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private get config() {
		return this.peerConnection.parent.config.avDesyncPlayoutDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) return;

		const inboundRtp = this.trackMonitor.getInboundRtp();

		if (!inboundRtp || inboundRtp.kind !== 'audio') return;

		if (this.trackMonitor.readyState !== 'live') {
			this._sustainedForInMs = 0;

			return this._raised ? this._resolve('track ended') : undefined;
		}
		if (this.trackMonitor.paused || this.trackMonitor.remoteOutboundTrackPaused) {
			this._sustainedForInMs = 0;

			return this._raised ? this._resolve('track paused') : undefined;
		}

		const diffInMs = this.trackMonitor.linkedVideoPlayoutDiffInMs;

		if (diffInMs === undefined) {
			// No pairing declared, or a timestamp missing — unmeasurable, not in sync.
			this.inputsUnavailable = true;
			this._sustainedForInMs = 0;

			return;
		}

		this.inputsUnavailable = false;

		const raiseAt = 0 < diffInMs
			? this.config.audioAheadRaiseInMs
			: this.config.audioBehindRaiseInMs;
		const resolveAt = 0 < diffInMs
			? this.config.audioAheadResolveInMs
			: this.config.audioBehindResolveInMs;
		const skewInMs = Math.abs(diffInMs);

		if (skewInMs < resolveAt) {
			this._sustainedForInMs = 0;

			if (this._raised) this._resolve('tracks back in sync');

			return;
		}

		// Between the thresholds nothing changes — the band is what stops flapping.
		if (skewInMs < raiseAt) return;

		this._sustainedForInMs += inboundRtp.deltaTime ?? 0;

		if (this._raised) return;
		if (this._sustainedForInMs < this.config.sustainForInMs) return;

		const direction: AVDesyncDirection = 0 < diffInMs ? 'audio-ahead' : 'audio-behind';
		const linkedVideoTrackId = this.trackMonitor.getLinkedVideoTrack()?.track.id;

		if (linkedVideoTrackId === undefined) return;

		this._raised = true;
		this._startedAt = Date.now();

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('av-desync', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			linkedVideoTrackId,
			playoutDiffInMs: diffInMs,
			direction,
		});

		this.trackMonitor.issues.raise({
			key: this.issueKey,
			includeInSample: this.includeIssueInSample,
			type: AVDesyncPlayoutDetector.ISSUE_TYPE,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				linkedVideoTrackId,
				playoutDiffInMs: diffInMs,
				direction,
				sustainedForInMs: this._sustainedForInMs,
			},
		});
	}

	private _resolve(comment: string) {
		this._raised = false;

		const issue = this.trackMonitor.issues.get(this.issueKey);
		let payload: AVDesyncPlayoutIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as AVDesyncPlayoutIssuePayload),
				durationInMs: this._startedAt ? Date.now() - this._startedAt : undefined,
			};
		}

		this.trackMonitor.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedAt = undefined;
	}
}

```
### AudioPlayoutSynthesisDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/AudioPlayoutSynthesisDetector.ts#L115)
Category: Perceived Quality
```ts
import type { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";
import { ClientEventTypes } from "../schema/ClientEventTypes";
import { Detector } from "./Detector";

/**
 * What the detector measured about the playout device in the window that raised the issue.
 *
 * Every field not marked optional is always present: the detector cannot reach the raise without it.
 */
export type AudioPlayoutSynthesisIssuePayload = {
	peerConnectionId: string;
	trackId: string;

	/**
	 * The share of playout the browser fabricated over the detection window,
	 * `synthesizedForDetectionInMs / playedOutForDetectionInMs`. Zero is audio played entirely from
	 * received packets; one is a device with nothing real left to play at all.
	 */
	synthesizedRatio: number;

	/** The milliseconds of audio the browser synthesized over the detection window. */
	synthesizedForDetectionInMs: number;

	/** The milliseconds of audio the device played over the detection window, synthesized included. */
	playedOutForDetectionInMs: number;

	/** The milliseconds of stats time the detection window spanned. */
	detectionWindowInMs: number;

	/**
	 * How many separate stretches of concealment the browser reported over the detection window.
	 * A handful at a given ratio is a few long dropouts; hundreds is constant micro-concealment,
	 * which sounds different and usually has a different cause.
	 */
	synthesisEvents?: number;

	/** The average delay from a sample being ready to being played, over the detection window. */
	playoutDelayPerSampleInMs?: number;

	// Written at resolution, from the recovery window that ended the issue. Absent when it was
	// resolved by a stand-down instead, where nothing was measured.

	/** The milliseconds of stats time the recovery window spanned. */
	recoveryWindowInMs?: number;

	/** The share of playout that was fabricated during the recovery window. */
	synthesizedRatioForRecovery?: number;

	/** The milliseconds of audio the browser synthesized during the recovery window. */
	synthesizedForRecoveryInMs?: number;

	/** The milliseconds of audio the device played during the recovery window. */
	playedOutForRecoveryInMs?: number;
}

export type AudioPlayoutSynthesisIssueType = 'synthesized-audio';

export type AudioPlayoutSynthesisDetectorConfig = {
	/** Also add a client event to the monitor when the issue opens. Default true. */
	createEvent?: boolean

	/**
	 * The share of playout that may be synthesized before the issue is raised, and must return to
	 * before it resolves.
	 */
	synthesizedRatioThreshold: number;
}

/**
 * Reports concealment audio the browser synthesized when the jitter buffer had nothing real left to
 * play — robotic, warbling or stretched speech as the listener hears it. Use it to see degradation
 * that packet statistics hide: concealment is the audio stack succeeding at keeping playback
 * continuous, so nothing upstream reports it as a failure.
 *
 * It runs on each inbound audio track and reads the playout device that track's RTP feeds, reached
 * as `getInboundRtp().getMediaPlayout()`. Several tracks can share one device, so on a call with
 * several talkers the same concealment is reported against each of their tracks — which is the
 * honest reading, because every one of those streams is what the listener heard through it.
 * `InventedSpeechDetector` sits alongside on the same track and answers a narrower question: how
 * much of *that stream* was invented. This one answers what the output device did.
 *
 * Both counters reach it through `InboundTrackMonitor.slicedWindow`, which carries the
 * playout totals alongside the track's own so every detector on the track judges the same stretch.
 * The verdict is a
 * **share of what was played**, never a duration per collection. An absolute per-tick threshold
 * makes the same fault read differently depending on how often stats are collected — twice the
 * collecting period is twice the synthesized milliseconds for identical audio. A ratio over a
 * window is free of that.
 *
 * The detection window raises, every later collection still over the threshold updates that issue
 * rather than opening another, and the recovery window resolves — so a buffer hovering at the line
 * cannot flap one bad minute into a stream of short reports. Neither window is read before it says
 * it is ready.
 *
 * A high share means the buffer kept running dry: loss or jitter on some inbound path, or a machine
 * too busy to feed the audio device on time. It says the listener's experience was damaged, not
 * which stream damaged it — `synthesisEvents` distinguishes a few long dropouts from constant
 * micro-concealment.
 *
 * It stands down when the window holds no playout to take a share of, which is a device that played
 * no audio at all rather than one that played fabricated audio.
 *
 * **Chromium only.** Firefox and WebKit produce no `media-playout` reports at all, so this raises
 * nothing there — absence of the issue on those browsers is absence of measurement, not health.
 *
 * Issue raised: `synthesized-audio`, on the inbound audio track, updated while it stays open and
 * resolved on recovery. Monitor event: `synthesized-audio`, emitted once at the raise; client event
 * `EXCESSIVE_SYNTHESIZED_AUDIO` alongside it when `createEvent` is left on.
 * Config: `audioPlayoutSynthesisDetector`.
 *
 * Category: Perceived Quality
 * Layer: Audio — naturalness
 *
 */
export class AudioPlayoutSynthesisDetector implements Detector {
	public static readonly ISSUE_TYPE: AudioPlayoutSynthesisIssueType = 'synthesized-audio';

	public readonly name = 'audio-playout-synthesis-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _issueKey: string;
	private _raised = false;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this._issueKey = `${AudioPlayoutSynthesisDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;

		// Read without the getter's non-null assertion: a monitor builds this detector whenever the
		// key is not explicitly `null`, which includes a config that never mentioned it at all.
		const config = this.peerConnection.parent.config.audioPlayoutSynthesisDetector;

		if (config && config.synthesizedRatioThreshold < 0) {
			this.peerConnection.parent.logger.warn(
				'audioPlayoutSynthesisDetector.synthesizedRatioThreshold must not be below 0, got '
				+ config.synthesizedRatioThreshold
			);
			config.synthesizedRatioThreshold = 0;
		}
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	private get config() {
		return this.peerConnection.parent.config.audioPlayoutSynthesisDetector!;
	}

	public update() {
		if (this.disabled) return;
		if (this.trackMonitor.kind !== 'audio') return;

		// A track that ended plays out nothing; there is no synthesis to take a share of.
		if (this.trackMonitor.readyState !== 'live') {
			this.trackMonitor.synthesizedAudioRatio = undefined;

			return this._clear('track ended');
		}

		const {
			detection: detectionWindow,
			recovery: recoveryWindow,
		} = this.trackMonitor.slicedWindow.slices;
		const synthesizedForDetectionInMs = detectionWindow.deltaTotalPlayoutSynthesizedDurationInMs;
		const playedOutForDetectionInMs = detectionWindow.deltaTotalPlayoutSamplesDurationInMs;
		const detectionWindowInMs = detectionWindow.durationInMs;

		// Both stand-downs blank the measurement as well as resolving: nothing was measured, which
		// is not the same as measuring nothing.
		if (synthesizedForDetectionInMs === null || playedOutForDetectionInMs === null) {
			this.trackMonitor.synthesizedAudioRatio = undefined;

			return this._clear('no playout measurement');
		}
		if (!detectionWindow.isReady || detectionWindowInMs < 1) return;

		// Nothing played is nothing to take a share of. A device that played no audio at all is not
		// a device playing fabricated audio.
		if (playedOutForDetectionInMs <= 0) {
			this.trackMonitor.synthesizedAudioRatio = undefined;

			return this._clear('nothing played out');
		}

		const synthesizedRatio = synthesizedForDetectionInMs / playedOutForDetectionInMs;

		// Beside the issue: the measurement itself, on every judged collection, so the score
		// calculator has a continuous number below the threshold as well as above it.
		this.trackMonitor.synthesizedAudioRatio = synthesizedRatio;

		if (this.config.synthesizedRatioThreshold < synthesizedRatio) {
			if (!this._raised) return this._raiseIssue({
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				synthesizedRatio,
				synthesizedForDetectionInMs,
				playedOutForDetectionInMs,
				detectionWindowInMs,
				synthesisEvents: detectionWindow.deltaTotalPlayoutSynthesisEvents ?? undefined,
				playoutDelayPerSampleInMs: this._playoutDelayPerSample(),
			});

			return void this.trackMonitor.issues.update({
				key: this._issueKey,
				payload: {
					synthesizedRatio,
				},
			});
		}

		if (!this._raised) return;

		// Below the threshold with a finding open: the recovery window decides whether it ends.

		const synthesizedForRecoveryInMs = recoveryWindow.deltaTotalPlayoutSynthesizedDurationInMs;
		const playedOutForRecoveryInMs = recoveryWindow.deltaTotalPlayoutSamplesDurationInMs;
		const recoveryWindowInMs = recoveryWindow.durationInMs;

		if (
			!recoveryWindow.isReady ||
			synthesizedForRecoveryInMs === null ||
			playedOutForRecoveryInMs === null ||
			playedOutForRecoveryInMs <= 0 ||
			recoveryWindowInMs < 1
		) {
			return void this.trackMonitor.issues.update({
				key: this._issueKey,
				payload: {
					synthesizedRatio,
				},
			});
		}

		const synthesizedRatioForRecovery = synthesizedForRecoveryInMs / playedOutForRecoveryInMs;

		if (this.config.synthesizedRatioThreshold < synthesizedRatioForRecovery) {
			return void this.trackMonitor.issues.update({
				key: this._issueKey,
				payload: {
					synthesizedRatio,
				},
			});
		}

		this._clear('playout recovered', {
			synthesizedRatioForRecovery,
			synthesizedForRecoveryInMs,
			playedOutForRecoveryInMs,
			recoveryWindowInMs,
		});
	}

	/** The average per-sample delay across the detection window, from the two totals that define it. */
	private _playoutDelayPerSample(): number | undefined {
		const { detection: detectionWindow } = this.trackMonitor.slicedWindow.slices;
		const delayInMs = detectionWindow.deltaTotalPlayoutDelayInMs;
		const samples = detectionWindow.deltaTotalPlayoutSamplesCount;

		if (delayInMs === null || samples === null || samples <= 0) return undefined;

		return delayInMs / samples;
	}

	private _raiseIssue(payload: AudioPlayoutSynthesisIssuePayload) {
		if (this._raised) return;

		this._raised = true;

		const clientMonitor = this.peerConnection.parent;
		// The window can still hold playout totals on a collection where the RTP stopped naming its
		// playout id, so the event is skipped rather than the finding withheld.
		const mediaPlayoutMonitor = this.trackMonitor.getInboundRtp()?.getMediaPlayout();

		if (mediaPlayoutMonitor) {
			clientMonitor.emit('synthesized-audio', {
				mediaPlayoutMonitor,
				trackMonitor: this.trackMonitor,
				clientMonitor: clientMonitor,
			});
		}

		if (this.config.createEvent !== false) {
			clientMonitor.addEvent({
				type: ClientEventTypes.EXCESSIVE_SYNTHESIZED_AUDIO,
				payload: {
					synthesizedRatio: payload.synthesizedRatio,
					synthesizedForDetectionInMs: payload.synthesizedForDetectionInMs,
					playedOutForDetectionInMs: payload.playedOutForDetectionInMs,
				},
			});
		}

		this.trackMonitor.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: AudioPlayoutSynthesisDetector.ISSUE_TYPE,
			payload,
			timestamp: Date.now(),
		});
	}

	private _clear(
		comment: string,
		payload?: Pick<AudioPlayoutSynthesisIssuePayload,
			'synthesizedRatioForRecovery' | 'synthesizedForRecoveryInMs' |
			'playedOutForRecoveryInMs' | 'recoveryWindowInMs'>,
	) {
		if (!this._raised) return;

		this._raised = false;

		this.trackMonitor.issues.resolve({
			key: this._issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});
	}
}

```
### BlockedInboundMediaDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/BlockedInboundMediaDetector.ts#L58)
Category: Transport Quality
```ts
import type { IcePathKind } from "../monitors/IceCandidatePairMonitor";
// Type-only: the monitor imports this detector, so a value import would close the cycle at runtime.
import type { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import type { Detector } from "./Detector";

export type BlockedInboundMediaIssuePayload = {
	peerConnectionId: string;
	/** The selected pair's path kind. Without BUNDLE, the first selected pair is reported. */
	pathKind?: IcePathKind;
	/** How long the far end's media had been failing to arrive when the issue was raised, in stats time. */
	blockedForMs: number;
	/** Packets the far end reported sending during that window, in reports that actually arrived. */
	remotePacketsSent: number;
	/** Filled in when the issue is resolved. */
	durationInMs?: number;
};

const ISSUE_TYPE = 'blocked-inbound-media-transport';

export type BlockedInboundMediaDetectorConfig = {
	/**
	 * How long the far end may claim to send while nothing arrives, in ms of stats time. Must outlast
	 * one RTCP reporting interval, or a quiet gap between reports reads as a block.
	 */
	thresholdInMs: number;
}

/**
 * The far end's media never reaches us while it is still telling us it sends: sender reports keep
 * arriving with a rising packet count, and our receivers take nothing off the wire. Use it to prove
 * an inbound block outright, rather than inferring one from a dry track.
 *
 * A finding means something on the path is discarding the far end's media specifically — a
 * middlebox or firewall passing signalling and dropping RTP — rather than the far end having
 * stopped. It is the strongest inbound evidence available, because the sender is still testifying.
 *
 * It is the one detector not registered unless you ask for it, because it only fires where RTCP
 * survives what killed the media. With `rtcp-mux` — which browsers now require — the far end's
 * sender reports die with its media, leaving the reading indistinguishable from a paused peer.
 * Setting `blockedInboundMediaDetector` opts in for endpoints where RTCP rides its own path.
 *
 * A claim counts only on the collection it arrives in: `getStats()` keeps serving the last
 * `remote-outbound-rtp` in between, so a positive `deltaTime` is what separates a live claim from a
 * frozen one still testifying for a sender that stopped. Quiet collections are expected, so the
 * window needs only some live claim across it. Every clock is the connection's own `deltaTime`.
 *
 * It stands down while `blockedTransport` is set, counts only streams with a linked remote report,
 * and sets `inputsUnavailable` where inbound streams carry no remote report at all.
 *
 * Issue raised: `blocked-inbound-media-transport`. Monitor event:
 * `blocked-inbound-media-transport`. Config: `blockedInboundMediaDetector` — unset leaves the
 * detector unregistered.
 *
 * Category: Transport Quality
 * Layer: Delivery reliability
 *
 */
export class BlockedInboundMediaDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'blocked-inbound-media-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	/** Stats time the far end's media has been failing to arrive, or `undefined` while it arrives. */
	private _blockedForInMs?: number;
	/** Packets the far end claimed, in reports that actually arrived during that window. */
	private _remotePacketsSent = 0;
	/** Wall clock, and only for the resolved issue's `durationInMs`. */
	private _raisedAt?: number;

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.blockedInboundMediaDetector!;
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) return;

		const pairs = this.peerConnection.selectedIceCandidatePairs.filter((pair) => pair.state === 'succeeded');
		const deltaTime = this.peerConnection.deltaTime ?? 0;

		this.inputsUnavailable = false;

		if (pairs.length === 0) {
			return this._blockedForInMs !== undefined ? this._clear('ice has not verified any path') : undefined;
		}

		// A path that answers no STUN carries nothing: the fault is the path, not the media.
		if (this.peerConnection.blockedTransport) {
			return this._blockedForInMs !== undefined ? this._clear('the transport is blocked') : undefined;
		}

		// Nothing negotiated to receive is nothing to judge — a send-only connection.
		if (this.peerConnection.inboundRtps.length === 0) {
			return this._blockedForInMs !== undefined ? this._clear('nothing is being received on this connection') : undefined;
		}

		let packetsReceived = 0;
		let remotePacketsSent = 0;
		let reportsExist = false;
		let claimArrived = false;

		for (const inboundRtp of this.peerConnection.inboundRtps) {
			const remote = inboundRtp.getRemoteOutboundRtp();

			if (!remote) continue;

			reportsExist = true;
			packetsReceived += inboundRtp.deltaPacketsReceived ?? 0;

			// Only a report that arrived on this collection says anything about now.
			if ((remote.deltaTime ?? 0) < 1 || remote.deltaPacketsSent === undefined) continue;

			claimArrived = true;
			remotePacketsSent += remote.deltaPacketsSent;
		}

		if (!reportsExist) {
			this.inputsUnavailable = true;

			return this._blockedForInMs !== undefined ? this._clear('the far end reports nothing it sent') : undefined;
		}

		if (0 < packetsReceived) {
			return this._blockedForInMs !== undefined ? this._clear('media is arriving again') : undefined;
		}

		// A live report claiming nothing agrees with our silence: a paused producer, not a block.
		if (claimArrived && remotePacketsSent < 1) {
			return this._blockedForInMs !== undefined ? this._clear('the far end is not sending') : undefined;
		}

		this._blockedForInMs = (this._blockedForInMs ?? 0) + deltaTime;
		this._remotePacketsSent += remotePacketsSent;

		// No live claim across the window, so nothing arriving proves nothing.
		if (this._remotePacketsSent < 1) return;

		if (this._blockedForInMs < this.config.thresholdInMs) return;
		if (this._raisedAt !== undefined) return;

		this._raisedAt = Date.now();

		const clientMonitor = this.peerConnection.parent;
		const payload: BlockedInboundMediaIssuePayload = {
			peerConnectionId: this.peerConnection.peerConnectionId,
			pathKind: pairs[0]?.pathKind,
			blockedForMs: this._blockedForInMs,
			remotePacketsSent: this._remotePacketsSent,
		};

		clientMonitor.emit('blocked-inbound-media-transport', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			...payload,
		});

		this.peerConnection.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: ISSUE_TYPE,
			payload,
		});
	}

	/** Ends the window, resolving any raised issue. Call sites test `_blockedForInMs` first. */
	private _clear(comment: string) {
		this._blockedForInMs = undefined;
		this._remotePacketsSent = 0;

		if (this._raisedAt === undefined) return;

		const issue = this.peerConnection.issues.get(this._issueKey);

		if (issue) {
			this.peerConnection.issues.resolve({
				key: this._issueKey,
				comment,
				payload: { ...issue.payload, durationInMs: Date.now() - this._raisedAt } as BlockedInboundMediaIssuePayload,
				resolvedAt: Date.now(),
			});
		}

		this._raisedAt = undefined;
	}

	private get _issueKey() {
		return `${ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}`;
	}
}

```
### BlockedOutboundMediaDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/BlockedOutboundMediaDetector.ts#L50)
Category: Transport Quality
```ts
import type { IcePathKind } from "../monitors/IceCandidatePairMonitor";
// Type-only: the monitor imports this detector, so a value import would close the cycle at runtime.
import type { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import type { Detector } from "./Detector";

export type BlockedOutboundMediaIssuePayload = {
	peerConnectionId: string;
	/** The selected pair's path kind. Without BUNDLE, the first selected pair is reported. */
	pathKind?: IcePathKind;
	/** How long no receiver report had come back when the issue was raised, in stats time. */
	blockedForMs: number;
	/** Packets our senders put on the wire during that window, none of them ever acknowledged. */
	packetsSent: number;
	/** Filled in when the issue is resolved. */
	durationInMs?: number;
};

const ISSUE_TYPE = 'blocked-outbound-media-transport';

export type BlockedOutboundMediaDetectorConfig = {
	/**
	 * How long senders may put packets on a STUN-answering path with no receiver report, in ms of
	 * stats time. Must outlast one RTCP reporting interval, or an ordinary quiet gap reads as a block.
	 */
	thresholdInMs: number;
}

/**
 * Our media leaves and nothing ever comes back about it: senders keep putting packets on a path
 * whose STUN keeps being answered, and no receiver report arrives for `thresholdInMs`. Use it to
 * name the selective block in the send direction — a middlebox that passes STUN and drops RTP —
 * as against a total block, which takes STUN with it and belongs to `BlockedStunRequestsDetector`.
 *
 * The evidence is the far end's silence rather than its numbers: with `rtcp-mux`, whatever drops
 * our media drops the reports about it, so a zero packet count is never observed. `remote-inbound-rtp`
 * carries the three-way reading — a positive `deltaTime` means a report just arrived, `0` a frozen
 * one served again, `undefined` that none ever came — and only the first clears the window. Idle
 * senders are not evidence, STUN must have answered somewhere in the window, and every clock is the
 * connection's own `deltaTime` so a delayed collection is not counted as far-end silence.
 *
 * `inputsUnavailable` is set only where our own send counters are missing: silence is a finding.
 *
 * Issue raised: `blocked-outbound-media-transport`. Monitor event:
 * `blocked-outbound-media-transport`. Config: `blockedOutboundMediaDetector`.
 *
 * Category: Transport Quality
 * Layer: Delivery reliability
 *
 */
export class BlockedOutboundMediaDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'blocked-outbound-media-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	/** Stats time no receiver report has come back, or `undefined` while they arrive. */
	private _blockedForInMs?: number;
	/** Packets we put on the wire during that window. */
	private _packetsSent = 0;
	/** Whether STUN answered at any point during the window. */
	private _stunAnswered = false;
	/** Wall clock, and only for the resolved issue's `durationInMs`. */
	private _raisedAt?: number;

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.blockedOutboundMediaDetector!;
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) return;

		const pairs = this.peerConnection.selectedIceCandidatePairs.filter((pair) => pair.state === 'succeeded');
		const deltaTime = this.peerConnection.deltaTime ?? 0;

		this.inputsUnavailable = false;

		if (pairs.length === 0) {
			return this._blockedForInMs !== undefined ? this._clear('ice has not verified any path') : undefined;
		}

		// A path that answers no STUN carries nothing: the fault is the path, not the media.
		if (this.peerConnection.blockedTransport) {
			return this._blockedForInMs !== undefined ? this._clear('the transport is blocked') : undefined;
		}

		let packetsSent = 0;
		let sendersReporting = false;
		let reportArrived = false;

		for (const outboundRtp of this.peerConnection.outboundRtps) {
			if (outboundRtp.deltaPacketsSent !== undefined) sendersReporting = true;

			const sent = outboundRtp.deltaPacketsSent ?? 0;

			// An idle sender is not evidence either way, and neither is its report.
			if (sent < 1) continue;

			packetsSent += sent;

			// A report that just arrived, not the last one served again: only its own clock says which.
			if (0 < (outboundRtp.getRemoteInboundRtp()?.deltaTime ?? 0)) reportArrived = true;
		}

		// Nothing exposes a packet count, so we cannot establish we are sending. Blind, not a verdict.
		if (!sendersReporting) {
			this.inputsUnavailable = true;

			return this._blockedForInMs !== undefined ? this._clear('our own send counters are not reported') : undefined;
		}

		// Nothing going out is nothing to judge — receive-only, or paused senders.
		if (packetsSent < 1) {
			return this._blockedForInMs !== undefined ? this._clear('no media is going out') : undefined;
		}

		if (reportArrived) {
			return this._blockedForInMs !== undefined ? this._clear('the far end is reporting again') : undefined;
		}

		this._blockedForInMs = (this._blockedForInMs ?? 0) + deltaTime;
		this._packetsSent += packetsSent;
		this._stunAnswered = this._stunAnswered || pairs.some((pair) => 0 < (pair.deltaResponsesReceived ?? 0));

		if (!this._stunAnswered) return;
		if (this._blockedForInMs < this.config.thresholdInMs) return;
		if (this._raisedAt !== undefined) return;

		this._raisedAt = Date.now();

		const clientMonitor = this.peerConnection.parent;
		const payload: BlockedOutboundMediaIssuePayload = {
			peerConnectionId: this.peerConnection.peerConnectionId,
			pathKind: pairs[0]?.pathKind,
			blockedForMs: this._blockedForInMs,
			packetsSent: this._packetsSent,
		};

		clientMonitor.emit('blocked-outbound-media-transport', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			...payload,
		});

		this.peerConnection.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: ISSUE_TYPE,
			payload,
		});
	}

	/** Ends the window, resolving any raised issue. Call sites test `_blockedForInMs` first. */
	private _clear(comment: string) {
		this._blockedForInMs = undefined;
		this._packetsSent = 0;
		this._stunAnswered = false;

		if (this._raisedAt === undefined) return;

		const issue = this.peerConnection.issues.get(this._issueKey);

		if (issue) {
			this.peerConnection.issues.resolve({
				key: this._issueKey,
				comment,
				payload: { ...issue.payload, durationInMs: Date.now() - this._raisedAt } as BlockedOutboundMediaIssuePayload,
				resolvedAt: Date.now(),
			});
		}

		this._raisedAt = undefined;
	}

	private get _issueKey() {
		return `${ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}`;
	}
}

```
### BlockedStunRequestsDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/BlockedStunRequestsDetector.ts#L52)
Category: Transport Quality
```ts
import type { IceTransportMonitor } from "../monitors/IceTransportMonitor";
import type { IcePathKind } from "../monitors/IceCandidatePairMonitor";
// Type-only: the monitor imports this detector, so a value import would close the cycle at runtime.
import type { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import type { Detector } from "./Detector";

export type BlockedTransportIssuePayload = {
	peerConnectionId: string;
	transportId: string;
	/** `direct`, `turn-udp`, `turn-tcp`, `turn-tls` or `turn-unknown`. */
	pathKind?: IcePathKind;
	/** How long the path had been answering nothing when the issue was raised, in stats time. */
	silentForMs: number;
	/** STUN requests — checks plus consent — that went out unanswered during that window. */
	requestsSent: number;
	/** Latest STUN round trip on the pair before it went silent, in seconds. */
	currentRoundTripTime?: number;
	/** Filled in when the issue is resolved. */
	durationInMs?: number;
};

const ISSUE_TYPE = 'blocked-stun-requests';

export type BlockedStunRequestsDetectorConfig = {
	/** Stats time the path may answer nothing before raising, in ms. Consent runs every ~5 s, so keep it well above that. */
	responseReceivedTimeoutInMs: number;

	/** Stats time to keep waiting while no STUN goes out at all, in ms, before standing down. */
	requestsSentTimeoutInMs: number;
}

/**
 * Reports a path that stopped answering STUN while this endpoint was still asking — the one firewall
 * signature a client can prove on its own. Use it to tell a middlebox dropping STUN, an expired NAT
 * binding or a network vanishing under the socket apart from a path that never worked at all.
 *
 * The pair must have reached `succeeded` first; a path that never answered is ordinary establishment
 * failure and belongs to `IceEstablishmentFailedDetector`. Both counters are read as interval
 * deltas, and "we asked" counts consent as well as connectivity checks, since after nomination
 * consent is the only STUN still leaving. Timing is the transport's own `deltaTime`, so a stalled
 * main thread is not counted as silence. While a finding is open the transport is marked `blocked`.
 *
 * It does not claim which cause is at work, only that the path went silent under questioning.
 *
 * Issue raised: `blocked-stun-requests`. Monitor event: `blocked-transport`. Connection attribute:
 * `PeerConnectionMonitor.blockedTransport`. Config: `blockedStunRequestsDetector`.
 *
 * Category: Transport Quality
 * Layer: Delivery reliability
 *
 */
export class BlockedStunRequestsDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'blocked-stun-requests-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	/** Stats time the path has answered nothing, or `undefined` while it is answering. */
	private _silentForInMs?: number;
	/** STUN requests that went out unanswered during that window. */
	private _requestsSentWhileSilent = 0;
	/** Wall clock, and only for the resolved issue's `durationInMs`. */
	private _raisedAt?: number;

	public constructor(
		public readonly iceTransport: IceTransportMonitor,
	) {
	}

	public get peerConnection(): PeerConnectionMonitor {
		return this.iceTransport.getPeerConnection();
	}

	private get config() {
		return this.peerConnection.parent.config.blockedStunRequestsDetector!;
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) return;

		const pair = this.iceTransport.getSelectedCandidatePair();
		const deltaTime = this.iceTransport.deltaTime ?? 0;

		this.inputsUnavailable = false;

		// Not applicable until a pair has answered once — which is not blindness, so the flag stays false.
		if (!pair || pair.state !== 'succeeded') {
			return this._silentForInMs !== undefined ? this._clear('ice has not verified this path') : undefined;
		}

		if (pair.deltaResponsesReceived === undefined) {
			this.inputsUnavailable = true;

			return this._silentForInMs !== undefined ? this._clear('stun responses are not reported') : undefined;
		}

		// Either counter alone proves some STUN went out, so only both missing is blindness.
		if (pair.deltaRequestsSent === undefined && pair.deltaConsentRequestsSent === undefined) {
			this.inputsUnavailable = true;

			return this._silentForInMs !== undefined ? this._clear('stun requests are not reported') : undefined;
		}

		if (0 < pair.deltaResponsesReceived) {
			return this._silentForInMs !== undefined ? this._clear('stun is answering again') : undefined;
		}

		this._silentForInMs = (this._silentForInMs ?? 0) + deltaTime;
		this._requestsSentWhileSilent += (pair.deltaRequestsSent ?? 0) + (pair.deltaConsentRequestsSent ?? 0);

		// Nothing has been asked for a while either, so nothing answered says nothing.
		if (this._requestsSentWhileSilent < 1) {
			return this.config.requestsSentTimeoutInMs < this._silentForInMs
				? this._clear('no stun requests are going out')
				: undefined;
		}

		if (this._silentForInMs < this.config.responseReceivedTimeoutInMs) return;
		if (this._raisedAt !== undefined) return;

		this._raisedAt = Date.now();
		this.iceTransport.blocked = true;

		const clientMonitor = this.peerConnection.parent;
		const payload: BlockedTransportIssuePayload = {
			peerConnectionId: this.peerConnection.peerConnectionId,
			transportId: this.iceTransport.id,
			pathKind: pair.pathKind,
			silentForMs: this._silentForInMs,
			requestsSent: this._requestsSentWhileSilent,
			currentRoundTripTime: pair.currentRoundTripTime,
		};

		clientMonitor.emit('blocked-transport', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			...payload,
		});

		this.iceTransport.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: ISSUE_TYPE,
			payload,
		});
	}

	/** Ends the silence window, resolving the issue if one was raised. */
	private _clear(comment: string) {
		this._silentForInMs = undefined;
		this._requestsSentWhileSilent = 0;

		if (this._raisedAt === undefined) return;

		this.iceTransport.blocked = false;

		const issue = this.iceTransport.issues.get(this._issueKey);

		if (issue) {
			this.iceTransport.issues.resolve({
				key: this._issueKey,
				comment,
				payload: { ...issue.payload, durationInMs: Date.now() - this._raisedAt } as BlockedTransportIssuePayload,
				resolvedAt: Date.now(),
			});
		}

		this._raisedAt = undefined;
	}

	private get _issueKey() {
		return `${ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}-transport-${this.iceTransport.id}`;
	}
}

```
### CaptureSourceLostDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CaptureSourceLostDetector.ts#L40)
Category: Pipeline Disruption
```ts
import { Detector } from "./Detector";
import { OutboundTrackMonitor } from "../monitors/OutboundTrackMonitor";
import { ClientEventTypes } from "../schema/ClientEventTypes";

export type CaptureSourceLostIssuePayload = {
	peerConnectionId: string;
	trackId: string;
	kind: string;
	deviceLabel?: string;
}
export type CaptureSourceLostIssueType = 'capture-source-lost';

export type CaptureSourceLostDetectorConfig = {
	/** Also buffer a `CAPTURE_SOURCE_LOST` client event into the sample. Default true. */
	createEvent?: boolean;
}

/**
 * Reports the capture device behind an outbound track being taken away: a webcam unplugged, a
 * headset that dropped its link, a screen share the user stopped, a permission revoked. Use it to
 * explain a track that went quiet for a reason no transport or encoder statistic can show — the
 * counters simply stop advancing, and the track object is the only place the reason is written down.
 *
 * The single input is `OutboundTrackMonitor.sourceEnded`, set from the track's `ended` event, which
 * fires when the source goes away and never for the application's own `stop()`. The loss is
 * terminal, so this is a one-shot `addIssue` rather than a condition to later resolve.
 *
 * It does not claim the track was live: a device unplugged during a pause is still a fact about the
 * device.
 *
 * Reports `capture-source-lost`. Emits `capture-source-lost`, plus the
 * `CAPTURE_SOURCE_LOST` client event unless `createEvent` is false.
 * Config: `captureSourceLostDetector`.
 * Track attribute: `OutboundTrackMonitor.lostCaptureSource`.
 *
 * Category: Pipeline Disruption
 * Layer: Send — the source
 *
 */
export class CaptureSourceLostDetector implements Detector {
	public static readonly ISSUE_TYPE: CaptureSourceLostIssueType = 'capture-source-lost';

	public readonly name = 'capture-source-lost-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private _reported = false;

	public constructor(
		public readonly trackMonitor: OutboundTrackMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.captureSourceLostDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) {
			this.trackMonitor.lostCaptureSource = undefined;

			return;
		}
		if (this._reported) return;

		// Not `track.readyState`: a lost device and the application's own `stop()` both leave it `ended`.
		if (this.trackMonitor.sourceEnded === false) {
			this.trackMonitor.lostCaptureSource = false;

			return;
		}

		this._reported = true;
		// Terminal: a device that went away never comes back to `false`.
		this.trackMonitor.lostCaptureSource = true;

		const track = this.trackMonitor.track;
		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('capture-source-lost', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
		});

		const payload: CaptureSourceLostIssuePayload = {
			peerConnectionId: this.peerConnection.peerConnectionId,
			trackId: track.id,
			kind: track.kind,
			deviceLabel: track.label,
		};

		// One-shot, so nothing is stored in any registry — but it still goes through the track's,
		// so every issue this detector reports leaves by the same door.
		this.trackMonitor.issues.notify({
			includeInSample: this.includeIssueInSample,
			type: CaptureSourceLostDetector.ISSUE_TYPE,
			payload,
		});

		if (this.config.createEvent === false) return;

		clientMonitor.addEvent({
			type: ClientEventTypes.CAPTURE_SOURCE_LOST,
			payload: { ...payload },
		});
	}
}

```
### CaptureTrackMutedDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CaptureTrackMutedDetector.ts#L28)
Category: Telemetry
```ts
import { Detector } from "./Detector";
import { OutboundTrackMonitor } from "../monitors/OutboundTrackMonitor";
import { ClientEventTypes } from "../schema/ClientEventTypes";

export type CaptureTrackMutedDetectorConfig = {
	/** Buffer a `CAPTURE_TRACK_MUTED` client event into the sample too. Default true. */
	createEvent?: boolean;
}

/**
 * Timestamps the moment something outside the application took the capture device away:
 * `track.muted` flipped to true — the OS grabbing the microphone, another app claiming the camera,
 * a closed lid, a privacy shutter. Use it to explain the silence and dry-track findings that follow
 * it, and to tell an external capture loss apart from the application's own mute (`track.enabled`).
 *
 * Only the false → true transition is reported, never the first observation and never the recovery.
 *
 * It raises no issue by design: a muted source is usually what the user intended, and the same flag
 * covers both cases.
 *
 * Raises no issue. Emits `capture-track-muted`, plus the `CAPTURE_TRACK_MUTED`
 * client event unless `createEvent` is false. Config: `captureTrackMutedDetector`.
 *
 * Category: Telemetry
 * Layer: Lifecycle
 *
 */
export class CaptureTrackMutedDetector implements Detector {
	public readonly name = 'capture-track-muted-detector';
	public disabled = false;

	private _lastMuted?: boolean;

	public constructor(
		public readonly trackMonitor: OutboundTrackMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.captureTrackMutedDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) return;

		const track = this.trackMonitor.track;
		const muted = track.muted === true;

		if (this._lastMuted === muted) return;

		const wasKnown = this._lastMuted !== undefined;

		this._lastMuted = muted;

		if (!wasKnown || !muted) return;

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('capture-track-muted', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
		});

		if (this.config.createEvent === false) return;

		clientMonitor.addEvent({
			type: ClientEventTypes.CAPTURE_TRACK_MUTED,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: track.id,
				kind: track.kind,
				deviceLabel: track.label,
			},
		});
	}
}

```
### CodecChangeDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CodecChangeDetector.ts#L26)
Category: Telemetry
```ts
import { Detector } from "./Detector";
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";
import { OutboundTrackMonitor } from "../monitors/OutboundTrackMonitor";
import { ClientEventTypes } from "../schema/ClientEventTypes";

export type CodecChangeDetectorConfig = {
	/** Buffer a `CODEC_CHANGED` client event into the sample too. Default true. */
	createEvent?: boolean;
}

/**
 * Records which codec each track is actually using, and when that changes. Use it to answer the
 * aggregate quality questions that need the codec as a column — whether bad calls cluster on H264,
 * whether AV1 is being negotiated at all, whether a hardware encoder fell back to software mid-call.
 *
 * `sdpFmtpLine` counts as well as `mimeType`, so a profile switch inside one mime type is not
 * invisible. The first codec seen is the baseline, not a change.
 *
 * Raises no issue. Emits `codec-changed`, plus the `CODEC_CHANGED` client event unless
 * `createEvent` is false. Config: `codecChangeDetector`.
 *
 * Category: Telemetry
 * Layer: Media
 *
 */
export class CodecChangeDetector implements Detector {
	public readonly name = 'codec-change-detector';
	public disabled = false;

	private _mimeType?: string;
	private _fmtp?: string;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor | OutboundTrackMonitor,
	) {}

	private get config() {
		return this.peerConnection.parent.config.codecChangeDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) return;

		// A track that ended negotiates nothing further; a codec still named in its last report
		// is the codec it died on, not a change. Both monitors carry `readyState`, so neither
		// direction needs its own case.
		if (this.trackMonitor.readyState !== 'live') return;

		const rtp = this.trackMonitor.direction === 'inbound'
			? this.trackMonitor.getInboundRtp()
			: this.trackMonitor.highestLayer;
		const codec = rtp?.getCodec();

		if (!codec?.mimeType) return;

		const previousMimeType = this._mimeType;
		const previousFmtp = this._fmtp;

		this._mimeType = codec.mimeType;
		this._fmtp = codec.sdpFmtpLine;

		if (previousMimeType === undefined) return;
		if (previousMimeType === codec.mimeType && previousFmtp === codec.sdpFmtpLine) return;

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('codec-changed', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			from: { mimeType: previousMimeType, sdpFmtpLine: previousFmtp },
			to: { mimeType: codec.mimeType, sdpFmtpLine: codec.sdpFmtpLine },
		});

		if (this.config.createEvent === false) return;

		clientMonitor.addEvent({
			type: ClientEventTypes.CODEC_CHANGED,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				direction: this.trackMonitor.direction,
				kind: this.trackMonitor.kind,
				fromMimeType: previousMimeType,
				fromSdpFmtpLine: previousFmtp,
				mimeType: codec.mimeType,
				sdpFmtpLine: codec.sdpFmtpLine,
				payloadType: codec.payloadType,
				clockRate: codec.clockRate,
				channels: codec.channels,
			},
		});
	}
}

```
### CongestionDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CongestionDetector.ts#L77)
Category: Transport Quality
```ts
import { Detector } from "./Detector";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { ClientMonitorEvents } from "../ClientMonitorEvents";

export type CongestionIssuePayload = {
	peerConnectionId: string;
	/** Bandwidth estimate at the moment congestion was declared, in bps. */
	availableIncomingBitrate: number;
	/** Bandwidth estimate at the moment congestion was declared, in bps. */
	availableOutgoingBitrate: number;
	/** Peak estimate observed during the healthy stretch immediately before this episode. */
	maxAvailableIncomingBitrate: number;
	/** Peak estimate observed during the healthy stretch immediately before this episode. */
	maxAvailableOutgoingBitrate: number;
	/** Peak bitrate actually received during that same healthy stretch. */
	maxReceivingBitrate: number;
	/** Peak bitrate actually sent during that same healthy stretch. */
	maxSendingBitrate: number;
	/** Filled in when the issue is resolved. */
	durationInMs?: number;
}

export type CongestionDecetorEvent = ClientMonitorEvents['congestion'];

export type CongestionDetectorConfig = {
	/**
	 * How much corroboration the browser's own bandwidth verdict needs before congestion is
	 * declared. `high` takes it at its word, `medium` also wants the round trip to be moving,
	 * `low` instead wants outbound loss above 5%.
	 */
	sensitivity: 'low' | 'medium' | 'high';
}

/**
 * **Deprecated.** Superseded by `UplinkCongestionDetector` and `DownlinkCongestionDetector`, which
 * judge each direction on its own evidence and report a graded `severity` rather than a single
 * on/off verdict for the whole connection. This class is kept only so integrations built against
 * the `congestion` event and the `congestion` issue keep working through the transition, and will
 * be removed. New code should read `uplink-congestion` and `downlink-congestion`.
 *
 * Watches a peer connection for the point at which the network stops being able to carry what
 * the encoder wants to produce — the cause behind collapsing resolution, stuttering video and
 * the "you're breaking up" complaint.
 *
 * The anchor signal is the browser's own verdict rather than any bitrate threshold this library
 * could invent: `qualityLimitationReason === 'bandwidth'` on an outbound stream means the
 * encoder is already being throttled by the bandwidth estimator, which sees far more than the
 * stats API exposes. That verdict is eager, so `sensitivity` decides how much corroboration is
 * demanded. `high` takes it at its word. `medium` additionally wants the round trip to be
 * moving — the current average diverging from its EWMA by more than a third of that EWMA,
 * clamped to a 50-150ms band — which is queue build-up rather than a link that is merely narrow.
 * `low` instead wants outbound loss above 5%, and deliberately applies no round-trip guard:
 * requiring both made a bandwidth-limited connection losing a twentieth of its packets read as
 * perfectly healthy until the first RTCP report happened to arrive.
 *
 * Both round-trip figures are drawn with the same source preference, RTCP first and ICE/STUN as
 * the fallback, so their difference can never compare two different round trips against each
 * other. Whenever the connection is *not* congested the detector keeps running maxima of the
 * available and actual bitrates; those travel with the issue as the "before" picture and are
 * then reset, so each episode is measured against the headroom that immediately preceded it
 * rather than against the whole call.
 *
 * Its issue is raised on the **client** registry rather than the connection's, which is what keeps
 * it out of the score: `uplink-congestion` and `downlink-congestion` already price congestion, and
 * a deprecated duplicate reporting the same condition must not penalise a call twice. The client
 * registry is not read by `DefaultScoreCalculator` at all, so raising it there is what makes that
 * true rather than a rule written down somewhere else.
 *
 * Raises `congestion`. Emits `congestion`. Config: `congestionDetector`.
 * Connection attribute: `PeerConnectionMonitor.congested`.
 *
 * Category: Transport Quality
 * Layer: Capacity
 *
 * @deprecated Use `UplinkCongestionDetector` and `DownlinkCongestionDetector` instead.
 */
export class CongestionDetector implements Detector {
	public static readonly ISSUE_TYPE = 'congestion';
	public readonly name = 'congestion-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private _maxAvailableIncomingBitrate = 0;

	private _maxReceivingBitrate = 0;

	private _maxAvailableOutgoingBitrate = 0;

	private _maxSendingBitrate = 0;

	private readonly issueKey: string;

	private _startedCongestionAt?: number;

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor
	) {
		this.issueKey = `${CongestionDetector.ISSUE_TYPE}-pc-${peerConnection.peerConnectionId}`;
	}

	private get config() {
		return this.peerConnection.parent.config.congestionDetector!;
	}

	public update() {

		if (this.disabled) return;
		let hasBwLimitedOutboundRtp = false;

		for (const outboundRtp of this.peerConnection.outboundRtps) {
			hasBwLimitedOutboundRtp ||= outboundRtp.qualityLimitationReason === 'bandwidth';
		}

		// avgRttInSec/ewmaRttInSec prefer the RTCP round trip and fall back to
		// ICE/STUN together, so the difference below never mixes two round trips
		let rttDiffInS = 0;

		if (this.peerConnection.avgRttInSec !== undefined) {
			if (this.peerConnection.ewmaRttInSec !== undefined) {
				rttDiffInS = Math.abs(this.peerConnection.avgRttInSec - this.peerConnection.ewmaRttInSec);
			}
		}

		let isCongested = false;

		switch (this.config.sensitivity) {
			case 'high':
				isCongested = hasBwLimitedOutboundRtp;
				break;
			case 'medium': {
				if (!this.peerConnection.ewmaRttInSec) break;

				const rttDiffThreshold = Math.min(0.15, Math.max(0.05, this.peerConnection.ewmaRttInSec * 0.33));

				isCongested = hasBwLimitedOutboundRtp && rttDiffInS > rttDiffThreshold;

				break;
			}
			case 'low': {
				// No RTT guard here (unlike `medium`): requiring one made a bandwidth-limited
				// connection losing >5% silently not congested before the first RTCP report.
				if (this.peerConnection.outboundFractionLost === undefined) break;

				isCongested = hasBwLimitedOutboundRtp && this.peerConnection.outboundFractionLost > 0.05;
				break;
			}
		}
		const availableIncomingBitrate = this.peerConnection.totalAvailableIncomingBitrate ?? 0;
		const availableOutgoingBitrate = this.peerConnection.totalAvailableOutgoingBitrate ?? 0;

		if (!isCongested) {
			if (this.peerConnection.congested) {
				this.peerConnection.congested = false;
				this._resolve('congestion ended');
			}
			this._maxAvailableIncomingBitrate = Math.max(this._maxAvailableIncomingBitrate, availableIncomingBitrate);
			this._maxAvailableOutgoingBitrate = Math.max(this._maxAvailableOutgoingBitrate, availableOutgoingBitrate);
			this._maxReceivingBitrate = Math.max(this._maxReceivingBitrate, this.peerConnection.receivingBitrate);
			this._maxSendingBitrate = Math.max(this._maxSendingBitrate, this.peerConnection.sendingBitrate);

			return;
		} else if (this.peerConnection.congested) {
			return;
		}

		this.peerConnection.congested = true;
		this.peerConnection.parent.emit('congestion', {
			clientMonitor: this.peerConnection.parent,
			peerConnectionMonitor: this.peerConnection,
			availableIncomingBitrate,
			availableOutgoingBitrate,
			maxAvailableIncomingBitrate: this._maxAvailableIncomingBitrate,
			maxAvailableOutgoingBitrate: this._maxAvailableOutgoingBitrate,
			maxReceivingBitrate: this._maxReceivingBitrate,
			maxSendingBitrate: this._maxSendingBitrate,
		});

		this._raise({
			peerConnectionId: this.peerConnection.peerConnectionId,
			availableIncomingBitrate,
			availableOutgoingBitrate,
			maxAvailableIncomingBitrate: this._maxAvailableIncomingBitrate,
			maxAvailableOutgoingBitrate: this._maxAvailableOutgoingBitrate,
			maxReceivingBitrate: this._maxReceivingBitrate,
			maxSendingBitrate: this._maxSendingBitrate,
		});

		this._maxAvailableIncomingBitrate = 0;
		this._maxAvailableOutgoingBitrate = 0;
		this._maxReceivingBitrate = 0;
		this._maxSendingBitrate = 0;
	}

	private _raise(payload: CongestionIssuePayload) {
		this._startedCongestionAt = Date.now();

		this.peerConnection.parent.raiseIssue<CongestionIssuePayload>(this.issueKey, {
			includeInSample: this.includeIssueInSample,
			type: CongestionDetector.ISSUE_TYPE,
			payload,
		});
	}

	private _resolve(comment?: string) {
		const clientMonitor = this.peerConnection.parent;

		clientMonitor.resolveIssue<CongestionIssuePayload>(this.issueKey, {
			comment,
			// The registry merges, so the raise's payload survives and only the duration is added.
			payload: {
				durationInMs: this._startedCongestionAt ? Date.now() - this._startedCongestionAt : undefined,
			} as CongestionIssuePayload,
			resolvedAt: Date.now(),
		});

		this._startedCongestionAt = undefined;
	}

}

```
### CpuPerformanceDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CpuPerformanceDetector.ts#L104)
Category: Pipeline Disruption
```ts
import { ClientMonitor } from "..";
import type { ClientWindowValues } from "../ClientMonitor";
import type { WindowSlice } from "../utils/SlicedWindow";
import { runsOffCpu } from "../utils/cpu";
import { Detector } from "./Detector";

export type CpuPerformanceIssuePayload = {
	/**
	 * Time spent inside the video encoders per unit of stats time, summed over every sending
	 * stream that encodes on the CPU. `0.5` is half the interval occupied encoding; because the
	 * streams add, three simulcast layers busy half the time each come to `1.5` rather than
	 * saturating at `1`.
	 */
	encoderUtilization: number;

	/** The same for the video decoders, summed over every receiving stream that decodes on the CPU. */
	decoderUtilization?: number;

	/**
	 * The lower of the two utilizations, or whichever one exists on a client that only sends or
	 * only receives. This is what gets compared against `utilizationThreshold`.
	 */
	minUtilization: number;

	/** How many video streams were left out of each sum for encoding or decoding off the CPU. */
	hardwareAcceleratedEncoders: number;
	hardwareAcceleratedDecoders: number;

	/** The stretch the reading above was taken over, as the window measured it. */
	sustainedForInMs: number;

	/** Filled in when the issue is resolved: the reading that cleared it, and how long it stood. */
	recoveredMinUtilization?: number;
	durationInMs?: number;
}

export type CpuPerformanceDetectorConfig = {
	/**
	 * The utilization `minUtilization` has to reach before this reports anything. Read it as a
	 * usage level: `0.5` means both halves of the pipeline are spending at least half the
	 * detection window inside a codec.
	 */
	utilizationThreshold: number;

	/**
	 * Utilization below which the finding clears. Keep it under `utilizationThreshold` to stop
	 * flapping. The sustain is not here: it is the detection slice, and `clientWindow` is where
	 * its length lives.
	 */
	recoveryThreshold: number;
}

/**
 * Reports the client machine, rather than the network, being why a call looks bad. Use it to tell a
 * saturated CPU apart from a congested link before anyone goes looking at the network.
 *
 * A finding means the device is out of headroom: too many streams for it, a thermal or battery
 * throttle, another application taking the machine, or a software codec on hardware too old to run
 * it. It is a property of the endpoint, so the same user tends to show it on every call.
 *
 * The measurement is **utilization** — codec time per unit of stats time, summed over the video
 * streams, where `0.25` is a quarter of the stretch spent inside a codec. Summed rather than
 * averaged, so three simulcast layers busy half the time each read `1.5`; nothing clamps it at `1`.
 * `encoderUtilization` and `decoderUtilization` combine with `min()` into `minUtilization`, so codec
 * work on one side alone is a busy stream and work on both at once is a busy machine. A client
 * missing one direction is judged on the other.
 *
 * **It reads that over `ClientMonitor.slicedWindow`**, not off a single collection. Utilization
 * swings with whatever the encoder happens to be doing from one collection to the next, and a
 * machine actually out of headroom stays busy across the stretch; reading one collection at a time
 * made a busy moment indistinguishable from a busy machine, and the finding flickered on and off
 * with it. The sustain *is* the detection slice, which is why this detector counts no duration of
 * its own: `clientWindow` is where its length lives.
 *
 * A finding clears when the *recovery* window — the stretch behind the detection window — is also
 * below `recoveryThreshold`, so the machine has to have been quiet across both spans rather than
 * merely the most recent one.
 *
 * The totals come off `PeerConnectionMonitor`, accumulated one collection's delta at a time and
 * summed across connections, rather than read from the streams' own counters. That is what makes a
 * stream appearing or disappearing mid-call a change in what is being measured instead of a step in
 * the total: a layer that joins brings only what it encodes from then on.
 *
 * It is not CPU time: `totalEncodeTime` is elapsed time inside the codec call, so a hardware codec
 * waiting on the GPU would count in full. Streams naming an off-CPU implementation, or flagged
 * `powerEfficient`, are left out as each collection's delta is taken — whether a stream counts is a
 * property of that collection, not of the stretch read back later. Whether there is anything to
 * measure at all is likewise decided on the current collection: a wholly hardware pipeline sets
 * `inputsUnavailable` rather than reading as healthy, which a cumulative total holding its last
 * value could not tell you. A backgrounded tab is not fed to the window at all, since throttled
 * timers stretch the interval and read as an idle machine; the hole that leaves trips the window's
 * own gap guard.
 *
 * Deliberately not gated on `qualityLimitationReason === 'cpu'`: Chrome's precedence is
 * `bandwidth > cpu > none`, so a machine that is both would report `bandwidth` and the gate would
 * close exactly where both problems are real.
 *
 * Raises `cpulimitation`. Emits `cpulimitation`. Config: `cpuPerformanceDetector`.
 *
 * Category: Pipeline Disruption
 * Layer: Across both chains — the machine
 *
 */
export class CpuPerformanceDetector implements Detector {
	public static readonly ISSUE_TYPE = 'cpulimitation';

	public readonly name = 'cpu-performance-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	private readonly issueKey = CpuPerformanceDetector.ISSUE_TYPE;

	private _startedAlertAt?: number;

	public constructor(
		public readonly clientMonitor: ClientMonitor,
	) {}

	private get config() {
		return this.clientMonitor.config.cpuPerformanceDetector!;
	}

	public update() {
		if (this.disabled) return;

		if (!this.clientMonitor.activeTab) {
			this.inputsUnavailable = false;
			this.clientMonitor.cpuUtilization = undefined;

			return this._standDown('tab in background');
		}

		// No video at all, or none of it running on the CPU. Either way there is no CPU cost
		// visible here — which is not the same as a machine with room to spare. Read from this
		// collection rather than from the window: whether there is anything to measure is a fact
		// about now, where the window's totals are cumulative and would keep their last value.
		const streams = this._videoStreams();

		if (streams.onCpu === 0) {
			this.inputsUnavailable = true;
			this.clientMonitor.cpuUtilization = undefined;

			return this._standDown(0 < streams.hardwareEncoders + streams.hardwareDecoders
				? 'all video is encoded and decoded off the cpu'
				: 'no video is being encoded or decoded');
		}

		const {
			detection: detectionWindow,
			recovery: recoveryWindow,
		} = this.clientMonitor.slicedWindow.slices;

		// Not enough values yet is not a verdict either way, and it is not blindness: the window is
		// filling and will have an answer shortly. The span is checked alongside the count because
		// a window counts values, not time — collections carrying no time between them fill it
		// while measuring nothing, which is a frozen collector rather than a busy machine.
		if (!detectionWindow.isReady || detectionWindow.durationInMs < 1) return;

		const detection = this._utilization(detectionWindow);

		// Streams are running on the CPU but the window could not produce a reading from them, so
		// the detector can no longer support the claim it made. An unsupportable claim must not
		// stand for the rest of the call: a detector able to raise is always able to clear.
		if (detection === undefined) {
			this.inputsUnavailable = true;
			this.clientMonitor.cpuUtilization = undefined;

			return this._standDown('codec time is no longer measurable');
		}

		this.inputsUnavailable = false;

		// Written before the threshold test, so the measurement is there below the bar as well as
		// above it — a machine at 0.7 of its budget is not the same as one nobody measured.
		this.clientMonitor.cpuUtilization = detection.min;

		if (this.config.utilizationThreshold <= detection.min) {
			if (this.clientMonitor.cpuPerformanceAlertOn) return;

			return this._raise({
				encoderUtilization: detection.encoder ?? 0,
				decoderUtilization: detection.decoder,
				minUtilization: detection.min,
				sustainedForInMs: detectionWindow.durationInMs,
				hardwareAcceleratedEncoders: streams.hardwareEncoders,
				hardwareAcceleratedDecoders: streams.hardwareDecoders,
			});
		}

		if (!this.clientMonitor.cpuPerformanceAlertOn) return;

		// Below the bar with a finding open. The machine has to have been quiet for the stretch
		// behind this one as well, which is what keeps a finding standing long enough to be worth
		// reporting rather than clearing on the collection after it was raised. A recovery slice
		// that has not filled yet is not a verdict — the window is filling and will have an answer
		// shortly — so the finding waits rather than being cleared on the detection stretch alone.
		if (!recoveryWindow.isReady) return;

		// Ready but unreadable is the other case, and it must not be able to hold a finding open
		// for ever: a detector that can raise has to be able to clear, so with nothing behind it
		// to consult the detection reading decides on its own.
		const clearing = this._utilization(recoveryWindow) ?? detection;

		if (this.config.recoveryThreshold <= clearing.min) return;

		this._standDown('cpu limitation ended', detection.min);
	}

	/**
	 * Codec time over the stretch the slice spans, for each direction, and the lower of the two.
	 *
	 * The denominator is the slice's own wall clock rather than a sum of per-stream intervals, so
	 * the summed-across-streams scale survives: three simulcast layers each busy half the stretch
	 * read `1.5`, where dividing by their combined interval would have averaged them back to `0.5`.
	 * Nothing clamps it at `1`.
	 *
	 * `undefined` when neither direction produced a delta — the window says it could not see, which
	 * is what keeps a receive-only client from reading as an idle encoder and a hardware pipeline
	 * from reading as an idle machine. A direction that is `null` on its own simply does not
	 * participate in the `min`.
	 */
	private _utilization(
		slice: WindowSlice<ClientWindowValues>,
	): { encoder?: number, decoder?: number, min: number } | undefined {
		if (slice.durationInMs < 1) return undefined;

		const perUnitTime = (delta: number | null) => delta === null
			? undefined
			: delta / slice.durationInMs;

		const encoder = perUnitTime(slice.deltaTotalVideoEncodeTimeInMs);
		const decoder = perUnitTime(slice.deltaTotalVideoDecodeTimeInMs);

		if (encoder === undefined && decoder === undefined) return undefined;

		// The lower of the two, and whichever one exists when the client only sends or only
		// receives: codec work on one side alone is a busy stream, on both at once a busy machine.
		const min = encoder === undefined
			? decoder as number
			: decoder === undefined
				? encoder
				: Math.min(encoder, decoder);

		return { encoder, decoder, min };
	}

	/**
	 * What the video pipeline looks like on this collection: how many streams have codec work
	 * landing on the CPU, and how many were left out because it lands somewhere else.
	 *
	 * A description of the pipeline right now, not a measurement over a stretch — which is what
	 * makes it the right thing to decide blindness on. A stream counts as on-CPU as soon as it is
	 * present and software, whether or not it reported codec time this collection.
	 */
	private _videoStreams() {
		let onCpu = 0;
		let hardwareEncoders = 0;
		let hardwareDecoders = 0;

		for (const outboundRtp of this.clientMonitor.outboundRtps) {
			if (outboundRtp.kind !== 'video') continue;

			if (runsOffCpu(outboundRtp.encoderImplementation, outboundRtp.powerEfficientEncoder)) ++hardwareEncoders;
			else ++onCpu;
		}
		for (const inboundRtp of this.clientMonitor.inboundRtps) {
			if (inboundRtp.kind !== 'video') continue;

			if (runsOffCpu(inboundRtp.decoderImplementation, inboundRtp.powerEfficientDecoder)) ++hardwareDecoders;
			else ++onCpu;
		}

		return { onCpu, hardwareEncoders, hardwareDecoders };
	}

	private _raise(payload: CpuPerformanceIssuePayload) {
		this._startedAlertAt = Date.now();
		// Set here, not at the call sites, so the flag and the finding cannot drift.
		this.clientMonitor.cpuPerformanceAlertOn = true;

		this.clientMonitor.emit('cpulimitation', {
			clientMonitor: this.clientMonitor,
		});

		this.clientMonitor.activeIssues.raise({
			key: this.issueKey,
			includeInSample: this.includeIssueInSample,
			type: CpuPerformanceDetector.ISSUE_TYPE,
			payload,
		});
	}

	/**
	 * Closes any open alert. Guarded, because this is a healthy machine's resting state.
	 *
	 * `recoveredMinUtilization` is the reading that cleared the finding, carried into the resolve
	 * payload beside the one that raised it — so whoever reads the pair can see the improvement
	 * rather than only that something stopped.
	 */
	private _standDown(comment: string, recoveredMinUtilization?: number) {
		if (!this.clientMonitor.cpuPerformanceAlertOn) return;

		this.clientMonitor.cpuPerformanceAlertOn = false;

		this.clientMonitor.activeIssues.resolve({
			key: this.issueKey,
			comment,
			payload: {
				recoveredMinUtilization,
				durationInMs: this._startedAlertAt ? Date.now() - this._startedAlertAt : undefined,
			},
			resolvedAt: Date.now(),
		});

		this._startedAlertAt = undefined;
	}
}

```
### DecoderBottleneckDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DecoderBottleneckDetector.ts#L126)
Category: Pipeline Disruption
```ts
import { Detector } from "./Detector";
import type { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";

/**
 * What the detector measured about the decoder in the window that raised the issue.
 *
 * Every field not marked optional is always present: the detector cannot reach the raise without
 * it. The track's own `readyState` and `muted` are not carried, because the detector only raises
 * on a track that is live, unmuted and enabled, so they could only ever read `'live'` and `false`.
 */
export type DecoderBottleneckIssuePayload = {
	peerConnectionId: string;
	trackId: string;

	/** The average frames per second that arrived over the detection window. */
	receivedFpsForDetection: number;

	/** The number of frames that arrived over the detection window. */
	receivedFramesForDetection: number;

	/** The average frames per second the decoder produced over the detection window. */
	decodedFpsForDetection: number;

	/** The number of frames the decoder produced over the detection window. */
	decodedFramesForDetection: number;

	/** The milliseconds of stats time the detection window spanned. */
	detectionWindowInMs: number;

	/**
	 * The share of the frames that arrived which the decoder did not get through,
	 * `1 - decodedFpsForDetection / receivedFpsForDetection`. Zero is a decoder keeping up with the
	 * wire and one is a decoder emitting nothing; a decoder ahead of the wire, which counters read a
	 * frame apart can produce, reports a negative.
	 */
	decodeDegradation: number;

	/** Frames the browser threw away before the decoder over the detection window. */
	droppedFramesForDetection: number;

	/**
	 * Frames that arrived over the detection window, dropped ones included.
	 *
	 * `receivedFramesForDetection` is this minus the dropped ones — what actually reached the
	 * decoder, and what `decodeDegradation` is measured against. The two are published side by
	 * side because their difference is the distinction between a decoder that could not keep up
	 * and a path delivering frames too late to use.
	 */
	arrivedFramesForDetection: number;

	/** The average frames per second that arrived, dropped ones included. */
	arrivedFpsForDetection: number;

	/** The decoded frame size when the issue opened. */
	frameWidth?: number;
	frameHeight?: number;

	// Written at resolution, from the recovery window that ended the issue. Absent when it was
	// resolved by a stand-down instead, where nothing was measured.

	/** The milliseconds of stats time the recovery window spanned. */
	recoveryWindowInMs?: number;

	/** The average frames per second that arrived during the recovery window. */
	receivedFpsForRecovery?: number;

	/** The number of frames that arrived during the recovery window. */
	receivedFramesForRecovery?: number;

	/** The average frames per second the decoder produced during the recovery window. */
	decodedFpsForRecovery?: number;

	/** The number of frames the decoder produced during the recovery window. */
	decodedFramesForRecovery?: number;
}

export type DecoderBottleneckDetectorConfig = {
	/**
	 * The share of the arriving frames the decoder may fail to get through before the issue is
	 * raised, and must return to before it resolves.
	 */
	decodeDegradationThreshold: number;

	/** Not a substituted baseline — it only refuses a ratio taken over a handful of frames. */
	minReceivedFps: number;
}

/**
 * Given a wire that is delivering, is the decoder keeping up with it? The receive-side mirror of
 * `EncoderBottleneckDetector`, and it reads the same way: two counters on the same stretch, frames
 * that arrived against frames the decoder produced. The difference is frames the decoder was handed
 * and never got through, and the viewer sees a stuttering tile.
 *
 * Both counters come from `InboundTrackMonitor.slicedWindow`. The detection window
 * raises — leaving more than `decodeDegradationThreshold` of the arriving frames undecoded opens
 * the issue, and every later collection still short of it updates that issue rather than opening
 * another. The recovery window resolves: the issue ends only once the stretch *before* the
 * detection window is back within the threshold, so a decoder hovering at the line cannot flap one
 * long fault into a stream of short ones. Neither window is read before it says it is ready.
 *
 * The bar is the measured arrival rate, never the sender's intent, so a stream throttled to 5fps
 * that decodes cleanly is silent. A stream thinner than `minReceivedFps` is refused rather than
 * judged, because a ratio taken over a handful of frames says nothing.
 *
 * A finding means the network did its job and this machine did not keep up: too many streams open
 * for it, a software codec on hardware too slow for the resolution, or the CPU taken by something
 * else. The fix is local — fewer or smaller streams — never a network one.
 *
 * This is the only detector that reports frames lost after arrival. `DecoderPerformanceDetector`
 * measures what decoding *cost* — time per frame against the frame budget — and says nothing about
 * how many frames came out, so the two describe one decoder from two sides without double-reporting
 * it. Cost is the earlier warning; loss is what the viewer sees.
 *
 * It stands down — reporting `undefined` rather than a verdict — for a backgrounded tab, a paused
 * consumer or sender, a track that is not playing, and a stream too thin to judge.
 *
 * Issue raised: `decoder-bottleneck`, updated while it stays open, resolved on recovery or on a
 * stand-down. Monitor event: `decoder-bottleneck`, emitted once at the raise.
 * Config: `decoderBottleneckDetector`.
 * Track attribute: `InboundTrackMonitor.degradedFrameSupply`.
 *
 * Category: Pipeline Disruption
 * Layer: Receive — frames to decoder
 *
 */
export class DecoderBottleneckDetector implements Detector {
	public static readonly ISSUE_TYPE = 'decoder-bottleneck';

	public readonly name = 'decoder-bottleneck-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _issueKey: string;
	private _raised = false;

	/**
	 * Frames that arrived in the previous collection, for the stats-gap guard.
	 *
	 * `undefined` until the first judged collection, `0` after one that carried nothing — which is
	 * the shape a frozen stats report leaves behind, and the one collection this must not judge
	 * across.
	 */
	private _previousCollectionArrived?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this._issueKey = `${DecoderBottleneckDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;

		// Read without the getter's non-null assertion: a monitor builds this detector whenever the
		// key is not explicitly `null`, which includes a config that never mentioned it at all.
		const config = this.peerConnection.parent.config.decoderBottleneckDetector;

		if (config && config.decodeDegradationThreshold < 0) {
			this.peerConnection.parent.logger.warn(
				'decoderBottleneckDetector.decodeDegradationThreshold must not be below 0, got '
				+ config.decodeDegradationThreshold
			);
			config.decodeDegradationThreshold = 0;
		}
	}

	private get config(): DecoderBottleneckDetectorConfig {
		return this.peerConnection.parent.config.decoderBottleneckDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) {
			this.trackMonitor.degradedFrameSupply = undefined;

			return;
		}
		if (this.trackMonitor.kind !== 'video') return;

		const track = this.trackMonitor.track;

		if (!this.peerConnection.parent.activeTab) return this._clear({
			comment: 'tab in background',
		});
		if (this.trackMonitor.paused) return this._clear({
			comment: 'consumer paused',
		});
		if (this.trackMonitor.remoteOutboundTrackPaused) return this._clear({
			comment: 'remote sender paused',
		});
		if (this.trackMonitor.readyState !== 'live') return this._clear({
			comment: 'track ended',
		});
		if (track.muted || !track.enabled) return this._clear({
			comment: 'track not playing',
		});

		const {
			detection: detectionWindow,
			recovery: recoveryWindow,
		} = this.trackMonitor.slicedWindow.slices;
		const arrivedFramesForDetection = detectionWindow.deltaTotalFramesReceived;
		const decodedFramesForDetection = detectionWindow.deltaTotalFramesDecoded;
		const droppedFramesForDetection = detectionWindow.deltaTotalFramesDropped;
		const detectionWindowInMs = detectionWindow.durationInMs;

		if (arrivedFramesForDetection === null) return this._clear({
			comment: 'no arriving frame count',
		});
		if (decodedFramesForDetection === null) return this._clear({
			comment: 'no decoded frame count',
		});
		if (droppedFramesForDetection === null) return this._clear({
			comment: 'no dropped frame count',
		});
		if (!detectionWindow.isReady || detectionWindowInMs < 1) return;

		// A dropped frame is one the browser threw away before the decoder, and on a captured call
		// it accounted for the shortfall to within two frames on 98% of the collections where one
		// existed — arriving late or incomplete under retransmission, not queued behind a decoder
		// that could not keep up. Charging them here made this a second, differently-named
		// `dropped-video-frames`, which the score already prices from the same counters. What is
		// left after subtracting them is the remainder the decoder is actually answerable for.
		const receivedFramesForDetection = Math.max(0, arrivedFramesForDetection - droppedFramesForDetection);
		const receivedFpsForDetection = receivedFramesForDetection / (detectionWindowInMs / 1000);
		const decodedFpsForDetection = decodedFramesForDetection / (detectionWindowInMs / 1000);
		const arrivedFpsForDetection = arrivedFramesForDetection / (detectionWindowInMs / 1000);

		// A collection whose counters froze, and a next one reporting both intervals' frames on one
		// interval's clock. The rate reads at twice the stream's own, and the backlog the decoder
		// discards on the way out reads as a bottleneck: on a captured call this raised at a
		// computed 76fps for a 30fps stream. `StatsGapDetector` reports the gap itself; this one
		// must not judge the collection that catches up after it.
		//
		// Read from the collection's own delta rather than the window's: the artefact belongs to
		// one collection boundary, and a window wide enough to dilute it would hide the guard
		// along with the fault.
		const arrivedThisCollection = this.trackMonitor.getInboundRtp()?.deltaFramesReceived;
		const caughtUp = this._previousCollectionArrived === 0 && 0 < (arrivedThisCollection ?? 0);

		this._previousCollectionArrived = arrivedThisCollection;

		if (caughtUp) return;

		// A ratio over a handful of frames is noise, and a stream this thin is not the decoder's
		// doing. Too thin to judge is not the same as healthy, so the verdict goes blind.
		if (receivedFpsForDetection < this.config.minReceivedFps) return this._clear({
			comment: 'stream too thin to judge',
		});

		const decodeDegradation = 0 < receivedFpsForDetection
			? 1 - (decodedFpsForDetection / receivedFpsForDetection)
			: 0;

		// Beside the flag and the issue: the measurement itself, on every judged collection, so the
		// score calculator has a continuous number below the threshold as well as above it.
		this.trackMonitor.decodingDegradation = decodeDegradation;
		const inboundRtp = this.trackMonitor.getInboundRtp();

		if (this.config.decodeDegradationThreshold < decodeDegradation) {
			if (!this._raised) return this._raiseIssue({
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: track.id,
				decodeDegradation,
				receivedFpsForDetection,
				receivedFramesForDetection,
				decodedFpsForDetection,
				decodedFramesForDetection,
				droppedFramesForDetection,
				arrivedFramesForDetection,
				arrivedFpsForDetection,
				detectionWindowInMs,
				frameWidth: inboundRtp?.frameWidth,
				frameHeight: inboundRtp?.frameHeight,
			}, receivedFpsForDetection, decodedFpsForDetection);

			return void this.trackMonitor.issues.update({
				key: this._issueKey,
				payload: {
					decodeDegradation,
				},
			});
		}

		// Below the threshold with nothing open: the decoder was judged and found to be keeping up,
		// which is not the same as not having been judged at all.
		if (!this._raised) return this._clear({
			comment: 'decoder keeping up',
			degradedFrameSupply: false,
		});

		// Below the threshold with a finding open: the recovery window decides whether it ends.

		const arrivedFramesForRecovery = recoveryWindow.deltaTotalFramesReceived;
		const decodedFramesForRecovery = recoveryWindow.deltaTotalFramesDecoded;
		const droppedFramesForRecovery = recoveryWindow.deltaTotalFramesDropped;
		const recoveryWindowInMs = recoveryWindow.durationInMs;

		if (
			!recoveryWindow.isReady ||
			arrivedFramesForRecovery === null ||
			decodedFramesForRecovery === null ||
			droppedFramesForRecovery === null ||
			recoveryWindowInMs < 1
		) {
			return void this.trackMonitor.issues.update({
				key: this._issueKey,
				payload: {
					decodeDegradation,
				},
			});
		}

		// The same subtraction the detection half makes, for the same reason: a stretch whose
		// frames were dropped on the way in is not a stretch the decoder failed on, and a recovery
		// judged without it could never be demonstrated on a lossy path.
		const receivedFramesForRecovery = Math.max(0, arrivedFramesForRecovery - droppedFramesForRecovery);
		const receivedFpsForRecovery = receivedFramesForRecovery / (recoveryWindowInMs / 1000);
		const decodedFpsForRecovery = decodedFramesForRecovery / (recoveryWindowInMs / 1000);

		// The same floor the detection half needs, and the same reason for wanting one: a thin
		// stretch cannot demonstrate a recovery any more than it can demonstrate a fault.
		if (receivedFpsForRecovery < this.config.minReceivedFps) {
			return void this.trackMonitor.issues.update({
				key: this._issueKey,
				payload: {
					decodeDegradation,
				},
			});
		}

		const recoveryDegradation = 0 < receivedFpsForRecovery
			? 1 - (decodedFpsForRecovery / receivedFpsForRecovery)
			: 0;

		if (this.config.decodeDegradationThreshold < recoveryDegradation) {
			return void this.trackMonitor.issues.update({
				key: this._issueKey,
				payload: {
					decodeDegradation,
				},
			});
		}

		this._clear({
			comment: 'decoding recovered',
			payload: {
				receivedFpsForRecovery,
				receivedFramesForRecovery,
				decodedFpsForRecovery,
				decodedFramesForRecovery,
				recoveryWindowInMs,
			},
			degradedFrameSupply: false,
		});
	}

	private _raiseIssue(payload: DecoderBottleneckIssuePayload, receivedFps: number, decodedFps: number) {
		if (this._raised) return;

		this._raised = true;
		this.trackMonitor.degradedFrameSupply = true;

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('decoder-bottleneck', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			decodedFps,
			receivedFps,
		});

		this.trackMonitor.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: DecoderBottleneckDetector.ISSUE_TYPE,
			payload,
			timestamp: Date.now(),
		});
	}

	private _clear(options: {
		comment: string,
		payload?: Pick<DecoderBottleneckIssuePayload,
			'receivedFpsForRecovery' | 'receivedFramesForRecovery' |
			'decodedFpsForRecovery' | 'decodedFramesForRecovery' | 'recoveryWindowInMs'>,
		degradedFrameSupply?: false
	}) {
		this.trackMonitor.degradedFrameSupply = options.degradedFrameSupply;

		// Blanked only on a stand-down, where nothing was measured. A verdict of `false` was
		// measured, and flattening it would leave nothing to read below the threshold.
		if (options.degradedFrameSupply !== false) this.trackMonitor.decodingDegradation = undefined;

		if (!this._raised) return;

		this._raised = false;

		this.trackMonitor.issues.resolve({
			key: this._issueKey,
			comment: options.comment,
			payload: options.payload,
			resolvedAt: Date.now(),
		});
	}
}

```
### DecoderPerformanceDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DecoderPerformanceDetector.ts#L73)
Category: Pipeline Disruption
```ts
import { Detector } from "./Detector";
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";

export type DecoderPerformanceIssuePayload = {
	peerConnectionId: string;
	trackId: string;
	/** Wall-clock decode cost per frame in the interval, in milliseconds. */
	decodeTimePerFrameInMs?: number;
	/** The per-frame budget it was compared against (1000/fps), in milliseconds. */
	frameBudgetInMs?: number;
	/**
	 * Delta `framesDropped` over delta `framesReceived` in the interval. Context only — frames
	 * lost after arrival are `DecoderBottleneckDetector`'s finding, never this one's trigger.
	 */
	droppedFrameRatio?: number;
	/** Delta `framesRendered` over delta `framesDecoded` in the interval. */
	renderRatio?: number;
	/** Frames that arrived in the interval — the evidence the decoder had something to do. */
	framesReceived: number;
	decoderImplementation?: string;
	powerEfficientDecoder?: boolean;
	/** Consecutive qualifying ticks behind the alert, at least `minConsecutiveTicks`. */
	consecutiveTicks: number;
	/** Filled in when the issue is resolved. */
	durationInMs?: number;
}

export type DecoderPerformanceDetectorConfig = {
	/** Fraction of the per-frame budget (1000/fps) decoding may consume before counting as overloaded. */
	decodeTimeBudgetRatio: number;

	/** Frames that must have been received in the interval before judging. */
	minFramesReceived: number;

	/** Loss fraction above which the network is the better explanation and the detector stays silent. */
	quietLossThreshold: number;

	/** Consecutive collections the condition must hold before raising. */
	minConsecutiveTicks: number;
}

/**
 * Reports decoding costing more time than the stream leaves for it — how *expensive* each frame was
 * to decode, not how many frames came out. One measurement:
 *
 * ```
 * frameBudgetInMs = 1000 / framesPerSecond          // 33ms at 30fps, 66ms at 15fps
 *
 * raise when  decodeTimePerFrameInMs  >  frameBudgetInMs × decodeTimeBudgetRatio
 * ```
 *
 * With the default `0.8`, a 30fps stream raises once a frame takes more than 26ms to decode. The
 * budget comes from the stream's own frame rate, so a 15fps stream is not accused for costs a 30fps
 * one could not afford, and the condition must hold for `minConsecutiveTicks` collections.
 *
 * A finding means this machine is the constraint: too many streams for it, a thermal throttle, or a
 * software codec on hardware that cannot run it at this resolution. Decoding this close to the
 * budget is the warning *before* frames start being lost — once they are, the shortfall is
 * `DecoderBottleneckDetector`'s finding. This detector owns cost, that one owns loss, and neither
 * reads the other.
 *
 * It stands down and resolves whenever it cannot clear the network or the machine: a backgrounded
 * tab, too few frames to judge, or a missing loss reading.
 *
 * Raises `video-decoder-overloaded`. Emits `video-decoder-overloaded`.
 * Config: `decoderPerformanceDetector`.
 * Track attribute: `InboundTrackMonitor.overloadedDecoder`.
 *
 * Category: Pipeline Disruption
 * Layer: Receive — frames to decoder
 *
 */
export class DecoderPerformanceDetector implements Detector {
	public static readonly ISSUE_TYPE = 'video-decoder-overloaded';
	public readonly name = 'decoder-performance-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly issueKey: string;
	private _consecutiveTicks = 0;
	private _alertOn = false;
	private _startedAt?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this.issueKey = `${DecoderPerformanceDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private get config() {
		return this.peerConnection.parent.config.decoderPerformanceDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) {
			this.trackMonitor.overloadedDecoder = undefined;
			this.trackMonitor.decodeBudgetUtilization = undefined;

			return;
		}

		const inboundRtp = this.trackMonitor.getInboundRtp();

		if (!inboundRtp || inboundRtp.kind !== 'video') {
			this.trackMonitor.overloadedDecoder = undefined;
			this.trackMonitor.decodeBudgetUtilization = undefined;

			return;
		}

		if (this.trackMonitor.readyState !== 'live') {
			this._consecutiveTicks = 0;
			this.trackMonitor.overloadedDecoder = undefined;
			this.trackMonitor.decodeBudgetUtilization = undefined;

			return this._alertOn ? this._clear('track ended') : undefined;
		}
		if (!this.peerConnection.parent.activeTab) {
			this._consecutiveTicks = 0;
			this.trackMonitor.overloadedDecoder = undefined;
			this.trackMonitor.decodeBudgetUtilization = undefined;

			return this._alertOn ? this._clear('tab in background') : undefined;
		}

		const framesReceived = inboundRtp.deltaFramesReceived ?? 0;

		if (framesReceived < this.config.minFramesReceived) {
			this._consecutiveTicks = 0;
			this.trackMonitor.overloadedDecoder = undefined;
			this.trackMonitor.decodeBudgetUtilization = undefined;

			return this._alertOn ? this._clear('not enough frames to evaluate') : undefined;
		}

		const fractionLost = inboundRtp.deltaFractionLost;

		if (fractionLost === undefined) {
			this._consecutiveTicks = 0;
			this.trackMonitor.overloadedDecoder = undefined;
			this.trackMonitor.decodeBudgetUtilization = undefined;

			return this._alertOn ? this._clear('no loss reading; cannot clear the network') : undefined;
		}

		// Loss dominating means the network owns the frame loss, not the decoder.
		if (this.config.quietLossThreshold < fractionLost) {
			this._consecutiveTicks = 0;
			this.trackMonitor.overloadedDecoder = undefined;
			this.trackMonitor.decodeBudgetUtilization = undefined;

			return this._alertOn ? this._clear('loss dominates; not a decoder problem') : undefined;
		}

		// Per-frame budget from the stream's own frame rate: 33ms at 30fps, 66ms at 15fps.
		const fps = inboundRtp.framesPerSecond ?? inboundRtp.avgFramesPerSec;
		const frameBudgetInMs = fps && 0 < fps ? 1000 / fps : undefined;
		const decodeTimePerFrameInMs = inboundRtp.decodeTimePerFrameInMs;

		// Beside the flag: how much of the budget decoding used, on every collection it could be
		// measured, so a decoder at 0.7 of its budget is distinguishable from one nobody measured.
		this.trackMonitor.decodeBudgetUtilization = frameBudgetInMs !== undefined
			&& decodeTimePerFrameInMs !== undefined
			&& 0 < frameBudgetInMs
			? decodeTimePerFrameInMs / frameBudgetInMs
			: undefined;

		const decodeTooSlow = frameBudgetInMs !== undefined &&
			decodeTimePerFrameInMs !== undefined &&
			frameBudgetInMs * this.config.decodeTimeBudgetRatio < decodeTimePerFrameInMs;

		if (!decodeTooSlow) {
			this._consecutiveTicks = 0;
			this.trackMonitor.overloadedDecoder = false;

			if (this._alertOn) {
				this._clear('decoder keeping up again');
			}

			return;
		}

		this._consecutiveTicks += 1;

		if (this._alertOn) return;

		// Over the budget, but not yet for long enough to be reportable.
		if (this._consecutiveTicks < this.config.minConsecutiveTicks) {
			this.trackMonitor.overloadedDecoder = false;

			return;
		}

		this._alertOn = true;
		this._startedAt = Date.now();
		// Set here, not at the call sites, so the flag and the finding cannot drift.
		this.trackMonitor.overloadedDecoder = true;

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('video-decoder-overloaded', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			decodeTimePerFrameInMs,
			frameBudgetInMs,
		});

		this.trackMonitor.issues.raise({
				key: this.issueKey,
				includeInSample: this.includeIssueInSample,
			type: DecoderPerformanceDetector.ISSUE_TYPE,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				decodeTimePerFrameInMs,
				frameBudgetInMs,
				droppedFrameRatio: inboundRtp.droppedFrameRatio,
				renderRatio: inboundRtp.renderRatio,
				framesReceived,
				decoderImplementation: inboundRtp.decoderImplementation,
				powerEfficientDecoder: inboundRtp.powerEfficientDecoder,
				consecutiveTicks: this._consecutiveTicks,
			},
		});
	}

	private _clear(comment: string) {
		this._alertOn = false;

		const issue = this.trackMonitor.issues.get(this.issueKey);
		let payload: DecoderPerformanceIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as DecoderPerformanceIssuePayload),
				durationInMs: this._startedAt ? Date.now() - this._startedAt : undefined,
			};
		}

		this.trackMonitor.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedAt = undefined;
	}
}

```
### DownlinkCongestionDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DownlinkCongestionDetector.ts#L105)
Category: Transport Quality
```ts
import { Detector } from "./Detector";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { DecayingMaxEstimator } from "../utils/DecayingMaxEstimator";
import { FrugalQuantileEstimator } from "../utils/FrugalQuantileEstimator";

/** Noise floor: a 2ms buffer doubling to 4ms is arithmetic, not congestion. */
const MIN_JITTER_BUFFER_DELAY_IN_MS = 10;

/** Half-life of the recent-maximum memory, ~3 minutes. Per second, not per collection. */
const RECEIVING_BITRATE_DECAY_PER_SECOND = 0.996;

/**
 * How much the maximum's decay is multiplied by while an episode is still recent: this the
 * moment the episode closes, easing back to 1 across the window below. A path rarely gives
 * back all of what an episode took, and without it a second dip arriving inside that window
 * is scored against a capacity the path no longer reaches.
 */
const POST_EPISODE_DECAY_BOOST = 0.85;
const POST_EPISODE_FADE_WINDOW_IN_MS = 30_000;

/** Share of `minSeverity` the severity must fall under before an open finding closes. */
const RESOLVE_SEVERITY_FRACTION = 0.5;

export type DownlinkCongestionIssuePayload = {
	peerConnectionId: string;

	/**
	 * The two witnesses, each a fraction in `0..1` where `0` is healthy. `undershoot` of
	 * 0.75 means a quarter of what was recently arriving is arriving now; `bufferBloating`
	 * of 1 means frames are waiting at least four times their usual.
	 */
	undershoot: number;
	bufferBloating: number;

	/** How deep the trouble is, `0..1` — the geometric mean of the two witnesses. */
	severity: number;

	/** The measurements the ratios were taken from, in their own units. */
	receivingBitrate: number;
	recentMaxReceivingBitrate: number;
	avgJitterBufferDelayInMs: number;
	estimatedMedianJitterBufferDelayInMs: number;

	/** Filled in when the finding closes. */
	durationInMs?: number;
}

export type DownlinkCongestionDetectorConfig = {
	/** How deep the trouble has to be before reporting it, `0..1`. */
	minSeverity: number;

	/**
	 * Where `bufferBloating` reaches the top of its scale, as a multiple of the connection's own
	 * median jitter buffer delay. The library default is `4`: frames waiting four times their
	 * usual score `1`, and twice the median scores a third of the way up.
	 *
	 * A bloating buffer runs orders of magnitude past this, so the scale tops out early by
	 * design and the rest of the severity is carried by the undershoot. Raise it on a connection
	 * whose buffer is naturally variable; values at or below `1` make any excess score `1`.
	 */
	bufferBloatingSaturatesAt: number;
}

/**
 * Reports this endpoint's **receiving** path running out of room — the cause behind a far end
 * that pixelates and stalls while their camera and their encoder are both fine. Use it to tell
 * "this user's download is the problem" apart from the sender, the decoder, or a track nobody
 * is sending on.
 *
 * A finding means this user's own download ran short: a contended home link, a weak wireless
 * signal, a shaper. It explains why *every* remote participant looks bad to them at once, which is
 * what separates it from one sender having trouble.
 *
 * **There is no bandwidth estimate on a receiver.** `availableIncomingBitrate` is specified but
 * absent on Chrome, whose congestion control is send-side: the estimate for a downlink is computed
 * at the far end's sender and never reaches the receiver. So the verdict is built from two
 * witnesses, each a fraction of this connection's own normal:
 *
 * - `undershoot` — how far the arriving bitrate has fallen below the highest it recently
 *   reached.
 * - `bufferBloating` — how far the per-frame jitter buffer delay sits above its own running
 *   median, with `bufferBloatingSaturatesAt` times the median as the top of the scale, `4`
 *   by default.
 *
 * Their geometric mean rides on the finding as `severity` in `0..1`, opening at `minSeverity` and
 * closing under half of it. Being a geometric mean, a witness at its healthy level takes the
 * severity to zero, which is what separates a path out of room from **a far end asked for less** —
 * a muted camera, a dropped simulcast layer, a still screen share, each undershooting with the
 * buffer flat.
 *
 * Recovery rests on no bitrate threshold, because nothing at a receiver knows what the path can
 * carry now; the recent maximum decays instead, so a link that settles at half its former bandwidth
 * is judged against what it now has. It reads no `qualityLimitationReason`, which describes this
 * endpoint's *encoder* and would leave a receive-only connection permanently blind. Where there is
 * no inbound video, or no frame left the buffer, it says so rather than reading as healthy.
 *
 * Issue raised: `downlink-congestion`. Monitor events: `downlink-congestion`, and `congestion`
 * with `direction: 'downlink'`. Connection attribute: `PeerConnectionMonitor.downlinkCongested`.
 * Config: `downlinkCongestionDetector`.
 *
 * Category: Transport Quality
 * Layer: Capacity
 *
 */
export class DownlinkCongestionDetector implements Detector {
	public static readonly ISSUE_TYPE = 'downlink-congestion';
	public readonly name = 'downlink-congestion-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	/**
	 * The two baselines each witness is measured against — how they are fed is at the call
	 * site in `update()`.
	 */
	public readonly recentMaxReceivingBitrateEstimator = new DecayingMaxEstimator(RECEIVING_BITRATE_DECAY_PER_SECOND);
	public readonly medianJitterBufferDelayEstimator = new FrugalQuantileEstimator(0.5);

	private readonly _issueKey: string;
	private _raised = false;

	/** When the last episode closed, while the faster fade that follows it is still running. */
	private _boostedDecayAt?: number;

	/** Wall clock, and only for the resolved finding's `durationInMs`. */
	private _raisedAt?: number;

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
		this._issueKey = `${DownlinkCongestionDetector.ISSUE_TYPE}-pc-${peerConnection.peerConnectionId}`;
	}

	private get config() {
		return this.peerConnection.parent.config.downlinkCongestionDetector!;
	}

	public update() {
		if (this.disabled) return;

		// No inbound video, no buffer witness — judged on half the evidence is not judged.
		if (!this.peerConnection.hasInboundVideo) {
			return this._standDown('no inbound video on this connection');
		}

		const avgJitterBufferDelayInMs = this.peerConnection.avgInboundVideoJitterBufferDelayInMs;

		// Missing counters, or no frame left the buffer — a stall, not a path out of room.
		// Blind, not healthy.
		if (avgJitterBufferDelayInMs === undefined) {
			this.inputsUnavailable = true;
			this.peerConnection.downlinkVideoCongestionSeverity = undefined;

			return;
		}

		this.inputsUnavailable = false;

		const receivingBitrate = this.peerConnection.receivingBitrate;
		const recentMaxReceivingBitrate = this.recentMaxReceivingBitrateEstimator.estimate;
		const estimatedMedianJitterBufferDelayInMs = this.medianJitterBufferDelayEstimator.estimate;

		this._easePostEpisodeDecay();

		// Fed after the reads above, so a collection cannot move the baseline it is judged
		// against. The maximum takes every collection, an open episode included: a congested
		// sample is lower so it cannot inflate it, and feeding it is the only way it fades.
		this.recentMaxReceivingBitrateEstimator.update(receivingBitrate, this.peerConnection.deltaTime ?? 0);

		// The median takes only collections with no finding open, or a sustained bloat would
		// drag it up and talk the episode out of existence.
		if (!this._raised) this.medianJitterBufferDelayEstimator.update(avgJitterBufferDelayInMs);

		// One observation is enough for both baselines: the maximum starts as that sample and
		// the quantile as its own estimate, so a witness reads 0 rather than wrong.
		if (
			recentMaxReceivingBitrate === undefined ||
			estimatedMedianJitterBufferDelayInMs === undefined ||
			recentMaxReceivingBitrate <= 0
		) {
			return this._standDown('not enough history to judge congestion');
		}

		// Checked rather than defaulted: an absent scale makes the bloating `NaN`, and every
		// comparison below reads false against `NaN` — the finding would raise on everything.
		if (this.config.bufferBloatingSaturatesAt === undefined) return;

		// Clamped: a rising bitrate can overtake a maximum seeded from lower samples.
		const undershoot = Math.max(0, 1 - (receivingBitrate / recentMaxReceivingBitrate));

		const bufferBaselineInMs = Math.max(estimatedMedianJitterBufferDelayInMs, MIN_JITTER_BUFFER_DELAY_IN_MS);
		// Never zero, so a `saturatesAt` of 1 or less saturates on any excess instead of dividing by it.
		const bufferBloatingSpan = Math.max(this.config.bufferBloatingSaturatesAt - 1, Number.EPSILON);
		const bufferBloating = Math.min(1, Math.max(0,
			(avgJitterBufferDelayInMs - bufferBaselineInMs) / (bufferBaselineInMs * bufferBloatingSpan),
		));

		// Geometric mean: a witness at its healthy level takes the whole thing to zero.
		const severity = Math.sqrt(undershoot * bufferBloating);

		this.peerConnection.downlinkVideoCongestionSeverity = severity;

		if (this._raised) {
			if (!(severity >= this.config.minSeverity * RESOLVE_SEVERITY_FRACTION)) {
				this._resolve('the undershoot and the buffer bloating have both eased');
			}

			return;
		}

		// Written to fail closed: `severity < undefined` is false, and would raise on everything.
		// Checked rather than compared against: `severity < undefined` is false, so a bare
		// comparison would raise on every collection where the config arrived without it. The
		// resolve above is left as a `>=` negation on purpose — with no threshold it reads true
		// and closes the finding, which is the safe direction for a verdict that cannot be made.
		if (this.config.minSeverity === undefined) return;
		if (severity < this.config.minSeverity) return;

		this._raise({
			peerConnectionId: this.peerConnection.peerConnectionId,
			undershoot,
			bufferBloating,
			severity,
			receivingBitrate,
			recentMaxReceivingBitrate,
			avgJitterBufferDelayInMs,
			estimatedMedianJitterBufferDelayInMs,
		});
	}

	/**
	 * Moves the maximum's decay along the post-episode window: fastest the moment the episode
	 * closed, easing back to the ordinary rate across the window, and back to it outright once
	 * past. Does nothing when no episode is recent.
	 */
	private _easePostEpisodeDecay() {
		if (this._boostedDecayAt === undefined) return;

		const sinceResolveInMs = this.peerConnection.statsClockTime - this._boostedDecayAt;

		if (POST_EPISODE_FADE_WINDOW_IN_MS <= sinceResolveInMs) {
			this._boostedDecayAt = undefined;

			return this.recentMaxReceivingBitrateEstimator.updateDecayRate(RECEIVING_BITRATE_DECAY_PER_SECOND);
		}

		const fadedBack = sinceResolveInMs / POST_EPISODE_FADE_WINDOW_IN_MS;
		const boost = POST_EPISODE_DECAY_BOOST + ((1 - POST_EPISODE_DECAY_BOOST) * fadedBack);

		this.recentMaxReceivingBitrateEstimator.updateDecayRate(RECEIVING_BITRATE_DECAY_PER_SECOND * boost);
	}

	private _raise(payload: DownlinkCongestionIssuePayload) {
		this._raised = true;
		this._raisedAt = Date.now();
		// Set here, not at the call sites, so the flag and the finding cannot drift.
		this.peerConnection.downlinkCongested = true;

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('downlink-congestion', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			...payload,
		});

		// The same finding again on the direction-agnostic feed. One issue, two deliveries.

		this.peerConnection.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: DownlinkCongestionDetector.ISSUE_TYPE,
			payload,
		});
	}

	/** Closes any open finding. Guarded, because this is every audio-only connection's resting state. */
	private _standDown(comment: string) {
		this.inputsUnavailable = false;
		this.peerConnection.downlinkVideoCongestionSeverity = undefined;

		if (this._raised) this._resolve(comment);
	}

	private _resolve(comment: string) {
		this._raised = false;
		this._boostedDecayAt = this.peerConnection.statsClockTime;
		this.peerConnection.downlinkCongested = false;

		const issue = this.peerConnection.issues.get(this._issueKey);

		this.peerConnection.issues.resolve({
			key: this._issueKey,
			comment,
			payload: issue
				? {
					...(issue.payload as DownlinkCongestionIssuePayload),
					durationInMs: this._raisedAt === undefined ? undefined : Date.now() - this._raisedAt,
				}
				: undefined,
			resolvedAt: Date.now(),
		});

		this._raisedAt = undefined;
	}
}

```
### DryInboundTrackDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DryInboundTrackDetector.ts#L39)
Category: Pipeline Disruption
```ts
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";
import { Detector } from "./Detector";

export type DryInboundTrackIssuePayload = {
	trackId: string;
	/** How long the track had already been dry when the issue was raised, in milliseconds of stats time. */
	duration: number;
	/** How long the episode lasted; filled in when the issue is resolved. */
	durationInMs?: number;
}

export type DryInboundTrackDetectorConfig = {
	/** How long (ms of stats time) an inbound track must be dry before it counts as stalled. */
	thresholdInMs: number;
}

/**
 * Reports one inbound track receiving zero bytes tick after tick — "their video is frozen" and "I
 * cannot hear them" at their most literal. Use it to catch the transmission failures that leave the
 * quality detectors quiet precisely because nothing is left to measure.
 *
 * A finding means delivery for this one track stopped while the connection itself stayed up: an
 * SFU that stopped forwarding, a producer that died, or a consumer wired to nothing. A connection
 * losing every track at once is a transport fault and belongs to the connectivity detectors.
 *
 * Silence is only a fault when unexplained: a paused consumer or a paused remote producer discards
 * the timer and resolves an open issue, naming which one it saw. A stall must last `thresholdInMs`
 * of the stream's own stats time — not wall clock, which would count the library's own late
 * collection towards the threshold — and is raised once per episode, not once per tick.
 *
 * Raises `dry-inbound-track`. Emits `dry-inbound-track`.
 * Track attribute: `InboundTrackMonitor.dry`.
 * Config: `dryInboundTrackDetector`.
 *
 * Category: Pipeline Disruption
 * Layer: Receive — the wire to the track
 *
 */
export class DryInboundTrackDetector implements Detector {
	public static readonly ISSUE_TYPE = 'dry-inbound-track';
	public readonly name = 'dry-inbound-track-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly issueKey: string;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this.issueKey = `${DryInboundTrackDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private _startedDryAt?: number;

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	private get config() {
		return this.peerConnection.parent.config.dryInboundTrackDetector!;
	}

	/** Stats time accumulated over the current dry stretch; `0` whenever the silence is explained or over. */
	private _dryForInMs = 0;

	public update() {
		if (this.disabled) {
			this.trackMonitor.dry = undefined;

			return;
		}
		if (this.trackMonitor.readyState !== 'live') {
			this.trackMonitor.dry = undefined;
			this._dryForInMs = 0;
			if (this._startedDryAt !== undefined) {
				this._resolve('track ended');
			}
			return;
		}

		// A paused end legitimately sends nothing, so there is no silence to judge.
		if (this.trackMonitor.paused || this.trackMonitor.remoteOutboundTrackPaused) {
			this.trackMonitor.dry = undefined;
			this._dryForInMs = 0;
			if (this._startedDryAt !== undefined) {
				this._resolve(this.trackMonitor.paused ? 'consumer paused' : 'remote track paused');
			}
			return;
		}

		const inboundRtp = this.trackMonitor.getInboundRtp();

		// No counter at all is blind; a non-zero one is bytes arriving, which is health.
		if (inboundRtp?.deltaBytesReceived === undefined) {
			this.trackMonitor.dry = undefined;
		}

		if (inboundRtp?.deltaBytesReceived !== 0) {
			if (inboundRtp?.deltaBytesReceived !== undefined) this.trackMonitor.dry = false;
			this._dryForInMs = 0;
			if (this._startedDryAt !== undefined) {
				this._resolve('dry inbound track recovered');
			}
			return;
		}

		// Zero bytes, but not yet long enough to be a fault: judged, and not yet wrong.
		this.trackMonitor.dry = false;

		this._dryForInMs += inboundRtp.deltaTime ?? 0;

		const duration = this._dryForInMs;
		const clientMonitor = this.peerConnection.parent;

		if (duration < this.config.thresholdInMs) return;

		if (this._startedDryAt !== undefined) return;

		clientMonitor.emit('dry-inbound-track', {
			trackMonitor: this.trackMonitor,
			clientMonitor: clientMonitor,
		});

		this._raise({
			trackId: this.trackMonitor.track.id,
			duration,
		});
	}

	private _raise(payload: DryInboundTrackIssuePayload) {
		// Set here, not at the call site, so the flag and the finding cannot drift.
		this.trackMonitor.dry = true;
		this._startedDryAt = Date.now();

		this.trackMonitor.issues.raise({
				key: this.issueKey,
				includeInSample: this.includeIssueInSample,
			type: DryInboundTrackDetector.ISSUE_TYPE,
			payload,
		});
	}

	private _resolve(comment?: string) {
		const issue = this.trackMonitor.issues.get(this.issueKey);
		let payload: DryInboundTrackIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as DryInboundTrackIssuePayload),
				durationInMs: this._startedDryAt ? Date.now() - this._startedDryAt : undefined,
			};
		}

		this.trackMonitor.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedDryAt = undefined;
	}
}
```
### DryOutboundTrackDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DryOutboundTrackDetector.ts#L78)
Category: Pipeline Disruption
```ts
import { OutboundTrackMonitor } from "../monitors/OutboundTrackMonitor";
import { Detector } from "./Detector";

export type DryOutboundTrackIssuePayload = {
	trackId: string;

	/**
	 * Milliseconds of stats time the track had already been dry when the issue was raised — the
	 * stretch that earned the finding, which is at least `thresholdInMs`.
	 *
	 * Not to be confused with `durationInMs` below, which was called `duration` here until the two
	 * names proved impossible to tell apart in a sample: one is how long the fault had lasted
	 * *before* it was reported, the other how long the report stayed open.
	 */
	dryForInMs: number;

	/** How many of this track's layers were sending nothing, and how many were being driven at all. */
	activeLayers: number;

	/** How long the issue was open, in wall-clock ms. Filled in when it resolves. */
	durationInMs?: number;
}
export type DryOutboundTrackIssueType = 'dry-outbound-track';

export type DryOutboundTrackDetectorConfig = {
	/** How long (ms of stats time) an outbound track must be dry before it counts as stalled. */
	thresholdInMs: number;
}

/**
 * Reasons the browser gives for holding an encoder back that *explain* silence, and so stand this
 * detector down.
 *
 * A sender that has stopped because there is no bandwidth, or no CPU, has not broken: it is doing
 * what it is supposed to do under pressure, and the pressure itself is already reported by
 * `uplink-congestion` and `cpulimitation`. Calling it a pipeline disruption on top would price the
 * same condition twice — and worse, point an operator at the capture chain when the answer is the
 * uplink. `other` is deliberately not here: it is the browser declining to say why, which is not an
 * explanation.
 */
const EXPLAINED_LIMITATIONS: ReadonlySet<string> = new Set([ 'bandwidth', 'cpu' ]);

/**
 * The sending-side counterpart: reports one outbound track sending zero bytes tick after tick — a
 * stalled encoder, a capture source that quietly stopped feeding it, or a sender that never really
 * started. Use it for the one failure the local user cannot see for themselves, since their own
 * preview keeps rendering.
 *
 * **It judges the track, which means every layer it is being sent over.** A simulcast track sends
 * across several RTP streams and the sender moves between them constantly: congestion makes the
 * encoder drop the top layer, and an application or an SFU switches layers off outright. Either
 * leaves one stream's counters frozen while the picture keeps going out over another, so a verdict
 * taken from a single stream is a verdict about a layer rather than about the track. Reading one
 * arbitrary stream reported a 640x360 camera as dry for fourteen minutes while the layer beside it
 * sent a hundred kilobytes every collection.
 *
 * Layers the sender is not driving are left out rather than counted as silence: an `active: false`
 * stream is switched off by design, and its counters stay where they stopped for the rest of the
 * call. A track whose layers are *all* inactive is not being sent at all, which is a stand-down and
 * not a fault — and it is also what keeps this detector able to close a finding it opened, since a
 * frozen counter can never differ from itself.
 *
 * A paused sender, a muted track, a track no longer `live`, or the browser reporting the encoder
 * limited by `bandwidth` or `cpu` all explain the silence: any of them discards the timer and
 * resolves an open issue. The limitation cases matter most on a bad network, where the sender stops
 * because it has been told to rather than because anything broke — and where `uplink-congestion`
 * and `cpulimitation` are already reporting the real condition. A stall must last `thresholdInMs` of the sender's
 * own stats time — a busy main thread that collects late would otherwise be counted as evidence for
 * a stalled encoder — and is raised once per episode, not once per tick.
 *
 * Raises `dry-outbound-track`. Emits `dry-outbound-track`. Config: `dryOutboundTrackDetector`.
 * Track attribute: `OutboundTrackMonitor.dry`.
 *
 * Category: Pipeline Disruption
 * Layer: Send — RTP sender to the wire
 *
 */
export class DryOutboundTrackDetector implements Detector {
	public static readonly ISSUE_TYPE: DryOutboundTrackIssueType = 'dry-outbound-track';

	public readonly name = 'dry-outbound-track-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly issueKey: string;

	public constructor(
		public readonly trackMonitor: OutboundTrackMonitor,
	) {
		this.issueKey = `${DryOutboundTrackDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private _startedDryAt?: number;

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	private get config() {
		return this.peerConnection.parent.config.dryOutboundTrackDetector!;
	}

	/** Stats time accumulated over the current dry stretch; `0` whenever the silence is explained or over. */
	private _dryForInMs = 0;

	public update() {
		if (this.disabled) {
			this.trackMonitor.dry = undefined;

			return;
		}

		// A paused, muted or dead track legitimately sends nothing.
		if (this.trackMonitor.paused || this.trackMonitor.track.muted || this.trackMonitor.track.readyState !== 'live') {
			this.trackMonitor.dry = undefined;
			this._dryForInMs = 0;
			if (this._startedDryAt !== undefined) {
				this._resolve('track paused, muted or not live');
			}
			return;
		}

		// Only the layers the sender is driving. A deactivated one sends nothing by design and its
		// counters never move again, so counting it as silence both invents a fault and makes the
		// finding it invents impossible to close.
		const activeRtps = this.trackMonitor.getOutboundRtps()
			.filter((outboundRtp) => outboundRtp.active !== false);

		// The browser saying why it is holding the encoder back is an explanation for the silence,
		// and this detector only reports silence that has none. Read from the layers rather than
		// from the connection: another track on the same peer connection may be the limited one.
		const limitation = activeRtps
			.map((outboundRtp) => outboundRtp.qualityLimitationReason)
			.find((reason) => reason !== undefined && EXPLAINED_LIMITATIONS.has(reason));

		if (limitation !== undefined) {
			this.trackMonitor.dry = undefined;
			this._dryForInMs = 0;

			if (this._startedDryAt !== undefined) {
				this._resolve(`the encoder is limited by ${limitation}`);
			}

			return;
		}

		if (activeRtps.length === 0) {
			this.trackMonitor.dry = undefined;
			this._dryForInMs = 0;

			if (this._startedDryAt !== undefined) {
				this._resolve('no layer of this track is being sent');
			}

			return;
		}

		let deltaBytesSent: number | undefined;
		let deltaTime: number | undefined;

		// Summed across the layers: the track is dry only when every one of them is.
		for (const outboundRtp of activeRtps) {
			if (outboundRtp.deltaBytesSent !== undefined) {
				deltaBytesSent = (deltaBytesSent ?? 0) + outboundRtp.deltaBytesSent;
			}
			if (deltaTime === undefined) deltaTime = outboundRtp.deltaTime;
		}

		// No counter on any layer is blind, which is not the same as silent.
		if (deltaBytesSent === undefined) {
			this.trackMonitor.dry = undefined;

			return;
		}

		if (deltaBytesSent !== 0) {
			this.trackMonitor.dry = false;
			this._dryForInMs = 0;

			if (this._startedDryAt !== undefined) {
				this._resolve('dry outbound track recovered');
			}

			return;
		}

		// Zero bytes, but not yet long enough to be a fault: judged, and not yet wrong.
		this.trackMonitor.dry = false;

		this._dryForInMs += deltaTime ?? 0;

		const dryForInMs = this._dryForInMs;

		if (dryForInMs < this.config.thresholdInMs) return;

		if (this._startedDryAt !== undefined) return;


		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('dry-outbound-track', {
			trackMonitor: this.trackMonitor,
			clientMonitor: clientMonitor,
		});

		this._raise({
			trackId: this.trackMonitor.track.id,
			dryForInMs,
			activeLayers: activeRtps.length,
		});
	}

	private _raise(payload: DryOutboundTrackIssuePayload) {
		// Set here, not at the call site, so the flag and the finding cannot drift.
		this.trackMonitor.dry = true;
		this._startedDryAt = Date.now();

		// The track's own registry, never the client's: it forwards up, and resolving anywhere
		// else would leave this copy standing for the rest of the call.
		this.trackMonitor.issues.raise({
			key: this.issueKey,
			includeInSample: this.includeIssueInSample,
			type: DryOutboundTrackDetector.ISSUE_TYPE,
			payload,
		});
	}

	private _resolve(comment?: string) {
		const issue = this.trackMonitor.issues.get(this.issueKey);
		let payload: DryOutboundTrackIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as DryOutboundTrackIssuePayload),
				durationInMs: this._startedDryAt ? Date.now() - this._startedDryAt : undefined,
			};
		}

		// Same registry the raise went to, so both copies close together.
		this.trackMonitor.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedDryAt = undefined;
	}
}
```
### DtlsHandshakeFailedDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DtlsHandshakeFailedDetector.ts#L38)
Category: Connectivity
```ts
import { IceTransportMonitor } from "../monitors/IceTransportMonitor";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

export type DtlsHandshakeFailedIssuePayload = {
	peerConnectionId: string;
	transportId: string;
	dtlsState?: string;
	iceState?: string;
	selectedCandidatePairId?: string;
	/** Filled in when the issue is resolved. */
	durationInMs?: number;
};

const ISSUE_TYPE = 'dtls-handshake-failed';

/** No tunables — a terminal state needs no threshold. `{}` enables the detector, `null` disables it. */
export type DtlsHandshakeFailedDetectorConfig = Record<string, never>;

/**
 * Reports `dtlsState` reading `failed`: the secure transport refusing to come up over a network
 * path that works. Use it to separate this from an ICE failure one layer below — a mismatched
 * certificate fingerprint, a peer that speaks no offered DTLS version, a middlebox that passes
 * STUN and drops handshake records — where the whole class would otherwise present as a peer
 * connection generically slow to leave `connecting`.
 *
 * `failed` is terminal, so the issue is raised on the first tick that reports it, once per
 * transport. Only a later `connected` resolves it — in practice an ICE restart that re-keyed the
 * transport; a drop back to `new`/`connecting` is not yet evidence of anything.
 *
 * Raises `dtls-handshake-failed`. Emits `dtls-handshake-failed`.
 * Config: `dtlsHandshakeFailedDetector`.
 *
 * Category: Connectivity
 * Layer: 4 — Secure transport
 *
 */
export class DtlsHandshakeFailedDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'dtls-handshake-failed-detector';
	public disabled = false;
	public includeIssueInSample = true;

	/** Transport id → raise time. Only raised transports are in here. */
	private readonly _raisedAt = new Map<string, number>();

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) return;

		for (const transport of this.peerConnection.iceTransports) {
			this._checkTransport(transport);
		}

		for (const transportId of [ ...this._raisedAt.keys() ]) {
			if (this.peerConnection.iceTransports.some((transport) => transport.id === transportId)) continue;

			this._resolve(transportId, 'ice transport is gone');
		}
	}

	private _checkTransport(transport: IceTransportMonitor) {
		const dtlsState = transport.dtlsState;

		if (dtlsState === 'connected') {
			// The only way out of `failed`: an ICE restart re-keyed the transport.
			return this._resolve(transport.id, 'dtls handshake completed');
		}

		if (dtlsState !== 'failed') return;
		if (this._raisedAt.has(transport.id)) return;

		this._raisedAt.set(transport.id, Date.now());

		const payload: DtlsHandshakeFailedIssuePayload = {
			peerConnectionId: this.peerConnection.peerConnectionId,
			transportId: transport.id,
			dtlsState,
			iceState: transport.iceState,
			selectedCandidatePairId: transport.selectedCandidatePairId,
		};

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('dtls-handshake-failed', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			...payload,
		});

		this.peerConnection.issues.raise({
				key: this._issueKey(transport.id),
				includeInSample: this.includeIssueInSample,
				type: ISSUE_TYPE,
				payload,
			}
		);
	}

	private _resolve(transportId: string, comment: string) {
		const raisedAt = this._raisedAt.get(transportId);

		if (raisedAt === undefined) return;

		this._raisedAt.delete(transportId);

		const key = this._issueKey(transportId);
		const issue = this.peerConnection.issues.get(key);

		if (!issue) return;

		this.peerConnection.issues.resolve({
			key: key,
			comment,
			payload: {
				...(issue.payload as DtlsHandshakeFailedIssuePayload),
				durationInMs: Date.now() - raisedAt,
			},
			resolvedAt: Date.now(),
		});
	}

	private _issueKey(transportId: string) {
		return `${ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}-transport-${transportId}`;
	}
}

```
### DtlsHandshakeStalledDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DtlsHandshakeStalledDetector.ts#L61)
Category: Connectivity
```ts
import { IceTransportMonitor } from "../monitors/IceTransportMonitor";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

/** How the detector proved the ICE side healthy before judging DTLS. */
export type DtlsIceEvidence =
	/** The transport reported `iceState` `connected`/`completed`. */
	| 'transport-ice-state'
	/** No `iceState` reported (Safari), so a `succeeded` selected pair stood in for it. */
	| 'selected-pair-succeeded';

export type DtlsHandshakeStalledIssuePayload = {
	peerConnectionId: string;
	transportId: string;
	dtlsState?: string;
	iceState?: string;
	iceEvidence: DtlsIceEvidence;
	selectedCandidatePairId?: string;
	/** How long DTLS had already sat in `new`/`connecting` when the issue was raised. */
	stalledForMs: number;
	/** Filled in when the issue is resolved. */
	durationInMs?: number;
};

type TransportState = {
	/** Update ticks this transport has been observed for — the first tick is never judged. */
	ticks: number;
	usernameFragment?: string;
	/** Stats time accumulated while ICE was healthy and DTLS was not, reset whenever that breaks. */
	stalledForInMs: number;
	raisedAt?: number;
};

const ISSUE_TYPE = 'dtls-handshake-stalled';

export type DtlsHandshakeStalledDetectorConfig = {
	/** How long DTLS may stay in `new`/`connecting` over a healthy ICE side before raising, in ms. */
	stalledThresholdInMs: number;
}

/**
 * Reports a DTLS handshake that never answers: the ICE side of the transport is demonstrably
 * working while `dtlsState` sits in `new` or `connecting` and stays there. Use it to tell a
 * handshake eaten by a middlebox from one the browser has actually failed — its sibling
 * `DtlsHandshakeFailedDetector` reports that verdict; only duration separates the two here.
 *
 * ICE must be proven healthy first, since DTLS cannot complete over an unusable path and the ICE
 * detectors already own that case. Proof comes from the transport's `iceState`, or from a
 * `succeeded` selected pair where no `iceState` is reported, and `iceEvidence` records which. The
 * clock is stats time, and it resets whenever the condition ends or an ICE restart re-keys DTLS,
 * which is what a changed local username fragment marks. The first observed tick is never judged,
 * because some browsers report pre-negotiation transport values.
 *
 * Raises `dtls-handshake-stalled`. Emits `dtls-handshake-stalled`.
 * Config: `dtlsHandshakeStalledDetector`.
 *
 * Category: Connectivity
 * Layer: 4 — Secure transport
 *
 */
export class DtlsHandshakeStalledDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'dtls-handshake-stalled-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _states = new Map<string, TransportState>();

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.dtlsHandshakeStalledDetector!;
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) return;

		for (const transport of this.peerConnection.iceTransports) {
			this._checkTransport(transport);
		}

		for (const transportId of [ ...this._states.keys() ]) {
			if (this.peerConnection.iceTransports.some((transport) => transport.id === transportId)) continue;

			this._resolve(transportId, 'ice transport is gone');
			this._states.delete(transportId);
		}
	}

	private _checkTransport(transport: IceTransportMonitor) {
		const state = this._getState(transport);
		const ticks = state.ticks;

		state.ticks += 1;

		// An ICE restart re-keys DTLS: the stall clock must restart with the new generation.
		const usernameFragment = this._usernameFragmentOf(transport);

		if (usernameFragment !== undefined && state.usernameFragment !== undefined
			&& usernameFragment !== state.usernameFragment) {
			state.stalledForInMs = 0;
		}
		if (usernameFragment !== undefined) state.usernameFragment = usernameFragment;

		const dtlsState = transport.dtlsState;

		if (dtlsState === 'connected') {
			state.stalledForInMs = 0;

			this._resolve(transport.id, 'dtls handshake completed');

			return;
		}

		if (dtlsState === 'failed') {
			// Terminal, and `DtlsHandshakeFailedDetector`'s to report.
			state.stalledForInMs = 0;

			this._resolve(transport.id, 'dtls handshake failed');

			return;
		}

		// 'closed' is a shutdown, not a failure; and without a dtlsState there is nothing to judge.
		if (dtlsState !== 'new' && dtlsState !== 'connecting') {
			state.stalledForInMs = 0;

			return;
		}

		// Never judge a first tick: some browsers report pre-negotiation transport values.
		if (ticks < 1) return;

		const iceEvidence = this._iceHealthEvidence(transport);

		if (iceEvidence === undefined) {
			// ICE is not proven healthy, so the ICE detectors own whatever is wrong.
			state.stalledForInMs = 0;

			return;
		}

		state.stalledForInMs += transport.deltaTime ?? 0;

		if (state.stalledForInMs < this.config.stalledThresholdInMs) return;
		if (state.raisedAt !== undefined) return;

		state.raisedAt = Date.now();

		const payload: DtlsHandshakeStalledIssuePayload = {
			peerConnectionId: this.peerConnection.peerConnectionId,
			transportId: transport.id,
			dtlsState,
			iceState: transport.iceState,
			iceEvidence,
			selectedCandidatePairId: transport.selectedCandidatePairId,
			stalledForMs: state.stalledForInMs,
		};

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('dtls-handshake-stalled', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			...payload,
		});

		this.peerConnection.issues.raise({
				key: this._issueKey(transport.id),
				includeInSample: this.includeIssueInSample,
				type: ISSUE_TYPE,
				payload,
			}
		);
	}

	/** Proof the ICE side is healthy. `undefined` means no proof, not proof of the opposite. */
	private _iceHealthEvidence(transport: IceTransportMonitor): DtlsIceEvidence | undefined {
		const iceState = transport.iceState;

		if (iceState === 'connected' || iceState === 'completed') return 'transport-ice-state';
		if (iceState !== undefined) return undefined;

		return transport.getSelectedCandidatePair()?.state === 'succeeded'
			? 'selected-pair-succeeded'
			: undefined;
	}

	private _usernameFragmentOf(transport: IceTransportMonitor): string | undefined {
		return transport.iceLocalUsernameFragment
			?? transport.getSelectedCandidatePair()?.getLocalCandidate()?.usernameFragment;
	}

	private _getState(transport: IceTransportMonitor): TransportState {
		let state = this._states.get(transport.id);

		if (!state) {
			state = {
				ticks: 0,
				usernameFragment: this._usernameFragmentOf(transport),
				stalledForInMs: 0,
			};
			this._states.set(transport.id, state);
		}

		return state;
	}

	private _resolve(transportId: string, comment: string) {
		const state = this._states.get(transportId);

		if (state?.raisedAt === undefined) return;

		const raisedAt = state.raisedAt;

		state.raisedAt = undefined;

		const key = this._issueKey(transportId);
		const issue = this.peerConnection.issues.get(key);

		if (!issue) return;

		this.peerConnection.issues.resolve({
			key: key,
			comment,
			payload: {
				...(issue.payload as DtlsHandshakeStalledIssuePayload),
				durationInMs: Date.now() - raisedAt,
			},
			resolvedAt: Date.now(),
		});
	}

	private _issueKey(transportId: string) {
		return `${ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}-transport-${transportId}`;
	}
}

```
### EncoderBottleneckDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/EncoderBottleneckDetector.ts#L113)
Category: Pipeline Disruption
```ts
import { Detector } from "./Detector";
import type { OutboundTrackMonitor } from "../monitors/OutboundTrackMonitor";

/**
 * What the detector measured about the encoder in the window that raised the issue.
 *
 * Every field not marked optional is always present: the detector cannot reach the raise without
 * it. The track's own `readyState` and `muted` are not carried, because the detector only raises
 * on a track that is live, unmuted and enabled, so they could only ever read `'live'` and `false`.
 */
export type EncoderBottleneckIssuePayload = {
	peerConnectionId: string;
	trackId: string;

	/** The average frames per second the media source handed the encoder over the detection window. */
	producedFpsForDetection: number;

	/** The number of frames the media source handed the encoder over the detection window. */
	producedFramesForDetection: number;

	/** The average frames per second the highest layer encoded over the detection window. */
	encodedFpsForDetection: number;

	/** The number of frames the highest layer encoded over the detection window. */
	encodedFramesForDetection: number;

	/** The milliseconds of stats time the detection window spanned. */
	detectionWindowInMs: number;

	/**
	 * The share of the frames handed over that the encoder did not encode,
	 * `1 - encodedFpsForDetection / producedFpsForDetection`. Zero is an encoder keeping up with its
	 * source and one is an encoder emitting nothing; an encoder ahead of the source, which counters
	 * read a frame apart can produce, reports a negative.
	 */
	encodeDegradation: number;

	/** What the browser said was limiting the encoder when the issue opened. */
	qualityLimitationReason?: string;

	/** Which encoder was running, and whether the browser called it power efficient. */
	encoderImplementation?: string;
	powerEfficientEncoder?: boolean;

	// Written at resolution, from the recovery window that ended the issue. Absent when it was
	// resolved by a stand-down instead, where nothing was measured.

	/** The milliseconds of stats time the recovery window spanned. */
	recoveryWindowInMs?: number;

	/** The average frames per second the media source handed over during the recovery window. */
	producedFpsForRecovery?: number;

	/** The number of frames the media source handed over during the recovery window. */
	producedFramesForRecovery?: number;

	/** The average frames per second the highest layer encoded during the recovery window. */
	encodedFpsForRecovery?: number;

	/** The number of frames the highest layer encoded during the recovery window. */
	encodedFramesForRecovery?: number;
}

export type EncoderBottleneckIssueType = 'encoder-bottleneck';

export type EncoderBottleneckDetectorConfig = {
	/**
	 * The share of the frames handed to the encoder that it may fail to encode before the issue is
	 * raised, and must return to before it resolves.
	 */
	encodeDegradationThreshold: number;
}


/**
 * Given a capture source that is delivering, is the encoder keeping up with it? Use it to tell a
 * struggling encoder apart from a starving camera, which is `VideoCaptureBottleneckDetector`'s
 * subject. The send-side mirror of `DecoderPerformanceDetector`.
 *
 * Both counters come from `OutboundTrackMonitor.slicedWindow`: the frames the media
 * source produced and the frames the highest layer encoded, each measured across the same stretch.
 * The detection window raises — leaving more than `encodeDegradationThreshold` of the frames handed
 * over unencoded opens the issue, and every later collection still short of it updates that issue
 * rather than opening another. The recovery window resolves: the issue ends only once the stretch
 * *before* the detection window is back within the threshold, so an encoder hovering at the line
 * cannot flap one long fault into a stream of short ones. Neither window is read before it says it
 * is ready.
 *
 * The comparison is always against what the source actually delivered, never the configured frame
 * rate, so a starving camera cannot make the encoder look guilty — handed nothing, it has nothing
 * to answer for and the detector stands down. That is also why screen shares are judged like any
 * other track: their frame rate follows the content, and the encoder is still expected to keep up
 * with whatever it is given.
 *
 * A finding means the frames existed and the encoder did not get through them: too much resolution
 * for the machine, a software codec where hardware was expected, or the CPU taken by something
 * else. `qualityLimitationReason` and `encoderImplementation` are carried for that diagnosis.
 *
 * It stands down — reporting `undefined` rather than a verdict — for a backgrounded tab, a paused
 * sender, a track that is not live, unmuted and enabled, a capture format that just changed, a
 * track with no active layer, and a window in which the source handed over nothing.
 *
 * Issue raised: `encoder-bottleneck`, updated while it stays open, resolved on recovery or on a
 * stand-down. No monitor event.
 * Config: `encoderBottleneckDetector`.
 * Track attribute: `OutboundTrackMonitor.degradedEncodingPerformance`.
 *
 * Category: Pipeline Disruption
 * Layer: Send — frames to encoder
 *
 */

export class EncoderBottleneckDetector implements Detector {
	public static readonly ISSUE_TYPE: EncoderBottleneckIssueType = 'encoder-bottleneck';

	public readonly name = 'encoder-bottleneck-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _issueKey: string;
	private _raised = false;

	public constructor(
		public readonly trackMonitor: OutboundTrackMonitor,
	) {
		this._issueKey = `${EncoderBottleneckDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;

		// Read without the getter's non-null assertion: a monitor builds this detector whenever the
		// key is not explicitly `null`, which includes a config that never mentioned it at all.
		const config = this.peerConnection.parent.config.encoderBottleneckDetector;

		if (config && config.encodeDegradationThreshold < 0) {
			this.peerConnection.parent.logger.warn(
				'encoderBottleneckDetector.encodeDegradationThreshold must not be below 0, got '
				+ config.encodeDegradationThreshold
			);
			config.encodeDegradationThreshold = 0;
		}
	}

	private get config(): EncoderBottleneckDetectorConfig {
		return this.peerConnection.parent.config.encoderBottleneckDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) {
			this.trackMonitor.degradedEncodingPerformance = undefined;

			return;
		}
		const track = this.trackMonitor.track;

		if (!this.peerConnection.parent.activeTab) return this._clear({
			comment: 'tab in background',
		});
		if (this.trackMonitor.paused) return this._clear({
			comment: 'track paused',
		});
		if (track.readyState !== 'live' || track.muted || !track.enabled) return this._clear({
			comment: 'track not sending',
		});

		// The track monitor read the settings once for every detector on this track and already said
		// whether the capture format moved. A new frame size changes what encoding costs, so the
		// collections either side of it are not comparable.
		if (this.trackMonitor.videoCaptureSettingsChanged) return this._clear({
			comment: 'capture settings changed',
		});

		const highestLayer = this.trackMonitor.highestLayer;

		// No layer is nothing to hold responsible: a track sending nothing at all is
		// `DryOutboundTrackDetector`'s subject, not this one's.
		if (!highestLayer || highestLayer.active === false) return this._clear({
			comment: 'no active layer',
		});

		const {
			detection: detectionWindow,
			recovery: recoveryWindow,
		} = this.trackMonitor.slicedWindow.slices;
		const producedFramesForDetection = detectionWindow.deltaMediaSourceTotalProducedFrames;
		const encodedFramesForDetection = detectionWindow.deltaHighestLayerTotalEncodedFrames;
		const detectionWindowInMs = detectionWindow.durationInMs;

		if (producedFramesForDetection === null) return this._clear({
			comment: 'no source frames in window',
		});
		if (encodedFramesForDetection === null) return this._clear({
			comment: 'no encoded frames in window',
		});
		if (!detectionWindow.isReady || detectionWindowInMs < 1) return;

		const producedFpsForDetection = producedFramesForDetection / (detectionWindowInMs / 1000);
		const encodedFpsForDetection = encodedFramesForDetection / (detectionWindowInMs / 1000);

		// Nothing handed over is nothing to encode, and no denominator to take a share of.
		if (producedFpsForDetection <= 0) return this._clear({
			comment: 'source handed over no frames',
		});

		const encodeDegradation = 1 - (encodedFpsForDetection / producedFpsForDetection);

		// Beside the flag and the issue: the measurement itself, on every judged collection, so the
		// score calculator has a continuous number below the threshold as well as above it.
		this.trackMonitor.videoEncodingDegradation = encodeDegradation;

		if (this.config.encodeDegradationThreshold < encodeDegradation) {
			if (!this._raised) return this._raiseIssue({
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: track.id,
				encodeDegradation,
				producedFpsForDetection,
				producedFramesForDetection,
				encodedFpsForDetection,
				encodedFramesForDetection,
				detectionWindowInMs,
				qualityLimitationReason: highestLayer.qualityLimitationReason,
				encoderImplementation: highestLayer.encoderImplementation,
				powerEfficientEncoder: highestLayer.powerEfficientEncoder,
			});

			return this.trackMonitor.issues.update({
				key: this._issueKey,
				payload: {
					encodeDegradation,
				},
			});
		}

		// Below the threshold with nothing open: the encoder was judged and found to be keeping up,
		// which is not the same as not having been judged at all.
		if (!this._raised) return this._clear({
			comment: 'encoder keeping up',
			degradedEncodingPerformance: false,
		});

		// Below the threshold with a finding open: the recovery window decides whether it ends.

		const producedFramesForRecovery = recoveryWindow.deltaMediaSourceTotalProducedFrames;
		const encodedFramesForRecovery = recoveryWindow.deltaHighestLayerTotalEncodedFrames;
		const recoveryWindowInMs = recoveryWindow.durationInMs;

		if (
			!recoveryWindow.isReady ||
			producedFramesForRecovery === null ||
			encodedFramesForRecovery === null ||
			recoveryWindowInMs < 1
		) {
			return this.trackMonitor.issues.update({
				key: this._issueKey,
				payload: {
					encodeDegradation,
				},
			});
		}

		const producedFpsForRecovery = producedFramesForRecovery / (recoveryWindowInMs / 1000);
		const encodedFpsForRecovery = encodedFramesForRecovery / (recoveryWindowInMs / 1000);

		// The same denominator the detection half needs, and the same reason for wanting one.
		if (producedFpsForRecovery <= 0) {
			return this.trackMonitor.issues.update({
				key: this._issueKey,
				payload: {
					encodeDegradation,
				},
			});
		}

		const recoveryDegradation = 1 - (encodedFpsForRecovery / producedFpsForRecovery);

		if (this.config.encodeDegradationThreshold < recoveryDegradation) {
			return this.trackMonitor.issues.update({
				key: this._issueKey,
				payload: {
					encodeDegradation,
				},
			});
		}

		this._clear({
			comment: 'encoding recovered',
			payload: {
				producedFpsForRecovery,
				producedFramesForRecovery,
				encodedFpsForRecovery,
				encodedFramesForRecovery,
				recoveryWindowInMs,
			},
			degradedEncodingPerformance: false,
		});
	}

	private _raiseIssue(payload: EncoderBottleneckIssuePayload) {
		if (this._raised) return;

		this._raised = true;
		this.trackMonitor.degradedEncodingPerformance = true;

		this.trackMonitor.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: EncoderBottleneckDetector.ISSUE_TYPE,
			payload,
			timestamp: Date.now(),
		});
	}

	private _clear(options: {
		comment: string,
		payload?: Pick<EncoderBottleneckIssuePayload,
			'producedFpsForRecovery' | 'producedFramesForRecovery' |
			'encodedFpsForRecovery' | 'encodedFramesForRecovery' | 'recoveryWindowInMs'>,
		degradedEncodingPerformance?: false
	}) {
		this.trackMonitor.degradedEncodingPerformance = options.degradedEncodingPerformance;

		// Blanked only on a stand-down, where nothing was measured. A verdict of `false` was
		// measured, and flattening it would leave nothing to read below the threshold.
		if (options.degradedEncodingPerformance !== false) this.trackMonitor.videoEncodingDegradation = undefined;

		if (!this._raised) return;

		this._raised = false;

		this.trackMonitor.issues.resolve({
			key: this._issueKey,
			comment: options.comment,
			payload: options.payload,
			resolvedAt: Date.now(),
		});
	}
}

```
### FrameAssemblyStalledDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/FrameAssemblyStalledDetector.ts#L44)
Category: Pipeline Disruption
```ts
import { Detector } from "./Detector";
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";

export type FrameAssemblyStalledIssuePayload = {
	peerConnectionId: string;
	trackId: string;
	ssrc?: number;
	/** RTP packets that arrived while no frame was completed. */
	packetsSinceLastFrame: number;
	/** How long packets kept arriving with no frame assembled, from stats timestamps. */
	stalledForInMs: number;
	/** Filled in when the issue is resolved. */
	durationInMs?: number;
}

export type FrameAssemblyStalledDetectorConfig = {
	/** Stats time packets must keep arriving with no frame completed before raising, in ms. */
	thresholdInMs: number;

	/** How many packets must have arrived over that time to count as a stall, not a trickle. */
	minPacketsReceived: number;
}

/**
 * Reports RTP arriving from the network with no complete frame coming out of reassembly —
 * `packetsReceived` advancing while `framesReceived` stays flat. Use it to place the break before
 * the decoder rather than in it: every frame is missing pieces, or the depacketizer has lost the
 * stream, which is a different fix from a decoder that is genuinely stuck.
 *
 * A sender that has simply stopped sending is not this: no packets arrive, so nothing accumulates.
 * Pause, mute and a backgrounded tab reset the stall rather than counting toward it.
 *
 * It does not claim *why* frames are not assembling — sustained loss and a codec mismatch look
 * identical from here, and attribution belongs to whoever reads the issues alongside each other.
 *
 * Issue raised: `frame-assembly-stalled`. Monitor event: `frame-assembly-stalled`.
 * Config: `frameAssemblyStalledDetector`.
 * Track attribute: `InboundTrackMonitor.stalledFrameAssembly`.
 *
 * Category: Pipeline Disruption
 * Layer: Receive — packets to frames
 *
 */
export class FrameAssemblyStalledDetector implements Detector {
	public static readonly ISSUE_TYPE = 'frame-assembly-stalled';
	public readonly name = 'frame-assembly-stalled-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	private readonly issueKey: string;
	private _stalledForInMs = 0;
	private _packetsSinceLastFrame = 0;
	private _raised = false;
	private _startedAt?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this.issueKey = `${FrameAssemblyStalledDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private get config() {
		return this.peerConnection.parent.config.frameAssemblyStalledDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) {
			this.trackMonitor.stalledFrameAssembly = undefined;

			return;
		}

		const inboundRtp = this.trackMonitor.getInboundRtp();

		// An audio track has no frames to assemble; there is nothing here to be right or wrong about.
		if (!inboundRtp || inboundRtp.kind !== 'video') {
			this.trackMonitor.stalledFrameAssembly = undefined;

			return;
		}

		if (this.trackMonitor.readyState !== 'live') {
			this.trackMonitor.stalledFrameAssembly = undefined;

			return this._reset('track ended');
		}

		if (
			this.trackMonitor.paused ||
			this.trackMonitor.remoteOutboundTrackPaused ||
			!this.peerConnection.parent.activeTab
		) {
			this.trackMonitor.stalledFrameAssembly = undefined;

			return this._reset('not watching this track right now');
		}

		const deltaPacketsReceived = inboundRtp.deltaPacketsReceived;
		const deltaFramesReceived = inboundRtp.deltaFramesReceived;

		// Without `framesReceived` the question cannot be asked at all. Blind, not healthy.
		if (deltaPacketsReceived === undefined || deltaFramesReceived === undefined) {
			this.inputsUnavailable = true;
			this.trackMonitor.stalledFrameAssembly = undefined;

			return;
		}

		this.inputsUnavailable = false;

		if (0 < deltaFramesReceived) {
			this.trackMonitor.stalledFrameAssembly = false;

			return this._reset('a frame was assembled');
		}

		// Nothing arriving is a silent sender, not a stalled assembler — a different detector's
		// question, and one this detector cannot answer either way.
		if (deltaPacketsReceived <= 0) {
			this.trackMonitor.stalledFrameAssembly = undefined;

			return this._reset('no packets arriving');
		}

		// Packets arriving with no frame out of them, but not yet for long enough to be a fault.
		this.trackMonitor.stalledFrameAssembly = false;

		this._packetsSinceLastFrame += deltaPacketsReceived;
		this._stalledForInMs += inboundRtp.deltaTime ?? 0;

		if (this._raised) return;
		if (this._stalledForInMs < this.config.thresholdInMs) return;
		if (this._packetsSinceLastFrame < this.config.minPacketsReceived) return;

		this._raised = true;
		this._startedAt = Date.now();
		// Set here, not at the call sites, so the flag and the finding cannot drift.
		this.trackMonitor.stalledFrameAssembly = true;

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('frame-assembly-stalled', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			packetsSinceLastFrame: this._packetsSinceLastFrame,
			stalledForInMs: this._stalledForInMs,
		});

		this.trackMonitor.issues.raise({
			key: this.issueKey,
			includeInSample: this.includeIssueInSample,
			type: FrameAssemblyStalledDetector.ISSUE_TYPE,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				ssrc: inboundRtp.ssrc,
				packetsSinceLastFrame: this._packetsSinceLastFrame,
				stalledForInMs: this._stalledForInMs,
			},
		});
	}

	private _reset(comment: string) {
		this._stalledForInMs = 0;
		this._packetsSinceLastFrame = 0;

		if (!this._raised) return;

		this._raised = false;

		const issue = this.trackMonitor.issues.get(this.issueKey);
		let payload: FrameAssemblyStalledIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as FrameAssemblyStalledIssuePayload),
				durationInMs: this._startedAt ? Date.now() - this._startedAt : undefined,
			};
		}

		this.trackMonitor.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedAt = undefined;
	}
}

```
### IceConnectionFailedDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceConnectionFailedDetector.ts#L51)
Category: Connectivity
```ts
import { IceTransportMonitor } from "../monitors/IceTransportMonitor";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

export type IceConnectionFailedIssuePayload = {
	peerConnectionId: string;
	transportId: string;
	dtlsState?: string;
	selectedCandidatePairId?: string;
	/** The transport's own latch: had it ever reached `connected`/`completed` before failing. */
	everConnected: boolean;
	/** ICE restarts observed on this transport so far. */
	iceGeneration: number;
	/** Filled in when the failure is resolved. */
	durationInMs?: number;
};

type TransportState = {
	/** ICE restarts observed on this transport, inferred from the local username fragment. */
	iceGeneration: number;
	usernameFragment?: string;
	raisedAt?: number;
};

const ISSUE_TYPE = 'ice-connection-failed';

/** No tunables — a terminal state needs no threshold. `{}` enables the detector, `null` disables it. */
export type IceConnectionFailedDetectorConfig = Record<string, never>;

/**
 * Reports an ICE transport the browser has given up on. Use `everConnected` in the payload to
 * tell apart the two faults that share the `failed` state and share nothing else: a path that
 * **never worked** (no candidate pair ever won — symmetric NAT with no TURN, a firewall eating
 * the checks, a credential that never arrived) and a path that **worked and was lost** (the
 * interface changed, the NAT binding expired, the route died).
 *
 * `failed` is terminal for the ICE generation, so the issue is raised on the first tick that
 * reports it rather than waited out. A changed ICE local username fragment means a new
 * generation: the standing issue is resolved so the next failure raises again with the
 * generation counter incremented.
 *
 * It does not claim a cause — only the fact, plus the one distinction the stats can support.
 *
 * Issue raised: `ice-connection-failed`, resolved when ICE comes back, when an ICE restart is
 * inferred, or when the transport goes away. Config: `iceConnectionFailedDetector`.
 *
 * Category: Connectivity
 * Layer: 5 — Path continuity
 *
 */
export class IceConnectionFailedDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'ice-connection-failed-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _states = new Map<string, TransportState>();

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) return;

		const seenIds = new Set<string>();

		for (const transport of this.peerConnection.iceTransports) {
			seenIds.add(transport.id);

			this._checkTransport(transport);
		}

		for (const transportId of [ ...this._states.keys() ]) {
			if (seenIds.has(transportId)) continue;

			this._resolve(transportId, 'ice transport is gone');
			this._states.delete(transportId);
		}
	}

	private _checkTransport(transport: IceTransportMonitor) {
		const state = this._getState(transport);
		const usernameFragment = this._usernameFragmentOf(transport);

		if (usernameFragment !== undefined && state.usernameFragment !== undefined
			&& usernameFragment !== state.usernameFragment) {
			state.iceGeneration += 1;

			this._resolve(transport.id, 'ice restarted');
		}
		if (usernameFragment !== undefined) state.usernameFragment = usernameFragment;

		const iceState = transport.iceState;

		if (iceState === 'connected' || iceState === 'completed') {
			this._resolve(transport.id, 'ice connection recovered');

			return;
		}

		if (iceState !== 'failed') return;
		if (state.raisedAt !== undefined) return;

		state.raisedAt = Date.now();

		this.peerConnection.issues.raise({
				key: this._issueKey(transport.id),
				includeInSample: this.includeIssueInSample,
				type: ISSUE_TYPE,
				payload: {
					peerConnectionId: this.peerConnection.peerConnectionId,
					transportId: transport.id,
					dtlsState: transport.dtlsState,
					selectedCandidatePairId: transport.selectedCandidatePairId,
					everConnected: transport.everConnected === true,
					iceGeneration: state.iceGeneration,
				},
			}
		);
	}

	private _usernameFragmentOf(transport: IceTransportMonitor): string | undefined {
		return transport.iceLocalUsernameFragment
			?? transport.getSelectedCandidatePair()?.getLocalCandidate()?.usernameFragment;
	}

	private _getState(transport: IceTransportMonitor): TransportState {
		let state = this._states.get(transport.id);

		if (!state) {
			state = {
				iceGeneration: 0,
				usernameFragment: this._usernameFragmentOf(transport),
			};
			this._states.set(transport.id, state);
		}

		return state;
	}

	private _resolve(transportId: string, comment: string) {
		const state = this._states.get(transportId);

		if (state?.raisedAt === undefined) return;

		const raisedAt = state.raisedAt;

		state.raisedAt = undefined;

		const key = this._issueKey(transportId);
		const issue = this.peerConnection.issues.get(key);

		if (!issue) return;

		this.peerConnection.issues.resolve({
			key: key,
			comment,
			payload: {
				...(issue.payload as IceConnectionFailedIssuePayload),
				durationInMs: Date.now() - raisedAt,
			},
			resolvedAt: Date.now(),
		});
	}

	private _issueKey(transportId: string) {
		return `${ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}-transport-${transportId}`;
	}
}

```
### IceDisconnectedDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceDisconnectedDetector.ts#L57)
Category: Connectivity
```ts
import { IceTransportMonitor } from "../monitors/IceTransportMonitor";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

export type IceDisconnectedIssuePayload = {
	peerConnectionId: string;
	transportId: string;
	iceState?: string;
	dtlsState?: string;
	selectedCandidatePairId?: string;
	/** How long the transport had been `disconnected` when the issue was raised — the threshold, not the episode. */
	disconnectedForMs: number;
	/** ICE restarts observed on this transport so far, tying the issue to its generation. */
	iceGeneration: number;
	/** The episode's length, filled in on resolve. */
	durationInMs?: number;
};

type TransportState = {
	/** ICE restarts observed on this transport, inferred from the local username fragment. */
	iceGeneration: number;
	usernameFragment?: string;
	/** Stats time accumulated while `disconnected`, reset the moment that stops being true. */
	disconnectedForInMs: number;
	raisedAt?: number;
};

const ISSUE_TYPE = 'ice-disconnected';

export type IceDisconnectedDetectorConfig = {
	/** How long a transport must stay `disconnected` before an issue is raised; shorter blips are ignored. */
	disconnectedThresholdInMs: number;
}

/**
 * Reports an ICE transport that has been `disconnected` long enough that it is no longer going to
 * fix itself. Use it to tell an outage from the ordinary blip a Wi-Fi roam or a busy CPU produces
 * several times a call: only duration separates them, which is what `disconnectedThresholdInMs`
 * measures.
 *
 * The clock is stats time, so a late or skipped collection still credits the outage with the time it
 * really lasted, and anything ending the condition zeroes it. A changed ICE local username fragment
 * means a new generation, which resolves the standing issue and restarts the clock; the fragment is
 * read here rather than asked of `IceRestartDetector`, so neither depends on the other's ordering.
 *
 * It does not claim the media path is gone — `disconnected` often comes back, terminal `failed`
 * belongs to `IceConnectionFailedDetector`, and a connected path carrying nothing belongs to
 * `IceTransportStalledDetector`.
 *
 * Issue raised: `ice-disconnected`, resolved when ICE reconnects, when an ICE restart is inferred,
 * or when the transport goes away. Config: `iceDisconnectedDetector`.
 *
 * Category: Connectivity
 * Layer: 5 — Path continuity
 *
 */
export class IceDisconnectedDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'ice-disconnected-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _states = new Map<string, TransportState>();

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.iceDisconnectedDetector!;
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) return;

		const seenIds = new Set<string>();

		for (const transport of this.peerConnection.iceTransports) {
			seenIds.add(transport.id);

			this._checkTransport(transport);
		}

		for (const transportId of [ ...this._states.keys() ]) {
			if (seenIds.has(transportId)) continue;

			this._resolve(transportId, 'ice transport is gone');
			this._states.delete(transportId);
		}
	}

	private _checkTransport(transport: IceTransportMonitor) {
		const state = this._getState(transport);
		const usernameFragment = this._usernameFragmentOf(transport);

		if (usernameFragment !== undefined && state.usernameFragment !== undefined
			&& usernameFragment !== state.usernameFragment) {
			state.iceGeneration += 1;
			state.disconnectedForInMs = 0;

			this._resolve(transport.id, 'ice restarted');
		}
		if (usernameFragment !== undefined) state.usernameFragment = usernameFragment;

		const iceState = transport.iceState;

		if (iceState === 'connected' || iceState === 'completed') {
			state.disconnectedForInMs = 0;

			this._resolve(transport.id, 'ice connection recovered');

			return;
		}

		if (iceState !== 'disconnected') {
			// A standing issue is left standing: a fall into `failed` is not a recovery.
			state.disconnectedForInMs = 0;

			return;
		}

		state.disconnectedForInMs += transport.deltaTime ?? 0;

		if (state.disconnectedForInMs < this.config.disconnectedThresholdInMs) return;
		if (state.raisedAt !== undefined) return;

		state.raisedAt = Date.now();

		this.peerConnection.issues.raise({
				key: this._issueKey(transport.id),
				includeInSample: this.includeIssueInSample,
				type: ISSUE_TYPE,
				payload: {
					peerConnectionId: this.peerConnection.peerConnectionId,
					transportId: transport.id,
					iceState,
					dtlsState: transport.dtlsState,
					selectedCandidatePairId: transport.selectedCandidatePairId,
					disconnectedForMs: state.disconnectedForInMs,
					iceGeneration: state.iceGeneration,
				},
			}
		);
	}

	private _usernameFragmentOf(transport: IceTransportMonitor): string | undefined {
		return transport.iceLocalUsernameFragment
			?? transport.getSelectedCandidatePair()?.getLocalCandidate()?.usernameFragment;
	}

	private _getState(transport: IceTransportMonitor): TransportState {
		let state = this._states.get(transport.id);

		if (!state) {
			state = {
				iceGeneration: 0,
				usernameFragment: this._usernameFragmentOf(transport),
				disconnectedForInMs: 0,
			};
			this._states.set(transport.id, state);
		}

		return state;
	}

	private _resolve(transportId: string, comment: string) {
		const state = this._states.get(transportId);

		if (state?.raisedAt === undefined) return;

		const raisedAt = state.raisedAt;

		state.raisedAt = undefined;

		const key = this._issueKey(transportId);
		const issue = this.peerConnection.issues.get(key);

		if (!issue) return;

		this.peerConnection.issues.resolve({
			key: key,
			comment,
			payload: {
				...(issue.payload as IceDisconnectedIssuePayload),
				durationInMs: Date.now() - raisedAt,
			},
			resolvedAt: Date.now(),
		});
	}

	private _issueKey(transportId: string) {
		return `${ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}-transport-${transportId}`;
	}
}

```
### IceEstablishmentFailedDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceEstablishmentFailedDetector.ts#L57)
Category: Connectivity
```ts
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

/** How many local candidates of each type ICE managed to gather before giving up. */
export type IceLocalCandidateCounts = {
	host: number;
	srflx: number;
	relay: number;
	prflx: number;
	/** Candidates whose `candidateType` the stats source did not report. */
	unknown: number;
};

/** A summary of what was actually tried: how far gathering got, and how far the checks against the far end got. */
export type IceEstablishmentFailedIssuePayload = {
	peerConnectionId: string;
	connectionState?: string;
	iceGatheringState?: string;
	localIceCandidateCount: number;
	localCandidateCounts: IceLocalCandidateCounts;
	/** Every distinct `state` seen across the candidate pairs, deduplicated and sorted. */
	candidatePairStates: string[];
	candidatePairCount: number;
	sustainedForInMs: number;
	durationInMs?: number;
};

const ISSUE_TYPE = 'ice-establishment-failed';

export type IceEstablishmentFailedDetectorConfig = {
	/** Stats time the connection must go on failing to establish before raising, in ms. Keep it above
	 * `icePathEstablishmentDetector.thresholdInMs` — merely slow is not yet failed. */
	thresholdInMs: number;
}

/**
 * Reports the call that never connected, as a resolvable issue rather than a passing event. The
 * payload carries what was actually tried, so an operator can tell the common causes apart: host
 * candidates only means gathering never reached a STUN server; host and reflexive but no relay means
 * TURN was never configured or never answered; relay candidates with every pair `in-progress` or
 * `failed` means the relay is unreachable or the far end never answered the checks.
 *
 * Three facts must hold together for the whole of `thresholdInMs` in stats time: local candidates
 * exist (so this is not the no-network case `IceReachabilityDetector` owns), the connection has
 * never reached `connected` (so this is establishment failing, not a working call that broke), and
 * no pair was ever nominated or `succeeded` (so a stalled DTLS handshake stays its owner's).
 *
 * It does not claim which side is at fault — every fact here is local.
 *
 * Issue raised: `ice-establishment-failed`, resolved if the connection establishes after all or
 * when the peer connection closes. Config: `iceEstablishmentFailedDetector`.
 *
 * Category: Connectivity
 * Layer: 3 — Path establishment
 *
 */
export class IceEstablishmentFailedDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'ice-establishment-failed-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _issueKey: string;

	private _everConnected = false;
	private _everNominated = false;
	private _sustainedForInMs = 0;
	private _raisedAt?: number;

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
		this._issueKey = `${ISSUE_TYPE}-pc-${peerConnection.peerConnectionId}`;
	}

	private get config() {
		return this.peerConnection.parent.config.iceEstablishmentFailedDetector!;
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) {
			this._resolve('peer connection closed');

			return;
		}

		const connectionState = this.peerConnection.connectionState;

		if (connectionState === 'connected') {
			this._everConnected = true;
		}

		// Latched, not sampled: a pair that won once stays proof on every later tick.
		for (const pair of this.peerConnection.iceCandidatePairs) {
			if (pair.nominated === true || pair.state === 'succeeded') {
				this._everNominated = true;
				break;
			}
		}

		if (this._everConnected || this._everNominated) {
			this._sustainedForInMs = 0;

			this._resolve('ice path established');

			return;
		}

		// Nothing to have failed with — `no-available-ice-candidate` owns that case.
		if (this.peerConnection.localIceCandidates.length === 0) {
			this._sustainedForInMs = 0;

			return;
		}

		this._sustainedForInMs += this.peerConnection.deltaTime ?? 0;

		if (this._sustainedForInMs < this.config.thresholdInMs) return;
		if (this._raisedAt !== undefined) return;

		this._raisedAt = Date.now();

		this.peerConnection.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: ISSUE_TYPE,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				connectionState,
				iceGatheringState: this.peerConnection.iceGatheringState,
				localIceCandidateCount: this.peerConnection.localIceCandidates.length,
				localCandidateCounts: this._localCandidateCounts(),
				candidatePairStates: this._candidatePairStates(),
				candidatePairCount: this.peerConnection.iceCandidatePairs.length,
				sustainedForInMs: this._sustainedForInMs,
			},
		});
	}

	private _localCandidateCounts(): IceLocalCandidateCounts {
		const counts: IceLocalCandidateCounts = { host: 0, srflx: 0, relay: 0, prflx: 0, unknown: 0 };

		for (const candidate of this.peerConnection.localIceCandidates) {
			switch (candidate.candidateType) {
				case 'host': counts.host += 1; break;
				case 'srflx': counts.srflx += 1; break;
				case 'relay': counts.relay += 1; break;
				case 'prflx': counts.prflx += 1; break;
				default: counts.unknown += 1; break;
			}
		}

		return counts;
	}

	private _candidatePairStates(): string[] {
		const states = new Set<string>();

		for (const pair of this.peerConnection.iceCandidatePairs) {
			states.add(pair.state ?? 'unknown');
		}

		return [ ...states ].sort();
	}

	private _resolve(comment: string) {
		if (this._raisedAt === undefined) return;

		const raisedAt = this._raisedAt;

		this._raisedAt = undefined;

		const issue = this.peerConnection.issues.get(this._issueKey);

		if (!issue) return;

		this.peerConnection.issues.resolve({
			key: this._issueKey,
			comment,
			payload: {
				...(issue.payload as IceEstablishmentFailedIssuePayload),
				durationInMs: Date.now() - raisedAt,
			},
			resolvedAt: Date.now(),
		});
	}
}

```
### IcePathEstablishmentDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IcePathEstablishmentDetector.ts#L43)
Category: Connectivity
```ts
import { ClientEventTypes } from "../schema/ClientEventTypes";
import { IceTransportMonitor } from "../monitors/IceTransportMonitor";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

/** Which stage of establishment a too-long `connecting` is actually stuck in. */
export type IcePathEstablishmentStage = 'ice-gathering' | 'ice-checking' | 'dtls' | 'unknown';

/** Severity order for picking the transport that best explains a stall — without BUNDLE there are several. */
const ICE_STATE_SEVERITY: Record<string, number> = {
	failed: 6, disconnected: 5, checking: 4, new: 3, connected: 2, completed: 1, closed: 0,
};

export type IcePathEstablishmentDetectorConfig = {
	/** Also add the `LONG_PC_CONNECTION_ESTABLISHMENT` client event, not just the monitor event. Default true. */
	createEvent?: boolean

	/** How long a connection may stay in `connecting` before it is reported, in ms. */
	thresholdInMs: number;
}

/**
 * Reports how long a peer connection has been trying to connect and, more usefully, which stage it
 * is stuck in. `connectionState: 'connecting'` covers ICE gathering, ICE checking and the DTLS
 * handshake alike; `stalledStage` tells them apart, so an operator can say whether to look at
 * candidate gathering, at reachability, or at the certificate exchange.
 *
 * The trigger is `connectionState` rather than any transport's ICE state, because a connection whose
 * ICE side finished and whose DTLS handshake hangs reads `connected` on every transport. Time is
 * accumulated from the connection's own `deltaTime`, so a backgrounded tab does not report the wall
 * clock it slept through, and the stage is read from the same observations as the duration. Any exit
 * from `connecting` re-arms the detector and zeroes the clock, so each attempt is timed on its own.
 *
 * It raises no issue: slow is not yet failed. `IceEstablishmentFailedDetector` makes that claim.
 *
 * Monitor event: `ice-path-establishment-slow`. Client event:
 * `LONG_PC_CONNECTION_ESTABLISHMENT`, when `createEvent`. Config: `icePathEstablishmentDetector`.
 *
 * Category: Connectivity
 * Layer: 3 — Path establishment
 *
 */
export class IcePathEstablishmentDetector implements Detector {
	public readonly name = 'ice-path-establishment-detector';
	public disabled = false;

	private _evented = false;
	/** Stats time this attempt has spent in `connecting`, accumulated from `deltaTime`. */
	private _connectingForInMs = 0;

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.icePathEstablishmentDetector!;
	}

	public update(): void {
		if (this.disabled) return;

		if (this.peerConnection.connectionState !== 'connecting') {
			// Any exit re-arms, not just `connected`, so each attempt is timed on its own.
			this._evented = false;
			this._connectingForInMs = 0;

			return;
		}

		this._connectingForInMs += this.peerConnection.deltaTime ?? 0;

		this._checkSlowEstablishment(this._connectingForInMs);
	}

	private _checkSlowEstablishment(durationInMs: number) {
		if (this._evented) return;
		if (durationInMs < this.config.thresholdInMs) return;

		this._evented = true;

		const clientMonitor = this.peerConnection.parent;
		const stalledStage = this._stalledStage();

		clientMonitor.emit('ice-path-establishment-slow', {
			peerConnectionMonitor: this.peerConnection,
			clientMonitor,
			stalledStage,
			sustainedForInMs: durationInMs,
		});

		if (!this.config.createEvent) return;

		const [ subject ] = this._bySeverity();

		clientMonitor.addEvent({
			type: ClientEventTypes.LONG_PC_CONNECTION_ESTABLISHMENT,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				// Stats time, not wall clock.
				duration: durationInMs,
				stalledStage,
				iceState: subject?.iceState,
				dtlsState: subject?.dtlsState,
				iceGatheringState: this.peerConnection.iceGatheringState,
			},
		});
	}

	/** Narrows a stalled `connecting` to the stage responsible, or `unknown` when the stats give no verdict. */
	private _stalledStage(): IcePathEstablishmentStage {
		const transports = this.peerConnection.iceTransports ?? [];

		if (transports.length === 0) {
			return this.peerConnection.iceGatheringState === 'gathering' ? 'ice-gathering' : 'unknown';
		}

		let anyIceDone = false;

		for (const transport of transports) {
			const iceState = transport.iceState;

			if (iceState === 'checking' || iceState === 'new') return 'ice-checking';
			if (iceState === 'connected' || iceState === 'completed') {
				anyIceDone = true;
				continue;
			}
			// Where no iceState is reported (Safari), a succeeded pair proves the ICE side done.
			if (iceState === undefined && transport.getSelectedCandidatePair()?.state === 'succeeded') {
				anyIceDone = true;
			}
		}

		return anyIceDone ? 'dtls' : 'unknown';
	}

	private _bySeverity(): IceTransportMonitor[] {
		return [ ...(this.peerConnection.iceTransports ?? []) ].sort(
			(a, b) => (ICE_STATE_SEVERITY[b.iceState ?? ''] ?? -1) - (ICE_STATE_SEVERITY[a.iceState ?? ''] ?? -1)
		);
	}
}

```
### IceReachabilityDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceReachabilityDetector.ts#L49)
Category: Connectivity
```ts
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

/** A snapshot of the connection at the moment the diagnosis was made. */
export type NoAvailableIceCandidateIssuePayload = {
	peerConnectionId: string;
	connectionState?: string;
	/** The last state seen before the connection fell to `disconnected`/`failed`. */
	previousConnectionState?: string;
	iceGatheringState?: string;
	/** Always 0 when raised — the whole point — kept for the record. */
	localIceCandidateCount: number;
	/** Observed time the connection went without a candidate, in stats time. */
	sustainedForInMs: number;
	/** How long the issue stayed active; filled in on resolution. */
	durationInMs?: number;
};

const ISSUE_TYPE = 'no-available-ice-candidate';

export type IceReachabilityDetectorConfig = {
	/** How long a never-connected peer connection may sit with zero candidates in `new`/`connecting`, in ms. */
	thresholdInMs: number;
}

/**
 * Reports ICE gathering producing zero local candidates on a connection that never connected — the
 * client had no network to connect *with*: no interface up, airplane mode, a VPN that tore down
 * every route. Use it to tell "this client cannot do WebRTC here at all" apart from every other ICE
 * issue, which describes a path that existed and then stopped working.
 *
 * Any interface that is up yields a host candidate within milliseconds, so an empty list once
 * gathering is `complete` is an absent network rather than a slow start. `disconnected`/`failed`
 * with zero candidates raises at once; `new`/`connecting` waits out `thresholdInMs` in stats time,
 * which is also what keeps it off an un-negotiated connection. It never fires once a connection has
 * reached `connected`.
 *
 * It cannot separate no network from every candidate type forbidden by policy, and does not try.
 *
 * Issue raised: `no-available-ice-candidate`, resolved when a candidate appears, the
 * connection connects, or the peer connection closes.
 * Monitor event: `no-available-ice-candidate`.
 * Config: `iceReachabilityDetector`.
 *
 * Category: Connectivity
 * Layer: 1 — Reachability
 *
 */
export class IceReachabilityDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'ice-reachability-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _issueKey: string;

	private _previousConnectionState?: string;
	private _stateBeforeFailure?: string;
	/** Stats time spent watching this connection go without a local candidate. */
	private _waitingForInMs = 0;
	private _everConnected = false;
	private _raisedAt?: number;

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
		this._issueKey = `${ISSUE_TYPE}-pc-${peerConnection.peerConnectionId}`;
	}

	private get config() {
		return this.peerConnection.parent.config.iceReachabilityDetector!;
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) {
			this._resolve('peer connection closed');
			return;
		}

		// Advanced before any verdict, so the branches below that break the condition zero it again.
		this._waitingForInMs += this.peerConnection.deltaTime ?? 0;

		const connectionState = this.peerConnection.connectionState;

		if (connectionState !== this._previousConnectionState) {
			if (connectionState === 'disconnected' || connectionState === 'failed') {
				this._stateBeforeFailure = this._previousConnectionState;
			}
			this._previousConnectionState = connectionState;
		}

		if (connectionState === 'connected') {
			this._everConnected = true;
			this._waitingForInMs = 0;
			this._resolve('connection established');
			return;
		}

		const localIceCandidateCount = this.peerConnection.localIceCandidates.length;

		if (0 < localIceCandidateCount) {
			// Candidates aging out later must start their own window, not inherit this one.
			this._waitingForInMs = 0;
			this._resolve('local ice candidate appeared');
			return;
		}

		if (this._everConnected) return;

		// Zero candidates is only evidence once gathering says it is done looking.
		if (this.peerConnection.iceGatheringState !== 'complete') return;

		const failing = connectionState === 'disconnected' || connectionState === 'failed';
		if (!failing && this._waitingForInMs < this.config.thresholdInMs) return;
		if (this._raisedAt !== undefined) return;

		// Wall clock, and only for the resolved issue's `durationInMs`.
		this._raisedAt = Date.now();

		const clientMonitor = this.peerConnection.parent;
		const payload: NoAvailableIceCandidateIssuePayload = {
			peerConnectionId: this.peerConnection.peerConnectionId,
			connectionState,
			previousConnectionState: this._stateBeforeFailure,
			iceGatheringState: this.peerConnection.iceGatheringState,
			localIceCandidateCount,
			sustainedForInMs: this._waitingForInMs,
		};

		clientMonitor.emit('no-available-ice-candidate', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			...payload,
		});

		this.peerConnection.issues.raise({
				key: this._issueKey,
				includeInSample: this.includeIssueInSample,
			type: ISSUE_TYPE,
			payload,
		});
	}

	private _resolve(comment: string) {
		if (this._raisedAt === undefined) return;

		const issue = this.peerConnection.issues.get(this._issueKey);

		if (issue) {
			this.peerConnection.issues.resolve({
				key: this._issueKey,
				comment,
				payload: {
					...issue.payload,
					durationInMs: Date.now() - this._raisedAt,
				} as NoAvailableIceCandidateIssuePayload,
				resolvedAt: Date.now(),
			});
		}

		this._raisedAt = undefined;
	}
}

```
### IceRestartDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceRestartDetector.ts#L53)
Category: Telemetry
```ts
import { IceTransportMonitor } from "../monitors/IceTransportMonitor";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { ClientEventTypes } from "../schema/ClientEventTypes";
import { Detector } from "./Detector";

export type IceRestartOutcome = 'detected' | 'recovered' | 'failed';

export type IceRestartClientEventPayload = {
	peerConnectionId: string;
	transportId: string;
	iceGeneration: number;
	/** `detected` when a new generation was observed, then `recovered` or `failed` once it resolved. */
	outcome: IceRestartOutcome;
	iceState?: string;
	/** How the generation was inferred — this is stats-based, not reported by the browser. */
	evidence: 'ice-username-fragment-changed';
	timestamp: number;
};

type TransportState = {
	usernameFragment?: string;
	iceGeneration: number;
	/** A restart has been reported and the generation it started has not resolved yet. */
	restartPending: boolean;
};

export type IceRestartDetectorConfig = {
	/** Also buffer `ICE_RESTART` client events into the sample. Default true. */
	createEvent?: boolean;
}

/**
 * Reports that an ICE transport started a new ICE generation, and how that generation turned out.
 * Use it to see whether a call's recoveries are working — a restart followed by `recovered` is the
 * network healing, a run of `failed` is a connection that cannot re-establish itself. It raises no
 * issue: a restart is a fact about the connection, not a fault.
 *
 * The evidence is a changed ICE local username fragment, the one field a restart cannot leave alone,
 * falling back to the selected local candidate's fragment and staying silent when neither exists.
 * `detected` goes out on the change; the generation is then followed to `connected`/`completed`
 * (`recovered`) or `failed`, and one still checking gets no outcome invented for it.
 *
 * It does not claim a restart was needed or is warranted — that is
 * `IceRestartRecommendationDetector`.
 *
 * Raises no issue. Monitor event: `ice-restart`. Client event: `ICE_RESTART`, when `createEvent`.
 * Config: `iceRestartDetector`.
 *
 * Category: Telemetry
 * Layer: Transport
 *
 */
export class IceRestartDetector implements Detector {
	public readonly name = 'ice-restart-detector';
	public disabled = false;

	private readonly _states = new Map<string, TransportState>();

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.iceRestartDetector!;
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) return;

		const seenIds = new Set<string>();

		for (const transport of this.peerConnection.iceTransports) {
			seenIds.add(transport.id);

			this._checkTransport(transport);
		}

		for (const transportId of [ ...this._states.keys() ]) {
			if (seenIds.has(transportId)) continue;

			this._states.delete(transportId);
		}
	}

	private _checkTransport(transport: IceTransportMonitor) {
		const state = this._getState(transport);
		const iceState = transport.iceState;

		// Order is load-bearing: this tick's ICE state describes the generation the tick started in,
		// so a pending outcome must settle before a fragment change starts the next generation.
		if (state.restartPending) {
			if (iceState === 'connected' || iceState === 'completed') {
				state.restartPending = false;

				this._notify(transport, state, 'recovered');
			} else if (iceState === 'failed') {
				state.restartPending = false;

				this._notify(transport, state, 'failed');
			}
		}

		const usernameFragment = this._usernameFragmentOf(transport);

		if (usernameFragment !== undefined && state.usernameFragment !== undefined
			&& usernameFragment !== state.usernameFragment) {
			state.iceGeneration += 1;
			state.restartPending = true;

			this._notify(transport, state, 'detected');
		}
		if (usernameFragment !== undefined) state.usernameFragment = usernameFragment;
	}

	private _notify(transport: IceTransportMonitor, state: TransportState, outcome: IceRestartOutcome) {
		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('ice-restart', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			transportId: transport.id,
			iceGeneration: state.iceGeneration,
			outcome,
		});

		if (!this.config.createEvent) return;

		clientMonitor.addEvent<IceRestartClientEventPayload>({
			type: ClientEventTypes.ICE_RESTART,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				transportId: transport.id,
				iceGeneration: state.iceGeneration,
				outcome,
				iceState: transport.iceState,
				evidence: 'ice-username-fragment-changed',
				timestamp: Date.now(),
			},
		});
	}

	private _usernameFragmentOf(transport: IceTransportMonitor): string | undefined {
		return transport.iceLocalUsernameFragment
			?? transport.getSelectedCandidatePair()?.getLocalCandidate()?.usernameFragment;
	}

	private _getState(transport: IceTransportMonitor): TransportState {
		let state = this._states.get(transport.id);

		if (!state) {
			state = {
				usernameFragment: this._usernameFragmentOf(transport),
				iceGeneration: 0,
				restartPending: false,
			};
			this._states.set(transport.id, state);
		}

		return state;
	}
}

```
### IceRestartRecommendationDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceRestartRecommendationDetector.ts#L87)
Category: Telemetry
```ts
import { IceTransportMonitor } from "../monitors/IceTransportMonitor";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { ClientEventTypes } from "../schema/ClientEventTypes";
import { Detector } from "./Detector";

/** Why a restart is warranted: a condition the browser will not recover from within the window. */
export type IceRestartRecommendationReason =
	/** ICE gave up on this generation; only a restart can revive it. */
	| 'ice-failed'
	/** `disconnected` outlasted the window in which ICE usually self-heals. */
	| 'ice-disconnected'
	/** ICE still reports connected, but the selected path stopped delivering. */
	| 'transport-stalled'
	/** The peer connection never finished establishing in the first place. */
	| 'never-established';

/**
 * `transportId` is absent for `never-established`, which is per peer connection. A rising
 * `recommendationCount` against a flat `iceGeneration` means the recommendations are not being acted on.
 */
export type IceRestartRecommendedEventPayload = {
	peerConnectionId: string;
	transportId?: string;
	reason: IceRestartRecommendationReason;
	conditionDurationInMs: number;
	iceGeneration: number;
	recommendationCount: number;
	iceState?: string;
	dtlsState?: string;
	selectedCandidatePairId?: string;
};

type TransportState = {
	usernameFragment?: string;
	iceGeneration: number;
	/** A restart has already been started on this transport and has not resolved yet. */
	restartPending: boolean;
	/** Whether inbound bytes were ever seen on this transport's selected pair. */
	sawInboundTraffic: boolean;
	failedForInMs: number;
	disconnectedForInMs: number;
	stalledForInMs: number;
	recommendedAt?: number;
	recommendations: number;
};

export type IceRestartRecommendationDetectorConfig = {
	/** Also add the `ICE_RESTART_RECOMMENDED` client event. DEFAULT: true */
	createEvent?: boolean;

	/** How long a `disconnected` or stalled transport must persist, in ms. `failed` recommends on sight. */
	iceRestartRecommendationThresholdInMs: number;

	/** Minimum time between repeated recommendations for the same transport, in ms. */
	iceRestartRecommendationCooldownInMs: number;

	/** How long the peer connection must have been establishing before `never-established`, in ms. */
	restartRecommendationThresholdInMs: number;

	/** Minimum time between repeated `never-established` recommendations, in ms. */
	restartRecommendationCooldownInMs: number;
}

/**
 * The one place that says "restart ICE". Use it to answer "is this connection worth restarting right
 * now" — it recommends and never performs, since only the application knows whether renegotiation is
 * safe. Listen for `'ice-restart-recommended'` and call `pc.restartIce()`.
 *
 * Four conditions warrant one, kept in one class so the rate limiting is shared. Three are per
 * transport — `failed` on sight, `disconnected` and a connected-but-not-receiving path once they
 * outlast `iceRestartRecommendationThresholdInMs` — and `never-established` is per peer connection,
 * where nothing ever got far enough to have a failing transport. Each verdict is read from raw
 * transport and connection state, so this runs in any order and no other detector can silence it.
 * Condition clocks are stats time; the cooldowns are wall clock, since they throttle notifications.
 * A restart already in flight, inferred from a changed username fragment, suppresses the rest.
 *
 * It does not claim a restart will help, only that it is the standard remedy for the condition.
 *
 * Raises no issue. Monitor event: `ice-restart-recommended`.
 * Client event: `ICE_RESTART_RECOMMENDED`, when `createEvent`.
 * Config: `iceRestartRecommendationDetector`.
 *
 * Category: Telemetry
 * Layer: Transport
 *
 */
export class IceRestartRecommendationDetector implements Detector {
	public readonly name = 'ice-restart-recommendation-detector';
	public disabled = false;

	private readonly _states = new Map<string, TransportState>();

	/** `never-established` is per peer connection, so its rate limiting cannot live in the map. */
	private _neverEstablishedRecommendedAt?: number;
	private _neverEstablishedRecommendations = 0;
	/** Stats time spent in `connecting`, from the connection's own `deltaTime`. */
	private _connectingForInMs = 0;

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.iceRestartRecommendationDetector!;
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) return;

		const seenIds = new Set<string>();

		for (const transport of this.peerConnection.iceTransports) {
			seenIds.add(transport.id);

			this._checkTransport(transport);
		}

		for (const transportId of [ ...this._states.keys() ]) {
			if (seenIds.has(transportId)) continue;

			this._states.delete(transportId);
		}

		this._checkEstablishment();
	}

	private _checkTransport(transport: IceTransportMonitor) {
		const config = this.config;
		const state = this._getState(transport);
		const iceState = transport.iceState;
		const usernameFragment = this._usernameFragmentOf(transport);

		if (usernameFragment !== undefined && state.usernameFragment !== undefined
			&& usernameFragment !== state.usernameFragment) {
			state.iceGeneration += 1;
			state.restartPending = true;
			state.failedForInMs = 0;
			state.disconnectedForInMs = 0;
			state.stalledForInMs = 0;
			state.sawInboundTraffic = false;
		}
		if (usernameFragment !== undefined) state.usernameFragment = usernameFragment;

		// A pending restart has resolved once the new generation reaches a terminal verdict.
		if (state.restartPending
			&& (iceState === 'connected' || iceState === 'completed' || iceState === 'failed')) {
			state.restartPending = false;
		}

		this._accumulate(transport, state);

		if (state.restartPending) return;

		let reason: IceRestartRecommendationReason | undefined;
		let conditionDurationInMs = 0;

		if (iceState === 'failed') {
			reason = 'ice-failed';
			conditionDurationInMs = state.failedForInMs;
		} else if (config.iceRestartRecommendationThresholdInMs <= state.disconnectedForInMs) {
			reason = 'ice-disconnected';
			conditionDurationInMs = state.disconnectedForInMs;
		} else if (config.iceRestartRecommendationThresholdInMs <= state.stalledForInMs) {
			reason = 'transport-stalled';
			conditionDurationInMs = state.stalledForInMs;
		}

		if (reason === undefined) {
			// Rearmed, so the next incident is not made to serve out a cleared condition's cooldown.
			state.recommendedAt = undefined;

			return;
		}

		const now = Date.now();

		// Wall clock, unlike the condition clocks: this throttles notifications, not measurement.
		if (state.recommendedAt !== undefined
			&& now - state.recommendedAt < config.iceRestartRecommendationCooldownInMs) {
			return;
		}

		state.recommendedAt = now;
		state.recommendations += 1;

		this._recommend({
			peerConnectionId: this.peerConnection.peerConnectionId,
			transportId: transport.id,
			reason,
			conditionDurationInMs,
			iceGeneration: state.iceGeneration,
			recommendationCount: state.recommendations,
			iceState,
			dtlsState: transport.dtlsState,
			selectedCandidatePairId: transport.selectedCandidatePairId,
		});
	}

	/**
	 * Advances the three per-transport condition clocks, each zeroed the moment its condition stops
	 * holding. The last stall guard is not optional: a send-only transport legitimately receives nothing.
	 */
	private _accumulate(transport: IceTransportMonitor, state: TransportState) {
		const iceState = transport.iceState;
		const deltaTime = transport.deltaTime ?? 0;

		state.failedForInMs = iceState === 'failed' ? state.failedForInMs + deltaTime : 0;
		state.disconnectedForInMs = iceState === 'disconnected' ? state.disconnectedForInMs + deltaTime : 0;

		const pair = transport.getSelectedCandidatePair();

		if ((iceState !== 'connected' && iceState !== 'completed') || !pair || pair.state !== 'succeeded') {
			state.stalledForInMs = 0;

			return;
		}

		const inboundBytesDelta = pair.deltaBytesReceived;
		const outboundBytesDelta = pair.deltaBytesSent;

		if (inboundBytesDelta === undefined || outboundBytesDelta === undefined) return;

		if (0 < inboundBytesDelta) {
			state.sawInboundTraffic = true;
			state.stalledForInMs = 0;

			return;
		}

		if (!state.sawInboundTraffic || outboundBytesDelta <= 0 || !this._expectsInboundMedia(transport)) {
			state.stalledForInMs = 0;

			return;
		}

		state.stalledForInMs += deltaTime;
	}

	/**
	 * Recommends for a peer connection that never finished establishing. Yields to `ice-failed` and
	 * `ice-disconnected`, which name what went wrong rather than only what did not happen.
	 */
	private _checkEstablishment() {
		const config = this.config;

		if (this.peerConnection.connectionState !== 'connecting') {
			this._neverEstablishedRecommendedAt = undefined;
			// The condition has broken, so the next attempt is timed from its own start.
			this._connectingForInMs = 0;

			return;
		}

		this._connectingForInMs += this.peerConnection.deltaTime ?? 0;

		for (const transport of this.peerConnection.iceTransports ?? []) {
			if (transport.iceState === 'failed' || transport.iceState === 'disconnected') return;
		}

		const conditionDurationInMs = this._connectingForInMs;

		if (conditionDurationInMs < config.restartRecommendationThresholdInMs) return;

		const now = Date.now();

		// Wall clock, unlike the condition clock above: this throttles notifications.
		if (this._neverEstablishedRecommendedAt !== undefined
			&& now - this._neverEstablishedRecommendedAt < config.restartRecommendationCooldownInMs) {
			return;
		}

		this._neverEstablishedRecommendedAt = now;
		this._neverEstablishedRecommendations += 1;

		const [ subject ] = this._bySeverity();

		this._recommend({
			peerConnectionId: this.peerConnection.peerConnectionId,
			reason: 'never-established',
			conditionDurationInMs,
			iceGeneration: 0,
			recommendationCount: this._neverEstablishedRecommendations,
			iceState: subject?.iceState,
			dtlsState: subject?.dtlsState,
		});
	}

	/** Picks the transport that best explains a stalled establishment, not whichever was listed first. */
	private static readonly ICE_STATE_SEVERITY: Record<string, number> = {
		failed: 6, disconnected: 5, checking: 4, new: 3, connected: 2, completed: 1, closed: 0,
	};

	private _bySeverity(): IceTransportMonitor[] {
		// nullish-guarded so a partially mocked monitor (tests, custom sources) stays judgeable
		return [ ...(this.peerConnection.iceTransports ?? []) ].sort(
			(a, b) => (IceRestartRecommendationDetector.ICE_STATE_SEVERITY[b.iceState ?? ''] ?? -1)
				- (IceRestartRecommendationDetector.ICE_STATE_SEVERITY[a.iceState ?? ''] ?? -1)
		);
	}

	private _expectsInboundMedia(transport: IceTransportMonitor): boolean {
		return 0 < transport.getInboundRtps().length;
	}

	private _recommend(payload: IceRestartRecommendedEventPayload) {
		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('ice-restart-recommended', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			...payload,
		});

		if (!this.config.createEvent) return;

		clientMonitor.addEvent({
			type: ClientEventTypes.ICE_RESTART_RECOMMENDED,
			payload: { ...payload },
		});
	}

	private _usernameFragmentOf(transport: IceTransportMonitor): string | undefined {
		return transport.iceLocalUsernameFragment
			?? transport.getSelectedCandidatePair()?.getLocalCandidate()?.usernameFragment;
	}

	private _getState(transport: IceTransportMonitor): TransportState {
		let state = this._states.get(transport.id);

		if (!state) {
			state = {
				usernameFragment: this._usernameFragmentOf(transport),
				iceGeneration: 0,
				restartPending: false,
				sawInboundTraffic: false,
				failedForInMs: 0,
				disconnectedForInMs: 0,
				stalledForInMs: 0,
				recommendations: 0,
			};
			this._states.set(transport.id, state);
		}

		return state;
	}
}

```
### IceTransportStalledDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceTransportStalledDetector.ts#L65)
Category: Connectivity
```ts
import { IceTransportMonitor } from "../monitors/IceTransportMonitor";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

export type IceTransportStalledIssuePayload = {
	peerConnectionId: string;
	transportId: string;
	iceState?: string;
	candidatePairState?: string;
	selectedCandidatePairId?: string;
	/** Inbound only — the both-directions-silent case is not reportable. */
	direction: 'inbound';
	stalledForMs: number;
	/** What was still going out while `inboundBytesDelta` stayed at zero. */
	outboundBytesDelta?: number;
	inboundBytesDelta?: number;
	currentRoundTripTime?: number;
	lastPacketReceivedTimestamp?: number;
	iceGeneration: number;
	/** Filled in when the finding closes. */
	durationInMs?: number;
};

type TransportState = {
	/** ICE restarts observed on this transport, inferred from the local username fragment. */
	iceGeneration: number;
	usernameFragment?: string;
	/** Whether inbound bytes were ever seen on this transport's selected pair. */
	sawInboundTraffic: boolean;
	/** Stats time accumulated while the stall condition held, reset the moment it breaks. */
	stalledForInMs: number;
	raisedAt?: number;
};

const ISSUE_TYPE = 'ice-transport-stalled';

export type IceTransportStalledDetectorConfig = {
	/** How long a connected transport may send without receiving anything before a stall is reported. */
	transportStallThresholdInMs: number;
}

/**
 * Reports the quiet failure every state machine misses: ICE `connected`, the selected pair
 * `succeeded`, no error anywhere, while the transport keeps sending and nothing comes back. Use it
 * to catch a dead path that still looks healthy — the only evidence is the asymmetry between what
 * leaves and what arrives.
 *
 * Our own outbound traffic makes the expectation defensible: a live path returns at least consent
 * responses and RTCP. Two guards keep it off paths where receiving nothing is healthy — inbound
 * traffic must have been seen here before, and inbound RTP must be attributed to this transport, so
 * a send-only SFU uplink with its seconds-apart consent bursts is never accused. The clock is stats
 * time; anything breaking the condition zeroes it, and an ICE restart also clears the
 * inbound-traffic latch, since the new generation has proven nothing yet.
 *
 * Silence in both directions is deliberately not reportable — it cannot be told apart from an idle
 * connection.
 *
 * Issue raised: `ice-transport-stalled`, resolved when inbound traffic resumes, when the path stops
 * being connected, or when the transport goes away. Config: `iceTransportStalledDetector`.
 *
 * Category: Connectivity
 * Layer: 5 — Path continuity
 *
 */
export class IceTransportStalledDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'ice-transport-stalled-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _states = new Map<string, TransportState>();

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.iceTransportStalledDetector!;
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) return;

		const seenIds = new Set<string>();

		for (const transport of this.peerConnection.iceTransports) {
			seenIds.add(transport.id);

			this._checkTransport(transport);
		}

		for (const transportId of [ ...this._states.keys() ]) {
			if (seenIds.has(transportId)) continue;

			this._resolve(transportId, 'ice transport is gone');
			this._states.delete(transportId);
		}
	}

	private _checkTransport(transport: IceTransportMonitor) {
		const state = this._getState(transport);
		const usernameFragment = this._usernameFragmentOf(transport);

		if (usernameFragment !== undefined && state.usernameFragment !== undefined
			&& usernameFragment !== state.usernameFragment) {
			state.iceGeneration += 1;
			state.stalledForInMs = 0;
			// The new generation has a new path and has proven nothing on it yet.
			state.sawInboundTraffic = false;

			this._resolve(transport.id, 'ice restarted');
		}
		if (usernameFragment !== undefined) state.usernameFragment = usernameFragment;

		const iceState = transport.iceState;
		const pair = transport.getSelectedCandidatePair();

		if ((iceState !== 'connected' && iceState !== 'completed') || !pair || pair.state !== 'succeeded') {
			state.stalledForInMs = 0;

			this._resolve(transport.id, 'ice path is no longer connected');

			return;
		}

		const inboundBytesDelta = pair.deltaBytesReceived;
		const outboundBytesDelta = pair.deltaBytesSent;

		// Half the evidence is no evidence: without both deltas the asymmetry cannot be measured.
		if (inboundBytesDelta === undefined || outboundBytesDelta === undefined) return;

		if (0 < inboundBytesDelta) {
			state.sawInboundTraffic = true;
			state.stalledForInMs = 0;

			this._resolve(transport.id, 'inbound traffic resumed');

			return;
		}

		if (!state.sawInboundTraffic || outboundBytesDelta <= 0) {
			state.stalledForInMs = 0;

			return;
		}

		if (!this._expectsInboundMedia(transport)) {
			state.stalledForInMs = 0;

			return;
		}

		state.stalledForInMs += transport.deltaTime ?? 0;

		if (state.stalledForInMs < this.config.transportStallThresholdInMs) return;
		if (state.raisedAt !== undefined) return;

		state.raisedAt = Date.now();

		this.peerConnection.issues.raise({
				key: this._issueKey(transport.id),
				includeInSample: this.includeIssueInSample,
				type: ISSUE_TYPE,
				payload: {
					peerConnectionId: this.peerConnection.peerConnectionId,
					transportId: transport.id,
					iceState,
					candidatePairState: pair.state,
					selectedCandidatePairId: transport.selectedCandidatePairId,
					direction: 'inbound',
					stalledForMs: state.stalledForInMs,
					outboundBytesDelta,
					inboundBytesDelta,
					currentRoundTripTime: pair.currentRoundTripTime,
					lastPacketReceivedTimestamp: pair.lastPacketReceivedTimestamp,
					iceGeneration: state.iceGeneration,
				},
			}
		);
	}

	/** Without an inbound RTP stream attributed here there is nothing for a stall to be about. */
	private _expectsInboundMedia(transport: IceTransportMonitor): boolean {
		return 0 < transport.getInboundRtps().length;
	}

	private _usernameFragmentOf(transport: IceTransportMonitor): string | undefined {
		return transport.iceLocalUsernameFragment
			?? transport.getSelectedCandidatePair()?.getLocalCandidate()?.usernameFragment;
	}

	private _getState(transport: IceTransportMonitor): TransportState {
		let state = this._states.get(transport.id);

		if (!state) {
			state = {
				iceGeneration: 0,
				usernameFragment: this._usernameFragmentOf(transport),
				sawInboundTraffic: false,
				stalledForInMs: 0,
			};
			this._states.set(transport.id, state);
		}

		return state;
	}

	private _resolve(transportId: string, comment: string) {
		const state = this._states.get(transportId);

		if (state?.raisedAt === undefined) return;

		const raisedAt = state.raisedAt;

		state.raisedAt = undefined;

		const key = this._issueKey(transportId);
		const issue = this.peerConnection.issues.get(key);

		if (!issue) return;

		this.peerConnection.issues.resolve({
			key: key,
			comment,
			payload: {
				...(issue.payload as IceTransportStalledIssuePayload),
				durationInMs: Date.now() - raisedAt,
			},
			resolvedAt: Date.now(),
		});
	}

	private _issueKey(transportId: string) {
		return `${ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}-transport-${transportId}`;
	}
}

```
### IceTraversalDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceTraversalDetector.ts#L26)
Category: Telemetry
```ts
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

/** No tunables. The type exists so the detector can be toggled: `{}` enables it, `null` disables it. */
export type IceTraversalDetectorConfig = Record<string, never>;

/**
 * Reports that the set of selected ICE candidate pairs changed — the network path under the call
 * moved. Use it to place the brief cut-out a user felt when Wi-Fi handed over to cellular, a VPN
 * came up, or a NAT rebinding forced a new pair. A tuple is
 * `localAddress:localPort:remoteAddress:remotePort:protocol`, built by the candidate pair itself,
 * so this and the connectivity detectors always agree on what the selected path is.
 *
 * Establishment is not a change: growing from an empty set is skipped.
 *
 * It reports only *that* the tuple set changed. `SelectedIcePath` classifies the kind of change,
 * and `UnstableIcePathDetector` owns the issue raised when a path keeps switching.
 *
 * Monitor event: `ice-tuple-changed`. No issue. Config: `iceTraversalDetector` — `{}` registers the
 * detector, `null` leaves it unregistered.
 *
 * Category: Telemetry
 * Layer: Transport
 *
 */
export class IceTraversalDetector implements Detector {
		public readonly name = 'ice-traversal-detector';
		
		public constructor(
				public readonly pcMonitor: PeerConnectionMonitor,
		) {
		}

		public readonly tuples = new Set<string>();

		public update() {
			if (this.pcMonitor.closed) return;
			
			const wasEmpty = this.tuples.size === 0;
			let changed = false;
			const curentTuples = new Set<string>();

			for (const pair of this.pcMonitor.selectedIceCandidatePairs) {
				const tuple = pair.tuple;

				curentTuples.add(tuple);
				if (!this.tuples.has(tuple)) {
					changed = true;
					this.tuples.add(tuple);
				}
			}
			for (const tuple of this.tuples) {
				if (!curentTuples.has(tuple)) {
					changed = true;
					this.tuples.delete(tuple);
				}
			}

			if (wasEmpty || !changed) return;
			
			this.pcMonitor.parent.emit('ice-tuple-changed', {
				clientMonitor: this.pcMonitor.parent,
				peerConnectionMonitor: this.pcMonitor,
			});
		}
	}
```
### InboundVideoFlowStateDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/InboundVideoFlowStateDetector.ts#L92)
Category: Perceived Quality
```ts
import { Detector } from "./Detector";
import { InboundTrackMonitor, InboundVideoFlowState } from "../monitors/InboundTrackMonitor";

/** The flow states that are a finding. Written as a subtraction so the two can never drift. */
export type VideoFlowIssueState = Exclude<InboundVideoFlowState, 'continuous'>;

type VideoFlowIssueBase = {
	peerConnectionId: string;
	trackId: string;
	/** How long the finding was open. Set when it resolves. */
	durationInMs?: number;
}

/** The picture stopped and stayed stopped. */
export type FrozenVideoFlow = VideoFlowIssueBase & {
	state: 'frozen';
	/** How long it had been stopped when the finding was raised, in ms. A floor, never above the truth. */
	observedFrozenTimeInMs: number;
}

/** The picture kept coming back and kept being interrupted. */
export type ChoppyVideoFlow = VideoFlowIssueBase & {
	state: 'choppy';
	/** Freezes counted across the detection window — at least `minFreezeCountForChoppy`. */
	freezeCount: number;
	/** The stretch they were counted over, in ms of stats time. */
	windowInMs: number;
	/** Share of that stretch the picture was stopped, `0..1`. */
	frozenRatio: number;
}

/** Discriminated on `state`: a freeze is one event with a length, choppiness several over a window. */
export type VideoFlowIssuePayload = FrozenVideoFlow | ChoppyVideoFlow;

export type InboundVideoFlowStateDetectorConfig = {
	/** How long one uninterrupted freeze must last to count as frozen rather than choppy, in ms. */
	frozenAfterInMs: number;

	/** Freezes across the detection window that make the picture choppy. Floored at two. */
	minFreezeCountForChoppy: number;
}

/**
 * Reports an inbound picture that stopped moving: repeatedly and briefly (`choppy`), or once and
 * for long (`frozen`). Use it to answer "is this person watching moving video right now" — the
 * complaint behind most "you're breaking up" reports, and one no single stat answers.
 *
 * **The evidence is `InboundTrackMonitor.slicedWindow`**, the same buffer every other detector on
 * the track reads, so this one keeps no history of its own — but over its own pair of slices,
 * `flowDetection` and `flowRecovery`, which are wider than the pair the others use. `totalFramesRendered`,
 * `totalFreezeCount` and `totalFreezesDurationInMs` are differenced across the detection window to
 * make the verdict, and across the recovery window behind it to decide when a choppy finding may
 * close. That replaces two private windows and a private clock, and it is what fixed the
 * sensitivity: an isolated freeze inside a multi-collection window no longer fills it, where
 * previously every freeze past `frozenAfterInMs` opened a finding that the next rendered frame
 * closed. On one captured call that produced eleven findings on a track that was moving 95% of the
 * time.
 *
 * The slice is the sustain, so how much evidence a verdict rests on is set by
 * `inboundTrackWindow.numberOfSamples.flowDetection`, not here — a wider slice is a slower, surer
 * detector, and `windowInMs` on the payload always says which stretch a given finding was measured
 * over. It is sized apart from the rest of the track's detectors because `frozen` is a claim about
 * *nothing at all* happening, which one interval cannot support: at the narrow pair a single empty
 * collection was a freeze, and the next rendered frame closed it again.
 *
 * `frozen` is **nothing rendered across the whole detection window**, which is a stronger claim
 * than one empty collection and takes as long to make as the window spans. A freeze that has
 * already ended is classified by its mean length: a mean at `frozenAfterInMs` proves one freeze
 * reached it, since a maximum is never below a mean. `choppy` is `minFreezeCountForChoppy` freezes
 * or more across the window with frames still arriving.
 *
 * The two states are mutually exclusive and one becoming the other closes the first: they are
 * different experiences with different causes, and a viewer whose stutter turned into a stop has a
 * new problem rather than a continuing one.
 *
 * `frozen` usually means delivery stopped or the decoder wedged; `choppy` usually means frames are
 * arriving late or in bursts. Both are what the viewer actually sees, so they are the right thing to
 * count when asking how a call went.
 *
 * It describes the picture, not the network — pair it with the transport detectors for a cause.
 * Paused tracks, a backgrounded tab and screen shares are not judged at all; note that a received
 * track is only known to be a screen share if the application declared it through `setContext`.
 *
 * Track attribute: `InboundTrackMonitor.frameFlowState`, also read by `DefaultScoreCalculator`.
 * Issue raised: `video-flow-disrupted`. Monitor event: `video-flow-disrupted`.
 * Config: `inboundVideoFlowStateDetector`.
 *
 * Category: Perceived Quality
 * Layer: Visual — continuity
 *
 */
export class InboundVideoFlowStateDetector implements Detector {
	public static readonly ISSUE_TYPE = 'video-flow-disrupted';
	public readonly name = 'inbound-video-flow-state-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	private readonly _issueKey: string;
	private _watching = false;
	/**
	 * Collections judged since this detector last stood down.
	 *
	 * The window is the track's, not this detector's, and it keeps being fed through a pause, a
	 * screen share and a backgrounded tab — every other detector on the track needs it to. So a
	 * window that is *full* is not necessarily full of collections this detector was looking at,
	 * and reading it on the first collection back would judge the stretch it deliberately skipped:
	 * a pause renders no frames, and would come back as a freeze. Counting what has been judged is
	 * what keeps a stand-down from being replayed as a fault.
	 */
	private _judgedCollections = 0;
	private _state?: InboundVideoFlowState;
	/** Wall clock, and only for the resolved issue's `durationInMs`. */
	private _raisedAt?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this._issueKey = `${InboundVideoFlowStateDetector.ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}-track-${trackMonitor.track.id}`;
	}

	private get config() {
		return this.peerConnection.parent.config.inboundVideoFlowStateDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	/** Floored at two: one freeze is one freeze, never stutter. */
	private get minFreezeCount() {
		return Math.max(2, this.config.minFreezeCountForChoppy);
	}

	public update() {
		if (this.disabled) return;

		const inboundRtp = this.trackMonitor.getInboundRtp();

		if (!inboundRtp || inboundRtp.kind !== 'video') {
			return this._standDown('the video stream is gone');
		}

		if (this.trackMonitor.readyState !== 'live') {
			return this._standDown('the track ended');
		}

		if (
			this.trackMonitor.paused ||
			this.trackMonitor.remoteOutboundTrackPaused ||
			this.trackMonitor.isScreenShare ||
			!this.peerConnection.parent.activeTab
		) {
			return this._standDown('not judging playback right now');
		}

		// Its own pair, wider than the one the rest of the track's detectors read: see
		// `InboundTrackWindowConfig.numberOfSamples`.
		const {
			flowDetection: detectionWindow,
			flowRecovery: recoveryWindow,
		} = this.trackMonitor.slicedWindow.slices;
		const renderedFrames = detectionWindow.deltaTotalFramesRendered
			?? detectionWindow.deltaTotalFramesDecoded;
		const freezes = detectionWindow.deltaTotalFreezeCount;
		const frozenInMs = detectionWindow.deltaTotalFreezesDurationInMs;
		const windowInMs = detectionWindow.durationInMs;

		// All three are load-bearing; missing any of them makes this stretch unjudgeable.
		if (renderedFrames === null || freezes === null || frozenInMs === null) {
			this.inputsUnavailable = true;

			return;
		}

		this.inputsUnavailable = false;

		// A window still filling is not a verdict, and a window spanning no stats time measures
		// nothing however many values it holds.
		if (!detectionWindow.isReady || windowInMs < 1) return;

		// Once, when judging starts, so `undefined` keeps meaning "no answer" rather than "healthy".
		if (!this._watching) {
			this.trackMonitor.frameFlowState = 'continuous';
			this._watching = true;
		}

		this._judgedCollections += 1;

		// The window may be full of collections this detector was not looking at; see the field.
		if (this._judgedCollections < detectionWindow.numberOfSamples) return;

		// Nothing rendered across the whole window: the picture is stopped, and has been for as
		// long as the window spans.
		if (renderedFrames === 0) {
			if (this.config.frozenAfterInMs <= windowInMs) {
				this._raise({
					state: 'frozen',
					observedFrozenTimeInMs: Math.max(frozenInMs, windowInMs),
				});
			}

			return;
		}

		// The picture is moving again, which ends a stop the moment it happens.
		if (this._state === 'frozen') {
			return this._resolve('the picture is moving again');
		}

		// A floor on the longest freeze here: a max is never below its mean, so a mean at the
		// threshold proves one freeze reached it.
		const longestFreezeInMs = 0 < freezes ? frozenInMs / freezes : 0;

		if (this.config.frozenAfterInMs <= longestFreezeInMs) {
			return this._raise({ state: 'frozen', observedFrozenTimeInMs: longestFreezeInMs });
		}

		if (this.minFreezeCount <= freezes) {
			return this._raise({
				state: 'choppy',
				freezeCount: freezes,
				windowInMs,
				frozenRatio: frozenInMs / windowInMs,
			});
		}

		if (this._state !== 'choppy') return;

		// Under the floor is not the same as clean, and the stretch behind this one has to be
		// clean too before a stutter is called over.
		if (0 < freezes) return;
		if (!recoveryWindow.isReady) return;

		const recoveryFreezes = recoveryWindow.deltaTotalFreezeCount;

		// No reading behind this one to corroborate with: the detection half decides alone rather
		// than holding a finding open on evidence that does not exist.
		if (recoveryFreezes !== null && 0 < recoveryFreezes) return;

		this._resolve('the picture has been continuous since');
	}

	private _raise(
		payload:
			| Omit<FrozenVideoFlow, 'peerConnectionId' | 'trackId'>
			| Omit<ChoppyVideoFlow, 'peerConnectionId' | 'trackId'>,
	) {
		// Mutually exclusive states: becoming the other closes the first rather than stacking.
		if (this._state === payload.state) return;
		if (this._state !== undefined) this._resolve(`the picture is ${payload.state} instead`);

		// After that resolve, never before — it sets the state back to `continuous`.
		this.trackMonitor.frameFlowState = payload.state;
		this._state = payload.state;
		this._raisedAt = Date.now();

		const clientMonitor = this.peerConnection.parent;
		const full: VideoFlowIssuePayload = {
			peerConnectionId: this.peerConnection.peerConnectionId,
			trackId: this.trackMonitor.track.id,
			...payload,
		};

		clientMonitor.emit('video-flow-disrupted', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			...full,
		});

		this.trackMonitor.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: InboundVideoFlowStateDetector.ISSUE_TYPE,
			payload: full,
		});
	}

	/** Forgets everything and closes any open finding. Guarded — this is a resting state for many tracks. */
	private _standDown(comment: string) {
		this.inputsUnavailable = false;

		if (this._watching) {
			this._watching = false;
			this._judgedCollections = 0;

			if (this._state !== undefined) this._resolve(comment);
		}

		// Last, overriding the `continuous` any resolve above set: nobody is looking, so there is no answer.
		this.trackMonitor.frameFlowState = undefined;
	}

	private _resolve(comment: string) {
		this._state = undefined;

		this.trackMonitor.frameFlowState = 'continuous';

		const issue = this.trackMonitor.issues.get(this._issueKey);

		this.trackMonitor.issues.resolve({
			key: this._issueKey,
			comment,
			payload: issue
				? {
					...(issue.payload as VideoFlowIssuePayload),
					durationInMs: this._raisedAt === undefined ? undefined : Date.now() - this._raisedAt,
				}
				: undefined,
			resolvedAt: Date.now(),
		});

		this._raisedAt = undefined;
	}
}

```
### InventedSpeechDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/InventedSpeechDetector.ts#L55)
Category: Perceived Quality
```ts
import { Detector } from "./Detector";
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";

/** One ongoing episode of audible invention on a single inbound audio track. */
export type InventedSpeechIssuePayload = {
	peerConnectionId: string;
	trackId: string;
	/** Share of the interval's audio that was invented, at the moment the issue was raised. */
	inventedSpeechRatio: number;
	/** Invented milliseconds beyond the allowance that had accumulated when it was raised. */
	excessInventedMs: number;
	/** Filled in when the issue is resolved. */
	durationInMs?: number;
}

export type InventedSpeechDetectorConfig = {
	/** Share of audio (`0..1`) that may be invented for free. Also the drain rate. */
	allowedInventedRatio: number;

	/**
	 * Invented milliseconds beyond the allowance needed to raise. Doubles as the resolve bar: a full
	 * accumulator empties after `raiseAfterInventedMs / allowedInventedRatio` ms of clean audio.
	 */
	raiseAfterInventedMs: number;
}

/**
 * Reports a listener being fed audio the sender never sent. Use it to answer how a call actually
 * sounded, which packet loss cannot: NetEQ hides a great deal of loss inaudibly, and audio falls
 * apart without dramatic loss when the jitter buffer misbehaves. What a listener hears is the
 * fabrication, so that is what is measured — `inboundRtp.inventedSpeechRatio`, which excludes
 * concealment during talker silence because nobody can hear the difference there.
 *
 * Each tick contributes `ratio × deltaTime` of invention against `allowedInventedRatio × deltaTime`
 * of tolerance, moving one accumulator clamped to `raiseAfterInventedMs`. The issue opens when it
 * is full and closes when it is empty. Integrating a rate makes the verdict independent of the
 * collection period, and a clean tick drains only the allowance, so a breath between two bad
 * stretches does not end the episode.
 *
 * A finding means this listener heard fabricated audio for a sustained stretch: loss or jitter on
 * the path from that talker, or a jitter buffer that could not keep up with it. It is per stream, so
 * one talker firing points at their uplink and every talker firing points at this listener's
 * downlink.
 *
 * It cannot tell one second at 25% from five at 5%, and it is not RFC 7294's per-second classifier:
 * the same 5% applied as a sustained rate rather than a verdict on each second.
 *
 * Issue raised: `invented-speech`. Monitor event: `invented-speech`.
 * Config: `inventedSpeechDetector`.
 *
 * Category: Perceived Quality
 * Layer: Audio — continuity
 *
 */
export class InventedSpeechDetector implements Detector {
	public static readonly ISSUE_TYPE = 'invented-speech';
	public readonly name = 'invented-speech-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	private readonly issueKey: string;
	/** Invented milliseconds accumulated beyond the allowance; the whole of this detector's state. */
	private _bucketInMs = 0;
	private _raised = false;
	private _startedAt?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this.issueKey = `${InventedSpeechDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private get config() {
		return this.peerConnection.parent.config.inventedSpeechDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) return;

		const inboundRtp = this.trackMonitor.getInboundRtp();

		if (!inboundRtp || inboundRtp.kind !== 'audio') return;

		if (this.trackMonitor.readyState !== 'live') {
			this._bucketInMs = 0;
			this.trackMonitor.inventedSpeechSeverity = undefined;

			return this._raised ? this._clear('track ended') : undefined;
		}
		if (this.trackMonitor.paused) {
			this._bucketInMs = 0;
			this.trackMonitor.inventedSpeechSeverity = undefined;

			return this._raised ? this._clear('consumer paused') : undefined;
		}
		if (this.trackMonitor.remoteOutboundTrackPaused) {
			this._bucketInMs = 0;
			this.trackMonitor.inventedSpeechSeverity = undefined;

			return this._raised ? this._clear('remote track paused') : undefined;
		}

		const ratio = inboundRtp.inventedSpeechRatio;

		if (ratio === undefined) {
			// No concealment counters, or no samples arrived. Blind, not fine.
			this.inputsUnavailable = true;
			this.trackMonitor.inventedSpeechSeverity = undefined;

			return;
		}

		this.inputsUnavailable = false;

		// One expression covers both directions: above the allowance it fills, below it drains.
		const elapsedInMs = inboundRtp.deltaTime ?? 0;
		const inventedInMs = ratio * elapsedInMs;
		const allowedInMs = this.config.allowedInventedRatio * elapsedInMs;

		this._bucketInMs = Math.min(
			this.config.raiseAfterInventedMs,
			Math.max(0, this._bucketInMs + inventedInMs - allowedInMs),
		);

		// Beside the verdict, the measurement it was a verdict on: how full the bucket is, where
		// `1` is the raise point. Published on every collection that was judged, so the score can
		// see audio heading towards a fault and not only the moment it becomes one.
		this.trackMonitor.inventedSpeechSeverity = 0 < this.config.raiseAfterInventedMs
			? this._bucketInMs / this.config.raiseAfterInventedMs
			: undefined;

		if (this._raised) {
			if (this._bucketInMs <= 0) return this._clear('audio recovered');

			return this.trackMonitor.issues.update({
				key: this.issueKey,
				payload: {
					excessInventedMs: this._bucketInMs,
					inventedSpeechRatio: ratio,
				},
			});
		}

		if (this._bucketInMs < this.config.raiseAfterInventedMs) return;

		this._raised = true;
		// Wall clock, and only for the resolved issue's `durationInMs`.
		this._startedAt = Date.now();

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('invented-speech', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			inventedSpeechRatio: ratio,
		});

		this.trackMonitor.issues.raise({
			key: this.issueKey,
			includeInSample: this.includeIssueInSample,
			type: InventedSpeechDetector.ISSUE_TYPE,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				inventedSpeechRatio: ratio,
				excessInventedMs: this._bucketInMs,
			},
		});
	}

	private _clear(comment: string) {
		this._raised = false;

		const issue = this.trackMonitor.issues.get(this.issueKey);
		let payload: InventedSpeechIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as InventedSpeechIssuePayload),
				durationInMs: this._startedAt ? Date.now() - this._startedAt : undefined,
			};
		}

		this.trackMonitor.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedAt = undefined;
	}
}

```
### JitterBufferStressDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/JitterBufferStressDetector.ts#L71)
Category: Perceived Quality
```ts
import { Detector } from "./Detector";
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";

export type JitterBufferStressIssuePayload = {
	peerConnectionId: string;
	trackId: string;
	/** What NetEQ is aiming for. */
	targetDelayInMs: number;
	/** What it really added per emitted sample. */
	actualDelayInMs?: number;
	/** Share of samples (`0..1`) stretched or compressed to keep up. */
	timeStretchRate: number;
	/** Collections in a row that agreed before raising. */
	consecutiveTicks: number;
	durationInMs?: number;
}

export type JitterBufferStressDetectorConfig = {
	/** Target delay above which the jitter buffer counts as stretched thin. */
	targetDelayThresholdInMs: number;

	/** Share of samples inserted or removed above which NetEQ counts as working hard. */
	timeStretchThreshold: number;

	/** Consecutive collections both conditions must hold before raising. */
	minConsecutiveTicks: number;

	/**
	 * The target delay at which the buffer counts as unbearable — the top of the severity scale,
	 * not a trigger. Only affects the published severity, never whether the issue is raised.
	 */
	unbearableTargetDelayInMs: number;

	/**
	 * The share of samples stretched or compressed that counts as unbearable — the top of the
	 * severity scale, not a trigger. Only affects the published severity, never the raise.
	 */
	unbearableTimeStretchRate: number;
}

/**
 * Reports an inbound track's audio jitter buffer fighting the network and losing — conversation gone
 * latent and slightly warped, voices sped up or dragged out. Use it to tell straining apart from a
 * buffer that has already run dry and is fabricating audio, which `InventedSpeechDetector` covers.
 *
 * A finding means the path is delivering unevenly enough that the buffer has to grow and warp
 * audio to cover it — congestion, a wireless link, or a route with variable queuing. The listener
 * hears added delay and slightly distorted voices before they hear anything break.
 *
 * Both a deep `jitterBufferTargetDelayInMs` and a raised `timeStretchRate` are required, for
 * `minConsecutiveTicks` collections: deep alone means NetEQ is succeeding, and stretching alone is
 * ordinary clock-drift correction. A tick missing either field is skipped rather than guessed at,
 * and a paused consumer or remote sender stands the detector down and resets the tick count.
 *
 * Beside the finding it publishes `InboundTrackMonitor.jitterBufferStressSeverity`, the geometric
 * mean of the same two witnesses measured against the levels that count as unbearable. It is an
 * absolute scale rather than a threshold-relative one: `0` is a buffer doing nothing and `1` is one
 * nobody could converse through, so the raise point sits well down the range — around `0.16` with
 * the shipped defaults — and most of the scale is left to say how much worse things got. Written on
 * every collection the detector could judge, below the threshold as well as above it, so a score
 * can fall off gradually instead of only when a finding opens. It never decides the raise.
 *
 * Issue raised: `audio-jitter-buffer-stress`. Monitor event: `audio-jitter-buffer-stress`.
 * Config: `jitterBufferStressDetector`.
 * Track attribute: `InboundTrackMonitor.jitterBufferStressSeverity`.
 *
 * Category: Perceived Quality
 * Layer: Responsiveness
 *
 */
export class JitterBufferStressDetector implements Detector {
	public static readonly ISSUE_TYPE = 'audio-jitter-buffer-stress';
	public readonly name = 'jitter-buffer-stress-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly issueKey: string;
	private _consecutiveTicks = 0;
	private _alertOn = false;
	private _startedAt?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this.issueKey = `${JitterBufferStressDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private get config() {
		return this.peerConnection.parent.config.jitterBufferStressDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) return;

		const inboundRtp = this.trackMonitor.getInboundRtp();

		if (!inboundRtp || inboundRtp.kind !== 'audio') return;
		if (this.trackMonitor.readyState !== 'live') {
			this._consecutiveTicks = 0;
			this.trackMonitor.jitterBufferStressSeverity = undefined;

			return this._alertOn ? this._clear('track ended') : undefined;
		}
		if (this.trackMonitor.paused) {
			this._consecutiveTicks = 0;
			this.trackMonitor.jitterBufferStressSeverity = undefined;

			return this._alertOn ? this._clear('consumer paused') : undefined;
		}
		if (this.trackMonitor.remoteOutboundTrackPaused) {
			this._consecutiveTicks = 0;
			this.trackMonitor.jitterBufferStressSeverity = undefined;

			return this._alertOn ? this._clear('remote track paused') : undefined;
		}

		const targetDelayInMs = inboundRtp.jitterBufferTargetDelayInMs;
		const timeStretchRate = inboundRtp.timeStretchRate;

		// A collection missing either witness is not judged at all, so the severity says nothing
		// rather than reporting the half it happens to have.
		if (targetDelayInMs === undefined || timeStretchRate === undefined) {
			this.trackMonitor.jitterBufferStressSeverity = undefined;

			return;
		}

		this.trackMonitor.jitterBufferStressSeverity = this._severity(targetDelayInMs, timeStretchRate);

		const stressed = this.config.targetDelayThresholdInMs < targetDelayInMs &&
			this.config.timeStretchThreshold < timeStretchRate;

		if (!stressed) {
			this._consecutiveTicks = 0;

			if (this._alertOn) {
				this._clear('jitter buffer recovered');
			}

			return;
		}

		this._consecutiveTicks += 1;

		if (this._alertOn) return;
		if (this._consecutiveTicks < this.config.minConsecutiveTicks) return;

		this._alertOn = true;
		this._startedAt = Date.now();

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('audio-jitter-buffer-stress', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			targetDelayInMs,
			timeStretchRate,
		});

		this.trackMonitor.issues.raise({
				key: this.issueKey,
				includeInSample: this.includeIssueInSample,
			type: JitterBufferStressDetector.ISSUE_TYPE,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				targetDelayInMs,
				actualDelayInMs: inboundRtp.avgJitterBufferDelayInMs,
				timeStretchRate,
				consecutiveTicks: this._consecutiveTicks,
			},
		});
	}

	/**
	 * How bad the buffer's behaviour is on an absolute scale, `0..1`, from the two witnesses the
	 * raise tests.
	 *
	 * Each witness is its value against the level that counts as unbearable, so `0` is a buffer
	 * doing nothing at all and `1` is one nobody could hold a conversation through. The scale is
	 * anchored on that, not on the thresholds, which is what puts the raise point well down the
	 * range rather than at zero: with the shipped defaults the issue opens around `0.16`, leaving
	 * most of the scale to describe how much worse it got afterwards.
	 *
	 * The two are combined with a geometric mean, so a witness at zero takes the whole thing to
	 * zero — the same "deep alone means NetEQ is succeeding, stretching alone is clock drift" that
	 * decides the finding. Undefined when an unbearable level is not positive, which leaves nothing
	 * to scale against.
	 */
	private _severity(targetDelayInMs: number, timeStretchRate: number): number | undefined {
		const witness = (value: number, unbearable: number) =>
			0 < unbearable ? Math.min(1, Math.max(0, value / unbearable)) : undefined;

		const delay = witness(targetDelayInMs, this.config.unbearableTargetDelayInMs);
		const stretch = witness(timeStretchRate, this.config.unbearableTimeStretchRate);

		if (delay === undefined || stretch === undefined) return undefined;

		return Math.sqrt(delay * stretch);
	}

	private _clear(comment: string) {
		this._alertOn = false;

		const issue = this.trackMonitor.issues.get(this.issueKey);
		let payload: JitterBufferStressIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as JitterBufferStressIssuePayload),
				durationInMs: this._startedAt ? Date.now() - this._startedAt : undefined,
			};
		}

		this.trackMonitor.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedAt = undefined;
	}
}

```
### PixelatedVideoDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/PixelatedVideoDetector.ts#L75)
Category: Perceived Quality
```ts
import { Detector } from "./Detector";
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";

export type PixelatedVideoIssuePayload = {
	peerConnectionId: string;
	trackId: string;
	/** The mean quantizer as a fraction of this codec's scale, `0..1`, at the moment of raising. */
	normalizedQp: number;
	/** The same reading in the codec's own units, which is what a debugger will want to compare. */
	avgQpPerFrame: number;
	/** The codec those units belong to; the two are meaningless apart. */
	mimeType?: string;
	frameWidth?: number;
	frameHeight?: number;
	framesPerSecond?: number;
	/** How long the picture stayed this coarse before raising, from stats timestamps. */
	sustainedForInMs: number;
	/** Filled in when the issue is resolved. */
	durationInMs?: number;
}

export type PixelatedVideoDetectorConfig = {
	/**
	 * Fraction of the codec's quantizer scale at or above which the picture counts as coarse.
	 *
	 * A fraction rather than a quantizer, so one number covers every codec: `0.62` is a mean
	 * quantizer of 79 on VP8, 158 on VP9 and AV1, and 32 on H.264 and H.265.
	 */
	threshold: number;

	/** Fraction below which the issue resolves. Keep it under `threshold`. */
	recoveryThreshold: number;

	/** How long (ms of stats time) the picture must stay coarse before raising. */
	durationInMs: number;
}

/**
 * Reports video the viewer would call blocky or smeared: a picture drawn too coarsely, for long
 * enough to be worth complaining about. Use it for the case no pipeline detector can reach —
 * nothing has stalled, frames arrive, decode and render on time, and the experience is still bad.
 *
 * **The judgement is the quantizer, and only the quantizer.** `InboundRtpMonitor.normalizedQp` is
 * the mean quantizer of the interval as a fraction of the codec's own scale, derived from `qpSum`.
 * A high quantizer is what a blocky picture is *made of*, which makes it the direct measurement
 * rather than a proxy for one.
 *
 * **Without `qpSum` this detector does not judge.** It sets `inputsUnavailable` and says nothing.
 * That is a statement of what it can do, not a compatibility gap to be papered over: an
 * application that wants pixelation reported has to be receiving `qpSum` and a codec whose scale
 * is known, and one that is not should be told it cannot have this finding rather than handed a
 * guess. The previous judgement, `bitPerPixel`, was such a guess and was wrong in the direction
 * that matters most — bits per pixel falls with frame area and with how cheap the content is to
 * code, so a large, static, visually perfect screen share reads as more pixelated than a small
 * camera picture at a quarter of the quality. On one captured call the screen share's median
 * `bitPerPixel` sat exactly on the threshold, producing a finding every ninety seconds, while its
 * mean quantizer of 15 on VP8's 127-point scale said the picture was close to lossless.
 *
 * A finding means the sender is encoding this stream coarsely: their uplink is limited, an SFU is
 * forwarding a low simulcast layer, or the encoder was configured for less than the resolution
 * needs.
 *
 * It is not a perceptual model, and content still matters at the margin: the same quantizer is more
 * visible on detailed content than on flat. Screen shares are excluded outright rather than given a
 * second threshold — but note that a track is only known to be a screen share if the application
 * says so through `setContext`, since nothing in the stats of a *received* track reveals it.
 *
 * Issue raised: `pixelated-video`. Monitor event: `pixelated-video`.
 * Config: `pixelatedVideoDetector`.
 *
 * Category: Perceived Quality
 * Layer: Visual — clarity
 *
 */
export class PixelatedVideoDetector implements Detector {
	public static readonly ISSUE_TYPE = 'pixelated-video';
	public readonly name = 'pixelated-video-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	private readonly issueKey: string;
	private _sustainedForInMs = 0;
	private _raised = false;
	private _startedAt?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this.issueKey = `${PixelatedVideoDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private get config() {
		return this.peerConnection.parent.config.pixelatedVideoDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) return;

		const inboundRtp = this.trackMonitor.getInboundRtp();

		if (!inboundRtp || inboundRtp.kind !== 'video') return;

		if (this.trackMonitor.readyState !== 'live') {
			this._sustainedForInMs = 0;

			if (this._raised) this._resolve('track ended');

			return;
		}

		if (this.trackMonitor.paused || this.trackMonitor.remoteOutboundTrackPaused) {
			this._sustainedForInMs = 0;

			if (this._raised) this._resolve('track paused');

			return;
		}

		// A screen share is coded coarsely on purpose where nothing is moving, and looks perfect.
		// Only the application knows this: a received track carries no `displaySurface`.
		if (this.trackMonitor.isScreenShare) {
			this._sustainedForInMs = 0;

			if (this._raised) this._resolve('screen share');

			return;
		}

		const normalizedQp = inboundRtp.normalizedQp;

		// No `qpSum`, no codec, or a codec whose scale is unknown. Blind, not healthy — and this
		// detector has nothing else to fall back on, by design.
		if (normalizedQp === undefined) {
			this.inputsUnavailable = true;
			this._sustainedForInMs = 0;

			if (this._raised) this._resolve('no quantizer reported');

			return;
		}

		this.inputsUnavailable = false;

		if (normalizedQp < this.config.recoveryThreshold) {
			this._sustainedForInMs = 0;

			if (this._raised) this._resolve('picture quality recovered');

			return;
		}

		// Between the two thresholds: hold whatever state exists, and let nothing accumulate.
		if (normalizedQp < this.config.threshold) return;

		this._sustainedForInMs += inboundRtp.deltaTime ?? 0;

		if (this._raised) return;
		if (this._sustainedForInMs < this.config.durationInMs) return;

		this._raised = true;
		this._startedAt = Date.now();

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('pixelated-video', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			normalizedQp,
		});

		this.trackMonitor.issues.raise({
			key: this.issueKey,
			includeInSample: this.includeIssueInSample,
			type: PixelatedVideoDetector.ISSUE_TYPE,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				normalizedQp,
				avgQpPerFrame: inboundRtp.avgQpPerFrame as number,
				mimeType: inboundRtp.getCodec()?.mimeType,
				frameWidth: inboundRtp.frameWidth,
				frameHeight: inboundRtp.frameHeight,
				framesPerSecond: inboundRtp.framesPerSecond,
				sustainedForInMs: this._sustainedForInMs,
			},
		});
	}

	private _resolve(comment: string) {
		this._raised = false;

		const issue = this.trackMonitor.issues.get(this.issueKey);
		let payload: PixelatedVideoIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as PixelatedVideoIssuePayload),
				durationInMs: this._startedAt ? Date.now() - this._startedAt : undefined,
			};
		}

		this.trackMonitor.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedAt = undefined;
	}
}

```
### PlayoutDiscrepancyDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/PlayoutDiscrepancyDetector.ts#L63)
Category: Pipeline Disruption
```ts
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";
import { Detector } from "./Detector";

export type PlayoutDiscrepancyIssuePayload = {
	trackId: string;
	/** Frames delivered to the track minus frames painted, over the tick that opened the episode. */
	frameSkew: number;
	/** {@link frameSkew} over the frames received in that tick — what the thresholds compare. */
	skewRatio?: number;
	/** The track's smoothed frame rate at that moment, for scale. */
	ewmaFps?: number;
	/** Filled in when the finding closes. */
	durationInMs?: number;
}

export type PlayoutDiscrepancyDetectorConfig = {
	/** Skew ratio at which an open episode resolves. */
	lowSkewRatio: number;

	/** Skew ratio at which an episode opens. A ratio, not a frame count, so it means the same at every interval and frame rate. */
	highSkewRatio: number;

	/** Frames the interval must carry before the ratio is computed at all. */
	minFramesReceived: number;
}

/**
 * Reports frames that arrived at an inbound video track but were never painted. Use it to tell a
 * rendering-path fault apart from loss, jitter or a slow decoder: the viewer sees a frozen or
 * stuttering tile while every network statistic reads healthy, because the frames are here and
 * something after the network dropped them.
 *
 * A finding means the fault is after the network and after the decoder: a throttled or hidden
 * element, a compositor under load, or a renderer that cannot keep up with the machine it is on.
 * Nothing about the call needs fixing; the page or the device does.
 *
 * Both frame counters come from `InboundTrackMonitor.slicedWindow` rather than from one
 * collection's deltas, so the ratio is an average over the window the whole inbound cluster judges
 * on. That is what catches a renderer dropping in bursts: interleave a stalled second with a clean
 * one and no single collection need cross the bar, while the window still shows a tenth of the
 * picture going unpainted. Endpoint differencing also means a missed collection costs nothing,
 * because the totals carry across it.
 *
 * The two skew ratios are hysteresis, not two conditions — the episode opens above `highSkewRatio`
 * and closes only below `lowSkewRatio`, so a track at the boundary does not flap. That hysteresis
 * is the detector's own and is kept: the window supplies the measurement, not the resolve.
 *
 * It refuses to judge a backgrounded tab, a paused consumer or a paused remote sender, where the
 * skew is by design rather than a fault.
 *
 * Issue raised: `inbound-video-playout-discrepancy`, resolved when the skew drops below
 * the low threshold or the detector stands down.
 * Monitor event: `inbound-video-playout-discrepancy`.
 * Config: `playoutDiscrepancyDetector`.
 * Track attributes: `InboundTrackMonitor.playoutDiscrepancy` for the verdict, and
 * `InboundTrackMonitor.videoPlayoutSkew` for the share of arriving frames that went unpainted,
 * written on every judged collection whether or not it crossed a threshold.
 *
 * Category: Pipeline Disruption
 * Layer: Receive — decoder to renderer
 *
 */
export class PlayoutDiscrepancyDetector implements Detector {
	public static readonly ISSUE_TYPE = 'inbound-video-playout-discrepancy';
	public readonly name = 'playout-discrepancy-detector';
	public disabled = false;
	public includeIssueInSample = true;
	
	private readonly issueKey: string;

	private _startedDiscrepancyAt?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this.issueKey = `${PlayoutDiscrepancyDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	private get config() {
		return this.peerConnection.parent.config.playoutDiscrepancyDetector!;
	}

	public active = false;

	private _standDown(comment: string): void {
		if (!this.active) return;

		this._resolve(comment);
		this.active = false;
	}

	public update() {

		if (this.disabled) {
			this.trackMonitor.playoutDiscrepancy = undefined;
			this.trackMonitor.videoPlayoutSkew = undefined;

			return;
		}

		if (!this.peerConnection.parent.activeTab) {
			this.trackMonitor.playoutDiscrepancy = undefined;
			this.trackMonitor.videoPlayoutSkew = undefined;

			if (this.active) {
				this._resolve('tab in background');
				this.active = false;
			}

			return;
		}

		if (this.trackMonitor.readyState !== 'live') {
			this.trackMonitor.playoutDiscrepancy = undefined;
			this.trackMonitor.videoPlayoutSkew = undefined;

			return this._standDown('track ended');
		}
		if (this.trackMonitor.paused) {
			this.trackMonitor.playoutDiscrepancy = undefined;
			this.trackMonitor.videoPlayoutSkew = undefined;

			return this._standDown('consumer paused');
		}
		if (this.trackMonitor.remoteOutboundTrackPaused) {
			this.trackMonitor.playoutDiscrepancy = undefined;
			this.trackMonitor.videoPlayoutSkew = undefined;

			return this._standDown('remote track paused');
		}

		const { detection: detectionWindow } = this.trackMonitor.slicedWindow.slices;
		const framesReceived = detectionWindow.deltaTotalFramesReceived;
		const framesRendered = detectionWindow.deltaTotalFramesRendered;

		// No render counter over the window: the comparison cannot be made at all.
		if (framesReceived === null || framesRendered === null) {
			this.trackMonitor.playoutDiscrepancy = undefined;
			this.trackMonitor.videoPlayoutSkew = undefined;

			return;
		}

		// Not judged before the window says it holds the stretch it is configured to cover.
		if (!detectionWindow.isReady) {
			this.trackMonitor.playoutDiscrepancy = undefined;
			this.trackMonitor.videoPlayoutSkew = undefined;

			return;
		}

		if (framesReceived < this.config.minFramesReceived) {
			this.trackMonitor.playoutDiscrepancy = undefined;
			this.trackMonitor.videoPlayoutSkew = undefined;

			return this._standDown('too few frames to judge');
		}

		const frameSkew = framesReceived - framesRendered;
		const skewRatio = frameSkew / framesReceived;

		// Beside the flag: the measurement it was a verdict on, on every collection that was judged
		// rather than only the ones past the threshold, so a score can read how much of the picture
		// is being dropped before it becomes a finding.
		this.trackMonitor.videoPlayoutSkew = skewRatio;

		if (this.active) {
			if (skewRatio < this.config.lowSkewRatio) {
				this.trackMonitor.playoutDiscrepancy = false;
				this._resolve('playout discrepancy ended');
				this.active = false;
				return;
			}

			return;
		}

		if (skewRatio < this.config.highSkewRatio) {
			this.trackMonitor.playoutDiscrepancy = false;

			return;
		}

		this.active = true;
		// Set here, not at the call sites, so the flag and the finding cannot drift.
		this.trackMonitor.playoutDiscrepancy = true;

		const clientMonitor = this.peerConnection.parent;

		// Spelled out rather than taken from the static: applications grep for the event name.
		clientMonitor.emit('inbound-video-playout-discrepancy', {
			trackMonitor: this.trackMonitor,
			clientMonitor: clientMonitor,
		});

		this._raise({
			trackId: this.trackMonitor.track.id,
			frameSkew,
			skewRatio,
			ewmaFps: this.trackMonitor.getInboundRtp()?.ewmaFps,
		});
	}

	private _raise(payload: PlayoutDiscrepancyIssuePayload) {
		this._startedDiscrepancyAt = Date.now();

		this.trackMonitor.issues.raise({
				key: this.issueKey,
				includeInSample: this.includeIssueInSample,
			type: PlayoutDiscrepancyDetector.ISSUE_TYPE,
			payload,
		});
	}

	private _resolve(comment?: string) {
		const issue = this.trackMonitor.issues.get(this.issueKey);
		let payload: PlayoutDiscrepancyIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as PlayoutDiscrepancyIssuePayload),
				durationInMs: this._startedDiscrepancyAt ? Date.now() - this._startedDiscrepancyAt : undefined,
			};
		}

		this.trackMonitor.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedDiscrepancyAt = undefined;
	}
}
```
### RtpSenderStalledDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/RtpSenderStalledDetector.ts#L51)
Category: Pipeline Disruption
```ts
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

export type RtpSenderStalledIssuePayload = {
	peerConnectionId: string;
	ssrc: number;
	trackId?: string;
	/** Encoder progress over the interval the issue was raised on. */
	framesEncodedDelta?: number;
	/** Sender progress over that same interval — the flat counter that is the whole finding. */
	packetsSentDelta?: number;
	/** How long the boundary had been broken at raise time, in stats time. */
	stalledForMs: number;
	/** Filled in when the issue is resolved. */
	durationInMs?: number;
};

type SenderState = {
	/** Stats time the boundary has been broken for; `undefined` while it is not broken. */
	stalledForMs?: number;
	raisedAt?: number;
};

const ISSUE_TYPE = 'rtp-sender-stalled';

export type RtpSenderStalledDetectorConfig = {
	/** How long the broken stage boundary must persist before the issue is raised, in ms. */
	thresholdInMs: number;
}

/**
 * Reports a wedged RTP sender or pacer: the encoder keeps producing frames while packets stop
 * leaving. Use it to name the stage rather than the symptom — the difference between "the call
 * broke" and a sender that will never transmit again, as seen after `replaceTrack` races and
 * simulcast reconfigurations.
 *
 * The boundary is broken when `deltaFramesEncoded > 0` while `deltaPacketsSent === 0` on the same
 * outbound RTP, held past `thresholdInMs` of accumulated stats time. The innocent explanations for
 * silence on the wire — congestion, adaptation, a paused sender — would have stopped the *encoder*,
 * so they cannot produce this signature; a track that is missing, muted, not live or on an inactive
 * simulcast layer is refused outright. State is per ssrc, since layers wedge one at a time.
 *
 * Issue raised: `rtp-sender-stalled`. Monitor event: `rtp-sender-stalled`.
 * Config: `rtpSenderStalledDetector`.
 * Connection attribute: `PeerConnectionMonitor.stalledRtpSender`.
 *
 * Category: Pipeline Disruption
 * Layer: Send — encoder to RTP sender
 *
 */
export class RtpSenderStalledDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'rtp-sender-stalled-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _states = new Map<number, SenderState>();

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.rtpSenderStalledDetector!;
	}

	public update(): void {
		if (this.disabled) {
			this.peerConnection.stalledRtpSender = undefined;

			return;
		}
		if (this.peerConnection.closed) {
			this.peerConnection.stalledRtpSender = undefined;

			return;
		}

		const seenSsrcs = new Set<number>();
		// The connection's flag is the worst of its senders: any one wedged is a wedged connection,
		// and it takes at least one judgeable sender before silence can be called health.
		let anyJudged = false;

		for (const outboundRtp of this.peerConnection.outboundRtps) {
			seenSsrcs.add(outboundRtp.ssrc);

			const state = this._getState(outboundRtp.ssrc);
			const track = outboundRtp.getTrack()?.track;

			const guarded = !track || track.muted || track.readyState !== 'live' || outboundRtp.active === false;
			const framesEncodedDelta = outboundRtp.deltaFramesEncoded;
			const packetsSentDelta = outboundRtp.deltaPacketsSent;

			if (!guarded && framesEncodedDelta !== undefined && packetsSentDelta !== undefined) {
				anyJudged = true;
			}
			// An encoded frame always packetizes, so a sustained violation is a wedged sender or pacer.
			const broken = !guarded
				&& framesEncodedDelta !== undefined && 0 < framesEncodedDelta
				&& packetsSentDelta !== undefined && packetsSentDelta === 0;

			if (!broken) {
				this._clear(outboundRtp.ssrc, 'packets are leaving the rtp sender again');
				continue;
			}

			if (state.stalledForMs === undefined) {
				state.stalledForMs = 0;
			} else {
				// Stats time, not wall-clock: only observed intervals count towards the threshold.
				state.stalledForMs += outboundRtp.deltaTime ?? 0;
			}

			if (state.stalledForMs < this.config.thresholdInMs) continue;
			if (state.raisedAt !== undefined) continue;

			state.raisedAt = Date.now();

			const clientMonitor = this.peerConnection.parent;
			const payload: RtpSenderStalledIssuePayload = {
				peerConnectionId: this.peerConnection.peerConnectionId,
				ssrc: outboundRtp.ssrc,
				trackId: track?.id,
				framesEncodedDelta,
				packetsSentDelta,
				stalledForMs: state.stalledForMs,
			};

			clientMonitor.emit('rtp-sender-stalled', {
				clientMonitor,
				peerConnectionMonitor: this.peerConnection,
				...payload,
			});

			this.peerConnection.issues.raise({
				key: this._issueKey(outboundRtp.ssrc),
				includeInSample: this.includeIssueInSample,
				type: ISSUE_TYPE,
				payload,
			});
		}

		for (const ssrc of [ ...this._states.keys() ]) {
			if (seenSsrcs.has(ssrc)) continue;

			this._clear(ssrc, 'outbound rtp is gone');
			this._states.delete(ssrc);
		}

		const anyStalled = [ ...this._states.values() ].some((state) => state.raisedAt !== undefined);

		this.peerConnection.stalledRtpSender = anyStalled ? true : anyJudged ? false : undefined;
	}

	private _getState(ssrc: number): SenderState {
		let state = this._states.get(ssrc);

		if (!state) {
			state = {};
			this._states.set(ssrc, state);
		}

		return state;
	}

	private _clear(ssrc: number, comment: string) {
		const state = this._states.get(ssrc);

		if (!state) return;

		state.stalledForMs = undefined;

		if (state.raisedAt === undefined) return;

		const key = this._issueKey(ssrc);
		const issue = this.peerConnection.issues.get(key);

		if (issue) {
			this.peerConnection.issues.resolve({
				key: key,
				comment,
				payload: {
					...issue.payload,
					durationInMs: Date.now() - state.raisedAt,
				} as RtpSenderStalledIssuePayload,
				resolvedAt: Date.now(),
			});
		}

		state.raisedAt = undefined;
	}

	private _issueKey(ssrc: number) {
		return `${ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}-send-${ssrc}`;
	}
}

```
### SilentAudioSourceDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/SilentAudioSourceDetector.ts#L106)
Category: Pipeline Disruption
```ts
import { Detector } from "./Detector";
import { OutboundTrackMonitor } from "../monitors/OutboundTrackMonitor";

/**
 * What the evidence says the silence is. The three are distinguishable from the stats and are not
 * equally strong, so the finding carries which one it rests on rather than flattening them.
 */
export type SilenceKind =
	/** Every sample was exactly zero. The device handed over digital silence — the strongest case. */
	| 'digital-silence'
	/** A real signal, too faint to be heard. A dead preamp, a gain at zero, or a very distant speaker. */
	| 'below-threshold'
	/** The sample clock did not move at all while the track claimed to be live: capture itself stalled. */
	| 'no-samples';

export type SilentAudioSourceIssuePayload = {
	peerConnectionId: string;
	trackId: string;

	/** Which of the three silences the stats showed; see `SilenceKind`. */
	silenceKind: SilenceKind;

	/** RMS level over the most recent collection; absent when no samples were captured to measure. */
	rmsAudioLevel?: number;

	/** Milliseconds of stats time the source has been silent, kept current while the issue is open. */
	silentForInMs: number;

	/**
	 * Milliseconds of audio the source actually delivered over that same stretch; absent when the
	 * browser does not report the sample clock. Well below `silentForInMs` means capture stalled
	 * rather than the room went quiet.
	 */
	capturedForInMs?: number;

	deviceLabel?: string;
}

const ISSUE_TYPE = 'silent-audio-source';

export type SilentAudioSourceDetectorConfig = {
	/** How long a live, unmuted microphone must produce silence before it is reported. */
	silenceThresholdInMs: number;

	/** RMS level at or below which the source counts as silent. */
	silenceRmsThreshold: number;

	/**
	 * RMS level a source has to reach before an open finding clears. Keep it above
	 * `silenceRmsThreshold` and below a working microphone's noise floor.
	 *
	 * The gap between the two is a dead band, and it exists because the raise threshold sits in
	 * the empty space between digital silence and a real noise floor: a source hovering just under
	 * it will cross by a dither bit or two and cross back, opening and closing the finding every
	 * few collections. Clearing needs a level a working device could actually produce, not merely
	 * one above the floor of what counts as silent.
	 */
	recoveryRmsThreshold: number;
}

/**
 * Reports a microphone that is live, unmuted, enabled and capturing nothing anyone could hear —
 * the "you're on mute" that muting does not explain. Use it to tell a dead capture device apart
 * from a healthy call, because the fault shows up nowhere else in the stats: the encoder runs,
 * packets flow, the transport is fine, and nobody can hear this person.
 *
 * It reads the media source's `rmsAudioLevel`, which integrates energy over the whole interval.
 * Not `audioLevel`: that reads zero between words and would fire on every pause for breath.
 *
 * **What separates a dead device from a quiet room.** Chiefly the measurement, not the clock. A
 * working microphone in a silent room still delivers its own noise floor — self-noise and preamp
 * hiss survive noise suppression at roughly -60 to -70 dBFS, which is several times the shipped
 * threshold of -80 dBFS. A device handing over digital silence reads exactly zero. The two sit
 * either side of a wide empty gap, and `silenceKind` records which side the finding is on.
 *
 * The duration threshold is not what makes that distinction, and does not need to be long enough
 * to outlast a listener. What it buys is immunity to a transient: a resampler hiccup or a buffer
 * underrun can zero one interval on a device that is working. It is a debounce, and a shorter one
 * would still serve — a dead microphone is a minute of lost recording.
 *
 * A sample clock that does not move at all is treated as a fault rather than as nothing to judge:
 * a live, unmuted track that produced no audio has a stalled capture pipeline, which is a stronger
 * finding than silence, not a weaker one. It is only when the browser reports no sample clock at
 * all — or reports samples with no energy alongside them — that there is nothing to go on and the
 * detector stands down.
 *
 * **It judges microphones only.** A track carrying screen-share audio, a WebAudio destination
 * node or a media file is silent whenever nothing is playing, which is not a fault and must not be
 * reported as one. A track the application has marked as screen share stands the check down, and so
 * does one whose settings name no capture device — the structural test, needed because
 * `contentType` is inferred from `getSettings().displaySurface`, a *video* track setting, so
 * display-capture audio is never auto-marked however plain its device label makes it.
 *
 * A paused sender, or a track that is not `live`, muted or disabled, also stands the check down:
 * silence is the correct behaviour there.
 *
 * Raises `silent-audio-source`, updated while it stays open so its measured stretch never goes
 * stale. Emits `silent-audio-source` once, at the raise.
 * Config: `silentAudioSourceDetector`.
 * Track attribute: `OutboundTrackMonitor.silentAudioSource`.
 *
 * Category: Pipeline Disruption
 * Layer: Send — the source
 *
 */
export class SilentAudioSourceDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'silent-audio-source-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _issueKey: string;
	private _raised = false;
	private _silentForInMs = 0;
	private _capturedForInMs?: number;

	public constructor(
		public readonly trackMonitor: OutboundTrackMonitor,
	) {
		this._issueKey = `${ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private get config() {
		return this.peerConnection.parent.config.silentAudioSourceDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) {
			this.trackMonitor.silentAudioSource = undefined;

			return;
		}

		// Video tracks carry this detector too, and leaving the verdict untouched is what says so:
		// `undefined` is "not judged here", which is right for a track it cannot judge.
		if (this.trackMonitor.kind !== 'audio') return;

		// **Only a capture device can be a microphone nobody can hear.** Screen-share audio, a
		// `MediaStreamAudioDestinationNode`, a media file piped into the call: all of them are
		// legitimately silent most of the time, and reporting that as a fault is noise. Both tests
		// are needed. The declared one catches a track the application marked, and the structural
		// one catches what the library can see for itself — `contentType` is auto-detected from
		// `getSettings().displaySurface`, which is a *video* track setting, so display-capture
		// audio is never auto-marked as screen share however obvious it looks from its label.
		if (this.trackMonitor.isScreenShare) return this._clear({
			comment: 'screen share audio, not a microphone',
		});
		if (!this.trackMonitor.settings?.deviceId) return this._clear({
			comment: 'no capture device, not a microphone',
		});

		const track = this.trackMonitor.track;
		const mediaSource = this.trackMonitor.getMediaSource();

		if (this.trackMonitor.paused) return this._clear({
			comment: 'sender paused',
		});
		if (track.readyState !== 'live' || track.muted || !track.enabled) return this._clear({
			comment: 'track not capturing',
		});

		// Seconds of audio the source delivered this collection. Undefined means the browser does
		// not report the sample clock, which is a different thing from reporting that it did not move.
		const capturedInSec = mediaSource?.deltaSamplesDuration;
		const rms = mediaSource?.rmsAudioLevel;

		if (!mediaSource) return this._clear({
			comment: 'no audio measurement',
		});

		let silenceKind: SilenceKind;

		if (rms !== undefined) {
			// A level was measured, so samples did flow, whatever the sample clock went on to report.
			// An open finding needs the higher of the two thresholds to close; see
			// `recoveryRmsThreshold` for why one number could not do both jobs.
			const audibleThreshold = this._raised
				? this.config.recoveryRmsThreshold
				: this.config.silenceRmsThreshold;

			if (audibleThreshold < rms) return this._clear({
				comment: 'audio detected',
				silentAudioSource: false,
			});

			// Inside the dead band with a finding open: not silence, and not enough to call the
			// device working either, so whatever state exists is held and nothing accumulates.
			if (this.config.silenceRmsThreshold < rms) return;

			silenceKind = rms === 0 ? 'digital-silence' : 'below-threshold';
		} else if (capturedInSec === 0) {
			silenceKind = 'no-samples';
		} else {
			// No level, and no sample clock saying the source stopped: nothing to go on either way.
			return this._clear({
				comment: 'no audio measurement',
			});
		}

		// Stats time, not captured time: the claim is that nothing audible left this microphone for
		// this long, and an interval that produced no samples at all is the most silent kind there
		// is. `capturedForInMs` carries what was actually delivered, so the two can be compared.
		this._silentForInMs += mediaSource.deltaTime ?? 0;

		if (capturedInSec !== undefined) {
			this._capturedForInMs = (this._capturedForInMs ?? 0) + capturedInSec * 1000;
		}

		if (!this._raised && this._silentForInMs < this.config.silenceThresholdInMs) {
			// Quiet, and judged to be quiet — but not yet for long enough to call it a fault.
			this.trackMonitor.silentAudioSource = false;

			return;
		}

		const payload = {
			silenceKind,
			rmsAudioLevel: rms,
			silentForInMs: this._silentForInMs,
			capturedForInMs: this._capturedForInMs,
		};

		// Set on both paths below, so the verdict cannot drift from the finding while it is open.
		this.trackMonitor.silentAudioSource = true;

		if (this._raised) {
			this.trackMonitor.issues.update({
				key: this._issueKey,
				payload,
			});

			return;
		}

		this._raised = true;

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('silent-audio-source', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			silentForInMs: this._silentForInMs,
		});

		this.trackMonitor.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: ISSUE_TYPE,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: track.id,
				deviceLabel: track.label,
				...payload,
			},
			timestamp: Date.now(),
		});
	}

	private _clear(options: {
		comment: string,
		silentAudioSource?: false,
	}) {
		this.trackMonitor.silentAudioSource = options.silentAudioSource;

		this._silentForInMs = 0;
		this._capturedForInMs = undefined;

		if (!this._raised) return;

		this._raised = false;

		// No payload: the registry merges, and every tick the issue was open kept `silentForInMs`
		// and `capturedForInMs` current, so the resolution already carries the whole episode.
		this.trackMonitor.issues.resolve({
			key: this._issueKey,
			comment: options.comment,
			resolvedAt: Date.now(),
		});
	}
}

```
### SimulcastLayerDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/SimulcastLayerDetector.ts#L45)
Category: Telemetry
```ts
import { Detector } from "./Detector";
import { OutboundTrackMonitor } from "../monitors/OutboundTrackMonitor";
import { ClientEventTypes } from "../schema/ClientEventTypes";

/** A snapshot of every encoding on the track, materialized only on a change. */
export type SimulcastLayerState = {
	/** The RID, when the application uses one. Falls back to the SSRC. */
	rid: string;
	ssrc: number;
	encodingIndex?: number;
	/** Not the encoding's flag alone: the layer also has to have sent bytes in the interval. */
	active: boolean;
	bitrate?: number;
	frameWidth?: number;
	frameHeight?: number;
	framesPerSecond?: number;
	scalabilityMode?: string;
}

export type SimulcastLayerDetectorConfig = {
	/** Whether to buffer a `SIMULCAST_LAYER_CHANGED` client event into the sample. DEFAULT: true */
	createEvent?: boolean;
}

/**
 * Reports a change in which simulcast layers an outbound video track is actually sending. Layers
 * are meant to come and go, so this is an observation rather than a fault — but use it to answer
 * "why is this participant blurry" with a client-side record that the high layer stopped being
 * produced at all.
 *
 * A layer counts as active only when the encoding is not explicitly disabled *and* it sent bytes
 * in the interval; `active: true` with no bytes is what a layer the encoder quietly gave up on
 * looks like. Fewer than two encodings is not simulcast and is left alone, the first observation
 * only establishes a baseline, and a pause forgets the baseline rather than reporting the pause
 * and the resume as two changes.
 *
 * Raises no issue.
 * Monitor event: `simulcast-layer-changed`; client event `SIMULCAST_LAYER_CHANGED` when
 * `createEvent` is left on. Config: `simulcastLayerDetector`.
 *
 * Category: Telemetry
 * Layer: Media
 *
 */
export class SimulcastLayerDetector implements Detector {
	public readonly name = 'simulcast-layer-detector';
	public disabled = false;

	private _previousActiveKeys?: string;

	public constructor(
		public readonly trackMonitor: OutboundTrackMonitor,
	) {}

	private get config() {
		return this.peerConnection.parent.config.simulcastLayerDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) return;
		if (this.trackMonitor.kind !== 'video') return;

		// A track that ended sends nothing on every layer at once, which is the end of the track
		// rather than the layers being dropped. Forgotten rather than skipped, so the last live
		// set cannot read as a change against whatever comes after it.
		if (this.trackMonitor.readyState !== 'live') {
			this._previousActiveKeys = undefined;

			return;
		}
		if (this.trackMonitor.paused) {
			this._previousActiveKeys = undefined;

			return;
		}

		const outboundRtps = this.trackMonitor.getOutboundRtps();

		if (outboundRtps.length < 2) return;

		const activeRids: string[] = [];

		for (const outboundRtp of outboundRtps) {
			if (outboundRtp.active !== false && 0 < (outboundRtp.deltaBytesSent ?? 0)) {
				activeRids.push(outboundRtp.rid ?? `${outboundRtp.ssrc}`);
			}
		}

		const activeKeys = activeRids.sort().join(',');

		if (this._previousActiveKeys === undefined) {
			this._previousActiveKeys = activeKeys;

			return;
		}
		if (this._previousActiveKeys === activeKeys) return;

		const layers: SimulcastLayerState[] = outboundRtps.map((outboundRtp) => ({
			rid: outboundRtp.rid ?? `${outboundRtp.ssrc}`,
			ssrc: outboundRtp.ssrc,
			encodingIndex: outboundRtp.encodingIndex,
			active: outboundRtp.active !== false && 0 < (outboundRtp.deltaBytesSent ?? 0),
			bitrate: outboundRtp.bitrate,
			frameWidth: outboundRtp.frameWidth,
			frameHeight: outboundRtp.frameHeight,
			framesPerSecond: outboundRtp.framesPerSecond,
			scalabilityMode: outboundRtp.scalabilityMode,
		}));

		const from = this._previousActiveKeys;

		this._previousActiveKeys = activeKeys;

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('simulcast-layer-changed', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			activeLayerIds: activeKeys.length ? activeKeys.split(',') : [],
			previousActiveLayerIds: from.length ? from.split(',') : [],
			layers,
		});

		if (this.config.createEvent === false) return;

		clientMonitor.addEvent({
			type: ClientEventTypes.SIMULCAST_LAYER_CHANGED,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				// Schema payloads are flat records of primitives, hence the joined ids and the stringified snapshot.
				activeLayerIds: activeKeys,
				previousActiveLayerIds: from,
				layers: JSON.stringify(layers),
			},
		});
	}
}

```
### StatsGapDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/StatsGapDetector.ts#L34)
Category: Telemetry
```ts
import { Detector } from "./Detector";
import { ClientMonitor } from "../ClientMonitor";
import { ClientEventTypes } from "../schema/ClientEventTypes";

export type StatsGapDetectorConfig = {
	/** Multiple of `collectingPeriodInMs` the actual interval must exceed to count as a gap. */
	gapRatioThreshold: number;

	/** Absolute floor in ms, below which an overrun is treated as ordinary scheduling jitter. */
	minGapInMs: number;

	/** Whether to buffer a `STATS_COLLECTION_GAP` client event into the sample. DEFAULT: true */
	createEvent?: boolean;
}

/**
 * Reports that stats collection itself ran late — a backgrounded tab, a sleeping device, a
 * blocked main thread. Use it to discount the interval afterwards: every rate here is a delta
 * over an elapsed time, so the first tick after a gap attributes a large accumulation to a short
 * window and reads as a network event that never happened.
 *
 * An overrun must clear both a ratio of `collectingPeriodInMs` and an absolute floor. The first
 * collection has nothing to be late relative to, so it only establishes the baseline.
 *
 * This is an observation about the *measurement*, not about the call, so it raises no issue.
 *
 * Monitor event: `stats-collection-gap`; client event `STATS_COLLECTION_GAP` when
 * `createEvent` is left on. Config: `statsGapDetector`.
 *
 * Category: Telemetry
 * Layer: Lifecycle
 *
 */
export class StatsGapDetector implements Detector {
	public readonly name = 'stats-gap-detector';
	public disabled = false;

	private _previousCollectionStartedAt?: number;

	public constructor(
		public readonly clientMonitor: ClientMonitor,
	) {}

	private get config() {
		return this.clientMonitor.config.statsGapDetector!;
	}

	public update() {
		if (this.disabled) return;

		const startedAt = this.clientMonitor.lastCollectingStatsAt;

		if (!startedAt) return;

		const previous = this._previousCollectionStartedAt;

		this._previousCollectionStartedAt = startedAt;

		if (previous === undefined) return;

		const actualPeriodInMs = startedAt - previous;
		const expectedPeriodInMs = this.clientMonitor.config.collectingPeriodInMs;

		if (!expectedPeriodInMs || expectedPeriodInMs < 1) return;

		const overran = expectedPeriodInMs * this.config.gapRatioThreshold < actualPeriodInMs &&
			this.config.minGapInMs < actualPeriodInMs;

		if (!overran) return;

		this.clientMonitor.emit('stats-collection-gap', {
			clientMonitor: this.clientMonitor,
			expectedPeriodInMs,
			actualPeriodInMs,
			gapInMs: actualPeriodInMs - expectedPeriodInMs,
		});

		if (this.config.createEvent === false) return;

		this.clientMonitor.addEvent({
			type: ClientEventTypes.STATS_COLLECTION_GAP,
			payload: {
				expectedPeriodInMs,
				actualPeriodInMs,
				gapInMs: actualPeriodInMs - expectedPeriodInMs,
				durationOfCollectingStatsInMs: this.clientMonitor.durationOfCollectingStatsInMs,
			},
		});
	}
}

```
### StuckDecoderDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/StuckDecoderDetector.ts#L66)
Category: Pipeline Disruption
```ts
import { Detector } from "./Detector";
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";

export type StuckDecoderVariant = 'assembly' | 'decode' | 'unknown';

export type StuckDecoderIssuePayload = {
	peerConnectionId: string;
	trackId: string;
	ssrc?: number;
	/** Where the chain broke: no frame reassembles, or frames assemble but none decode. */
	variant: StuckDecoderVariant;
	stuckForInMs: number;
	/** RTP bytes received while nothing decoded. */
	deadBytesReceived: number;
	/** PLIs sent since the wedge began, not over the track's lifetime. */
	pliCountSinceStuck: number;
	frameWidth?: number;
	frameHeight?: number;
	decoderImplementation?: string;
	/** How long the issue stayed active; filled in on resolution. */
	durationInMs?: number;
}

export type StuckDecoderDetectorConfig = {
	/** Floor on the wait before raising, in ms. The effective wait is `max(thresholdInMs, rttMultiplier × RTT)`. */
	thresholdInMs: number;

	/** Multiple of current RTT the condition must outlast, so high-latency paths get longer to recover. */
	rttMultiplier: number;

	/** Receive bitrate (bps) above which the stream counts as still being delivered rather than starved. */
	minBitrate: number;

	/** PLIs that must have been sent during the stuck stretch. */
	minPliCount: number;
}

/**
 * Reports an inbound video track wedged: RTP keeps arriving but nothing decodes any more, and the
 * viewer sees a permanently frozen tile until the track is recreated. Use it to tell a wedge from a
 * starved track — bytes still flowing is exactly what separates the two, and it is what makes
 * recreating the track the right mitigation rather than a network fix.
 *
 * A finding means decodable state was lost and never recovered — a keyframe that never arrived, a
 * codec or resolution switch the decoder did not survive, or a browser decoder bug. It does not
 * self-heal, which is why the event exists as a hook for recreating the track.
 *
 * It waits `max(thresholdInMs, rttMultiplier × RTT)` with at least `minPliCount` PLIs sent, since a
 * wedge never self-heals and the wait only has to outlast a legitimate PLI to keyframe recovery.
 * Only RTP deltas are read, counted in the stream's own time so the interval matches the counters
 * reported with it. `variant` names whether frames failed to assemble or failed to decode.
 *
 * It refuses to judge a paused consumer, a paused sender or a backgrounded tab, where stopped
 * decoding with bytes flowing is expected.
 *
 * Issue raised: `stuck-decoder`, resolved when frames decode again or the detector
 * stands down.
 * Monitor event: `stuck-decoder` — the hook for the application-side mitigation.
 * Config: `stuckDecoderDetector`.
 * Track attribute: `InboundTrackMonitor.stuckedDecoder`.
 *
 * Category: Pipeline Disruption
 * Layer: Receive — frames to decoder
 *
 */
export class StuckDecoderDetector implements Detector {
	public static readonly ISSUE_TYPE = 'stuck-decoder';

	public readonly name = 'stuck-decoder-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly issueKey: string;

	/** Stats time accumulated over the current wedge; `0` outside one. */
	private _stuckForInMs = 0;
	private _deadBytes = 0;
	private _plisSinceStuck = 0;
	private _sawAssembledFrames = false;
	private _alertOn = false;
	private _startedAt?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this.issueKey = `${StuckDecoderDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private get config() {
		return this.peerConnection.parent.config.stuckDecoderDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) {
			this.trackMonitor.stuckedDecoder = undefined;

			return;
		}

		const inboundRtp = this.trackMonitor.getInboundRtp();

		if (!inboundRtp || inboundRtp.kind !== 'video') {
			this.trackMonitor.stuckedDecoder = undefined;

			return;
		}
		if (this.trackMonitor.readyState !== 'live') {
			this.trackMonitor.stuckedDecoder = undefined;

			return this._reset('track ended');
		}
		if (this.trackMonitor.paused) {
			this.trackMonitor.stuckedDecoder = undefined;

			return this._reset('consumer paused');
		}
		if (this.trackMonitor.remoteOutboundTrackPaused) {
			this.trackMonitor.stuckedDecoder = undefined;

			return this._reset('remote track paused');
		}
		if (!this.peerConnection.parent.activeTab) {
			this.trackMonitor.stuckedDecoder = undefined;

			return this._reset('tab in background');
		}

		const deltaBytes = inboundRtp.deltaBytesReceived ?? 0;
		const deltaFramesDecoded = inboundRtp.deltaFramesDecoded;

		// No counter is blind; frames coming out is the decoder demonstrably working.
		if (deltaFramesDecoded === undefined) {
			this.trackMonitor.stuckedDecoder = undefined;

			return this._reset('frames decoding');
		}

		if (0 < deltaFramesDecoded) {
			this.trackMonitor.stuckedDecoder = false;

			return this._reset('frames decoding');
		}

		// Nothing decoding, but nothing arriving either: a starved track, not a wedged one.
		if (inboundRtp.bitrate === undefined || inboundRtp.bitrate < this.config.minBitrate) {
			this.trackMonitor.stuckedDecoder = undefined;

			return inboundRtp.bitrate === undefined ? undefined : this._reset('rtp not flowing');
		}

		// Bytes arriving with nothing decoding, but not yet long enough to call it wedged.
		this.trackMonitor.stuckedDecoder = false;

		this._stuckForInMs += inboundRtp.deltaTime ?? 0;
		this._deadBytes += deltaBytes;
		this._plisSinceStuck += inboundRtp.deltaPliCount ?? 0;

		if (0 < (inboundRtp.deltaFramesReceived ?? 0)) {
			this._sawAssembledFrames = true;
		}

		if (this._alertOn) return;

		const stuckForInMs = this._stuckForInMs;

		// The wait scales with RTT: a legitimate PLI -> keyframe recovery costs a round trip.
		const rttInMs = (this.peerConnection.avgRttInSec ?? 0) * 1000;
		const requiredInMs = Math.max(this.config.thresholdInMs, this.config.rttMultiplier * rttInMs);

		if (stuckForInMs < requiredInMs) return;
		if (this._plisSinceStuck < this.config.minPliCount) return;

		this._alertOn = true;
		// Wall clock, and only for the resolved finding's `durationInMs`.
		this._startedAt = Date.now();
		// Set here, not at the call sites, so the flag and the finding cannot drift.
		this.trackMonitor.stuckedDecoder = true;

		const variant: StuckDecoderVariant = inboundRtp.deltaFramesReceived === undefined
			? 'unknown'
			: this._sawAssembledFrames ? 'decode' : 'assembly';

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('stuck-decoder', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			variant,
			stuckForInMs,
			deadBytesReceived: this._deadBytes,
			pliCountSinceStuck: this._plisSinceStuck,
		});

		this.trackMonitor.issues.raise({
				key: this.issueKey,
				includeInSample: this.includeIssueInSample,
			type: StuckDecoderDetector.ISSUE_TYPE,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				ssrc: inboundRtp.ssrc,
				variant,
				stuckForInMs,
				deadBytesReceived: this._deadBytes,
				pliCountSinceStuck: this._plisSinceStuck,
				frameWidth: inboundRtp.frameWidth,
				frameHeight: inboundRtp.frameHeight,
				decoderImplementation: inboundRtp.decoderImplementation,
			},
		});
	}

	private _reset(comment: string) {
		this._stuckForInMs = 0;
		this._deadBytes = 0;
		this._plisSinceStuck = 0;
		this._sawAssembledFrames = false;

		if (!this._alertOn) return;

		this._alertOn = false;

		const issue = this.trackMonitor.issues.get(this.issueKey);
		let payload: StuckDecoderIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as StuckDecoderIssuePayload),
				durationInMs: this._startedAt ? Date.now() - this._startedAt : undefined,
			};
		}

		this.trackMonitor.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedAt = undefined;
	}
}

```
### TransportDelayDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/TransportDelayDetector.ts#L70)
Category: Transport Quality
```ts
import { WindowSlice } from "../utils/SlicedWindow";
import type { PeerConnectionWindowValues } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";

/** Which round trip a reading came from: they span different paths and are never blended. */
export type TransportDelayRttSource = 'rtcp' | 'ice';

export type TransportDelayIssuePayload = {
	peerConnectionId: string;
	/** Mean round trip in milliseconds over the detection window, at the moment the issue was raised. */
	rttInMs: number;
	/**
	 * Which measurement `rttInMs` came from. `rtcp` is the media round trip, out to the far
	 * endpoint; `ice` is the connectivity-check round trip, which in an SFU topology reaches only
	 * the SFU. A reading that changes source mid-call is describing a different path, not a
	 * changed one.
	 */
	rttSource: TransportDelayRttSource;
	/** The stretch of stats time `rttInMs` is the mean over. */
	sustainedForInMs: number;
	durationInMs?: number;
}

export type TransportDelayDetectorConfig = {
	/** Mean round trip (ms) at or above which the path counts as slow. */
	thresholdInMs: number;

	/** Round trip (ms) below which the issue resolves. Keep it under `thresholdInMs` to stop flapping. */
	recoveryThresholdInMs: number;
}

/**
 * Reports a network path that works but takes too long — the round trip high enough, for long
 * enough, that conversation becomes turn-taking. Use it to tell a slow path (a long route, a relay
 * on the wrong continent) apart from a congested one: the congestion detectors answer "is the path
 * out of room", a different fault with a different fix. Both can be true at once, and none of them
 * reads the others.
 *
 * **It reads the mean round trip over `PeerConnectionMonitor.slicedWindow`**, which is
 * `totalRoundTripTime` divided by the number of measurements that produced it, across a span the
 * window states in milliseconds. That is deliberately not the EWMA this detector used to read: an
 * EWMA at a fixed smoothing factor has a memory set by how often stats are collected — roughly a
 * minute at a five-second period, under half that at two — so the same configuration meant
 * different things in different deployments. The window's span is the same everywhere, which is
 * also why the detector no longer counts a `durationInMs` of its own: the sustain *is* the
 * detection slice, and `peerConnectionWindow` is where its length now lives.
 *
 * **RTCP is preferred over ICE, per reading rather than once per call.** RTCP measures out to the
 * far endpoint and ICE only as far as the peer this connection talks to, so they answer different
 * questions and are never averaged together. The preference is re-decided from the window each
 * time: an RTCP total that stops advancing produces no reading at all and the detector falls back,
 * where reading a latched `rtcpRttInSec` would have kept thresholding a number that had stopped
 * moving while reporting that it could see. The source travels with the issue as `rttSource`.
 *
 * A finding clears when the *recovery* window — the stretch behind the detection window — also
 * reads below `recoveryThresholdInMs`, so a path has to have been good for both spans, not merely
 * for the most recent one.
 *
 * RTT to an SFU is a half-path measurement, so this is evidence about *this endpoint's* path and is
 * not end-to-end latency.
 *
 * Issue raised: `transport-delay-degraded`. Monitor event: `transport-delay-degraded`.
 * Config: `transportDelayDetector`.
 *
 * Category: Transport Quality
 * Layer: Delay
 *
 */
export class TransportDelayDetector implements Detector {
	public static readonly ISSUE_TYPE = 'transport-delay-degraded';
	public readonly name = 'transport-delay-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	private readonly issueKey: string;
	private _raised = false;
	private _startedAt?: number;

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
		this.issueKey = `${TransportDelayDetector.ISSUE_TYPE}-pc-${peerConnection.peerConnectionId}`;
	}

	private get config() {
		return this.peerConnection.parent.config.transportDelayDetector!;
	}

	public update() {
		if (this.disabled) return;

		const {
			detection: detectionWindow,
			recovery: recoveryWindow,
		} = this.peerConnection.slicedWindow.slices;

		// Not enough values yet is not a verdict either way, and it is not blindness: the window is
		// filling and will have an answer shortly. The span is checked alongside the count because
		// a window counts values, not time — ten collections carrying no stats time between them
		// fill it while measuring nothing, which is a frozen collector rather than a slow path.
		if (!detectionWindow.isReady || detectionWindow.durationInMs < 1) return;

		const detection = this._readRtt(detectionWindow);

		if (detection === undefined) {
			this.inputsUnavailable = true;

			// Nothing readable anywhere in the detection window — not one missed collection, since
			// the window spans several — so the detector can no longer support the claim it made.
			// An unsupportable claim must not stand for the rest of the call: same rule as the
			// recovery window below, that a detector able to raise is always able to clear.
			if (this._raised) this._resolve('round trip no longer measurable');

			return;
		}

		this.inputsUnavailable = false;

		if (this.config.thresholdInMs <= detection.rttInMs) {
			return this._raise(detection, detectionWindow.durationInMs);
		}

		if (!this._raised) return;

		// Below the raise threshold with a finding open: the recovery window is corroboration, not
		// a gate. A path has to have been good for the stretch behind this one as well *when that
		// stretch can be read* — but a window that cannot produce a reading must never be able to
		// hold a finding open for ever. A detector that can raise has to be able to clear, so with
		// nothing behind it to consult the detection reading decides on its own.
		const recovery = recoveryWindow.isReady
			? this._readRtt(recoveryWindow)
			: undefined;
		const clearing = recovery ?? detection;

		if (this.config.recoveryThresholdInMs <= clearing.rttInMs) return;

		this._resolve('round trip recovered');
	}

	/**
	 * The mean round trip across one window's deltas, or `undefined` when neither measurement
	 * moved far enough to produce one.
	 *
	 * A count delta of zero is the case that matters: the totals are still being reported, but no
	 * new measurement landed in this window, so dividing would resurrect the last mean instead of
	 * saying there is nothing new to read.
	 */
	private _readRtt(
		slice: WindowSlice<PeerConnectionWindowValues>,
	): { rttInMs: number, source: TransportDelayRttSource } | undefined {
		const mean = (
			timeInMs: number | null,
			count: number | null,
			source: TransportDelayRttSource,
		) => timeInMs !== null && count !== null && 0 < count
			? { rttInMs: timeInMs / count, source }
			: undefined;


		return mean(slice.deltaTotalRtcpRoundTripTimeInMs, slice.deltaTotalRtcpRoundTripMeasurements, 'rtcp')
			?? mean(slice.deltaTotalIceRoundTripTimeInMs, slice.deltaTotalIceResponsesReceived, 'ice');
	}

	private _raise(
		reading: { rttInMs: number, source: TransportDelayRttSource },
		windowInMs: number,
	) {
		const payload: TransportDelayIssuePayload = {
			peerConnectionId: this.peerConnection.peerConnectionId,
			rttInMs: reading.rttInMs,
			rttSource: reading.source,
			sustainedForInMs: windowInMs,
		};

		// Already open: refresh the measurement rather than raising a second time, so the payload
		// an operator reads is the current round trip and not the one that opened the episode.
		if (this._raised) {
			return void this.peerConnection.issues.update({
				key: this.issueKey,
				payload,
			});
		}

		this._raised = true;
		this._startedAt = Date.now();

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('transport-delay-degraded', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			rttInMs: reading.rttInMs,
		});

		this.peerConnection.issues.raise({
			key: this.issueKey,
			includeInSample: this.includeIssueInSample,
			type: TransportDelayDetector.ISSUE_TYPE,
			payload,
		});
	}

	private _resolve(comment: string) {
		this._raised = false;

		const issue = this.peerConnection.issues.get(this.issueKey);
		let payload: TransportDelayIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as TransportDelayIssuePayload),
				durationInMs: this._startedAt ? Date.now() - this._startedAt : undefined,
			};
		}

		this.peerConnection.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedAt = undefined;
	}
}

```
### TransportDemuxStalledDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/TransportDemuxStalledDetector.ts#L52)
Category: Pipeline Disruption
```ts
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

/** What the transport says arrived against how much of it reached an inbound RTP stream — zero, which is the finding. */
export type TransportDemuxStalledIssuePayload = {
	peerConnectionId: string;
	transportId: string;
	demuxedBytesDelta?: number;
	transportReceivingBitrate?: number;
	stalledForMs: number;
	durationInMs?: number;
};

type DemuxState = {
	/** Stats time the boundary has been broken for; `undefined` while it is not broken. */
	stalledForMs?: number;
	raisedAt?: number;
};

const ISSUE_TYPE = 'transport-demux-stalled';

export type TransportDemuxStalledDetectorConfig = {
	/** How long the broken boundary must persist before raising, in ms. */
	thresholdInMs: number;

	/** Receive bitrate (bps) above which arriving traffic counts as media — set well above RTCP plus STUN. */
	minTransportReceiveBitrateBps: number;
}

/**
 * Reports media arriving on an ICE transport that never reaches any inbound RTP stream — the
 * transport counters climb while every stream attributed to it stays at zero bytes. Use it to
 * explain a tile that never appears while the call otherwise looks healthy: an SSRC mismatch after
 * renegotiation, or a consumer created against a producer that is already gone.
 *
 * `minTransportReceiveBitrateBps` rules out RTCP and STUN explaining the arriving bytes, and a
 * transport with no inbound RTP attributed to it is not judged at all, since a send-only transport
 * has nothing to demux into by design. The stall clock is stats time, kept per transport id, and a
 * transport that disappears resolves its issue.
 *
 * Where the browser reports no transport receiving bitrate it sets `inputsUnavailable` rather than
 * reading as healthy — with no evidence bytes arrived, the boundary is never called broken.
 *
 * Issue raised: `transport-demux-stalled`. Monitor event: `transport-demux-stalled`.
 * Config: `transportDemuxStalledDetector`.
 * Connection attribute: `PeerConnectionMonitor.stalledTransportDemux`.
 *
 * Category: Pipeline Disruption
 * Layer: Receive — transport to RTP streams
 *
 */
export class TransportDemuxStalledDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'transport-demux-stalled-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	private readonly _states = new Map<string, DemuxState>();

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.transportDemuxStalledDetector!;
	}

	public update(): void {
		if (this.disabled) {
			this.peerConnection.stalledTransportDemux = undefined;

			return;
		}
		if (this.peerConnection.closed) {
			this.peerConnection.stalledTransportDemux = undefined;

			return;
		}

		const seenTransports = new Set<string>();
		// A transport with no inbound RTP has no demux expectation to violate, so it neither
		// proves nor disproves anything; the flag needs at least one that does.
		let anyJudged = false;
		// One unjudgeable transport makes this tick's silence unusable as evidence of health.
		let inputsUnavailable = false;

		for (const transport of this.peerConnection.iceTransports) {
			seenTransports.add(transport.id);

			const state = this._getState(transport.id);
			const inboundRtps = transport.getInboundRtps();
			const receivingBitrate = transport.receivingBitrate;
			let demuxedBytesDelta: number | undefined;

			for (const inboundRtp of inboundRtps) {
				if (inboundRtp.deltaBytesReceived === undefined) continue;
				demuxedBytesDelta = (demuxedBytesDelta ?? 0) + inboundRtp.deltaBytesReceived;
			}

			// Nothing demuxed and no word on whether anything arrived — unanswerable this tick.
			if (0 < inboundRtps.length && demuxedBytesDelta === 0 && receivingBitrate === undefined) {
				inputsUnavailable = true;
			}

			// No inbound RTP means no demux expectation to violate; the floor rules out RTCP and STUN.
			if (0 < inboundRtps.length && receivingBitrate !== undefined) anyJudged = true;

			const broken = 0 < inboundRtps.length
				&& demuxedBytesDelta === 0
				&& receivingBitrate !== undefined
				&& this.config.minTransportReceiveBitrateBps <= receivingBitrate;

			if (!broken) {
				this._clear(transport.id, 'inbound rtp is receiving again');
				continue;
			}

			if (state.stalledForMs === undefined) {
				state.stalledForMs = 0;
			} else {
				// Stats time: only observed intervals count towards the threshold.
				state.stalledForMs += transport.deltaTime ?? 0;
			}

			if (state.stalledForMs < this.config.thresholdInMs) continue;
			if (state.raisedAt !== undefined) continue;

			state.raisedAt = Date.now();

			const clientMonitor = this.peerConnection.parent;
			const payload: TransportDemuxStalledIssuePayload = {
				peerConnectionId: this.peerConnection.peerConnectionId,
				transportId: transport.id,
				demuxedBytesDelta,
				transportReceivingBitrate: receivingBitrate,
				stalledForMs: state.stalledForMs,
			};

			clientMonitor.emit('transport-demux-stalled', {
				clientMonitor,
				peerConnectionMonitor: this.peerConnection,
				...payload,
			});

			this.peerConnection.issues.raise({
				key: this._issueKey(transport.id),
				includeInSample: this.includeIssueInSample,
				type: ISSUE_TYPE,
				payload,
			});
		}

		this.inputsUnavailable = inputsUnavailable;

		for (const transportId of [ ...this._states.keys() ]) {
			if (seenTransports.has(transportId)) continue;

			this._clear(transportId, 'ice transport is gone');
			this._states.delete(transportId);
		}

		const anyStalled = [ ...this._states.values() ].some((state) => state.raisedAt !== undefined);

		this.peerConnection.stalledTransportDemux = anyStalled
			? true
			: anyJudged && !inputsUnavailable ? false : undefined;
	}

	private _getState(transportId: string): DemuxState {
		let state = this._states.get(transportId);

		if (!state) {
			state = {};
			this._states.set(transportId, state);
		}

		return state;
	}

	private _clear(transportId: string, comment: string) {
		const state = this._states.get(transportId);

		if (!state) return;

		state.stalledForMs = undefined;

		if (state.raisedAt === undefined) return;

		const key = this._issueKey(transportId);
		const issue = this.peerConnection.issues.get(key);

		if (issue) {
			this.peerConnection.issues.resolve({
				key: key,
				comment,
				payload: {
					...issue.payload,
					durationInMs: Date.now() - state.raisedAt,
				} as TransportDemuxStalledIssuePayload,
				resolvedAt: Date.now(),
			});
		}

		state.raisedAt = undefined;
	}

	private _issueKey(transportId: string) {
		return `${ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}-transport-${transportId}`;
	}
}

```
### TransportLossDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/TransportLossDetector.ts#L47)
Category: Transport Quality
```ts
import { Detector } from "./Detector";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";

export type TransportLossIssuePayload = {
	peerConnectionId: string;
	/** Mean interval loss fraction (`0..1`) at the moment the issue was raised. */
	fractionLost: number;
	/** Which direction the loss was measured in. */
	direction: 'inbound' | 'outbound';
	/** How long loss stayed above the threshold before raising, from stats timestamps. */
	sustainedForInMs: number;
	durationInMs?: number;
}

export type TransportLossDetectorConfig = {
	/** Mean interval loss fraction (`0..1`) at or above which loss counts as material. */
	threshold: number;

	/** Loss fraction below which the issue resolves. Keep it under `threshold`. */
	recoveryThreshold: number;

	/** How long (ms of stats time) loss must stay high before raising. */
	durationInMs: number;
}

/**
 * Reports a path that is persistently dropping a material share of what is sent over it: the path is
 * up and stable, and packets simply are not all arriving. Use it to tell loss apart from congestion —
 * a well-behaved congestion controller congests a path with almost no loss, and a lossy wireless link
 * loses packets with no congestion signal at all. Both can be true at once, decided independently.
 *
 * A finding points at the medium rather than at load: a weak or contended wireless link, a faulty
 * cable or port, or a middlebox dropping under pressure. Sustained loss with no congestion signal is
 * the signature of a path that is damaged rather than full.
 *
 * Both directions are watched with one threshold and the worse one is reported, its direction in the
 * payload. Streams that carried nothing this tick are excluded from the mean rather than counted as
 * healthy, so a call with eight muted tracks and one bleeding one does not look fine.
 *
 * Issue raised: `transport-loss-sustained`. Monitor event: `transport-loss-sustained`.
 * Config: `transportLossDetector`.
 *
 * Category: Transport Quality
 * Layer: Delivery reliability
 *
 */
export class TransportLossDetector implements Detector {
	public static readonly ISSUE_TYPE = 'transport-loss-sustained';
	public readonly name = 'transport-loss-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	private readonly issueKey: string;
	private _sustainedForInMs = 0;
	private _raised = false;
	private _startedAt?: number;

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
		this.issueKey = `${TransportLossDetector.ISSUE_TYPE}-pc-${peerConnection.peerConnectionId}`;
	}

	private get config() {
		return this.peerConnection.parent.config.transportLossDetector!;
	}

	public update() {
		if (this.disabled) return;

		const inbound = this.peerConnection.avgInboundFractionLost;
		const outbound = this.peerConnection.avgOutboundFractionLost;

		if (inbound === undefined && outbound === undefined) {
			this.inputsUnavailable = true;

			return;
		}

		this.inputsUnavailable = false;

		const direction: 'inbound' | 'outbound' = (outbound ?? -1) > (inbound ?? -1) ? 'outbound' : 'inbound';
		const fractionLost = Math.max(inbound ?? 0, outbound ?? 0);

		if (fractionLost < this.config.recoveryThreshold) {
			this._sustainedForInMs = 0;

			if (this._raised) this._resolve('loss recovered');

			return;
		}

		if (fractionLost < this.config.threshold) return;

		this._sustainedForInMs += this.peerConnection.deltaTime ?? 0;

		if (this._raised) return;
		if (this._sustainedForInMs < this.config.durationInMs) return;

		this._raised = true;
		this._startedAt = Date.now();

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('transport-loss-sustained', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			fractionLost,
			direction,
		});

		this.peerConnection.issues.raise({
			key: this.issueKey,
			includeInSample: this.includeIssueInSample,
			type: TransportLossDetector.ISSUE_TYPE,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				fractionLost,
				direction,
				sustainedForInMs: this._sustainedForInMs,
			},
		});
	}

	private _resolve(comment: string) {
		this._raised = false;

		const issue = this.peerConnection.issues.get(this.issueKey);
		let payload: TransportLossIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as TransportLossIssuePayload),
				durationInMs: this._startedAt ? Date.now() - this._startedAt : undefined,
			};
		}

		this.peerConnection.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedAt = undefined;
	}
}

```
### UnstableIcePathDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/UnstableIcePathDetector.ts#L60)
Category: Connectivity
```ts
import { IcePathKind } from "../monitors/IceCandidatePairMonitor";
import { IceTransportMonitor } from "../monitors/IceTransportMonitor";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { Detector } from "./Detector";

/** The path whose selection keeps moving, and how many switches were counted inside the window. */
export type UnstableIcePathIssuePayload = {
	peerConnectionId: string;
	pathKey: string;
	transportId?: string;
	switches: number;
	windowInMs: number;
	/** Absent when the transport had no selected candidate pair to classify at raise time. */
	kind?: IcePathKind;
	/** Switches per the browser's own counter, where it reports one. It also sees flaps too fast to diff. */
	nativePairChanges?: number;
	durationInMs?: number;
};

type TransportState = {
	/** The selected pair id as of the previous tick, for the portable diffing fallback. */
	selectedCandidatePairId?: string;
	/** Stats time accumulated in the current window; the window tumbles when it exceeds the config. */
	windowElapsedInMs: number;
	switchesInWindow: number;
	nativeChangesInWindow: number;
	raisedAt?: number;
};

const ISSUE_TYPE = 'unstable-ice-path';

export type UnstableIcePathDetectorConfig = {
	/** Tumbling window over which selected-path switches are counted, in stats time. */
	pathSwitchWindowInMs: number;

	/** Switches inside one window needed before the path counts as unstable. */
	pathSwitchThreshold: number;
}

/**
 * Reports an ICE transport whose selected path will not settle. Use it to tell path churn from a
 * path that is simply down: each reselection costs a fresh round of consent checks and a discarded
 * bandwidth estimate, so the call stutters while every state field reads `connected` throughout —
 * two live interfaces fighting, a NAT rewriting bindings, a TURN allocation being re-established.
 *
 * Switches are the larger of two counts. Diffing `selectedCandidatePairId` tick to tick is portable
 * but blind to a flap that departs and returns inside one collecting period; the browser's own
 * `deltaSelectedCandidatePairChanges` sees those but is not reported everywhere. The window tumbles
 * rather than slides, in stats time, so a late collection cannot shrink what it was measuring.
 *
 * It does not claim which path is better, or that the switching is the fault rather than a symptom.
 *
 * Issue raised: `unstable-ice-path`, resolved when a whole window passes below the threshold or when
 * the transport goes away. Config: `unstableIcePathDetector`.
 *
 * Category: Connectivity
 * Layer: 5 — Path continuity
 *
 */
export class UnstableIcePathDetector implements Detector {
	public static readonly ISSUE_TYPE = ISSUE_TYPE;

	public readonly name = 'unstable-ice-path-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _states = new Map<string, TransportState>();

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
	}

	private get config() {
		return this.peerConnection.parent.config.unstableIcePathDetector!;
	}

	public update(): void {
		if (this.disabled) return;
		if (this.peerConnection.closed) return;

		const seenIds = new Set<string>();

		for (const transport of this.peerConnection.iceTransports) {
			seenIds.add(transport.id);

			this._checkTransport(transport);
		}

		for (const transportId of [ ...this._states.keys() ]) {
			if (seenIds.has(transportId)) continue;

			this._resolve(transportId, 'ice transport is gone');
			this._states.delete(transportId);
		}
	}

	private _checkTransport(transport: IceTransportMonitor) {
		const { pathSwitchWindowInMs, pathSwitchThreshold } = this.config;
		const state = this._getState(transport);
		const observedSwitch = state.selectedCandidatePairId !== undefined
			&& state.selectedCandidatePairId !== transport.selectedCandidatePairId;
		const nativeChanges = transport.deltaSelectedCandidatePairChanges ?? 0;

		state.selectedCandidatePairId = transport.selectedCandidatePairId;
		state.windowElapsedInMs += transport.deltaTime ?? 0;
		state.switchesInWindow += Math.max(observedSwitch ? 1 : 0, nativeChanges);
		state.nativeChangesInWindow += nativeChanges;

		if (pathSwitchThreshold <= state.switchesInWindow && state.raisedAt === undefined) {
			const pair = transport.getSelectedCandidatePair();

			state.raisedAt = Date.now();

			this.peerConnection.issues.raise({
					key: this._issueKey(transport.id),
					includeInSample: this.includeIssueInSample,
					type: ISSUE_TYPE,
					payload: {
						peerConnectionId: this.peerConnection.peerConnectionId,
						pathKey: pair?.pathKey ?? transport.id,
						transportId: transport.id,
						switches: state.switchesInWindow,
						windowInMs: pathSwitchWindowInMs,
						kind: pair?.pathKind,
						nativePairChanges: 0 < state.nativeChangesInWindow ? state.nativeChangesInWindow : undefined,
					},
				}
			);
		}

		if (state.windowElapsedInMs < pathSwitchWindowInMs) return;

		// A standing issue survives only if the window just closing still justified it.
		if (state.switchesInWindow < pathSwitchThreshold) {
			this._resolve(transport.id, 'ice path became stable');
		}

		state.windowElapsedInMs = 0;
		state.switchesInWindow = 0;
		state.nativeChangesInWindow = 0;
	}

	private _getState(transport: IceTransportMonitor): TransportState {
		let state = this._states.get(transport.id);

		if (!state) {
			state = {
				selectedCandidatePairId: transport.selectedCandidatePairId,
				windowElapsedInMs: 0,
				switchesInWindow: 0,
				nativeChangesInWindow: 0,
			};
			this._states.set(transport.id, state);
		}

		return state;
	}

	private _resolve(transportId: string, comment: string) {
		const state = this._states.get(transportId);

		if (state?.raisedAt === undefined) return;

		const raisedAt = state.raisedAt;

		state.raisedAt = undefined;

		const key = this._issueKey(transportId);
		const issue = this.peerConnection.issues.get(key);

		if (!issue) return;

		this.peerConnection.issues.resolve({
			key: key,
			comment,
			payload: {
				...(issue.payload as UnstableIcePathIssuePayload),
				durationInMs: Date.now() - raisedAt,
			},
			resolvedAt: Date.now(),
		});
	}

	private _issueKey(transportId: string) {
		return `${ISSUE_TYPE}-pc-${this.peerConnection.peerConnectionId}-transport-${transportId}`;
	}
}

```
### UplinkCongestionDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/UplinkCongestionDetector.ts#L95)
Category: Transport Quality
```ts
import { Detector } from "./Detector";
import { PeerConnectionMonitor } from "../monitors/PeerConnectionMonitor";
import { DecayingMaxEstimator } from "../utils/DecayingMaxEstimator";
import { FrugalQuantileEstimator } from "../utils/FrugalQuantileEstimator";

/** Noise floor: a 0.2ms queue doubling to 0.4ms is arithmetic, not congestion. */
const MIN_PACKET_SEND_DELAY_IN_MS = 1;

/** Half-life of the recent-maximum memory, ~3 minutes. Per second, not per collection. */
const AVAILABLE_BITRATE_DECAY_PER_SECOND = 0.996;

/**
 * How much the maximum's decay is multiplied by while an episode is still recent: this the
 * moment the episode closes, easing back to 1 across the window below. A path rarely gives
 * back all of what an episode took, and without it a second dip arriving inside that window
 * is scored against a capacity the path no longer reaches.
 */
const POST_EPISODE_DECAY_BOOST = 0.85;
const POST_EPISODE_FADE_WINDOW_IN_MS = 30_000;


export type UplinkCongestionIssuePayload = {
	peerConnectionId: string;

	/**
	 * The two witnesses, each a fraction in `0..1` where `0` is healthy. `undershoot`
	 * of 0.75 means the path is carrying a quarter of what it recently did;
	 * `pacerBloating` of 1 means the pacer is at least four times its usual depth.
	 */
	undershoot: number;
	pacerBloating: number;

	/** How deep the trouble is, `0..1` — the geometric mean of the two witnesses. */
	severity: number;

	/** The measurements the ratios were taken from, in their own units. */
	availableOutgoingBitrate: number;
	recentMaxAvailableBitrate: number;
	sendingBitrate: number;
	avgPacketSendDelayInMs: number;
	estimatedMedianPacketSendDelayInMs: number;

	/** Filled in when the finding closes. */
	durationInMs?: number;
}

export type UplinkCongestionDetectorConfig = {
	/** How deep the trouble has to be before reporting it, `0..1`. */
	minSeverity: number;

	/**
	 * Where `pacerBloating` reaches the top of its scale, as a multiple of the connection's own
	 * median pacer delay. The library default is `4`: a pacer sitting at four times its usual
	 * depth scores `1`, and one at twice the median scores a third of the way up.
	 *
	 * Raise it to make the witness harder to satisfy on a connection whose pacer is naturally
	 * spiky; lower it to make a mild bloat count for more. Values at or below `1` make any
	 * excess over the median score `1` outright.
	 */
	pacerBloatingSaturatesAt: number;
}

/**
 * Reports this endpoint's **sending** path running out of room — the cause behind collapsing
 * outgoing resolution and the far end saying you are breaking up. Use it to tell "this user's
 * upload is the problem" apart from a decoder, a camera or the far end's own link.
 *
 * A finding means the path itself ran short, not the endpoints: an uplink shared with something
 * else, a wireless link that degraded, a shaper or a cellular cell that narrowed. It is about this
 * user's own upload, so it explains why *everyone else* sees them badly while their own preview
 * looks perfect.
 *
 * The browser reporting the encoder bandwidth limited decides *whether* this is congestion.
 * Two witnesses decide how deep it is, each a fraction of this connection's own normal:
 *
 * - `undershoot` — how far the bandwidth estimate has fallen below the highest it recently
 *   reached.
 * - `pacerBloating` — how far pacer time per packet sits above its own running median, with
 *   `pacerBloatingSaturatesAt` times the median as the top of the scale, `4` by default.
 *
 * Their geometric mean rides on the finding as `severity` in `0..1`, opening at `minSeverity`.
 * Being a geometric mean, a witness at its healthy level takes the severity to zero: a narrowing
 * path with the pacer empty is an encoder asked for less, and a filling pacer on an unchanged path
 * is a hiccup. Where the browser reports no estimate or no verdict it sets `inputsUnavailable`
 * rather than reading as healthy.
 *
 * Issue raised: `uplink-congestion`. Monitor events: `uplink-congestion`, and `congestion` with
 * `direction: 'uplink'`. Connection attribute: `PeerConnectionMonitor.uplinkCongested`.
 * Config: `uplinkCongestionDetector`.
 *
 * Category: Transport Quality
 * Layer: Capacity
 *
 */
export class UplinkCongestionDetector implements Detector {
	public static readonly ISSUE_TYPE = 'uplink-congestion';
	public readonly name = 'uplink-congestion-detector';
	public disabled = false;
	public includeIssueInSample = true;
	public inputsUnavailable = false;

	/**
	 * The two baselines each witness is measured against — how they are fed is at the call
	 * site in `update()`.
	 */
	public readonly recentMaxAvailableBitrateEstimator = new DecayingMaxEstimator(AVAILABLE_BITRATE_DECAY_PER_SECOND);
	public readonly medianPacketSendDelayEstimator = new FrugalQuantileEstimator(0.5);

	private readonly _issueKey: string;
	private _raised = false;

	/** When the last episode closed, while the faster fade that follows it is still running. */
	private _boostedDecayAt?: number;


	/** Wall clock, and only for the resolved finding's `durationInMs`. */
	private _raisedAt?: number;

	public constructor(
		public readonly peerConnection: PeerConnectionMonitor,
	) {
		this._issueKey = `${UplinkCongestionDetector.ISSUE_TYPE}-pc-${peerConnection.peerConnectionId}`;
	}

	private get config() {
		return this.peerConnection.parent.config.uplinkCongestionDetector!;
	}

	public update() {
		if (this.disabled) return;

		const sendingBitrate = this.peerConnection.sendingBitrate;

		// No sending path to judge — a receive-only connection lives here permanently.
		if (sendingBitrate <= 0) {
			return this._standDown('nothing is being sent over this connection');
		}

		const availableOutgoingBitrate = this.peerConnection.totalAvailableOutgoingBitrate;
		const avgPacketSendDelayInMs = this.peerConnection.avgPacketSendDelayInMs;
		const qualityLimitationReason = this.peerConnection.qualityLimitationReason;

		// No estimate or no verdict. Blind, not healthy.
		if (
			availableOutgoingBitrate === undefined ||
			avgPacketSendDelayInMs === undefined ||
			qualityLimitationReason === undefined
		) {
			this.inputsUnavailable = true;
			this.peerConnection.uplinkVideoCongestionSeverity = undefined;

			return;
		}

		this.inputsUnavailable = false;

		const recentMaxAvailableBitrate = this.recentMaxAvailableBitrateEstimator.estimate;
		const estimatedMedianPacketSendDelayInMs = this.medianPacketSendDelayEstimator.estimate;

		this._easePostEpisodeDecay();

		// Fed after the reads above, so a collection cannot move the baseline it is judged
		// against. The maximum takes every collection, an open episode included: a congested
		// sample is lower so it cannot inflate it, and feeding it is the only way it fades.
		this.recentMaxAvailableBitrateEstimator.update(availableOutgoingBitrate, this.peerConnection.deltaTime ?? 0);

		// The median takes only collections with no finding open, or a sustained bloat would
		// drag it up and talk the episode out of existence.
		if (!this._raised) this.medianPacketSendDelayEstimator.update(avgPacketSendDelayInMs);

		// The verdict decides whether this is congestion; the witnesses below decide how deep.
		// It is also the only thing that closes an open finding.
		if (qualityLimitationReason !== 'bandwidth') {
			return this._standDown('the browser no longer reports the encoder as bandwidth limited');
		}

		// One observation is enough for both baselines: the maximum starts as that sample and
		// the quantile as its own estimate, so a witness reads 0 rather than wrong.
		if (
			recentMaxAvailableBitrate === undefined ||
			estimatedMedianPacketSendDelayInMs === undefined ||
			recentMaxAvailableBitrate <= 0 ||
			availableOutgoingBitrate <= 0
		) {
			return this._standDown('not enough history to judge congestion');
		}

		// Checked rather than defaulted: an absent scale makes the bloating `NaN`, and every
		// comparison below reads false against `NaN` — the finding would raise on everything.
		if (this.config.pacerBloatingSaturatesAt === undefined) return;

		// Clamped: a rising estimate can overtake a maximum seeded from lower samples.
		const undershoot = Math.max(0, 1 - (availableOutgoingBitrate / recentMaxAvailableBitrate));
		const pacerBaselineInMs = Math.max(estimatedMedianPacketSendDelayInMs, MIN_PACKET_SEND_DELAY_IN_MS);
		// Never zero, so a `saturatesAt` of 1 or less saturates on any excess instead of dividing by it.
		const pacerBloatingSpan = Math.max(this.config.pacerBloatingSaturatesAt - 1, Number.EPSILON);
		const pacerBloating = Math.min(1, Math.max(0,
			(avgPacketSendDelayInMs - pacerBaselineInMs) / (pacerBaselineInMs * pacerBloatingSpan),
		));

		// Geometric mean: a witness at its healthy level takes the whole thing to zero.
		const severity = Math.sqrt(undershoot * pacerBloating);

		// Kept current on every judged collection, an open episode included, so an application
		// reading it sees the trouble deepening rather than the value that opened the finding.
		this.peerConnection.uplinkVideoCongestionSeverity = severity;

		// An open finding is not raised again; it closes on the verdict above.
		if (this._raised) return;

		// Checked rather than compared against: `severity < undefined` is false, so a bare
		// comparison would raise on every collection where the config arrived without it.
		if (this.config.minSeverity === undefined) return;
		if (severity < this.config.minSeverity) return;

		this._raise({
			peerConnectionId: this.peerConnection.peerConnectionId,
			undershoot,
			pacerBloating,
			severity,
			availableOutgoingBitrate,
			recentMaxAvailableBitrate,
			sendingBitrate,
			avgPacketSendDelayInMs,
			estimatedMedianPacketSendDelayInMs,
		});
	}

	/**
	 * Moves the maximum's decay along the post-episode window: fastest the moment the episode
	 * closed, easing back to the ordinary rate across the window, and back to it outright once
	 * past. Does nothing when no episode is recent.
	 */
	private _easePostEpisodeDecay() {
		if (this._boostedDecayAt === undefined) return;

		const sinceResolveInMs = this.peerConnection.statsClockTime - this._boostedDecayAt;

		if (POST_EPISODE_FADE_WINDOW_IN_MS <= sinceResolveInMs) {
			this._boostedDecayAt = undefined;

			return this.recentMaxAvailableBitrateEstimator.updateDecayRate(AVAILABLE_BITRATE_DECAY_PER_SECOND);
		}

		const fadedBack = sinceResolveInMs / POST_EPISODE_FADE_WINDOW_IN_MS;
		const boost = POST_EPISODE_DECAY_BOOST + ((1 - POST_EPISODE_DECAY_BOOST) * fadedBack);

		this.recentMaxAvailableBitrateEstimator.updateDecayRate(AVAILABLE_BITRATE_DECAY_PER_SECOND * boost);
	}

	private _raise(payload: UplinkCongestionIssuePayload) {
		this._raised = true;
		this._raisedAt = Date.now();
		// Set here, not at the call sites, so the flag and the finding cannot drift.
		this.peerConnection.uplinkCongested = true;

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('uplink-congestion', {
			clientMonitor,
			peerConnectionMonitor: this.peerConnection,
			...payload,
		});

		// The same finding again on the direction-agnostic feed. One issue, two deliveries.

		this.peerConnection.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: UplinkCongestionDetector.ISSUE_TYPE,
			payload,
		});
	}

	/** Closes any open finding. Guarded, because this is every receive-only connection's resting state. */
	private _standDown(comment: string) {
		this.inputsUnavailable = false;
		this.peerConnection.uplinkVideoCongestionSeverity = undefined;

		if (this._raised) this._resolve(comment);
	}

	private _resolve(comment: string) {
		this._raised = false;
		this._boostedDecayAt = this.peerConnection.statsClockTime;
		this.peerConnection.uplinkCongested = false;

		const issue = this.peerConnection.issues.get(this._issueKey);

		this.peerConnection.issues.resolve({
			key: this._issueKey,
			comment,
			payload: issue
				? {
					...(issue.payload as UplinkCongestionIssuePayload),
					durationInMs: this._raisedAt === undefined ? undefined : Date.now() - this._raisedAt,
				}
				: undefined,
			resolvedAt: Date.now(),
		});

		this._raisedAt = undefined;
	}
}

```
### VideoCaptureBottleneckDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/VideoCaptureBottleneckDetector.ts#L97)
Category: Pipeline Disruption
```ts
import { Detector } from "./Detector";
import type { OutboundTrackMonitor } from "../monitors/OutboundTrackMonitor";

/**
 * What the detector measured about the capture device in the window that raised the issue.
 *
 * Every field not marked optional is always present: the detector cannot reach the raise without
 * it. The track's own `readyState` and `muted` are not carried, because the detector only raises
 * on a track that is live, unmuted and enabled, so they could only ever read `'live'` and `false`.
 */
export type VideoCaptureBottleneckIssuePayload = {
	peerConnectionId: string;
	trackId: string;

	/** The frames per second the track was configured to capture, from `getSettings().frameRate`. */
	expectedFps: number;

	/** The average frames per second the media source produced over the detection window. */
	producedFpsForDetection: number;

	/** The number of frames the media source produced over the detection window. */
	producedFramesForDetection: number;

	/** The milliseconds of stats time the detection window spanned. */
	detectionWindowInMs: number;

	/**
	 * The share of the configured frame rate the camera failed to deliver,
	 * `1 - producedFpsForDetection / expectedFps`. Zero is a camera meeting its rate and one is a
	 * camera delivering nothing; a camera exceeding its rate reports a negative.
	 */
	produceDegradation: number;

	/** The frame width and height the track was configured for, from `getSettings()`. */
	trackSettingsHeight?: number;
	trackSettingsWidth?: number;

	// Written at resolution, from the recovery window that ended the issue. Absent when it was
	// resolved by a stand-down instead, where nothing was measured.

	/** The milliseconds of stats time the recovery window spanned. */
	recoveryWindowInMs?: number;

	/** The average frames per second the media source produced over the recovery window. */
	producedFpsForRecovery?: number;

	/** The number of frames the media source produced over the recovery window. */
	producedFramesForRecovery?: number;
}

export type VideoCaptureBottleneckIssueType = 'video-capture-bottleneck';

export type VideoCaptureBottleneckDetectorConfig = {
	/**
	 * The share of the configured frame rate the camera may fall short by before the issue is
	 * raised, and must return to before it resolves.
	 */
	produceDegradationThreshold: number;
}


/**
 * Reports a camera failing to deliver the frames the track was configured to capture, while the
 * track reports itself `live` and unmuted throughout — a struggling driver, another application
 * contending for the device, thermal throttling. Use it to place a stuttery outgoing picture at the
 * capture stage rather than at the encoder (`EncoderBottleneckDetector`) or on the network.
 *
 * The frames the media source produced are summed by `OutboundTrackMonitor.slicedWindow`
 * over two windows, and this compares each average against `getSettings().frameRate`. The detection
 * window raises: falling short by more than `produceDegradationThreshold` of the configured rate
 * opens the issue, and every later collection still short of it updates the issue rather than
 * opening another. The recovery window resolves: the issue ends only once the stretch *before* the
 * detection window is back within the threshold, so a camera hovering at the line cannot flap one
 * long fault into a stream of short ones. Neither window is read before it says it is ready.
 *
 * Averaging over a window rather than judging each collection is what catches a camera whose
 * starving stretches are interleaved with healthy ones, and it weighs how far the source fell short
 * rather than only how often.
 *
 * A finding means the fault is upstream of the encoder and the network: nothing downstream can
 * recover frames the camera never produced.
 *
 * It stands down — reporting `undefined` rather than a verdict — for a backgrounded tab, a paused
 * sender, a track that is not live, unmuted and enabled, a screen share, a capture format that just
 * changed, a track with no configured frame rate, and a window holding no measured frames.
 *
 * Issue raised: `video-capture-bottleneck`, updated while it stays open, resolved on recovery or on
 * a stand-down. No monitor event.
 * Config: `videoCaptureBottleneckDetector`.
 * Track attribute: `OutboundTrackMonitor.degradedVideoCapture`.
 *
 * Category: Pipeline Disruption
 * Layer: Send — capture to frame supply
 *
 */

export class VideoCaptureBottleneckDetector implements Detector {
	public static readonly ISSUE_TYPE: VideoCaptureBottleneckIssueType = 'video-capture-bottleneck';

	public readonly name = 'video-capture-bottleneck-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly _issueKey: string;
	private _raised = false;

	public constructor(
		public readonly trackMonitor: OutboundTrackMonitor,
	) {
		this._issueKey = `${VideoCaptureBottleneckDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;

		if (this.config.produceDegradationThreshold < 0) {
			this.trackMonitor.getPeerConnection().parent.logger.warn(
				'videoCaptureBottleneckDetector.produceDegradationThreshold must not be below 0, got '+ this.config.produceDegradationThreshold
			);
			this.config.produceDegradationThreshold = 0;
		}
	}

	private get config(): VideoCaptureBottleneckDetectorConfig {
		return this.peerConnection.parent.config.videoCaptureBottleneckDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) {
			this.trackMonitor.degradedVideoCapture = undefined;

			return;
		}
		const track = this.trackMonitor.track;

		if (!this.peerConnection.parent.activeTab) return this._clear({
			comment: 'tab in background',
		});
		if (this.trackMonitor.paused) return this._clear({
			comment: 'track paused'
		});
		if (track.readyState !== 'live' || track.muted || !track.enabled) return this._clear({
			comment: 'track not sending',
		});
		if (this.trackMonitor.isScreenShare) return this._clear({
			comment: 'screen share',
		});

		// The track monitor read the settings once for every detector on this track and already
		// said whether the capture format moved, so this only has to act on the answer.
		if (this.trackMonitor.videoCaptureSettingsChanged) return this._clear({
			comment: 'capture settings changed',
		});

		const {
			detection: detectionWindow,
			recovery: recoveryWindow,
		} = this.trackMonitor.slicedWindow.slices;
		const trackSettings = this.trackMonitor.settings;
		const expectedFps = trackSettings?.frameRate;
		const producedFramesForDetection = detectionWindow.deltaMediaSourceTotalProducedFrames;
		const detectionWindowInMs = detectionWindow.durationInMs;

		if (expectedFps === undefined) return this._clear({
			comment: 'no configured frame rate',
		});
		if (producedFramesForDetection === null) return this._clear({
			comment: 'no source frames in window',
		});
		if (!detectionWindow.isReady || detectionWindowInMs < 1) return;

		const producedFpsForDetection = producedFramesForDetection / (detectionWindowInMs / 1000);
		const produceDegradation = 1 - (producedFpsForDetection / expectedFps);

		this.trackMonitor.videoCaptureDegradation = produceDegradation;

		if (this.config.produceDegradationThreshold < produceDegradation) {
			if (!this._raised) return this._raiseIssue({
					peerConnectionId: this.peerConnection.peerConnectionId,
					trackId: track.id,
					expectedFps,
					produceDegradation,
					producedFpsForDetection,
					producedFramesForDetection,
					detectionWindowInMs,
					trackSettingsHeight: trackSettings?.height,
					trackSettingsWidth: trackSettings?.width,
				});

			return;
		}

		// Below the threshold with nothing open: the camera was judged and found fine, which is not
		// the same as not having been judged at all.
		if (!this._raised) return this._clear({
			comment: 'capture within tolerance',
			degradedVideoCapture: false,
		});

		// Below the threshold with a finding open: the recovery window decides whether it ends.

		if (
			!recoveryWindow.isReady ||
			recoveryWindow.deltaMediaSourceTotalProducedFrames === null ||
			recoveryWindow.durationInMs < 1
		)
		{
				return;
		}

		const recoveryWindowInMs = recoveryWindow.durationInMs;
		const producedFramesForRecovery = recoveryWindow.deltaMediaSourceTotalProducedFrames;
		const producedFpsForRecovery = producedFramesForRecovery / (recoveryWindowInMs / 1000);
		const recoveryDegradation = 1 - (producedFpsForRecovery / expectedFps);

		if (this.config.produceDegradationThreshold < recoveryDegradation) {
			return;
		}

		this._clear({
			comment: 'capture recovered',
			payload: {
				producedFpsForRecovery,
				producedFramesForRecovery,
				recoveryWindowInMs,
			},
			degradedVideoCapture: false,
		});
	}


	private _raiseIssue(payload: VideoCaptureBottleneckIssuePayload) {
		if (this._raised) return;

		this._raised = true;
		this.trackMonitor.degradedVideoCapture = true;

		this.trackMonitor.issues.raise({
			key: this._issueKey,
			includeInSample: this.includeIssueInSample,
			type: VideoCaptureBottleneckDetector.ISSUE_TYPE,
			payload,
			timestamp: Date.now(),
		});
	}

	private _clear(options: {
		comment: string,
		payload?: Pick<VideoCaptureBottleneckIssuePayload, 'producedFpsForRecovery' | 'producedFramesForRecovery' | 'recoveryWindowInMs'>,
		degradedVideoCapture?: false
	}) {
		this.trackMonitor.degradedVideoCapture = options.degradedVideoCapture;
		// Blanked only on a stand-down, where nothing was measured. A verdict of `false` was measured
		// — a camera 0.15 short is judged fine and still 0.15 short — and flattening it to 0 would
		// leave the score calculator nothing to read below the threshold, which is the whole point
		// of carrying a continuous value beside the flag.
		if (options.degradedVideoCapture !== false) this.trackMonitor.videoCaptureDegradation = undefined;

		if (!this._raised) return;

		this._raised = false;

		this.trackMonitor.issues.resolve({
			key: this._issueKey,
			comment: options.comment,
			payload: options.payload,
			resolvedAt: Date.now(),
		});
	}
}

```
### VideoRecoveryFailedDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/VideoRecoveryFailedDetector.ts#L44)
Category: Pipeline Disruption
```ts
import { Detector } from "./Detector";
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";

export type VideoRecoveryFailedIssuePayload = {
	peerConnectionId: string;
	trackId: string;
	/** Keyframe requests sent since the current unrecovered stretch began. */
	pliCountSinceStalled: number;
	/** How long the picture has been stuck with `keyFramesDecoded` not advancing. */
	stalledForInMs: number;
	freezeCount?: number;
	/** Filled in when the finding closes. */
	durationInMs?: number;
}

export type VideoRecoveryFailedDetectorConfig = {
	/** How long the stall must last before the issue is raised. */
	recoveryFailedThresholdInMs: number;

	/** PLIs that must have been sent during the stall — evidence that repair was asked for. */
	recoveryFailedMinPliCount: number;
}

/**
 * Reports a frozen inbound video where keyframes were requested repeatedly and none arrived. Use it
 * to tell a broken repair loop apart from an ordinary freeze: `video-flow-disrupted` says a viewer
 * is looking at a still picture, this says the mechanism that exists to end it is not working —
 * a different fault with a different owner, somewhere past the first hop.
 *
 * The stall is derived from the raw counters rather than another detector's verdict: frames not
 * rendering *and* `deltaKeyFramesDecoded === 0`. The clock only starts once a PLI has actually gone
 * out, and both the stall duration and the PLI count must clear their thresholds, so the claim
 * always has both halves of its evidence. Time accumulates from each tick's `deltaTime`, so a
 * throttled tab cannot age a stall into an issue.
 *
 * Issue raised: `video-recovery-failed`. Monitor event: `video-recovery-failed`.
 * Config: `videoRecoveryFailedDetector`.
 * Track attribute: `InboundTrackMonitor.failedVideoRecovery`.
 *
 * Category: Pipeline Disruption
 * Layer: Beside the receive chain — the repair loop
 *
 */
export class VideoRecoveryFailedDetector implements Detector {
	public static readonly ISSUE_TYPE = 'video-recovery-failed';

	public readonly name = 'video-recovery-failed-detector';
	public disabled = false;
	public includeIssueInSample = true;

	private readonly issueKey: string;

	private _stalled = false;
	private _stalledForInMs = 0;
	private _pliCountSinceStalled = 0;
	private _startedAt?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor,
	) {
		this.issueKey = `${VideoRecoveryFailedDetector.ISSUE_TYPE}-track-${trackMonitor.track.id}`;
	}

	private get config() {
		return this.peerConnection.parent.config.videoRecoveryFailedDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) {
			this.trackMonitor.failedVideoRecovery = undefined;

			return;
		}

		const inboundRtp = this.trackMonitor.getInboundRtp();

		if (!inboundRtp ||
			this.trackMonitor.readyState !== 'live' ||
			!this.peerConnection.parent.activeTab ||
			this.trackMonitor.paused ||
			this.trackMonitor.remoteOutboundTrackPaused
		) {
			this.trackMonitor.failedVideoRecovery = undefined;

			return;
		}

		const deltaPli = inboundRtp.deltaPliCount ?? 0;
		const deltaKeyFrames = inboundRtp.deltaKeyFramesDecoded ?? 0;
		// Raw counters, never `frameFlowState`: no picture reaching the renderer and no keyframe to make one.
		const stalled = inboundRtp.deltaFramesRendered === 0 && deltaKeyFrames === 0;

		if (!stalled) {
			this.trackMonitor.failedVideoRecovery = false;
			this._stalled = false;
			this._stalledForInMs = 0;
			this._pliCountSinceStalled = 0;

			if (this._startedAt !== undefined) this._resolve('video recovered');

			return;
		}

		// Stalled, but recovery has not yet had long enough to be called failed.
		this.trackMonitor.failedVideoRecovery = false;

		// The clock only starts once a keyframe has actually been asked for.
		if (deltaPli < 1 && !this._stalled) return;

		if (this._stalled) {
			// Stats time, not wall-clock: a throttled tab must not age a stall into an issue.
			this._stalledForInMs += inboundRtp.deltaTime ?? 0;
		} else {
			this._stalled = true;
			this._stalledForInMs = 0;
		}

		this._pliCountSinceStalled += deltaPli;

		if (this._startedAt !== undefined) return;
		if (this._stalledForInMs < this.config.recoveryFailedThresholdInMs) return;
		if (this._pliCountSinceStalled < this.config.recoveryFailedMinPliCount) return;

		this._startedAt = Date.now();
		// Set here, not at the call sites, so the flag and the finding cannot drift.
		this.trackMonitor.failedVideoRecovery = true;

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('video-recovery-failed', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			pliCountSinceStalled: this._pliCountSinceStalled,
			stalledForInMs: this._stalledForInMs,
		});

		this.trackMonitor.issues.raise({
			key: this.issueKey,
			includeInSample: this.includeIssueInSample,
			type: VideoRecoveryFailedDetector.ISSUE_TYPE,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				pliCountSinceStalled: this._pliCountSinceStalled,
				stalledForInMs: this._stalledForInMs,
				freezeCount: inboundRtp.freezeCount,
			},
		});
	}

	private _resolve(comment: string) {
		const issue = this.trackMonitor.issues.get(this.issueKey);
		let payload: VideoRecoveryFailedIssuePayload | undefined;

		if (issue) {
			payload = {
				...(issue.payload as VideoRecoveryFailedIssuePayload),
				durationInMs: this._startedAt ? Date.now() - this._startedAt : undefined,
			};
		}

		this.trackMonitor.issues.resolve({
			key: this.issueKey,
			comment,
			payload,
			resolvedAt: Date.now(),
		});

		this._startedAt = undefined;
	}
}

```
### VideoResolutionChangeDetector
[Pinned implementation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/VideoResolutionChangeDetector.ts#L34)
Category: Telemetry
```ts
import { Detector } from "./Detector";
import { InboundTrackMonitor } from "../monitors/InboundTrackMonitor";
import { OutboundTrackMonitor } from "../monitors/OutboundTrackMonitor";
import { ClientEventTypes } from "../schema/ClientEventTypes";

/** `upgrade`/`downgrade` by pixel count; `reshape` when the pixel count holds but the aspect ratio does not. */
export type VideoResolutionChangeDirection = 'upgrade' | 'downgrade' | 'reshape';

export type VideoResolutionChangeDetectorConfig = {
	/** Whether to buffer a `VIDEO_RESOLUTION_CHANGED` client event into the sample. DEFAULT: true */
	createEvent?: boolean;
}

/**
 * Reports a video track's frame size changing, in either direction of the connection. The
 * adaptation ladder moving is the system working, so this emits events and raises no issue — the
 * value is the context attached: outbound, `qualityLimitationReason` at the moment of the change
 * separates an encoder dropping resolution for bandwidth or CPU from the application changing its
 * constraints, which look identical from the resolution alone; inbound, a change usually means the
 * SFU switched which simulcast layer it forwards.
 *
 * On an outbound simulcast track only the highest layer is followed. A zero or absent frame size
 * is a stream that has not produced a frame yet rather than a downgrade, and the first size seen
 * is the baseline, not a change.
 *
 * Raises no issue.
 * Monitor event: `video-resolution-changed`; client event `VIDEO_RESOLUTION_CHANGED`
 * when `createEvent` is left on. Config: `videoResolutionChangeDetector`.
 *
 * Category: Telemetry
 * Layer: Media
 *
 */
export class VideoResolutionChangeDetector implements Detector {
	public readonly name = 'video-resolution-change-detector';
	public disabled = false;

	private _width?: number;
	private _height?: number;

	public constructor(
		public readonly trackMonitor: InboundTrackMonitor | OutboundTrackMonitor,
	) {}

	private get config() {
		return this.peerConnection.parent.config.videoResolutionChangeDetector!;
	}

	private get peerConnection() {
		return this.trackMonitor.getPeerConnection();
	}

	public update() {
		if (this.disabled) return;
		if (this.trackMonitor.kind !== 'video') return;

		if (this.trackMonitor.readyState !== 'live') return;

		const rtp = this.trackMonitor.direction === 'inbound'
			? this.trackMonitor.getInboundRtp()
			: this.trackMonitor.highestLayer;

		if (!rtp) return;

		const width = rtp.frameWidth;
		const height = rtp.frameHeight;

		if (width === undefined || height === undefined) return;
		if (width < 1 || height < 1) return;

		const previousWidth = this._width;
		const previousHeight = this._height;

		this._width = width;
		this._height = height;

		if (previousWidth === undefined || previousHeight === undefined) return;
		if (previousWidth === width && previousHeight === height) return;

		const previousPixels = previousWidth * previousHeight;
		const pixels = width * height;
		const direction: VideoResolutionChangeDirection = pixels > previousPixels
			? 'upgrade'
			: pixels < previousPixels ? 'downgrade' : 'reshape';

		const qualityLimitationReason = this.trackMonitor.direction === 'outbound'
			? (rtp as { qualityLimitationReason?: string }).qualityLimitationReason
			: undefined;

		const clientMonitor = this.peerConnection.parent;

		clientMonitor.emit('video-resolution-changed', {
			clientMonitor,
			trackMonitor: this.trackMonitor,
			direction,
			from: { width: previousWidth, height: previousHeight },
			to: { width, height },
			qualityLimitationReason,
		});

		if (this.config.createEvent === false) return;

		clientMonitor.addEvent({
			type: ClientEventTypes.VIDEO_RESOLUTION_CHANGED,
			payload: {
				peerConnectionId: this.peerConnection.peerConnectionId,
				trackId: this.trackMonitor.track.id,
				direction: this.trackMonitor.direction,
				change: direction,
				fromWidth: previousWidth,
				fromHeight: previousHeight,
				width,
				height,
				framesPerSecond: rtp.framesPerSecond,
				qualityLimitationReason,
			},
		});
	}
}

```
## observer-js
### CallConcurrentIssueDetector
[Pinned implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/CallConcurrentIssueDetector.ts#L112)
```ts
import type { Detector } from './Detector';
import type { ObservedCall } from '../ObservedCall';
import type { ActiveClientIssue } from '../issues/ActiveClientIssue';
import type { ActiveIssueTracker } from '../issues/ActiveIssueTracker';
import { concludeCallIssue } from './IssueConclusion';

export const CallConcurrentIssueTypes = {
	/** Several participants of this call have the same issue open **at the same time**. */
	concurrentClientIssues: 'CONCURRENT_CLIENT_ISSUES',

	/** Those issues also *began* together — the signature of one shared event. */
	issueOnsetBurst: 'ISSUE_ONSET_BURST',
} as const;

export type CallConcurrentIssueDetectorConfig = {

	/**
	 * The issue types to watch. **Required, and must not be empty** — the detector subscribes to
	 * exactly these and sees nothing else.
	 */
	issueTypes: string[];

	/**
	 * Participants the call needs before a ratio means anything. Default `3`.
	 *
	 * In a 1:1 call "half the participants" is one person, which is a client problem and not a call
	 * problem — `2` effectively disables the ratio gate. Raise it for large-meeting products where you
	 * only care once a handful are affected.
	 */
	minClients: number;

	/**
	 * Distinct clients that must share the issue. Default `3`.
	 *
	 * The absolute floor under `affectedRatioThreshold`, so a small call cannot clear a ratio with two
	 * unlucky people. Sensible range `2`–`5`; `2` is the lowest that can still mean "more than one
	 * participant", which is the whole premise.
	 */
	minAffectedClients: number;

	/**
	 * Fraction of the call's participants that must share it, `0`–`1`. Default `0.5`.
	 *
	 * Typical `0.3`–`0.7`. Lower catches partial events — a subset on one SFU worker — at the cost of
	 * firing on a few coincidentally unhappy participants; `1` demands literally everyone, which real
	 * incidents rarely produce because someone always reconnects first.
	 */
	affectedRatioThreshold: number;

	/**
	 * Onsets falling within this span (ms) escalate the finding to `ISSUE_ONSET_BURST` — they did not
	 * just overlap, they started together. Default `2_000`.
	 *
	 * Bound this by your sampling period, not below it: onsets are only known as accurately as clients
	 * report them, so a window shorter than one sampling period can only fire by luck. Typical
	 * `1_000`–`5_000`. Wider makes the escalation meaningless, since unrelated issues drift into the
	 * same window.
	 */
	onsetBurstWindowInMs: number;

	/**
	 * Re-arm time per issue type (ms). Default `60_000`.
	 *
	 * A shared event is one incident, not one per tick. Too low and a persistent problem raises an
	 * issue every tick for as long as it lasts; too high and a genuinely new occurrence is swallowed
	 * by the previous one's cooldown. Typical `30_000`–`300_000`.
	 */
	cooldownMs: number;
};

/** What the detector currently knows about one issue type in this call. */
export type CallConcurrentIssueGroup = {
	type: string;
	issues: ActiveClientIssue[];
	clientIds: string[];
	affectedRatio: number;
	totalClients: number;

	/**
	 * Spread of the onsets, in **observer** time (ms) — `max(observedAt) - min(observedAt)`.
	 *
	 * Measured on the observer clock on purpose: `raisedAt` comes from each client's own clock, and
	 * comparing those across machines makes clock skew look like a shared event.
	 */
	onsetSpreadInMs: number;
	firstObservedAt: number;
};

/**
 * Answers **"is this meeting in trouble?"** — several participants of one call with the same issue
 * open simultaneously.
 *
 * The client already decides *what* is wrong for itself — `congestion`, `ice-disconnected`,
 * `audio-concealment`, `video-decoder-overloaded` — with hysteresis and multi-signal confirmation
 * behind each verdict. Re-deriving those server-side from raw counters would be strictly worse. What
 * the server uniquely knows is *how many other participants of the same call are in that state right
 * now*, which is the difference between "one person's Wi-Fi" and "this room is broken".
 *
 * Concurrency is judged from the **open interval set**, not a window of recent reports. A window has
 * to guess whether a symptom is still happening; an interval is closed by the client when the episode
 * actually ends (client-monitor-js >= 4.6.0 ships the `<type>-resolved` companion for exactly this).
 *
 * ```ts
 * observedCall.addDetector('call-concurrent-issue-detector', {
 *   issueTypes: [ 'congestion', 'ice-disconnected' ],
 * });
 * ```
 *
 * For the cross-call version of this question — which is a different question, not this one with a
 * bigger denominator — see `ObserverConcurrentIssueDetector`.
 */
export class CallConcurrentIssueDetector implements Detector, ActiveIssueTracker {
	public static readonly NAME = 'call-concurrent-issue-detector' as const;

	public readonly name = CallConcurrentIssueDetector.NAME;

	private readonly _config: CallConcurrentIssueDetectorConfig;
	private readonly _lastRaisedAt = new Map<string, number>();

	/** issue type -> the issues of that type currently open in this call. */
	private readonly _byType = new Map<string, Set<ActiveClientIssue>>();
	private _size = 0;

	/** The groups that qualified on the most recent `update()`. Exposed for tests/dashboards. */
	public lastGroups: CallConcurrentIssueGroup[] = [];

	public constructor(
		private readonly _call: ObservedCall,
		config: Partial<CallConcurrentIssueDetectorConfig> = {},
	) {
		this._config = {
			issueTypes: [],
			minClients: 3,
			minAffectedClients: 3,
			affectedRatioThreshold: 0.5,
			onsetBurstWindowInMs: 2_000,
			cooldownMs: 60_000,
			...config,
		};

		for (const type of this._config.issueTypes) {
			this._call.activeIssuesRegistry.addIssueTracker(type, this);
		}
	}

	public get size(): number {
		return this._size;
	}

	public has(issue: ActiveClientIssue): boolean {
		return this._byType.get(issue.type)?.has(issue) ?? false;
	}

	public add(issue: ActiveClientIssue): void {
		let bucket = this._byType.get(issue.type);

		if (!bucket) {
			bucket = new Set();
			this._byType.set(issue.type, bucket);
		}
		if (bucket.has(issue)) return;

		bucket.add(issue);
		++this._size;
	}

	public delete(issue: ActiveClientIssue): boolean {
		const bucket = this._byType.get(issue.type);

		if (!bucket?.delete(issue)) return false;

		--this._size;
		// Drop the empty bucket, so a long call doesn't retain one map entry per issue type ever seen.
		if (bucket.size === 0) this._byType.delete(issue.type);

		return true;
	}

	public clear(): void {
		this._byType.clear();
		this._size = 0;
		this.lastGroups = [];
	}

	public update(): void {
		this.lastGroups = [];

		// Nothing subscribed is open: the overwhelmingly common case, and it costs one check.
		if (this._size === 0) return;

		const now = Date.now();
		const totalClients = this._call.observedClients.size;

		if (totalClients < this._config.minClients) return;

		for (const [ type, issues ] of this._byType) {
			const group = this._groupOf(type, issues, totalClients);

			if (group.clientIds.length < this._config.minAffectedClients) continue;
			if (group.affectedRatio < this._config.affectedRatioThreshold) continue;

			this.lastGroups.push(group);

			if (now - (this._lastRaisedAt.get(type) ?? 0) < this._config.cooldownMs) continue;

			this._lastRaisedAt.set(type, now);

			const burst = group.onsetSpreadInMs <= this._config.onsetBurstWindowInMs;
			const issueType = burst
				? CallConcurrentIssueTypes.issueOnsetBurst
				: CallConcurrentIssueTypes.concurrentClientIssues;
			// The interpretation step: what this spread implies, stated once here rather than left to
			// whoever reads the alert.
			const conclusion = concludeCallIssue({
				issueType: type,
				affectedClients: group.clientIds.length,
				totalClients: group.totalClients,
				onsetBurst: burst,
			});

			this._call.addIssue({
				type: issueType,
				timestamp: now,
				conclusion,
				payload: {
					issueType: type,
					clients: group.totalClients,
					affectedClients: group.clientIds.length,
					affectedRatio: group.affectedRatio,
					affectedClientIds: group.clientIds,
					onsetSpreadInMs: group.onsetSpreadInMs,
					onsetBurst: burst,
					firstObservedAt: group.firstObservedAt,
				},
			});
		}
	}

	public close(): void {
		this._call.activeIssuesRegistry.removeIssueTracker(this);
		this._lastRaisedAt.clear();
		this.clear();
	}

	private _groupOf(type: string, issues: Set<ActiveClientIssue>, totalClients: number): CallConcurrentIssueGroup {
		// One pass, accumulating everything. `Math.min(...array)` on a spread would allocate and can
		// blow the stack on large groups, so the onsets are tracked here instead.
		const clientIds = new Set<string>();
		const list: ActiveClientIssue[] = [];
		let earliest = Infinity;
		let latest = -Infinity;

		for (const issue of issues) {
			list.push(issue);
			// One client can hold several issues of a type (one per track); the unit is the client, so
			// the ratio can never exceed 1.
			clientIds.add(issue.clientId);

			if (issue.observedAt < earliest) earliest = issue.observedAt;
			if (latest < issue.observedAt) latest = issue.observedAt;
		}

		return {
			type,
			issues: list,
			clientIds: [ ...clientIds ],
			totalClients,
			affectedRatio: 0 < totalClients ? clientIds.size / totalClients : 0,
			onsetSpreadInMs: latest - earliest,
			firstObservedAt: earliest,
		};
	}
}

```
### ClientPopulationIssueDetector
[Pinned implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/ClientPopulationIssueDetector.ts#L261)
```ts
import type { Detector } from './Detector';
import type { Observer } from '../Observer';
import type { ObservedClient } from '../ObservedClient';
import type { ActiveClientIssue } from '../issues/ActiveClientIssue';
import type { ActiveIssueTracker } from '../issues/ActiveIssueTracker';
import { geohash, type ClientLocation } from '../utils/geohash';
import { createLogger } from '../common/logger';

const logger = createLogger('ClientPopulationIssueDetector');

export const ClientPopulationIssueTypes = {
	/** One issue type is concentrated on one client population while the rest of the fleet is fine. */
	clientPopulationIssue: 'CLIENT_POPULATION_ISSUE',
} as const;

/** The client attribute to group by. One axis per detector — see the class description. */
export type ClientPopulationAxis = 'browser' | 'engine' | 'platform' | 'operationSystem' | 'location';

/**
 * Reads a client's coordinates, for `groupBy: 'location'`. **Required for that axis.**
 *
 * There is no coordinate field in `ClientSample`, so the shape is yours: read it off
 * `client.attachments`, off a custom meta item, or from an `appData` field your accept middleware
 * filled in. Return `undefined` for clients whose location you do not know — they are then excluded
 * from both the population and the control group, exactly like a client that never reported its
 * browser.
 */
export type ClientLocationResolver = (client: ObservedClient) => ClientLocation | undefined;

export type ClientPopulationIssueDetectorConfig = {

	/**
	 * The issue types to watch. **Required, and must not be empty.**
	 *
	 * **Match the issue family to the axis.** On the endpoint axes (`browser`, `engine`, `platform`,
	 * `operationSystem`) the types worth grouping are the ones an endpoint owns: `cpulimitation`,
	 * `encoder-bottleneck`, `capture-bottleneck`, `stuck-decoder`, `video-decoder-overloaded`.
	 * Grouping a *network* symptom by browser is a category error — `congestion` clusters by ISP and
	 * geography, not by build, and the detector would happily report a browser correlation that is
	 * really a "most of our users are on Chrome" artefact.
	 *
	 * On the `location` axis it is the other way round: group the network symptoms — `congestion`,
	 * `ice-disconnected`, `unstable-ice-path` — and not the endpoint ones, since there is no reason a
	 * decoder should stall by geography.
	 */
	issueTypes: string[];

	/** Which client attribute to group by. Default `'browser'`. */
	groupBy: ClientPopulationAxis;

	/**
	 * Where to read a client's coordinates. **Required when `groupBy` is `'location'`**, ignored
	 * otherwise. See {@link ClientLocationResolver}.
	 */
	resolveClientLocation?: ClientLocationResolver;

	/**
	 * Geohash characters to group locations by, i.e. how coarse a "place" is. Default `3` (~156 km).
	 *
	 * `2` ~1250 km, `3` ~156 km, `4` ~39 km, `5` ~5 km. Coarser cells hold more clients, which is what
	 * makes a rate mean anything, so start coarse: a city-sized cell rarely has `minPopulationSize`
	 * participants in it. See `utils/geohash` for why this is a grid cell and not a radius.
	 */
	locationPrecision: number;

	/**
	 * Group by `name` only, or by `name + version`. Default `true` (include version).
	 *
	 * Version is usually the point: "Chrome" is not actionable, "Chrome 141" is, because it names a
	 * thing that changed on a date. Set to `false` when comparing whole engines.
	 */
	includeVersion: boolean;

	/**
	 * Clients in a population before its rate means anything. Default `20`.
	 *
	 * Higher than the other detectors' minimums on purpose: this one compares *rates*, and a rate over
	 * five clients is not a rate. Sensible range `20`–`100`. On the `location` axis this is the field
	 * most likely to silence the detector — a city-sized cell rarely holds twenty concurrent
	 * participants, so reach for a coarser `locationPrecision` before lowering this.
	 */
	minPopulationSize: number;

	/**
	 * Affected clients required within the population. Default `5`.
	 *
	 * Checked independently of `affectedRatioThreshold`, so one unlucky user on a rare browser cannot
	 * page anyone however striking the ratio looks. Sensible range `5`–`20`.
	 */
	minAffectedClients: number;

	/**
	 * Share of the population that must be affected, `0`–`1`. Default `0.3`.
	 *
	 * Lower than the per-call thresholds deliberately: an issue hitting 30% of one browser version while
	 * the rest of the fleet is clean is already a strong signal, and endpoint faults rarely affect
	 * *everyone* on a build. Typical `0.2`–`0.5`. This is the weakest of the gates —
	 * `minRelativeRisk` is what makes the finding mean anything.
	 */
	affectedRatioThreshold: number;

	/**
	 * How many times worse the suspect population must be than the rest of the fleet. Default `3`.
	 *
	 * **This is the gate that makes the finding mean anything** — see the class description. Typical
	 * `2`–`10`. At `2` you will see populations that are merely somewhat worse, which is often just a
	 * different usage pattern; at `10` only stark, unambiguous concentrations survive. A spotless
	 * control group yields `Infinity`, which clears any threshold, so the minimum-count gates above are
	 * what stop that from being trivial.
	 */
	minRelativeRisk: number;

	/**
	 * Clients **outside** the suspect population before a comparison is possible. Default `20`.
	 *
	 * "Worse than everyone else" needs an everyone else. Sensible range `20`–`100`. Note the practical
	 * consequence: a fleet that is overwhelmingly one browser can never have that browser reported,
	 * because there is no control group left — which is honest, since at 95% Chrome you cannot separate a
	 * Chrome fault from a fleet-wide one.
	 */
	minControlSize: number;

	/**
	 * Re-arm time per (population, issue type) in ms. Default `300_000`.
	 *
	 * Long by design: a bad client build is a condition lasting days, not an event, and the action it
	 * prompts — ship a fix, roll back a version — is not one you take twice an hour. Typical
	 * `300_000`–`3_600_000`.
	 */
	cooldownMs: number;
};

/** The rollup for one population on one issue type. */
export type ClientPopulation = {

	/**
	 * e.g. `'Chrome 141'`, or `'Chrome'` when `includeVersion` is off. For the `'location'` axis this
	 * is the geohash cell — never the coordinates themselves, so an archived payload carries a place
	 * at the configured resolution and not a person's position.
	 */
	population: string;
	axis: ClientPopulationAxis;
	issueType: string;

	clients: number;
	affectedClients: number;
	affectedRatio: number;
	affectedClientIds: string[];

	/** Everyone not in this population. */
	controlClients: number;
	controlAffectedClients: number;
	controlAffectedRatio: number;

	/** `affectedRatio / controlAffectedRatio`. `Infinity` when the control group is completely clean. */
	relativeRisk: number;
};

/**
 * Finds an issue that is concentrated on **one kind of client** — one browser, one browser version,
 * one OS — rather than on anything the servers own.
 *
 * ### Why this exists
 *
 * The other observer-scoped detectors all answer "who else has this open, and what do they share?"
 * with the answer *the infrastructure*, because clients in unrelated calls share nothing else. That
 * inference is right for network symptoms and **wrong for endpoint symptoms**, and the difference
 * matters at 3am. `cpulimitation` opening across six unrelated calls is not an SFU event: CPU is
 * owned by the endpoint, so what those endpoints have in common is a client release, a browser
 * update, or a fleet of identical VDI hosts. `IssueConclusion` already says exactly this — it maps
 * the endpoint-capacity family to a `client-population` fault domain instead of `infrastructure` —
 * but until now nothing in the library actually computed the grouping that claim refers to. This
 * detector is that computation.
 *
 * It is the one correlation in this library that is neither per-call nor per-server. A client knows
 * its own browser and nothing about anyone else's; only something sitting above the whole fleet can
 * notice that every complaint is coming from the same build.
 *
 * ### The control group is the whole point
 *
 * "30% of Chrome 141 users report encoder-bottleneck" is not a finding on its own. If 30% of
 * *everyone* reports it, Chrome 141 is not the story — you have a fleet-wide problem and this
 * detector would be pointing at the largest population rather than at a cause. Naive share-based
 * grouping always indicts whichever browser is most popular, which is why the gate here is
 * **relative risk**: the suspect population's rate divided by the rate among everyone else. A
 * population only qualifies when it is `minRelativeRisk` times worse than the rest of the fleet, and
 * only when the rest of the fleet is large enough (`minControlSize`) for "the rest of the fleet" to
 * be a real measurement.
 *
 * A completely clean control group gives `Infinity`, which is honest — nobody outside this
 * population has the problem at all — and is exactly why `minAffectedClients` and
 * `minPopulationSize` are checked independently, so a single unlucky user on a rare browser cannot
 * page anyone.
 *
 * ### One axis per detector
 *
 * `groupBy` takes a single attribute. Add a second instance if you want a second axis:
 *
 * ```ts
 * observer.addObserverDetector('client-population-issue-detector', {
 *   issueTypes: [ 'cpulimitation', 'encoder-bottleneck', 'stuck-decoder' ],
 *   groupBy: 'browser',
 * });
 *
 * observer.on('observer-issue', ({ issue }) => {
 *   if (issue.type !== ClientPopulationIssueTypes.clientPopulationIssue) return;
 *   // → { population: 'Chrome 141', issueType: 'encoder-bottleneck',
 *   //     affectedRatio: 0.34, controlAffectedRatio: 0.02, relativeRisk: 17 }
 * });
 * ```
 *
 * Deliberately not a cross-product of every axis at once: an issue that clusters on macOS *and* on
 * Safari is usually one fact reported twice, and a detector that emits both leaves the reader to
 * work out which one is causal. Pick the axis you want to reason about.
 *
 * ### The `location` axis
 *
 * With `groupBy: 'location'` the population is a **geohash cell** rather than a client attribute, so
 * the same machinery answers a different question: *is this symptom concentrated in one place?* That
 * is the grouping the note above says browsers cannot give you, and it is the one that matters for
 * network symptoms.
 *
 * The observer does not derive "this client's RTT jumped" — `client-monitor`'s `CongestionDetector`
 * already owns that verdict, comparing each peer connection's RTT against its own EWMA baseline and
 * requiring a bandwidth-limitation corroboration before it raises `congestion`. Absolute RTT is not
 * comparable between clients anyway: someone 200 ms away is *always* 200 ms away, so the only signal
 * is deviation from that client's own baseline, which is exactly what the client already measures.
 * This detector's contribution is the part no endpoint can see — that many of the affected clients
 * are in the same place at the same time.
 *
 * ```ts
 * observer.addObserverDetector('client-population-issue-detector', {
 *   issueTypes: [ 'congestion', 'ice-disconnected' ],
 *   groupBy: 'location',
 *   locationPrecision: 3,                                  // ~156 km cells
 *   resolveClientLocation: (client) => client.attachments?.geo as { latitude: number, longitude: number },
 * });
 * ```
 *
 * Coordinates are not in `ClientSample`, so `resolveClientLocation` is required — see
 * {@link ClientLocationResolver}. Only the cell key reaches the issue payload, never the
 * coordinates, which matters because these payloads are archived into call summaries.
 *
 * **The limitation to state plainly: geography is confounded with your topology.** The control group
 * is "everyone outside this cell", which cannot separate *"the path into this region degraded"* from
 * *"the SFU that happens to serve this region degraded"*. If a region maps largely onto one
 * deployment, both hypotheses fit the same evidence. The discriminator is whether clients elsewhere
 * on the same server also degraded, which is what `SfuCongestionDetector` and
 * `TurnServerHealthDetector` answer — so the conclusion here points at them rather than claiming an
 * attribution it cannot support.
 *
 * ### Clients that never reported their metadata
 *
 * `browser` / `engine` / `platform` / `operationSystem` arrive as client metadata and may be absent —
 * a client that closed before sending them, or an application that does not collect them. Those
 * clients are excluded from **both** the population and the control group rather than bucketed as
 * `'unknown'`. The same applies to a client whose location `resolveClientLocation` cannot supply. A synthetic `'unknown'` population would be a mixture of every real one, so any rate
 * computed for it means nothing, and leaving those clients in the control group would dilute the
 * comparison with clients whose kind we cannot verify.
 */
export class ClientPopulationIssueDetector implements Detector, ActiveIssueTracker {
	public static readonly NAME = 'client-population-issue-detector' as const;

	public readonly name = ClientPopulationIssueDetector.NAME;

	private readonly _config: ClientPopulationIssueDetectorConfig;
	private readonly _lastRaisedAt = new Map<string, number>();
	private readonly _issues = new Set<ActiveClientIssue>();

	/** The populations that qualified on the most recent `update()`. Exposed for tests/dashboards. */
	public lastPopulations: ClientPopulation[] = [];

	public constructor(
		private readonly _observer: Observer,
		config: Partial<ClientPopulationIssueDetectorConfig> = {},
	) {
		this._config = {
			issueTypes: [],
			groupBy: 'browser',
			locationPrecision: 3,
			includeVersion: true,
			minPopulationSize: 20,
			minAffectedClients: 5,
			affectedRatioThreshold: 0.3,
			minRelativeRisk: 3,
			minControlSize: 20,
			cooldownMs: 300_000,
			...config,
		};

		// Misconfiguration must not look like "nothing is wrong". Without a resolver every client
		// returns `undefined`, the detector finds no populations, and it would sit there silently
		// reporting nothing for the life of the process.
		if (this._config.groupBy === 'location' && !this._config.resolveClientLocation) {
			logger.warn(
				'%s is configured with groupBy: \'location\' but no resolveClientLocation, so no client can be placed and nothing will ever be detected',
				this.name,
			);
		}

		for (const type of this._config.issueTypes) {
			this._observer.activeIssuesRegistry.addIssueTracker(type, this);
		}
	}

	public get size(): number {
		return this._issues.size;
	}

	public has(issue: ActiveClientIssue): boolean {
		return this._issues.has(issue);
	}

	public add(issue: ActiveClientIssue): void {
		this._issues.add(issue);
	}

	public delete(issue: ActiveClientIssue): boolean {
		return this._issues.delete(issue);
	}

	public clear(): void {
		this._issues.clear();
		this.lastPopulations = [];
	}

	public update(): void {
		this.lastPopulations = [];

		if (this._issues.size === 0) return;

		const now = Date.now();
		// The denominators: how many clients of each population exist at all. Built from the fleet
		// rather than from the affected set, because a rate needs everyone, not just the unhappy.
		const populationSizes = new Map<string, number>();

		for (const call of this._observer.observedCalls.values()) {
			for (const client of call.observedClients.values()) {
				const population = this._populationOf(client);

				if (population === undefined) continue;

				populationSizes.set(population, (populationSizes.get(population) ?? 0) + 1);
			}
		}

		if (populationSizes.size === 0) return;

		// (issueType, population) -> the affected client ids. Built from the issues we hold, so the
		// cost is the number of open issues rather than the size of the fleet.
		const affected = new Map<string, Map<string, Set<string>>>();

		for (const issue of this._issues) {
			const client = this._observer.observedCalls.get(issue.callId)?.observedClients.get(issue.clientId);

			if (!client) continue;

			const population = this._populationOf(client);

			if (population === undefined) continue;

			let byPopulation = affected.get(issue.type);

			if (!byPopulation) {
				byPopulation = new Map();
				affected.set(issue.type, byPopulation);
			}

			const clientIds = byPopulation.get(population) ?? new Set<string>();

			clientIds.add(issue.clientId);
			byPopulation.set(population, clientIds);
		}

		for (const [ issueType, byPopulation ] of affected) {
			// The fleet total for this issue type, so each population can be compared against everyone
			// else rather than against an absolute threshold.
			let totalAffected = 0;

			for (const clientIds of byPopulation.values()) totalAffected += clientIds.size;

			let totalClients = 0;

			for (const size of populationSizes.values()) totalClients += size;

			for (const [ population, clientIds ] of byPopulation) {
				const clients = populationSizes.get(population) ?? clientIds.size;
				const rollup = this._rollupOf(
					population,
					issueType,
					clientIds,
					clients,
					totalClients - clients,
					totalAffected - clientIds.size,
				);

				if (rollup.clients < this._config.minPopulationSize) continue;
				if (rollup.affectedClients < this._config.minAffectedClients) continue;
				if (rollup.affectedRatio < this._config.affectedRatioThreshold) continue;
				// Without a control group there is nothing to be "worse than", and a bare share would
				// simply indict the most popular browser.
				if (rollup.controlClients < this._config.minControlSize) continue;
				if (rollup.relativeRisk < this._config.minRelativeRisk) continue;

				this.lastPopulations.push(rollup);

				const key = `${population}:${issueType}`;

				if (now - (this._lastRaisedAt.get(key) ?? 0) < this._config.cooldownMs) continue;

				this._lastRaisedAt.set(key, now);

				const isLocation = this._config.groupBy === 'location';

				this._observer.addIssue({
					type: ClientPopulationIssueTypes.clientPopulationIssue,
					timestamp: now,
					conclusion: {
						// Geography is not something endpoints own. A cluster of network symptoms in one
						// place is a path/transit story, so it is attributed to the infrastructure rather
						// than to a client build.
						faultDomain: isLocation ? 'infrastructure' : 'client-population',
						summary: `'${issueType}' is ${this._riskText(rollup.relativeRisk)} more likely ${isLocation ? `in cell ${population}` : `on ${population}`} than across the rest of the fleet (${rollup.affectedClients}/${rollup.clients} vs ${rollup.controlAffectedClients}/${rollup.controlClients})`,
						recommendation: isLocation
							// The confounder is real and not separable here: see the class description.
							? 'look at the path into that region — ISP, transit or peering — but first rule out the servers those clients share, since a region often maps onto one SFU or TURN deployment'
							: 'this is not an SFU symptom — look at what those clients share: a recent release, a browser version, or shared/virtualised hardware',
						confidence: this._confidenceOf(rollup),
					},
					payload: { ...rollup },
				});
			}
		}
	}

	public close(): void {
		this._observer.activeIssuesRegistry.removeIssueTracker(this);
		this._lastRaisedAt.clear();
		this.clear();
	}

	/** `undefined` when the client never reported this attribute — see the class description. */
	private _populationOf(client: ObservedClient): string | undefined {
		if (this._config.groupBy === 'location') {
			const location = this._config.resolveClientLocation?.(client);

			return location ? geohash(location, this._config.locationPrecision) : undefined;
		}

		const attribute = client[this._config.groupBy];

		if (!attribute?.name) return undefined;

		return this._config.includeVersion && attribute.version
			? `${attribute.name} ${attribute.version}`
			: attribute.name;
	}

	private _rollupOf(
		population: string,
		issueType: string,
		clientIds: Set<string>,
		clients: number,
		controlClients: number,
		controlAffectedClients: number,
	): ClientPopulation {
		const affectedRatio = 0 < clients ? clientIds.size / clients : 0;
		const controlAffectedRatio = 0 < controlClients ? controlAffectedClients / controlClients : 0;

		return {
			population,
			axis: this._config.groupBy,
			issueType,
			clients,
			affectedClients: clientIds.size,
			affectedRatio,
			affectedClientIds: [ ...clientIds ],
			controlClients,
			controlAffectedClients,
			controlAffectedRatio,
			// A spotless control group means nobody outside this population has the problem at all.
			// `Infinity` says that plainly rather than dividing by zero or inventing a ceiling.
			relativeRisk: 0 < controlAffectedRatio
				? affectedRatio / controlAffectedRatio
				: (0 < affectedRatio ? Infinity : 0),
		};
	}

	private _riskText(relativeRisk: number): string {
		return Number.isFinite(relativeRisk) ? `${relativeRisk.toFixed(1)}x` : 'exclusively';
	}

	/** Bigger populations and starker contrasts are harder to produce by chance. */
	private _confidenceOf(rollup: ClientPopulation): number {
		let confidence = 0.4;

		if (100 <= rollup.clients) confidence += 0.2;
		else if (50 <= rollup.clients) confidence += 0.1;

		if (10 <= rollup.relativeRisk) confidence += 0.3;
		else if (5 <= rollup.relativeRisk) confidence += 0.2;
		else confidence += 0.1;

		return Math.min(1, Math.round(confidence * 100) / 100);
	}
}

```
### IssueFanOutDetector
[Pinned implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/IssueFanOutDetector.ts#L100)
```ts
import type { Detector } from './Detector';
import type { ObservedCall } from '../ObservedCall';
import type { ObservedOutboundTrack } from '../ObservedOutboundTrack';
import type { ActiveClientIssue } from '../issues/ActiveClientIssue';
import type { ActiveIssueTracker } from '../issues/ActiveIssueTracker';
import { concludeCallIssue } from './IssueConclusion';

export const IssueFanOutTypes = {
	/** Most receivers of one published track have the same issue open → the fault follows the source. */
	publishedTrackIssueFanOut: 'PUBLISHED_TRACK_ISSUE_FAN_OUT',

	/** Exactly one receiver of a track has it → that receiver's own problem. */
	singleReceiverIssue: 'SINGLE_RECEIVER_ISSUE',
} as const;

export type IssueFanOutDetectorConfig = {

	/**
	 * The receiver-side issue types to attribute to publishers. **Required, and must not be empty** —
	 * the detector subscribes to exactly these.
	 *
	 * There is no "all types" option. Which of a receiver's complaints are worth blaming a publisher
	 * for is application knowledge: `freezed-video-track` fanning out across a track's subscribers
	 * implicates the source, `cpulimitation` fanning out the same way implicates the receivers'
	 * hardware and would be a false accusation.
	 */
	issueTypes: string[];

	/**
	 * Receivers a track needs before a ratio means anything. Default `3`.
	 *
	 * With two receivers, "60% affected" is one of them — which is the single-receiver case below, not
	 * a fan-out. Sensible range `2`–`5`; in small calls a published track rarely has more than a couple
	 * of subscribers, so raising this can silence the detector entirely.
	 */
	minReceivers: number;

	/**
	 * Fraction of a track's receivers that must share the issue, `0`–`1`. Default `0.6`.
	 *
	 * The higher this is, the more the finding points at the publisher rather than at the network
	 * between: *everyone* receiving this track badly is hard to explain any other way. Typical
	 * `0.5`–`0.8`. Below `0.5` you are reporting "some receivers", which usually means their own
	 * last miles.
	 */
	affectedRatioThreshold: number;

	/**
	 * Also report when exactly one receiver is affected. Default `true`.
	 *
	 * Kept on because the finding is *useful and correctly weaker*: it is raised with a lower
	 * confidence and the opposite conclusion — one unhappy receiver out of eight points at that
	 * receiver, not at the publisher. Turn it off if you only want publisher-blaming findings and
	 * treat single-receiver trouble as the client's own business.
	 */
	reportSingleReceiver: boolean;

	/**
	 * Re-arm time per (track, issue type) in ms. Default `60_000`.
	 *
	 * Per track, so a call with many bad publishers still reports each of them. Typical
	 * `30_000`–`300_000`.
	 */
	cooldownMs: number;
};

/**
 * Attributes **client-reported issues to the published track they are about**, then asks how far
 * the problem fans out across that track's receivers.
 *
 * The join is what makes this possible: a receiver-side issue payload carries `trackId` (the client
 * detectors report it for every track-scoped issue), the observer resolves that to an inbound track,
 * and `RemoteTrackResolver` links the inbound track to the `remoteOutboundTrack` that published it.
 * With the whole subscriber set of one source in hand, the verdict is straightforward and is the
 * single most useful thing a server can say:
 *
 * - **most receivers of Alice's track are affected** → the fault is on Alice's path — her uplink, the
 *   SFU's ingress, or its forwarding of that stream.
 * - **one receiver of Alice's track is affected** → that receiver's downlink. Nothing to do with
 *   Alice, even though the symptom is reported against her stream.
 *
 * Deliberately generic over the issue vocabulary: `freezed-video-track`, `keyframe-storm`,
 * `audio-concealment`, `video-decoder-overloaded`, `stuck-decoder` and anything a custom client
 * detector invents all fan out the same way, so one mechanism replaces a family of symptom-specific
 * detectors.
 *
 * ### It walks the affected tracks, never all of them
 *
 * The detector is fed open issues by the call's registry and keeps only those carrying a `trackId`.
 * Each tick it resolves *those* tracks to their publishers — never the published tracks of the call,
 * of which there are many more and almost all of them fine. A call with nothing wrong costs one
 * `size === 0` check.
 *
 * ### Requires a `RemoteTrackResolver`
 *
 * Without publisher↔subscriber links there is no way to know which receivers belong to one source,
 * so the detector does nothing when the call has no resolver. It does not fall back to guessing:
 * "one receiver of an unknown set" is not a statement worth raising.
 */
export class IssueFanOutDetector implements Detector, ActiveIssueTracker {
	public static readonly NAME = 'issue-fan-out-detector';

	public readonly name = IssueFanOutDetector.NAME;

	private readonly _config: IssueFanOutDetectorConfig;
	private readonly _lastRaisedAt = new Map<string, number>();

	/** Open issues that name a track. Issues without a `trackId` cannot be attributed and are dropped. */
	private readonly _trackIssues = new Set<ActiveClientIssue>();

	public constructor(
		private readonly _call: ObservedCall,
		config: Partial<IssueFanOutDetectorConfig> = {},
	) {
		this._config = {
			issueTypes: [],
			minReceivers: 3,
			affectedRatioThreshold: 0.6,
			reportSingleReceiver: true,
			cooldownMs: 60_000,
			...config,
		};

		for (const type of this._config.issueTypes) {
			this._call.activeIssuesRegistry.addIssueTracker(type, this);
		}
	}

	public get size(): number {
		return this._trackIssues.size;
	}

	public has(issue: ActiveClientIssue): boolean {
		return this._trackIssues.has(issue);
	}

	public add(issue: ActiveClientIssue): void {
		// An issue with no `trackId` says nothing about a published track; holding it would only make
		// `size` lie about how much there is to do.
		if (issue.trackId === undefined) return;

		this._trackIssues.add(issue);
	}

	public delete(issue: ActiveClientIssue): boolean {
		return this._trackIssues.delete(issue);
	}

	public clear(): void {
		this._trackIssues.clear();
	}

	public update(): void {
		if (this._trackIssues.size === 0) return;
		// Without links, "the receivers of this track" is unknowable — never guess.
		if (!this._call.remoteTrackResolver) return;

		const now = Date.now();
		// publisher track -> issue type -> the affected receiver client ids.
		const byPublisher = new Map<ObservedOutboundTrack, Map<string, Set<string>>>();

		for (const issue of this._trackIssues) {
			const publisher = this._publisherOf(issue);

			if (!publisher) continue;

			let byType = byPublisher.get(publisher);

			if (!byType) {
				byType = new Map();
				byPublisher.set(publisher, byType);
			}

			const clientIds = byType.get(issue.type) ?? new Set<string>();

			clientIds.add(issue.clientId);
			byType.set(issue.type, clientIds);
		}

		for (const [ publisher, byType ] of byPublisher) {
			const numberOfReceivers = publisher.remoteInboundTracks.size;

			if (numberOfReceivers === 0) continue;

			for (const [ issueType, clientIds ] of byType) {
				// A receiver may hold several issues of one type (one per track); the unit is the client,
				// and `clientIds` is already a set, so the ratio can never exceed 1.
				const affectedRatio = clientIds.size / numberOfReceivers;
				const isFanOut = this._config.minReceivers <= numberOfReceivers
					&& this._config.affectedRatioThreshold <= affectedRatio;
				const isSingle = this._config.reportSingleReceiver
					&& clientIds.size === 1 && 1 < numberOfReceivers;

				if (!isFanOut && !isSingle) continue;

				const key = `${publisher.id}:${issueType}`;

				if (now - (this._lastRaisedAt.get(key) ?? 0) < this._config.cooldownMs) continue;

				this._lastRaisedAt.set(key, now);

				const type = isFanOut
					? IssueFanOutTypes.publishedTrackIssueFanOut
					: IssueFanOutTypes.singleReceiverIssue;

				// What the fan-out implies. A track-scoped group is a strong statement: the affected
				// clients share a publisher and nothing else, so the receivers are exonerated.
				const conclusion = concludeCallIssue({
					issueType,
					affectedClients: clientIds.size,
					totalClients: numberOfReceivers,
					onsetBurst: false,
					publishedTrackId: isFanOut ? publisher.id : undefined,
				});

				this._call.addIssue({
					type,
					timestamp: now,
					conclusion,
					payload: {
						issueType,
						trackId: publisher.id,
						kind: publisher.kind,
						publisherClientId: publisher.getPeerConnection().client.clientId,
						// The corroborating half: if the source's own egress looks fine while its
						// receivers do not, the SFU/forwarding path is implicated rather than the sender.
						publisherBitrate: publisher.bitrate,
						publisherDegraded: publisher.degraded,
						publisherDegradedReasons: publisher.degradedReasons,
						receivers: numberOfReceivers,
						affectedReceivers: clientIds.size,
						affectedRatio,
						affectedClientIds: [ ...clientIds ],
					},
				});
			}
		}
	}

	public close(): void {
		this._call.activeIssuesRegistry.removeIssueTracker(this);
		this._lastRaisedAt.clear();
		this.clear();
	}

	/**
	 * Resolve the issue's `trackId` to the outbound track that published it.
	 *
	 * Looked up through the reporting client's own peer connections rather than by scanning the call:
	 * the issue names its client, so the search is bounded by that client's transports (typically one
	 * or two) instead of by the size of the meeting.
	 */
	private _publisherOf(issue: ActiveClientIssue): ObservedOutboundTrack | undefined {
		const client = this._call.observedClients.get(issue.clientId);

		if (!client || issue.trackId === undefined) return undefined;

		for (const peerConnection of client.observedPeerConnections.values()) {
			const inboundTrack = peerConnection.observedInboundTracks.get(issue.trackId);

			if (inboundTrack) return inboundTrack.remoteOutboundTrack;
		}

		return undefined;
	}
}

```
### ObserverConcurrentIssueDetector
[Pinned implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/ObserverConcurrentIssueDetector.ts#L128)
```ts
import type { Detector } from './Detector';
import type { Observer } from '../Observer';
import type { ActiveClientIssue } from '../issues/ActiveClientIssue';
import type { ActiveIssueTracker } from '../issues/ActiveIssueTracker';
import { concludeObserverIssue } from './IssueConclusion';

export const ObserverConcurrentIssueTypes = {
	/**
	 * The same issue is open in **several unrelated calls at once**. Those clients share no meeting,
	 * no publisher and no room — only the infrastructure serving them.
	 */
	crossCallConcurrentIssues: 'CROSS_CALL_CONCURRENT_ISSUES',

	/** The cross-call version that also started together. The strongest "it's us" signal available. */
	crossCallIssueOnsetBurst: 'CROSS_CALL_ISSUE_ONSET_BURST',
} as const;

export type ObserverConcurrentIssueDetectorConfig = {

	/**
	 * The issue types to watch. **Required, and must not be empty** — the detector subscribes to
	 * exactly these and sees nothing else.
	 */
	issueTypes: string[];

	/**
	 * Distinct clients that must share the open issue. Default `3`.
	 *
	 * Absolute, deliberately — see `affectedCallRatioThreshold` for why no client *ratio* exists at
	 * this scope. Sensible range `3`–`10`; scale it with fleet size, since three clients is a real
	 * signal across five calls and background noise across five hundred.
	 */
	minAffectedClients: number;

	/**
	 * Minimum number of *distinct calls* the affected clients must span. Default `2`.
	 *
	 * This is what makes an observer-scoped finding mean something a call-scoped one doesn't. Without
	 * it, one thirty-person meeting with congestion satisfies every client-count threshold and raises
	 * a fleet-wide alert for what is really one bad room — which `CallConcurrentIssueDetector` has
	 * already reported. Requiring two or more independent calls is the difference between a
	 * coincidence and a shared cause.
	 */
	minAffectedCalls: number;

	/**
	 * Fraction of the calls in flight that must be affected. Default `0` — off, because absolute
	 * counts matter more than ratios here: three broken calls out of a thousand is still worth
	 * knowing about, and a ratio threshold would hide it. Raise it if you only care about fleet-wide
	 * events.
	 *
	 * Note there is deliberately **no participant ratio** at this scope. Six broken calls out of forty
	 * is a handful of clients against the whole fleet, so any meaningful client ratio would suppress
	 * exactly the finding this detector exists to produce.
	 */
	affectedCallRatioThreshold: number;

	/**
	 * Onsets falling within this span (ms) escalate the finding to `CROSS_CALL_ISSUE_ONSET_BURST`.
	 * Default `2_000`.
	 *
	 * This is the strongest evidence the detector produces: independent calls starting to fail *at the
	 * same instant* has no explanation other than something they share. Keep it at or above your
	 * sampling period — onsets are only as precise as clients report them — and no wider than a few
	 * seconds, or unrelated failures drift into the same window. Typical `1_000`–`5_000`.
	 */
	onsetBurstWindowInMs: number;

	/**
	 * Re-arm time per issue type (ms). Default `60_000`.
	 *
	 * Typical `60_000`–`600_000`. A fleet-wide event is one incident: without a cooldown a sustained
	 * outage would raise an issue on every tick for its whole duration.
	 */
	cooldownMs: number;
};

/** What the detector currently knows about one issue type across the fleet. */
export type ObserverConcurrentIssueGroup = {
	type: string;
	issues: ActiveClientIssue[];
	clientIds: string[];
	totalClients: number;
	affectedRatio: number;
	callIds: string[];
	totalCalls: number;
	affectedCallRatio: number;

	/** Per-call breakdown, largest first — the first question anyone asks is "which calls, how badly?". */
	perCall: { callId: string, affectedClients: number, totalClients: number }[];

	/**
	 * Spread of the onsets, in **observer** time (ms). Client clocks are never compared across
	 * machines here — skew between them would masquerade as a synchronized event.
	 */
	onsetSpreadInMs: number;
	firstObservedAt: number;
};

/**
 * Answers **"is our infrastructure in trouble?"** — the same issue open across several *unrelated*
 * calls at the same moment.
 *
 * This is not the call-scoped question with a bigger denominator, which is why it is a separate
 * detector with separate gates and its own finding types. Participant count alone is a bad fleet
 * signal: one thirty-person meeting where everybody is congested clears every client threshold, yet
 * it has an obvious local explanation. Clients in *different* calls share no room, no publisher and
 * no host — only the servers and the network. When the same issue opens across several of them at
 * once, the infrastructure is the only remaining common factor, and that is the finding worth paging
 * someone about.
 *
 * ```ts
 * observer.addObserverDetector('observer-concurrent-issue-detector', {
 *   issueTypes: [ 'congestion', 'ice-disconnected' ],
 *   minAffectedCalls: 3,
 * });
 *
 * observer.on('observer-issue', ({ issue }) => {
 *   if (issue.type === ObserverConcurrentIssueTypes.crossCallIssueOnsetBurst) page(issue);
 * });
 * // → CROSS_CALL_ISSUE_ONSET_BURST { issueType: 'congestion', calls: 40, affectedCalls: 6, … }
 * ```
 *
 * Onsets are compared on the **observer clock** (`observedAt`), never on client clocks: participants
 * degrading together within a couple of seconds is far more likely to be a deploy, a TURN failover or
 * a link flap than a coincidence — but only if the timestamps being compared came from one clock.
 */
export class ObserverConcurrentIssueDetector implements Detector, ActiveIssueTracker {
	public static readonly NAME = 'observer-concurrent-issue-detector' as const;

	public readonly name = ObserverConcurrentIssueDetector.NAME;

	private readonly _config: ObserverConcurrentIssueDetectorConfig;
	private readonly _lastRaisedAt = new Map<string, number>();

	/** issue type -> the issues of that type currently open anywhere in the fleet. */
	private readonly _byType = new Map<string, Set<ActiveClientIssue>>();
	private _size = 0;

	/** The groups that qualified on the most recent `update()`. Exposed for tests/dashboards. */
	public lastGroups: ObserverConcurrentIssueGroup[] = [];

	public constructor(
		private readonly _observer: Observer,
		config: Partial<ObserverConcurrentIssueDetectorConfig> = {},
	) {
		this._config = {
			issueTypes: [],
			minAffectedClients: 3,
			minAffectedCalls: 2,
			affectedCallRatioThreshold: 0,
			onsetBurstWindowInMs: 2_000,
			cooldownMs: 60_000,
			...config,
		};

		for (const type of this._config.issueTypes) {
			this._observer.activeIssuesRegistry.addIssueTracker(type, this);
		}
	}

	public get size(): number {
		return this._size;
	}

	public has(issue: ActiveClientIssue): boolean {
		return this._byType.get(issue.type)?.has(issue) ?? false;
	}

	public add(issue: ActiveClientIssue): void {
		let bucket = this._byType.get(issue.type);

		if (!bucket) {
			bucket = new Set();
			this._byType.set(issue.type, bucket);
		}
		if (bucket.has(issue)) return;

		bucket.add(issue);
		++this._size;
	}

	public delete(issue: ActiveClientIssue): boolean {
		const bucket = this._byType.get(issue.type);

		if (!bucket?.delete(issue)) return false;

		--this._size;
		if (bucket.size === 0) this._byType.delete(issue.type);

		return true;
	}

	public clear(): void {
		this._byType.clear();
		this._size = 0;
		this.lastGroups = [];
	}

	public update(): void {
		this.lastGroups = [];

		if (this._size === 0) return;

		const now = Date.now();

		for (const [ type, issues ] of this._byType) {
			const group = this._groupOf(type, issues);

			if (group.clientIds.length < this._config.minAffectedClients) continue;
			if (group.callIds.length < this._config.minAffectedCalls) continue;
			if (group.affectedCallRatio < this._config.affectedCallRatioThreshold) continue;

			this.lastGroups.push(group);

			if (now - (this._lastRaisedAt.get(type) ?? 0) < this._config.cooldownMs) continue;

			this._lastRaisedAt.set(type, now);

			const burst = group.onsetSpreadInMs <= this._config.onsetBurstWindowInMs;
			const issueType = burst
				? ObserverConcurrentIssueTypes.crossCallIssueOnsetBurst
				: ObserverConcurrentIssueTypes.crossCallConcurrentIssues;
			const conclusion = concludeObserverIssue({
				issueType: type,
				affectedClients: group.clientIds.length,
				totalClients: group.totalClients,
				affectedCalls: group.callIds.length,
				totalCalls: group.totalCalls,
				onsetBurst: burst,
			});

			this._observer.addIssue({
				type: issueType,
				timestamp: now,
				conclusion,
				payload: {
					issueType: type,
					clients: group.totalClients,
					affectedClients: group.clientIds.length,
					affectedRatio: group.affectedRatio,
					affectedClientIds: group.clientIds,
					// The dimension that makes this finding what it is.
					calls: group.totalCalls,
					affectedCalls: group.callIds.length,
					affectedCallRatio: group.affectedCallRatio,
					affectedCallIds: group.callIds,
					perCall: group.perCall,
					onsetSpreadInMs: group.onsetSpreadInMs,
					onsetBurst: burst,
					firstObservedAt: group.firstObservedAt,
				},
			});
		}
	}

	public close(): void {
		this._observer.activeIssuesRegistry.removeIssueTracker(this);
		this._lastRaisedAt.clear();
		this.clear();
	}

	private _groupOf(type: string, issues: Set<ActiveClientIssue>): ObserverConcurrentIssueGroup {
		const clientIds = new Set<string>();
		const affectedByCall = new Map<string, Set<string>>();
		const list: ActiveClientIssue[] = [];
		let earliest = Infinity;
		let latest = -Infinity;

		for (const issue of issues) {
			list.push(issue);
			clientIds.add(issue.clientId);

			let clients = affectedByCall.get(issue.callId);

			if (!clients) {
				clients = new Set();
				affectedByCall.set(issue.callId, clients);
			}
			clients.add(issue.clientId);

			if (issue.observedAt < earliest) earliest = issue.observedAt;
			if (latest < issue.observedAt) latest = issue.observedAt;
		}

		const totalClients = this._observer.numberOfClients;
		const totalCalls = this._observer.observedCalls.size;
		const perCall: ObserverConcurrentIssueGroup['perCall'] = [];

		for (const [ callId, clients ] of affectedByCall) {
			perCall.push({
				callId,
				affectedClients: clients.size,
				// A call that closed while its issues were still open has no participant count left;
				// fall back to the affected count rather than reporting a 0 denominator.
				totalClients: this._observer.observedCalls.get(callId)?.observedClients.size ?? clients.size,
			});
		}
		perCall.sort((a, b) => b.affectedClients - a.affectedClients);

		return {
			type,
			issues: list,
			clientIds: [ ...clientIds ],
			totalClients,
			affectedRatio: 0 < totalClients ? clientIds.size / totalClients : 0,
			callIds: perCall.map((entry) => entry.callId),
			totalCalls,
			affectedCallRatio: 0 < totalCalls ? perCall.length / totalCalls : 0,
			perCall,
			onsetSpreadInMs: latest - earliest,
			firstObservedAt: earliest,
		};
	}
}

```
### PublisherFaultCorroborationDetector
[Pinned implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/PublisherFaultCorroborationDetector.ts#L109)
```ts
import type { Detector } from './Detector';
import type { ObservedCall } from '../ObservedCall';
import type { ObservedOutboundTrack } from '../ObservedOutboundTrack';
import type { ActiveClientIssue } from '../issues/ActiveClientIssue';
import type { ActiveIssueTracker } from '../issues/ActiveIssueTracker';

export const PublisherFaultTypes = {
	/**
	 * A publisher is reporting trouble on its own send path **while** its subscribers report trouble
	 * receiving it. Both ends agree, so the source is implicated rather than inferred.
	 */
	corroboratedPublisherFault: 'CORROBORATED_PUBLISHER_FAULT',
} as const;

export type PublisherFaultCorroborationDetectorConfig = {

	/**
	 * Issue types raised by the **publishing** client about its own outbound path. **Required.**
	 *
	 * The natural set from client-monitor-js: `encoder-bottleneck`, `capture-bottleneck`,
	 * `dry-outbound-track`. All three mean "I am failing to produce or send this properly", which is
	 * the half of the story the receivers cannot see.
	 */
	publisherIssueTypes: string[];

	/**
	 * Issue types raised by the **subscribing** clients about the track they receive. **Required.**
	 *
	 * The natural set: `freezed-video-track`, `dry-inbound-track`, `video-recovery-failed`. These say
	 * "I am not getting this properly", which is the half the publisher cannot see.
	 */
	receiverIssueTypes: string[];

	/**
	 * Subscribers of the track that must be complaining at the same time. Default `2`.
	 *
	 * `1` still yields a genuine two-sided corroboration — publisher and one receiver agreeing is
	 * already more than either says alone — but `2` rules out the case where a single receiver's own
	 * downlink is at fault and merely coincides with the publisher's complaint. Sensible range `1`–`3`;
	 * higher mostly costs you findings in small calls, where a track may only have two subscribers.
	 */
	minAffectedReceivers: number;

	/**
	 * Re-arm time per published track (ms). Default `60_000`.
	 *
	 * Typical `30_000`–`300_000`. This detector raises the highest-confidence finding in the library,
	 * so it is the one you least want repeating every tick.
	 */
	cooldownMs: number;
};

/** The two-sided evidence behind one finding. */
export type CorroboratedPublisherFault = {
	trackId: string;
	kind: string;
	publisherClientId: string;

	/** The publisher's own open issue types on this track. */
	publisherIssueTypes: string[];

	/** The receiver-side open issue types across this track's subscribers. */
	receiverIssueTypes: string[];

	receivers: number;
	affectedReceivers: number;
	affectedClientIds: string[];
	publisherBitrate?: number;
};

/**
 * Fires only when **both ends of one published track are complaining at the same time**: the
 * publisher about its own send path, and its subscribers about receiving it.
 *
 * ### How this differs from `IssueFanOutDetector`
 *
 * Fan-out sees one end. It observes that most of Alice's subscribers are unhappy and *infers* that
 * the fault is on Alice's side, because the affected clients share a publisher and nothing else. That
 * inference is sound, and it is still a inference: the same observation is produced by the SFU
 * mangling Alice's stream on the way out, with Alice herself perfectly healthy.
 *
 * This detector removes the inference. When Alice reports `encoder-bottleneck` *and* four of her six
 * subscribers report `freezed-video-track` in the same window, there is nothing left to deduce — the
 * source said it was struggling and the receivers confirmed the consequence. That is the strongest
 * statement this library can make about where a fault sits, and it is only available to something
 * holding both ends at once. Neither the publisher nor any receiver can reach this conclusion alone.
 *
 * Run both: fan-out is broader and catches the SFU-forwarding case where the publisher is fine;
 * this one is narrower and, when it fires, needs no interpretation.
 *
 * ### Silence here is not health
 *
 * A quiet detector means only that the two halves have not coincided — most commonly because the
 * publisher is genuinely fine and the fault is in forwarding, which is exactly the case `fan-out`
 * exists to report. Do not read "no corroborated fault" as "no publisher-side problem".
 *
 * ```ts
 * observedCall.addDetector('publisher-fault-corroboration-detector', {
 *   publisherIssueTypes: [ 'encoder-bottleneck', 'capture-bottleneck', 'dry-outbound-track' ],
 *   receiverIssueTypes: [ 'freezed-video-track', 'dry-inbound-track' ],
 * });
 * ```
 *
 * ### Requires a `RemoteTrackResolver`
 *
 * Matching a publisher's issue to its subscribers' issues needs the publisher↔subscriber links. With
 * no resolver the detector does nothing rather than guessing.
 */
export class PublisherFaultCorroborationDetector implements Detector, ActiveIssueTracker {
	public static readonly NAME = 'publisher-fault-corroboration-detector' as const;

	public readonly name = PublisherFaultCorroborationDetector.NAME;

	private readonly _config: PublisherFaultCorroborationDetectorConfig;
	private readonly _lastRaisedAt = new Map<string, number>();

	/** Open publisher-side issues that name a track. */
	private readonly _publisherIssues = new Set<ActiveClientIssue>();

	/** Open receiver-side issues that name a track. */
	private readonly _receiverIssues = new Set<ActiveClientIssue>();

	/** The faults corroborated on the most recent `update()`. Exposed for tests/dashboards. */
	public lastFaults: CorroboratedPublisherFault[] = [];

	public constructor(
		private readonly _call: ObservedCall,
		config: Partial<PublisherFaultCorroborationDetectorConfig> = {},
	) {
		this._config = {
			publisherIssueTypes: [],
			receiverIssueTypes: [],
			minAffectedReceivers: 2,
			cooldownMs: 60_000,
			...config,
		};

		for (const type of this._config.publisherIssueTypes) {
			this._call.activeIssuesRegistry.addIssueTracker(type, this);
		}
		for (const type of this._config.receiverIssueTypes) {
			this._call.activeIssuesRegistry.addIssueTracker(type, this);
		}
	}

	public get size(): number {
		return this._publisherIssues.size + this._receiverIssues.size;
	}

	public has(issue: ActiveClientIssue): boolean {
		return this._publisherIssues.has(issue) || this._receiverIssues.has(issue);
	}

	public add(issue: ActiveClientIssue): void {
		// Without a `trackId` the issue cannot be attached to either end of a specific stream.
		if (issue.trackId === undefined) return;

		if (this._config.publisherIssueTypes.includes(issue.type)) this._publisherIssues.add(issue);
		else if (this._config.receiverIssueTypes.includes(issue.type)) this._receiverIssues.add(issue);
	}

	public delete(issue: ActiveClientIssue): boolean {
		return this._publisherIssues.delete(issue) || this._receiverIssues.delete(issue);
	}

	public clear(): void {
		this._publisherIssues.clear();
		this._receiverIssues.clear();
		this.lastFaults = [];
	}

	public update(): void {
		this.lastFaults = [];

		// Corroboration needs both halves. If either side is silent there is nothing to correlate, and
		// this is the common case — so it costs two `size` checks.
		if (this._publisherIssues.size === 0 || this._receiverIssues.size === 0) return;
		if (!this._call.remoteTrackResolver) return;

		const now = Date.now();
		// Start from the publisher side: it is the smaller set (one client per track, versus one per
		// subscriber) and it is the side that has to be present for a finding to exist at all.
		const suspects = new Map<ObservedOutboundTrack, Set<string>>();

		for (const issue of this._publisherIssues) {
			const publisher = this._outboundTrackOf(issue);

			if (!publisher) continue;

			const types = suspects.get(publisher) ?? new Set<string>();

			types.add(issue.type);
			suspects.set(publisher, types);
		}

		if (suspects.size === 0) return;

		// Index the receiver complaints by the inbound track they name, so each suspect's subscriber
		// set can be checked with a lookup per subscriber instead of a scan of every open issue.
		const receiverIssuesByTrackId = new Map<string, ActiveClientIssue[]>();

		for (const issue of this._receiverIssues) {
			const existing = receiverIssuesByTrackId.get(issue.trackId as string);

			if (existing) existing.push(issue);
			else receiverIssuesByTrackId.set(issue.trackId as string, [ issue ]);
		}

		for (const [ publisher, publisherIssueTypes ] of suspects) {
			const receivers = publisher.remoteInboundTracks;

			if (receivers.size === 0) continue;

			const affectedClientIds = new Set<string>();
			const receiverIssueTypes = new Set<string>();

			for (const receiver of receivers) {
				const issues = receiverIssuesByTrackId.get(receiver.id);

				if (!issues) continue;

				for (const issue of issues) {
					affectedClientIds.add(issue.clientId);
					receiverIssueTypes.add(issue.type);
				}
			}

			if (affectedClientIds.size < this._config.minAffectedReceivers) continue;

			const fault: CorroboratedPublisherFault = {
				trackId: publisher.id,
				kind: publisher.kind,
				publisherClientId: publisher.getPeerConnection().client.clientId,
				publisherIssueTypes: [ ...publisherIssueTypes ],
				receiverIssueTypes: [ ...receiverIssueTypes ],
				receivers: receivers.size,
				affectedReceivers: affectedClientIds.size,
				affectedClientIds: [ ...affectedClientIds ],
				publisherBitrate: publisher.bitrate,
			};

			this.lastFaults.push(fault);

			if (now - (this._lastRaisedAt.get(publisher.id) ?? 0) < this._config.cooldownMs) continue;

			this._lastRaisedAt.set(publisher.id, now);

			this._call.addIssue({
				type: PublisherFaultTypes.corroboratedPublisherFault,
				timestamp: now,
				conclusion: {
					faultDomain: 'published-track',
					summary: `${fault.publisherClientId} reports ${fault.publisherIssueTypes.join(', ')} on track ${fault.trackId} while ${fault.affectedReceivers} of ${fault.receivers} subscribers report ${fault.receiverIssueTypes.join(', ')} — both ends agree`,
					recommendation: 'the source is implicated, not inferred: check that publisher\'s capture, encoder and uplink before looking at the SFU or the receivers',
					// Higher than any single-ended finding: two independent parties, one conclusion.
					confidence: 0.9,
				},
				payload: { ...fault },
			});
		}
	}

	public close(): void {
		this._call.activeIssuesRegistry.removeIssueTracker(this);
		this._lastRaisedAt.clear();
		this.clear();
	}

	/**
	 * Resolve a publisher-side issue's `trackId` to the outbound track it is about.
	 *
	 * Looked up through the reporting client's own peer connections: the issue names its client, so
	 * the search is bounded by that client's transports rather than by the size of the call.
	 */
	private _outboundTrackOf(issue: ActiveClientIssue): ObservedOutboundTrack | undefined {
		const client = this._call.observedClients.get(issue.clientId);

		if (!client || issue.trackId === undefined) return undefined;

		for (const peerConnection of client.observedPeerConnections.values()) {
			const outboundTrack = peerConnection.observedOutboundTracks.get(issue.trackId);

			if (outboundTrack) return outboundTrack;
		}

		return undefined;
	}
}

```
### SfuCongestionDetector
[Pinned implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/SfuCongestionDetector.ts#L164)
```ts
import { Detector, Observer } from '..';
import { median, robustZScore } from '../utils/stats';
import { ActiveClientIssue } from '../issues/ActiveClientIssue';
import { ActiveIssueTracker } from '../issues/ActiveIssueTracker';

/**
 * One completed sampling bucket: how many/which clients reported congestion during it.
 *
 * `totalClients` (and therefore `congestedClientRatio`) is a snapshot of `observer.numberOfClients`
 * taken when the bucket closes — an approximation of "how many clients could have been congested",
 * not a claim that every client sent exactly one sample within the bucket. Good enough for a ratio
 * that only needs to be comparable bucket-to-bucket.
 */
export type SfuCongestionDetectorBucket = {
	observedAt: number;
	totalClients: number;
	congestedClients: number;
	congestedClientRatio: number;
	affectedClientIds: string[];
	affectedCallIds: string[];
};

export type SfuCongestionDetectorReport = {
	affectedCallIds: string[];
	affectedClientIds: string[];
	congestedClientRatio: number;
	totalNumberOfClients: number;
	numberOfCongestedClients: number;
	// the number of completed buckets kept in history at the time of detection
	historySize: number;
	// diagnostics: the baseline this bucket was judged against, and by how much it cleared it
	baselineCongestedClientRatio: number;
	robustZ: number;
	absoluteIncrease: number;
	relativeIncrease: number;
}

export type SfuCongestionDetectorConfig = {

	/**
	 * Client issue types counted as "congestion" for this indicator. Default `[ 'congestion' ]`.
	 *
	 * Keep this narrow. Every type you add widens what counts as a congested client, and the whole
	 * method rests on comparing *like with like* across time buckets — mixing in a type that appears
	 * for unrelated reasons raises the baseline and buries the spike you are looking for.
	 */
	consumedClientIssueTypes: string[];

	/** The `observer-issue` type raised when a bucket is judged congested. Default `'sfu-congestion'`. */
	emittedObserverIssueType: string;

	/**
	 * How long your clients take to send a sample (ms). Default `10_000`.
	 *
	 * **Set this to your collector's actual sampling period** — it is a description of your clients,
	 * not a tuning knob. The bucket is `samplesSendingTimeInMs * 2`, so every client gets a fair
	 * chance to report at least once inside each bucket. Set it too short and clients that simply had
	 * not reported yet look absent, so the ratio jumps around on sampling noise; too long and the
	 * detector reacts slowly and averages a spike away.
	 */
	samplesSendingTimeInMs: number;

	/**
	 * Completed buckets kept as history — the candidate plus its baseline. Default `30`.
	 *
	 * At the default bucket size this is ~10 minutes of baseline. Sensible range `10`–`60`. Longer is
	 * more robust to a single odd bucket but slower to accept a genuinely changed normal (a growth
	 * spurt, a new region coming online); shorter adapts quickly but lets a sustained problem become
	 * the new baseline and stop being reported.
	 */
	historySize: number;

	/**
	 * Buckets required before any judgement is made. Default `5`.
	 *
	 * Below this the detector is silent, which is the point: a median and MAD over two buckets is not
	 * a baseline. Costs `minHistorySize * samplesSendingTimeInMs * 2` of warm-up after start — about
	 * 100 s at the defaults. Do not lower it to make a test fire faster; shorten the bucket instead.
	 */
	minHistorySize: number;

	/**
	 * Distinct congested clients required in the candidate bucket. Default `3`.
	 *
	 * The absolute floor beneath every ratio below, so that a tiny fleet cannot produce a finding: two
	 * unhappy clients out of four is 50% and means nothing. Raise it on a large fleet where three
	 * clients is always noise.
	 */
	minAffectedClients: number;

	/**
	 * How far the candidate's congested-client **ratio** must exceed the baseline median, in absolute
	 * terms (`0`–`1`). Default `0.05`, i.e. five percentage points.
	 *
	 * This is the practical-significance gate: it stops a statistically striking move from 0.5% to 2%
	 * being reported as an event. Typical `0.03`–`0.15`.
	 */
	minAbsoluteRatioIncrease: number;

	/**
	 * How many times the baseline median the candidate ratio must reach. Default `2`.
	 *
	 * Multiplicative counterpart to the absolute gate — both must pass. Typical `1.5`–`3`. Below
	 * `1.5` ordinary fluctuation qualifies; above ~`4` only near-total events do.
	 */
	minRelativeRatioIncrease: number;

	/**
	 * Robust z-score the candidate must reach against a median+MAD baseline. Default `3`.
	 *
	 * The statistical-significance gate. `3` is the conventional "clearly outside normal variation";
	 * `2` is noticeably chattier, `4`–`5` only for very stable fleets. Median and MAD rather than mean
	 * and standard deviation on purpose — a couple of past incidents in the history would inflate a
	 * standard deviation enough to hide the next one. Note that a perfectly flat baseline gives
	 * `MAD = 0`, where any increase scores `Infinity`; the two ratio gates above are what keep that
	 * honest.
	 */
	robustZThreshold: number;
}

/** The statistical/practical-significance verdict for one candidate bucket against its baseline. */
export type SfuCongestionDetectorEvaluation = {
	isCongested: boolean;
	baselineCongestedClientRatio: number;
	robustZ: number;
	absoluteIncrease: number;
	relativeIncrease: number;
};

/**
 * Detects a **shared** congestion event: many clients, across different calls, reporting congestion
 * inside the same slice of time.
 *
 * Only add this when the observer's calls all come from the **same SFU** — the finding's whole
 * meaning is "these clients have nothing in common except that server", and that is only true if the
 * server really is the common factor.
 *
 * ### Why fixed-interval buckets, and not the update tick
 *
 * The obvious implementation counts congested clients on each `update()`. It is wrong here, for two
 * separate reasons:
 *
 * - **The tick is not evenly spaced.** `update()` fires when a client is updated, so its rate is a
 *   function of how many clients are connected and how their sampling happens to interleave. Two
 *   counts taken from windows of different length are not comparable, and this detector's entire
 *   job is to compare a count against earlier counts.
 * - **Clients report on their own schedule.** A client sends a sample roughly every
 *   `samplesSendingTimeInMs`, unsynchronised with every other client. A window shorter than that
 *   systematically undercounts — half the congested clients simply hadn't spoken yet — and the
 *   undercount varies with arrival phase, which is noise indistinguishable from signal.
 *
 * So the detector runs on a wall-clock interval and closes a bucket every
 * `samplesSendingTimeInMs`, giving every client a fair chance to be heard in each one. Buckets are
 * equal-length and equally lagged, which is what makes bucket-to-bucket comparison mean something.
 * {@link update} is deliberately empty: nothing here is driven by the update tick.
 *
 * ### Occurrences, not intervals
 *
 * Unlike `ConcurrentIssueDetector`, this one ignores resolutions — see {@link delete}. It counts how
 * many *distinct clients reported* congestion in a bucket, not how many are still congested. A
 * client that hits congestion and immediately drops its bitrate resolves the issue within seconds
 * and would vanish from an open-interval view, yet it is exactly the evidence wanted here.
 */
export class SfuCongestionDetector implements Detector, ActiveIssueTracker {
	public static readonly NAME = 'sfu-congestion-detector';

	public readonly name = SfuCongestionDetector.NAME;

	private readonly _config: SfuCongestionDetectorConfig;
	private readonly _history: SfuCongestionDetectorBucket[] = [];
	private readonly _trackedIssues = new Set<ActiveClientIssue>();
	private timer: ReturnType<typeof setInterval> | undefined;
	private _lastEvaluatedBucket: SfuCongestionDetectorBucket | undefined;

	public constructor(
		private readonly _observer: Observer,
		config: Partial<SfuCongestionDetectorConfig> = {},
	) {
		this._config = {
			consumedClientIssueTypes: [
				'congestion'
			],
			emittedObserverIssueType: 'sfu-congestion',
			samplesSendingTimeInMs: 10_000,
			historySize: 30,
			minHistorySize: 5,
			minAffectedClients: 3,
			minAbsoluteRatioIncrease: 0.05,
			minRelativeRatioIncrease: 2,
			robustZThreshold: 3,
			...config,
		};

		for (const issueType of this._config.consumedClientIssueTypes) {
			this._observer.activeIssuesRegistry.addIssueTracker(issueType, this);
		}

		this.timer = setInterval(() => {
			this._closeBucket(Date.now());
			this._evaluateLatestBucket();
		}, this._config.samplesSendingTimeInMs);

		// Do not hold the process open. This is a monitoring side-channel: if the application has
		// nothing else to do, it should be allowed to exit, and without this a library import alone
		// keeps Node alive forever. Optional-called because some fake-timer implementations return a
		// handle without `unref`, and a monitoring detail must never break a caller's test run.
		this.timer.unref?.();
	}
	public get size() {
		return this._trackedIssues.size;
	}

	/** Record the issue against the bucket currently open. The timer, not this, closes the bucket. */
	public add(issue: ActiveClientIssue): void {
		this._trackedIssues.add(issue);
	}

	/**
	 * Deliberately a no-op returning `false`.
	 *
	 * Resolutions are not interesting here. A congested client typically fixes its own symptom by
	 * dropping bitrate hard, so the issue closes within seconds — but it still *happened*, and it is
	 * evidence that the server was under pressure during this bucket. What matters is how many
	 * distinct clients reported congestion within the bucket and whether that count suddenly jumps,
	 * not how long any one client's issue stayed open.
	 *
	 * Nothing leaks: the tracked set is emptied wholesale every time a bucket closes.
	 */
	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	public delete(_issue: ActiveClientIssue): boolean {
		return false;
	}

	public clear(): void {
		this._trackedIssues.clear();
		this._history.length = 0;
		this._lastEvaluatedBucket = undefined;
	}

	public has(issue: ActiveClientIssue): boolean {
		return this._trackedIssues.has(issue);
	}

	public close(): void {
		if (this.timer) {
			clearInterval(this.timer);
			this.timer = undefined;
		}

		// Unsubscribe, or the registry keeps feeding a detector that has stopped rotating its buckets —
		// `_trackedIssues` would then grow for the life of the observer.
		this._observer.activeIssuesRegistry.removeIssueTracker(this);

		this.clear();
	}

	/** The completed buckets kept so far, oldest first. Read-only — for introspection/tests. */
	public get history(): readonly SfuCongestionDetectorBucket[] {
		return this._history;
	}

	/**
	 * Intentionally empty — see the class description.
	 *
	 * Everything here is driven by the bucket timer, because the update tick is neither evenly spaced
	 * nor long enough for every client to have reported. Counting on it would compare windows of
	 * different lengths and call the difference a signal.
	 */
	public update(): void {
		// no-op
	}

	private _closeBucket(observedAt: number): void {
		const totalClients = this._observer.numberOfClients;
		const affectedClientIds = [ ...new Set(Array.from(this._trackedIssues, (issue) => issue.clientId)) ];
		const affectedCallIds = [ ...new Set(Array.from(this._trackedIssues, (issue) => issue.callId)) ];
		const congestedClients = affectedClientIds.length;
		const congestedClientRatio = 0 < totalClients ? congestedClients / totalClients : 0;

		this._history.push({
			observedAt,
			totalClients,
			congestedClients,
			congestedClientRatio,
			affectedClientIds,
			affectedCallIds,
		});

		while (this._config.historySize < this._history.length) this._history.shift();

		this._trackedIssues.clear();
	}

	/**
	 * Evaluate only the latest completed bucket (the candidate) against the buckets before it (the
	 * baseline) — never against itself. Reached once per newly-closed bucket via {@link update}; the
	 * identity check below additionally guards against evaluating the same bucket twice, in case
	 * `update()` is ever called again before the next rotation.
	 */
	private _evaluateLatestBucket(): void {
		const candidate = this._history[this._history.length - 1];

		if (candidate === this._lastEvaluatedBucket) return;
		this._lastEvaluatedBucket = candidate;

		const baseline = this._history.slice(0, -1);
		const evaluation = this._evaluateBucket(candidate, baseline);

		if (!evaluation.isCongested) return;

		const payload: SfuCongestionDetectorReport = {
			affectedCallIds: candidate.affectedCallIds,
			affectedClientIds: candidate.affectedClientIds,
			congestedClientRatio: candidate.congestedClientRatio,
			totalNumberOfClients: candidate.totalClients,
			numberOfCongestedClients: candidate.congestedClients,
			historySize: this._history.length,
			baselineCongestedClientRatio: evaluation.baselineCongestedClientRatio,
			robustZ: evaluation.robustZ,
			absoluteIncrease: evaluation.absoluteIncrease,
			relativeIncrease: evaluation.relativeIncrease,
		};

		// Through `addIssue`, not a raw `emit`: that is what stamps `scope` and keeps this finding
		// indistinguishable in shape from every other observer-scoped one.
		this._observer.addIssue({
			type: this._config.emittedObserverIssueType,
			timestamp: Date.now(),
			payload: { ...payload },
		});
	}

	/**
	 * Is `candidate` — the latest completed bucket — abnormally high compared with the `baseline`
	 * buckets before it?
	 *
	 * Requires both **statistical** significance (a robust z-score against a median+MAD baseline —
	 * deliberately not Mann-Kendall, which asks "is this a monotonic trend", not "is the latest point
	 * an outlier"; a single sudden spike on an otherwise flat series is exactly what should trigger
	 * here and exactly what a trend test would miss) and **practical** significance (enough affected
	 * clients, and a big enough absolute/relative jump — a statistically significant move in a tiny
	 * or trivial ratio is not worth an alert).
	 */
	private _evaluateBucket(candidate: SfuCongestionDetectorBucket, baseline: SfuCongestionDetectorBucket[]): SfuCongestionDetectorEvaluation {
		const baselineRatios = baseline.map((bucket) => bucket.congestedClientRatio);
		const baselineMedian = median(baselineRatios) ?? 0;
		const robustZ = robustZScore(candidate.congestedClientRatio, baselineRatios) ?? 0;
		const absoluteIncrease = candidate.congestedClientRatio - baselineMedian;
		const relativeIncrease = 0 < baselineMedian
			? candidate.congestedClientRatio / baselineMedian
			: (0 < candidate.congestedClientRatio ? Infinity : 0);

		const isCongested = this._config.minHistorySize <= baseline.length + 1
			// Practical significance first: these are cheap, and they are what stop a statistically
			// perfect signal over three clients from waking anyone.
			&& this._config.minAffectedClients <= candidate.congestedClients
			&& this._config.minAbsoluteRatioIncrease <= absoluteIncrease
			&& this._config.minRelativeRatioIncrease <= relativeIncrease
			&& this._config.robustZThreshold <= robustZ;

		return { isCongested, baselineCongestedClientRatio: baselineMedian, robustZ, absoluteIncrease, relativeIncrease };
	}
}

```
### TrackDeliveryMismatchDetector
[Pinned implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/TrackDeliveryMismatchDetector.ts#L99)
```ts
import type { Detector } from './Detector';
import type { ObservedCall } from '../ObservedCall';
import { ActiveIssueTracker } from '../issues/ActiveIssueTracker';
import { ActiveClientIssue } from '../issues/ActiveClientIssue';

export const TrackDeliveryMismatchTypes = {
	/**
	 * The source is sending, but **none** of its subscribers are receiving → the media is being lost
	 * between the publisher and the receivers. In an SFU that means the forwarding path.
	 */
	publishedTrackNotDelivered: 'PUBLISHED_TRACK_NOT_DELIVERED',

	/**
	 * The source is sending and most subscribers are fine, but **some** are dry → those consumers are
	 * broken individually (in mediasoup, the usual mitigation is recreating the consumer).
	 */
	receiverTrackNotDelivered: 'RECEIVER_TRACK_NOT_DELIVERED',

	/**
	 * The source itself stopped producing, so its subscribers being dry is expected and **not** an
	 * SFU fault. Reported so the other two verdicts can be trusted as *not* being this.
	 */
	publisherTrackDry: 'PUBLISHER_TRACK_DRY',
} as const;

export type TrackDeliveryMismatchDetectorConfig = {

	/**
	 * The receiver-side issue type meaning "no media arriving". Default `'dry-inbound-track'`, which is
	 * what client-monitor-js raises. Only change it if you raise your own equivalent.
	 */
	dryInboundIssueType: string;

	/**
	 * The publisher-side issue type meaning "not producing". Default `'dry-outbound-track'`, as raised
	 * by client-monitor-js. The pairing of these two types is the whole detector: their **disagreement**
	 * is the finding.
	 */
	dryOutboundIssueType: string;

	/**
	 * Subscribers required before "all of them" means anything. Default `2`.
	 *
	 * With one subscriber, "every receiver is dry" is a single client's report and carries no more
	 * weight than the client issue already does. Sensible range `2`–`4`.
	 */
	minReceivers: number;

	/**
	 * Fraction of subscribers that must be dry to call it a whole-track delivery failure. Default `1`.
	 *
	 * `1` — literally all of them — on purpose. The inference here is sharp: the publisher says it is
	 * sending and *every* receiver says nothing arrives, so the fault is between them, in the SFU's
	 * forwarding. Lowering it to `0.8` admits mixed evidence, where some receivers do get the media, and
	 * the conclusion no longer follows: that is a per-receiver problem and `IssueFanOutDetector`'s
	 * question. Do not lower it without deciding what the finding then means.
	 */
	allReceiversRatio: number;

	/** Re-arm time per (track, verdict) in ms. Default `60_000`. Typical `30_000`–`300_000`. */
	cooldownMs: number;

};

type DeliveryItem = {
	publisherClientId: string,
	publisherSending: boolean,
	publisherDryIssue: boolean,
	publisherBitrate: number,
	numberOfSubscribers: number,
	numberOfDrySubscribers: number,
}

/**
 * Answers **"is the media actually getting through?"** by joining the two ends of a published track.
 *
 * A dry track is the clearest possible symptom — no bytes are arriving — but on its own it is
 * ambiguous, and the ambiguity is precisely what a single endpoint cannot resolve. A receiver seeing
 * silence cannot tell whether the camera was switched off, the SFU stopped forwarding, or its own
 * consumer wedged. All three look identical from the browser.
 *
 * With the publisher↔subscriber links this becomes a three-way decision:
 *
 * | publisher | subscribers | verdict |
 * |---|---|---|
 * | sending | **all** dry | `PUBLISHED_TRACK_NOT_DELIVERED` — the SFU/forwarding path |
 * | sending | **some** dry | `RECEIVER_TRACK_NOT_DELIVERED` — those consumers (recreate them) |
 * | dry | any dry | `PUBLISHER_TRACK_DRY` — the source stopped; not an SFU fault |
 *
 * The publisher side is judged from **both** signals available: its own `dry-outbound-track` issue
 * when the client reports one, and — as the fallback, and the corroboration when it does not — the
 * observed outbound RTP (`deltaPacketsSent`). That combination is what makes the first row
 * trustworthy: the server can state that packets demonstrably left the publisher during the same
 * interval in which every receiver got nothing.
 *
 * This is the "SFU forwarding mismatch" check, and notably it needs **no** mediasoup instrumentation
 * — the client's own dry-track verdicts plus the resolver links are sufficient.
 */
export class TrackDeliveryMismatchDetector implements Detector, ActiveIssueTracker {
	public static readonly NAME = 'track-delivery-mismatch-detector' as const;
	public readonly name = TrackDeliveryMismatchDetector.NAME;

	private readonly _config: TrackDeliveryMismatchDetectorConfig;
	private readonly _lastRaisedAt = new Map<string, number>();
	private readonly dryOutboundTracks = new Set<string>();
	private readonly dryInboundTracks = new Set<string>();

	public constructor(
		private readonly call: ObservedCall,
		config: Partial<TrackDeliveryMismatchDetectorConfig> = {},
	) {
		this._config = {
			dryOutboundIssueType: 'dry-outbound-track',
			dryInboundIssueType: 'dry-inbound-track',
			minReceivers: 2,
			allReceiversRatio: 1,
			cooldownMs: 60_000,
			...config,
		};

		// Subscribe here, like every other tracker-shaped detector. Without this the dry-track sets
		// stay empty forever and `update()` silently judges every publisher as having zero dry
		// subscribers — the detector would run, cost time, and never be able to find anything.
		this.call.activeIssuesRegistry.addIssueTracker(this._config.dryOutboundIssueType, this);
		this.call.activeIssuesRegistry.addIssueTracker(this._config.dryInboundIssueType, this);
	}

	public close(): void {
		this.call.activeIssuesRegistry.removeIssueTracker(this);
		this._lastRaisedAt.clear();
		this.clear();
	}

	public add(issue: ActiveClientIssue): void {
		if (issue.type === this._config.dryOutboundIssueType) {
			if (issue.trackId) {
				this.dryOutboundTracks.add(issue.trackId);
			}
		} else if (issue.type === this._config.dryInboundIssueType) {
			if (issue.trackId) {
				this.dryInboundTracks.add(issue.trackId);
			}
		}
	}

	public delete(issue: ActiveClientIssue): boolean {
		if (issue.type === this._config.dryOutboundIssueType) {
			this.dryOutboundTracks.delete(issue.trackId ?? '');
		} else if (issue.type === this._config.dryInboundIssueType) {
			this.dryInboundTracks.delete(issue.trackId ?? '');
		}
		
		return true;
	}

	public get size(): number {
		return this.dryOutboundTracks.size + this.dryInboundTracks.size;
	}

	public clear(): void {
		this.dryOutboundTracks.clear();
		this.dryInboundTracks.clear();
	}

	public has(issue: ActiveClientIssue): boolean {
		if (issue.type === this._config.dryOutboundIssueType) {
			return this.dryOutboundTracks.has(issue.trackId ?? '');
		} else if (issue.type === this._config.dryInboundIssueType) {
			return this.dryInboundTracks.has(issue.trackId ?? '');
		}
		
		return false;
	}

	public update(): void {
		const now = Date.now();
		const deliveries = new Map<string, DeliveryItem>();

		for (const client of this.call.observedClients.values()) {
			for (const peerConnection of client.observedPeerConnections.values()) {
				for (const outboundTrack of peerConnection.observedOutboundTracks.values()) {
					deliveries.set(outboundTrack.id, {
						publisherClientId: client.clientId,
						publisherSending: (outboundTrack.bitrate ?? 0) > 0,
						publisherDryIssue: this.dryOutboundTracks.has(outboundTrack.id),
						publisherBitrate: outboundTrack.bitrate ?? 0,
						numberOfDrySubscribers: 0,
						numberOfSubscribers: 0,
					});
				}
				for (const inboundTrack of peerConnection.observedInboundTracks.values()) {
					const delivery = deliveries.get(inboundTrack.remoteOutboundTrack?.id ?? '');

					if (!delivery) {
						continue;
					}

					delivery.numberOfDrySubscribers += this.dryInboundTracks.has(inboundTrack.id) ? 1 : 0;
					delivery.numberOfSubscribers += 1;
				}
			}
		}

		for (const [ outboundTrackId, delivery ] of deliveries) {
			if (delivery.numberOfSubscribers < this._config.minReceivers) {
				continue;
			}

			// Nothing is wrong: the publisher is sending and no subscriber reported a dry track. Without
			// this the `else` branch below is unconditional, so a perfectly healthy call raises
			// RECEIVER_TRACK_NOT_DELIVERED for every published track, every cooldown period.
			if (delivery.publisherSending && delivery.numberOfDrySubscribers === 0) continue;

			const dryRatio = delivery.numberOfDrySubscribers / delivery.numberOfSubscribers;
			let type: string;

			if (!delivery.publisherSending) {
				type = TrackDeliveryMismatchTypes.publisherTrackDry;
			} else if (this._config.allReceiversRatio <= dryRatio) {
				type = TrackDeliveryMismatchTypes.publishedTrackNotDelivered;
			} else {
				type = TrackDeliveryMismatchTypes.receiverTrackNotDelivered;
			}

			const key = `${outboundTrackId}:${type}`;

			if (now - (this._lastRaisedAt.get(key) ?? 0) < this._config.cooldownMs) continue;

			this._lastRaisedAt.set(key, now);

			this.call.addIssue({
				type,
				timestamp: now,
				payload: {
					trackId: outboundTrackId,
					publisherClientId: delivery.publisherClientId,
					publisherSending: delivery.publisherSending,
					publisherDryIssue: delivery.publisherDryIssue,
					publisherBitrate: delivery.publisherBitrate,
					numberOfSubscribers: delivery.numberOfSubscribers,
					numberOfDrySubscribers: delivery.numberOfDrySubscribers,
				},
			});
		}
	}

}

```
### TurnServerHealthDetector
[Pinned implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/TurnServerHealthDetector.ts#L93)
```ts
import type { Detector } from './Detector';
import type { Observer } from '../Observer';
import type { ObservedPeerConnection } from '../ObservedPeerConnection';

export const TurnServerHealthTypes = {
	/** One TURN server's clients are in trouble while other servers' clients are fine. */
	turnServerDegraded: 'TURN_SERVER_DEGRADED',
} as const;

export type TurnServerHealthDetectorConfig = {

	/**
	 * Clients a server must be carrying before its ratio means anything. Default `5`.
	 *
	 * With two relayed clients, "half are degraded" is one person having a bad time. Sensible range
	 * `5`–`20`; raise it if you run many small TURN deployments, since each needs enough traffic to be
	 * measurable on its own.
	 */
	minClientsPerServer: number;

	/**
	 * Fraction of a server's clients that must have an open issue, `0`–`1`. Default `0.5`.
	 *
	 * Typical `0.4`–`0.7`. Remember each finding also carries the *other* servers' ratios, so the
	 * threshold is not doing the comparison on its own — a server at 50% next to peers at 45% reads very
	 * differently from one next to peers at 3%. Below `0.3` you will report servers that are merely
	 * carrying unlucky clients.
	 */
	degradedRatioThreshold: number;

	/**
	 * Which client issue types count as "in trouble". Empty (the default) means **any** open issue.
	 *
	 * The permissive default is deliberate and unusual for this library: the question is not *what* is
	 * wrong with each client but whether trouble clusters on one relay, and a relay problem shows up as
	 * whatever symptom each client happens to notice first. Narrow it to network types
	 * (`congestion`, `ice-disconnected`) if endpoint issues like `cpulimitation` are common enough in
	 * your fleet to blur the comparison between servers.
	 */
	issueTypes: string[];

	/**
	 * Consecutive `observer.update()` ticks the condition must hold before raising. Default `2`.
	 *
	 * The de-bounce. `1` reacts immediately and will fire on a single tick where several clients
	 * happened to be mid-reconnect; `2`–`3` costs a tick or two of delay and removes most of that.
	 * Note this counts *ticks*, not time, so how long it actually waits depends on your sample rate.
	 */
	consecutiveTicks: number;

	/**
	 * Re-arm time per server (ms). Default `60_000`.
	 *
	 * Shorter than the outage detector's, because degradation is a condition you may want re-reported as
	 * it persists or worsens, not a single event. Typical `60_000`–`300_000`.
	 */
	cooldownMs: number;
};

/** The per-server view this detector builds. */
export type TurnServerHealth = {
	serverUrl: string;

	/** Distinct clients whose media is relayed through this server. */
	clients: number;

	/** Of those, how many currently have at least one open issue. */
	degradedClients: number;
	degradedRatio: number;
	affectedClientIds: string[];

	/** The open issue types seen on this server's clients, most common first. */
	issueTypes: string[];
};

/**
 * An **observer-level** detector that groups relayed clients by the TURN server carrying them and
 * compares the servers against each other.
 *
 * Counting TURN usage is not useful on its own; knowing that `turn-eu-1` has 22 of 30 clients in
 * trouble while `turn-eu-2` has 1 of 34 is. Because the comparison spans calls it lives on
 * `observer.detectors` and raises `observer-issue` — one actionable alert instead of fifty
 * per-client ones. Each finding carries the other servers' ratios as context, since "half the
 * clients here are unhappy" only means something relative to the rest of the fleet.
 *
 * Whether a client is in trouble comes from **its own reported issues**, not from thresholds applied
 * here. The client already decides that far better than a server-side rule could; the value this
 * adds is the grouping — the dimension no endpoint can see.
 *
 * For a relay that has stopped serving entirely, see `TurnServerOutageDetector`: this detector needs
 * clients *on* the server to ask how many are unhappy, and an outage takes them away.
 */
export class TurnServerHealthDetector implements Detector {
	public static readonly NAME = 'turn-server-health-detector';

	public readonly name = TurnServerHealthDetector.NAME;

	private readonly _config: TurnServerHealthDetectorConfig;
	private readonly _streaks = new Map<string, number>();
	private readonly _lastRaisedAt = new Map<string, number>();

	/** The per-server rollup computed on the most recent `update()`. */
	public lastServers: TurnServerHealth[] = [];

	public constructor(
		private readonly _observer: Observer,
		config: Partial<TurnServerHealthDetectorConfig> = {},
	) {
		this._config = {
			minClientsPerServer: 5,
			degradedRatioThreshold: 0.5,
			// any open issue: the question is where trouble clusters, not what it is
			issueTypes: [],
			consecutiveTicks: 2,
			cooldownMs: 60_000,
			...config,
		};
	}

	public update(): void {
		const now = Date.now();
		const wanted = new Set(this._config.issueTypes);
		const issuesByClientId = new Map<string, string[]>();

		// Read straight off the registry rather than subscribing as a tracker: this detector asks
		// "any open issue", so a subscription would just re-derive the registry's own set.
		for (const issue of this._observer.activeIssuesRegistry.values()) {
			if (0 < wanted.size && !wanted.has(issue.type)) continue;

			const types = issuesByClientId.get(issue.clientId);

			if (types) types.push(issue.type);
			else issuesByClientId.set(issue.clientId, [ issue.type ]);
		}

		// Compute every server first, so each finding can carry the full cross-server comparison.
		this.lastServers = [ ...this._observer.observedTURN.servers ]
			.map(([ serverUrl, server ]) => this._serverHealth(serverUrl, server.observedPeerConnections, issuesByClientId));

		for (const health of this.lastServers) {
			const serverUrl = health.serverUrl;

			if (health.clients < this._config.minClientsPerServer || health.degradedRatio < this._config.degradedRatioThreshold) {
				this._streaks.delete(serverUrl);
				continue;
			}

			const ticks = (this._streaks.get(serverUrl) ?? 0) + 1;

			this._streaks.set(serverUrl, ticks);

			if (ticks < this._config.consecutiveTicks) continue;
			if (now - (this._lastRaisedAt.get(serverUrl) ?? 0) < this._config.cooldownMs) continue;

			this._lastRaisedAt.set(serverUrl, now);

			const otherServers = this.lastServers
				.filter((server) => server.serverUrl !== serverUrl)
				.map((server) => ({ serverUrl: server.serverUrl, clients: server.clients, degradedRatio: server.degradedRatio }));

			this._observer.addIssue({
				type: TurnServerHealthTypes.turnServerDegraded,
				timestamp: now,
				payload: { ...health, otherServers },
			});
		}

		for (const serverUrl of [ ...this._streaks.keys() ]) {
			if (!this.lastServers.some((server) => server.serverUrl === serverUrl)) this._streaks.delete(serverUrl);
		}
	}

	public close(): void {
		this._streaks.clear();
		this._lastRaisedAt.clear();
		this.lastServers = [];
	}

	private _serverHealth(
		serverUrl: string,
		peerConnections: Map<string, ObservedPeerConnection>,
		issuesByClientId: Map<string, string[]>,
	): TurnServerHealth {
		// A client can hold several relayed peer connections; the unit of comparison is the client.
		const clientIds = new Set<string>();
		const affectedClientIds = new Set<string>();
		const typeCounts = new Map<string, number>();

		for (const peerConnection of peerConnections.values()) {
			const clientId = peerConnection.client.clientId;

			clientIds.add(clientId);

			const types = issuesByClientId.get(clientId);

			if (!types) continue;

			affectedClientIds.add(clientId);
			for (const type of types) typeCounts.set(type, (typeCounts.get(type) ?? 0) + 1);
		}

		return {
			serverUrl,
			clients: clientIds.size,
			degradedClients: affectedClientIds.size,
			degradedRatio: 0 < clientIds.size ? affectedClientIds.size / clientIds.size : 0,
			affectedClientIds: [ ...affectedClientIds ],
			issueTypes: [ ...typeCounts.entries() ].sort((a, b) => b[1] - a[1]).map(([ type ]) => type),
		};
	}
}

```
### TurnServerOutageDetector
[Pinned implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/TurnServerOutageDetector.ts#L125)
```ts
import type { Detector } from './Detector';
import type { Observer } from '../Observer';
import type { ObservedPeerConnection } from '../ObservedPeerConnection';

export const TurnServerOutageTypes = {
	/** One TURN server's relayed population collapsed while the rest of the fleet is fine. */
	turnServerOutage: 'TURN_SERVER_OUTAGE',
} as const;

export type TurnServerOutageDetectorConfig = {

	/**
	 * Clients a server must have been carrying at its peak before its collapse means anything. Default
	 * `5`.
	 *
	 * Below this, one or two people leaving looks like an outage. Sensible range `5`–`50`; the higher it
	 * is the more confident the finding, and the more small deployments go unwatched.
	 */
	minClientsAtPeak: number;

	/**
	 * Fraction of the peak population that must be gone or disrupted. Default `0.8` — an outage is
	 * near-total by definition; partial degradation is `TurnServerHealthDetector`'s question.
	 */
	lossRatioThreshold: number;

	/**
	 * Window the peak population is measured over (ms). Default `120_000`.
	 *
	 * Long enough to span a real outage's onset, short enough that yesterday's peak is not held against
	 * today. Typical `60_000`–`600_000`. Too long and the natural end of a busy period reads as a
	 * collapse; too short and a gradual failure never shows a peak to fall from.
	 */
	peakWindowMs: number;

	/**
	 * Require a healthy **control group** — clients not relayed through this server that are still
	 * connected — before blaming the server. Without this, a call ending, a fleet-wide network
	 * event, or the observer shutting down all look exactly like a TURN outage. Default `true`.
	 */
	requireControlGroup: boolean;

	/**
	 * Clients elsewhere before the control group is worth anything. Default `5`.
	 *
	 * If you run a single TURN server there is never a control group, so with `requireControlGroup: true`
	 * this detector can never fire — which is correct rather than unfortunate: with one relay you cannot
	 * distinguish "the relay died" from "everyone went home". Sensible range `5`–`20`.
	 */
	minControlGroupClients: number;

	/**
	 * Fraction of the control group that must still be healthy, `0`–`1`. Default `0.7`.
	 *
	 * The evidence that the rest of the world is fine. Typical `0.6`–`0.9`. Set it too high and a
	 * concurrent unrelated problem elsewhere masks a real outage; too low and a fleet-wide network event
	 * gets blamed on whichever server lost clients first.
	 */
	controlGroupHealthyRatio: number;

	/**
	 * Consecutive `observer.update()` ticks the condition must hold before raising. Default `2`.
	 *
	 * Counts ticks, not time. `1` will fire on a single tick where a batch of clients happened to be
	 * between samples; `2`–`4` is the useful range for something this consequential to declare.
	 */
	consecutiveTicks: number;

	/**
	 * Re-arm time (ms) per server. Long by default (`300_000`) — an outage is one event, not one
	 * per tick, and a server that stays down would otherwise alert forever.
	 */
	cooldownMs: number;
};

/** ICE / connection states treated as "this client is not currently relaying". */
const brokenStates = new Set([ 'disconnected', 'failed', 'closed' ]);

type PeakEntry = { clients: number, at: number };

/**
 * Detects a **TURN server outage** — a relay that has stopped serving — by watching its client
 * population collapse while the rest of the fleet carries on.
 *
 * This is the case its sibling `TurnServerHealthDetector` structurally *cannot* see, and the
 * distinction is worth being precise about. That detector groups clients by the server relaying them
 * and asks how many are reporting issues. It needs clients on the server to ask the question. When a
 * TURN server goes down completely, allocation fails: existing sessions drop, and new clients never
 * obtain a relay candidate through it at all, so they are never attributed to it. The server's
 * population goes to zero and the health detector falls silent for the worst possible reason — it
 * has nobody left to ask. Degradation makes clients unhappy; an outage makes them *disappear*.
 *
 * So the signal here is absence, measured against the server's own recent peak:
 *
 * - clients gone entirely (their relayed peer connections closed, or they re-negotiated onto a
 *   different path), plus
 * - clients still attributed to the server whose ICE or connection state is `disconnected` /
 *   `failed` / `closed` — the ones mid-collapse, which is what you catch if you look during the
 *   outage rather than after it.
 *
 * ### The control group is the whole design
 *
 * Absence is a dangerous signal: a call ending, everyone going home at 6pm, a fleet-wide network
 * event, and the observer itself shutting down all produce exactly the same collapse. The detector
 * therefore refuses to blame a server unless clients **not** relayed through it are demonstrably
 * still connected — `requireControlGroup`, on by default. "Everyone on `turn-eu-1` vanished" is
 * ambiguous; "everyone on `turn-eu-1` vanished while 200 clients elsewhere are fine" is an outage.
 *
 * That comparison is only available to something watching every call at once, which is why this is
 * an observer-level detector raising `observer-issue` — one alert for the fleet, not one per
 * abandoned call.
 *
 * ### Caveats worth knowing before you tune it
 *
 * Clients that fail over cleanly to a second TURN server still count as lost here, which is
 * correct — the server did stop serving them — but it means a well-configured fleet with automatic
 * failover reports outages that users never felt. That is the intended behaviour: the failover
 * worked *and* the server is down are both true, and you want to know the second one.
 *
 * A genuinely quiet server (last call of the day ends) is suppressed by the control group, not by
 * the collapse test. If you run a small deployment where the control group is routinely below
 * `minControlGroupClients`, this detector will stay quiet — prefer alerting on your TURN server's
 * own health checks there, since a handful of clients cannot distinguish these cases.
 */
export class TurnServerOutageDetector implements Detector {
	public static readonly NAME = 'turn-server-outage-detector';

	public readonly name = TurnServerOutageDetector.NAME;

	private readonly _config: TurnServerOutageDetectorConfig;

	/** serverUrl -> recent population observations, used to derive the windowed peak. */
	private readonly _peaks = new Map<string, PeakEntry[]>();
	private readonly _streaks = new Map<string, number>();
	private readonly _lastRaisedAt = new Map<string, number>();

	public constructor(
		private readonly _observer: Observer,
		config: Partial<TurnServerOutageDetectorConfig> = {},
	) {
		this._config = {
			minClientsAtPeak: 5,
			// an outage is near-total by definition; partial degradation is the health detector's question
			lossRatioThreshold: 0.8,
			peakWindowMs: 120_000,
			// absence without a control group is just quiet
			requireControlGroup: true,
			minControlGroupClients: 5,
			controlGroupHealthyRatio: 0.7,
			consecutiveTicks: 2,
			// one event, not one per tick
			cooldownMs: 300_000,
			...config,
		};
	}

	public update(): void {
		const now = Date.now();
		const servers = [ ...this._observer.observedTURN.servers ];

		// Per-server populations first: the control group for one server is every *other* server's
		// clients plus the non-relayed ones, so all of them have to be known up front.
		const populations = new Map<string, { healthy: Set<string>, broken: Set<string> }>();

		for (const [ serverUrl, server ] of servers) {
			populations.set(serverUrl, this._populationOf(server.observedPeerConnections));
		}

		for (const [ serverUrl, population ] of populations) {
			const live = population.healthy.size;
			const broken = population.broken.size;
			const peak = this._recordAndPeak(serverUrl, live + broken, now);

			if (peak < this._config.minClientsAtPeak) {
				this._streaks.delete(serverUrl);
				continue;
			}

			// Everything the server has lost: gone entirely, or still attributed but not connected.
			const lost = Math.max(0, peak - live);
			const lossRatio = lost / peak;

			if (lossRatio < this._config.lossRatioThreshold) {
				this._streaks.delete(serverUrl);
				continue;
			}

			const control = this._controlGroup(serverUrl, populations);

			if (this._config.requireControlGroup) {
				if (control.total < this._config.minControlGroupClients) {
					this._streaks.delete(serverUrl);
					continue;
				}
				if (control.healthyRatio < this._config.controlGroupHealthyRatio) {
					// Everyone is having a bad time; this is not one server's fault.
					this._streaks.delete(serverUrl);
					continue;
				}
			}

			const ticks = (this._streaks.get(serverUrl) ?? 0) + 1;

			this._streaks.set(serverUrl, ticks);

			if (ticks < this._config.consecutiveTicks) continue;
			if (now - (this._lastRaisedAt.get(serverUrl) ?? 0) < this._config.cooldownMs) continue;

			this._lastRaisedAt.set(serverUrl, now);

			this._observer.addIssue({
				type: TurnServerOutageTypes.turnServerOutage,
				timestamp: now,
				payload: {
					serverUrl,
					peakClients: peak,
					currentClients: live,
					disruptedClients: broken,
					lostClients: lost,
					lossRatio,
					disruptedClientIds: [ ...population.broken ],
					controlGroupClients: control.total,
					controlGroupHealthyClients: control.healthy,
					controlGroupHealthyRatio: control.healthyRatio,
					peakWindowMs: this._config.peakWindowMs,
				},
			});
		}

		// Forget servers that are no longer known at all.
		for (const key of [ ...this._peaks.keys() ]) {
			if (populations.has(key)) continue;
			this._peaks.delete(key);
			this._streaks.delete(key);
		}
	}

	public close(): void {
		this._peaks.clear();
		this._streaks.clear();
		this._lastRaisedAt.clear();
	}

	/** Distinct clients on a server, split by whether their relayed transport is actually up. */
	private _populationOf(peerConnections: Map<string, ObservedPeerConnection>) {
		const healthy = new Set<string>();
		const broken = new Set<string>();

		for (const peerConnection of peerConnections.values()) {
			const clientId = peerConnection.client.clientId;
			const isBroken = peerConnection.closed
				|| brokenStates.has(peerConnection.iceConnectionState ?? '')
				|| brokenStates.has(peerConnection.connectionState ?? '');

			if (isBroken) broken.add(clientId);
			else healthy.add(clientId);
		}

		// A client with one healthy relayed transport is not a casualty, even if another of its
		// peer connections is down.
		for (const clientId of healthy) broken.delete(clientId);

		return { healthy, broken };
	}

	/** Record this tick's population and return the peak across `peakWindowMs`. */
	private _recordAndPeak(serverUrl: string, clients: number, now: number): number {
		const entries = this._peaks.get(serverUrl) ?? [];
		const cutoff = now - this._config.peakWindowMs;
		const kept = entries.filter((e) => cutoff <= e.at);

		kept.push({ clients, at: now });
		this._peaks.set(serverUrl, kept);

		return kept.reduce((max, e) => Math.max(max, e.clients), 0);
	}

	/**
	 * Everyone *not* relayed through `serverUrl`: clients on other TURN servers plus every client
	 * the observer knows about that isn't relayed at all. The healthy share of that group is what
	 * separates "this server broke" from "everything broke".
	 */
	private _controlGroup(serverUrl: string, populations: Map<string, { healthy: Set<string>, broken: Set<string> }>) {
		const healthy = new Set<string>();
		const broken = new Set<string>();

		for (const [ otherUrl, population ] of populations) {
			if (otherUrl === serverUrl) continue;
			for (const clientId of population.healthy) healthy.add(clientId);
			for (const clientId of population.broken) broken.add(clientId);
		}

		// Non-relayed clients count as control too: they are the cleanest evidence that the
		// observer is still receiving samples and the world at large is fine.
		const onThisServer = populations.get(serverUrl);

		for (const call of this._observer.observedCalls.values()) {
			for (const client of call.observedClients.values()) {
				if (onThisServer?.healthy.has(client.clientId) || onThisServer?.broken.has(client.clientId)) continue;
				if (broken.has(client.clientId)) continue;
				healthy.add(client.clientId);
			}
		}

		for (const clientId of healthy) broken.delete(clientId);

		const total = healthy.size + broken.size;

		return {
			total,
			healthy: healthy.size,
			healthyRatio: 0 < total ? healthy.size / total : 0,
		};
	}
}

```
### UnconsumedTrackDetector
[Pinned implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/UnconsumedTrackDetector.ts#L62)
```ts
import type { Detector } from './Detector';
import type { ObservedCall } from '../ObservedCall';

export const UnconsumedTrackTypes = {
	/** A track is being published to the SFU that nobody is subscribed to — pure wasted uplink. */
	unconsumedPublishedTrack: 'UNCONSUMED_PUBLISHED_TRACK',
} as const;

export type UnconsumedTrackDetectorConfig = {

	/**
	 * How long a track must stay unconsumed **while still sending** before it is reported (ms).
	 * Default `30_000`.
	 *
	 * This is the main guard against a false alarm, because a gap between publishing and the first
	 * subscription is completely normal at join time — and again after every renegotiation. Sensible
	 * range `15_000`–`120_000`. Too low and you report every join; too high and you tolerate wasted
	 * uplink for longer than you need to. Waste is not an outage, so err high.
	 */
	minUnconsumedDurationInMs: number;

	/**
	 * Ignore tracks sending below this bitrate (**bits per second**). Default `50_000` (50 kbps).
	 *
	 * The point of the detector is wasted bandwidth, and a track trickling keep-alive packets wastes
	 * none worth an alert. Typical `20_000`–`100_000`: muted or paused tracks sit near zero, a real
	 * video track is hundreds of kbps. Set it to `0` to report every unconsumed track regardless of
	 * cost.
	 */
	minBitrate: number;

	/**
	 * Re-arm time per track (ms). Default `300_000`.
	 *
	 * Long on purpose: an unconsumed track usually *stays* unconsumed, so a short cooldown means a
	 * steady drip of the same finding for the life of the call. Typical `300_000`–`900_000`.
	 */
	cooldownMs: number;
};

/**
 * Finds tracks that are **published but consumed by nobody** — uplink and SFU ingress spent on media
 * that is never forwarded anywhere.
 *
 * This is the one detector that reads the resolver's *silence* as the signal: an outbound track with
 * an empty `remoteInboundTracks` set, still pushing packets. It reads `call.unconsumedOutboundTracks`,
 * which the resolver maintains as tracks gain and lose subscribers, so a healthy call costs one
 * `size === 0` check rather than a walk over every published track. The usual causes are a participant
 * publishing while everyone has them hidden or muted-in-UI, a simulcast layer no viewer's bandwidth
 * ever selects, or an application that forgot to stop a track after the last subscriber left.
 *
 * It is deliberately slow to fire: `minUnconsumedDurationInMs` must elapse with the track still
 * sending, because a brief gap between publishing and the first subscription is completely normal at
 * join time.
 *
 * ### Careful: this detector is only sound with a resolver
 *
 * "No subscribers" and "no resolver configured" produce the identical observation — an empty link
 * set. Without a `RemoteTrackResolver` this would report *every* published track in the call as
 * unconsumed, so it checks `call.remoteTrackResolver` at runtime and does nothing without one.
 */
export class UnconsumedTrackDetector implements Detector {
	public static readonly NAME = 'unconsumed-track-detector';
	public readonly name = UnconsumedTrackDetector.NAME;

	public readonly config: UnconsumedTrackDetectorConfig;

	/** trackId -> when it was first seen sending with no subscribers. */
	private readonly _unconsumedSince = new Map<string, number>();
	private readonly _lastRaisedAt = new Map<string, number>();

	public constructor(
		private readonly call: ObservedCall,
		config: Partial<UnconsumedTrackDetectorConfig> = {},
	) {
		this.config = {
			cooldownMs: 300_000,
			minUnconsumedDurationInMs: 30_000,
			minBitrate: 50_000,
			...config,
		};
	}

	public update(): void {
		// Without links, "no subscribers" is unknowable — never guess.
		if (!this.call.remoteTrackResolver) return;

		const unconsumed = this.call.unconsumedOutboundTracks;

		// The common case: every published track has a subscriber, so there is nothing to look at.
		// The set is maintained by the resolver at the two moments the answer can change (a track
		// gains its first subscriber, or loses its last), so this costs nothing on a healthy call
		// rather than a walk over every published track in it.
		if (unconsumed.size === 0) {
			if (0 < this._unconsumedSince.size) this._unconsumedSince.clear();

			return;
		}

		const now = Date.now();
		const seen = new Set<string>();

		for (const outboundTrack of unconsumed) {
			const rtps = outboundTrack.getOutboundRtps() ?? [];
			let bitrate = 0;
			let sending = false;

			for (let i = 0; i < rtps.length; i++) {
				bitrate += rtps[i].bitrate;
				if (0 < rtps[i].deltaPacketsSent) sending = true;
			}

			seen.add(outboundTrack.id);

			if (!sending || bitrate < this.config.minBitrate) {
				this._unconsumedSince.delete(outboundTrack.id);
				continue;
			}

			const since = this._unconsumedSince.get(outboundTrack.id) ?? now;

			this._unconsumedSince.set(outboundTrack.id, since);

			const unconsumedForMs = now - since;

			if (unconsumedForMs < this.config.minUnconsumedDurationInMs) continue;
			if (now - (this._lastRaisedAt.get(outboundTrack.id) ?? 0) < this.config.cooldownMs) continue;

			this._lastRaisedAt.set(outboundTrack.id, now);

			const peerConnection = outboundTrack.getPeerConnection();

			this.call.addIssue({
				type: UnconsumedTrackTypes.unconsumedPublishedTrack,
				timestamp: now,
				payload: {
					trackId: outboundTrack.id,
					kind: outboundTrack.kind,
					publisherClientId: peerConnection?.client.clientId,
					peerConnectionId: peerConnection?.peerConnectionId,
					bitrate,
					unconsumedForMs,
					// what the waste costs, roughly, if it continues
					wastedBytesPerSecond: bitrate / 8,
				},
			});
		}

		for (const trackId of [ ...this._unconsumedSince.keys() ]) {
			if (!seen.has(trackId)) this._unconsumedSince.delete(trackId);
		}
	}

	public close(): void {
		this._unconsumedSince.clear();
		this._lastRaisedAt.clear();
	}
}

```