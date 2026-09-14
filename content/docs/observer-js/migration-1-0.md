---
title: "What changed in 1.0"
description: "Upgrading observer-js from the 0.x / 1.0.0-beta line"
lead: "Detector configuration, the update policy enum and the pluggable Updater are gone — the API is now small enough to be stable"
date: 2026-09-13T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 305
toc: true
---

`1.0.0` is the first stable release: the API described across these pages follows semver from here,
so a breaking change means a 2.0.0. Getting there meant removing several things rather than
deprecating them, because each of them was a mechanism that had earned its way out.

## ⚠️ `ObservedInboundRtp.bitrate` is now bits per second

It was computed as `(deltaBytes * 8) / elapsedMs` — bits per *millisecond*, i.e. **1000× smaller**
than `ObservedOutboundRtp.bitrate` and the client-level bitrates, which were already bps. The same
field name meant two different units depending on direction.

**If you have thresholds or dashboards reading inbound `bitrate`, they need rescaling by 1000.**

## ⚠️ `currentRttInMs` no longer blends two different round trips

It previously took the median of ICE/STUN RTT and RTCP RTT mixed together, so the value moved as
streams came and went for reasons unrelated to the network.

It now **prefers `rtcpRttInMs` and falls back to `iceRttInMs`** — always one kind within a tick,
never an average of both. Both are exposed separately, along with `sfuHopRttInMs` (`rtcp − ice`):

- `iceRttInMs` comes from ICE/STUN consent checks and measures the trip to *whatever terminates
  ICE* — **in an SFU topology that is the SFU**, so it is the client↔SFU leg.
- `rtcpRttInMs` comes from RTCP receiver reports and is an **end-to-end** media-path round trip.
- `sfuHopRttInMs` estimates everything past the SFU, which separates "this client's last mile is
  slow" from "the path beyond the SFU is slow".

## ⚠️ `updatePolicy`, `defaultCallUpdatePolicy` and the `Updater` are gone

The update model is now **structural rather than configurable**:

> A call is updated when any of its clients is updated. The observer is updated when any of its
> calls is updated.

Two booleans, both defaulting to `true`, opt out of a link in that chain:
`ObserverConfig.autoUpdateOnCallUpdate` and `ObservedCallSettings.autoUpdateOnClientUpdate`. Set both
`false` and drive `observer.update()` from your own interval for a fixed cadence.

```typescript
const observer = new Observer({ autoUpdateOnCallUpdate: false });
setInterval(() => observer.update(), 5_000);
```

The old `'update-when-all-…'` policies were **removed rather than renamed**. "When all clients have
updated" sounds appealing and deadlocks on the first client that stops sending — one silent
participant froze the whole call's aggregation until it timed out.

{{< callout context="caution" title="Observer-scoped detectors and validators run nowhere else" icon="alert-triangle" >}}
If the observer never updates, they never run.
{{< /callout >}}

## ⚠️ Detector configuration is gone from `ObserverConfig`

`new Observer()` has **zero detectors and zero validators**. `observerDetectors` / `callDetectors`
no longer exist as config keys; neither do `DetectorSlot` as a config mechanism,
`defaultCallDetectorsConfig`, `defaultObserverDetectorsConfig`, `createCallDetectors`,
`createObserverDetectors` or `detectorSlot`. The per-detector `registry` option is gone too.

```typescript
observer.addObserverDetector('observer-concurrent-issue-detector', {
    issueTypes: ['congestion', 'ice-disconnected'],
    minAffectedCalls: 3,
});

observer.addCallDetector('call-concurrent-issue-detector', { issueTypes: ['congestion'] });
observedCall.addDetector('issue-fan-out-detector', { issueTypes: ['video-flow-disrupted'] });
```

Detectors are named by their kebab-case `static NAME`, and **the name types the config** — an
unknown name, or a key belonging to a different detector, will not compile. Each detector owns its
defaults in its own constructor, beside the doc explaining what the threshold means; there is no
central table to keep in sync.

> **Why the reversal?** Earlier drafts auto-created every detector from a three-state config slot. A
> detector nobody asked for costs time on every tick and raises finding types into a handler that was
> never written to expect them. **Silence you configured is better than findings you didn't.**

