---
title: "Recipes"
description: "End-to-end patterns: HTTP ingestion, alerting, dashboards, archival"
lead: "Copy-ready wiring for the shapes most deployments end up with"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 380
toc: true
---

## A complete SFU-side setup

```typescript
import {
    Observer,
    createDefaultMediasoupRemoteTrackResolverFactory,
    createJsonlFileSinkFactory,
} from '@observertc/observer-js';

const observer = new Observer({
    closeClientIfIdleForMs: 60_000,
    closeCallIfEmptyForMs: 20_000,

    // Publisher ↔ subscriber links, which four detectors and two validators need.
    createRemoteTrackResolver: createDefaultMediasoupRemoteTrackResolverFactory(),

    // Archive every accepted sample, one file per client.
    createClientSink: createJsonlFileSinkFactory({ directory: './stats' }),

    // The one record that outlives the call.
    callSummary: { include: ['clients', 'issues', 'turnServers', 'scores'] },

    // Bake the tenant into appData at birth, resolved once in a middleware.
    createCallAppData:   ({ callId, acceptCtx })      => ({ callId, tenant: acceptCtx?.tenant }),
    createClientAppData: ({ clientId, observedCall }) => ({ clientId, tenant: observedCall.appData.tenant }),
});

// Nothing is implicit — say what you want to watch.
observer
    .addObserverDetector('observer-concurrent-issue-detector', {
        issueTypes: ['congestion', 'ice-disconnected', 'ice-connection-failed'],
        minAffectedCalls: 3,
    })
    .addObserverDetector('client-population-issue-detector', {
        issueTypes: ['cpulimitation'],
        groupBy: 'browser',
    })
    .addObserverDetector('turn-server-health-detector')
    .addObserverDetector('turn-server-outage-detector', { minClientsAtPeak: 10 });

observer.addCallDetector('call-concurrent-issue-detector', {
    issueTypes: ['congestion', 'video-flow-disrupted', 'invented-speech'],
});
observer.addCallDetector('track-delivery-mismatch-detector', {});
observer.addCallDetector('publisher-fault-corroboration-detector', {
    publisherIssueTypes: ['encoder-bottleneck', 'video-capture-bottleneck'],
    receiverIssueTypes: ['video-flow-disrupted', 'dry-inbound-track'],
});

// Prove the resolver is actually wired — the failure mode is permanent silence.
observer.addValidator('remote-track-resolver');

process.on('SIGINT', () => observer.close());
```

## HTTP ingestion

```typescript
import express from 'express';

const app = express();
app.use(express.json({ limit: '2mb' }));

// Carry the clientId outside the payload so routing never depends on decoding it.
app.post('/api/samples/:clientId', (req, res) => {
    observer.accept(req.body, { receivedAt: Date.now(), tenant: req.header('x-tenant') });
    res.sendStatus(202);
});
```

With a binary codec, one decoder per connection and in order — see
[the protobuf codec](/docs/samples-protobuf-codec/):

```typescript
import { ClientSampleDecoder } from '@observertc/samples-protobuf-codec';

const decoders = new Map<string, ClientSampleDecoder>();

wss.on('connection', (ws, req) => {
    const clientId = clientIdFrom(req);
    const decoder = new ClientSampleDecoder();
    decoders.set(clientId, decoder);

    ws.on('message', (data: Buffer) => {
        const result = decoder.tryDecode(new Uint8Array(data));
        if (!result.ok) {
            metrics.increment('codec.decode_failed', { code: result.error.code });
            return;
        }
        observer.accept(result.value, { clientId });
    });

    ws.on('close', () => decoders.delete(clientId));
});
```

## Routing ids with a middleware

When the client does not know its own `callId` / `clientId`, derive them once before dispatch rather
than in every handler:

```typescript
import type { AcceptMiddleware } from '@observertc/observer-js';

const route: AcceptMiddleware = ({ sample, context }, next) => {
    sample.callId ??= sample.attachments?.roomId as string;
    sample.clientId ??= sample.attachments?.peerId as string;
    next({ sample, context });
};

const redact: AcceptMiddleware = ({ sample, context }, next) => {
    delete (sample.attachments as Record<string, unknown>)?.email;
    next({ sample, context });
};

observer.addAcceptMiddleware(route, redact);
observer.on('sample-rejected', ({ reason, sample }) => log.warn('dropped', reason, sample.clientId));
```

## Alerting on findings rather than symptoms

The conclusion is the interpretation step, so the person reading the page does not have to perform
it.

```typescript
observer.on('observer-issue', ({ issue }) => {
    if ((issue.conclusion?.confidence ?? 0) < 0.7) return;

    page({
        title: issue.type,
        summary: issue.conclusion?.summary,
        next: issue.conclusion?.recommendation,
        domain: issue.conclusion?.faultDomain,   // infrastructure | client-population | …
        evidence: issue.payload,
    });
});

observer.on('call-issue', ({ observedCall, issue }) => {
    ticket.attach(observedCall.callId, { type: issue.type, conclusion: issue.conclusion });
});
```

**Episode durations, not raises, are the useful analytics event:**

```typescript
observer.on('client-issue-resolved', ({ observedClient, resolvedIssue }) => {
    analytics.track('quality_episode', {
        clientId: observedClient.clientId,
        type: resolvedIssue.type,
        durationInMs: resolvedIssue.durationInMs,
        resolvedBy: resolvedIssue.resolvedBy,     // 'client' | 'timeout' | 'client-closed'
    });
});
```

## A live per-call dashboard feed

Read off the entities on `call-updated` rather than subscribing to every sub-stat event — the
`*-updated` events fire per stream, per sample.

