---
title: "ClientSample"
description: "ClientSample schema definition and field reference"
lead: "Complete reference for ClientSample schema structure and fields based on schema version 3.0.0"
date: 2024-01-15T10:00:00+02:00
lastmod: 2024-01-15T10:00:00+02:00
draft: false
weight: 220
toc: true
---

## ClientSample

The `ClientSample` is the primary schema for WebRTC monitoring data collected from clients. It contains comprehensive statistics and metadata about WebRTC sessions, extending the WebRTC W3C Stats API standard with additional context for observability and analytics.

**Schema Version**: 3.0.0

### Core Structure

The ClientSample follows a hierarchical structure with PeerConnectionSample containing nested arrays of different statistics types:

```
ClientSample
├── Basic Metadata (timestamp, callId, clientId, attachments, score)
├── peerConnections[] (PeerConnectionSample)
│   ├── inboundTracks[]
│   ├── outboundTracks[]
│   ├── codecs[]
│   ├── inboundRtps[]
│   ├── remoteInboundRtps[]
│   ├── outboundRtps[]
│   ├── remoteOutboundRtps[]
│   ├── mediaSources[]
│   ├── mediaPlayouts[]
│   ├── peerConnectionTransports[]
│   ├── dataChannels[]
│   ├── iceTransports[]
│   ├── iceCandidates[]
│   ├── iceCandidatePairs[]
│   └── certificates[]
├── clientEvents[]
├── clientIssues[]
├── clientMetaItems[]
└── extensionStats[]
```

## ClientSample

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp the sample is created in GMT |
| `callId` | `string` (optional) | The unique identifier of the call or session |
| `clientId` | `string` (optional) | Unique id of the client providing samples |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this sample (e.g.: roomId, userId, displayName, etc...) |
| `score` | `number` (optional) | Calculated score for client (details should be added to attachments) |
| `peerConnections` | `PeerConnectionSample[]` (optional) | Samples taken from PeerConnections |
| `clientEvents` | `ClientEvent[]` (optional) | A list of client events |
| `clientIssues` | `ClientIssue[]` (optional) | A list of client issues |
| `clientMetaItems` | `ClientMetaData[]` (optional) | A list of additional client events |
| `extensionStats` | `ExtensionStat[]` (optional) | The WebRTC app provided custom stats payload |

---

## PeerConnectionSample

Represents a WebRTC peer connection and contains all its associated statistics.

| Field | Type | Description |
|-------|------|-------------|
| `peerConnectionId` | `string` | Unique identifier of the stats object |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this sample |
| `score` | `number` (optional) | Calculated score for peer connection (details should be added to attachments) |
| `inboundTracks` | `InboundTrackSample[]` (optional) | Inbound Track Stats items |
| `outboundTracks` | `OutboundTrackSample[]` (optional) | Outbound Track Stats items |
| `codecs` | `CodecStats[]` (optional) | Codec items |
| `inboundRtps` | `InboundRtpStats[]` (optional) | Inbound RTPs |
| `remoteInboundRtps` | `RemoteInboundRtpStats[]` (optional) | Remote Inbound RTPs |
| `outboundRtps` | `OutboundRtpStats[]` (optional) | Outbound RTPs |
| `remoteOutboundRtps` | `RemoteOutboundRtpStats[]` (optional) | Remote Outbound RTPs |
| `mediaSources` | `MediaSourceStats[]` (optional) | Audio Source Stats |
| `mediaPlayouts` | `MediaPlayoutStats[]` (optional) | Media Playout Stats |
| `peerConnectionTransports` | `PeerConnectionTransportStats[]` (optional) | PeerConnection Transport Stats |
| `dataChannels` | `DataChannelStats[]` (optional) | Data Channels Stats |
| `iceTransports` | `IceTransportStats[]` (optional) | ICE Transport Stats |
| `iceCandidates` | `IceCandidateStats[]` (optional) | ICE Candidate Stats |
| `iceCandidatePairs` | `IceCandidatePairStats[]` (optional) | ICE Candidate Pair Stats |
| `certificates` | `CertificateStats[]` (optional) | Certificates |

