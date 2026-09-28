---
title: "Architecture"
slug: "architecture"
description: "Browser diagnostics, sample transport and server-side call analysis."
lead: "What runs in the browser, what reaches the server, and where your application takes over."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 20
toc: true
---

ObserveRTC adds a monitoring pipeline beside your existing WebRTC application. **Client Monitor** diagnoses an endpoint. **Observer** combines samples from multiple endpoints into a live view of calls and their issues.

```text
 BROWSER                         YOUR BACKEND
+----------------------+        +-----------------------------+
| Client Monitor       |        | Observer                    |
|                      |        |                             |
| getStats()           | sample | Live calls, clients, tracks  |
|   -> adapt           +------->| Client issue lifecycles      |
|   -> derive metrics  |  via   | Cross-client analysis        |
|   -> detect issues   |  API   | Publisher / receiver links   |
|   -> score quality   |        +--------------+--------------+
+----------+-----------+                       |
           | local events                      | events / sinks
           v                                   v
+----------------------+        +-----------------------------+
| In-call diagnostics  |        | Your metrics, alerts,       |
| and application UI   |        | storage and reporting       |
+----------------------+        +-----------------------------+
```

The sample arrow carries **telemetry**, not audio or video. Your peer connections, media servers and signaling keep their existing roles.

## Diagnose at the endpoint, correlate on the server

The browser can combine stats with local track state, application intent and a sequence of observations. That is where Client Monitor calculates metrics and decides whether an endpoint condition should raise or resolve an issue.

The server adds scope: which participants have overlapping issues, which publisher their tracks belong to, and whether similar conditions appear across calls. Shared symptoms provide evidence for a cause; they do not automatically prove an infrastructure fault.

| Responsibility | Owner |
|---|---|
| Browser adaptation, interval metrics, endpoint detectors | Client Monitor |
| Sample fields and wire types | ObserveRTC schemas |
| Delivery, authentication and input validation | Your application |
| Live call state, track correlation, cross-client analysis | Observer |
| Persistence, dashboards and actions | Your application, using events and sinks |

## In the browser

Client Monitor attaches to an existing `RTCPeerConnection`, or to mediasoup-client devices and transports. Collection and sampling both default to five seconds, but they are separate operations.

```text
RTCPeerConnection.getStats()
            |
            v
Browser adapters -> linked monitor graph
                         |
                         +--> interval metrics
                         +--> detectors -> issues / events
                         +--> quality scores
                         |
                         v
                   createSample()
                         |
                         v
                    ClientSample
```

The graph links RTP streams to tracks, codecs, remote reports and ICE transports. A track can have multiple outbound encodings; a peer connection can have multiple transports.

Local code can read metrics after `stats-collected` and react to issue events without sending samples anywhere. ObserveRTC reports conditions; your application chooses whether to update a quality indicator, prompt the user or change media settings.

**A sample contains selected state, not every live monitor property.** Explicit `createSample()` methods project counters, references, scores and attachments, together with buffered events, issues, metadata and extension stats. Most derived rates, detector state and declared context stay local. Sampling less often does not create an average of the intervening collections.

[Monitor graph and API](/docs/client-monitor-js/api-reference/) · [Collection and sampling](/docs/client-monitor-js/sampling/) · [Metric calculations](/docs/client-monitor-js/metrics/)

## Across the wire

`ClientSample` is the shared contract. It can travel as ordinary JSON, or through an optional delta codec. The schema defines the record; it is not another processing service.

```text
ClientSample -> JSON ----------------------------> ClientSample

ClientSample -> delta encoder -> your transport
                                      |
                                      v
                               delta decoder ----> ClientSample
                                                       |
                                                       v
                                                Observer.accept()
```

| Representation | Integration choice |
|---|---|
| Plain JSON sample | Send complete samples through your existing telemetry endpoint. |
| [JSON codec](/docs/samples-json-codec/) | Encode changes between samples in a JSON representation. |
| [Protobuf codec](/docs/samples-protobuf-codec/) | Encode changes between samples in a binary representation. |

