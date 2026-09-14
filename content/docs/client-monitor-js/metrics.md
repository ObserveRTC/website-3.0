---
title: "Monitors & derived metrics"
description: "The object graph and every computed field on it"
lead: "The monitors compute the facts; the detectors hold the opinions about them"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 260
toc: true
---

Every derived value is a property of the stats — a bitrate, a mean, a delta — and is published
whether or not any detector reads it.

Three conventions run through all of them:

- **A value the browser did not report is `undefined`, never `0`.** "Nothing arrived" and "nothing
  was lost" must not look the same.
- **Means exclude streams that carried nothing this tick** rather than counting them as healthy.
- **Every duration is stats time**, aged on the gaps between stats reports rather than on
  `Date.now()`.

## The monitor tree

```text
ClientMonitor
└── PeerConnectionMonitor
    ├── InboundTrackMonitor / OutboundTrackMonitor
    ├── InboundRtpMonitor / OutboundRtpMonitor
    ├── RemoteInboundRtpMonitor / RemoteOutboundRtpMonitor
    ├── IceTransportMonitor → IceCandidatePairMonitor → IceCandidateMonitor
    ├── CodecMonitor, MediaSourceMonitor, MediaPlayoutMonitor
    ├── DataChannelMonitor, CertificateMonitor
    └── PeerConnectionTransportMonitor
```

### Reaching a monitor

Every collection getter returns a **fresh array**, so hold the result rather than calling it in a
loop.

```typescript
monitor.peerConnections;      // PeerConnectionMonitor[]
monitor.tracks;               // TrackMonitor[] — both directions, every connection
monitor.inboundRtps;
monitor.outboundRtps;
monitor.remoteInboundRtps;
monitor.remoteOutboundRtps;
monitor.iceTransports;
monitor.codecs;
monitor.certificates;

monitor.getPeerConnectionMonitor(peerConnectionId);
monitor.getTrackMonitor(trackId);                    // either direction
monitor.mappedPeerConnections;                       // the underlying Map, to iterate without allocating

const pc = monitor.peerConnections[0];
pc.getTrackMonitor(trackId);
pc.getInboundTrackMonitor(trackId);
pc.getOutboundTrackMonitor(trackId);
```

### Walking the graph

`getStats()` reports a flat list of objects that reference each other by id. The monitors resolve
those joins once, so *"what codec is this inbound stream using, and which ICE transport carries
it?"* is two property accesses. Every accessor returns `undefined` when the browser did not report
the link, or when the object it points at has gone away.

| From | Accessor | To |
|---|---|---|
| any monitor | `getPeerConnection()` | `PeerConnectionMonitor` |
| `InboundRtpMonitor` | `getTrack()` | `InboundTrackMonitor` |
| | `getCodec()` | `CodecMonitor` |
| | `getRemoteOutboundRtp()` | the sender's own view |
| | `getMediaPlayout()` | `MediaPlayoutMonitor` |
| | `getIceTransport()`, `getSelectedCandidatePair()` | the path carrying it |
| `OutboundRtpMonitor` | `getTrack()`, `getCodec()`, `getMediaSource()` | |
| | `getRemoteInboundRtp()` | the receiver's report about us |
| | `getIceTransport()`, `getSelectedCandidatePair()` | as above |
| `InboundTrackMonitor` | `getInboundRtp()` | `InboundRtpMonitor` |
| | `getLinkedVideoTrack()` | the video track this audio track is paired with |
| `OutboundTrackMonitor` | `getMediaSource()` | `MediaSourceMonitor` |
| | `getOutboundRtps()` | one per simulcast layer |
| | `highestLayer` | the layer carrying the most bits |
| `MediaSourceMonitor` | `getTrack()`, `getOutboundRtps()` | the track and its layers |
| `IceTransportMonitor` | `getSelectedCandidatePair()`, `getSelectedIcePath()` | |
| | `getInboundRtps()`, `getOutboundRtps()` | the streams attributed to this transport |
| `IceCandidatePairMonitor` | `getLocalCandidate()`, `getRemoteCandidate()` | `IceCandidateMonitor` |
| `RemoteInboundRtpMonitor` | `getOutboundRtp()` | the local stream it reports on |
| `RemoteOutboundRtpMonitor` | `getInboundRtp()` | the local stream it describes |

