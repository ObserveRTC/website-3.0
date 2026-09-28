---
slug: "clientsample"
title: "ClientSample field reference"
description: "Every nested record, field type and default from schema 3.7.0."
lead: "Every nested record, field type and default from schema 3.7.0."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 10
toc: true
---

This inventory comes from the actual Avro definitions. A field's presence in this schema does not prove it is a browser-native statistic. Client `createSample()` methods determine the values actually emitted.

Most derived rates, detector state and declared context stay on live monitors. Track samples project identity, kind, timestamp, attachments and score information. Extension entries contain `type` and `payload`; a local extension monitor ID is not transmitted.

[Serialization methods](/reference/monitor-fields-and-formulas.md) · [Generation and compatibility](/docs/schema/general/)

## ClientSample
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/ClientSample.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `callId` | `["null","string"]` | `null` | the unique identifier of the call or session |
| `clientId` | `["null","string"]` | `null` | Unique id of the client providing samples. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this sample (e.g.: roomId, userId, displayName, etc...) |
| `timestamp` | `"long"` | `required` | The timestamp the sample is created in GMT |
| `score` | `["null","double"]` | `null` | Calculated score for client (details should be added to scoreReasons) |
| `scoreReasons` | `["null",{"type":"map","values":"double"}]` | `null` | Reasons for the score calculation, mapping each reason to how much it contributed to the score |
| `peerConnections` | `["null",{"type":"array","items":"@include-chunk PeerConnectionSample"}]` | `null` | Samples taken PeerConnections |
| `clientEvents` | `["null",{"type":"array","items":{"name":"ClientEvent","type":"record"}}]` | `null` | A list of client events. |
| `clientIssues` | `["null",{"type":"array","items":{"name":"ClientIssue","type":"record"}}]` | `null` | A list of client issues. |
| `clientMetaItems` | `["null",{"type":"array","items":{"name":"ClientMetaData","type":"record"}}]` | `null` | A list of additional client events. |
| `extensionStats` | `["null",{"type":"array","items":{"name":"ExtensionStat","type":"record"}}]` | `null` | The WebRTC app provided custom stats payload |

## ClientEvent
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/ClientSample.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `type` | `"string"` | `required` | The name of the event used as an identifier (e.g., MEDIA_TRACK_MUTED, USER_REJOINED, etc.). |
| `payload` | `["null",{"type":"map","values":{"name":"AnyValue","type":"record"}}]` | `null` | The attributes of the event, if applicable. |
| `timestamp` | `["null","long"]` | `null` | The timestamp in epoch format when the event was generated. |

## AnyValue
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/ClientSample.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `boolValue` | `["null","boolean"]` | `null` |  |
| `stringValue` | `["null","string"]` | `null` |  |
| `numberValue` | `["null","double"]` | `null` |  |
| `objectValue` | `["null",{"type":"map","values":"AnyValue"}]` | `null` |  |
| `arrayValue` | `["null",{"type":"array","items":"AnyValue"}]` | `null` |  |

## ClientIssue
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/ClientSample.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `type` | `"string"` | `required` | The name of the issue |
| `key` | `["null","string"]` | `null` | Identifier of the related issue or resolution when it is provided. |
| `payload` | `["null",{"type":"map","values":"AnyValue"}]` | `null` | The attributes of the issue, if applicable. |
| `timestamp` | `["null","long"]` | `null` | The timestamp in epoch format when the event was generated. |

## ClientMetaData
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/ClientSample.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `type` | `"string"` | `required` | The name of the event used as an identifier (e.g., MEDIA_TRACK_MUTED, USER_REJOINED, etc.). |
| `payload` | `["null",{"type":"map","values":"AnyValue"}]` | `null` | The attributes of the meta data entry, if applicable. |
| `peerConnectionId` | `["null","string"]` | `null` | The unique identifier of the peer connection for which the event was generated. |
| `trackId` | `["null","string"]` | `null` | The identifier of the media track related to the event, if applicable. |
| `ssrc` | `["null","long"]` | `null` | The SSRC (Synchronization Source) identifier associated with the event, if applicable. |
| `timestamp` | `["null","long"]` | `null` | The timestamp in epoch format when the event was generated. |

## ExtensionStat
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/ClientSample.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `type` | `"string"` | `required` | The type of the extension stats the custom app provides |
| `payload` | `["null",{"type":"map","values":"AnyValue"}]` | `null` | The payload of the extension stats the custom app provides |

