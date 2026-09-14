---
title: "ClientSample reference"
slug: "clientsample"
description: "Field-by-field reference for the ClientSample schema"
lead: "Every field of the ClientSample schema, generated from schema version 3.7.0"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 620
toc: true
---

`ClientSample` is the object a client-side monitor produces and an observer consumes. It is the
contract between [`client-monitor-js`](/docs/client-monitor-js/) and
[`observer-js`](/docs/observer-js/), and the thing you store if you build your own pipeline.

{{< callout context="note" title="Schema version 3.7.0" icon="info-circle" >}}
This page is generated from the `3.7.0` Avro sources. Fields added since `3.0.0` are marked inline.
No field has ever been **removed** in the 3.x line; what changed since `3.3.0` is the *type* of the
four payload fields and of `scoreReasons`. See the [version history](/docs/schema/versions/) for
what changed and when.
{{< /callout >}}

## Shape at a glance

```text
ClientSample
├─ timestamp, callId, clientId, score, scoreReasons, attachments
├─ peerConnections[]  (PeerConnectionSample)
│   ├─ inboundTracks[]              outboundTracks[]
│   ├─ inboundRtps[]                outboundRtps[]
│   ├─ remoteInboundRtps[]          remoteOutboundRtps[]
│   ├─ mediaSources[]               mediaPlayouts[]
│   ├─ codecs[]                     dataChannels[]
│   ├─ iceTransports[]              iceCandidates[]
│   ├─ iceCandidatePairs[]          peerConnectionTransports[]
│   └─ certificates[]
├─ clientEvents[]      (ClientEvent)
├─ clientIssues[]      (ClientIssue)
├─ clientMetaItems[]   (ClientMetaData)
└─ extensionStats[]    (ExtensionStat)
```

Three conventions run through the whole schema:

- **`timestamp` + `id`** — every stats record carries the collection time and the identifier the
  browser assigned, so records can be correlated across samples.
- **`attachments`** — every record has a free-form slot for your own data. This is how a track becomes
  "Alice's screen share" rather than an opaque SSRC.
- **`score` + `scoreReasons`** — clients, peer connections and tracks can carry a computed 0–5 quality
  score with a machine-readable explanation.


## Top level


### ClientSample

The root object. One `ClientSample` is a snapshot of one participant at one point in time.

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp the sample is created in GMT |
| `callId` | `string`<br>*optional* | the unique identifier of the call or session |
| `clientId` | `string`<br>*optional* | Unique id of the client providing samples. |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this sample (e.g.: roomId, userId, displayName, etc...) |
| `score` | `number`<br>*optional* | Calculated score for client (details should be added to scoreReasons) |
| `scoreReasons` | `Record<string, number>`<br>*optional* | Reasons for the score calculation, mapping each reason to how much it contributed **`changed in 3.6.0`** |
| `peerConnections` | `PeerConnectionSample[]`<br>*optional* | Samples taken PeerConnections |
| `clientEvents` | `ClientEvent[]`<br>*optional* | A list of client events. |
| `clientIssues` | `ClientIssue[]`<br>*optional* | A list of client issues. |
| `clientMetaItems` | `ClientMetaData[]`<br>*optional* | A list of additional client events. |
| `extensionStats` | `ExtensionStat[]`<br>*optional* | The WebRTC app provided custom stats payload |


### PeerConnectionSample

Everything observed on a single `RTCPeerConnection` during the sampling interval.

| Field | Type | Description |
|---|---|---|
| `peerConnectionId` | `string` | Unique identifier of the stats object. |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this sample |
| `score` | `number`<br>*optional* | Calculated score for peer connection (details should be added to scoreReasons) |
| `scoreReasons` | `Record<string, number>`<br>*optional* | Reasons for the score calculation, mapping each reason to how much it contributed **`changed in 3.6.0`** |
| `inboundTracks` | `InboundTrackSample[]`<br>*optional* | Inbound Track Stats items |
| `outboundTracks` | `OutboundTrackSample[]`<br>*optional* | Outbound Track Stats items |
| `codecs` | `CodecStats[]`<br>*optional* | Codec items |
| `inboundRtps` | `InboundRtpStats[]`<br>*optional* | Inbound RTP Stats |
| `remoteInboundRtps` | `RemoteInboundRtpStats[]`<br>*optional* | Remote Inbound RTP Stats |
| `outboundRtps` | `OutboundRtpStats[]`<br>*optional* | Outbound RTP Stats |
| `remoteOutboundRtps` | `RemoteOutboundRtpStats[]`<br>*optional* | Remote Outbound RTP Stats |
| `mediaSources` | `MediaSourceStats[]`<br>*optional* | Audio Source Stats |
| `mediaPlayouts` | `MediaPlayoutStats[]`<br>*optional* | Media Playout Stats |
| `peerConnectionTransports` | `PeerConnectionTransportStats[]`<br>*optional* | PeerConnection Transport Stats |
| `dataChannels` | `DataChannelStats[]`<br>*optional* | Data Channels Stats |
| `iceTransports` | `IceTransportStats[]`<br>*optional* | ICE Transport Stats |
| `iceCandidates` | `IceCandidateStats[]`<br>*optional* | ICE Candidate Stats |
| `iceCandidatePairs` | `IceCandidatePairStats[]`<br>*optional* | ICE Candidate Pair Stats |
| `certificates` | `CertificateStats[]`<br>*optional* | Certificate Stats |


