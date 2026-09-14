---
title: "API reference"
slug: "api-reference"
description: "ClientMonitor constructor, methods, properties and events"
lead: "The public surface of @observertc/client-monitor-js 4.9.0"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 290
toc: true
---

## `new ClientMonitor(config?)`

Every configuration field is optional — see [Configuration](../configuration/) for the full object
and its defaults.

```typescript
const monitor = new ClientMonitor(config?: ClientMonitorConfig);
```

`ClientMonitor` and `AppliedClientMonitorConfig` are generic over your `appData` shape.

## Methods

### Sources and lifecycle

| Method | Description |
|---|---|
| `addSource(source)` | Adds an `RTCPeerConnection`, mediasoup `Device` or mediasoup transport |
| `collect()` | Runs one stats collection immediately, outside the timer |
| `createSample()` | Builds a `ClientSample` from current state; requires `bufferingEventsForSamples` when automatic sampling is off |
| `close()` | Stops collection, releases monitors, auto-resolves open issues, emits `'close'` |

### Configuration at runtime

| Method | Description |
|---|---|
| `setCollectingPeriod(periodInMs)` | Changes the stats collection interval |
| `setSamplingPeriod(periodInMs)` | Changes the sampling interval |
| `setScore(score, ownReasons?, aggregatedReasons?)` | Sets the client score directly, bypassing the calculator |
| `setInboundTrackContext(trackId, ctx)` | Declares what the stats cannot reveal about an inbound track |
| `setOutboundTrackContext(trackId, ctx)` | The same for an outbound track |

### Events, issues and metadata

| Method | Description |
|---|---|
| `addEvent(event)` | Records an immutable `ClientEvent` |
| `addIssue({ type, payload?, timestamp? })` | Records a one-shot issue; emits `'issue'`, never enters `activeIssues` |
| `raiseIssue(key, { type, payload?, timestamp? })` | Creates or refreshes a stateful issue; emits `'issue'` or `'issue-updated'` |
| `resolveIssue(key, { comment?, payload?, resolvedAt? })` | Resolves a stateful issue; emits `'issue-resolved'` |
| `getActiveIssuesByType(type?)` | Snapshot of active stateful issues, optionally filtered |
| `isIssueActive(key)` | `true` when an issue with that key is open |
| `addMetaData(metaData)` | Records a `ClientMetaData` item |
| `addExtensionStats(stats)` | Records an `ExtensionStat`; with an `id`, readable back |

### Utilities

| Method | Description |
|---|---|
| `getPeerConnectionMonitor(peerConnectionId)` | Peer connection monitor by id |
| `getTrackMonitor(trackId)` | Track monitor by `MediaStreamTrack` id, either direction |
| `getExtensionStatsMonitor(id)` / `getExtensionStatsPayload(id)` | Reads application stats back off the monitor tree |
| `watchMediaDevices()` | Integrates with `navigator.mediaDevices` |
| `fetchUserAgentData()` | Resolves User-Agent Client Hints into client metadata |

## Properties

| Property | Type | Description |
|---|---|---|
| `score` | `number \| undefined` | Current client score, 0.0–5.0 |
| `scoreReasons` | `Record<string, number> \| undefined` | This entity's own subtractions |
| `scoreCalculator` | `ScoreCalculator` | The implementation in use — assignable |
| `cpuUtilization` | `number \| undefined` | The reading behind `cpulimitation`, published whether or not it raised |
| `createdAt` / `uptimeInMs` | `number` | When this monitor started, and how long it has run |
| `activeTab` | `boolean` | `false` while the tab is backgrounded |
| `closed` | `boolean` | Whether `close()` has been called |
| `config` | `ClientMonitorConfig` | The effective configuration |
| `detectors` | `Detectors` | Client-level detector registry |
| `statsAdapters` | `StatsAdapters` | Registry of stats adapters |
| `extensionStatsProviders` | `Set<ExtensionStatProvider>` | Called on every collection |
| `peerConnections` | `PeerConnectionMonitor[]` | Monitored peer connections |
| `mappedPeerConnections` | `Map<string, PeerConnectionMonitor>` | Same, keyed by id |
| `tracks` | `TrackMonitor[]` | All monitored tracks, both directions |
| `inboundRtps` / `outboundRtps` | `…RtpMonitor[]` | Every RTP monitor across connections |
| `remoteInboundRtps` / `remoteOutboundRtps` | `…RtpMonitor[]` | The far end's reports |
| `iceTransports` / `codecs` / `certificates` | monitor arrays | |
| `mappedExtensionStatsMonitors` | `Map<string, ExtensionStatsMonitor>` | Application stats folded into the tree |
| `activeIssues` | `Map<string, RaisedClientIssue>` | Open stateful issues, keyed by `key` |
| `samplingSchemaVersion` | `string` | The `ClientSample` schema this build emits — `3.7.0` |
| `attachments` | `Record<string, unknown>` | Shipped with every sample |
| `appData` | `Record<string, unknown>` | Local only, never shipped |