## ⚠️ `CallIssue` and `ObserverIssue` are separate types, and the payload is evidence only

| | Raised by | Delivered as | `scope` |
|---|---|---|---|
| `CallIssue` | `observedCall.addIssue(…)` | `call-issue` | `'call'` |
| `ObserverIssue` | `observer.addIssue(…)` | `observer-issue` | `'observer'` |

Both share `IssueBase` — `type`, `timestamp`, `conclusion?`, `payload?` — and `Issue` is the union,
discriminated on `scope`. `scope` is **stamped by `addIssue`**; callers pass `Omit<…, 'scope'>`.

**Payloads were simplified to evidence alone.** They no longer carry `type`, `scope`, or the
`callId` already present on the event, and **`conclusion` was lifted out of the payload to a
first-class field**:

```typescript
observer.on('call-issue', ({ observedCall, issue }) => {
    issue.conclusion?.faultDomain;   // was payload.conclusion.faultDomain
    issue.payload;                   // evidence only — and always an object
});
```

The `string` variant of `payload` and `issuePayloadOf()` are removed. `issuePayloadAsString(issue)`
remains for boundaries that genuinely need text. `ClientIssue` is unchanged — those genuinely are
wire entries.

## ⚠️ Removed and renamed

| Gone | Use instead |
|---|---|
| `IceDisruptionDetector` | `ObserverConcurrentIssueDetector` with the `ice-*` issue types — the server sees less and guesses more than the client does |
| `ConcurrentIssueDetector` | Split into `CallConcurrentIssueDetector` and `ObserverConcurrentIssueDetector` (`lastCohorts` → `lastGroups`) |
| `IssueIndex`, `observedCall.issueIndex`, `observer.issueIndex` | `activeIssuesRegistry` — issues are **pushed** to detectors now, not polled |
| `TrackDistributionAggregator`, `call.trackDistributionAggregator` | Walk the resolver links directly. The statistics helpers it used (`percentile`, `median`, `summarize`, `counterDelta`, `robustZScore`, `SlidingWindow`, `TrendTester`) are all still exported |
| `ObservedCall.updateGeneration` | — |
| `concludeFrom` | `concludeCallIssue()` / `concludeObserverIssue()` |
| `validator-settled` event | `validation-ready` |
| validator name `simulcast-receiver-validator` | `simulcast-receivers` |
| `ResolvedClientIssue` | `ResolvedActiveClientIssue` |
| `isResolutionEntry` | `isClientIssueResolutionEntry` |
| `WorstReceiverContagionDetector` | `SimulcastReceiverValidator` — it still raises `WORST_RECEIVER_CONTAGION`, so alerting is unchanged |

**`TurnServerHealthDetector`'s payload changed.** It was rewritten to the same source-of-truth
principle: it still groups relayed clients by TURN server, but "in trouble" now comes from each
client's own reported issues rather than server-side RTT/loss thresholds. `clients` /
`degradedClients` / `issueTypes` replace the old `peerConnections` / `rttInMs` / `fractionLost`
summaries.

**Mediasoup sample types lost their index signature.** They were `Record<string, unknown> & { … }`,
which allowed arbitrary top-level keys but silently accepted typos on real fields and weakened
autocomplete. Custom data belongs in the typed `attachments` slot present on every entity.

**`mediasoup` is now an optional `peerDependency`** (`>=3.11.0`). It was only in `devDependencies`
while `ObservedMediasoupRouter` exposed `types.Router` in its public signature, so the emitted
declarations referenced a package consumers might not have. Runtime is unaffected — the import is
type-only.

## Issues are pushed, not polled

`ActiveIssuesRegistry` replaces the pull-based `IssueIndex`. A detector implements
`ActiveIssueTracker` and registers for the issue types it consumes; the registry hands them over as
they open and close.

```typescript
observer.activeIssuesRegistry.addIssueTracker('congestion', myDetector);
observer.activeIssuesRegistry.removeIssueTracker(myDetector);
```

