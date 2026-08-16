---
title: "Events & issues"
slug: "events-and-issues"
description: "The issue lifecycle, events, and type-safe handling"
lead: "Issues describe a problem state with a start and an end; events describe something that happened. Getting the distinction right keeps your alerting sane."
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 314
toc: true
---

`ClientMonitor` emits two categories of notification, and they have deliberately different
lifecycles.

| | **Issue** | **Event** |
|---|---|---|
| Represents | An ongoing or one-shot condition (congestion, dry track, …) | A discrete thing that happened (client joined, ICE candidate found, …) |
| Lifecycle | Raised → updated → resolved | Immutable record |
| Resolution | Yes, for the stateful flavour | No |
| API | `addIssue` / `raiseIssue` / `resolveIssue` | `addEvent` |
| Sample field | `sample.clientIssues[]` | `sample.clientEvents[]` |
| Monitor events | `'issue'`, `'issue-updated'`, `'issue-resolved'` | `'client-event'` |

Events need no further explanation — `monitor.addEvent({ type, payload, timestamp })` records one
and it ships in the next sample. The rest of this page is about issues.

## Two flavours of issue

| Flavour | Method | Has `key` | Enters `activeIssues` | Resolvable | Use for |
|---|---|---|---|---|---|
| One-shot | `addIssue({ type, payload?, timestamp? })` | no | no | no | Incidents with no "ended" condition — `USER_MEDIA_ERROR`, a one-off SDK warning |
| Stateful | `raiseIssue(key, { type, payload?, timestamp? })` | **required** | yes | yes | Anything with a start and an end — congestion, CPU pressure, freeze, dry track |

Every built-in detector uses the stateful flavour. The library only insists on one thing: if you
want to resolve an issue later, you must have raised it with a `key`.

## The lifecycle

{{< steps >}}
{{< step >}}
**Raise.** `raiseIssue('congestion-pc-7', { type: 'congestion', payload })` creates the issue,
stores it in `activeIssues` under that key, emits `'issue'`, and adds one entry to the next
sample's `clientIssues[]`.
{{< /step >}}
{{< step >}}
**Update.** Re-raising the same key while it is active refreshes the payload and `updatedAt` in
place and emits `'issue-updated'`. **No duplicate is added to the sample buffer** — one entry per
episode.
{{< /step >}}
{{< step >}}
**Resolve.** `resolveIssue('congestion-pc-7', { comment, payload })` removes it from
`activeIssues` and emits `'issue-resolved'`. A supplied `payload` **overwrites** the stored one —
that is how detectors enrich the resolution with `durationInMs`.
{{< /step >}}
{{< step >}}
**Auto-resolve on close.** `monitor.close()` resolves every still-active issue with
`comment: 'monitor closed before issue could be resolved'`, so a call that drops mid-incident
still produces a clean lifecycle.
{{< /step >}}
{{< /steps >}}

## In-memory types

```typescript
type ClientIssuePayload = Record<string, unknown> | boolean | string | number;

// Produced by addIssue.
type AddedClientIssue<T = ClientIssuePayload> = {
    type: string;
    payload?: T;
    timestamp: number;
};

// Produced by raiseIssue.
type RaisedClientIssue<T = ClientIssuePayload> = {
    type: string;
    key: string;          // unique handle within this monitor
    payload?: T;
    raisedAt: number;
    updatedAt: number;    // bumped on every re-raise
};

type ClientIssue<T = ClientIssuePayload> = AddedClientIssue<T> | RaisedClientIssue<T>;

// Delivered by 'issue-resolved'.
type ResolvedClientIssue<T = ClientIssuePayload> = RaisedClientIssue<T> & {
    resolvedAt: number;
    comment?: string;
};
```

Narrow between the two flavours with `'key' in issue` — that is the discriminant.

{{< callout context="note" title="Wire format" icon="info-circle" >}}
`ClientSample.clientIssues[]` carries a stripped shape: `{ type, key?, payload?: string, timestamp }`,
with the payload JSON-stringified. The richer in-memory objects are a runtime concern. The `key`
field was added to the schema in [3.3.0](/docs/schema/versions/v3-3-0/) — it is what lets
`observer-js` pair a raise with its resolution.
{{< /callout >}}