## PeerConnectionSample
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `peerConnectionId` | `"string"` | `required` | Unique identifier of the stats object. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this sample |
| `score` | `["null","double"]` | `null` | Calculated score for peer connection (details should be added to scoreReasons) |
| `scoreReasons` | `["null",{"type":"map","values":"double"}]` | `null` | Reasons for the score calculation, mapping each reason to how much it contributed to the score |
| `inboundTracks` | `["null",{"type":"array","items":{"type":"record","name":"InboundTrackSample"}}]` | `null` | Inbound Track Stats items |
| `outboundTracks` | `["null",{"type":"array","items":{"type":"record","name":"OutboundTrackSample"}}]` | `null` | Outbound Track Stats items |
| `codecs` | `["null",{"type":"array","items":{"type":"record","name":"CodecStats"}}]` | `null` | Codec items |
| `inboundRtps` | `["null",{"type":"array","items":{"name":"InboundRtpStats","type":"record"}}]` | `null` | Inbound RTP Stats |
| `remoteInboundRtps` | `["null",{"type":"array","items":{"name":"RemoteInboundRtpStats","type":"record"}}]` | `null` | Remote Inbound RTP Stats |
| `outboundRtps` | `["null",{"type":"array","items":{"name":"OutboundRtpStats","type":"record"}}]` | `null` | Outbound RTP Stats |
| `remoteOutboundRtps` | `["null",{"type":"array","items":{"name":"RemoteOutboundRtpStats","type":"record"}}]` | `null` | Remote Outbound RTP Stats |
| `mediaSources` | `["null",{"type":"array","items":{"name":"MediaSourceStats","type":"record"}}]` | `null` | Audio Source Stats |
| `mediaPlayouts` | `["null",{"type":"array","items":{"name":"MediaPlayoutStats","type":"record"}}]` | `null` | Media Playout Stats |
| `peerConnectionTransports` | `["null",{"type":"array","items":{"name":"PeerConnectionTransportStats","type":"record"}}]` | `null` | PeerConnection Transport Stats |
| `dataChannels` | `["null",{"type":"array","items":{"name":"DataChannelStats","type":"record"}}]` | `null` | Data Channels Stats |
| `iceTransports` | `["null",{"type":"array","items":{"name":"IceTransportStats","type":"record"}}]` | `null` | ICE Transport Stats |
| `iceCandidates` | `["null",{"type":"array","items":{"name":"IceCandidateStats","type":"record"}}]` | `null` | ICE Candidate Stats |
| `iceCandidatePairs` | `["null",{"type":"array","items":{"name":"IceCandidatePairStats","type":"record"}}]` | `null` | ICE Candidate Pair Stats |
| `certificates` | `["null",{"type":"array","items":{"name":"CertificateStats","type":"record"}}]` | `null` | Certificate Stats |

