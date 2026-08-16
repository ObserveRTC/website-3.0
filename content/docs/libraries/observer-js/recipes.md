---
title: "Recipes"
slug: "recipes"
description: "End-to-end integration patterns for observer-js"
lead: "Ingestion endpoints, alerting, metrics export, archival and post-call reporting"
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 328
toc: true
---

## A complete SFU observer

Everything wired: ingestion, correlation, detection, validation, persistence and alerting.

```typescript
import {
    Observer,
    createDefaultMediasoupRemoteTrackResolverFactory,
    createJsonlFileSinkFactory,
    setObserverLogger,
} from "@observertc/observer-js";

setObserverLogger({
    trace: () => {},
    debug: () => {},
    info:  (m, ...a) => log.info({ module: m }, ...a),
    warn:  (m, ...a) => log.warn({ module: m }, ...a),
    error: (m, ...a) => log.error({ module: m }, ...a),
});

const observer = new Observer({
    // Auto-teardown so crashed participants cannot poison cross-client detection.
    closeClientIfIdleForMs: 60_000,
    closeCallIfEmptyForMs: 20_000,

    // Publisher ↔ subscriber links — required by four of the detectors below.
    createRemoteTrackResolver: createDefaultMediasoupRemoteTrackResolverFactory(),

    // Archive every sample, one JSONL file per client.
    createClientSink: createJsonlFileSinkFactory({ directory: "./stats" }),

    // Enrich entities at creation.
    createCallAppData:   ({ callId })                 => ({ callId, startedAt: Date.now(), region: REGION }),
    createClientAppData: ({ clientId, observedCall }) => ({ clientId, region: observedCall.appData.region }),
});

// ── Detection ──────────────────────────────────────────────────────────────
observer
    .addCallDetector("call-concurrent-issue-detector", {
        issueTypes: ["congestion", "cpulimitation", "ice-disconnected", "freezed-video-track"],
    })
    .addCallDetector("issue-fan-out-detector", {
        issueTypes: ["freezed-video-track", "dry-inbound-track"],
    })
    .addCallDetector("publisher-fault-corroboration-detector", {
        publisherIssueTypes: ["encoder-bottleneck", "cpulimitation"],
        receiverIssueTypes:  ["freezed-video-track"],
    })
    .addCallDetector("track-delivery-mismatch-detector", {
        dryInboundIssueType: "dry-inbound-track",
        dryOutboundIssueType: "dry-outbound-track",
        minReceivers: 2,
    })
    .addCallDetector("unconsumed-track-detector", {
        minUnconsumedDurationInMs: 30_000,
    })
    .addObserverDetector("observer-concurrent-issue-detector", {
        issueTypes: ["congestion", "ice-disconnected", "ice-connection-failed"],
        minAffectedCalls: 3,
    })
    .addObserverDetector("client-population-issue-detector", {
        issueTypes: ["cpulimitation"],
        groupBy: "browser",
    })
    .addObserverDetector("turn-server-health-detector")
    .addObserverDetector("turn-server-outage-detector", { minClientsAtPeak: 10 });

// ── Structural validation, once at start-up ────────────────────────────────
observer
    .addValidator("remote-track-resolver")
    .addValidator("simulcast-receivers", { minChecks: 5 });

// ── Ingestion ──────────────────────────────────────────────────────────────
observer.addAcceptMiddleware(({ sample }, next) => {
    sample.callId   ??= sample.attachments?.roomId as string;
    sample.clientId ??= sample.attachments?.peerId as string;
    next({ sample });
});

// ── Reaction ───────────────────────────────────────────────────────────────
observer.on("call-issue",     ({ observedCall, issue }) => alerting.callIssue(observedCall.callId, issue));
observer.on("observer-issue", ({ issue })               => alerting.page(issue));

observer.on("client-issue-resolved", ({ observedCall, observedClient, resolvedIssue }) => {
    analytics.track("quality_episode", {
        callId: observedCall.callId,
        clientId: observedClient.clientId,
        type: resolvedIssue.type,
        durationInMs: resolvedIssue.durationInMs,
        resolvedBy: resolvedIssue.resolvedBy,
    });
});

observer.on("validation-ready", ({ validator, report }) => {
    if (report.verdict === "no-links-resolved") {
        alerting.page("remote track resolver is not linking anything", { validator, report });
    }
});

observer.on("sample-rejected", ({ reason }) => metrics.increment("observer.rejected", { reason }));

process.on("SIGTERM", () => observer.close());
```

## HTTP ingestion