```typescript
const track = monitor.getTrackMonitor(trackId);
const rtp = track?.direction === 'inbound' ? track.getInboundRtp() : undefined;

const codec = rtp?.getCodec()?.mimeType;               // 'video/VP8'
const pair = rtp?.getSelectedCandidatePair();
const relayed = pair?.getRemoteCandidate()?.candidateType === 'relay';
const senderView = rtp?.getRemoteOutboundRtp();        // what the far end says it sent
```

{{< callout context="caution" title="Renamed in 4.9" icon="alert-triangle" >}}
`OutboundTrackMonitor.getHighestLayer()` is now the property `highestLayer`.
`PeerConnectionMonitor.attributeRtpToTransport()` is withdrawn — `hasInboundMedia`,
`hasInboundVideo` and `hasOutboundMedia` answer what the detectors used it for, and
`IceTransportMonitor.getInboundRtps()` / `getOutboundRtps()` are a plain `transportId` lookup.
{{< /callout >}}

## Client level

```javascript
monitor.sendingAudioBitrate;      // bps, aggregated across every peer connection
monitor.sendingVideoBitrate;
monitor.receivingAudioBitrate;
monitor.receivingVideoBitrate;

monitor.totalAvailableIncomingBitrate;
monitor.totalAvailableOutgoingBitrate;

monitor.avgRttInSec;                      // mean across connections
monitor.score;                            // 0.0–5.0, undefined until it settles
monitor.scoreReasons;                     // this entity's own subtractions
monitor.cpuUtilization;                   // the reading behind `cpulimitation`, published either way
monitor.durationOfCollectingStatsInMs;    // how long the collection took — wall clock, on purpose
monitor.createdAt;  monitor.uptimeInMs;   // how long this monitor has been running
monitor.activeTab;                        // false while the tab is backgrounded
```

## Peer connection level

```javascript
pc.sendingAudioBitrate;  pc.sendingVideoBitrate;
pc.receivingAudioBitrate; pc.receivingVideoBitrate;

// Means over the streams that actually carried packets this tick — `undefined`
// rather than 0 when none did.
pc.avgInboundFractionLost;      // mean interval inbound loss fraction (0..1)
pc.avgOutboundFractionLost;     // mean loss the far end reported for what we send
pc.avgInboundJitterInMs;        // published deliberately without a detector

// Sums kept for backwards compatibility
pc.outboundFractionLost;  pc.inboundFractionalLost;

// Round trip — two different measurements, never blended
pc.avgRttInSec;                 // rtcpRttInSec ?? iceRttInSec
pc.ewmaRttInSec;                // EWMA of whichever of those is reporting (α = 0.1)

// Pacer and jitter-buffer facts the capacity detectors read
pc.avgPacketSendDelayInMs;
pc.avgInboundVideoJitterBufferDelayInMs;
pc.availableOutgoingBitrate;    // undefined where no selected pair reported one
pc.qualityLimitationReason;     // most limiting reason across streams that sent something

// Deltas
pc.deltaInboundPacketsLost;  pc.deltaInboundPacketsReceived;
pc.deltaOutboundPacketsSent;
pc.deltaAudioBytesSent;  pc.deltaVideoBytesSent;  pc.deltaDataChannelBytesSent;

// Stats time, not wall clock: this collection's newest timestamp minus the previous one's.
pc.deltaTime;
pc.statsClockTime;              // accumulated stats time — the clock every window is aged on

// Topology and state
pc.usingTURN;  pc.usingTCP;  pc.iceState;
pc.connectingStartedAt;  pc.connectedAt;
pc.congested;  pc.uplinkCongested;  pc.downlinkCongested;
pc.hasInboundMedia;  pc.hasInboundVideo;  pc.hasOutboundMedia;
pc.selectedIcePath;  pc.selectedIcePaths;
pc.issues;                      // the IssueRegistry for this peer connection
pc.slicedWindow;                // the shared window every pc-level detector reads
pc.calculatedStabilityScore;    // { value, reasons, weight }
```

{{< callout context="note" title="Withdrawn in 4.9" icon="info-circle" >}}
`highestSeenSendingBitrate`, `highestSeenReceivingBitrate`, `highestSeenAvailableIncomingBitrate`
and `highestSeenAvailableOutgoingBitrate` are gone. The congestion detectors hold their own
`DecayingMaxEstimator`, which **forgets** — a rolling maximum that never decays holds a finding open
against a peak the path no longer reaches.
{{< /callout >}}

## Track level

