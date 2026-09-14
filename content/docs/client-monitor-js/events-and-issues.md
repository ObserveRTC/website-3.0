---
title: "Events & issues"
description: "The raise / update / resolve lifecycle, every issue type, and type-safe handling"
lead: "Issues are conditions with a lifetime; events are notifications. Two channels, on purpose"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 240
toc: true
---

`ClientMonitor` emits two categories of notification: **issues**, which describe a problem state,
and **events**, which describe a thing that happened. Picking the right one is the key to keeping
alerting code sane.

| | Issue | Event |
|---|---|---|
| Represents | An ongoing or one-shot condition | A discrete thing that happened |
| Lifecycle | Raised, updated, resolved | Immutable record |
| API | `addIssue` / `raiseIssue` / `resolveIssue` | `addEvent` |
| Sample buffer | `sample.clientIssues[]` | `sample.clientEvents[]` |
| Monitor events | `'issue'`, `'issue-updated'`, `'issue-resolved'` | `'client-event'` |

## Two flavours of issue

| Flavour | Method | Has `key` | Enters `activeIssues` | Can be resolved |
|---|---|---|---|---|
| One-shot | `addIssue({ type, payload?, timestamp? })` | no | no | no |
| Stateful | `raiseIssue(key, { type, payload?, timestamp? })` | **yes (required)** | yes | yes |

Use the one-shot flavour for an incident with no "ended" condition — a `getUserMedia` failure, a
click-to-call timeout. Every built-in detector uses the stateful flavour. The library only insists
that *if* you want to resolve later, you must have raised with a `key`.

```typescript
type ClientIssuePayload = Record<string, unknown> | boolean | string | number;

type AddedClientIssue<T = ClientIssuePayload> = {
    type: string;
    payload?: T;
    timestamp: number;
};

type RaisedClientIssue<T = ClientIssuePayload> = {
    type: string;
    key: string;           // globally unique handle within this monitor
    payload?: T;
    raisedAt: number;
    updatedAt: number;     // bumped on every re-raise of the same key
};

type ResolvedClientIssue<T = ClientIssuePayload> = RaisedClientIssue<T> & {
    resolvedAt: number;
    comment?: string;
};
```

Narrow between the two by checking for `'key' in issue` — that is the discriminant.

## The lifecycle

```typescript
monitor.on('issue',          (issue) => { /* new addIssue or new raiseIssue */ });
monitor.on('issue-updated',  (issue) => { /* re-raise of an existing key */ });
monitor.on('issue-resolved', (resolved) => { /* resolveIssue or close() auto-resolve */ });
```

| Step | What happens | Event |
|---|---|---|
| `raiseIssue('x', …)` for an **unknown** key | Created and stored in `activeIssues` | `'issue'` |
| `raiseIssue('x', …)` for an **active** key | Payload and `updatedAt` refreshed in place; no duplicate | `'issue-updated'` |
| `addIssue({ … })` | Created; **not** added to `activeIssues` | `'issue'` |
| `resolveIssue('x', …)` | Removed from `activeIssues`; an optional `payload` overwrites the stored one | `'issue-resolved'` |
| `monitor.close()` | All still-active issues auto-resolve | `'issue-resolved'` each, with a comment |

```typescript
// Snapshot helpers
monitor.getActiveIssuesByType(type?);   // RaisedClientIssue[]
monitor.isIssueActive(key);             // boolean
monitor.activeIssues;                   // Map<string, RaisedClientIssue>
```

**Issue registries per monitor (new in 4.9).** Every monitor also owns the issues raised against it,
which is what lets a score calculator read one monitor's findings directly instead of reaching into
a client-wide map:

```typescript
pcMonitor.issues.hasType('transport-loss-sustained');
inboundTrackMonitor.issues.getFirstPayloadByType('decoder-bottleneck');
outboundTrackMonitor.issues.size;
```

## Every built-in issue type

**37 types, one per issue-raising detector class.** Nine classes emit events only:
`CodecChangeDetector`, `VideoResolutionChangeDetector`, `SimulcastLayerDetector`,
`CaptureTrackMutedDetector`, `StatsGapDetector`, `IceTraversalDetector`,
`IcePathEstablishmentDetector`, `IceRestartDetector` and `IceRestartRecommendationDetector`.

Every resolved payload is the raise-time payload plus `durationInMs` (and, for some, refreshed
metrics).

### Connectivity

