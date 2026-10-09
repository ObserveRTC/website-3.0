---
slug: "integrations"
title: "Browser & mediasoup integration"
description: "Attach sources and declare the context the browser cannot infer."
lead: "Attach sources and declare the context the browser cannot infer."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "Markdown"]
weight: 10
toc: true
---
Client Monitor attaches to your existing media objects. Start with a peer connection if your application uses the browser API directly, or attach a mediasoup device if mediasoup manages your transports.

## RTCPeerConnection

```javascript
monitor.addSource(peerConnection);
// During application teardown:
monitor.removeSource(peerConnection);
```

Register the connection you already use for media. Removing a source stops monitoring it; your application still owns the connection.

## mediasoup-client

A mediasoup device creates the send and receive transports used by your application. Attaching the device early lets the monitor follow new transports. If a transport already exists, register that transport explicitly:

```javascript
monitor.addSource(device, 'mediasoup-device');
// For a transport created before device instrumentation:
monitor.addSource(transport, 'mediasoup-transport');
```

## Application context

The browser cannot tell whether a quiet stream is intentionally paused or unexpectedly broken. Tell the monitor about application intent through `setInboundTrackContext` and `setOutboundTrackContext`. Pausing, screen sharing and expected media flow can change the meaning of a silent interval. Context may be pending until the track appears.

Keep identifiers distinct: a browser stats ID, SSRC, `MediaStreamTrack` ID and SFU producer ID identify different things. Use track attachments and a server resolver for publisher/subscriber correlation.

[Application context](/docs/client-monitor-js/application-context/) · [Server SFU integration](/docs/observer-js/sfu/)

Sources: [ClientMonitor.addSource](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts), [Sources](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/sources/Sources.ts).