```javascript
// Inbound
inboundTrack.bitrate;  inboundTrack.jitter;  inboundTrack.fractionLost;
inboundTrack.calculatedScore;      // { value, reasons, weight }
inboundTrack.issues;               // this track's IssueRegistry
inboundTrack.slicedWindow;
inboundTrack.frameFlowState;       // 'continuous' | 'choppy' | 'frozen'
inboundTrack.decodeBudgetUtilization;
inboundTrack.quantizationDegradation;
inboundTrack.displayMagnification; // sqrt(presented area / decoded area), unbounded
inboundTrack.linkedVideoPlayoutDiffInMs;
inboundTrack.contentType;  inboundTrack.motionType;   // read-only getters over the declared context
inboundTrack.presentedResolution;  inboundTrack.videoTag;
inboundTrack.paused;  inboundTrack.remoteOutboundTrackPaused;

// Outbound
outboundTrack.bitrate;
outboundTrack.sendingPacketRate;
outboundTrack.remoteReceivedPacketRate;
outboundTrack.jitter;  outboundTrack.fractionLost;    // as the far end reported them
outboundTrack.highestLayer;                            // was getHighestLayer()
outboundTrack.settings;  outboundTrack.videoCaptureSettingsChanged;
outboundTrack.calculatedScore;  outboundTrack.issues;
```

The context fields are **read-only getters** as of 4.9 — write them with
`ClientMonitor.setInboundTrackContext()` / `setOutboundTrackContext()`, or `trackMonitor.setContext()`.

## Inbound RTP

```javascript
// Rates
inboundRtp.bitrate;  inboundRtp.packetRate;  inboundRtp.fractionLost;
inboundRtp.bitPerPixel;                 // bitrate / (width × height × fps)

// Video timing
inboundRtp.avgFramesPerSec;
inboundRtp.ewmaFps;
inboundRtp.interFrameDelayVariation;    // frame-timing stability (lower is better)
inboundRtp.fpsVolatility;               // deprecated: prefer interFrameDelayVariation

// Audio — the "how did it sound" set
inboundRtp.inventedSpeechRatio;         // share NetEQ invented this interval — silence excluded
inboundRtp.concealmentEventRate;
inboundRtp.timeStretchRate;             // share of samples stretched or compressed
inboundRtp.avgJitterBufferDelayInMs;    // latency the buffer actually added, per sample
inboundRtp.jitterBufferTargetDelayInMs; // what NetEQ is aiming for
inboundRtp.discardRate;                 // packets that arrived too late to use
inboundRtp.estimatedPlayoutTimestamp;   // the sender's NTP time of the last playable sample

// Video decode cost and recovery pressure
inboundRtp.decodeTimePerFrameInMs;
inboundRtp.droppedFrameRatio;           // this interval's share (was `dropRatio`)
inboundRtp.renderRatio;                 // frames rendered vs decoded
inboundRtp.keyFrameRate;  inboundRtp.pliRate;  inboundRtp.firRate;  inboundRtp.nackRate;
inboundRtp.retransmissionRatio;
inboundRtp.avgQpPerFrame;

// Deltas
inboundRtp.deltaPacketsLost;  inboundRtp.deltaPacketsReceived;  inboundRtp.deltaBytesReceived;
inboundRtp.deltaFramesReceived;  inboundRtp.deltaFramesDecoded;  inboundRtp.deltaFramesRendered;
inboundRtp.deltaKeyFramesDecoded;  inboundRtp.deltaPliCount;
inboundRtp.deltaJitterBufferDelay;  inboundRtp.deltaCorruptionProbability;
inboundRtp.deltaTime;
```

{{< callout context="caution" title="Renamed and removed in 4.9" icon="alert-triangle" >}}
`concealmentRate` → **`inventedSpeechRatio`**, and it now excludes silent concealment.
`dropRatio` → **`droppedFrameRatio`**, and it is this interval's share rather than the call's.
`isFreezed` is gone — `InboundVideoFlowStateDetector` owns the verdict and publishes it as
`InboundTrackMonitor.frameFlowState`.
{{< /callout >}}

> Every delta is **counter-reset safe**: a counter that goes backwards (SSRC reuse, an ICE restart,
> a stats-object replacement) yields `0` rather than a negative value, so no rate derived from it
> can go negative. `packetsLost` legitimately *decreases* when a late packet arrives, so the guard
> is not merely defensive there.

## Outbound RTP

