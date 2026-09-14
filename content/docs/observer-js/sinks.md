---
title: "Sinks & injection"
description: "Persisting samples per client, injecting application data, and logging"
lead: "Every accepted sample can be archived, and anything your application knows can be merged into the stream"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 370
toc: true
---

## Sinks

A **sink** receives the samples a client accepts — for archival, streaming, or later offline replay.
Each `ObservedClient` gets its **own** sink, produced by the `ObserverConfig.createClientSink`
factory when the client is created (return `undefined` for no sink). The client pushes every accepted
sample to its sink and `end()`s it on close.

```typescript
import { Observer, createJsonlFileSinkFactory } from '@observertc/observer-js';

const observer = new Observer({
    // one ./stats/<callId>__<clientId>.jsonl per client
    createClientSink: createJsonlFileSinkFactory({ directory: './stats' }),
});

observer.on('client-sink-created', ({ observedClient, sink }) => {
    sink.on('close', () => {
        // the file is fully flushed and its fd closed — ready to upload, move, etc.
    });
});
```

### Built-in sinks

| Export | Signature | Notes |
|---|---|---|
| `createJsonlFileSinkFactory` | `({ directory, flags?, getFileName?, serializeSample? })` | Per-client JSONL files; path defaults to `${callId}__${clientId}.jsonl` under `directory`, **which must exist** |
| `createJsonlFileSink` | `({ path, flags?, serializeSample? })` | A single JSONL file; wraps `fs.WriteStream` and re-emits its `close` / `finish` / `drain` / `error` |
| `JsonlFileSink` | `class extends ClientSampleSink` | The underlying class; exposes `readonly path` |
| `createInMemorySink` / `InMemorySink` | `(samples?: ClientSample[])` | Collects the accepted **sample objects** into `.samples`; emits `close` on `end()` |

`serializeSample?: (sample: ClientSample) => string` overrides the default `JSON.stringify` for the
JSONL sinks — to redact or reshape before writing.

### The `ClientSampleSink` base class

An **abstract base class** (a typed `EventEmitter`). You create a sink by **subclassing it** and
implementing `write` and `end`. It is **object-mode**: `write` receives the `ClientSample` *object*,
so each sink decides how — or whether — to serialize it.

```typescript
abstract class ClientSampleSink /* extends EventEmitter */ {
    abstract write(sample: ClientSample): boolean;   // accept one sample; `false` = backpressure
    abstract end(): void;                            // flush; emit `close` when the destination is ready

    on(event: 'close' | 'finish' | 'drain', listener: () => void): this;
    on(event: 'error', listener: (err: Error) => void): this;
}
```

| Event | Meaning |
|---|---|
| `close` | The destination is fully written and closed — "ready" |
| `error` | The destination failed |
| `finish` | `end()` was processed and queued data flushed (before `close`) |
| `drain` | The buffer drained after backpressure; safe to write more |

The library calls `write(sample)` **synchronously** per accepted sample (it is not awaited), `end()`s
the sink when the client closes, and attaches an `error` listener so a failing sink cannot crash the
process — it also catches throws from `write` / `end`. **Because `write` is not awaited in the
`accept()` hot path, backpressure and batching are the sink's concern.**

### Reading sink-specific information

The bus hands you the sink as the base `ClientSampleSink`. To read something specific to a sink type
— for a file sink, where it was written — narrow with `instanceof`:

```typescript
import { JsonlFileSink } from '@observertc/observer-js';

observer.on('client-sink-created', ({ sink }) => {
    if (sink instanceof JsonlFileSink) {
        const { path } = sink;
        sink.once('close', () => uploadFile(path));   // close = flushed & fd closed → ready
    }
});
```

Each concrete sink exposes whatever it wants as `public readonly` fields, and consumers narrow to
read them. Your own sinks do the same.

### Writing your own

