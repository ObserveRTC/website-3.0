---
title: "Entities & API reference"
slug: "entities"
description: "Observer, ObservedCall, ObservedClient, ObservedPeerConnection and their members"
lead: "The in-memory model: what each node holds, and every public member you can read"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 323
toc: true
---

## The hierarchy

| Class | Created by | Keyed on its parent as | Holds |
|---|---|---|---|
| `Observer` | `new Observer(config?)` | — (root) | `observedCalls`, global counters, the event bus |
| `ObservedCall` | `observer.createObservedCall(settings)` or lazily by `accept` | `observedCalls` | `observedClients`, call-wide metrics, `detectors`, `scoreCalculator` |
| `ObservedClient` | `call.createObservedClient(settings)` or lazily | `observedClients` | `observedPeerConnections`, per-client metrics |
| `ObservedPeerConnection` | lazily, from `sample.peerConnections[]` | `observedPeerConnections` | fifteen sub-stat maps, transport / RTT / bitrate metrics |
| Sub-stats | lazily, from the `PeerConnectionSample` | maps on the PC | individual WebRTC stat objects plus derived fields |

The fifteen sub-stat maps on `ObservedPeerConnection`, all `public readonly`:

```text
observedCertificates      observedCodecs             observedDataChannels
observedIceCandidates     observedIceCandidatesPair  observedIceTransports
observedInboundRtps       observedInboundTracks      observedMediaPlayouts
observedMediaSources      observedOutboundRtps       observedOutboundTracks
observedPeerConnectionTransports
observedRemoteInboundRtps observedRemoteOutboundRtps
```

Each sub-stat class (`ObservedInboundRtp`, `ObservedOutboundRtp`, `ObservedInboundTrack`,
`ObservedOutboundTrack`, `ObservedDataChannel`, `ObservedIceCandidate`,
`ObservedIceCandidatePair`, `ObservedIceTransport`, `ObservedCertificate`, `ObservedCodec`,
`ObservedMediaSource`, `ObservedMediaPlayout`, `ObservedPeerConnectionTransport`,
`ObservedRemoteInboundRtp`, `ObservedRemoteOutboundRtp`) mirrors the corresponding
[schema](/docs/schema/clientsample/) fields plus derived deltas and bitrates.

---

## `Observer`

```typescript
new Observer<AppData>(config?: ObserverConfig<AppData>)

type ObserverConfig<AppData = Record<string, unknown>> = {
    // a call updates when any client does; the observer when any call does. Default true.
    autoUpdateOnCallUpdate?: boolean;

    appData?: AppData;

    closeClientIfIdleForMs?: number;
    closeCallIfEmptyForMs?: number;

    // appData factories — run when an entity is created without explicit appData.
    createCallAppData?: (p: { callId: string; observer: Observer }) => Record<string, unknown>;
    createClientAppData?: (p: { clientId: string; observedCall: ObservedCall }) => Record<string, unknown>;

    // per-client sink factory
    createClientSink?: (p: { clientId: string; observedCall: ObservedCall }) => ClientSampleSink | undefined;

    // per-call remote track resolver factory
    createRemoteTrackResolver?: (observedCall: ObservedCall) => RemoteTrackResolver | undefined;
};
```

### Methods

| Method | Description |
|---|---|
| `accept(sample, context?)` | The single ingestion entry point |
| `addAcceptMiddleware(...mw)` / `removeAcceptMiddleware(...mw)` | Global pre-dispatch sample hooks |
| `getObservedCall<T>(callId)` | `ObservedCall<T> \| undefined` |
| `createObservedCall<T>(settings)` | Returns the existing instance (with a warning) on duplicate id |
| `getOrCreateObservedCall<T>(settings)` | Get or create |
| `update()` | Force an aggregation tick and `observer-updated` |
| `addObserverDetector(name, config?)` | Build a cross-call detector onto `observer.detectors`. Chainable |
| `removeObserverDetector(name)` | Remove every instance under that name. Returns the count |
| `addCallDetector(name, config?)` | Register a call-scoped detector for every call created from now on. Chainable |
| `removeCallDetector(name, { includeOpenCalls? })` | Stop building it and, by default, drop it from open calls |
| `addValidator(name, config?)` | Start a one-shot structural check. Chainable |
| `cancelValidator(name \| validator, reason?)` | Stop a running check; it finishes `inconclusive` with the reason |
| `addIssue(issue)` | Raise an observer-level finding → `observer-issue` |
| `createObservedMediasoupRouter(settings)` | Observe a live mediasoup router |
| `close()` | Tear everything down |

### Properties

