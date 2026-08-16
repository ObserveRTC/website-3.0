---
title: "API reference"
slug: "api-reference"
description: "ClientMonitor constructor, methods, properties and events"
lead: "The public surface of @observertc/client-monitor-js 4.3.2"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 319
toc: true
---

## `new ClientMonitor(config?)`

Creates a monitor. Every configuration field is optional — see
[Configuration](../configuration/) for the full object and defaults.

```typescript
const monitor = new ClientMonitor(config?: ClientMonitorConfig);
```

## Methods

### Sources and lifecycle

| Method | Description |
|---|---|
| `addSource(source)` | Adds an `RTCPeerConnection`, mediasoup `Device` or mediasoup transport for monitoring |
| `collect()` | Runs one stats collection immediately, outside the timer |
| `createSample()` | Builds a `ClientSample` from current state; requires `bufferingEventsForSamples` when automatic sampling is off |
| `close()` | Stops collection, releases monitors, auto-resolves open issues, emits `'close'` |

### Configuration at runtime

| Method | Description |
|---|---|
| `setCollectingPeriod(periodInMs)` | Changes the stats collection interval |
| `setSamplingPeriod(periodInMs)` | Changes the sampling interval |
| `setScore(score, reasons?)` | Sets the client score directly, bypassing the calculator |

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
| `addExtensionStats(stats)` | Records a one-off `ExtensionStat` |

### Utilities

| Method | Description |
|---|---|
| `getTrackMonitor(trackId)` | Track monitor by `MediaStreamTrack` id |
| `fetchUserAgentData()` | Resolves User-Agent Client Hints into client metadata |

## Properties

| Property | Type | Description |
|---|---|---|
| `score` | `number \| undefined` | Current client score, 0.0–5.0 |
| `scoreReasons` | `Record<string, number> \| undefined` | Penalty breakdown |
| `closed` | `boolean` | Whether `close()` has been called |
| `config` | `ClientMonitorConfig` | The effective configuration |
| `detectors` | `Detectors` | Client-level detector registry |
| `extensionStatsProviders` | `Set<ExtensionStatProvider>` | Providers called on every collection |
| `peerConnections` | `PeerConnectionMonitor[]` | Monitored peer connections |
| `mappedPeerConnections` | `Map<string, PeerConnectionMonitor>` | Same, keyed by id |
| `tracks` | `(InboundTrackMonitor \| OutboundTrackMonitor)[]` | All monitored tracks |
| `activeIssues` | `Map<string, RaisedClientIssue>` | Open stateful issues, keyed by `key` |
| `attachments` | `Record<string, unknown>` | Shipped with every sample |
| `appData` | `Record<string, unknown>` | Local only, never shipped |

Derived client-level metrics (`sendingVideoBitrate`, `avgRttInSec`,
`totalAvailableOutgoingBitrate`, `durationOfCollectingStatsInMs`, …) are documented in
[Monitors & derived metrics](../metrics/).

## Events

```typescript
interface ClientMonitorEvents {
    // Collection & sampling
    "stats-collected": (data: {
        durationOfCollectingStatsInMs: number;
        collectedStats: [string, RTCStats[]][];
    }) => void;
    "sample-created": (sample: ClientSample) => void;

    // Scoring
    "score": (data: { clientScore: number; scoreReasons?: Record<string, number> }) => void;

    // Issue lifecycle
    "issue":          (issue: ClientIssue) => void;
    "issue-updated":  (issue: RaisedClientIssue) => void;
    "issue-resolved": (issue: ResolvedClientIssue) => void;

    // Application records
    "client-event": (event: ClientEvent) => void;

    // Detector-specific
    "congestion":                        (e: CongestionEvent) => void;
    "cpulimitation":                     (e: CpuPerformanceEvent) => void;
    "audio-desync-track":                (e: AudioDesyncEvent) => void;
    "freezed-video-track":               (e: FreezedVideoTrackEvent) => void;
    "dry-inbound-track":                 (e: DryInboundTrackEvent) => void;
    "dry-outbound-track":                (e: DryOutboundTrackEvent) => void;
    "inbound-video-playout-discrepancy": (e: PlayoutDiscrepancyEvent) => void;

    // Lifecycle
    "close": () => void;
}
```