## Public API

```typescript
// One-shot: never enters activeIssues, cannot be resolved.
addIssue<T>(input: { type: string; payload?: T; timestamp?: number }): AddedClientIssue<T> | undefined;

// Stateful: enters activeIssues under `key`; re-raising updates in place.
raiseIssue<T>(key: string, input: { type: string; payload?: T; timestamp?: number }): RaisedClientIssue<T> | undefined;

// Resolves by key. `payload`, when provided, overwrites the stored payload.
resolveIssue<T>(key: string, input: { comment?: string; payload?: T; resolvedAt?: number }): ResolvedClientIssue | undefined;

// Snapshot helpers.
getActiveIssuesByType(type?: string): RaisedClientIssue[];
isIssueActive(key: string): boolean;

// The live store — readable, but prefer the helpers above.
readonly activeIssues: Map<string, RaisedClientIssue>;
```

## The built-in issue types

Seven detectors ship, each raising its own type with a typed payload, emitting a
detector-specific event on entry, and resolving with `durationInMs` merged into the payload.

| `type` | Raised when | Resolved when | Named event | Payload type |
|---|---|---|---|---|
| `congestion` | Per-PC bandwidth limitation plus a sensitivity-specific corroborator | Limitation clears | `'congestion'` | `CongestionIssuePayload` |
| `cpulimitation` | CPU-tagged outbound RTP, slow stats collection, or low decoded/received frame ratio | Indicators normalise | `'cpulimitation'` | `CpuPerformanceIssuePayload` |
| `audio-desync` | Sample-correction fraction crosses the on-threshold | Falls below the off-threshold | `'audio-desync-track'` | `AudioDesyncIssuePayload` |
| `freezed-video-track` | `freezeCount` increases | No new freezes for one tick | `'freezed-video-track'` | `FreezedVideoTrackIssuePayload` |
| `dry-inbound-track` | Inbound bytes flat for `thresholdInMs` | Bytes flow again | `'dry-inbound-track'` | `DryInboundTrackIssuePayload` |
| `dry-outbound-track` | Outbound bytes flat for `thresholdInMs` | Bytes flow again | `'dry-outbound-track'` | `DryOutboundTrackIssuePayload` |
| `inbound-video-playout-discrepancy` | `framesReceived − framesRendered > highSkewThreshold` | Skew below `lowSkewThreshold` | `'inbound-video-playout-discrepancy'` | `PlayoutDiscrepancyIssuePayload` |

Every payload type is exported from the package root.

## Type-safe handling

Listeners receive the generic `ClientIssue` types. To get full payload typing for the built-ins,
use the exported discriminated unions and type guards:

```typescript
import {
    ClientMonitor,
    ClientMonitorIssue,
    ClientMonitorResolvedIssue,
    isClientMonitorIssue,
} from "@observertc/client-monitor-js";

monitor.on("issue", (issue) => {
    if (!isClientMonitorIssue(issue)) {
        // Your own / app-raised issue — handle generically.
        return;
    }

    switch (issue.type) {
        case "congestion":
            // issue.payload is CongestionIssuePayload
            ui.showBandwidthWarning(issue.payload.availableIncomingBitrate);
            break;

        case "cpulimitation":
            // issue.payload is CpuPerformanceIssuePayload
            video.lowerEncodingQuality();
            break;

        case "audio-desync":
            log.warn("audio desync on track", issue.payload.trackId);
            break;

        case "freezed-video-track":
            ui.markTileFrozen(issue.payload.trackId);
            break;

        case "dry-inbound-track":
        case "dry-outbound-track":
            log.warn("dry track", issue.payload.trackId);
            break;

        case "inbound-video-playout-discrepancy":
            log.warn("playout skew", issue.payload.frameSkew);
            break;
    }
});

monitor.on("issue-resolved", (resolved) => {
    const own = resolved as ClientMonitorResolvedIssue;
    if (own.type === "congestion") {
        analytics.track("congestion_episode", {
            pc: own.payload.peerConnectionId,
            durationInMs: own.payload.durationInMs,
        });
    }
});
```