## Tracks


### InboundTrackSample

A received media track, scored by the client.

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp when the stats were generated. |
| `id` | `string` | The unique identifier for the stats object. |
| `kind` | `string` | Kind of the media (e.g., 'audio' or 'video'). |
| `score` | `number`<br>*optional* | Calculated score for track (details should be added to scoreReasons) |
| `scoreReasons` | `Record<string, number>`<br>*optional* | Reasons for the score calculation, mapping each reason to how much it contributed **`changed in 3.6.0`** |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


### OutboundTrackSample

A sent media track, scored by the client.

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp when the stats were generated. |
| `id` | `string` | The unique identifier for the stats object. |
| `kind` | `string` | Kind of the media (e.g., 'audio' or 'video'). |
| `score` | `number`<br>*optional* | Calculated score for track (details should be added to scoreReasons) |
| `scoreReasons` | `Record<string, number>`<br>*optional* | Reasons for the score calculation, mapping each reason to how much it contributed **`changed in 3.6.0`** |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


## RTP statistics


### InboundRtpStats

Receiving side of one RTP stream (`inbound-rtp`).

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The time the stats were collected, in high-resolution time. |
| `id` | `string` | Unique identifier of the stats object. |
| `ssrc` | `number` | Synchronization source identifier of the RTP stream. |
| `kind` | `string` | Kind of the media (e.g., 'audio' or 'video'). |
| `trackIdentifier` | `string` | Identifier for the media track associated with the RTP stream. |
| `transportId` | `string`<br>*optional* | ID of the transport associated with the RTP stream. |
| `codecId` | `string`<br>*optional* | ID of the codec used for the RTP stream. |
| `packetsReceived` | `number`<br>*optional* | Number of packets received on the RTP stream. |
| `packetsReceivedWithEct1` | `number`<br>*optional* | Total number of RTP packets received for this SSRC marked with the ECT(1) marking. **`new in 3.2.0`** |
| `packetsReceivedWithCe` | `number`<br>*optional* | Total number of RTP packets received for this SSRC marked with the CE marking. **`new in 3.2.0`** |
| `packetsReportedAsLost` | `number`<br>*optional* | Total number of RTP packets for which an RFC8888 report has been sent with a zero R bit. **`new in 3.2.0`** |
| `packetsReportedAsLostButRecovered` | `number`<br>*optional* | Total number of RTP packets reported as lost but later recovered in a subsequent RFC8888 report. **`new in 3.2.0`** |
| `packetsLost` | `number`<br>*optional* | Number of packets lost on the RTP stream. |
| `jitter` | `number`<br>*optional* | Jitter of the RTP stream in seconds. |
| `mid` | `string`<br>*optional* | The media stream identification tag from the SDP media section. |
| `remoteId` | `string`<br>*optional* | Remote stats object ID associated with the RTP stream. |
| `framesDecoded` | `number`<br>*optional* | Number of frames decoded. |
| `keyFramesDecoded` | `number`<br>*optional* | Number of keyframes decoded. |
| `framesRendered` | `number`<br>*optional* | Number of frames rendered. |
| `framesDropped` | `number`<br>*optional* | Number of frames dropped. |
| `frameWidth` | `number`<br>*optional* | Width of the decoded video frames. |
| `frameHeight` | `number`<br>*optional* | Height of the decoded video frames. |
| `framesPerSecond` | `number`<br>*optional* | Frame rate in frames per second. |
| `qpSum` | `number`<br>*optional* | Sum of the Quantization Parameter values for decoded frames. |
| `totalDecodeTime` | `number`<br>*optional* | Total time spent decoding in seconds. |
| `totalInterFrameDelay` | `number`<br>*optional* | Sum of inter-frame delays in seconds. |
| `totalSquaredInterFrameDelay` | `number`<br>*optional* | Sum of squared inter-frame delays in seconds. |
| `pauseCount` | `number`<br>*optional* | Number of times playback was paused. |
| `totalPausesDuration` | `number`<br>*optional* | Total duration of pauses in seconds. |
| `freezeCount` | `number`<br>*optional* | Number of times playback was frozen. |
| `totalFreezesDuration` | `number`<br>*optional* | Total duration of freezes in seconds. |
| `lastPacketReceivedTimestamp` | `number`<br>*optional* | Timestamp of the last packet received. |
| `headerBytesReceived` | `number`<br>*optional* | Total header bytes received. |
| `packetsDiscarded` | `number`<br>*optional* | Total packets discarded. |
| `fecBytesReceived` | `number`<br>*optional* | Total bytes received from FEC. |
| `fecPacketsReceived` | `number`<br>*optional* | Total packets received from FEC. |
| `fecPacketsDiscarded` | `number`<br>*optional* | Total FEC packets discarded. |
| `bytesReceived` | `number`<br>*optional* | Total bytes received on the RTP stream. |
| `nackCount` | `number`<br>*optional* | Number of NACKs received. |
| `firCount` | `number`<br>*optional* | Number of Full Intra Requests received. |
| `pliCount` | `number`<br>*optional* | Number of Picture Loss Indications received. |
| `totalProcessingDelay` | `number`<br>*optional* | Total processing delay in seconds. |
| `estimatedPlayoutTimestamp` | `number`<br>*optional* | Estimated timestamp of playout. |
| `jitterBufferDelay` | `number`<br>*optional* | Total jitter buffer delay in seconds. |
| `jitterBufferTargetDelay` | `number`<br>*optional* | Target delay for the jitter buffer in seconds. |
| `jitterBufferEmittedCount` | `number`<br>*optional* | Number of packets emitted from the jitter buffer. |
| `jitterBufferMinimumDelay` | `number`<br>*optional* | Minimum delay of the jitter buffer in seconds. |
| `totalSamplesReceived` | `number`<br>*optional* | Total audio samples received. |
| `concealedSamples` | `number`<br>*optional* | Number of concealed audio samples. |
| `silentConcealedSamples` | `number`<br>*optional* | Number of silent audio samples concealed. |
| `concealmentEvents` | `number`<br>*optional* | Number of audio concealment events. |
| `insertedSamplesForDeceleration` | `number`<br>*optional* | Number of audio samples inserted for deceleration. |
| `removedSamplesForAcceleration` | `number`<br>*optional* | Number of audio samples removed for acceleration. |
| `audioLevel` | `number`<br>*optional* | Audio level in the range [0.0, 1.0]. |
| `totalAudioEnergy` | `number`<br>*optional* | Total audio energy in the stream. |
| `totalSamplesDuration` | `number`<br>*optional* | Total duration of all received audio samples in seconds. |
| `framesReceived` | `number`<br>*optional* | Total number of frames received. |
| `decoderImplementation` | `string`<br>*optional* | Decoder implementation used for decoding frames. |
| `playoutId` | `string`<br>*optional* | Playout identifier for the RTP stream. |
| `powerEfficientDecoder` | `boolean`<br>*optional* | Indicates if the decoder is power-efficient. |
| `framesAssembledFromMultiplePackets` | `number`<br>*optional* | Number of frames assembled from multiple packets. |
| `totalAssemblyTime` | `number`<br>*optional* | Total assembly time for frames in seconds. |
| `retransmittedPacketsReceived` | `number`<br>*optional* | Number of retransmitted packets received. |
| `retransmittedBytesReceived` | `number`<br>*optional* | Number of retransmitted bytes received. |
| `rtxSsrc` | `number`<br>*optional* | SSRC of the retransmission stream. |
| `fecSsrc` | `number`<br>*optional* | SSRC of the FEC stream. |
| `totalCorruptionProbability` | `number`<br>*optional* | Total corruption probability of packets. |
| `totalSquaredCorruptionProbability` | `number`<br>*optional* | Total squared corruption probability of packets. |
| `corruptionMeasurements` | `number`<br>*optional* | Number of corruption measurements. |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