---

## InboundRtpStats

Statistics for incoming RTP streams.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The time the stats were collected, in high-resolution time |
| `id` | `string` | Unique identifier of the stats object |
| `ssrc` | `number` | Synchronization source identifier of the RTP stream |
| `kind` | `string` | Kind of the media (e.g., 'audio' or 'video') |
| `trackIdentifier` | `string` | Identifier for the media track associated with the RTP stream |
| `transportId` | `string` (optional) | ID of the transport associated with the RTP stream |
| `codecId` | `string` (optional) | ID of the codec used for the RTP stream |
| `packetsReceived` | `number` (optional) | Number of packets received on the RTP stream |
| `packetsLost` | `number` (optional) | Number of packets lost on the RTP stream |
| `jitter` | `number` (optional) | Jitter of the RTP stream in seconds |
| `mid` | `string` (optional) | The MediaStream ID of the RTP stream |
| `remoteId` | `string` (optional) | Remote stats object ID associated with the RTP stream |
| `framesDecoded` | `number` (optional) | Number of frames decoded |
| `keyFramesDecoded` | `number` (optional) | Number of keyframes decoded |
| `framesRendered` | `number` (optional) | Number of frames rendered |
| `framesDropped` | `number` (optional) | Number of frames dropped |
| `frameWidth` | `number` (optional) | Width of the decoded video frames |
| `frameHeight` | `number` (optional) | Height of the decoded video frames |
| `framesPerSecond` | `number` (optional) | Frame rate in frames per second |
| `qpSum` | `number` (optional) | Sum of the Quantization Parameter values for decoded frames |
| `totalDecodeTime` | `number` (optional) | Total time spent decoding in seconds |
| `totalInterFrameDelay` | `number` (optional) | Sum of inter-frame delays in seconds |
| `totalSquaredInterFrameDelay` | `number` (optional) | Sum of squared inter-frame delays in seconds |
| `pauseCount` | `number` (optional) | Number of times playback was paused |
| `totalPausesDuration` | `number` (optional) | Total duration of pauses in seconds |
| `freezeCount` | `number` (optional) | Number of times playback was frozen |
| `totalFreezesDuration` | `number` (optional) | Total duration of freezes in seconds |
| `lastPacketReceivedTimestamp` | `number` (optional) | Timestamp of the last packet received |
| `headerBytesReceived` | `number` (optional) | Total header bytes received |
| `packetsDiscarded` | `number` (optional) | Total packets discarded |
| `fecBytesReceived` | `number` (optional) | Total bytes received from FEC |
| `fecPacketsReceived` | `number` (optional) | Total packets received from FEC |
| `fecPacketsDiscarded` | `number` (optional) | Total FEC packets discarded |
| `bytesReceived` | `number` (optional) | Total bytes received on the RTP stream |
| `nackCount` | `number` (optional) | Number of NACKs sent |
| `firCount` | `number` (optional) | Number of Full Intra Requests sent |
| `pliCount` | `number` (optional) | Number of Picture Loss Indications sent |
| `totalProcessingDelay` | `number` (optional) | Total processing delay in seconds |
| `estimatedPlayoutTimestamp` | `number` (optional) | Estimated timestamp of playout |
| `jitterBufferDelay` | `number` (optional) | Total jitter buffer delay in seconds |
| `jitterBufferTargetDelay` | `number` (optional) | Target delay for the jitter buffer in seconds |
| `jitterBufferEmittedCount` | `number` (optional) | Number of packets emitted from the jitter buffer |
| `jitterBufferMinimumDelay` | `number` (optional) | Minimum delay of the jitter buffer in seconds |
| `totalSamplesReceived` | `number` (optional) | Total audio samples received |
| `concealedSamples` | `number` (optional) | Number of concealed audio samples |
| `silentConcealedSamples` | `number` (optional) | Number of silent audio samples concealed |
| `concealmentEvents` | `number` (optional) | Number of audio concealment events |
| `insertedSamplesForDeceleration` | `number` (optional) | Number of audio samples inserted for deceleration |
| `removedSamplesForAcceleration` | `number` (optional) | Number of audio samples removed for acceleration |
| `audioLevel` | `number` (optional) | Audio level in the range [0.0, 1.0] |
| `totalAudioEnergy` | `number` (optional) | Total audio energy in the stream |
| `totalSamplesDuration` | `number` (optional) | Total duration of all received audio samples in seconds |
| `framesReceived` | `number` (optional) | Total number of frames received |
| `decoderImplementation` | `string` (optional) | Decoder implementation used for decoding frames |
| `playoutId` | `string` (optional) | Playout identifier for the RTP stream |
| `powerEfficientDecoder` | `boolean` (optional) | Indicates if the decoder is power-efficient |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## OutboundRtpStats

