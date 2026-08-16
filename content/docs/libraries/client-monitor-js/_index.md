---
title: "client-monitor-js"
description: "Client-side WebRTC monitoring library for browsers"
lead: "Drop it next to your RTCPeerConnection and get derived metrics, quality scores and confirmed issue verdicts — in the browser, in real time"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 310
toc: true
---

`@observertc/client-monitor-js` turns the raw, awkward output of `RTCPeerConnection.getStats()`
into something you can actually act on: a navigable object model, per-interval derived metrics,
0–5 quality scores with reasons, and a set of detectors that raise and resolve **issues** with
proper hysteresis instead of flapping on every tick.

It runs entirely in the browser, has two runtime dependencies, and does not require any
ObserveRTC server component — you can use it purely for local UI, or ship its `ClientSample`
output to [`observer-js`](/docs/libraries/observer-js/) for cross-participant analysis.

{{< callout context="note" title="Current version" icon="info-circle" >}}
This documentation tracks **`4.3.2`**. The issue lifecycle (`raiseIssue` / `resolveIssue`),
runtime detector toggling and `null`-means-don't-construct config were introduced in `4.3.0`
and changed several APIs — see [Events & issues](./events-and-issues/) for the current model.
{{< /callout >}}

## Install

```bash
npm install @observertc/client-monitor-js
```

```bash
yarn add @observertc/client-monitor-js
```

Runtime dependencies: `eventemitter3` and `ua-parser-js`. Ships ESM with TypeScript declarations,
tree-shakeable (`sideEffects: false`), targeting evergreen browsers.

## Sixty-second start

```javascript
import { ClientMonitor } from "@observertc/client-monitor-js";

const monitor = new ClientMonitor({
    clientId: "user-42",
    callId: "room-abc",
    collectingPeriodInMs: 2000,   // how often getStats() is polled
    samplingPeriodInMs: 4000,     // how often a ClientSample is emitted
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
monitor.on("sample-created", (sample) => transport.send(sample));

// 4. Clean shutdown — still-open issues auto-resolve.
monitor.close();
```

That is the whole integration. Everything below is about what you get for free, and how to bend
it to your application.

## What the library actually does for you

{{< callout context="tip" title="The short version" icon="rocket" >}}
Raw `getStats()` gives you monotonically increasing counters. Almost every question you want to
ask — *"what is the bitrate?"*, *"is video frozen?"*, *"is the CPU the bottleneck?"* — requires
differencing those counters across ticks, normalising browser differences, and applying
hysteresis so you do not alert on a single bad sample. That is the work this library does.
{{< /callout >}}

### 1. Counters become metrics

`getStats()` reports `bytesReceived: 918273645`. What you want is *bits per second over the last
interval*. The library computes per-interval deltas and rates for every stat type, and exposes
them as plain properties:

```javascript
monitor.sendingVideoBitrate;              // bps, aggregated across all peer connections
pcMonitor.deltaInboundPacketsLost;        // packets lost in this interval only
inboundRtp.ewmaFps;                       // smoothed frame rate
inboundRtp.fpsVolatility;                 // how unstable that frame rate is
outboundRtp.payloadBitrate;               // excludes headers and retransmissions
candidatePair.availableOutgoingBitrate;   // the browser's own bandwidth estimate
```

See [Derived metrics](./metrics/) for the full catalogue.

### 2. Raw stats become a navigable object graph

Browser stats are a flat map of records joined by string ids. The library resolves those joins
once and hands you objects that know their neighbours:

```javascript
const track = monitor.tracks.find((t) => t.kind === "video" && t.direction === "outbound");
const rtp = track.getHighestLayer();          // the top simulcast layer
const remote = rtp.getRemoteInboundRtp();     // what the far end reports about it
const source = rtp.getMediaSource();          // the local camera feeding it
```

### 3. Symptoms become verdicts

Seven built-in detectors watch for the conditions that actually degrade calls, each with its own
on/off thresholds so a single noisy tick does not raise an alert:

| Issue `type` | What it catches |
|---|---|
| `congestion` | Sending or receiving above the available bandwidth estimate |
| `cpulimitation` | Encoder CPU limitation, slow stats collection, or received frames not being decoded |
| `audio-desync` | Audio being accelerated/decelerated to stay in sync |
| `freezed-video-track` | Video freeze count climbing |
| `dry-inbound-track` / `dry-outbound-track` | A track that stopped moving bytes |
| `inbound-video-playout-discrepancy` | Frames arriving but not being rendered |

Every one of them **raises** an issue when the condition starts and **resolves** it when the
condition clears, enriching the resolution with `durationInMs`. That is the difference between
"we saw congestion" and "congestion lasted 14 seconds on this peer connection".

[Detectors →](./detectors/) &nbsp;·&nbsp; [Events & issues →](./events-and-issues/)

### 4. Quality becomes a number you can chart

A `DefaultScoreCalculator` produces 0.0–5.0 scores for each track, each peer connection and the
client as a whole, together with a breakdown of *why*:

```javascript
monitor.on("score", ({ clientScore, scoreReasons }) => {
    // clientScore: 3.2
    // scoreReasons: { "high-rtt": 1.0, "high-packetloss": 0.8 }
});
```

The whole calculator is replaceable — see [Scoring](./scoring/).

### 5. Everything becomes a `ClientSample`

On the sampling period the monitor snapshots its entire state into a
[`ClientSample`](/docs/schema/clientsample/): every peer connection, every stats record, the
events and issues since the last sample, your metadata and your extension stats. That object is
the input to [`observer-js`](/docs/libraries/observer-js/) and to your own storage.

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
  description="React in the client: drop to audio-only on sustained congestion, lower the encoding on cpulimitation, prompt a device change on a dry outbound track."
  href="./detectors/" >}}
{{< /card-grid >}}

## Integration surface

| Extension point | What you can do |
|---|---|
| **Sources** | `RTCPeerConnection`, a mediasoup `Device` (new transports hooked automatically) or a single mediasoup transport |
| **Detectors** | Add your own, remove built-ins, or toggle any of them at runtime |
| **Score calculator** | Replace the scoring model wholesale while keeping the metric plumbing |
| **Stats adapters** | Pre- and post-process the raw stats array — normalise, filter, or synthesize records |
| **Extension stats providers** | Inject application metrics (sync or async) into every sample |
| **`attachments` / `appData`** | Per-entity data that either ships with samples or stays local |
| **Logger** | Route the library's logs into your own logger, or silence it entirely |

## Documentation map

{{< card-grid >}}
{{< link-card title="Integrations" description="RTCPeerConnection, mediasoup, and logging setup." href="./integrations/" >}}
{{< link-card title="Configuration" description="Every option, with defaults and the null / undefined / object rule." href="./configuration/" >}}
{{< link-card title="Detectors" description="The seven built-ins, their thresholds, and writing your own." href="./detectors/" >}}
{{< link-card title="Events & issues" description="The raise / update / resolve lifecycle and type-safe handling." href="./events-and-issues/" >}}
{{< link-card title="Scoring" description="How the default 0–5 score is computed and how to replace it." href="./scoring/" >}}
{{< link-card title="Monitors & derived metrics" description="The object graph and every computed field on it." href="./metrics/" >}}
{{< link-card title="Sampling & transport" description="Samples, stats adapters, extension stats, and binary compression." href="./sampling/" >}}
{{< link-card title="Recipes" description="Worked patterns: dashboards, adaptive UX, production tuning, frameworks." href="./recipes/" >}}
{{< link-card title="API reference" description="Constructor, methods, properties and the full event table." href="./api-reference/" >}}
{{< /card-grid >}}

## Resources

- [npm package](https://www.npmjs.com/package/@observertc/client-monitor-js)
- [GitHub repository](https://github.com/ObserveRTC/client-monitor-js)
- [Schema definitions](/docs/schema/)