## Interfaces

### `Detector`

```typescript
interface Detector {
    readonly name: string;
    disabled?: boolean;
    update(): void;
}
```

### `StatsAdapter`

```typescript
interface StatsAdapter {
    readonly name: string;
    adapt(stats: RtcStats[]): RtcStats[];        // before monitors update — required
    postAdapt?(stats: RtcStats[]): RtcStats[];   // after monitors update — optional
}
```

Registered on a peer connection monitor, not on the client:

```typescript
peerConnectionMonitor.statsAdapters.add(adapter);
```

### `ExtensionStatProvider`

```typescript
type ExtensionStatProvider = () =>
    | { type: string; payload?: Record<string, unknown> }
    | Promise<{ type: string; payload?: Record<string, unknown> }>;
```

### `ScoreCalculator`

```typescript
interface ScoreCalculator {
    update(): void;
    encodeClientScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
    encodePeerConnectionScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
    encodeInboundAudioScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
    encodeInboundVideoScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
    encodeOutboundAudioScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
    encodeOutboundVideoScoreReasons?<T extends Record<string, number>>(reasons?: T): string;
}
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

## Exported issue payload types

Each built-in detector's payload type is exported from the package root, along with the
discriminated unions and type guards described in [Events & issues](../events-and-issues/):

```typescript
import {
    AudioDesyncIssuePayload,
    CongestionIssuePayload,
    CpuPerformanceIssuePayload,
    DryInboundTrackIssuePayload,
    DryOutboundTrackIssuePayload,
    FreezedVideoTrackIssuePayload,
    PlayoutDiscrepancyIssuePayload,

    ClientMonitorIssue,
    ClientMonitorResolvedIssue,
    isClientMonitorIssue,
    isClientMonitorResolvedIssue,
} from "@observertc/client-monitor-js";
```

## Version notes

{{< details "4.3.2" >}}
`CpuPerformanceDetector` no longer infers inbound CPU limitation from frame-rate volatility, which
false-triggered on screen share. It now uses the decoded-to-received frames ratio.
`cpuPerformanceDetector.fpsVolatilityThresholds` was replaced by
`incomingDecodedFramesRatioThresholds` (`{ alertOn: 0.7, alertOff: 0.85, minReceivedFrames: 10 }`).
{{< /details >}}

{{< details "4.3.1" >}}
`dataChannels` added to peer-connection sample serialisation, so data channel stats now reach
`ClientSample.peerConnections[].dataChannels`.
{{< /details >}}

{{< details "4.3.0 — breaking" >}}
- Issue lifecycle rebuilt around `raiseIssue(key, …)` / `resolveIssue(key, …)`;
  `resolveActiveIssues` removed.
- `activeIssues` changed from `Record<string, ClientIssue[]>` to `Map<string, RaisedClientIssue>`.
- `createIssue` and `disabled` removed from detector config blocks; use `null` config or the
  runtime `detector.disabled` flag.
- `'resolved-issue'` renamed to `'issue-resolved'`.
- Global `setLogger` removed in favour of `new ClientMonitor({ logger })`.
- `ClientMonitorIssue` / `ClientMonitorResolvedIssue` unions and type guards added.
- `Detectors` registry gained `has`, `getByName`, `find`, `filter`, iteration and
  `disable` / `enable` / `disableAll` / `enableAll` / `isEnabled`.
{{< /details >}}

Full history: [CHANGELOG on GitHub](https://github.com/ObserveRTC/client-monitor-js/blob/master/CHANGELOG.md).