```typescript
import express from "express";
import { ClientSampleDecoder } from "@observertc/samples-decoder";

const app = express();

// The decoder is stateful and per-client: it reconstructs ids the encoder elided.
const decoders = new Map<string, ClientSampleDecoder>();
const decoderFor = (clientId: string) => {
    let decoder = decoders.get(clientId);
    if (!decoder) decoders.set(clientId, (decoder = new ClientSampleDecoder()));
    return decoder;
};
observer.on("client-closed", ({ observedClient }) => decoders.delete(observedClient.clientId));

// JSON samples.
app.post("/api/samples", express.json({ limit: "4mb" }), (req, res) => {
    observer.accept(req.body, {
        receivedAt: Date.now(),
        ingestNode: process.env.HOSTNAME,
        remoteIp: req.ip,
    });
    res.sendStatus(202);
});

// Binary (protobuf) samples — smaller on the wire. Route by clientId so the right
// decoder sees the whole stream, in order.
app.post("/api/samples/bin/:clientId", express.raw({ type: "application/octet-stream", limit: "2mb" }), (req, res) => {
    const sample = decoderFor(req.params.clientId).decodeFromBytes(req.body);
    if (!sample) return res.sendStatus(400);

    observer.accept(sample, { receivedAt: Date.now() });
    res.sendStatus(202);
});

// Read the live model.
app.get("/api/calls/:callId", (req, res) => {
    const call = observer.getObservedCall(req.params.callId);
    if (!call) return res.sendStatus(404);

    res.json({
        callId: call.callId,
        numberOfClients: call.numberOfClients,
        maxNumberOfClients: call.maxNumberOfClients,
        score: call.score,
        startedAt: call.startedAt,
        clients: [...call.observedClients.values()].map((c) => ({
            clientId: c.clientId,
            score: c.score,
            rttMs: c.currentAvgRttInMs,
            usingTURN: c.usingTURN,
            browser: c.browser,
            openIssues: [...c.activeIssues.values()].map((i) => i.type),
        })),
    });
});
```

## WebSocket ingestion

```typescript
import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8080 });

wss.on("connection", (ws, req) => {
    const connectionId = crypto.randomUUID();

    ws.on("message", (data) => {
        let sample;
        try {
            sample = JSON.parse(data.toString());
        } catch {
            return;   // ignore garbage; accept() would reject it anyway
        }
        observer.accept(sample, { connectionId });
    });
});
```

## Prometheus-style metrics export

