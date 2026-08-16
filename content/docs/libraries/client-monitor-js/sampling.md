---
title: "Sampling & transport"
slug: "sampling"
description: "Creating ClientSamples, adapting stats, extension stats and binary compression"
lead: "How client state becomes a ClientSample, and how to get it to your backend efficiently"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 317
toc: true
---

A **sample** is a snapshot of everything the monitor knows at one instant, serialised into the
[`ClientSample`](/docs/schema/clientsample/) schema. It is the unit of telemetry: what you upload,
what you store, and what [`observer-js`](/docs/libraries/observer-js/) consumes.

## What a sample contains

| Section | Content |
|---|---|
| Identity | `clientId`, `callId`, `timestamp`, `score`, `scoreReasons`, `attachments` |
| `peerConnections[]` | Every monitored peer connection with all fifteen stats arrays |
| `clientEvents[]` | Events recorded since the last sample |
| `clientIssues[]` | Issues raised (and resolutions) since the last sample |
| `clientMetaItems[]` | Device lists, browser/OS metadata, SDP, media constraints |
| `extensionStats[]` | Whatever your extension stats providers returned |

## Automatic sampling

Set `samplingPeriodInMs` and the monitor emits a sample on that cadence:

```javascript
const monitor = new ClientMonitor({
    collectingPeriodInMs: 2000,
    samplingPeriodInMs: 4000,
});

monitor.on("sample-created", (sample) => {
    transport.send(sample);
});
```

Events and issues that occur between samples are buffered and all ship in the next one — a longer
sampling period costs you timing resolution on the server, not data.

## Manual sampling

Omit `samplingPeriodInMs` and call `createSample()` yourself. You **must** set
`bufferingEventsForSamples: true`, otherwise events and issues are not retained between calls.

```javascript
const monitor = new ClientMonitor({
    collectingPeriodInMs: 2000,
    bufferingEventsForSamples: true,
});

// Drive sampling from your own scheduler, or on demand.
const sample = monitor.createSample();
if (sample) transport.send(sample);
```

Manual sampling is the right choice when upload timing is not yours to decide — batching into an
existing telemetry channel, flushing on `visibilitychange`, or sampling only while a support agent
is watching.

## Stats adapters

Adapters sit between `getStats()` and the monitors. Each one can rewrite the stats array before
the monitors consume it (`adapt`) and again after they have updated (`postAdapt`).

### The processing flow

{{< steps >}}
{{< step >}}**Collect** — `getStats()` is called on every source.{{< /step >}}
{{< step >}}**Pre-adapt** — every adapter's `adapt(stats)` runs, in registration order.{{< /step >}}
{{< step >}}**Update** — monitors consume the adapted stats and recompute derived fields.{{< /step >}}
{{< step >}}**Post-adapt** — every adapter's `postAdapt(stats)` runs, for cross-stat work.{{< /step >}}
{{< step >}}**Detect & score** — detectors run, then the score calculator.{{< /step >}}
{{< /steps >}}

### Built-in adapters

Installed automatically based on the detected environment:

| Adapter | Applies to | Purpose |
|---|---|---|
| `Firefox94StatsAdapter` | Firefox | Normalises `mediaType` → `kind` on RTP stats |
| `FirefoxTransportStatsAdapter` | Firefox | Synthesizes transport stats from ICE candidate pairs |
| mediasoup probator filter | mediasoup sources | Drops probe traffic from the stats array |

### Where adapters live

Adapters are registered per peer connection, on `peerConnectionMonitor.statsAdapters`. The
registry is keyed by the adapter's `name`, so adding two adapters with the same name is a no-op
(the second is rejected with a warning).

```javascript
monitor.on("stats-collected", () => {
    for (const pc of monitor.peerConnections) {
        if (!pc.statsAdapters.adapters.has("my-adapter")) {
            pc.statsAdapters.add(myAdapter);
        }
    }
});
```

### A full adapter class

An adapter is an object with a `name`, a required `adapt(stats)` and an optional
`postAdapt(stats)`. Errors thrown from either are caught and logged — a broken adapter cannot stop
collection.

```javascript
class CorrelationAdapter {
    name = "correlation-adapter";

    adapt(stats) {
        // Runs before monitors update — normalise, filter, annotate.
        return stats.filter((s) => s.trackIdentifier !== "probator");
    }

    postAdapt(stats) {
        // Runs after monitors update — synthesize records from several stats at once.
        const pair = stats.find((s) => s.type === "candidate-pair" && s.state === "succeeded");
        if (!pair?.availableIncomingBitrate) return stats;

        const inboundTotal = stats
            .filter((s) => s.type === "inbound-rtp")
            .reduce((sum, s) => sum + (s.bitrate ?? 0), 0);

        stats.push({
            type: "custom-bandwidth",
            id: "bandwidth-estimation",
            timestamp: Date.now(),
            estimatedBandwidth: pair.availableIncomingBitrate,
            utilization: inboundTotal / pair.availableIncomingBitrate,
        });

        return stats;
    }
}

const adapter = new CorrelationAdapter();
pcMonitor.statsAdapters.add(adapter);

// Remove by instance or by name.
pcMonitor.statsAdapters.remove(adapter);
pcMonitor.statsAdapters.remove("correlation-adapter");
```