### OutboundRtpStats

Sending side of one RTP stream (`outbound-rtp`).

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp for this stats object in DOMHighResTimeStamp format. |
| `id` | `string` | The unique identifier for this stats object. |
| `ssrc` | `number` | The SSRC identifier of the RTP stream. |
| `kind` | `string` | The type of media ('audio' or 'video'). |
| `transportId` | `string`<br>*optional* | The ID of the transport used for this stream. |
| `codecId` | `string`<br>*optional* | The ID of the codec used for this stream. |
| `packetsSent` | `number`<br>*optional* | The total number of packets sent on this stream. |
| `bytesSent` | `number`<br>*optional* | The total number of bytes sent on this stream. |
| `mid` | `string`<br>*optional* | The media ID associated with this RTP stream. |
| `mediaSourceId` | `string`<br>*optional* | The ID of the media source associated with this stream. |
| `remoteId` | `string`<br>*optional* | The ID of the remote object corresponding to this stream. |
| `rid` | `string`<br>*optional* | The RID value of the RTP stream. |
| `encodingIndex` | `number`<br>*optional* | Index of the encoding in the encoding array. **`new in 3.2.0`** |
| `headerBytesSent` | `number`<br>*optional* | The total number of header bytes sent on this stream. |
| `retransmittedPacketsSent` | `number`<br>*optional* | The number of retransmitted packets sent on this stream. |
| `retransmittedBytesSent` | `number`<br>*optional* | The number of retransmitted bytes sent on this stream. |
| `rtxSsrc` | `number`<br>*optional* | The SSRC for the RTX stream, if applicable. |
| `targetBitrate` | `number`<br>*optional* | The target bitrate for this RTP stream in bits per second. |
| `totalEncodedBytesTarget` | `number`<br>*optional* | The total target encoded bytes for this stream. |
| `frameWidth` | `number`<br>*optional* | The width of the frames sent in pixels. |
| `frameHeight` | `number`<br>*optional* | The height of the frames sent in pixels. |
| `framesPerSecond` | `number`<br>*optional* | The number of frames sent per second. |
| `framesSent` | `number`<br>*optional* | The total number of frames sent on this stream. |
| `hugeFramesSent` | `number`<br>*optional* | The total number of huge frames sent on this stream. |
| `framesEncoded` | `number`<br>*optional* | The total number of frames encoded on this stream. |
| `keyFramesEncoded` | `number`<br>*optional* | The total number of key frames encoded on this stream. |
| `qpSum` | `number`<br>*optional* | The sum of QP values for all frames encoded on this stream. |
| `psnrSum` | `PsnrSum`<br>*optional* | Cumulative PSNR measurements for Y, U, V components. **`new in 3.2.0`** |
| `psnrMeasurements` | `number`<br>*optional* | Total number of PSNR measurements collected. **`new in 3.2.0`** |
| `totalEncodeTime` | `number`<br>*optional* | The total time spent encoding frames on this stream in seconds. |
| `totalPacketSendDelay` | `number`<br>*optional* | The total delay for packets sent on this stream in seconds. |
| `qualityLimitationReason` | `string`<br>*optional* | The reason for any quality limitation on this stream (e.g., 'cpu', 'bandwidth', 'other'). |
| `qualityLimitationDurations` | `QualityLimitationDurations`<br>*optional* | The duration of quality limitation reasons categorized by type. **`new in 3.2.0`** |
| `qualityLimitationResolutionChanges` | `number`<br>*optional* | The number of resolution changes due to quality limitations. |
| `nackCount` | `number`<br>*optional* | The total number of NACK packets sent on this stream. |
| `firCount` | `number`<br>*optional* | The total number of FIR packets sent on this stream. |
| `pliCount` | `number`<br>*optional* | The total number of PLI packets sent on this stream. |
| `encoderImplementation` | `string`<br>*optional* | The implementation of the encoder used for this stream. |
| `powerEfficientEncoder` | `boolean`<br>*optional* | Indicates whether the encoder is power-efficient. |
| `active` | `boolean`<br>*optional* | Indicates whether this stream is actively sending data. |
| `scalabilityMode` | `string`<br>*optional* | The scalability mode of the encoder used for this stream. |
| `packetsSentWithEct1` | `number`<br>*optional* | Number of packets sent with ECT(1) congestion marking. **`new in 3.2.0`** |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats. |