| `type` | Raised when | Resolved when | Payload |
|---|---|---|---|
| `no-available-ice-candidate` | Gathering reported `complete` with zero local candidates on a never-connected PC | A candidate appears, the connection connects, or the PC closes | `NoAvailableIceCandidateIssuePayload` |
| `ice-establishment-failed` | Local candidates existed, the PC never reached `connected`, and no pair was ever nominated, for `thresholdInMs` | The connection establishes after all | `IceEstablishmentFailedIssuePayload` |
| `dtls-handshake-failed` | An ICE transport reached `dtlsState: 'failed'` | A later handshake connects | `DtlsHandshakeFailedIssuePayload` |
| `dtls-handshake-stalled` | ICE proven healthy while DTLS sat in `new`/`connecting` past `stalledThresholdInMs` | The handshake completes | `DtlsHandshakeStalledIssuePayload` |
| `ice-disconnected` | An ICE transport stayed `disconnected` past `disconnectedThresholdInMs` | ICE reconnects, or the transport goes away | `IceDisconnectedIssuePayload` |
| `ice-connection-failed` | An ICE transport reached `failed` | ICE reconnects (typically after a restart) | `IceConnectionFailedIssuePayload` |
| `ice-transport-stalled` | Still sending on a succeeded pair, receiving nothing for `transportStallThresholdInMs` | Inbound traffic resumes | `IceTransportStalledIssuePayload` |
| `unstable-ice-path` | `pathSwitchThreshold` selected-path switches within `pathSwitchWindowInMs` | A whole window passes below the threshold | `UnstableIcePathIssuePayload` |

### Transport quality

| `type` | Raised when | Resolved when | Event | Payload |
|---|---|---|---|---|
| `uplink-congestion` | The browser reports the encoder bandwidth-limited **and** `sqrt(undershoot × pacerBloating)` reaches `minSeverity` | The browser stops reporting a bandwidth limitation | `'uplink-congestion'` | `UplinkCongestionIssuePayload` |
| `downlink-congestion` | `sqrt(undershoot × bufferBloating)` reaches `minSeverity` | That severity falls under half of `minSeverity` | `'downlink-congestion'` | `DownlinkCongestionIssuePayload` |
| `congestion` *(deprecated)* | Per-PC bandwidth limitation + a sensitivity-specific corroborator | Bandwidth limitation clears | `'congestion'` | `CongestionIssuePayload` |
| `transport-delay-degraded` | Mean RTT over the detection window reached `thresholdInMs` | The recovery window also reads below `recoveryThresholdInMs` | `'transport-delay-degraded'` | `TransportDelayIssuePayload` |
| `transport-loss-sustained` | Mean interval loss (worse direction) stayed at or above `threshold` for `durationInMs` | Loss falls below `recoveryThreshold` | `'transport-loss-sustained'` | `TransportLossIssuePayload` |
| `blocked-stun-requests` | A succeeded pair stopped answering STUN while this endpoint kept asking | STUN is answered again | `'blocked-transport'` | `BlockedTransportIssuePayload` |
| `blocked-outbound-media-transport` | Media leaving on a STUN-answered path with no receiver report for `thresholdInMs` | A report arrives | `'blocked-outbound-media-transport'` | `BlockedOutboundMediaIssuePayload` |
| `blocked-inbound-media-transport` | The far end's sender reports advance while our receivers take nothing | Media arrives | `'blocked-inbound-media-transport'` | `BlockedInboundMediaIssuePayload` |

### Pipeline disruption

