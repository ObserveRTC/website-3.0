---
title: "Monitors & derived metrics"
slug: "metrics"
description: "The monitor object graph and every metric computed from raw WebRTC stats"
lead: "What the library computes for you, and where to find it"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 316
toc: true
---

`getStats()` returns a flat map of records joined by string ids, containing monotonically
increasing counters. The monitor turns that into a navigable object graph with per-interval
metrics already computed.

## The monitor hierarchy

```text
ClientMonitor
├── PeerConnectionMonitor[]
│   ├── InboundRtpMonitor[]
│   ├── OutboundRtpMonitor[]
│   ├── RemoteInboundRtpMonitor[]
│   ├── RemoteOutboundRtpMonitor[]
│   ├── MediaSourceMonitor[]
│   ├── MediaPlayoutMonitor[]
│   ├── CodecMonitor[]
│   ├── IceTransportMonitor[]
│   ├── IceCandidateMonitor[]
│   ├── IceCandidatePairMonitor[]
│   ├── CertificateMonitor[]
│   └── DataChannelMonitor[]
├── InboundTrackMonitor[]
└── OutboundTrackMonitor[]
```

Track monitors sit at the client level rather than under a peer connection, because that is how
applications think about them — "Alice's camera" is one thing, even when it is carried by three
simulcast RTP streams.

### Navigating

```javascript
monitor.peerConnections;                    // PeerConnectionMonitor[]
monitor.tracks;                             // (InboundTrackMonitor | OutboundTrackMonitor)[]
monitor.getTrackMonitor(track.id);          // by MediaStreamTrack id

track.getInboundRtp();                      // inbound track → its RTP monitor
track.getOutboundRtps();                    // outbound track → all simulcast layers
track.getHighestLayer();                    // outbound track → the top layer

outboundRtp.getRemoteInboundRtp();          // what the far end reports about this stream
outboundRtp.getMediaSource();               // the local capture feeding it

pcMonitor.mappedInboundRtpMonitors;
pcMonitor.mappedOutboundRtpMonitors;
pcMonitor.mappedIceCandidatePairMonitors;
pcMonitor.mappedDataChannelMonitors;
```

## Client-level metrics

Available directly on `ClientMonitor`, aggregated across every peer connection:

```javascript
// Bitrates (bits per second)
monitor.sendingAudioBitrate;
monitor.sendingVideoBitrate;
monitor.receivingAudioBitrate;
monitor.receivingVideoBitrate;

// Network capacity, from the selected candidate pairs
monitor.totalAvailableIncomingBitrate;
monitor.totalAvailableOutgoingBitrate;

// Quality
monitor.avgRttInSec;                    // average RTT across connections
monitor.score;                          // 0.0–5.0
monitor.scoreReasons;

// Self-observation
monitor.durationOfCollectingStatsInMs;  // how long the last getStats() pass took
```

{{< callout context="tip" title="durationOfCollectingStatsInMs is a CPU signal" icon="rocket" >}}
`getStats()` runs on the main thread. When it starts taking seconds instead of milliseconds, the
tab is saturated — which is exactly why `CpuPerformanceDetector` watches this number alongside
encoder and decoder signals.
{{< /callout >}}

## Peer connection metrics

```javascript
// Bitrates by media type
pc.sendingAudioBitrate;
pc.sendingVideoBitrate;
pc.receivingAudioBitrate;
pc.receivingVideoBitrate;

// Loss
pc.outboundFractionLost;
pc.inboundFractionalLost;

// Per-interval deltas
pc.deltaInboundPacketsLost;
pc.deltaInboundPacketsReceived;
pc.deltaOutboundPacketsSent;
pc.deltaAudioBytesSent;
pc.deltaVideoBytesSent;
pc.deltaDataChannelBytesSent;

// RTT and timing
pc.avgRttInSec;
pc.ewmaRttInSec;                 // smoothed
pc.connectingStartedAt;
pc.connectedAt;

// Topology
pc.usingTURN;                    // relayed
pc.usingTCP;                     // TCP transport rather than UDP
pc.iceState;

// Historical peaks (never reset)
pc.highestSeenSendingBitrate;
pc.highestSeenReceivingBitrate;
pc.highestSeenAvailableIncomingBitrate;
pc.highestSeenAvailableOutgoingBitrate;
```

{{< callout context="note" title="Why the peaks matter" icon="info-circle" >}}
`highestSeenAvailableOutgoingBitrate` gives you a per-session ceiling to compare the current
estimate against. "Available bandwidth is 400 kbps" means nothing on its own; "available bandwidth
is 400 kbps having peaked at 3 Mbps ten seconds ago" is a congestion event.
{{< /callout >}}

## Track metrics

### Inbound