### RemoteInboundRtpStats

The remote peer's view of what we send (`remote-inbound-rtp`, from RTCP Receiver Reports).

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp for this stats object in DOMHighResTimeStamp format. |
| `id` | `string` | The unique identifier for this stats object. |
| `ssrc` | `number` | The SSRC identifier of the RTP stream. |
| `kind` | `string` | The type of media ('audio' or 'video'). |
| `transportId` | `string`<br>*optional* | The ID of the transport used for this stream. |
| `codecId` | `string`<br>*optional* | The ID of the codec used for this stream. |
| `packetsReceived` | `number`<br>*optional* | The total number of packets received on this stream. |
| `packetsReceivedWithEct1` | `number`<br>*optional* | Total number of RTP packets received for this SSRC marked with the ECT(1) marking. **`new in 3.2.0`** |
| `packetsReceivedWithCe` | `number`<br>*optional* | Total number of RTP packets received for this SSRC marked with the CE marking. **`new in 3.2.0`** |
| `packetsReportedAsLost` | `number`<br>*optional* | Total number of RTP packets for which an RFC8888 report has been sent with a zero R bit. **`new in 3.2.0`** |
| `packetsReportedAsLostButRecovered` | `number`<br>*optional* | Total number of RTP packets reported as lost but later recovered in a subsequent RFC8888 report. **`new in 3.2.0`** |
| `packetsLost` | `number`<br>*optional* | The total number of packets lost on this stream. |
| `jitter` | `number`<br>*optional* | The jitter value for this stream in seconds. |
| `localId` | `string`<br>*optional* | The ID of the local object corresponding to this remote stream. |
| `roundTripTime` | `number`<br>*optional* | The most recent RTT measurement for this stream in seconds. |
| `totalRoundTripTime` | `number`<br>*optional* | The cumulative RTT for all packets on this stream in seconds. |
| `fractionLost` | `number`<br>*optional* | The fraction of packets lost on this stream, calculated over a time interval. |
| `roundTripTimeMeasurements` | `number`<br>*optional* | The total number of RTT measurements for this stream. |
| `packetsWithBleachedEct1Marking` | `number`<br>*optional* | Number of packets with ECT(1) marking that were bleached by a middlebox. **`new in 3.2.0`** |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