Statistics for outgoing RTP streams.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp for this stats object in DOMHighResTimeStamp format |
| `id` | `string` | The unique identifier for this stats object |
| `ssrc` | `number` | The SSRC identifier of the RTP stream |
| `kind` | `string` | The type of media ('audio' or 'video') |
| `transportId` | `string` (optional) | The ID of the transport used for this stream |
| `codecId` | `string` (optional) | The ID of the codec used for this stream |
| `packetsSent` | `number` (optional) | The total number of packets sent on this stream |
| `bytesSent` | `number` (optional) | The total number of bytes sent on this stream |
| `mid` | `string` (optional) | The media ID associated with this RTP stream |
| `mediaSourceId` | `string` (optional) | The ID of the media source associated with this stream |
| `remoteId` | `string` (optional) | The ID of the remote object corresponding to this stream |
| `rid` | `string` (optional) | The RID value of the RTP stream |
| `headerBytesSent` | `number` (optional) | The total number of header bytes sent on this stream |
| `retransmittedPacketsSent` | `number` (optional) | The number of retransmitted packets sent on this stream |
| `retransmittedBytesSent` | `number` (optional) | The number of retransmitted bytes sent on this stream |
| `rtxSsrc` | `number` (optional) | The SSRC for the RTX stream, if applicable |
| `targetBitrate` | `number` (optional) | The target bitrate for this RTP stream in bits per second |
| `totalEncodedBytesTarget` | `number` (optional) | The total target encoded bytes for this stream |
| `frameWidth` | `number` (optional) | The width of the frames sent in pixels |
| `frameHeight` | `number` (optional) | The height of the frames sent in pixels |
| `framesPerSecond` | `number` (optional) | The number of frames sent per second |
| `framesSent` | `number` (optional) | The total number of frames sent on this stream |
| `hugeFramesSent` | `number` (optional) | The total number of huge frames sent on this stream |
| `framesEncoded` | `number` (optional) | The total number of frames encoded on this stream |
| `keyFramesEncoded` | `number` (optional) | The total number of key frames encoded on this stream |
| `qpSum` | `number` (optional) | The sum of QP values for all frames encoded on this stream |
| `totalEncodeTime` | `number` (optional) | The total time spent encoding frames on this stream in seconds |
| `totalPacketSendDelay` | `number` (optional) | The total delay for packets sent on this stream in seconds |
| `qualityLimitationReason` | `string` (optional) | The reason for any quality limitation on this stream |
| `qualityLimitationResolutionChanges` | `number` (optional) | The number of resolution changes due to quality limitations |
| `nackCount` | `number` (optional) | The total number of NACK packets sent on this stream |
| `firCount` | `number` (optional) | The total number of FIR packets sent on this stream |
| `pliCount` | `number` (optional) | The total number of PLI packets sent on this stream |
| `encoderImplementation` | `string` (optional) | The implementation of the encoder used for this stream |
| `powerEfficientEncoder` | `boolean` (optional) | Indicates whether the encoder is power efficient |
| `active` | `boolean` (optional) | Indicates whether this stream is actively sending data |
| `scalabilityMode` | `string` (optional) | The scalability mode of the encoder used for this stream |
| `qualityLimitationDurations` | `QualityLimitationDurations` (optional) | The duration of quality limitation reasons categorized by type |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## IceCandidatePairStats