| `type` | Raised when | Resolved when | Event | Payload |
|---|---|---|---|---|
| `capture-source-lost` | The outbound track's device reached `ended` | — (terminal) | `'capture-source-lost'` | `CaptureSourceLostIssuePayload` |
| `silent-audio-source` | A live, enabled, unmuted microphone produced silence for `silenceThresholdInMs` | Audio appears, or the track stops capturing | `'silent-audio-source'` | `SilentAudioSourceIssuePayload` |
| `video-capture-bottleneck` | The camera fell more than `produceDegradationThreshold` short of the configured frame rate across the detection window | The recovery window comes back under the same threshold | `'video-capture-bottleneck'` | `VideoCaptureBottleneckIssuePayload` |
| `encoder-bottleneck` | A delivering source outran the encoder across the detection window | The encoder keeps up again | `'encoder-bottleneck'` | `EncoderBottleneckIssuePayload` |
| `rtp-sender-stalled` | `deltaFramesEncoded > 0` while `deltaPacketsSent === 0` on one ssrc, for `thresholdInMs` | Packets leave again, or the ssrc goes away | `'rtp-sender-stalled'` | `RtpSenderStalledIssuePayload` |
| `dry-outbound-track` | Outbound bytes stay flat across **every active layer** for `thresholdInMs`, with no `bandwidth`/`cpu` limitation to explain it | Any layer sends bytes again | `'dry-outbound-track'` | `DryOutboundTrackIssuePayload` |
| `transport-demux-stalled` | Transport receiving above `minTransportReceiveBitrateBps` while every inbound RTP on it stays flat | Inbound RTP receives again | `'transport-demux-stalled'` | `TransportDemuxStalledIssuePayload` |
| `dry-inbound-track` | Inbound bytes stay flat for `thresholdInMs` | Bytes start flowing again | `'dry-inbound-track'` | `DryInboundTrackIssuePayload` |
| `frame-assembly-stalled` | Packets kept arriving with `framesReceived` flat for `thresholdInMs`, past `minPacketsReceived` | A frame is assembled, or packets stop arriving | `'frame-assembly-stalled'` | `FrameAssemblyStalledIssuePayload` |
| `decoder-bottleneck` | The decoder left more than `decodeDegradationThreshold` of arriving frames undecoded over the window | The next average comes back under it | `'decoder-bottleneck'` | `DecoderBottleneckIssuePayload` |
| `video-decoder-overloaded` | Frames arrived and loss was quiet, but decode time overran the frame budget | The decoder keeps up again | `'video-decoder-overloaded'` | `DecoderPerformanceIssuePayload` |
| `stuck-decoder` | RTP bytes flowing, nothing decoding, PLIs firing, for `max(thresholdInMs, rttMultiplier × RTT)` | Frames decode again | `'stuck-decoder'` | `StuckDecoderIssuePayload` |
| `inbound-video-playout-discrepancy` | `(framesReceived − framesRendered) / framesReceived > highSkewRatio` | The ratio drops below `lowSkewRatio` | `'inbound-video-playout-discrepancy'` | `PlayoutDiscrepancyIssuePayload` |
| `video-recovery-failed` | PLIs sent, picture stalled, `keyFramesDecoded` not advancing for `recoveryFailedThresholdInMs` | A keyframe arrives or the stall ends | `'video-recovery-failed'` | `VideoRecoveryFailedIssuePayload` |
| `cpulimitation` | Codec utilization reached `utilizationThreshold` across the detection slice | The recovery slice also reads below the recovery threshold | `'cpulimitation'` | `CpuPerformanceIssuePayload` |

### Perceived quality

| `type` | Raised when | Resolved when | Event | Payload |
|---|---|---|---|---|
| `pixelated-video` | `bitPerPixel` stayed at or below `threshold` for `durationInMs` of stats time | It rises above `recoveryThreshold`, or the track pauses | `'pixelated-video'` | `PixelatedVideoIssuePayload` |
| `video-flow-disrupted` | Freezes counted across the track's detection window reach the `frozen` or `choppy` verdict | Frames render again (`frozen`), or both halves of the window read freeze-free (`choppy`) | `'video-flow-disrupted'` | `VideoFlowIssuePayload` |
| `invented-speech` | Invented audio (silence excluded) accumulates `raiseAfterInventedMs` beyond `allowedInventedRatio` | The accumulator drains back to zero | `'invented-speech'` | `InventedSpeechIssuePayload` |
| `synthesized-audio` | The share of played audio that was invented exceeds `synthesizedRatioThreshold` | The share falls back under it | `'synthesized-audio'` | `AudioPlayoutSynthesisIssuePayload` |
| `av-desync` | The audio track's playout ran ahead of its linked video track's by `audioAheadRaiseInMs`, or behind by `audioBehindRaiseInMs`, for `sustainForInMs` | The skew falls inside the matching resolve threshold | `'av-desync'` | `AVDesyncPlayoutIssuePayload` |
| `audio-jitter-buffer-stress` | Target delay grown **and** NetEQ time-stretching, for `minConsecutiveTicks` | Either condition clears | `'audio-jitter-buffer-stress'` | `JitterBufferStressIssuePayload` |

{{< callout context="caution" title="Types retired in 4.9" icon="alert-triangle" >}}
`audio-concealment` → `invented-speech`; `audio-desync` → `av-desync`; `capture-track-ended` →
`capture-source-lost`; `freezed-video-track` → `video-flow-disrupted`; `capture-bottleneck` →
`video-capture-bottleneck`; `blocked-transport` → three `blocked-*` types (the **event** of that
name survives); `media-pipeline-stalled` → `rtp-sender-stalled` + `transport-demux-stalled`.
**`keyframe-storm` is removed outright**, with no replacement. Update any server-side allow-list —
see [What changed in 4.9](../migration-4-9/).
{{< /callout >}}