A detector's cost is then proportional to the issues it actually receives rather than to the number
of participants: an `update()` that finds nothing was pushed costs one comparison, whatever the
fleet size.

**There is no wildcard subscription.** Every issue-driven detector requires an explicit, non-empty
`issueTypes` (or `publisherIssueTypes` / `receiverIssueTypes`). "Feed me everything and I'll work
out what matters" moves the decision from the application — which knows its client build and its
issue vocabulary — onto a detector that has to guess, and makes the cost of a subscription unbounded
and invisible.

## `client-monitor-js` ≥ 4.6.0 is required, with no fallback

Every issue-driven detector reads the raise + `<type>-resolved` lifecycle. There is no path that
infers these conditions from raw counters for the benefit of older clients: the client decides
better, and maintaining a worse second implementation to be polite is how both end up wrong. Issues
without a `key` have no lifecycle and stay one-shot.

## New in 1.0

- **[Call summaries](../call-summaries/)** — the one record that outlives a call. Configured at
  construction or not at all.
- **[Validators](../validators/)** — one-shot structural checks: `simulcast-receivers`,
  `remote-track-resolver`, `codec-consistency`.
- **`TurnServerOutageDetector`** — covers what the health detector structurally cannot. Degradation
  makes clients unhappy; **an outage makes them disappear**, so it measures a server's population
  against its own recent peak and refuses to blame it without a control group.
- **`ClientPopulationIssueDetector` gained a `location` axis** — grouping by geohash cell, which is
  how network symptoms actually cluster.
- **`appData` factories see the accept context** — an accept middleware can resolve a tenant or a
  trace id once, and the factory bakes it into `appData` at birth.
- **Every config field is documented for IntelliSense** — all fifteen `*Config` types plus
  `ObserverConfig` now state units, defaults, sensible ranges, and what going too far in either
  direction costs.
- **The public type surface is complete.** Eighteen schema types plus `CalculatedScore`,
  `MediaKind`, `MiddlewareProcessor`, `ObservedCallSettings`, `ObservedClientSettings`,
  `ObservedTURN`, `ObservedTurnServer` and `schemaVersion` are exported. They were reachable but not
  nameable.

## Fixed in 1.0

| Fix | What was wrong |
|---|---|
| Remote track resolution was **one-shot** | It linked tracks only on `*-track-added`, which fires once per track — so a strategy that could not produce a publisher id at that instant lost the track for its entire life. Unresolved tracks are now retried on their own `*-track-updated`, and `resolver.pendingTrackCounts` reports what is still waiting |
| `createObservedClient` mutated the settings object it was given | It wrote the resolved `appData` and `closeClientIfIdleForMs` back onto the caller's object, so a settings object reused as a template came back carrying the first client's `appData` |
| `SfuCongestionDetectorConfig` hovered with no documentation at all | It used `//` line comments, which JSDoc tooling ignores entirely |

## Three schema generations still read

The bundled schema types are **3.7.0**, and `accept()` takes all three payload generations on the
same call, because a fleet is never on one client version:

- **pre-3.5.0** — payloads carried as pre-serialised JSON **strings**;
- **3.5.0 / 3.6.0** — payloads became records of primitives, and `scoreReasons` became a
  `Record<string, number>` rather than a `string[]` of labels;
- **3.7.0** — payload values widened to free-form JSON, so a payload may nest objects and arrays.

Every payload read inside the library goes through `parseJsonAs` / `parseJsonObject`, which pass an
object through untouched and parse a string; `normalizeScoreReasons` folds a legacy `string[]` into
the record shape with a magnitude of `0`, which keeps any summing of contributions honest about the
magnitude the old wire never carried.

**What this asks of you:** a payload value is now `unknown`, so narrow before reading it —
`typeof payload.trackId === 'string'` rather than a bare `payload.trackId`. Writers need no change.

## Publishing note

The npm dist-tag is now a property of the **branch**, not of the version string: anything pushed to
`master` publishes as `latest`, whether the version is stable or a prerelease. Previously only a
stable version reached `latest`, which left `npm install @observertc/observer-js` resolving to
whatever was last released as stable rather than to the current release line.