Statistics for ICE candidate pairs.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | The unique identifier for this RTCStats object |
| `timestamp` | `number` | The timestamp of when the stats were recorded, in seconds |
| `transportId` | `string` (optional) | The transport id of the connection this candidate pair belongs to |
| `localCandidateId` | `string` (optional) | The ID of the local ICE candidate in this pair |
| `remoteCandidateId` | `string` (optional) | The ID of the remote ICE candidate in this pair |
| `state` | `string` (optional) | ICE candidate pair state |
| `nominated` | `boolean` (optional) | Whether this candidate pair has been nominated |
| `packetsSent` | `number` (optional) | The number of packets sent using this candidate pair |
| `packetsReceived` | `number` (optional) | The number of packets received using this candidate pair |
| `bytesSent` | `number` (optional) | The total number of bytes sent using this candidate pair |
| `bytesReceived` | `number` (optional) | The total number of bytes received using this candidate pair |
| `lastPacketSentTimestamp` | `number` (optional) | The timestamp of the last packet sent using this candidate pair |
| `lastPacketReceivedTimestamp` | `number` (optional) | The timestamp of the last packet received using this candidate pair |
| `totalRoundTripTime` | `number` (optional) | The total round trip time (RTT) for this candidate pair in seconds |
| `currentRoundTripTime` | `number` (optional) | The current round trip time (RTT) for this candidate pair in seconds |
| `availableOutgoingBitrate` | `number` (optional) | The available outgoing bitrate (in bits per second) for this candidate pair |
| `availableIncomingBitrate` | `number` (optional) | The available incoming bitrate (in bits per second) for this candidate pair |
| `requestsReceived` | `number` (optional) | The number of ICE connection requests received by this candidate pair |
| `requestsSent` | `number` (optional) | The number of ICE connection requests sent by this candidate pair |
| `responsesReceived` | `number` (optional) | The number of ICE connection responses received by this candidate pair |
| `responsesSent` | `number` (optional) | The number of ICE connection responses sent by this candidate pair |
| `consentRequestsSent` | `number` (optional) | The number of ICE connection consent requests sent by this candidate pair |
| `packetsDiscardedOnSend` | `number` (optional) | The number of packets discarded while attempting to send via this candidate pair |
| `bytesDiscardedOnSend` | `number` (optional) | The total number of bytes discarded while attempting to send via this candidate pair |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## DataChannelStats

Statistics for WebRTC data channels.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp of the stat |
| `id` | `string` | A unique identifier for the stat |
| `label` | `string` (optional) | The label of the data channel |
| `protocol` | `string` (optional) | The protocol of the data channel |
| `dataChannelIdentifier` | `number` (optional) | The identifier for the data channel |
| `state` | `string` (optional) | The state of the data channel (e.g., 'open', 'closed') |
| `messagesSent` | `number` (optional) | The number of messages sent on the data channel |
| `bytesSent` | `number` (optional) | The number of bytes sent on the data channel |
| `messagesReceived` | `number` (optional) | The number of messages received on the data channel |
| `bytesReceived` | `number` (optional) | The number of bytes received on the data channel |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## MediaSourceStats

Statistics for media sources (cameras, microphones, screen capture).

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp of the stat |
| `id` | `string` | A unique identifier for the stat |
| `kind` | `string` | The type of media ('audio' or 'video') |
| `trackIdentifier` | `string` (optional) | The identifier of the media track |
| `audioLevel` | `number` (optional) | The current audio level |
| `totalAudioEnergy` | `number` (optional) | The total audio energy |
| `totalSamplesDuration` | `number` (optional) | The total duration of audio samples |
| `echoReturnLoss` | `number` (optional) | The echo return loss |
| `echoReturnLossEnhancement` | `number` (optional) | The enhancement of echo return loss |
| `width` | `number` (optional) | The width of the video |
| `height` | `number` (optional) | The height of the video |
| `frames` | `number` (optional) | The total number of frames |
| `framesPerSecond` | `number` (optional) | The frames per second of the video |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## CodecStats

