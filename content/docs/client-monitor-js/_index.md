---
title: "Client Monitor"
linkTitle: "Client Monitor"
description: "client-monitor-js — client-side WebRTC monitoring for browsers"
lead: "Drop it next to your RTCPeerConnection and get derived metrics, quality scores and confirmed issue verdicts — in the browser, in real time"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 200
toc: true
---

`@observertc/client-monitor-js` turns the raw, awkward output of `RTCPeerConnection.getStats()`
into something you can act on: a navigable object model, per-interval derived metrics, 0–5 quality
scores with reasons, and **46 detectors** that raise and resolve **37 issue types** with proper
hysteresis instead of flapping on every tick.

It runs entirely in the browser, has two runtime dependencies, and needs no ObserveRTC server
component — use it purely for local UI, or ship its `ClientSample` output to
[`observer-js`](/docs/observer-js/) for cross-participant analysis.

{{< callout context="note" title="Current version — 4.9.0" icon="info-circle" >}}
This documentation tracks **`4.9.0`**. It is a large release: the detector layer was rebuilt
around one rule — **one detector class raises one issue type** — which turned 27 classes into 46
and 27 issue types into 37, retired every group config key, and made the default score calculator
a reading of the open issues rather than a second opinion formed from raw stats.

`collectingPeriodInMs` and `samplingPeriodInMs` both default to **5000** now (they were 2000 and
8000). See [What changed in 4.9](./migration-4-9/) before upgrading from 4.8 or earlier.
{{< /callout >}}

## Install

```bash
npm install @observertc/client-monitor-js
```

```bash
yarn add @observertc/client-monitor-js
```

Runtime dependencies: `eventemitter3` and `ua-parser-js`. Ships ESM with TypeScript declarations,
tree-shakeable (`sideEffects: false`), targeting evergreen browsers. This release ships
`ClientSample` schema **3.7.0**.

## Sixty-second start

```javascript
import { ClientMonitor } from "@observertc/client-monitor-js";

const monitor = new ClientMonitor({
    clientId: "user-42",
    callId: "room-abc",
    collectingPeriodInMs: 5000,   // how often getStats() is polled  (default 5000)
    samplingPeriodInMs: 5000,     // how often a ClientSample is emitted (default 5000)
});

// Anything that produces WebRTC stats can be a source.
monitor.addSource(peerConnection);

// 1. Live metrics for your own UI.
monitor.on("stats-collected", () => {
    ui.render({
        sendingVideo: monitor.sendingVideoBitrate,
        receivingVideo: monitor.receivingVideoBitrate,
        rttMs: (monitor.avgRttInSec ?? 0) * 1000,
        score: monitor.score,
    });
});

// 2. Confirmed problems, with a start and an end.
monitor.on("issue", (issue) => log.warn(issue.type, issue.payload));
monitor.on("issue-resolved", (issue) => log.info(issue.type, "lasted", issue.payload?.durationInMs));

// 3. Telemetry for the backend.
monitor.on("sample-created", ({ sample }) => transport.send(sample));

// 4. Clean shutdown — still-open issues auto-resolve.
monitor.close();
```

That is the whole integration. Everything below is what you get for free, and how to bend it to
your application.

## What the library actually does for you

{{< callout context="tip" title="The short version" icon="rocket" >}}
Raw `getStats()` gives you monotonically increasing counters. Almost every question you want to
ask — *"what is the bitrate?"*, *"is video frozen?"*, *"is the CPU the bottleneck?"* — requires
differencing those counters across ticks, normalising browser differences, and applying hysteresis
so you do not alert on a single bad sample. That is the work this library does.
{{< /callout >}}

### 1. Counters become metrics

`getStats()` reports `bytesReceived: 918273645`. What you want is *bits per second over the last
interval*. The library computes per-interval deltas and rates for every stat type and exposes them
as plain properties:

```javascript
monitor.sendingVideoBitrate;              // bps, aggregated across all peer connections
pcMonitor.deltaInboundPacketsLost;        // packets lost in this interval only
inboundRtp.ewmaFps;                       // smoothed frame rate
inboundRtp.fpsVolatility;                 // how unstable that frame rate is
inboundRtp.inventedSpeechRatio;           // share of audio NetEQ had to invent
outboundRtp.payloadBitrate;               // excludes headers and retransmissions
pcMonitor.statsClockTime;                 // the stats-time clock every window is aged on
```

See [Derived metrics](./metrics/) for the full catalogue.

### 2. Raw stats become a navigable object graph

Browser stats are a flat map of records joined by string ids. The library resolves those joins once
and hands you objects that know their neighbours:

```javascript
const track = monitor.tracks.find((t) => t.kind === "video" && t.direction === "outbound");
const rtp = track.highestLayer;               // the top simulcast layer (was getHighestLayer())
const remote = rtp.getRemoteInboundRtp();     // what the far end reports about it
const source = rtp.getMediaSource();          // the local camera feeding it
```

### 3. Symptoms become verdicts

46 detector classes watch the conditions that actually degrade calls, each with its own on/off
thresholds so a single noisy tick cannot raise an alert. They are grouped into five categories by
**what the detection looks for**:

| Category | Question it answers | Classes |
|---|---|---|
| [Connectivity](./detectors-connectivity/) | Can this endpoint establish and keep the path? | 9 |
| [Transport quality](./detectors-transport-quality/) | The path exists — is it carrying traffic well enough? | 8 |
| [Pipeline disruption](./detectors-pipeline/) | Did the media chain stop, or do two components disagree? | 15 |
| [Perceived quality](./detectors-perceived-quality/) | Is what the user sees and hears degraded? | 6 |
| [Telemetry](./detectors-telemetry/) | What is this session's shape, and what changed? | 8 |

Every issue-raising detector **raises** an issue when the condition starts and **resolves** it when
the condition clears, enriching the resolution with `durationInMs`. That is the difference between
"we saw congestion" and "congestion lasted 14 seconds on this peer connection".

[All detectors →](./detectors/) &nbsp;·&nbsp; [Events & issues →](./events-and-issues/)

### 4. Quality becomes a number you can chart

`DefaultScoreCalculator` produces 0.0–5.0 scores for each track, each peer connection and the
client as a whole, together with a breakdown of *why*:

```javascript
monitor.on("score", ({ clientScore, currentReasons }) => {
    // clientScore: 3.2
    // currentReasons: { "decoder-bottleneck": 1.0, "transport-loss-sustained": 2.5 }
});
```

As of 4.9 the client score is **`5 − RMSE`** across five dimensions — the transport, and inbound
and outbound audio and video — and every charge is either an open issue or a named continuous
reading. The whole calculator is replaceable; see [Scoring](./scoring/).

### 5. Everything becomes a `ClientSample`

On the sampling period the monitor snapshots its entire state into a
[`ClientSample`](/docs/schema/clientsample/): every peer connection, every stats record, the events
and issues since the last sample, your metadata and your extension stats. That object is the input
to [`observer-js`](/docs/observer-js/) and to your own storage.

## Where it pays off

{{< card-grid >}}
{{< link-card
  title="Support triage"
  description="A user says 'the call was bad at 3pm'. Issues carry start, end and duration, so you can answer what was wrong instead of guessing from averages."
  href="./recipes/" >}}
{{< link-card
  title="In-call UX"
  description="Show a real network warning at the moment congestion is detected, and take it down when it resolves — not a spinner that never goes away."
  href="./recipes/" >}}
{{< link-card
  title="Release regression"
  description="Score and issue rates per client build. Tag samples with your app version via attachments and compare releases directly."
  href="./sampling/" >}}
{{< link-card
  title="Adaptive behaviour"
  description="React in the client: drop to audio-only on sustained uplink congestion, lower the encoding on cpulimitation, prompt a device change on a lost capture source."
  href="./detectors/" >}}
{{< /card-grid >}}

## Integration surface

| Extension point | What you can do |
|---|---|
| **Sources** | `RTCPeerConnection`, a mediasoup `Device` (new transports hooked automatically) or a single mediasoup transport |
| **Detectors** | Add your own, never construct a built-in (`null` on its key), or toggle any of them at runtime |
| **Score calculator** | Replace the scoring model wholesale while keeping the metric plumbing |
| **Stats adapters** | Pre- and post-process the raw stats array — normalise, filter, or synthesize records |
| **Extension stats providers** | Inject application metrics (sync or async) into every sample |
| **Declared track context** | Tell the library what the stats cannot: screen share, presented size, the paired video track |
| **`attachments` / `appData`** | Per-entity data that either ships with samples or stays local |
| **Logger** | Route the library's logs into your own logger, or silence it entirely |

## Documentation map

{{< card-grid >}}
{{< link-card title="What changed in 4.9" description="Every break, every retired key, and the migration for each one." href="./migration-4-9/" >}}
{{< link-card title="Integrations" description="RTCPeerConnection, mediasoup, and logging setup." href="./integrations/" >}}
{{< link-card title="Configuration" description="Every option and every detector block, with defaults." href="./configuration/" >}}
{{< link-card title="Detectors" description="The taxonomy, the five design rules, and the index of all 46 classes." href="./detectors/" >}}
{{< link-card title="Events & issues" description="The raise / update / resolve lifecycle, every issue type, and type-safe handling." href="./events-and-issues/" >}}
{{< link-card title="Scoring" description="How the default 0–5 score is computed, what it charges, and how to replace it." href="./scoring/" >}}
{{< link-card title="Monitors & derived metrics" description="The object graph and every computed field on it." href="./metrics/" >}}
{{< link-card title="Sampling & transport" description="Samples, stats adapters, extension stats, and delta codecs." href="./sampling/" >}}
{{< link-card title="Recipes" description="Worked patterns: dashboards, adaptive UX, production tuning, frameworks." href="./recipes/" >}}
{{< link-card title="API reference" description="Constructor, methods, properties and the full event table." href="./api-reference/" >}}
{{< /card-grid >}}

## Resources

- [npm package](https://www.npmjs.com/package/@observertc/client-monitor-js)
- [GitHub repository](https://github.com/ObserveRTC/client-monitor-js)
- [Schema definitions](/docs/schema/)