```javascript
track.track;           // the underlying MediaStreamTrack
track.kind;            // 'audio' | 'video'
track.direction;       // 'inbound'
track.bitrate;         // receiving bitrate (bps)
track.jitter;          // seconds
track.fractionLost;    // 0..1
track.dtxMode;         // discontinuous transmission
track.score;           // 0.0–5.0
track.scoreReasons;
track.detectors;       // attached detectors
```

### Outbound

```javascript
track.track;                      // the underlying MediaStreamTrack
track.bitrate;                    // aggregate across simulcast layers
track.sendingPacketRate;
track.remoteReceivedPacketRate;   // from RTCP receiver reports
track.jitter;                     // as reported by the remote peer
track.fractionLost;               // as reported by the remote peer
track.score;

track.getHighestLayer();
track.getOutboundRtps();
```

## RTP-level metrics

### InboundRtpMonitor

```javascript
// Rates
rtp.bitrate;
rtp.packetRate;
rtp.fractionLost;
rtp.bitPerPixel;                    // video coding efficiency

// Video
rtp.avgFramesPerSec;
rtp.ewmaFps;                        // smoothed
rtp.fpsVolatility;                  // lower is more stable
rtp.isFreezed;

// Audio
rtp.receivingAudioSamples;
rtp.desync;

// Per-interval deltas
rtp.deltaPacketsLost;
rtp.deltaPacketsReceived;
rtp.deltaBytesReceived;
rtp.deltaJitterBufferDelay;
rtp.deltaFramesDecoded;
rtp.deltaFramesReceived;
rtp.deltaFramesRendered;
rtp.deltaCorruptionProbability;
rtp.deltaTime;                      // ms covered by these deltas
```

### OutboundRtpMonitor

```javascript
rtp.bitrate;               // total, including headers and retransmissions
rtp.payloadBitrate;        // payload only
rtp.packetRate;
rtp.bitPerPixel;

rtp.deltaPacketsSent;
rtp.deltaBytesSent;
```

{{< callout context="tip" title="bitrate vs payloadBitrate" icon="rocket" >}}
The gap between them is your overhead: RTP headers plus retransmissions. A widening gap under
constant `payloadBitrate` means loss is forcing retransmissions — visible before quality drops.
{{< /callout >}}

### Remote RTP monitors

```javascript
remoteInbound.packetRate;        // what the far end is receiving
remoteInbound.deltaPacketsLost;  // what the far end lost this interval

remoteOutbound.bitrate;          // what the far end says it is sending
```

## ICE and transport metrics

```javascript
iceTransport.sendingBitrate;
iceTransport.receivingBitrate;
iceTransport.deltaPacketsSent;
iceTransport.deltaPacketsReceived;
iceTransport.deltaBytesSent;
iceTransport.deltaBytesReceived;

candidatePair.availableIncomingBitrate;   // the browser's bandwidth estimate
candidatePair.availableOutgoingBitrate;

iceTransport.selectedCandidatePair;
```

## Data channel and playout metrics

```javascript
dataChannel.deltaBytesSent;
dataChannel.deltaBytesReceived;

mediaPlayout.deltaSynthesizedSamplesDuration;   // audio the browser had to invent
mediaPlayout.deltaSamplesDuration;
```

The ratio of those two is the cleanest available audio-gap indicator: if 8 % of playout duration
was synthesized, the user heard artefacts regardless of what the packet-loss number says.

## Reading metrics in practice

```javascript
monitor.on("stats-collected", () => {
    // Client-level summary.
    const totalSending = monitor.sendingAudioBitrate + monitor.sendingVideoBitrate;

    for (const pc of monitor.peerConnections) {
        console.log(`PC ${pc.peerConnectionId}`, {
            rttMs: (pc.avgRttInSec ?? 0) * 1000,
            turn: pc.usingTURN,
            headroom: pc.highestSeenAvailableOutgoingBitrate - pc.sendingVideoBitrate,
        });
    }

    // Per-track video quality.
    for (const track of monitor.tracks) {
        if (track.kind !== "video" || track.direction !== "inbound") continue;
        const rtp = track.getInboundRtp();
        console.log(track.track.id, {
            bitrate: rtp?.bitrate,
            fps: rtp?.ewmaFps,
            volatility: rtp?.fpsVolatility,
            loss: rtp?.fractionLost,
        });
    }
});
```

## `attachments` and `appData` on monitors

Every monitor in the hierarchy carries both bags. `attachments` ships with the sample;
`appData` never leaves the browser.

```javascript
// Reaches your backend — this is how a server knows what a track is.
trackMonitor.attachments = {
    roomId: "room-456",
    participantRole: "presenter",
    mediaType: "screen-share",
    producerId: producer.id,
};

// Stays local.
trackMonitor.appData = {
    videoElementId: "tile-7",
    localProcessingFlags: { enableBlur: true },
};
```

See [`ClientSample`](/docs/schema/clientsample/) for how attachments appear on the wire, and
[Remote track resolution](/docs/libraries/observer-js/sfu/) for what a server can do with them.