Three helpers are exported:

- `ClientMonitorIssue` — union of every raised issue produced by the bundled detectors
- `ClientMonitorResolvedIssue` — the same, for `'issue-resolved'`
- `isClientMonitorIssue(issue)` / `isClientMonitorResolvedIssue(issue)` — runtime type guards

## Managing active issues

```typescript
// Everything currently active.
const all = monitor.getActiveIssuesByType();

// One type only.
for (const issue of monitor.getActiveIssuesByType("congestion")) {
    if (issue.payload?.availableIncomingBitrate < 200_000) {
        ui.showLowBandwidthWarning(issue.key);
    }
}

// Is a specific incident open?
if (monitor.isIssueActive("congestion-pc-123")) { /* … */ }

// Raw iteration (advanced).
for (const [key, issue] of monitor.activeIssues) {
    console.log(key, issue.type, issue.payload);
}
```

This is the cleanest way to drive an in-call status indicator: render from `activeIssues` on every
`stats-collected` tick and the indicator is correct by construction — it disappears when the
condition ends, because the detector resolved the issue.

## Raising your own issues

Pick a key that is unique per logical incident. The detector convention is `${type}-${scope}`.

```typescript
// Start.
monitor.raiseIssue(`unexpected-mute-${participantId}`, {
    type: "unexpected-mute",
    payload: { participantId, detectedAt: Date.now() },
});

// Refresh while it persists (emits 'issue-updated', no duplicate sample entry).
monitor.raiseIssue(`unexpected-mute-${participantId}`, {
    type: "unexpected-mute",
    payload: { participantId, stillMutedForMs: elapsed },
});

// End.
monitor.resolveIssue(`unexpected-mute-${participantId}`, {
    comment: "participant unmuted",
    payload: { participantId, durationInMs: elapsed },
});

// Or, for something with no end state:
monitor.addIssue({ type: "USER_MEDIA_ERROR", payload: { name: err.name } });
```

## Sample-channel behaviour

{{< callout context="caution" title="What reaches the server" icon="alert-triangle" >}}
- Every `addIssue` and every **first** `raiseIssue` adds one entry to the next
  `ClientSample.clientIssues[]`.
- **Re-raises do not add a new entry** — they only emit `'issue-updated'` to live listeners.
- Resolutions reach the server as a companion `<type>-resolved` entry sharing the same `key`.
  `observer-js` strips the suffix and pairs the two into one interval.

If you reconstruct state server-side from stored samples yourself, treat each `clientIssues` entry
as "the issue started here" and use the `key` to pair it with its resolution.
{{< /callout >}}

## Event listener cheat-sheet

```typescript
// Samples.
monitor.on("sample-created", ({ sample }) => { /* … */ });

// Stats lifecycle.
monitor.on("stats-collected", ({ durationOfCollectingStatsInMs, collectedStats }) => { /* … */ });

// Scores.
monitor.on("score", ({ clientScore, scoreReasons }) => { /* … */ });

// Issue lifecycle.
monitor.on("issue",          (issue)    => { /* new addIssue or new raiseIssue */ });
monitor.on("issue-updated",  (issue)    => { /* re-raise of an existing key */ });
monitor.on("issue-resolved", (resolved) => { /* resolveIssue or close() auto-resolve */ });

// Detector-specific (fire alongside 'issue', once per episode).
monitor.on("congestion",                        (e) => { /* … */ });
monitor.on("cpulimitation",                     (e) => { /* … */ });
monitor.on("audio-desync-track",                (e) => { /* … */ });
monitor.on("freezed-video-track",               (e) => { /* … */ });
monitor.on("dry-inbound-track",                 (e) => { /* … */ });
monitor.on("dry-outbound-track",                (e) => { /* … */ });
monitor.on("inbound-video-playout-discrepancy", (e) => { /* … */ });

// Shutdown.
monitor.on("close", () => { /* … */ });
```