Information about codecs used in the session.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the stats were generated |
| `id` | `string` | The unique identifier for the stats object |
| `mimeType` | `string` | The MIME type of the codec |
| `payloadType` | `number` (optional) | The payload type of the codec |
| `transportId` | `string` (optional) | The identifier of the transport associated with the codec |
| `clockRate` | `number` (optional) | The clock rate of the codec in Hz |
| `channels` | `number` (optional) | The number of audio channels for the codec, if applicable |
| `sdpFmtpLine` | `string` (optional) | The SDP format-specific parameters line for the codec |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## InboundTrackSample

Statistics for inbound media tracks.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the stats were generated |
| `id` | `string` | The unique identifier for the stats object |
| `kind` | `string` | The kind of media ('audio' or 'video') |
| `trackIdentifier` | `string` (optional) | The identifier of the media track |
| `remoteSource` | `boolean` (optional) | Whether the track is from a remote source |
| `ended` | `boolean` (optional) | Whether the track has ended |
| `detached` | `boolean` (optional) | Whether the track is detached |
| `frameWidth` | `number` (optional) | The width of video frames |
| `frameHeight` | `number` (optional) | The height of video frames |
| `framesPerSecond` | `number` (optional) | The frame rate |
| `framesReceived` | `number` (optional) | The total number of frames received |
| `framesDecoded` | `number` (optional) | The total number of frames decoded |
| `framesDropped` | `number` (optional) | The total number of frames dropped |
| `audioLevel` | `number` (optional) | The audio level for audio tracks |
| `totalAudioEnergy` | `number` (optional) | The total audio energy |
| `totalSamplesDuration` | `number` (optional) | The total duration of audio samples |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## OutboundTrackSample

Statistics for outbound media tracks.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the stats were generated |
| `id` | `string` | The unique identifier for the stats object |
| `kind` | `string` | The kind of media ('audio' or 'video') |
| `trackIdentifier` | `string` (optional) | The identifier of the media track |
| `remoteSource` | `boolean` (optional) | Whether the track is from a remote source |
| `ended` | `boolean` (optional) | Whether the track has ended |
| `detached` | `boolean` (optional) | Whether the track is detached |
| `frameWidth` | `number` (optional) | The width of video frames |
| `frameHeight` | `number` (optional) | The height of video frames |
| `framesPerSecond` | `number` (optional) | The frame rate |
| `framesSent` | `number` (optional) | The total number of frames sent |
| `framesEncoded` | `number` (optional) | The total number of frames encoded |
| `audioLevel` | `number` (optional) | The audio level for audio tracks |
| `totalAudioEnergy` | `number` (optional) | The total audio energy |
| `totalSamplesDuration` | `number` (optional) | The total duration of audio samples |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## RemoteInboundRtpStats

