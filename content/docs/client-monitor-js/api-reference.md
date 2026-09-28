---
slug: "api-reference"
title: "Monitor API & graph"
description: "Navigate ownership, cross-links and the public API."
lead: "Navigate ownership, cross-links and the public API."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 20
toc: true
---

`src/index.ts` is the package export boundary. `ClientMonitor` is the root EventEmitter3-based API. Its core operations are:

| Need | Public surface |
|---|---|
| Attach instrumentation | `addSource(source, type?)`, `removeSource(source, type?)`; types: RTCPeerConnection, mediasoup device, mediasoup transport |
| Control updates | `collect()`, `setCollectingPeriod(ms)`, `setSamplingPeriod(ms)`, `createSample()`, `close()` |
| Identity / app-owned state | `clientId`, `callId`, `appData`, `attachments` |
| Traverse | `peerConnections`, `tracks`, `inboundRtps`, `outboundRtps`, remote RTP arrays, codecs, ICE entities, media sources/playouts, certificates, data channels; `getPeerConnectionMonitor`, `getTrackMonitor`, direction-specific getters |
| Declare intent | `setInboundTrackContext(trackId, context)`, `setOutboundTrackContext(trackId, context)`; pending context is applied when the track appears |
| Extend | `extensionStatsProviders`, `addExtensionStats`, `getExtensionStatsPayload`, `getExtensionStatsMonitor`; replaceable `scoreCalculator`; per-PC `statsAdapters`; scoped detector registries |
| Record | `addEvent`, `addIssue`, `raiseIssue`, `resolveIssue`, `addMetaData`, join/left event helpers |
| Subscribe | `on`, `once`, `off`, typed `ClientMonitorEvents`; convenience callback setters |

Sources: [client-monitor-js/src/index.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/index.ts), [client-monitor-js/src/ClientMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts), [client-monitor-js/docs/MONITOR_API.md](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/docs/MONITOR_API.md). Export nuances matter: `DefaultScoreCalculator` is exported as a **type** from the package root, despite being a runtime class internally; not every detector class is root-exported merely because its config type is.

The graph has ownership and cross-links:

- Client → peer connections, plus root extension monitors and client detector registry.
- PC → maps of codecs, inbound/outbound RTP, remote RTP, sources/playouts, data channels, ICE candidates/pairs/transports, certificates, peer-connection stats, inbound/outbound tracks.
- RTP → codec (`codecId`), ICE transport (`transportId`), counterpart remote report, track; outbound RTP → media source; inbound RTP → media playout.
- Track → actual MediaStreamTrack plus associated stream(s); outbound tracks can own several simulcast encodings, while an inbound track holds its inbound RTP monitor.
- ICE transport → selected pair; pair → local/remote candidates; `SelectedIcePath` tracks path identity, evidence and transitions. A PC may contain several transports; never assume one transport equals one PC.
- Track/PC issue registries forward toward the root registry. Ownership is not the same as the detector taxonomy.

References: [client-monitor-js/src/monitors/PeerConnectionMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts), [client-monitor-js/src/monitors/InboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundRtpMonitor.ts), [client-monitor-js/src/monitors/OutboundRtpMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundRtpMonitor.ts), [client-monitor-js/src/monitors/InboundTrackMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts), [client-monitor-js/src/monitors/OutboundTrackMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts), [client-monitor-js/src/monitors/SelectedIcePath.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts), [client-monitor-js/src/utils/IssueRegistry.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/IssueRegistry.ts).

RTP monitor maps use SSRC in several lookup paths; stats-object IDs are not interchangeable with SSRC or MediaStreamTrack IDs. Preserve each identifier's role when adding fields or joining server entities. `visited` getters can consume/reset bookkeeping state; never read them from an inspector UI.

[Browse all public fields in the monitor catalog →](/docs/reference/monitor-catalog/)
