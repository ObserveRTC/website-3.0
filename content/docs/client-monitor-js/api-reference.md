---
slug: "api-reference"
title: "Monitor API and relationships"
description: "Navigate ownership, cross-links and the public API."
lead: "Navigate ownership, cross-links and the public API."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "Markdown"]
weight: 30
toc: true
---
## What a monitor represents

`ClientMonitor` is the starting point for one endpoint. Each peer connection has its own monitor, and its tracks, RTP streams, codecs, and network path are connected through references. This lets you follow a symptom from “receiving video is poor” down to the relevant stream and transport.

A **track** is the audio or video your application works with. An **RTP stream** is an encoded stream carrying that track over the network. A sending video track can have several RTP streams, such as simulcast layers, so a track and a stream are not interchangeable.

## Navigate the graph

```text
ClientMonitor — this endpoint
├── PeerConnectionMonitor — one browser connection
│   ├── InboundTrackMonitor — received audio/video
│   │   └── InboundRtpMonitor — received stream measurements
│   ├── OutboundTrackMonitor — sent audio/video
│   │   └── OutboundRtpMonitor(s) — one or more encoded streams
│   ├── Remote RTP reports — the other endpoint's reported measurements
│   ├── Codecs — encoding used by the streams
│   ├── Media sources / playout — capture and playback measurements
│   ├── ICE transports → selected candidate pair → candidates
│   └── Data channels / certificates / peer-connection statistics
└── ExtensionStatsMonitor — your additional application measurements
```

The diagram groups objects for reading; references between them are described below. Root getters also provide convenient arrays across connections, so you do not need to traverse every connection for every query.

```javascript
monitor.on('stats-collected', () => {
  for (const connection of monitor.peerConnections) {
    console.log('Connection:', connection.peerConnectionId);
  }
  const trackMonitor = monitor.getTrackMonitor(mediaTrack.id);
  if (trackMonitor) {
    console.log('Track score:', trackMonitor.score);
  }
});
```

`mediaTrack` is a `MediaStreamTrack` from your application. A lookup can return `undefined` before statistics discover the object or after it is removed. Read the graph after `stats-collected` when you need the latest metrics.

## Choose the right scope

| Question | Start with |
|---|---|
| Is this endpoint generally healthy? | The root client's aggregate metrics and score. |
| Which connection is failing? | `peerConnections` and the connection's issues/transport state. |
| Is a specific camera or received video affected? | `getTrackMonitor(trackId)` and its associated RTP measurements. |
| Are multiple encodings being sent? | The outbound track's RTP streams. |
| What network path is carrying media? | ICE transports, selected pairs, and local/remote candidates. |
| What did the remote endpoint report? | Remote RTP reports when the browser supplies them. |
| Which fields exist and what are their types? | The [public monitor catalog](/docs/reference/monitor-catalog/). |

## Public operations

`src/index.ts` is the package export boundary. `ClientMonitor` is the root EventEmitter3-based API. Its core operations are:

| Need | Public surface |
|---|---|
| Attach instrumentation | `addSource(source, type?)`, `removeSource(source, type?)`; types: `RTCPeerConnection`, mediasoup device, mediasoup transport |
| Control updates | `collect()`, `setCollectingPeriod(ms)`, `setSamplingPeriod(ms)`, `createSample()`, `close()` |
| Identity / app-owned state | `clientId`, `callId`, `appData`, `attachments` |
| Traverse | `peerConnections`, `tracks`, `inboundRtps`, `outboundRtps`, remote RTP arrays, codecs, ICE entities, media sources/playouts, certificates, data channels; `getPeerConnectionMonitor`, `getTrackMonitor`, direction-specific getters |
| Declare intent | `setInboundTrackContext(trackId, context)`, `setOutboundTrackContext(trackId, context)`; pending context is applied when the track appears |
| Extend | `extensionStatsProviders`, `addExtensionStats`, `getExtensionStatsPayload`, `getExtensionStatsMonitor`; replaceable `scoreCalculator`; per-PC `statsAdapters`; scoped detector registries |
| Record | `addEvent`, `addIssue`, `raiseIssue`, `resolveIssue`, `addMetaData`, join/left event helpers |
| Subscribe | `on`, `once`, `off`, typed `ClientMonitorEvents`; convenience callback setters |

{{< details "Source references" >}}

- [client-monitor-js/src/index.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/index.ts)
- [client-monitor-js/src/ClientMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts)
- [client-monitor-js/docs/MONITOR_API.md](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/docs/MONITOR_API.md)

{{< /details >}}

Export nuances matter: `DefaultScoreCalculator` is exported as a **type** from the package root, despite being a runtime class internally; not every detector class is root-exported merely because its config type is.

## Ownership and cross-links

The graph has ownership and cross-links:

- Client → peer connections, plus root extension monitors and client detector registry.
- PC → maps of codecs, inbound/outbound RTP, remote RTP, sources/playouts, data channels, ICE candidates/pairs/transports, certificates, peer-connection stats, inbound/outbound tracks.
- RTP → codec (`codecId`), ICE transport (`transportId`), counterpart remote report, track; outbound RTP → media source; inbound RTP → media playout.
- Track → actual `MediaStreamTrack` plus associated stream(s); outbound tracks can own several simulcast encodings, while an inbound track holds its inbound RTP monitor.
- ICE transport → selected pair; pair → local/remote candidates; `SelectedIcePath` tracks path identity, evidence and transitions. A PC may contain several transports; never assume one transport equals one PC.
- Track/PC issue registries forward toward the root registry. Ownership is not the same as the detector taxonomy.

{{< details "Source references" >}}

- [client-monitor-js/src/monitors/PeerConnectionMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts)
- [client-monitor-js/src/monitors/InboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts)
- [client-monitor-js/src/monitors/OutboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts)
- [client-monitor-js/src/monitors/InboundTrackMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts)
- [client-monitor-js/src/monitors/OutboundTrackMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts)
- [client-monitor-js/src/monitors/SelectedIcePath.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts)
- [client-monitor-js/src/utils/IssueRegistry.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/IssueRegistry.ts)

{{< /details >}}

## Identifier scope

RTP monitor maps use SSRC in several lookup paths; stats-object IDs are not interchangeable with SSRC or `MediaStreamTrack` IDs. Preserve each identifier's role when adding fields or joining server entities. `visited` getters can consume/reset bookkeeping state; never read them from an inspector UI.

[Browse all public fields in the monitor catalog →](/docs/reference/monitor-catalog/)
