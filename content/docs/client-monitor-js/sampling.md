---
title: "Sampling & transport"
description: "The collection loop, stats adapters, extension stats, and delta codecs"
lead: "Adapters normalise, monitors derive, detectors threshold — and every sampling period the whole state becomes a ClientSample"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 270
toc: true
---

## The collection loop

Every `collectingPeriodInMs`:

{{< steps >}}
{{< step >}}`getStats()` is called on every source.{{< /step >}}
{{< step >}}The raw stats array passes through the **stats adapters**, which normalise it toward the W3C spec.{{< /step >}}
{{< step >}}The monitor tree is updated and every derived value recomputed.{{< /step >}}
{{< step >}}Every attached detector's `update()` runs, each in its own try/catch.{{< /step >}}
{{< step >}}The score calculator runs.{{< /step >}}
{{< step >}}On a sampling boundary, a `ClientSample` is created and `'sample-created'` fires.{{< /step >}}
{{< /steps >}}

```typescript
const monitor = new ClientMonitor({ collectingPeriodInMs: 5000, samplingPeriodInMs: 5000 });

monitor.on('sample-created', ({ sample }) => transport.send(sample));
monitor.on('stats-collected', ({ durationOfCollectingStatsInMs, collectedStats }) => { /* … */ });
```

Both periods default to **5000** as of 4.9, and the sampling period should always be a multiple of
the collecting period — a sample can only be created on a collection, so anything else makes the
interval between samples drift, and the monitor warns about it.

**Adapters normalise, monitors derive, detectors threshold.** An adapter never invents a
measurement: where a browser reports nothing, the field stays absent and whatever reads it says so.

### Buffering samples until someone listens

Samples created before anything listens for `'sample-created'` are dropped — unless:

```typescript
new ClientMonitor({ bufferClientSamplesUntilSubscriber: true });
```

Then they are held and replayed in creation order to the first listener, so a monitor started before
the transport is ready does not lose the opening of the call. *(New in 4.9.)*

## Manual sampling

```typescript
const monitor = new ClientMonitor({
    collectingPeriodInMs: 5000,
    bufferingEventsForSamples: true,   // required, or events are dropped between samples
});

const sample = monitor.createSample();
```

{{< callout context="caution" title="Events need somewhere to go" icon="alert-triangle" >}}
`addEvent()` returns immediately when the monitor is not sampling and `bufferingEventsForSamples` is
`false` (the default). With `samplingPeriodInMs` unset or zero, **no client event is recorded at
all** — while the detectors' own monitor events still fire. That is easy to mistake for a detector
that is not working.
{{< /callout >}}

## What a sample contains

The sample schema version is **3.7.0** (`ClientMonitor.samplingSchemaVersion`).

```text
ClientSample
├─ timestamp, callId, clientId, score, scoreReasons, attachments
├─ peerConnections[]  (PeerConnectionSample)
│   └─ fifteen arrays mirroring the W3C getStats() dictionaries
├─ clientEvents[]      — things that happened
├─ clientIssues[]      — problem states, raised and resolved
├─ clientMetaItems[]   — devices, browser, OS, SDP
└─ extensionStats[]    — your own application metrics
```

Two things to know on the consuming side:

- **Payloads may nest** (schema 3.7.0). Client event, issue, meta and extension-stat payloads are
  records that may carry nested structures — records on the wire, never pre-serialised JSON strings.
  `PEER_CONNECTION_ICE_PATH_CHANGED` ships its `from` / `to` path evidence as structured records.
- **Static ICE transport metadata ships on change only.** `iceRole`, `dtlsRole`,
  `iceLocalUsernameFragment`, `tlsVersion`, `dtlsCipher`, `srtpCipher` and the certificate
  references appear in a transport's first sample and again only when a value changes. **Absence
  means *unchanged*, not unknown** — keep the last seen value per transport `id`, or set
  `sendIceTransportMetadataOnChangeOnly: false`.

`scoreReasons` is a `Record<string, number>` mapping each reason to how much it took off the score
(schema 3.6.0 changed it from a list of labels). Set `sendScoreReasonsToServer: false` to drop it
from the wire without changing any score.

See the [`ClientSample` reference](/docs/schema/clientsample/) for every field.

## Stats adapters

Adapters make the stats spec-conformant *before* any monitor sees them. Compensating for a browser
that omits or misreports a spec-required field belongs here and nowhere else — which is what keeps
the monitors and detectors honest about what was actually measured.

The built-ins are installed automatically once `fetchUserAgentData()` identifies the browser:
`ChromeStatsAdapter` (Chrome, Edge, Opera), `SafariStatsAdapter`, `FirefoxStatsAdapter`. A browser
outside the recognised set is `unknown` rather than guessed at.