### RemoteOutboundRtpStats

The remote peer's view of what it sends us (`remote-outbound-rtp`, from RTCP Sender Reports).

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp for this stats object in DOMHighResTimeStamp format. |
| `id` | `string` | The unique identifier for this stats object. |
| `ssrc` | `number` | The SSRC identifier of the RTP stream. |
| `kind` | `string` | The type of media ('audio' or 'video'). |
| `transportId` | `string`<br>*optional* | The ID of the transport used for this stream. |
| `codecId` | `string`<br>*optional* | The ID of the codec used for this stream. |
| `packetsSent` | `number`<br>*optional* | The total number of packets sent on this stream. |
| `bytesSent` | `number`<br>*optional* | The total number of bytes sent on this stream. |
| `localId` | `string`<br>*optional* | The ID of the local object corresponding to this stream. |
| `remoteTimestamp` | `number`<br>*optional* | The remote timestamp for this stats object in DOMHighResTimeStamp format. |
| `reportsSent` | `number`<br>*optional* | The total number of reports sent on this stream. |
| `roundTripTime` | `number`<br>*optional* | The current estimated round-trip time for this stream in seconds. |
| `totalRoundTripTime` | `number`<br>*optional* | The total round-trip time for this stream in seconds. |
| `roundTripTimeMeasurements` | `number`<br>*optional* | The total number of round-trip time measurements for this stream. |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


### QualityLimitationDurations

Cumulative seconds spent in each quality-limitation state, nested inside `OutboundRtpStats`.

| Field | Type | Description |
|---|---|---|
| `none` | `number` | Duration of no quality limitation in seconds. |
| `cpu` | `number` | Duration of CPU-based quality limitation in seconds. |
| `bandwidth` | `number` | Duration of bandwidth-based quality limitation in seconds. |
| `other` | `number` | Duration of other quality limitation reasons in seconds. |


### PsnrSum

Cumulative per-plane PSNR, nested inside `OutboundRtpStats`.

| Field | Type | Description |
|---|---|---|
| `y` | `number` | PSNR value for the Y (luminance) component. |
| `u` | `number` | PSNR value for the U (chrominance) component. |
| `v` | `number` | PSNR value for the V (chrominance) component. |


## Media


### MediaSourceStats

A local capture source (`media-source`) feeding one or more outbound RTP streams.

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp of the stat. |
| `id` | `string` | A unique identifier for the stat. |
| `kind` | `string` | The type of media ('audio' or 'video'). |
| `trackIdentifier` | `string`<br>*optional* | The identifier of the media track. |
| `audioLevel` | `number`<br>*optional* | The current audio level. |
| `totalAudioEnergy` | `number`<br>*optional* | The total audio energy. |
| `totalSamplesDuration` | `number`<br>*optional* | The total duration of audio samples. |
| `echoReturnLoss` | `number`<br>*optional* | The echo return loss. |
| `echoReturnLossEnhancement` | `number`<br>*optional* | The enhancement of echo return loss. |
| `width` | `number`<br>*optional* | The width of the video. |
| `height` | `number`<br>*optional* | The height of the video. |
| `frames` | `number`<br>*optional* | The total number of frames. |
| `framesPerSecond` | `number`<br>*optional* | The frames per second of the video. |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


### MediaPlayoutStats

Audio playout path (`media-playout`) — where synthesized/stretched samples show up.

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp of the stat. |
| `id` | `string` | A unique identifier for the stat. |
| `kind` | `string` | The kind of media (audio/video). |
| `synthesizedSamplesDuration` | `number`<br>*optional* | The duration of synthesized audio samples. |
| `synthesizedSamplesEvents` | `number`<br>*optional* | The number of synthesized audio samples events. |
| `totalSamplesDuration` | `number`<br>*optional* | The total duration of all audio samples. |
| `totalPlayoutDelay` | `number`<br>*optional* | The total delay experienced during audio playout. |
| `totalSamplesCount` | `number`<br>*optional* | The total count of audio samples. |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