Both delta codecs keep state. Use one encoder per client and one decoder per client stream; preserve message order and reliable delivery. Decode before passing a sample to Observer.

Your ingestion boundary authenticates the sender, validates the payload and checks call/client identity. `Observer.accept()` requires `callId` and `clientId`, but does not perform complete schema validation. In the documented Observer 1.0.0 implementation, middleware cannot be relied on to drop or replace samples; filter before calling `accept()`.

[ClientSample fields](/docs/schema/clientsample/) · [Ingestion behavior](/docs/observer-js/ingestion/)

## On the server

Observer creates entities as samples arrive and maintains their current state in memory:

```text
Observer
+-- ObservedCall
|   +-- ObservedClient
|   |   +-- ObservedPeerConnection
|   |       +-- Tracks and RTP streams
|   |       +-- Remote RTP reports
|   |       +-- ICE transports, pairs and candidates
|   |       +-- Codecs, media sources and playout
|   |       +-- Data channels and certificates
|   +-- ObservedClient
+-- ObservedCall
```

Peer-connection updates create, refresh and clean up child entities. Idle clients and empty calls have configurable timeouts. This model is live state, not a historical database.

Client issue records with matching keys let Observer maintain active issue intervals. The central event bus includes the relevant call, client and entity ancestry in its payloads.

A new Observer has **no detectors registered**. Register the analysis your application needs:

- **Call detectors** compare participants, linked tracks and issue overlap within a call.
- **Observer detectors** analyze populations and patterns across calls.
- **Validators** gather evidence for a structural check, then report a result when they can decide.

Analysis runs on updates, not on a separate universal detector timer. When disabling automatic updates, your application must drive them explicitly.

[Entities and state](/docs/observer-js/entities/) · [Server detectors](/docs/observer-js/detectors/) · [Event bus](/docs/observer-js/event-bus/)

## Publisher, SFU and receiver

To explain a delivery problem, Observer needs to know which outbound track feeds which receivers. A `RemoteTrackResolver` supplies that relationship using identifiers from your signaling and track attachments.

```text
Publisher                 Media path                 Receivers
outbound track -----------> SFU --------------------> inbound track
                             +----------------------> inbound track

              Signaling IDs / track attachments
                             |
                             v
                      RemoteTrackResolver
                             |
                             v
             Observer links publisher to receivers
```

The mediasoup resolver uses producer/consumer identifiers. Other SFUs need an appropriate resolver; matching browser stats IDs alone is not a general publisher-to-receiver mapping.

For mediasoup, Observer can also attach to a live server `Router`. This supplies transport, producer and consumer lifecycle data in a separate `MediasoupRouterSample`. It complements client samples rather than replacing them. Your application decides when and where to persist it.

[SFU integration](/docs/observer-js/sfu/)

## Choose your deployment

Start with the smallest pipeline that answers your question. These can grow independently.

```text
Local diagnostics
  Client Monitor -> in-call UI

Support history
  Client Monitor -> your endpoint -> stored samples

Live call analysis
  Client Monitor -> your endpoint -> Observer -> events / alerts
                         |               |
                         v               v
                   sample archive   call summaries
```

For full-stack deployments, per-client sinks can persist accepted samples and opt-in call summaries can record selected call-level results. Your application owns storage, retention and downstream actions.

Archived samples are useful for later analysis, but a fast replay is not timing-equivalent to live ingestion: some Observer rates use server arrival intervals. Account for those timing rules when comparing replay results.

[Sinks and persistence](/docs/observer-js/sinks/) · [Call summaries](/docs/observer-js/call-summaries/) · [Try the live example](https://webrtc-observer.org/)

## Implementation sources

This architecture follows the released versions listed in [Versions & compatibility](/docs/reference/versions/).

- [ClientMonitor: collection and sample creation](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts)
- [ClientSample: authoritative schema](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/samples/ClientSample.avsc)
- [Observer: ingestion and registration](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts)
- [ObservedClient: sample processing and timing](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts)
- [Remote track resolver factories](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/resolvers/RemoteTrackResolverFactories.ts)
- [Mediasoup router observation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedMediasoupRouter.ts)