One event per client per tick keeps the export cost bounded — see
[choosing a subscription strategy](../event-bus/#choosing-a-subscription-strategy).

```typescript
observer.on("client-updated", ({ observedCall, observedClient }) => {
    const labels = { call: observedCall.callId, client: observedClient.clientId };

    gauges.clientScore.set(labels, observedClient.score ?? 0);
    gauges.rtt.set(labels, observedClient.currentAvgRttInMs ?? 0);
    gauges.sendingVideo.set(labels, observedClient.sendingVideoBitrate);
    gauges.receivingVideo.set(labels, observedClient.receivingVideoBitrate);
    gauges.usingTurn.set(labels, observedClient.usingTURN ? 1 : 0);
    gauges.openIssues.set(labels, observedClient.activeIssues.size);
});

// Fleet-level, on the observer tick.
observer.on("observer-updated", () => {
    gauges.calls.set({}, observer.numberOfCalls);
    gauges.clients.set({}, observer.numberOfClients);
    gauges.clientsUsingTurn.set({}, observer.numberOfClientsUsingTurn);
    gauges.peerConnections.set({}, observer.numberOfPeerConnections);
});
```

## Post-call reporting

Build the report on `call-closed`, when every metric is final.

```typescript
import { CallHealthAggregator } from "@observertc/observer-js";

const episodes = new Map<string, unknown[]>();   // callId → resolved issues

observer.on("client-issue-resolved", ({ observedCall, observedClient, resolvedIssue }) => {
    const list = episodes.get(observedCall.callId) ?? [];
    list.push({
        clientId: observedClient.clientId,
        type: resolvedIssue.type,
        durationInMs: resolvedIssue.durationInMs,
    });
    episodes.set(observedCall.callId, list);
});

observer.on("call-closed", ({ observedCall }) => {
    const health = new CallHealthAggregator(observedCall).aggregate();

    reports.save({
        callId: observedCall.callId,
        startedAt: observedCall.startedAt,
        endedAt: observedCall.endedAt,
        maxParticipants: observedCall.maxNumberOfClients,
        score: observedCall.score,
        totalIssues: observedCall.numberOfIssues,
        clientsUsedTurn: [...observedCall.clientsUsedTurn],

        degradedRatio: health.degradedRatio,
        inboundDegradedRatio: health.inboundDegradedRatio,
        outboundDegradedRatio: health.outboundDegradedRatio,
        medianRttMs: health.rttInMs?.median,
        qualityLimitation: health.qualityLimitation,

        episodes: episodes.get(observedCall.callId) ?? [],
    });

    episodes.delete(observedCall.callId);
});
```

## Offline replay from archived samples

Because a sink writes the exact `ClientSample` objects that were accepted, an archived call can be
replayed through a fresh observer — with different detector configuration — to test a hypothesis
without touching production.

```typescript
import fs from "node:fs";
import readline from "node:readline";
import { Observer } from "@observertc/observer-js";

async function replay(files: string[], configure: (o: Observer) => void) {
    const observer = new Observer({ autoUpdateOnCallUpdate: true });
    configure(observer);

    const findings: unknown[] = [];
    observer.on("call-issue",     ({ issue }) => findings.push(issue));
    observer.on("observer-issue", ({ issue }) => findings.push(issue));

    // Interleave by timestamp so cross-client correlation behaves as it did live.
    const samples = [];
    for (const file of files) {
        const rl = readline.createInterface({ input: fs.createReadStream(file) });
        for await (const line of rl) samples.push(JSON.parse(line));
    }
    samples.sort((a, b) => a.timestamp - b.timestamp);

    for (const sample of samples) observer.accept(sample);

    observer.close();
    return findings;
}

// Would a lower minAffectedCalls have caught last Tuesday's incident?
const findings = await replay(archivedFiles, (o) => {
    o.addObserverDetector("observer-concurrent-issue-detector", {
        issueTypes: ["congestion"],
        minAffectedCalls: 2,
    });
});
```

{{< callout context="tip" title="This is the highest-value habit" icon="rocket" >}}
Detector thresholds are a judgement call, and tuning them against live traffic is slow and risky.
Archiving samples means every past incident becomes a test case you can replay against a new
configuration in seconds.
{{< /callout >}}

## Fixed-cadence aggregation

When you want a predictable tick rather than one driven by client sampling:

```typescript
const observer = new Observer({ autoUpdateOnCallUpdate: false });

const timer = setInterval(() => observer.update(), 5_000);

observer.on("observer-closed", () => clearInterval(timer));
```

Remember that observer-scoped detectors and validators run **only** inside `observer.update()`.

## Troubleshooting

{{< details "No events at all" >}}
- Is `accept()` being called? Subscribe to `sample-rejected` — missing `callId` / `clientId` is the
  most common cause, and an [accept middleware](../ingestion/#accept-middlewares) is the place to
  derive them.
- Is the observer closed? A closed observer rejects every sample with
  `reason: 'observer-closed'`.
{{< /details >}}

{{< details "Detectors never fire" >}}
- `new Observer()` has **zero** detectors. Register them with `addObserverDetector`,
  `addCallDetector` or `call.addDetector`.
- `addCallDetector` applies to calls created **after** the call — register at start-up, before
  ingestion.
- 🔗 detectors need a `RemoteTrackResolver`. Run the
  [`remote-track-resolver` validator](../validators/) to confirm the links exist.
- Issue-driven detectors need `client-monitor-js` ≥ 4.6.0, which sends keyed raise/resolve pairs.
{{< /details >}}

{{< details "Memory grows over time" >}}
- Set `closeClientIfIdleForMs` and `closeCallIfEmptyForMs`. Without them a dropped participant is
  never cleaned up.
- If you observe mediasoup routers, the router sample is cumulative and never evicted — snapshot
  and drop it yourself. See [memory and large meetings](../sfu/#memory-and-large-meetings).
- Your own maps keyed by `callId` need cleaning on `call-closed`.
{{< /details >}}

{{< details "High CPU on the event loop" >}}
The sub-stat `*-updated` events fire per stream per tick. Move to `client-updated` and walk the
tree, or subscribe only to the specific events you export. `yarn bench` in the repository measures
the detector pass for your shape.
{{< /details >}}

{{< details "Findings look wrong or too broad" >}}
Read the `conclusion` on the payload — `faultDomain` comes from the spread, not the issue type. If
a finding's `faultDomain` disagrees with your intuition, the
[conclusions section](../detectors/#conclusions) explains the reasoning, including the case where
`cpu-limitation` across many calls concludes `client-population` rather than `infrastructure`.
{{< /details >}}
