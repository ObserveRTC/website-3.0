---
title: "Entities & API reference"
description: "Observer, call, client, peer connection — members, metrics and methods"
lead: "A live, queryable tree created lazily from the samples you feed in"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 330
toc: true
---

## The hierarchy

| Class | Created by | Keyed on its parent as | Holds |
|---|---|---|---|
| `Observer` | `new Observer(config?)` | — (root) | `observedCalls`, global counters, the event bus |
| `ObservedCall` | `observer.createObservedCall(settings)` / lazily by `accept` | `observedCalls` | `observedClients`, call-wide metrics, `detectors`, `scoreCalculator` |
| `ObservedClient` | `call.createObservedClient(settings)` / lazily | `observedClients` | `observedPeerConnections`, per-client metrics |
| `ObservedPeerConnection` | lazily, from `sample.peerConnections[]` | `observedPeerConnections` | the 15 sub-stat maps, transport/RTT/bitrate metrics |
| Sub-stats | lazily, from the `PeerConnectionSample` | maps on the PC | individual WebRTC stat objects |

`ObservedPeerConnection` holds fifteen `public readonly` sub-stat maps:

```text
observedCertificates, observedCodecs, observedDataChannels,
observedIceCandidates, observedIceCandidatesPair, observedIceTransports,
observedInboundRtps, observedInboundTracks, observedMediaPlayouts,
observedMediaSources, observedOutboundRtps, observedOutboundTracks,
observedPeerConnectionTransports, observedRemoteInboundRtps, observedRemoteOutboundRtps
```

Each sub-stat class mirrors the corresponding stat fields from the schema plus derived fields
(deltas, bitrates).

## `Observer`

```typescript
new Observer<AppData>(config?: ObserverConfig<AppData>)

type ObserverConfig<AppData = Record<string, unknown>> = {
    // a call updates when any client does; the observer when any call does. Default true.
    autoUpdateOnCallUpdate?: boolean;
    appData?: AppData;
    closeClientIfIdleForMs?: number;
    closeCallIfEmptyForMs?: number;

    // accumulate a per-call summary. Absent or null = off, and nothing subscribes
    // to anything. `{}` is valid: a summary with no built-in sections.
    callSummary?: Partial<CallSummaryConfig> | null;

    // appData factories — run when an entity is created without explicit appData
    // (including lazily by accept()). The accept context is offered, never written across.
    createCallAppData?: (p: { callId: string; observer: Observer; acceptCtx?: AcceptContext }) => Record<string, unknown>;
    createClientAppData?: (p: { clientId: string; observedCall: ObservedCall; acceptCtx?: AcceptContext }) => Record<string, unknown>;

    // per-client sink factory
    createClientSink?: (p: { clientId: string; observedCall: ObservedCall }) => ClientSampleSink | undefined;

    // a call's RemoteTrackResolver
    createRemoteTrackResolver?: (observedCall: ObservedCall) => RemoteTrackResolver | undefined;
};
```

### Key members

```typescript
observer.accept(sample, context?);

observer.addAcceptMiddleware(...mw);      // global pre-dispatch hooks
observer.removeAcceptMiddleware(...mw);

observer.getObservedCall<T>(callId);
observer.createObservedCall<T>(settings, acceptCtx?);
observer.getOrCreateObservedCall<T>(settings, acceptCtx?);

observer.addIssue(issue);                 // observer-level finding → 'observer-issue'; `scope` is stamped
observer.update();                        // force an aggregation tick

observer.addObserverDetector(name, config?);        // chainable
observer.addCallDetector(name, config?);            // applies to calls created from now on
observer.removeObserverDetector(name);              // → how many instances went
observer.removeCallDetector(name, { includeOpenCalls? });
observer.addValidator(name, config?);
observer.cancelValidator(nameOrInstance, reason?);

observer.close();
```

### Key properties