## Type-safe handling

Listeners receive the generic `ClientIssue` / `RaisedClientIssue` / `ResolvedClientIssue`. To get
full payload typing for the built-ins, narrow with the exported guards:

```typescript
import {
    ClientMonitor,
    ClientMonitorIssue,
    ClientMonitorResolvedIssue,
    isClientMonitorIssue,
} from '@observertc/client-monitor-js';

monitor.on('issue', (issue) => {
    if (!isClientMonitorIssue(issue)) return;   // custom or app-raised

    switch (issue.type) {
        case 'uplink-congestion':
            // issue.payload is UplinkCongestionIssuePayload
            sender.capBitrate(issue.payload.availableOutgoingBitrate * 0.8);
            break;

        case 'av-desync':
            console.log('lip sync off by', issue.payload.playoutDiffInMs, 'ms',
                '(', issue.payload.direction, ')',
                'on', issue.payload.trackId, 'vs', issue.payload.linkedVideoTrackId);
            break;

        case 'video-flow-disrupted':
            // payload.state is 'frozen' | 'choppy'
            ui.showFreeze(issue.payload.trackId, issue.payload.state);
            break;

        case 'stuck-decoder':
            if (issue.payload.variant === 'decode') recreateConsumer(issue.payload.trackId);
            break;
    }
});

monitor.on('issue-resolved', (resolved) => {
    const own = resolved as ClientMonitorResolvedIssue;
    console.log(own.type, 'lasted', own.payload.durationInMs, 'ms');
});
```

- `ClientMonitorIssue` / `ClientMonitorResolvedIssue` — discriminated unions over every built-in.
- `isClientMonitorIssue()` / `isClientMonitorResolvedIssue()` — guards returning `true` only for
  built-in types.
- `ClientMonitorIssueType` — the literal union of those strings, useful for exhaustive switches and
  for typing a server-side allow-list.

## Raising your own

Pick a `key` unique per logical incident; the detector convention is `${type}-${scope}`.

```typescript
monitor.raiseIssue(`unexpected-mute-${participantId}`, {
    type: 'unexpected-mute',
    payload: { participantId, sinceUtc: new Date().toISOString() },
});

// Re-raise updates in place → emits 'issue-updated', not 'issue'
monitor.raiseIssue(`unexpected-mute-${participantId}`, {
    type: 'unexpected-mute',
    payload: { participantId, framesSpoken: 0 },
});

monitor.resolveIssue(`unexpected-mute-${participantId}`, {
    comment: 'participant unmuted',
    payload: { participantId, durationInMs: Date.now() - mutedAtMs },
});

// A moment rather than a condition — no key, nothing to resolve.
monitor.addIssue({ type: 'USER_MEDIA_ERROR', payload: { error: `${err}` } });
```

Custom issues ride the same events and reach the sample the same way. They do **not** affect any
score: the shipped calculator prices only the types it knows about, and there is no table to
register a new one in. A custom issue that should cost score belongs to a custom `ScoreCalculator`
— see [Scoring](../scoring/).

## What reaches the sample

Every `addIssue` and every `raiseIssue` adds an entry to the next `ClientSample.clientIssues[]`,
unless the detector's `includeIssueInSample` is `false`. **Re-raises do not add a new entry** — they
emit `'issue-updated'` to live listeners and leave the buffer unchanged.

**The whole lifecycle reaches the sample** (`sendResolvedIssuesToServer`, default `true`), so a
server can keep an on-the-fly mirror of each client's *currently active* issues rather than only
learning that issues started:

```text
raise:      { type: 'stuck-decoder',          key, payload,                          timestamp: raisedAt }
resolution: { type: 'stuck-decoder-resolved', key, payload: { raisedAt, comment, … }, timestamp: resolvedAt }
```

The resolution's payload carries only what was **explicitly passed** to `resolveIssue`, flattened —
the built-in detectors pass their final payload, so `durationInMs` appears here. `raisedAt` equals
the raise entry's `timestamp`, a secondary join for consumers that do not store keys. Issues still
active at `close()` are auto-resolved and reach the final sample.

Servers switching on issue `type` should handle or ignore the `-resolved` suffix;
[`observer-js`](/docs/observer-js/) pairs them for you and emits `client-issue-resolved` with
`durationInMs` and `resolvedBy`. Pass `sendResolvedIssuesToServer: false` to restore the older wire
format exactly (raise entries only, no `key`); the realtime `'issue-resolved'` event fires either
way.