```typescript
import { CallHealthAggregator } from '@observertc/observer-js';

observer.on('call-updated', ({ observedCall }) => {
    const health = new CallHealthAggregator(observedCall).aggregate();

    dashboard.push({
        callId: observedCall.callId,
        clients: observedCall.numberOfClients,
        score: observedCall.score,

        degradedRatio: health.degradedRatio,
        inboundDegradedRatio: health.inboundDegradedRatio,
        outboundDegradedRatio: health.outboundDegradedRatio,
        rttMedian: health.rttInMs?.median,
        qualityLimitation: health.qualityLimitation,

        openIssues: [...observedCall.activeIssuesRegistry.values()].map((i) => i.type),
        unconsumed: observedCall.unconsumedOutboundTracks.size,
    });
});
```

## Fixed-cadence aggregation

Updates are event-driven by default. To drive them yourself — for a fixed metrics interval, say —
opt out of both links in the chain:

```typescript
const observer = new Observer({ autoUpdateOnCallUpdate: false });

observer.on('call-added', ({ observedCall }) => {
    // per call, if you also want the call to update only on your tick
    // (ObservedCallSettings.autoUpdateOnClientUpdate: false)
});

setInterval(() => observer.update(), 5_000);
```

Remember that **observer-scoped detectors and validators run nowhere else** — if the observer never
updates, they never run.

## Archival and offline replay

Sinks write the samples; replaying them through a fresh observer is how you test a detector change
against real traffic.

```typescript
import { Observer } from '@observertc/observer-js';
import { createInterface } from 'node:readline';
import { createReadStream } from 'node:fs';

const replay = new Observer({ autoUpdateOnCallUpdate: true });
replay.addCallDetector('call-concurrent-issue-detector', { issueTypes: ['congestion'] });
replay.on('call-issue', ({ issue }) => console.log(issue.type, issue.conclusion?.summary));

for await (const line of createInterface({ input: createReadStream('./stats/room-1__alice.jsonl') })) {
    replay.accept(JSON.parse(line));
}

replay.close();
```

Because the library holds **no timer of its own**, a replay runs as fast as you feed it — the whole
model is driven by `accept()`.

## Archiving what outlived the call

```typescript
observer.on('call-summary', async ({ summary }) => {
    await warehouse.insert('call_summaries', {
        ...summary,
        // truncated is present only when something was really dropped
        trueIssueCount: summary.issues.length + (summary.truncated?.issues ?? 0),
    });
});
```

## Correlating with the SFU's own view

```typescript
const observedRouter = observer.createObservedMediasoupRouter({
    router,
    matchPeerConnectionByWebRtcTransportId: true,
});

observer.on('mediasoup-router-matched-with-peer-connection',
    ({ observedMediasoupRouter, observedCall, observedPeerConnection }) => {
        (observedPeerConnection.appData ??= {}).routerId = observedMediasoupRouter.id;
        store.linkRouterToCall(observedCall.callId, observedMediasoupRouter.id);
    },
);

// For large meetings, sample it yourself — nothing is evicted for you.
setInterval(() => persist(observedRouter.snapshot()), 10_000);
```

## Troubleshooting

{{< details "Every sample is rejected" >}}
`sample-rejected` names the reason. `missing-callId` / `missing-clientId` mean the client is not
setting them and no middleware derived them — see
[routing ids with a middleware](#routing-ids-with-a-middleware). `observer-closed` means something
closed the observer earlier than you thought.
{{< /details >}}

{{< details "A resolver-dependent detector never fires" >}}
Silence and "no links resolved" look identical from the outside. Start the validator:

```typescript
observer.addValidator('remote-track-resolver');
observer.on('validation-ready', ({ validator, report }) => console.log(validator, report.verdict));
```

`resolver.pendingTrackCounts` also reports tracks still waiting for a key; in a healthy setup it is
`{ inbound: 0, outbound: 0 }`.
{{< /details >}}

{{< details "An issue-driven detector never fires" >}}
- Every issue-driven detector requires an explicit, non-empty `issueTypes` — the default `[]` is
  subscribed to nothing and will never fire. There is no wildcard.
- The issue type strings must match what the client actually raises. `client-monitor-js` 4.9 renamed
  several: `audio-concealment` → `invented-speech`, `freezed-video-track` → `video-flow-disrupted`,
  `capture-track-ended` → `capture-source-lost`, `media-pipeline-stalled` → two types, and
  `keyframe-storm` is gone entirely.
- `client-monitor-js` **≥ 4.6.0** is required: without the raise + `<type>-resolved` lifecycle there
  is nothing to register.
{{< /details >}}

{{< details "One participant shows up as two clients" >}}
`closeClientIfIdleForMs` is too low for your sampling period: a paused participant is re-created as
a *new* client, restarting its detectors and splitting one person into two in any summary. The same
applies one level up — too low a `closeCallIfEmptyForMs` splits one meeting into several calls,
each emitting its own `call-summary`.
{{< /details >}}

{{< details "Inbound bitrates look 1000× too small" >}}
That was true before 1.0: `ObservedInboundRtp.bitrate` was bits per *millisecond*. It is bits per
second now — rescale any threshold or dashboard that was compensating. See
[what changed in 1.0](../migration-1-0/).
{{< /details >}}

{{< details "A codec change fires a fleet-wide degradation alert" >}}
It should not: `counterResetBoundary` suppresses every delta on a tick where `codecId`,
`encoder`/`decoderImplementation` or `scalabilityMode` changed. If you compute your own deltas from
the cumulative counters, apply the same guard — Chrome resets an SSRC's counters when the codec
switches.
{{< /details >}}