| Property | What it holds |
|---|---|
| `detectors` | The observer-scoped registry. **Starts empty**; nothing is implicit |
| `callDetectorConfigs` | `Map<name, config>` — what `addCallDetector` recorded |
| `callSummaryCollector?` | Owns the resolved `config.callSummary` and the summaries. `undefined` when summaries are off — the only place that answer lives |
| `validators` | The set currently running; normally empty, since each removes itself on finishing |
| `activeIssuesRegistry` | The fleet's open client issues |
| `observedCalls` | `Map<string, ObservedCall>` |
| `observedTURN` | The fleet's TURN view |
| `appData`, `numberOfCalls` | |
| counters | `numberOfClients`, `numberOfClientsUsingTurn`, `numberOfInboundRtpStreams`, `numberOfOutboundRtpStreams`, `numberOfDataChannels`, `numberOfPeerConnections`, `totalAddedCall`, `totalRemovedCall`, `closed` |

## `ObservedCall`

```typescript
type ObservedCallSettings<AppData = Record<string, unknown>> = {
    autoUpdateOnClientUpdate?: boolean;   // default true
    callId: string;
    appData?: AppData;
    closeCallIfEmptyForMs?: number;
};
```

```typescript
call.callId;  call.appData;
call.observedClients;  call.numberOfClients;

call.getObservedClient<T>(clientId);
call.createObservedClient<T>(settings, acceptCtx?);
call.getOrCreateObservedClient<T>(settings, acceptCtx?);

call.addIssue(issue);                     // call-level finding → 'call-issue'
call.addDetector(name, config?);          // this call only
call.removeDetector(name);

call.detectors;                           // empty by default
call.activeIssuesRegistry;                // this call's open client issues, propagating into the observer's
call.unconsumedOutboundTracks;            // Set<ObservedOutboundTrack>, maintained by the resolver
call.remoteTrackResolver?;                // set from createRemoteTrackResolver at call creation
call.summary?;                            // the live record, when summaries are on

call.scoreCalculator;  call.score;  call.calculatedScore;

// aggregates
call.numberOfIssues;  call.numberOfPeerConnections;
call.numberOfInboundRtpStreams;  call.numberOfOutboundRtpStreams;  call.numberOfDataChannels;
call.maxNumberOfClients;  call.clientsUsedTurn;
call.startedAt;  call.endedAt;  call.closedAt;  call.closed;

call.update();  call.close();
```

## `ObservedClient`

```typescript
type ObservedClientSettings<AppData = Record<string, unknown>> = {
    clientId: string;
    appData?: AppData;
    closeClientIfIdleForMs?: number;
};
```

```typescript
client.clientId;  client.appData;  client.call;
client.observedPeerConnections;
client.sink?;                     // the per-client sink, if createClientSink is configured
client.activeIssues;              // ObservedClientIssueRegistry, keyed by issue.key

// Injection — merged into the next sample processing
client.injectEvent(clientEvent);
client.injectIssue(clientIssue);
client.injectMetaData(clientMetaData);
client.injectExtensionStat(extensionStat);
client.injectAttachment(attachments);

// Direct add — processed immediately
client.addIssue(clientIssue);
client.addMetadata(clientMetaData);
client.addExtensionStats(extensionStat);

// Current / derived metrics
client.currentAvgRttInMs;  client.currentMinRttInMs;  client.currentMaxRttInMs;
client.receivingAudioBitrate;  client.receivingVideoBitrate;
client.sendingAudioBitrate;    client.sendingVideoBitrate;
client.usingTURN;  client.usingTCP;
client.availableIncomingBitrate;  client.availableOutgoingBitrate;

// Counts and per-tick deltas
client.numberOfInboundRtpStreams;  client.numberOfOutboundRtpStreams;
client.numberOfInbundTracks;  client.numberOfOutboundTracks;
client.numberOfDataChannels;  client.numberOfPeerConnections;
client.deltaReceivedAudioBytes;  client.deltaSentAudioBytes;  /* … */

// Lifecycle and metadata
client.joinedAt;  client.leftAt;  client.closedAt;  client.closed;  client.score;
client.browser;  client.engine;  client.platform;  client.operationSystem;
client.mediaDevices;  client.mediaConstraints;

client.accept(sample, context?);  client.close();
```

## `ObservedPeerConnection`