### CodecStats

A negotiated codec (`codec`).

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp when the stats were generated. |
| `id` | `string` | The unique identifier for the stats object. |
| `mimeType` | `string` | The MIME type of the codec. |
| `payloadType` | `number`<br>*optional* | The payload type of the codec. |
| `transportId` | `string`<br>*optional* | The identifier of the transport associated with the codec. |
| `clockRate` | `number`<br>*optional* | The clock rate of the codec in Hz. |
| `channels` | `number`<br>*optional* | The number of audio channels for the codec, if applicable. |
| `sdpFmtpLine` | `string`<br>*optional* | The SDP format-specific parameters line for the codec. |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


## Transport & connectivity


### PeerConnectionTransportStats

Peer-connection level data channel counters (`peer-connection`).

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp of the stat. |
| `id` | `string` | A unique identifier for the stat. |
| `dataChannelsOpened` | `number`<br>*optional* | The number of data channels opened. |
| `dataChannelsClosed` | `number`<br>*optional* | The number of data channels closed. |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


### DataChannelStats

One `RTCDataChannel` (`data-channel`).

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp of the stat. |
| `id` | `string` | A unique identifier for the stat. |
| `label` | `string`<br>*optional* | The label of the data channel. |
| `protocol` | `string`<br>*optional* | The protocol of the data channel. |
| `dataChannelIdentifier` | `number`<br>*optional* | The identifier for the data channel. |
| `state` | `string`<br>*optional* | The state of the data channel (e.g., 'open', 'closed'). |
| `messagesSent` | `number`<br>*optional* | The number of messages sent on the data channel. |
| `bytesSent` | `number`<br>*optional* | The number of bytes sent on the data channel. |
| `messagesReceived` | `number`<br>*optional* | The number of messages received on the data channel. |
| `bytesReceived` | `number`<br>*optional* | The number of bytes received on the data channel. |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


### IceTransportStats

ICE/DTLS transport (`transport`).

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp of the stat. |
| `id` | `string` | A unique identifier for the stat. |
| `packetsSent` | `number`<br>*optional* | The number of packets sent. |
| `packetsReceived` | `number`<br>*optional* | The number of packets received. |
| `bytesSent` | `number`<br>*optional* | The number of bytes sent. |
| `bytesReceived` | `number`<br>*optional* | The number of bytes received. |
| `iceRole` | `string`<br>*optional* | The ICE role (e.g., 'controlling', 'controlled'). |
| `iceLocalUsernameFragment` | `string`<br>*optional* | The local username fragment for ICE. |
| `dtlsState` | `string`<br>*optional* | The DTLS transport state (e.g., 'new', 'connecting', 'connected'). |
| `iceState` | `string`<br>*optional* | The ICE transport state (e.g., 'new', 'checking', 'connected'). |
| `selectedCandidatePairId` | `string`<br>*optional* | The ID of the selected ICE candidate pair. |
| `localCertificateId` | `string`<br>*optional* | The ID of the local certificate. |
| `remoteCertificateId` | `string`<br>*optional* | The ID of the remote certificate. |
| `tlsVersion` | `string`<br>*optional* | The TLS version used for encryption. |
| `dtlsCipher` | `string`<br>*optional* | The DTLS cipher suite used. |
| `dtlsRole` | `string`<br>*optional* | The role in the DTLS handshake (e.g., 'client', 'server'). |
| `srtpCipher` | `string`<br>*optional* | The SRTP cipher used for encryption. |
| `selectedCandidatePairChanges` | `number`<br>*optional* | The number of changes to the selected ICE candidate pair. |
| `ccfbMessagesSent` | `number`<br>*optional* | Number of congestion control feedback (CCFB) messages sent on this transport. **`new in 3.2.0`** |
| `ccfbMessagesReceived` | `number`<br>*optional* | Number of congestion control feedback (CCFB) messages received on this transport. **`new in 3.2.0`** |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats. |


### IceCandidateStats

