---
slug: "entities"
title: "Entities & state"
description: "Live state follows the call, client and peer-connection hierarchy."
lead: "Live state follows the call, client and peer-connection hierarchy."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
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