Statistics for remote inbound RTP streams (received by the remote peer).

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the stats were generated |
| `id` | `string` | The unique identifier for the stats object |
| `ssrc` | `number` | The SSRC identifier of the RTP stream |
| `kind` | `string` | The kind of media ('audio' or 'video') |
| `transportId` | `string` (optional) | The ID of the transport associated with this stream |
| `codecId` | `string` (optional) | The ID of the codec used for this stream |
| `packetsReceived` | `number` (optional) | The total number of packets received |
| `packetsLost` | `number` (optional) | The total number of packets lost |
| `jitter` | `number` (optional) | The jitter in seconds |
| `packetsDiscarded` | `number` (optional) | The total number of packets discarded |
| `packetsRepaired` | `number` (optional) | The total number of packets repaired |
| `burstPacketsLost` | `number` (optional) | The number of packets lost in bursts |
| `burstPacketsDiscarded` | `number` (optional) | The number of packets discarded in bursts |
| `burstLossCount` | `number` (optional) | The number of burst loss events |
| `burstDiscardCount` | `number` (optional) | The number of burst discard events |
| `burstLossRate` | `number` (optional) | The burst loss rate |
| `burstDiscardRate` | `number` (optional) | The burst discard rate |
| `gapLossRate` | `number` (optional) | The gap loss rate |
| `gapDiscardRate` | `number` (optional) | The gap discard rate |
| `framesDropped` | `number` (optional) | The number of frames dropped |
| `partialFramesLost` | `number` (optional) | The number of partial frames lost |
| `fullFramesLost` | `number` (optional) | The number of full frames lost |
| `roundTripTime` | `number` (optional) | The round trip time in seconds |
| `totalRoundTripTime` | `number` (optional) | The total round trip time |
| `roundTripTimeMeasurements` | `number` (optional) | The number of round trip time measurements |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## RemoteOutboundRtpStats

Statistics for remote outbound RTP streams (sent by the remote peer).

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the stats were generated |
| `id` | `string` | The unique identifier for the stats object |
| `ssrc` | `number` | The SSRC identifier of the RTP stream |
| `kind` | `string` | The kind of media ('audio' or 'video') |
| `transportId` | `string` (optional) | The ID of the transport associated with this stream |
| `codecId` | `string` (optional) | The ID of the codec used for this stream |
| `packetsSent` | `number` (optional) | The total number of packets sent |
| `bytesSent` | `number` (optional) | The total number of bytes sent |
| `localId` | `string` (optional) | The ID of the local inbound RTP stream |
| `remoteTimestamp` | `number` (optional) | The timestamp from the remote peer |
| `reportsSent` | `number` (optional) | The number of RTCP sender reports sent |
| `roundTripTime` | `number` (optional) | The round trip time in seconds |
| `totalRoundTripTime` | `number` (optional) | The total round trip time |
| `roundTripTimeMeasurements` | `number` (optional) | The number of round trip time measurements |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## MediaPlayoutStats

Statistics for media playout.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the stats were generated |
| `id` | `string` | The unique identifier for the stats object |
| `kind` | `string` | The kind of media ('audio' or 'video') |
| `synthesizedSamplesDuration` | `number` (optional) | The duration of synthesized samples in seconds |
| `synthesizedSamplesEvents` | `number` (optional) | The number of synthesized sample events |
| `totalSamplesDuration` | `number` (optional) | The total duration of samples in seconds |
| `totalPlayoutDelay` | `number` (optional) | The total playout delay in seconds |
| `totalSamplesCount` | `number` (optional) | The total number of samples |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## PeerConnectionTransportStats

Statistics for peer connection transports.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the stats were generated |
| `id` | `string` | The unique identifier for the stats object |
| `packetsSent` | `number` (optional) | The total number of packets sent |
| `packetsReceived` | `number` (optional) | The total number of packets received |
| `bytesSent` | `number` (optional) | The total number of bytes sent |
| `bytesReceived` | `number` (optional) | The total number of bytes received |
| `rtcpPacketsSent` | `number` (optional) | The total number of RTCP packets sent |
| `rtcpPacketsReceived` | `number` (optional) | The total number of RTCP packets received |
| `rtcpBytesSent` | `number` (optional) | The total number of RTCP bytes sent |
| `rtcpBytesReceived` | `number` (optional) | The total number of RTCP bytes received |
| `iceRole` | `string` (optional) | The ICE role of the transport |
| `dtlsState` | `string` (optional) | The DTLS state of the transport |
| `selectedCandidatePairId` | `string` (optional) | The ID of the selected candidate pair |
| `localCertificateId` | `string` (optional) | The ID of the local certificate |
| `remoteCertificateId` | `string` (optional) | The ID of the remote certificate |
| `tlsVersion` | `string` (optional) | The TLS version used |
| `cipher` | `string` (optional) | The cipher used |
| `srtpCipher` | `string` (optional) | The SRTP cipher used |
| `tlsGroup` | `string` (optional) | The TLS group used |
| `selectedCandidatePairChanges` | `number` (optional) | The number of selected candidate pair changes |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## CertificateStats