One local or remote ICE candidate (`local-candidate` / `remote-candidate`).

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp of the stat. |
| `id` | `string` | A unique identifier for the stat. |
| `transportId` | `string`<br>*optional* | The transport ID associated with the ICE candidate. |
| `address` | `string`<br>*optional* | The IP address of the ICE candidate. |
| `port` | `number`<br>*optional* | The port number of the ICE candidate. |
| `protocol` | `string`<br>*optional* | The transport protocol used by the candidate (e.g., 'udp', 'tcp'). |
| `candidateType` | `string`<br>*optional* | The type of the ICE candidate (e.g., 'host', 'srflx', 'relay'). |
| `priority` | `number`<br>*optional* | The priority of the ICE candidate. |
| `url` | `string`<br>*optional* | The URL of the ICE candidate. |
| `relayProtocol` | `string`<br>*optional* | The protocol used for the relay (e.g., 'tcp', 'udp'). |
| `foundation` | `string`<br>*optional* | A string representing the foundation for the ICE candidate. |
| `relatedAddress` | `string`<br>*optional* | The related address for the ICE candidate (if any). |
| `relatedPort` | `number`<br>*optional* | The related port for the ICE candidate (if any). |
| `usernameFragment` | `string`<br>*optional* | The username fragment for the ICE candidate. |
| `tcpType` | `string`<br>*optional* | The TCP type of the ICE candidate (e.g., 'active', 'passive'). |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


### IceCandidatePairStats

One ICE candidate pair (`candidate-pair`) — where RTT and bandwidth estimates live.

| Field | Type | Description |
|---|---|---|
| `id` | `string` | The unique identifier for this RTCStats object. |
| `timestamp` | `number` | The timestamp of when the stats were recorded, in milliseconds. |
| `transportId` | `string`<br>*optional* | The transport id of the connection this candidate pair belongs to. |
| `localCandidateId` | `string`<br>*optional* | The ID of the local ICE candidate in this pair. |
| `remoteCandidateId` | `string`<br>*optional* | The ID of the remote ICE candidate in this pair. |
| `state` | `"new" \| "frozen" \| "in-progress" \| "waiting" \| "failed" \| "succeeded" \| "cancelled" \| "inprogress"`<br>*optional* | The checklist state of this candidate pair. Values follow the W3C RTCStatsIceCandidatePairState enum (frozen, waiting, in-progress, failed, succeeded). Two further values are accepted for backward compatibility and are not part of the current spec: `new` (never standardised) and `cancelled` (removed from the spec after 2016). |
| `nominated` | `boolean`<br>*optional* | Whether this candidate pair has been nominated. |
| `packetsSent` | `number`<br>*optional* | The number of packets sent using this candidate pair. |
| `packetsReceived` | `number`<br>*optional* | The number of packets received using this candidate pair. |
| `bytesSent` | `number`<br>*optional* | The total number of bytes sent using this candidate pair. |
| `bytesReceived` | `number`<br>*optional* | The total number of bytes received using this candidate pair. |
| `lastPacketSentTimestamp` | `number`<br>*optional* | The timestamp of the last packet sent using this candidate pair. |
| `lastPacketReceivedTimestamp` | `number`<br>*optional* | The timestamp of the last packet received using this candidate pair. |
| `totalRoundTripTime` | `number`<br>*optional* | The total round trip time (RTT) for this candidate pair in seconds. |
| `currentRoundTripTime` | `number`<br>*optional* | The current round trip time (RTT) for this candidate pair in seconds. |
| `availableOutgoingBitrate` | `number`<br>*optional* | The available outgoing bitrate (in bits per second) for this candidate pair. |
| `availableIncomingBitrate` | `number`<br>*optional* | The available incoming bitrate (in bits per second) for this candidate pair. |
| `requestsReceived` | `number`<br>*optional* | The number of ICE connection requests received by this candidate pair. |
| `requestsSent` | `number`<br>*optional* | The number of ICE connection requests sent by this candidate pair. |
| `responsesReceived` | `number`<br>*optional* | The number of ICE connection responses received by this candidate pair. |
| `responsesSent` | `number`<br>*optional* | The number of ICE connection responses sent by this candidate pair. |
| `consentRequestsSent` | `number`<br>*optional* | The number of ICE connection consent requests sent by this candidate pair. |
| `packetsDiscardedOnSend` | `number`<br>*optional* | The number of packets discarded while attempting to send via this candidate pair. |
| `bytesDiscardedOnSend` | `number`<br>*optional* | The total number of bytes discarded while attempting to send via this candidate pair. |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


### CertificateStats

A DTLS certificate (`certificate`).

| Field | Type | Description |
|---|---|---|
| `timestamp` | `number` | The timestamp of the stat. |
| `id` | `string` | A unique identifier for the stat. |
| `fingerprint` | `string`<br>*optional* | The fingerprint of the certificate. |
| `fingerprintAlgorithm` | `string`<br>*optional* | The algorithm used for the fingerprint (e.g., 'SHA-256'). |
| `base64Certificate` | `string`<br>*optional* | The certificate encoded in base64 format. |
| `issuerCertificateId` | `string`<br>*optional* | The certificate ID of the issuer. |
| `attachments` | `Record<string, unknown>`<br>*optional* | Additional information attached to this stats |


