---
title: "Sinks, injection & logging"
slug: "sinks"
description: "Persisting every sample, merging application data into a client, and routing logs"
lead: "Where samples go after they are processed, and how to add what only your application knows"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 327
toc: true
---

## Sinks

A **sink** receives the samples a client accepts — for archival, streaming, or later offline
replay. Each `ObservedClient` gets its **own** sink, produced by the
`ObserverConfig.createClientSink` factory when the client is created (return `undefined` for no
sink). The client pushes every accepted sample to its sink and `end()`s it on close.

```typescript
import { Observer, createJsonlFileSinkFactory } from "@observertc/observer-js";

const observer = new Observer({
    // one ./stats/<callId>__<clientId>.jsonl per client
    createClientSink: createJsonlFileSinkFactory({ directory: "./stats" }),
});

observer.on("client-sink-created", ({ observedClient, sink }) => {
    sink.on("close", () => {
        // the destination is fully flushed and closed — ready to upload, move, etc.
    });
});
```

### Built-in sinks

| Export | Signature | Notes |
|---|---|---|
| `createJsonlFileSinkFactory` | `({ directory, flags?, getFileName?, serializeSample? }) => ClientSampleSinkFactory` | Per-client JSONL files; path defaults to `${callId}__${clientId}.jsonl` under `directory`, which **must exist** |
| `createJsonlFileSink` | `({ path, flags?, serializeSample? }) => ClientSampleSink` | A single JSONL file wrapping `fs.WriteStream` |
| `JsonlFileSink` | `class extends ClientSampleSink` | Exposes `readonly path` |
| `createInMemorySink` / `InMemorySink` | `(samples?: ClientSample[]) => InMemorySink` | Collects sample objects into `.samples` |

`serializeSample?: (sample: ClientSample) => string` overrides the default `JSON.stringify` for the
JSONL sinks — use it to redact or reshape before writing.

### The `ClientSampleSink` base class

`ClientSampleSink` is an abstract, typed `EventEmitter`. You create a sink by subclassing it and
implementing `write` and `end`. It is **object-mode**: `write` receives the `ClientSample` *object*,
so each sink decides how, or whether, to serialise it.

```typescript
abstract class ClientSampleSink /* extends EventEmitter */ {
    abstract write(sample: ClientSample): boolean;   // false = backpressure
    abstract end(): void;                            // flush; emit 'close' when the destination is ready

    on(event: "close" | "finish" | "drain", listener: () => void): this;
    on(event: "error", listener: (err: Error) => void): this;
}
```

| Event | Meaning |
|---|---|
| `close` | The destination is fully written and closed — "ready" |
| `error` | The destination failed |
| `finish` | `end()` was processed and queued data flushed (before `close`) |
| `drain` | The buffer drained after backpressure; safe to write more |

{{< callout context="caution" title="write() is not awaited" icon="alert-triangle" >}}
The library calls `write(sample)` **synchronously** per accepted sample, on the `accept()` hot path,
and does not await it. **Backpressure and batching are the sink's concern.**

It attaches an `error` listener so a failing sink cannot crash the process, and catches throws from
`write` / `end` — but a sink that blocks will block ingestion.
{{< /callout >}}

### Reading sink-specific information

The bus hands you the base `ClientSampleSink`. Narrow with `instanceof` to read a concrete sink's
public fields:

```typescript
import { JsonlFileSink } from "@observertc/observer-js";

observer.on("client-sink-created", ({ observedClient, sink }) => {
    if (sink instanceof JsonlFileSink) {
        const { path } = sink;
        sink.once("close", () => uploadFile(path));   // close = flushed & fd closed
    }
});
```

Your own sinks follow the same pattern: expose whatever you want as `public readonly` and let
consumers narrow.

### Writing your own sink

```typescript
import { ClientSampleSink, ClientSample, ClientSampleSinkFactory } from "@observertc/observer-js";

class HttpSink extends ClientSampleSink {
    private buffer: ClientSample[] = [];

    constructor(private readonly url: string) { super(); }

    write(sample: ClientSample): boolean {
        this.buffer.push(sample);
        if (this.buffer.length >= 50) this.flush();
        return this.buffer.length < 500;   // signal backpressure past a bound
    }

    end(): void {
        this.flush()
            .then(() => this.emit("close"))
            .catch((err) => this.emit("error", err));
    }

    private async flush() {
        if (this.buffer.length === 0) return;
        const batch = this.buffer;
        this.buffer = [];
        await fetch(this.url, { method: "POST", body: JSON.stringify(batch) });
        this.emit("drain");
    }
}

const createClientSink: ClientSampleSinkFactory = ({ clientId, observedCall }) =>
    new HttpSink(`https://stats.example.com/${observedCall.callId}/${clientId}`);

