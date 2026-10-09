---
title: "Client Monitor"
description: "Collect browser stats, inspect live monitors, and detect endpoint problems."
lead: "Collect browser stats, inspect live monitors, and detect endpoint problems."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "RSS", "SITEMAP", "Markdown"]
landingTitle: "What is Client Monitor?"
weight: 20
toc: true
---

Client Monitor helps you understand what happens at one WebRTC endpoint. It runs in the browser beside the connections your application already owns, reads `getStats()` reports, and turns them into live metrics, issue evidence, and samples for your backend.

## Why use it?

Browser statistics are distributed across connections, tracks, streams, and network objects. Their fields vary between browsers, and many useful rates require comparing observations over time. Client Monitor connects these measurements so you can investigate questions such as whether a received video stopped arriving, decoding, or playing.

## What it provides

| Capability | What you can do with it |
|---|---|
| Browser-stat adaptation | Work with normalized reports while retaining the distinction between reported and inferred values. |
| Live monitor relationships | Follow a track to its RTP streams, codec, and transport. |
| Derived metrics | Read interval bitrates and other calculated measurements after collection. |
| Endpoint detectors | Evaluate defined connectivity, transport, pipeline, and quality conditions. |
| Issues and events | React locally and record discrete telemetry for samples. |
| Quality scores | Locate affected components using penalties and reasons. |
| Samples and extensions | Send a schema-defined snapshot and your explicit application context through your own transport. |

## How collection works

```text
Your peer connection → browser statistics → adaptation
                                         → monitor updates
                                         → detector evaluation
                                         → quality scores
                                         → local events / scheduled sample
```

Each collection updates live state. Sampling packages current stat snapshots and buffered records; it does not average every collection since the previous sample. Collection and sampling both default to five seconds. Shorter collection intervals cost more browser work and shorten value-counted detection windows.

## Start monitoring

```javascript
import { ClientMonitor } from '@observertc/client-monitor-js';

const monitor = new ClientMonitor({
  clientId: 'participant-42',
  callId: 'room-123',
});
monitor.addSource(peerConnection);
monitor.on('stats-collected', () => {
  console.log('Received video, bits/s:', monitor.receivingVideoBitrate);
});
```

`peerConnection` is your existing browser connection. With active received video and successive usable observations, you can inspect the received bitrate. If it is unavailable, check media direction and browser evidence rather than converting it to zero. Follow the [quick start](/docs/client-monitor-js/quick-start/) for sample forwarding and cleanup.

## Integration decisions

- Attach each relevant connection, or instrument your [mediasoup device/transports](/docs/client-monitor-js/integrations/).
- Use [configuration](/docs/client-monitor-js/configuration/) to choose collection cadence, sample detail, and detector settings.
- Declare [application context](/docs/client-monitor-js/application-context/) so intentional pauses and screen sharing are interpreted correctly.
- Handle [events](/docs/client-monitor-js/monitor-events/) and [issues](/docs/client-monitor-js/monitor-issues/) through distinct channels.
- Choose a transport only when you need backend reporting. Client Monitor also works locally.

## Runtime state and boundaries

The root monitor exposes aggregate metrics and arrays of child monitors. A track is not the same as an RTP encoding; a sending track can have several streams. Read [Monitor API and relationships](/docs/client-monitor-js/api-reference/) before joining objects by identifiers.

Statistics may be unavailable, delayed, or reset. Detectors have input guards and thresholds; their output does not independently prove a root cause. The library does not create calls, control your media routing, authenticate your telemetry, or store history.

Call `monitor.close()` when monitoring ends. Your application decides when to close the actual peer connection. If sending telemetry, attach listeners before sampling begins and choose how to handle delivery failures.

## Go deeper

Use [metrics and missing values](/docs/client-monitor-js/metrics/), [collection and sampling](/docs/client-monitor-js/sampling/), [quality scores](/docs/client-monitor-js/scoring/), and the [detector catalog](/docs/client-monitor-js/detectors/) for implementation behavior and evidence. The [public catalog](/docs/reference/monitor-catalog/) retains its documented source baseline.

Installation and configuration guidance covers **4.10.1**. Install with `npm install @observertc/client-monitor-js`; detailed references identify their verified versions.

[Release source](https://github.com/ObserveRTC/client-monitor-js/blob/4ae541eac3305d1cc779ff6dd703211e837a7f7b/src/ClientMonitor.ts) · [Version coverage](/docs/reference/versions/).