Derived client-level metrics (`sendingVideoBitrate`, `avgRttInSec`,
`totalAvailableOutgoingBitrate`, `durationOfCollectingStatsInMs`, …) are documented in
[Monitors & derived metrics](../metrics/).

## Declared track context

Some of what decides a verdict is invisible to `getStats()`.

```typescript
monitor.setInboundTrackContext(trackId, {
    contentType: 'screenshare',     // no frame-rate penalties on static content
    motionType: 'lowmotion',
    videoTag: videoElement,         // presented size, re-measured every tick
    presentedResolution: { width: 1280, height: 720 },   // or declare it directly
    linkedVideoTrackId: videoTrackId,                    // enables AVDesyncPlayoutDetector
    paused: true,
    remoteOutboundTrackPaused: true,
});

monitor.setOutboundTrackContext(trackId, { contentType: 'camera', paused: false });
```

Declarations may be made **before the track exists** — signalling usually announces a guest's screen
share before a packet arrives — and are applied to whichever peer connection first manifests the
track. They **merge** rather than replace: a field the call does not mention keeps its value, and a
field passed as an explicit `undefined` is cleared. Those are different statements.

Outbound `contentType` is auto-detected from `track.getSettings().displaySurface` where the browser
reports one.

## Events

```typescript
type ClientMonitorEvents = {
    // Collection & sampling
    'stats-collected': [{
        clientMonitor: ClientMonitor;
        startedAt: number;
        durationOfCollectingStatsInMs: number;
        collectedStats: [string, RtcStats[]][];
    }];
    'sample-created': [{ clientMonitor: ClientMonitor; sample: ClientSample }];

    // Scoring
    'score': [{ clientMonitor: ClientMonitor; clientScore: number; currentReasons: Record<string, number> }];

    // Issue lifecycle
    'issue':          [ClientIssue];
    'issue-updated':  [RaisedClientIssue];
    'issue-resolved': [ResolvedClientIssue];

    // Application records
    'client-event': [ClientEvent];

    // One entry per detector event — see Events & issues for the full list
    'uplink-congestion':   [UplinkCongestionEventPayload];
    'downlink-congestion': [DownlinkCongestionEventPayload];
    'video-flow-disrupted':[VideoFlowEventPayload];
    // …

    'close': [];
};
```