```typescript
pc.peerConnectionId;  pc.client;  pc.appData;

// Array getters alongside the fifteen maps
pc.codecs;  pc.inboundRtps;  pc.outboundRtps;
pc.remoteInboundRtps;  pc.remoteOutboundRtps;
pc.mediaSources;  pc.mediaPlayouts;  pc.dataChannels;
pc.peerConnectionTransports;  pc.iceTransports;
pc.iceCandidates;  pc.iceCandidatePairs;  pc.certificates;
pc.selectedIceCandidatePairs;  pc.selectedIceCandiadtePairForTurn;

// State
pc.connectionState;  pc.iceConnectionState;  pc.iceGatheringState;
pc.usingTURN;  pc.usingTCP;

// Metrics
pc.currentRttInMs;  pc.iceRttInMs;  pc.rtcpRttInMs;  pc.sfuHopRttInMs;
pc.currentJitter;
pc.availableIncomingBitrate;  pc.availableOutgoingBitrate;
// …plus sending/receiving bitrates, packet rates, and total* / delta* counters

pc.accept(pcSample, context?);  pc.close();  pc.score;
```

### Two different round trips — do not mix them

{{< callout context="caution" title="iceRttInMs and rtcpRttInMs measure different paths" icon="alert-triangle" >}}
`iceRttInMs` comes from ICE/STUN consent checks and measures the trip to *whatever terminates ICE* —
**in an SFU topology that is the SFU**, so it is the client↔SFU leg. `rtcpRttInMs` comes from RTCP
receiver reports and is an **end-to-end** media-path round trip.

They are not interchangeable, and averaging them produces a number that moves as streams come and go
for reasons unrelated to the network. `currentRttInMs` therefore *prefers* RTCP and falls back to
ICE — always one kind within a tick, never a blend. `sfuHopRttInMs` (`rtcp − ice`) estimates
everything past the SFU, which separates "this client's last mile is slow" from "the path beyond the
SFU is slow".
{{< /callout >}}

### Counter-reset boundaries

Chrome resets an SSRC's cumulative counters when the codec switches
([crbug/webrtc/5361](https://bugs.chromium.org/p/webrtc/issues/detail?id=5361), open since 2015),
which otherwise shows up as a sawtooth spike or a negative bitrate.

`ObservedInboundRtp` / `ObservedOutboundRtp` therefore set **`counterResetBoundary`** on any tick
where `codecId`, `encoder`/`decoderImplementation` or `scalabilityMode` changed, and **suppress every
delta for that tick**. Without this, a room-wide codec rollout fires a synchronized fake-degradation
alert across every participant at once.

### Remote-RTP correlation

During `accept()`, receiver and sender reports are linked to the local streams by `remoteId`
(falling back to SSRC) and surfaced as fields:

- on `ObservedOutboundRtp`: `remoteRttInMs`, `remoteFractionLost`, `remoteJitter`,
  `remotePacketsLost`
- on `ObservedInboundRtp`: `remoteRttInMs`, `remoteBytesSent`, `remotePacketsSent`,
  `remoteTimestamp`

These are reset each tick and only set when the matching remote report is present.

## Call health: `CallHealthAggregator`

The **client** axis. Where the resolver links answer "how was *this source* delivered?", this asks
"how is *each participant* doing, sending vs receiving?"

```typescript
import { CallHealthAggregator } from '@observertc/observer-js';

const health = new CallHealthAggregator(observedCall).aggregate();

health.degradedRatio;          // 0.82 — the number distinguishing shared faults from individual ones
health.inboundDegradedRatio;   // receiving side → egress / downstream suspicion
health.outboundDegradedRatio;  // sending side  → ingress suspicion
health.rttInMs?.median;        // percentile rollups, never means
health.qualityLimitation;      // { cpu, bandwidth, other } client counts
health.clients;                // per-client entries with `reasons`, direction flags, TURN/TCP
```

## Statistics helpers

Exported for building your own detectors and aggregations: `percentile`, `median`, `summarize`,
`counterDelta`, `robustZScore`, `SlidingWindow`, `TrendTester`, and `geohash` /
`GEOHASH_CELL_SIZES` for the geographic grouping axis.

## Schema types

`ClientSample` and friends are re-exported from this package — the same shapes the schema publishes,
so the client and the server always agree. `schemaVersion` is exported too, so an application can
assert which schema generation the build it installed speaks:

```typescript
import { schemaVersion } from '@observertc/observer-js';
console.log(schemaVersion);   // '3.7.0'
```

See the [`ClientSample` reference](/docs/schema/clientsample/) for every field.
