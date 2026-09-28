---
slug: "introduction"
title: "Quick start"
description: "Add monitoring to an existing WebRTC connection."
lead: "Add monitoring to an existing WebRTC connection."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 10
toc: true
---

ObserveRTC is a set of libraries for WebRTC monitoring. Start in the browser with Client Monitor. Add sample transport and Observer when you need analysis across participants.

## Install Client Monitor

```bash
npm install @observertc/client-monitor-js@4.9.1
```

Use your application's existing `RTCPeerConnection`:

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

// Call monitor.close() when the session ends.
```

Collection and sampling both default to five seconds. Rates need successive measurements; missing values and initial sentinel values are not healthy measurements.

## Send samples when you need a backend

```javascript
monitor.on('sample-created', ({ sample }) => {
  // Use your application's authenticated, ordered transport.
  sendSample(sample);
});
```

`sendSample` is application code. Client Monitor does not choose your server, transport or storage. Subscribe before the first sample; buffering samples before a subscriber is opt-in.

On the server:

```bash
npm install @observertc/observer-js@1.0.0
```

```javascript
import { Observer } from '@observertc/observer-js';

const observer = new Observer();

// After your endpoint authenticates and validates an incoming sample:
observer.accept(sample);

// Call observer.close() during application shutdown.
```

Both `clientId` and `callId` must be present for Observer ingestion. Register server detectors explicitly: a new Observer has none.

## Next steps
{{< card-grid >}}
{{< link-card title="Read the monitor graph" description="Find a track, RTP stream, codec or selected ICE path." href="/docs/client-monitor-js/api-reference/" >}}
{{< link-card title="Choose detectors" description="Understand the five categories and their evidence." href="/docs/client-monitor-js/detectors/" >}}
{{< link-card title="Define the wire contract" description="See what is and is not serialized." href="/docs/schema/clientsample/" >}}
{{< /card-grid >}}
Sources: [ClientMonitor](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts), [Observer.accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts#L710).