## InboundTrackSample
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp when the stats were generated. |
| `id` | `"string"` | `required` | The unique identifier for the stats object. |
| `kind` | `"string"` | `required` | Kind of the media (e.g., 'audio' or 'video'). |
| `score` | `["null","double"]` | `null` | Calculated score for track (details should be added to scoreReasons) |
| `scoreReasons` | `["null",{"type":"map","values":"double"}]` | `null` | Reasons for the score calculation, mapping each reason to how much it contributed to the score |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## OutboundTrackSample
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp when the stats were generated. |
| `id` | `"string"` | `required` | The unique identifier for the stats object. |
| `kind` | `"string"` | `required` | Kind of the media (e.g., 'audio' or 'video'). |
| `score` | `["null","double"]` | `null` | Calculated score for track (details should be added to scoreReasons) |
| `scoreReasons` | `["null",{"type":"map","values":"double"}]` | `null` | Reasons for the score calculation, mapping each reason to how much it contributed to the score |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## CodecStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp when the stats were generated. |
| `id` | `"string"` | `required` | The unique identifier for the stats object. |
| `payloadType` | `["null","int"]` | `null` | The payload type of the codec. |
| `transportId` | `["null","string"]` | `null` | The identifier of the transport associated with the codec. |
| `mimeType` | `"string"` | `required` | The MIME type of the codec. |
| `clockRate` | `["null","int"]` | `null` | The clock rate of the codec in Hz. |
| `channels` | `["null","int"]` | `null` | The number of audio channels for the codec, if applicable. |
| `sdpFmtpLine` | `["null","string"]` | `null` | The SDP format-specific parameters line for the codec. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## InboundRtpStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The time the stats were collected, in high-resolution time. |
| `id` | `"string"` | `required` | Unique identifier of the stats object. |
| `ssrc` | `"long"` | `required` | Synchronization source identifier of the RTP stream. |
| `kind` | `"string"` | `required` | Kind of the media (e.g., 'audio' or 'video'). |
| `transportId` | `["null","string"]` | `null` | ID of the transport associated with the RTP stream. |
| `codecId` | `["null","string"]` | `null` | ID of the codec used for the RTP stream. |
| `packetsReceived` | `["null","int"]` | `null` | Number of packets received on the RTP stream. |
| `packetsReceivedWithEct1` | `["null","int"]` | `null` | Total number of RTP packets received for this SSRC marked with the ECT(1) marking. |
| `packetsReceivedWithCe` | `["null","int"]` | `null` | Total number of RTP packets received for this SSRC marked with the CE marking. |
| `packetsReportedAsLost` | `["null","int"]` | `null` | Total number of RTP packets for which an RFC8888 report has been sent with a zero R bit. |
| `packetsReportedAsLostButRecovered` | `["null","int"]` | `null` | Total number of RTP packets reported as lost but later recovered in a subsequent RFC8888 report. |
| `packetsLost` | `["null","int"]` | `null` | Number of packets lost on the RTP stream. |
| `jitter` | `["null","double"]` | `null` | Jitter of the RTP stream in seconds. |
| `trackIdentifier` | `"string"` | `required` | Identifier for the media track associated with the RTP stream. |
| `mid` | `["null","string"]` | `null` | The media stream identification tag from the SDP media section. |
| `remoteId` | `["null","string"]` | `null` | Remote stats object ID associated with the RTP stream. |
| `framesDecoded` | `["null","int"]` | `null` | Number of frames decoded. |
| `keyFramesDecoded` | `["null","int"]` | `null` | Number of keyframes decoded. |
| `framesRendered` | `["null","int"]` | `null` | Number of frames rendered. |
| `framesDropped` | `["null","int"]` | `null` | Number of frames dropped. |
| `frameWidth` | `["null","int"]` | `null` | Width of the decoded video frames. |
| `frameHeight` | `["null","int"]` | `null` | Height of the decoded video frames. |
| `framesPerSecond` | `["null","double"]` | `null` | Frame rate in frames per second. |
| `qpSum` | `["null","double"]` | `null` | Sum of the Quantization Parameter values for decoded frames. |
| `totalDecodeTime` | `["null","double"]` | `null` | Total time spent decoding in seconds. |
| `totalInterFrameDelay` | `["null","double"]` | `null` | Sum of inter-frame delays in seconds. |
| `totalSquaredInterFrameDelay` | `["null","double"]` | `null` | Sum of squared inter-frame delays in seconds. |
| `pauseCount` | `["null","int"]` | `null` | Number of times playback was paused. |
| `totalPausesDuration` | `["null","double"]` | `null` | Total duration of pauses in seconds. |
| `freezeCount` | `["null","int"]` | `null` | Number of times playback was frozen. |
| `totalFreezesDuration` | `["null","double"]` | `null` | Total duration of freezes in seconds. |
| `lastPacketReceivedTimestamp` | `["null","double"]` | `null` | Timestamp of the last packet received. |
| `headerBytesReceived` | `["null","long"]` | `null` | Total header bytes received. |
| `packetsDiscarded` | `["null","int"]` | `null` | Total packets discarded. |
| `fecBytesReceived` | `["null","long"]` | `null` | Total bytes received from FEC. |
| `fecPacketsReceived` | `["null","int"]` | `null` | Total packets received from FEC. |
| `fecPacketsDiscarded` | `["null","int"]` | `null` | Total FEC packets discarded. |
| `bytesReceived` | `["null","long"]` | `null` | Total bytes received on the RTP stream. |
| `nackCount` | `["null","int"]` | `null` | Number of NACKs received. |
| `firCount` | `["null","int"]` | `null` | Number of Full Intra Requests received. |
| `pliCount` | `["null","int"]` | `null` | Number of Picture Loss Indications received. |
| `totalProcessingDelay` | `["null","double"]` | `null` | Total processing delay in seconds. |
| `estimatedPlayoutTimestamp` | `["null","double"]` | `null` | Estimated timestamp of playout. |
| `jitterBufferDelay` | `["null","double"]` | `null` | Total jitter buffer delay in seconds. |
| `jitterBufferTargetDelay` | `["null","double"]` | `null` | Target delay for the jitter buffer in seconds. |
| `jitterBufferEmittedCount` | `["null","int"]` | `null` | Number of packets emitted from the jitter buffer. |
| `jitterBufferMinimumDelay` | `["null","double"]` | `null` | Minimum delay of the jitter buffer in seconds. |
| `totalSamplesReceived` | `["null","long"]` | `null` | Total audio samples received. |
| `concealedSamples` | `["null","long"]` | `null` | Number of concealed audio samples. |
| `silentConcealedSamples` | `["null","long"]` | `null` | Number of silent audio samples concealed. |
| `concealmentEvents` | `["null","int"]` | `null` | Number of audio concealment events. |
| `insertedSamplesForDeceleration` | `["null","long"]` | `null` | Number of audio samples inserted for deceleration. |
| `removedSamplesForAcceleration` | `["null","long"]` | `null` | Number of audio samples removed for acceleration. |
| `audioLevel` | `["null","double"]` | `null` | Audio level in the range [0.0, 1.0]. |
| `totalAudioEnergy` | `["null","double"]` | `null` | Total audio energy in the stream. |
| `totalSamplesDuration` | `["null","double"]` | `null` | Total duration of all received audio samples in seconds. |
| `framesReceived` | `["null","int"]` | `null` | Total number of frames received. |
| `decoderImplementation` | `["null","string"]` | `null` | Decoder implementation used for decoding frames. |
| `playoutId` | `["null","string"]` | `null` | Playout identifier for the RTP stream. |
| `powerEfficientDecoder` | `["null","boolean"]` | `null` | Indicates if the decoder is power-efficient. |
| `framesAssembledFromMultiplePackets` | `["null","int"]` | `null` | Number of frames assembled from multiple packets. |
| `totalAssemblyTime` | `["null","double"]` | `null` | Total assembly time for frames in seconds. |
| `retransmittedPacketsReceived` | `["null","int"]` | `null` | Number of retransmitted packets received. |
| `retransmittedBytesReceived` | `["null","long"]` | `null` | Number of retransmitted bytes received. |
| `rtxSsrc` | `["null","long"]` | `null` | SSRC of the retransmission stream. |
| `fecSsrc` | `["null","long"]` | `null` | SSRC of the FEC stream. |
| `totalCorruptionProbability` | `["null","double"]` | `null` | Total corruption probability of packets. |
| `totalSquaredCorruptionProbability` | `["null","double"]` | `null` | Total squared corruption probability of packets. |
| `corruptionMeasurements` | `["null","int"]` | `null` | Number of corruption measurements. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## RemoteInboundRtpStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp for this stats object in DOMHighResTimeStamp format. |
| `id` | `"string"` | `required` | The unique identifier for this stats object. |
| `ssrc` | `"long"` | `required` | The SSRC identifier of the RTP stream. |
| `kind` | `"string"` | `required` | The type of media ('audio' or 'video'). |
| `transportId` | `["null","string"]` | `null` | The ID of the transport used for this stream. |
| `codecId` | `["null","string"]` | `null` | The ID of the codec used for this stream. |
| `packetsReceived` | `["null","int"]` | `null` | The total number of packets received on this stream. |
| `packetsReceivedWithEct1` | `["null","int"]` | `null` | Total number of RTP packets received for this SSRC marked with the ECT(1) marking. |
| `packetsReceivedWithCe` | `["null","int"]` | `null` | Total number of RTP packets received for this SSRC marked with the CE marking. |
| `packetsReportedAsLost` | `["null","int"]` | `null` | Total number of RTP packets for which an RFC8888 report has been sent with a zero R bit. |
| `packetsReportedAsLostButRecovered` | `["null","int"]` | `null` | Total number of RTP packets reported as lost but later recovered in a subsequent RFC8888 report. |
| `packetsLost` | `["null","int"]` | `null` | The total number of packets lost on this stream. |
| `jitter` | `["null","double"]` | `null` | The jitter value for this stream in seconds. |
| `localId` | `["null","string"]` | `null` | The ID of the local object corresponding to this remote stream. |
| `roundTripTime` | `["null","double"]` | `null` | The most recent RTT measurement for this stream in seconds. |
| `totalRoundTripTime` | `["null","double"]` | `null` | The cumulative RTT for all packets on this stream in seconds. |
| `fractionLost` | `["null","double"]` | `null` | The fraction of packets lost on this stream, calculated over a time interval. |
| `roundTripTimeMeasurements` | `["null","long"]` | `null` | The total number of RTT measurements for this stream. |
| `packetsWithBleachedEct1Marking` | `["null","long"]` | `null` | Number of packets with ECT(1) marking that were bleached by a middlebox. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## OutboundRtpStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp for this stats object in DOMHighResTimeStamp format. |
| `id` | `"string"` | `required` | The unique identifier for this stats object. |
| `ssrc` | `"long"` | `required` | The SSRC identifier of the RTP stream. |
| `kind` | `"string"` | `required` | The type of media ('audio' or 'video'). |
| `transportId` | `["null","string"]` | `null` | The ID of the transport used for this stream. |
| `codecId` | `["null","string"]` | `null` | The ID of the codec used for this stream. |
| `packetsSent` | `["null","int"]` | `null` | The total number of packets sent on this stream. |
| `bytesSent` | `["null","long"]` | `null` | The total number of bytes sent on this stream. |
| `mid` | `["null","string"]` | `null` | The media ID associated with this RTP stream. |
| `mediaSourceId` | `["null","string"]` | `null` | The ID of the media source associated with this stream. |
| `remoteId` | `["null","string"]` | `null` | The ID of the remote object corresponding to this stream. |
| `rid` | `["null","string"]` | `null` | The RID value of the RTP stream. |
| `encodingIndex` | `["null","int"]` | `null` | Index of the encoding in the encoding array. |
| `headerBytesSent` | `["null","long"]` | `null` | The total number of header bytes sent on this stream. |
| `retransmittedPacketsSent` | `["null","int"]` | `null` | The number of retransmitted packets sent on this stream. |
| `retransmittedBytesSent` | `["null","long"]` | `null` | The number of retransmitted bytes sent on this stream. |
| `rtxSsrc` | `["null","long"]` | `null` | The SSRC for the RTX stream, if applicable. |
| `targetBitrate` | `["null","double"]` | `null` | The target bitrate for this RTP stream in bits per second. |
| `totalEncodedBytesTarget` | `["null","long"]` | `null` | The total target encoded bytes for this stream. |
| `frameWidth` | `["null","int"]` | `null` | The width of the frames sent in pixels. |
| `frameHeight` | `["null","int"]` | `null` | The height of the frames sent in pixels. |
| `framesPerSecond` | `["null","double"]` | `null` | The number of frames sent per second. |
| `framesSent` | `["null","int"]` | `null` | The total number of frames sent on this stream. |
| `hugeFramesSent` | `["null","int"]` | `null` | The total number of huge frames sent on this stream. |
| `framesEncoded` | `["null","int"]` | `null` | The total number of frames encoded on this stream. |
| `keyFramesEncoded` | `["null","int"]` | `null` | The total number of key frames encoded on this stream. |
| `qpSum` | `["null","long"]` | `null` | The sum of QP values for all frames encoded on this stream. |
| `psnrSum` | `["null",{"type":"record","name":"PsnrSum"}]` | `null` | Cumulative PSNR measurements for Y, U, V components. |
| `psnrMeasurements` | `["null","long"]` | `null` | Total number of PSNR measurements collected. |
| `totalEncodeTime` | `["null","double"]` | `null` | The total time spent encoding frames on this stream in seconds. |
| `totalPacketSendDelay` | `["null","double"]` | `null` | The total delay for packets sent on this stream in seconds. |
| `qualityLimitationReason` | `["null","string"]` | `null` | The reason for any quality limitation on this stream (e.g., 'cpu', 'bandwidth', 'other'). |
| `qualityLimitationDurations` | `["null",{"type":"record","name":"QualityLimitationDurations"}]` | `null` | The duration of quality limitation reasons categorized by type. |
| `qualityLimitationResolutionChanges` | `["null","int"]` | `null` | The number of resolution changes due to quality limitations. |
| `nackCount` | `["null","int"]` | `null` | The total number of NACK packets sent on this stream. |
| `firCount` | `["null","int"]` | `null` | The total number of FIR packets sent on this stream. |
| `pliCount` | `["null","int"]` | `null` | The total number of PLI packets sent on this stream. |
| `encoderImplementation` | `["null","string"]` | `null` | The implementation of the encoder used for this stream. |
| `powerEfficientEncoder` | `["null","boolean"]` | `null` | Indicates whether the encoder is power-efficient. |
| `active` | `["null","boolean"]` | `null` | Indicates whether this stream is actively sending data. |
| `scalabilityMode` | `["null","string"]` | `null` | The scalability mode of the encoder used for this stream. |
| `packetsSentWithEct1` | `["null","long"]` | `null` | Number of packets sent with ECT(1) congestion marking. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats. |