Every payload but `issue` carries the emitting `clientMonitor`. The complete event table is in
[Events & issues](../events-and-issues/#event-listeners-cheat-sheet).

## Interfaces

### `Detector`

```typescript
interface Detector {
    readonly name: string;
    disabled?: boolean;
    includeIssueInSample?: boolean;
    update(): void;
}
```

Classes that can compute it also expose a public `inputsUnavailable: boolean`. It is deliberately
**not** on the interface — that contract carries only what the registry needs to run a detector and
what an application needs to toggle one — so reading it means naming the class:

```typescript
pcMonitor.detectors.getByName<TransportDelayDetector>('transport-delay-detector')?.inputsUnavailable;
```

### `Detectors`

```typescript
detectors.size;  detectors.listOfNames;
detectors.has(name);  detectors.getByName<T>(name);
detectors.find(pred);  detectors.filter(pred);
detectors.add(detector);  detectors.remove(detector);  detectors.clear();
detectors.disable(name);  detectors.enable(name);  detectors.isEnabled(name);
detectors.disableAll();   detectors.enableAll();
for (const d of detectors) { /* … */ }
```

Registries exist on `ClientMonitor`, `PeerConnectionMonitor`, `IceTransportMonitor`, both track
monitors and `MediaPlayoutMonitor`. **Lookup by `name` is exact and there is no alias table** — a
retired name returns `undefined` / `false`.

### `IssueRegistry`

Every monitor owns the issues raised against it. *(New in 4.9.)*

```typescript
monitorIssues.hasType(type);
monitorIssues.getByType(type);
monitorIssues.getFirstPayloadByType(type);
monitorIssues.size;
```

### `ScoreCalculator`

```typescript
interface ScoreCalculator {
    update(): void;
}
```

That is the whole contract as of 4.9 — the `encode*ScoreReasons` hooks are gone, along with every
other score internal that used to be reachable from outside the package. See
[Scoring](../scoring/#writing-your-own).

### `StatsAdapter`

```typescript
interface StatsAdapter {
    readonly name: string;
    preAdapt?(stats: RtcStats[]): RtcStats[];    // before the built-ins
    postAdapt?(stats: RtcStats[]): RtcStats[];   // after them
}
```

### `ExtensionStatProvider`

```typescript
type ExtensionStatProvider = () =>
    | { type: string; id?: string; payload?: Record<string, unknown> }
    | Promise<{ type: string; id?: string; payload?: Record<string, unknown> }>;
```

### `Logger`

```typescript
interface Logger {
    trace(...args: unknown[]): void;
    debug(...args: unknown[]): void;
    info(...args: unknown[]): void;
    warn(...args: unknown[]): void;
    error(...args: unknown[]): void;
}
```

## Exported types

Each built-in detector's class, its `<ClassName>Config` type and its issue payload type are exported
from the package root, along with the discriminated unions and guards:

```typescript
import {
    ClientMonitor,

    // unions and guards
    ClientMonitorIssue,
    ClientMonitorResolvedIssue,
    ClientMonitorIssueType,
    isClientMonitorIssue,
    isClientMonitorResolvedIssue,

    // a detector, its config type and its payload type
    StuckDecoderDetector,
    StuckDecoderIssuePayload,
} from '@observertc/client-monitor-js';

import type { StuckDecoderDetectorConfig } from '@observertc/client-monitor-js';
```

Shared estimators introduced in 4.9 are exported too: `SlicedWindow`, `DecayingMaxEstimator` and
`FrugalQuantileEstimator`.

{{< callout context="caution" title="Class exports retired in 4.9" icon="alert-triangle" >}}
`IceTupleChangeDetector`, `LongPcConnectionEstablishmentDetector`,
`LongPcConnectionEstablishmentStage` and `NoAvailableIceCandidateDetector` are removed — import
`IceTraversalDetector`, `IcePathEstablishmentDetector`, `IcePathEstablishmentStage` and
`IceReachabilityDetector`. The classes that were *split* (`IcePathStabilityDetector`,
`DtlsHandshakeDetector`, `CaptureFailureDetector`, `MediaPipelineDetector`) never had an alias to
remove: a class that raised four issues cannot be aliased onto one that raises a single one without
lying about what it does. Import the part you meant — see
[What changed in 4.9](../migration-4-9/).
{{< /callout >}}

## Release candidates

Stable releases come from npm as usual. Every push to `develop` publishes a release candidate as
`X.Y.Z-rc.<N>`; depend on the **`next` dist-tag** to track them:

```jsonc
"dependencies": { "@observertc/client-monitor-js": "next" }
```

`next` always points at the newest RC across all version lines, so the dependency never has to be
edited when the line bumps.

{{< callout context="caution" title="A caret range cannot track RCs" icon="alert-triangle" >}}
`"^4.9.0"` resolves to the stable `4.9.0` and silently excludes every RC — a range with no
prerelease in it never matches prerelease versions. `"^4.9.1-rc.5"` does match RCs, but only of
`4.9.1`, so it stops updating the moment the line bumps.
{{< /callout >}}

Full history: [CHANGELOG on GitHub](https://github.com/ObserveRTC/client-monitor-js/blob/master/CHANGELOG.md).