const observer = new Observer({ createClientSink });
```

`ClientSampleSinkFactory` is
`(p: { clientId: string; observedCall: ObservedCall }) => ClientSampleSink | undefined` — so you can
return `undefined` to skip persistence for clients you do not care about:

```typescript
const createClientSink: ClientSampleSinkFactory = ({ observedCall }) =>
    observedCall.appData?.recordSamples
        ? createJsonlFileSink({ path: `./stats/${observedCall.callId}.jsonl` })
        : undefined;
```

---

## Injecting data into a client

Sometimes the application holds data that belongs on a client's record but is not part of the
client-reported sample — a room id or display name, an application-level event (*"recording
started"*), a server-detected issue, an extension stat, a device item.

`ObservedClient` exposes **injection** methods that merge such data into the client's sample stream,
so it updates the live model **and** is persisted to the sink exactly like sampled data.

| Method | Adds to the sample's | Surfaces as |
|---|---|---|
| `injectAttachment(attachments)` | `attachments` (merged via `Object.assign`) | `observedClient.attachments` |
| `injectEvent(event)` | `clientEvents` | `client-event`, plus any state the event drives |
| `injectIssue(issue)` | `clientIssues` | `client-issue` |
| `injectMetaData(meta)` | `clientMetaItems` | `client-metadata` |
| `injectExtensionStat(stat)` | `extensionStats` | `client-extension-stats` |

### When injected data lands

Injection is timing-aware so nothing is dropped, regardless of *when* you call it:

{{< steps >}}
{{< step >}}
**During a sample's processing** — e.g. from inside a `client-updated` or `client-event` handler,
which run within `accept()` — the data is applied to the **current** sample immediately: reflected
in entity state and written to the sink as part of that sample.
{{< /step >}}
{{< step >}}
**Between samples** — the data is buffered and merged into the **next** `accept()`'s sample.
{{< /step >}}
{{< step >}}
**On `close()` with pending injections and no further sample** — the buffer is flushed as a final
synthetic sample before the sink is ended, so a last-moment injection is never lost.
{{< /step >}}
{{< /steps >}}

In every case the sink receives the final, **injection-merged** sample — the sink write happens at
the end of `accept()`, after the merge.

### Example

```typescript
// Enrich at creation from your app's knowledge of the participant. Injecting in 'client-added'
// (which runs just before the first accept) lands on the first sample.
observer.on("client-added", ({ observedClient }) => {
    observedClient.injectAttachment({
        roomId: lookupRoomId(observedClient.clientId),
        displayName: lookupDisplayName(observedClient.clientId),
        plan: lookupPlan(observedClient.clientId),
    });
});

// Application-level signals at any time.
const client = observer.getObservedCall(callId)?.getObservedClient(clientId);
client?.injectEvent({ type: "RECORDING_STARTED", timestamp: Date.now() });
client?.injectIssue({ type: "app-kicked-participant", timestamp: Date.now() });
```

{{< callout context="note" title="attachments vs appData, again" icon="info-circle" >}}
`attachments` are latest-wins, like sampled attachments: injecting a key overwrites its previous
value. `appData` is unaffected — injections flow into the sample and the telemetry, not into the
app-owned `appData` bag. See [Ingestion](../ingestion/#context-vs-appdata).
{{< /callout >}}

### Direct-add variants

`addIssue`, `addMetadata` and `addExtensionStats` process immediately rather than queueing into
the next sample. Use the `inject*` family when you want the data to be part of the persisted
sample stream; use the `add*` family when you only want the live model and the event.

---

## Logging

`observer-js` logs through a single, swappable sink. Out of the box it writes `debug` and above to
`console` — verbose, so install your own for production.

```typescript
import { setObserverLogger, type ObserverLogger } from "@observertc/observer-js";

setObserverLogger({
    trace: (m, ...a) => myLogger.trace(`[${m}]`, ...a),
    debug: (m, ...a) => myLogger.debug(`[${m}]`, ...a),
    info:  (m, ...a) => myLogger.info(`[${m}]`, ...a),
    warn:  (m, ...a) => myLogger.warn(`[${m}]`, ...a),
    error: (m, ...a) => myLogger.error(`[${m}]`, ...a),
});
```

The first argument to each method is the module name, so you can route or filter per module.
`createLogger(moduleName)` is also exported for your own modules.

Silencing it completely:

```typescript
const noop = () => {};
setObserverLogger({ trace: noop, debug: noop, info: noop, warn: noop, error: noop });
```

Full recipes for pino, winston and console — level filtering, per-module routing — are in
[`docs/logging.md`](https://github.com/ObserveRTC/observer-js/blob/master/docs/logging.md).

{{< callout context="tip" title="Do not silence warn" icon="rocket" >}}
The library's error-handling philosophy is warn-don't-throw, so `warn` is where duplicate ids,
closed-parent creations and dropped samples show up. Silencing it removes your only signal that
something is being quietly discarded.
{{< /callout >}}