Statistics for certificates used in the session.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the stats were generated |
| `id` | `string` | The unique identifier for the stats object |
| `fingerprint` | `string` (optional) | The fingerprint of the certificate |
| `fingerprintAlgorithm` | `string` (optional) | The algorithm used to generate the fingerprint |
| `base64Certificate` | `string` (optional) | The base64-encoded certificate |
| `issuerCertificateId` | `string` (optional) | The ID of the issuer certificate |
| `subjectName` | `string` (optional) | The subject name of the certificate |
| `validFrom` | `number` (optional) | The start of the certificate's validity period |
| `validTo` | `number` (optional) | The end of the certificate's validity period |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## IceCandidateStats

Statistics for ICE candidates.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the stats were generated |
| `id` | `string` | The unique identifier for the stats object |
| `transportId` | `string` (optional) | The ID of the transport associated with this candidate |
| `candidateType` | `string` (optional) | The type of ICE candidate |
| `protocol` | `string` (optional) | The protocol used by the ICE candidate |
| `address` | `string` (optional) | The IP address of the ICE candidate |
| `port` | `number` (optional) | The port number of the ICE candidate |
| `priority` | `number` (optional) | The priority of the ICE candidate |
| `url` | `string` (optional) | The URL of the ICE candidate |
| `relatedAddress` | `string` (optional) | The related IP address of the ICE candidate |
| `relatedPort` | `number` (optional) | The related port number of the ICE candidate |
| `usernameFragment` | `string` (optional) | The username fragment of the ICE candidate |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## IceTransportStats

Statistics for ICE transports.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the stats were generated |
| `id` | `string` | The unique identifier for the stats object |
| `packetsSent` | `number` (optional) | The total number of packets sent |
| `packetsReceived` | `number` (optional) | The total number of packets received |
| `bytesSent` | `number` (optional) | The total number of bytes sent |
| `bytesReceived` | `number` (optional) | The total number of bytes received |
| `iceState` | `string` (optional) | The ICE state of the transport |
| `localCandidateId` | `string` (optional) | The ID of the local ICE candidate |
| `remoteCandidateId` | `string` (optional) | The ID of the remote ICE candidate |
| `selectedCandidatePairId` | `string` (optional) | The ID of the selected candidate pair |
| `localCertificateId` | `string` (optional) | The ID of the local certificate |
| `remoteCertificateId` | `string` (optional) | The ID of the remote certificate |
| `tlsVersion` | `string` (optional) | The TLS version used |
| `dtlsCipher` | `string` (optional) | The DTLS cipher used |
| `srtpCipher` | `string` (optional) | The SRTP cipher used |
| `tlsGroup` | `string` (optional) | The TLS group used |
| `selectedCandidatePairChanges` | `number` (optional) | The number of selected candidate pair changes |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |

---

## ClientEvent

Represents a client event.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the event occurred |
| `type` | `string` | The type of the event |
| `description` | `string` (optional) | A description of the event |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this event |

---

## ClientIssue

Represents a client issue.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the issue occurred |
| `type` | `string` | The type of the issue |
| `description` | `string` (optional) | A description of the issue |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this issue |

---

## ClientMetaData

Represents additional client metadata.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the metadata was generated |
| `type` | `string` | The type of the metadata |
| `description` | `string` (optional) | A description of the metadata |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this metadata |

---

## ExtensionStat

Represents a custom WebRTC app provided stats payload.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `number` | The timestamp when the stats were generated |
| `id` | `string` | The unique identifier for the stats object |
| `payload` | `Record<string, unknown>` | The custom stats payload |
| `attachments` | `Record<string, unknown>` (optional) | Additional information attached to this stats |
