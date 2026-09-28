---
slug: "integrations"
title: "Browser & mediasoup integration"
description: "Attach sources and declare the context the browser cannot infer."
lead: "Attach sources and declare the context the browser cannot infer."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 10
toc: true
---

## RTCPeerConnection

```javascript
monitor.addSource(peerConnection);
// During application teardown:
monitor.removeSource(peerConnection);
```

Register the connection you already use for media. Removing a source stops monitoring it; your application still owns the connection.

## mediasoup-client

Attach a device before it creates transports. Attach existing transports explicitly:

```javascript
monitor.addSource(device, 'mediasoup-device');
// For a transport created before device instrumentation:
monitor.addSource(transport, 'mediasoup-transport');
```

## Application context

Tell the monitor about application intent through `setInboundTrackContext` and `setOutboundTrackContext`. Pausing, screen sharing and expected media flow can change the meaning of a silent interval. Context may be pending until the track appears.

Keep identifiers distinct: a browser stats ID, SSRC, MediaStreamTrack ID and SFU producer ID identify different things. Use track attachments and a server resolver for publisher/subscriber correlation.

[Context and extension stats](/docs/client-monitor-js/events-and-issues/) · [Server SFU integration](/docs/observer-js/sfu/)

Sources: [ClientMonitor.addSource](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts), [Sources](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/sources/Sources.ts).