{{< callout context="note" title="Extension stats are usually the better tool" icon="info-circle" >}}
If you want to *add* your own numbers to the telemetry, use an
[extension stats provider](#extension-stats-providers) rather than synthesizing stats records in
`postAdapt`. Adapters are for reshaping what the browser reported; providers are for what only
your application knows.
{{< /callout >}}

{{< callout context="caution" title="Adapters run on every tick" icon="alert-triangle" >}}
An adapter is on the hot path of every stats collection, on the main thread. Keep them cheap:
filtering and field rewriting, not heavy computation. If you need expensive work, do it in an
[extension stats provider](#extension-stats-providers), which can be asynchronous.
{{< /callout >}}

## Extension stats providers

Extension stats are your own metrics, injected into the pipeline and shipped in every sample.
They exist so you can correlate WebRTC quality with things only your application knows: render
frame rate, decode worker backlog, feature flags, a user-visible latency measurement.

```javascript
// Synchronous.
monitor.extensionStatsProviders.add(() => ({
    type: "render-metrics",
    payload: {
        uiFps: renderer.currentFps,
        droppedTiles: renderer.droppedTiles,
    },
}));

// Asynchronous — the collector awaits it.
monitor.extensionStatsProviders.add(async () => {
    const cpu = await measureCpuUsage();
    return {
        type: "system-metrics",
        payload: {
            cpu,
            heapUsed: performance.memory?.usedJSHeapSize ?? 0,
        },
    };
});
```

| Property | Behaviour |
|---|---|
| Return shape | `{ type: string, payload?: object }` |
| Timing | Called during every stats collection cycle |
| Async | Promises are awaited |
| Errors | Logged, never propagated — a broken provider cannot stop monitoring |

They arrive on the sample as-is:

```javascript
monitor.on("sample-created", (sample) => {
    sample.extensionStats;
    // [
    //   { type: "render-metrics", payload: { uiFps: 58, droppedTiles: 0 } },
    //   { type: "system-metrics",  payload: { cpu: 45, heapUsed: 52428800 } },
    // ]
});
```

On the server side these surface as `client-extension-stats` events on the
[observer event bus](/docs/libraries/observer-js/event-bus/).

## Metadata

```javascript
monitor.addMetaData({ type: "LOCAL_SDP", payload: JSON.stringify(offer) });
monitor.addEvent({ type: "RECORDING_STARTED", timestamp: Date.now() });
```

Known metadata types (`MEDIA_DEVICE`, `MEDIA_CONSTRAINT`, `USER_MEDIA_ERROR`, `LOCAL_SDP`,
`BROWSER`, `ENGINE`, `PLATFORM`, `OPERATION_SYSTEM`, …) are recognised and interpreted by
`observer-js`; anything else passes through untouched.

## Binary compression

JSON samples are readable but large. Two companion packages encode a `ClientSample` into the
compact protobuf representation defined by the [schema](/docs/schema/) and decode it again.

```bash
# Client side
npm install @observertc/samples-encoder

# Server side
npm install @observertc/samples-decoder
```

{{< tabs "codec" >}}
{{< tab "Encode (browser)" >}}
```javascript
import { ClientSampleEncoder } from "@observertc/samples-encoder";

// One encoder per client, created once and kept for the life of the stream.
const encoder = new ClientSampleEncoder(clientId);

monitor.on("sample-created", async (sample) => {
    await fetch(`/api/samples/${clientId}`, {
        method: "POST",
        headers: { "Content-Type": "application/octet-stream" },
        body: encoder.encodeToBytes(sample),
    });
});
```
{{< /tab >}}
{{< tab "Decode (server)" >}}
```javascript
import { ClientSampleDecoder } from "@observertc/samples-decoder";

// One decoder per client stream, fed the samples in order.
const decoders = new Map();

app.post("/api/samples/:clientId", raw, (req, res) => {
    let decoder = decoders.get(req.params.clientId);
    if (!decoder) decoders.set(req.params.clientId, (decoder = new ClientSampleDecoder()));

    const sample = decoder.decodeFromBytes(req.body);
    if (!sample) return res.sendStatus(400);

    observer.accept(sample);
    res.sendStatus(202);
});
```
{{< /tab >}}
{{< /tabs >}}

Encoding is transport-agnostic — WebSocket, `fetch`, `sendBeacon`, or a message queue all work.
See [sample-encoder-js](/docs/libraries/sample-encoder-js/) and
[sample-decoder-js](/docs/libraries/sample-decoder-js/).

{{< callout context="caution" title="Both sides are stateful, and versions must match" icon="alert-triangle" >}}
The encoder writes unchanging values — `clientId`, `callId`, peer connection and track ids — **once**
and omits them afterwards. That is where most of the saving comes from, and it means: one encoder
per client, one decoder per client stream, samples delivered in order. A restarted or shared
decoder does not throw; it produces samples with missing ids.

Protobuf field numbers are also derived from field order, so keep both packages on the same schema
version — they are released in lockstep. See [schema versions](/docs/schema/versions/).
{{< /callout >}}

## Reducing telemetry volume

In rough order of impact:

1. **Increase `samplingPeriodInMs`.** Ten seconds instead of four cuts upload volume by more than
   half with no loss of issue fidelity.
2. **Use the binary encoder.** Same information, far fewer bytes.
3. **Turn off detectors you do not act on** with `null` in the
   [configuration](../configuration/) — fewer issues, less work per tick.
4. **Filter in an adapter.** If you never analyse certificates or codecs server-side, drop them
   before the sample is built.
5. **Sample conditionally.** Switch to manual sampling and only upload when something interesting
   is happening — for example, always upload while any issue is active, and at a reduced rate
   otherwise:

```javascript
setInterval(() => {
    const interesting = monitor.getActiveIssuesByType().length > 0;
    if (!interesting && Math.random() > 0.2) return;   // 20% baseline sampling
    const sample = monitor.createSample();
    if (sample) transport.send(sample);
}, 5000);
```