## PsnrSum
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `y` | `"double"` | `required` | PSNR value for the Y (luminance) component. |
| `u` | `"double"` | `required` | PSNR value for the U (chrominance) component. |
| `v` | `"double"` | `required` | PSNR value for the V (chrominance) component. |

## QualityLimitationDurations
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `none` | `"double"` | `required` | Duration of no quality limitation in seconds. |
| `cpu` | `"double"` | `required` | Duration of CPU-based quality limitation in seconds. |
| `bandwidth` | `"double"` | `required` | Duration of bandwidth-based quality limitation in seconds. |
| `other` | `"double"` | `required` | Duration of other quality limitation reasons in seconds. |

## RemoteOutboundRtpStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp for this stats object in DOMHighResTimeStamp format. |
| `id` | `"string"` | `required` | The unique identifier for this stats object. |
| `ssrc` | `"long"` | `required` | The SSRC identifier of the RTP stream. |
| `kind` | `"string"` | `required` | The type of media ('audio' or 'video'). |
| `transportId` | `["null","string"]` | `null` | The ID of the transport used for this stream. |
| `codecId` | `["null","string"]` | `null` | The ID of the codec used for this stream. |
| `packetsSent` | `["null","int"]` | `null` | The total number of packets sent on this stream. |
| `bytesSent` | `["null","long"]` | `null` | The total number of bytes sent on this stream. |
| `localId` | `["null","string"]` | `null` | The ID of the local object corresponding to this stream. |
| `remoteTimestamp` | `["null","double"]` | `null` | The remote timestamp for this stats object in DOMHighResTimeStamp format. |
| `reportsSent` | `["null","int"]` | `null` | The total number of reports sent on this stream. |
| `roundTripTime` | `["null","double"]` | `null` | The current estimated round-trip time for this stream in seconds. |
| `totalRoundTripTime` | `["null","double"]` | `null` | The total round-trip time for this stream in seconds. |
| `roundTripTimeMeasurements` | `["null","int"]` | `null` | The total number of round-trip time measurements for this stream. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## MediaSourceStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp of the stat. |
| `id` | `"string"` | `required` | A unique identifier for the stat. |
| `kind` | `"string"` | `required` | The type of media ('audio' or 'video'). |
| `trackIdentifier` | `["null","string"]` | `null` | The identifier of the media track. |
| `audioLevel` | `["null","double"]` | `null` | The current audio level. |
| `totalAudioEnergy` | `["null","double"]` | `null` | The total audio energy. |
| `totalSamplesDuration` | `["null","double"]` | `null` | The total duration of audio samples. |
| `echoReturnLoss` | `["null","double"]` | `null` | The echo return loss. |
| `echoReturnLossEnhancement` | `["null","double"]` | `null` | The enhancement of echo return loss. |
| `width` | `["null","int"]` | `null` | The width of the video. |
| `height` | `["null","int"]` | `null` | The height of the video. |
| `frames` | `["null","int"]` | `null` | The total number of frames. |
| `framesPerSecond` | `["null","double"]` | `null` | The frames per second of the video. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## MediaPlayoutStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp of the stat. |
| `id` | `"string"` | `required` | A unique identifier for the stat. |
| `kind` | `"string"` | `required` | The kind of media (audio/video). |
| `synthesizedSamplesDuration` | `["null","double"]` | `null` | The duration of synthesized audio samples. |
| `synthesizedSamplesEvents` | `["null","long"]` | `null` | The number of synthesized audio samples events. |
| `totalSamplesDuration` | `["null","double"]` | `null` | The total duration of all audio samples. |
| `totalPlayoutDelay` | `["null","double"]` | `null` | The total delay experienced during audio playout. |
| `totalSamplesCount` | `["null","long"]` | `null` | The total count of audio samples. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## PeerConnectionTransportStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp of the stat. |
| `id` | `"string"` | `required` | A unique identifier for the stat. |
| `dataChannelsOpened` | `["null","int"]` | `null` | The number of data channels opened. |
| `dataChannelsClosed` | `["null","int"]` | `null` | The number of data channels closed. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## DataChannelStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp of the stat. |
| `id` | `"string"` | `required` | A unique identifier for the stat. |
| `label` | `["null","string"]` | `null` | The label of the data channel. |
| `protocol` | `["null","string"]` | `null` | The protocol of the data channel. |
| `dataChannelIdentifier` | `["null","int"]` | `null` | The identifier for the data channel. |
| `state` | `["null","string"]` | `null` | The state of the data channel (e.g., 'open', 'closed'). |
| `messagesSent` | `["null","int"]` | `null` | The number of messages sent on the data channel. |
| `bytesSent` | `["null","long"]` | `null` | The number of bytes sent on the data channel. |
| `messagesReceived` | `["null","int"]` | `null` | The number of messages received on the data channel. |
| `bytesReceived` | `["null","long"]` | `null` | The number of bytes received on the data channel. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## IceTransportStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp of the stat. |
| `id` | `"string"` | `required` | A unique identifier for the stat. |
| `packetsSent` | `["null","long"]` | `null` | The number of packets sent. |
| `packetsReceived` | `["null","long"]` | `null` | The number of packets received. |
| `bytesSent` | `["null","long"]` | `null` | The number of bytes sent. |
| `bytesReceived` | `["null","long"]` | `null` | The number of bytes received. |
| `iceRole` | `["null","string"]` | `null` | The ICE role (e.g., 'controlling', 'controlled'). |
| `iceLocalUsernameFragment` | `["null","string"]` | `null` | The local username fragment for ICE. |
| `dtlsState` | `["null","string"]` | `null` | The DTLS transport state (e.g., 'new', 'connecting', 'connected'). |
| `iceState` | `["null","string"]` | `null` | The ICE transport state (e.g., 'new', 'checking', 'connected'). |
| `selectedCandidatePairId` | `["null","string"]` | `null` | The ID of the selected ICE candidate pair. |
| `localCertificateId` | `["null","string"]` | `null` | The ID of the local certificate. |
| `remoteCertificateId` | `["null","string"]` | `null` | The ID of the remote certificate. |
| `tlsVersion` | `["null","string"]` | `null` | The TLS version used for encryption. |
| `dtlsCipher` | `["null","string"]` | `null` | The DTLS cipher suite used. |
| `dtlsRole` | `["null","string"]` | `null` | The role in the DTLS handshake (e.g., 'client', 'server'). |
| `srtpCipher` | `["null","string"]` | `null` | The SRTP cipher used for encryption. |
| `selectedCandidatePairChanges` | `["null","long"]` | `null` | The number of changes to the selected ICE candidate pair. |
| `ccfbMessagesSent` | `["null","long"]` | `null` | Number of congestion control feedback (CCFB) messages sent on this transport. |
| `ccfbMessagesReceived` | `["null","long"]` | `null` | Number of congestion control feedback (CCFB) messages received on this transport. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats. |

## IceCandidateStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp of the stat. |
| `id` | `"string"` | `required` | A unique identifier for the stat. |
| `transportId` | `["null","string"]` | `null` | The transport ID associated with the ICE candidate. |
| `address` | `["null","string"]` | `null` | The IP address of the ICE candidate. |
| `port` | `["null","int"]` | `null` | The port number of the ICE candidate. |
| `protocol` | `["null","string"]` | `null` | The transport protocol used by the candidate (e.g., 'udp', 'tcp'). |
| `candidateType` | `["null","string"]` | `null` | The type of the ICE candidate (e.g., 'host', 'srflx', 'relay'). |
| `priority` | `["null","long"]` | `null` | The priority of the ICE candidate. |
| `url` | `["null","string"]` | `null` | The URL of the ICE candidate. |
| `relayProtocol` | `["null","string"]` | `null` | The protocol used for the relay (e.g., 'tcp', 'udp'). |
| `foundation` | `["null","string"]` | `null` | A string representing the foundation for the ICE candidate. |
| `relatedAddress` | `["null","string"]` | `null` | The related address for the ICE candidate (if any). |
| `relatedPort` | `["null","int"]` | `null` | The related port for the ICE candidate (if any). |
| `usernameFragment` | `["null","string"]` | `null` | The username fragment for the ICE candidate. |
| `tcpType` | `["null","string"]` | `null` | The TCP type of the ICE candidate (e.g., 'active', 'passive'). |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## IceCandidatePairStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `id` | `"string"` | `required` | The unique identifier for this RTCStats object. |
| `timestamp` | `"long"` | `required` | The timestamp of when the stats were recorded, in milliseconds. |
| `transportId` | `["null","string"]` | `null` | The transport id of the connection this candidate pair belongs to. |
| `localCandidateId` | `["null","string"]` | `null` | The ID of the local ICE candidate in this pair. |
| `remoteCandidateId` | `["null","string"]` | `null` | The ID of the remote ICE candidate in this pair. |
| `state` | `["null",{"type":"enum","name":"RTCStatsIceCandidatePairState","symbols":["new","frozen","inProgress","waiting","failed","succeeded","cancelled"]}]` | `null` | The checklist state of this candidate pair. Values follow the W3C RTCStatsIceCandidatePairState enum (frozen, waiting, in-progress, failed, succeeded). Two further values are accepted for backward compatibility and are not part of the current spec: `new` (never standardised) and `cancelled` (removed from the spec after 2016). |
| `nominated` | `["null","boolean"]` | `null` | Whether this candidate pair has been nominated. |
| `packetsSent` | `["null","int"]` | `null` | The number of packets sent using this candidate pair. |
| `packetsReceived` | `["null","int"]` | `null` | The number of packets received using this candidate pair. |
| `bytesSent` | `["null","long"]` | `null` | The total number of bytes sent using this candidate pair. |
| `bytesReceived` | `["null","long"]` | `null` | The total number of bytes received using this candidate pair. |
| `lastPacketSentTimestamp` | `["null","double"]` | `null` | The timestamp of the last packet sent using this candidate pair. |
| `lastPacketReceivedTimestamp` | `["null","double"]` | `null` | The timestamp of the last packet received using this candidate pair. |
| `totalRoundTripTime` | `["null","double"]` | `null` | The total round trip time (RTT) for this candidate pair in seconds. |
| `currentRoundTripTime` | `["null","double"]` | `null` | The current round trip time (RTT) for this candidate pair in seconds. |
| `availableOutgoingBitrate` | `["null","double"]` | `null` | The available outgoing bitrate (in bits per second) for this candidate pair. |
| `availableIncomingBitrate` | `["null","double"]` | `null` | The available incoming bitrate (in bits per second) for this candidate pair. |
| `requestsReceived` | `["null","int"]` | `null` | The number of ICE connection requests received by this candidate pair. |
| `requestsSent` | `["null","int"]` | `null` | The number of ICE connection requests sent by this candidate pair. |
| `responsesReceived` | `["null","int"]` | `null` | The number of ICE connection responses received by this candidate pair. |
| `responsesSent` | `["null","int"]` | `null` | The number of ICE connection responses sent by this candidate pair. |
| `consentRequestsSent` | `["null","int"]` | `null` | The number of ICE connection consent requests sent by this candidate pair. |
| `packetsDiscardedOnSend` | `["null","int"]` | `null` | The number of packets discarded while attempting to send via this candidate pair. |
| `bytesDiscardedOnSend` | `["null","long"]` | `null` | The total number of bytes discarded while attempting to send via this candidate pair. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |

## CertificateStats
[Source](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/PeerConnectionSample.chunk.avsc)

| Field | Avro type | Default | Description |
|---|---|---|---|
| `timestamp` | `"long"` | `required` | The timestamp of the stat. |
| `id` | `"string"` | `required` | A unique identifier for the stat. |
| `fingerprint` | `["null","string"]` | `null` | The fingerprint of the certificate. |
| `fingerprintAlgorithm` | `["null","string"]` | `null` | The algorithm used for the fingerprint (e.g., 'SHA-256'). |
| `base64Certificate` | `["null","string"]` | `null` | The certificate encoded in base64 format. |
| `issuerCertificateId` | `["null","string"]` | `null` | The certificate ID of the issuer. |
| `attachments` | `["null","string"]` | `null` | Additional information attached to this stats |