```javascript
outboundRtp.bitrate;
outboundRtp.payloadBitrate;             // excludes headers and retransmissions
outboundRtp.packetRate;
outboundRtp.bitPerPixel;

outboundRtp.encodeTimePerFrameInMs;     // the most direct send-side CPU signal
outboundRtp.avgQpPerFrame;
outboundRtp.avgPacketSendDelayInMs;     // per-packet pacer delay
outboundRtp.retransmissionRatio;  outboundRtp.retransmittedPacketRatio;
outboundRtp.keyFrameRate;  outboundRtp.nackRate;  outboundRtp.pliRate;  outboundRtp.firRate;

// What the encoder spent THIS interval doing, 0..1 — unlike the raw
// qualityLimitationDurations accumulators, this can be compared to a threshold.
outboundRtp.qualityLimitationDurationShares;
// => { none: 0.25, cpu: 0.75, bandwidth: 0, other: 0 }

outboundRtp.deltaPacketsSent;  outboundRtp.deltaBytesSent;  outboundRtp.deltaFramesEncoded;
```

## Remote RTP

```javascript
// Remote inbound — what the far end reports about the stream we send
remoteInboundRtp.packetRate;
remoteInboundRtp.deltaPacketsLost;
remoteInboundRtp.deltaFractionLost;
remoteInboundRtp.avgRoundTripTimeInSec;   // totalRoundTripTime / roundTripTimeMeasurements
                                          // — `roundTripTime` alone is one noisy measurement

// Remote outbound — what the far end reports about the stream we receive
remoteOutboundRtp.bitrate;
remoteOutboundRtp.deltaPacketsSent;
```

## ICE transport, candidate pairs and data channels

```javascript
iceTransport.sendingBitrate;  iceTransport.receivingBitrate;
iceTransport.deltaBytesSent;  iceTransport.deltaBytesReceived;
iceTransport.deltaPacketsSent;  iceTransport.deltaPacketsReceived;
iceTransport.deltaSelectedCandidatePairChanges;   // from the browser's own counter, where reported
iceTransport.everConnected;                       // latched the first time it read connected
iceTransport.detectors;                           // the three Blocked* detectors live here

candidatePair.availableIncomingBitrate;
candidatePair.availableOutgoingBitrate;
candidatePair.deltaResponsesReceived;             // the STUN consent counter
candidatePair.tuple;                              // local:port:remote:port:protocol

dataChannel.deltaBytesSent;  dataChannel.deltaBytesReceived;
```

## Media source and playout

```javascript
mediaSource.deltaFrames;      // frames the capture source produced this interval
mediaSource.sourceFps;        // …as a rate — compare against what the encoder managed
mediaSource.rmsAudioLevel;    // RMS over the interval, from totalAudioEnergy — unlike
                              // `audioLevel` it does not read zero between words
mediaSource.getOutboundRtps();

mediaPlayout.deltaSynthesizedSamplesDuration;
mediaPlayout.deltaSamplesDuration;
mediaPlayout.synthesizedSamplesRatio;      // synthesized share of the interval, 0..1
mediaPlayout.playoutDelayPerSampleInMs;    // `totalPlayoutDelay` grows forever; this can be
                                           // compared to a threshold
```

## Extension stats

Anything your application measures can be folded into the monitor tree and read back off it.

```typescript
monitor.addExtensionStats({
    type: 'render-stats',
    id: 'tile-42',                  // giving an id is what makes it readable back
    payload: { droppedFrames: 3, canvasFps: 24 },
});

monitor.getExtensionStatsPayload<{ droppedFrames: number }>('tile-42')?.droppedFrames;  // 3
monitor.getExtensionStatsMonitor('tile-42')?.timestamp;
monitor.mappedExtensionStatsMonitors;
```

**It is a current-value store, not a history.** Each id holds only the most recent payload, and a
monitor is dropped one collection after the id stops being reported. To report every collection
without wiring a timer, register a provider — providers are awaited as part of each collection, so
their values land in the same tick as the `getStats()` they sit beside:

```typescript
monitor.extensionStatsProviders.add(async () => ({
    type: 'render-stats',
    id: 'tile-42',
    payload: { canvasFps: renderer.fps },
}));
```

## Reading them

```javascript
monitor.on('stats-collected', () => {
    console.log('sending:', monitor.sendingAudioBitrate + monitor.sendingVideoBitrate);

    for (const pc of monitor.peerConnections) {
        console.log(pc.peerConnectionId, 'RTT', (pc.avgRttInSec ?? 0) * 1000, 'ms');

        for (const track of pc.mappedInboundTracks.values()) {
            if (track.kind !== 'video') continue;
            const rtp = track.getInboundRtp();
            console.log('fps', rtp?.ewmaFps, 'bpp', rtp?.bitPerPixel, 'flow', track.frameFlowState);
        }
    }
});
```