| Property | Description |
|---|---|
| `observedCalls` | `Map<string, ObservedCall>` |
| `observedTURN` | Aggregated TURN metrics across the fleet |
| `detectors` | Observer-scoped registry. **Starts empty** |
| `callDetectorConfigs` | `Map<name, config>` — what `addCallDetector` recorded |
| `validators` | `Set<RunningValidator>` — normally empty; each removes itself on finishing |
| `activeIssuesRegistry` | The fleet's open client issues |
| `appData` | Application data |
| `numberOfCalls`, `numberOfClients`, `numberOfClientsUsingTurn` | Live counts |
| `numberOfInboundRtpStreams`, `numberOfOutboundRtpStreams` | Live counts |
| `numberOfDataChannels`, `numberOfPeerConnections` | Live counts |
| `totalAddedCall`, `totalRemovedCall` | Cumulative counters |
| `closed` | Whether `close()` has run |

---

## `ObservedCall`

```typescript
type ObservedCallSettings<AppData = Record<string, unknown>> = {
    callId: string;
    appData?: AppData;
    // update this call whenever one of its clients accepts a sample. Default true.
    autoUpdateOnClientUpdate?: boolean;
    closeCallIfEmptyForMs?: number;
};
```

### Members

| Member | Description |
|---|---|
| `callId`, `appData` | Identity |
| `observedClients` | `Map<string, ObservedClient>` |
| `numberOfClients`, `maxNumberOfClients` | Participant counts |
| `getObservedClient<T>(clientId)` | `\| undefined` |
| `createObservedClient<T>(settings)` / `getOrCreateObservedClient<T>(settings)` | `\| undefined` |
| `addIssue(issue: ObserverIssue)` | Raise a call-level finding → `call-issue` |
| `addDetector(name, config?)` | Build a call-scoped detector on this call only. Chainable |
| `removeDetector(name)` | Remove and `close()` it. Returns the count |
| `detectors` | Call-scoped registry, empty by default |
| `activeIssuesRegistry` | This call's open client issues; propagates into the observer's |
| `unconsumedOutboundTracks` | `Set<ObservedOutboundTrack>` — maintained by the resolver |
| `remoteTrackResolver?` | Set from `ObserverConfig.createRemoteTrackResolver` at creation |
| `scoreCalculator`, `score`, `calculatedScore` | Call-level quality |
| `numberOfIssues`, `numberOfPeerConnections` | Aggregates |
| `numberOfInboundRtpStreams`, `numberOfOutboundRtpStreams`, `numberOfDataChannels` | Aggregates |
| `clientsUsedTurn` | `Set<string>` of client ids that relayed |
| `startedAt?`, `endedAt?`, `closedAt?`, `closed` | Lifecycle |
| `update()`, `close()` | Control |

---

## `ObservedClient`

```typescript
type ObservedClientSettings<AppData = Record<string, unknown>> = {
    clientId: string;
    appData?: AppData;
    closeClientIfIdleForMs?: number;
};
```

### Identity and structure

| Member | Description |
|---|---|
| `clientId`, `appData`, `call` | Identity and parent |
| `observedPeerConnections` | `Map<string, ObservedPeerConnection>` |
| `attachments` | Populated from the sample — read it on `client-updated` |
| `sink?` | The per-client [sink](../sinks/), if `createClientSink` is configured |
| `activeIssues` | Live registry of this client's open issues, keyed by `issue.key` |

### Injection API