An adapter is a **named object**, not a bare function:

```typescript
monitor.statsAdapters.add({
    name: 'strip-braces-from-track-identifiers',
    postAdapt: (stats) => stats.map((stat) => {
        if (stat.type === 'inbound-rtp' && stat.trackIdentifier) {
            stat.trackIdentifier = stat.trackIdentifier.replace(/[{}]/g, '');
        }
        return stat;
    }),
});
```

`preAdapt` runs before the built-ins, `postAdapt` after. Use `postAdapt` to filter records (a
mediasoup probator track, say) or to synthesize one the browser does not report.

## Extension stats

Application metrics that ride along in every sample — and, given an `id`, stay readable off the
monitor.

```typescript
// One-off
monitor.addExtensionStats({
    type: 'render-stats',
    id: 'tile-42',
    payload: { droppedFrames: 3, canvasFps: 24 },
});

// Every collection, no timer of your own. Providers may be async and are awaited
// as part of the collection, so their values land in the same tick as getStats().
monitor.extensionStatsProviders.add(async () => ({
    type: 'system-metrics',
    id: 'system',
    payload: { cpu: await readCpu() },
}));

monitor.getExtensionStatsPayload<{ cpu: number }>('system')?.cpu;
monitor.getExtensionStatsMonitor('system')?.timestamp;
```

- **The `id` is what makes it readable back.** Without one the payload still reaches the sample, but
  nothing is kept on the monitor.
- **Latest only** — re-reporting an id replaces its payload. This is a current-value store, not a
  history.
- **Lifetime** — a one-off value is dropped one collection after the id stops being reported; a
  provider-backed id stays readable for the whole call.
- **The type is asserted, not checked.** `getExtensionStatsPayload<T>(id)` casts to the shape you
  name; nothing validates it.
- **Errors in a provider are logged** and do not stop the collection.

## Cutting the size of what you upload

`ClientSample` objects compress extraordinarily well, because consecutive samples are nearly
identical — the same tracks, the same peer connections, counters that moved a little. Two codec
packages exploit exactly that by encoding **each sample as the delta from the previous one**.

| Package | Wire format | Take it when |
|---|---|---|
| [`@observertc/samples-protobuf-codec`](/docs/samples-protobuf-codec/) | Protobuf binary | Bytes on the wire are the binding constraint |
| [`@observertc/samples-json-codec`](/docs/samples-json-codec/) | JSON | The transport already compresses, and you would rather have zero dependencies (~2 KB gzipped) and a payload you can read in a log |

Both expose the same shape — a `ClientSampleEncoder`, a `ClientSampleDecoder`, and a
`createClientSampleCodec()` factory returning a matched pair — with the same delta semantics and the
same error codes, so you can swap one for the other without changing anything downstream.

{{< tabs "codec" >}}
{{< tab "Protobuf" >}}
```typescript
import { ClientSampleEncoder } from '@observertc/samples-protobuf-codec';

const encoder = new ClientSampleEncoder({ clientId });

monitor.on('sample-created', ({ sample }) => {
    websocket.send(encoder.encode(sample));   // Uint8Array
});
```
{{< /tab >}}
{{< tab "JSON" >}}
```typescript
import { ClientSampleEncoder } from '@observertc/samples-json-codec';

const encoder = new ClientSampleEncoder({ clientId });

monitor.on('sample-created', ({ sample }) => {
    websocket.send(encoder.encodeToJson(sample));   // string
});
```
{{< /tab >}}
{{< /tabs >}}

{{< callout context="caution" title="Delta encoding is stateful" icon="alert-triangle" >}}
1. **One encoder per client, one decoder per client stream.** Each holds the previous sample as its
   baseline.
2. **Messages must be decoded in the order they were encoded**, over an ordered, lossless transport
   — a WebSocket or an HTTP/2 stream is fine, a datagram transport is not.
3. **`reset()` is a keyframe.** Call it on both halves at the same point in the stream — after a
   reconnect, or whenever a new receiver needs to be able to join.

A decoder that has not seen enough of the stream raises `STREAM_DESYNC` rather than handing back an
object quietly missing its ids.
{{< /callout >}}

`sendScoreReasonsToServer: false`, `sendResolvedIssuesToServer: false` and a detector's
`includeIssueInSample = false` drop optional parts of a sample without changing any score or event.

## Where samples go next

[`observer-js`](/docs/observer-js/) accepts them directly:

```typescript
observer.accept(sample, { studioVersion: '1.2.3' });
```

It pairs the raise and `<type>-resolved` entries of each stateful issue, so the server sees the
**interval** a condition covered rather than a series of point-in-time reports.
