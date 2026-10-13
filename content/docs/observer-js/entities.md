---
slug: "entities"
title: "Calls, clients, and tracks"
description: "Live state follows the call, client and peer-connection hierarchy."
lead: "Live state follows the call, client and peer-connection hierarchy."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "Markdown"]
weight: 40
toc: true
---

An entity is the live representation of something in a call: a participant, a connection, or a media stream. Start at the call when investigating a meeting, then follow the client and track that show the symptom.

## Entity hierarchy

```text
Observer
└── ObservedCall
    └── ObservedClient
        └── ObservedPeerConnection
            ├── inbound / outbound tracks and RTP
            ├── remote inbound / outbound RTP
            ├── ICE transports, pairs and candidates
            ├── codecs, media sources and playout
            └── data channels and certificates
```

## Lifecycle and identity

Entities are created lazily from accepted samples. Sub-entity cleanup uses visited bookkeeping. Live state can disappear; persist samples or summaries if you need history.

RTP maps commonly use SSRC, tracks use track IDs, and other objects use browser stat IDs. Preserve each identifier's scope when correlating clients.

## Rates and scores

Client-level rates use the server arrival interval. RTP entities have their own timestamp processing. Replaying samples as fast as possible does not reproduce live client-level bitrates.

Client scores arrive in samples. Call scoring uses a weighted arithmetic mean of client scores, unlike the client calculator's RMSE across quality dimensions.

Sources: [ObservedCall](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedCall.ts), [ObservedClient](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts), [ObservedPeerConnection](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedPeerConnection.ts), [call scoring](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/scores/DefaultCallScoreCalculator.ts).

## Client session totals

Use `ObservedClient` session totals when you need a participant-level summary rather than its most recent sample. They accumulate across the session and survive peer connection closure.

| Evidence | Fields and interpretation |
|---|---|
| Round-trip time | `totalRttSumInMs`, `numberOfRttMeasurements`, `minRttInMs`, `maxRttInMs`, and `rttHistogram`; 50 buckets of 20 ms, with the final bucket covering 980 ms and above. |
| RTT summary | `rttSummary` returns a frozen, cached object with `p50`, `p75`, `p95`, `p99`, and `avg`. |
| Quality score | `scoreHistogram` uses five one-point buckets across 0–5; `minScore` and `maxScore` retain extrema. Zero scores count as measurements. |
| Score summary | `scoreSummary` returns a frozen, cached object with `p5`, `p25`, `p50`, `p75`, `p95`, and `avg`. |
| Issues | `issueHistogram` counts raises by base issue type; resolutions and re-raises of an already-open keyed issue do not add a count. `totalNumberOfIssues` is the sum. |
| Traffic | Packet-loss/received/sent counters, audio/video bytes, transport bytes, and data-channel totals describe accumulated activity. |
| Path | `numberOfSamplesOverUdp`, `numberOfSamplesOverTcp`, `numberOfSamplesOverTurnUdp`, `numberOfSamplesOverTurnTcp`, and `numberOfSamplesWithUnknownPath` count samples, not elapsed time. Relay TCP/TLS classification uses `relayProtocol`. |
| Changes and peaks | `numberOfPublicAddressChanges`, `peakSendingBitrate`, and `peakReceivingBitrate`. |

Histogram percentiles are bucket-based estimates, not exact percentiles of retained raw observations. `percentileOfHistogram()` can calculate percentiles from histograms combined across clients; keep bucket widths and units consistent. A session summary does not replace an archived sample timeline when investigating when a problem occurred.

## Audio evidence

`ObservedInboundRtp` exposes `audioLevel`, `totalAudioEnergy`, `totalSamplesDuration`, per-tick energy/duration deltas, and `rmsAudioLevel`. `ObservedMediaSource` also exposes energy/duration deltas and RMS level. An outbound track's `rmsAudioLevel` uses its media source when available, otherwise the receivers' median; `rmsAudioLevelSource` identifies the source. `receivedRmsAudioLevel` and `audioInputDevice` add receiver and capture-device context.

`ObservedClient.audioInputDevices` is keyed by track ID and populated from `AUDIO_INPUT_DEVICE` client metadata when supplied. Missing metadata is not evidence that no capture device exists.

Source: [Observer 1.2.0 contracts](https://github.com/ObserveRTC/observer-js/releases/tag/1.2.0).