## Event listeners cheat-sheet

```typescript
// Lifecycle
monitor.on('sample-created', ({ sample }) => transport.send(sample));
monitor.on('stats-collected', ({ durationOfCollectingStatsInMs, collectedStats }) => { /* … */ });
monitor.on('score', ({ clientScore, currentReasons }) => { /* … */ });
monitor.on('close', () => { /* … */ });

// Issues
monitor.on('issue',          (issue) => { /* … */ });
monitor.on('issue-updated',  (issue) => { /* … */ });
monitor.on('issue-resolved', (resolved) => { /* … */ });

// Transport quality — properties of a path that is up and holding
monitor.on('uplink-congestion',                (e) => { /* sending path out of room — graded severity */ });
monitor.on('downlink-congestion',              (e) => { /* receiving path — same shape, own evidence */ });
monitor.on('transport-delay-degraded',         (e) => { /* round trip long enough to break turn-taking */ });
monitor.on('transport-loss-sustained',         (e) => { /* `direction` says which way */ });
monitor.on('blocked-inbound-media-transport',  (e) => { /* the far end sent; nothing arrived */ });
monitor.on('blocked-outbound-media-transport', (e) => { /* we sent; nothing got through */ });
monitor.on('blocked-transport',                (e) => { /* STUN unanswered — the firewall signature */ });
monitor.on('congestion',                       (e) => { /* the deprecated one-verdict detector */ });

// Pipeline
monitor.on('capture-source-lost',      (e) => { /* the device is gone */ });
monitor.on('silent-audio-source',      (e) => { /* live mic producing digital silence */ });
monitor.on('video-capture-bottleneck', (e) => { /* the camera never produced the frames */ });
monitor.on('encoder-bottleneck',       (e) => { /* the source did; the encoder could not keep up */ });
monitor.on('rtp-sender-stalled',       (e) => { /* frames encode, no packet leaves */ });
monitor.on('dry-outbound-track',       (e) => { /* nothing going on the wire for this track */ });
monitor.on('transport-demux-stalled',  (e) => { /* traffic arrives, no inbound RTP accounts for it */ });
monitor.on('dry-inbound-track',        (e) => { /* nothing arriving */ });
monitor.on('frame-assembly-stalled',   (e) => { /* packets arriving, no frame ever assembled */ });
monitor.on('decoder-bottleneck',       (e) => { /* frames arrived; the decoder could not decode them */ });
monitor.on('video-decoder-overloaded', (e) => { /* decoding overran its budget */ });
monitor.on('stuck-decoder',            (e) => { /* RTP flowing, nothing decodes — recreate the consumer */ });
monitor.on('inbound-video-playout-discrepancy', (e) => { /* frames decoded, not painted */ });
monitor.on('video-recovery-failed',    (e) => { /* we asked for a keyframe; nothing came back */ });
monitor.on('cpulimitation',            (e) => { /* the machine is the bottleneck */ });

// Perceived quality
monitor.on('pixelated-video',           (e) => { /* too few bits per pixel, sustained */ });
monitor.on('video-flow-disrupted',      (e) => { /* `state` is 'frozen' or 'choppy' */ });
monitor.on('invented-speech',           (e) => { /* NetEQ invented audio, not raw loss */ });
monitor.on('synthesized-audio',         (e) => { /* the playout device invented samples */ });
monitor.on('av-desync',                 (e) => { /* lip sync, in ms of skew */ });
monitor.on('audio-jitter-buffer-stress',(e) => { /* buffer grown AND stretching */ });

// Telemetry — these never raise an issue
monitor.on('codec-changed',            (e) => { /* mime type or profile switched */ });
monitor.on('video-resolution-changed', (e) => { /* the adaptation ladder moved */ });
monitor.on('simulcast-layer-changed',  (e) => { /* which layers are actually being sent */ });
monitor.on('capture-track-muted',      (e) => { /* the OS or another app took it */ });
monitor.on('stats-collection-gap',     (e) => { /* discount this interval's rates */ });
monitor.on('ice-path-changed',         (e) => { /* direct <-> TURN, protocol, server */ });
monitor.on('ice-tuple-changed',        (e) => { /* low-level: the selected tuple set changed */ });
monitor.on('ice-restart',              (e) => { /* detected / recovered / failed */ });
monitor.on('ice-restart-recommended',  (e) => { /* YOUR app decides whether to restartIce() */ });
monitor.on('ice-path-establishment-slow', ({ stalledStage }) => { /* and which stage it is stuck in */ });
```
