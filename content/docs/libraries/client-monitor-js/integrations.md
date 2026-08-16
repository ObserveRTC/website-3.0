---
title: "Integrations"
slug: "integrations"
description: "Connecting client-monitor-js to RTCPeerConnection, mediasoup and your logger"
lead: "How to attach the monitor to the things that produce WebRTC statistics"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 311
toc: true
---

The monitor collects nothing until you give it a **source**. A source is anything that owns
`RTCPeerConnection`s: a peer connection itself, a mediasoup `Device`, or a single mediasoup
transport.

```javascript
monitor.addSource(source);
```

The monitor keeps polling each source on the collecting period and cleans up automatically when a
peer connection closes — you never need to remove a source by hand.

## RTCPeerConnection

The plain case. Works for P2P, for a client talking to any SFU, and for any number of connections.

```javascript
import { ClientMonitor } from "@observertc/client-monitor-js";

const monitor = new ClientMonitor({ clientId, callId });

const pc = new RTCPeerConnection(config);
monitor.addSource(pc);
```

Multiple peer connections are supported directly — add each one, and the client-level metrics
aggregate across all of them:

```javascript
monitor.addSource(publishPc);
monitor.addSource(subscribePc);

monitor.sendingVideoBitrate;   // summed across both
monitor.peerConnections;       // PeerConnectionMonitor[]
```

{{< callout context="note" title="Closed connections" icon="info-circle" >}}
When a peer connection closes, the monitor releases the associated monitors and emits the
corresponding events. There is no `removeSource` to call.
{{< /callout >}}

## mediasoup

Adding a mediasoup `Device` is the recommended integration: the monitor hooks the device's
`newtransport` event, so every transport created *after* the device is added is monitored
automatically.

```javascript
import mediasoup from "mediasoup-client";
import { ClientMonitor } from "@observertc/client-monitor-js";

const device = new mediasoup.Device();
await device.load({ routerRtpCapabilities });

const monitor = new ClientMonitor({ clientId, callId });
monitor.addSource(device);

// Automatically monitored — no extra call needed.
const sendTransport = device.createSendTransport(transportOptions);
const producer = await sendTransport.produce({ track: videoTrack });
```

{{< callout context="caution" title="Transports created before the device was added" icon="alert-triangle" >}}
The `newtransport` hook only sees transports created after `addSource(device)`. If your
application creates transports first and wires up monitoring later, add those transports
explicitly:

```javascript
monitor.addSource(existingTransport);
```
{{< /callout >}}

The mediasoup integration also installs a stats adapter that filters mediasoup's `probator` track
out of the collected stats, so probe traffic does not pollute your bitrates or trigger detectors.

### Tagging tracks for server-side correlation

If you are going to feed samples to [`observer-js`](/docs/libraries/observer-js/) and want it to
link a publisher's outbound track to every subscriber's inbound track, put mediasoup's ids into the
track `attachments`. The default resolver on the server reads `producerId` and `consumerId`:

```javascript
const producer = await sendTransport.produce({ track });
monitor.getTrackMonitor(track.id).attachments = {
    producerId: producer.id,
    direction: "send",
    label: "camera",
};

const consumer = await recvTransport.consume(consumerOptions);
monitor.getTrackMonitor(consumer.track.id).attachments = {
    consumerId: consumer.id,
    producerId: consumer.producerId,
    direction: "recv",
};
```

This is what makes server-side questions like *"did everyone receiving Alice see the same
freeze?"* answerable. See [Remote track resolution](/docs/libraries/observer-js/sfu/).

## Logging

By default the library logs `warn` and `error` to the console and treats `trace` / `debug` /
`info` as no-ops. Pass your own `logger` to route everything into your application's logging
stack — the same instance is propagated into sources and internal monitors, and messages carry
module prefixes such as `[ClientMonitor]:` and `[Sources]:`.

{{< tabs "logger" >}}
{{< tab "Custom" >}}
```typescript
import { ClientMonitor, Logger } from "@observertc/client-monitor-js";

const logger: Logger = {
    trace: (...args) => console.trace(...args),
    debug: (...args) => console.debug(...args),
    info:  (...args) => console.info(...args),
    warn:  (...args) => console.warn(...args),
    error: (...args) => console.error(...args),
};

const monitor = new ClientMonitor({ logger });
```
{{< /tab >}}
{{< tab "Adapter" >}}
```javascript
import { ClientMonitor } from "@observertc/client-monitor-js";
import pino from "pino";

const appLogger = pino({ level: "info" });

const monitor = new ClientMonitor({
    logger: {
        trace: (...a) => appLogger.trace(...a),
        debug: (...a) => appLogger.debug(...a),
        info:  (...a) => appLogger.info(...a),
        warn:  (...a) => appLogger.warn(...a),
        error: (...a) => appLogger.error(...a),
    },
});
```
{{< /tab >}}
{{< tab "Silent" >}}
```javascript
const noop = () => {};

const monitor = new ClientMonitor({
    logger: { trace: noop, debug: noop, info: noop, warn: noop, error: noop },
});
```
{{< /tab >}}
{{< /tabs >}}

{{< callout context="caution" title="Breaking change in 4.3.0" icon="alert-triangle" >}}
The global `setLogger()` API was removed in favour of per-instance injection through the
constructor. If you were calling `setLogger`, move that object into `new ClientMonitor({ logger })`.
{{< /callout >}}

## Browser environment integration

Two optional helpers enrich samples with environment information:

`integrateNavigatorMediaDevices` defaults to `true`, so the monitor watches
`navigator.mediaDevices` and records the device list and any device changes as client metadata
without you doing anything. Set it to `false` in the [configuration](../configuration/) to opt out.

Browser, engine, platform and OS are resolved from User-Agent Client Hints on start-up; you can
also trigger it yourself:

```javascript
await monitor.fetchUserAgentData();
```

All of this arrives server-side as `client-metadata` events and populates
`observedClient.browser` / `.platform` / `.operationSystem` / `.mediaDevices`.

## Browser differences

You do not need to handle browser quirks yourself — the monitor installs adapters based on
detected browser:

| Adapter | Applies to | What it fixes |
|---|---|---|
| `Firefox94StatsAdapter` | Firefox | Normalises `mediaType` to `kind` on RTP stats |
| `FirefoxTransportStatsAdapter` | Firefox | Synthesizes transport stats from ICE candidate pairs |
| mediasoup probator filter | mediasoup sources | Drops `probator` track records |

If you need your own normalisation on top, see [Stats adapters](../sampling/#stats-adapters).