```typescript
import { ClientSampleSink, ClientSample, ClientSampleSinkFactory } from '@observertc/observer-js';

class HttpSink extends ClientSampleSink {
    private buffer: ClientSample[] = [];

    constructor(private readonly url: string) { super(); }

    write(sample: ClientSample): boolean {
        this.buffer.push(sample);              // batch; decide your own backpressure
        return true;
    }

    end(): void {
        fetch(this.url, { method: 'POST', body: JSON.stringify(this.buffer) })
            .then(() => this.emit('close'))    // signal "destination ready"
            .catch((err) => this.emit('error', err));
    }
}

const createClientSink: ClientSampleSinkFactory = ({ clientId, observedCall }) =>
    new HttpSink(`https://stats.example.com/${observedCall.callId}/${clientId}`);

const observer = new Observer({ createClientSink });
```

`observedClient.sink?` exposes the created sink, and `client-sink-created` delivers it on the bus
with full ancestry.

## Injecting data into a client

Sometimes the application holds data that belongs on a client's record but is not part of the
client-reported sample — a room id or display name, an application-level event ("recording started"),
a server-detected issue, an extension stat, or a device item.

| Method | Adds to the sample's | Surfaces as |
|---|---|---|
| `injectAttachment(attachments)` | `attachments` (merged via `Object.assign`) | `observedClient.attachments` |
| `injectEvent(event)` | `clientEvents` | `client-event`, plus any state the event drives |
| `injectIssue(issue)` | `clientIssues` | `client-issue` |
| `injectMetaData(meta)` | `clientMetaItems` | `client-metadata` |
| `injectExtensionStat(stat)` | `extensionStats` | `client-extension-stats` |

Injected data **updates the live model *and* is persisted to the client's sink**, exactly like
sampled data — the sink write happens at the end of `accept()`, after the merge, so it always
receives the injection-merged sample.

### When it lands

Injection is timing-aware, so nothing is dropped regardless of *when* you call it:

- **During a sample's processing** — e.g. from inside a `client-updated` or `client-event` handler,
  which run within `accept()` — the data is applied to the **current** sample immediately.
- **Between samples** — it is buffered and merged into the **next** `accept()`'s sample.
- **On `close()` with pending injections and no further sample** — the buffer is flushed as a final
  synthetic sample before the sink is ended, so a last-moment injection is never lost.

```typescript
// Enrich at creation from your app's knowledge of the participant. Injecting in `client-added`
// (which runs just before the first accept) lands on the first sample.
observer.on('client-added', ({ observedClient }) => {
    observedClient.injectAttachment({ roomId: lookupRoomId(observedClient.clientId) });
});

// Application-level signals at any time:
const client = observer.getObservedCall(callId)?.getObservedClient(clientId);
client?.injectEvent({ type: 'RECORDING_STARTED', timestamp: Date.now() });
client?.injectIssue({ type: 'app-kicked-participant', timestamp: Date.now() });
```

`attachments` are latest-wins, like sampled attachments: injecting a key overwrites its previous
value. **`appData` is unaffected** — injections flow into the sample and telemetry, not the
app-owned bag.

There is also a **direct add** API that processes immediately rather than merging into the next
sample: `addIssue(…)`, `addMetadata(…)`, `addExtensionStats(…)`.

## Logging

`observer-js` logs through a single swappable sink. Out of the box it writes `debug` and above to
`console` — verbose, so install your own for production.

```typescript
import { setObserverLogger, type ObserverLogger } from '@observertc/observer-js';

setObserverLogger({
    trace: (m, ...a) => myLogger.trace(`[${m}]`, ...a),
    debug: (m, ...a) => myLogger.debug(`[${m}]`, ...a),
    info:  (m, ...a) => myLogger.info(`[${m}]`, ...a),
    warn:  (m, ...a) => myLogger.warn(`[${m}]`, ...a),
    error: (m, ...a) => myLogger.error(`[${m}]`, ...a),
});
```

The first argument is the module name, so per-module routing and filtering are one `switch` away.
`createLogger(moduleName)` is exported for your own modules.