Queue application data to be merged into the client's sample stream — it updates the live model
**and** reaches the sink. See [Injection](../sinks/#injecting-data-into-a-client).

```typescript
observedClient.injectEvent(event);
observedClient.injectIssue(issue);
observedClient.injectMetaData(meta);
observedClient.injectExtensionStat(stat);
observedClient.injectAttachment({ roomId });
```

Direct-add variants process immediately instead of queueing: `addIssue`, `addMetadata`,
`addExtensionStats`.

### Metrics

| Group | Members |
|---|---|
| RTT | `currentAvgRttInMs?`, `currentMinRttInMs?`, `currentMaxRttInMs?` |
| Bitrates | `receivingAudioBitrate`, `receivingVideoBitrate`, `sendingAudioBitrate`, `sendingVideoBitrate` |
| Capacity | `availableIncomingBitrate`, `availableOutgoingBitrate` |
| Topology | `usingTURN`, `usingTCP` |
| Counts | `numberOfInboundRtpStreams`, `numberOfOutboundRtpStreams`, `numberOfInbundTracks`, `numberOfOutboundTracks`, `numberOfDataChannels`, `numberOfPeerConnections` |
| Deltas | `deltaReceivedAudioBytes`, `deltaSentAudioBytes`, … |
| Environment | `browser?`, `engine?`, `platform?`, `operationSystem?`, `mediaDevices`, `mediaConstraints` |
| Lifecycle | `joinedAt?`, `leftAt?`, `closedAt?`, `closed`, `score` |
| Control | `accept(sample, context?)`, `close()` |

{{< callout context="tip" title="browser / platform are what population detectors group by" icon="rocket" >}}
`ClientPopulationIssueDetector` groups by exactly these fields. They are populated from
`clientMetaItems`, which `client-monitor-js` sends automatically — so this works out of the box as
long as you are not stripping metadata in a middleware.
{{< /callout >}}

---

## `ObservedPeerConnection`

### Members

| Group | Members |
|---|---|
| Identity | `peerConnectionId`, `client`, `appData?` |
| Sub-stat maps | the fifteen `observed*` maps listed above |
| Array getters | `codecs`, `inboundRtps`, `outboundRtps`, `remoteInboundRtps`, `remoteOutboundRtps`, `mediaSources`, `mediaPlayouts`, `dataChannels`, `peerConnectionTransports`, `iceTransports`, `iceCandidates`, `iceCandidatePairs`, `certificates`, `selectedIceCandidatePairs`, `selectedIceCandiadtePairForTurn` |
| State | `connectionState?`, `iceConnectionState?`, `iceGatheringState?`, `usingTURN`, `usingTCP` |
| RTT | `currentRttInMs?`, `iceRttInMs?`, `rtcpRttInMs?`, `sfuHopRttInMs?` |
| Quality | `currentJitter?`, `availableIncomingBitrate`, `availableOutgoingBitrate`, sending/receiving bitrates, packet rates, `total*` and `delta*` byte/packet counters |
| Control | `accept(pcSample, context?)`, `close()`, `score` |

### Two different round trips — do not mix them

{{< callout context="caution" title="iceRttInMs vs rtcpRttInMs" icon="alert-triangle" >}}
`iceRttInMs` comes from ICE/STUN consent checks and measures the trip to **whatever terminates
ICE** — in an SFU topology that is the SFU, so it is the client↔SFU leg.

`rtcpRttInMs` comes from RTCP receiver reports and is an **end-to-end** media-path round trip.

They are not interchangeable, and averaging them produces a number that moves as streams come and
go for reasons unrelated to the network. `currentRttInMs` therefore **prefers RTCP and falls back
to ICE** — always one kind within a tick, never a blend.

`sfuHopRttInMs` (`rtcp − ice`) estimates everything past the SFU, which separates *"this client's
last mile is slow"* from *"the path beyond the SFU is slow"*.
{{< /callout >}}

### Counter-reset boundaries

Chrome resets an SSRC's cumulative counters when the codec switches
([crbug/webrtc/5361](https://bugs.chromium.org/p/webrtc/issues/detail?id=5361), open since 2015),
which otherwise appears as a sawtooth spike or a negative bitrate.

`ObservedInboundRtp` and `ObservedOutboundRtp` set **`counterResetBoundary`** on any tick where
`codecId`, `encoderImplementation` / `decoderImplementation` or `scalabilityMode` changed, and
suppress every delta for that tick.

Without this, a room-wide codec rollout fires a synchronized fake-degradation alert across every
participant at once.

### Remote-RTP correlation

During `accept()`, RTCP receiver and sender reports are linked to the local streams by `remoteId`
(falling back to SSRC) and surfaced as fields. They are reset each tick and only set when the
matching remote report is present.

| On | Fields |
|---|---|
| `ObservedOutboundRtp` | `remoteRttInMs?`, `remoteFractionLost?`, `remoteJitter?`, `remotePacketsLost?` |
| `ObservedInboundRtp` | `remoteRttInMs?`, `remoteBytesSent?`, `remotePacketsSent?`, `remoteTimestamp?` |

---

## Track links

When a [`RemoteTrackResolver`](../sfu/) is configured, tracks carry the publisher ↔ subscriber
links directly:

```typescript
outboundTrack.remoteInboundTracks;      // Set<ObservedInboundTrack> — every subscriber of this source
inboundTrack.remoteOutboundTrack;       // the publisher, or undefined if unlinked
inboundTrack.getInboundRtp();           // that receiver's RTP stats
observedCall.unconsumedOutboundTracks;  // published tracks with no subscriber at all
```

---

## `CallHealthAggregator`

A ready-made per-call rollup along the **client** axis: how is each participant doing, sending
versus receiving?

```typescript
import { CallHealthAggregator } from "@observertc/observer-js";

const health = new CallHealthAggregator(observedCall).aggregate();

health.degradedRatio;          // 0.82 — distinguishes shared faults from individual ones
health.inboundDegradedRatio;   // receiving side → egress / downstream suspicion
health.outboundDegradedRatio;  // sending side  → ingress suspicion
health.rttInMs?.median;        // percentile rollups, never means
health.qualityLimitation;      // { cpu, bandwidth, other } client counts
health.clients;                // per-client entries with reasons, direction flags, TURN/TCP
```

{{< callout context="note" title="Percentiles, not means" icon="info-circle" >}}
Everything here rolls up as percentiles. One participant on a satellite link drags a mean RTT
somewhere useless; the median plus the degraded ratio tells you whether the room is broken or one
person is.
{{< /callout >}}

## Statistics helpers

Exported for building your own aggregations and detectors:

```typescript
import {
    percentile, median, summarize,
    counterDelta, robustZScore,
    SlidingWindow, TrendTester,
} from "@observertc/observer-js";
```
