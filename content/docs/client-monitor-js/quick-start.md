---
slug: "quick-start"
title: "Quick start"
description: "Quick start for engineers integrating ObserveRTC."
draft: false
outputs: ["HTML", "Markdown"]
weight: 5
toc: true
---

Client Monitor runs alongside the WebRTC connection your application already owns. It reads browser statistics and reports metrics and issues; it does not create calls or send media.

## Install

```bash
npm install @observertc/client-monitor-js
```

## Monitor a connection

```javascript
import { ClientMonitor } from '@observertc/client-monitor-js';

const monitor = new ClientMonitor({
  clientId: 'participant-42',
  callId: 'room-123',
});
monitor.addSource(peerConnection);

monitor.on('stats-collected', () => {
  console.log('Receiving video (bps):', monitor.receivingVideoBitrate);
  console.log('Quality score:', monitor.score);
});
monitor.on('issue', issue => console.log(issue.type, issue.payload));
```

Here `peerConnection` is your existing `RTCPeerConnection`. Choose identifiers from your application: `callId` groups participants into a call, and `clientId` identifies this monitored client. They are required if you later send samples to Observer.

By default the monitor collects every five seconds. Rates require successive measurements, so the first update may not contain a usable bitrate. Treat a missing value as unavailable, rather than zero.

## Add backend reporting when needed

```javascript
monitor.on('sample-created', ({ sample }) => {
  sendSample(sample);
});
```

`sendSample` is your function for forwarding samples over an authenticated transport. Attach this listener before the first sample. Client Monitor can also be used entirely in the browser, without Observer.

## Clean up

Call `monitor.close()` when monitoring ends. Your application still owns the peer connection and decides when to close it.

Continue with [browser and mediasoup integration](/docs/client-monitor-js/integrations/) and [configuration](/docs/client-monitor-js/configuration/).