## Application-level payloads


### ClientEvent

A discrete thing that happened on the client (joined, track added, ICE state change, …).

| Field | Type | Description |
|---|---|---|
| `type` | `string` | The name of the event used as an identifier (e.g., MEDIA_TRACK_MUTED, USER_REJOINED, etc.). |
| `payload` | `Record<string, unknown>`<br>*optional* | Free-form JSON associated with the event. Was a pre-serialised string before 3.5.0, a flat record of primitives in 3.5.0–3.6.0 **`changed in 3.7.0`** |
| `timestamp` | `number`<br>*optional* | The timestamp in epoch format when the event was generated. |


### ClientIssue

A problem state reported by the client, with an optional `key` tying a raise to its resolution.

| Field | Type | Description |
|---|---|---|
| `type` | `string` | The name of the issue |
| `key` | `string`<br>*optional* | Identifier of the related issue or resolution when it is provided. **`new in 3.3.0`** |
| `payload` | `Record<string, unknown>`<br>*optional* | Free-form JSON associated with the issue **`changed in 3.7.0`** |
| `timestamp` | `number`<br>*optional* | The timestamp in epoch format when the event was generated. |


### ClientMetaData

Environment and device information (browser, OS, media devices, SDP, …).

| Field | Type | Description |
|---|---|---|
| `type` | `string` | The name of the event used as an identifier (e.g., MEDIA_TRACK_MUTED, USER_REJOINED, etc.). |
| `payload` | `Record<string, unknown>`<br>*optional* | Free-form JSON associated with the meta item **`changed in 3.7.0`** |
| `peerConnectionId` | `string`<br>*optional* | The unique identifier of the peer connection for which the event was generated. |
| `trackId` | `string`<br>*optional* | The identifier of the media track related to the event, if applicable. |
| `ssrc` | `number`<br>*optional* | The SSRC (Synchronization Source) identifier associated with the event, if applicable. |
| `timestamp` | `number`<br>*optional* | The timestamp in epoch format when the event was generated. |


### ExtensionStat

Free-form application statistics carried alongside the WebRTC stats.

| Field | Type | Description |
|---|---|---|
| `type` | `string` | The type of the extension stats the custom app provides |
| `payload` | `Record<string, unknown>`<br>*optional* | Free-form JSON provided by the application **`changed in 3.7.0`** |


## Notes on selected fields

### `payload` fields are free-form JSON, and have been through three shapes

`ClientEvent.payload`, `ClientIssue.payload`, `ClientMetaData.payload` and `ExtensionStat.payload`
are `Record<string, unknown>` as of **3.7.0**, so a payload may nest objects and arrays freely —
structured context such as `{ device: { os: { name, version } } }` no longer has to be flattened
into dotted keys or stringified into one field.

| Generation | Payload shape |
|---|---|
| pre-3.5.0 | A pre-serialised JSON **string** |
| 3.5.0 – 3.6.0 | A flat record of primitives — `Record<string, boolean \| string \| number>` |
| 3.7.0 | Free-form JSON — `Record<string, unknown>` |

**A fleet does not have to move in step.** `observer-js` passes an object through untouched and
parses a string, so an old client and a new one produce the same object downstream.

**Reading a payload value now needs narrowing**: `payload.role` was `boolean | string | number` and
is `unknown`, so `String(payload.role)` or a type guard replaces a bare read. Writers need no
change — everything that was valid before still is.

### `attachments` is free-form JSON too

It has been `Record<string, unknown>` since it stopped being a string, and it is the model the
payload fields caught up with in 3.7.0.

### Non-finite numbers are rejected, not silently nulled

Both codecs walk an opaque value before copying it and reject a `NaN`, an `Infinity` or a `bigint`
anywhere inside a payload or `attachments`, reporting the path that reached it. `JSON.stringify`
would have turned the first two into `null` without complaint.

### ECN and RFC 8888 counters

`packetsReceivedWithEct1`, `packetsReceivedWithCe`, `packetsReportedAsLost`,
`packetsReportedAsLostButRecovered`, `packetsSentWithEct1` and `packetsWithBleachedEct1Marking`
support Explicit Congestion Notification and RFC 8888 congestion control feedback. They are only
populated by browsers that implement L4S-style congestion signalling — treat them as optional
everywhere.

### `IceCandidatePairStats.state`

The schema keeps two values that are no longer in the W3C enum, so older clients keep validating:
`new` (never standardised) and `cancelled` (removed after
[w3c/webrtc-stats#66](https://github.com/w3c/webrtc-stats/issues/66)). The current spec values are
`frozen`, `waiting`, `in-progress`, `failed`, `succeeded`.
