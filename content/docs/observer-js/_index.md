---
title: "Observer"
description: "Turn client samples into live calls, participants, tracks and server analysis."
lead: "Turn client samples into live calls, participants, tracks and server analysis."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "RSS", "SITEMAP", "Markdown"]
landingTitle: "What is Observer?"
weight: 30
toc: true
---

Observer helps your backend understand a WebRTC call across its monitored endpoints. It accepts decoded `ClientSample` records, maintains live calls and clients, follows their media objects, and exposes events and registered analysis.

## Why use it?

A browser sees its own endpoint. Support and operations often need to compare participants: did several receivers lose the same publisher, are problems isolated to one client, or do similar issues appear across calls? Observer provides the live state and extension points for those investigations.

## What it provides

| Capability | Engineering use |
|---|---|
| Call and client state | Group samples by identity and inspect the current participants. |
| Track and transport entities | Follow media and network measurements within a client. |
| Client issue lifecycles | Maintain active keyed problems as raises and resolutions arrive. |
| Server detectors | Run explicitly registered analysis across clients or calls. |
| Track correlation | Relate publishers to receivers using configured signaling-ID resolvers. |
| Validators | Check a specific expectation over a limited lifecycle. |
| Sinks and summaries | Connect accepted samples and completed-call records to your storage. |

## How ingestion works

```text
Your authenticated handler → decode and validate → Observer.accept(sample)
                                                → find/create call and client
                                                → update entities and issues
                                                → events and registered analysis
                                                → configured sample sink
```

`accept()` is synchronous. A sample's `callId` and `clientId` identify the live state to update. Calls and clients can be created on first observation; idle clients and empty calls can be closed according to configuration. Live state is not a history database.

## Begin with a sample

```javascript
import { Observer } from '@observertc/observer-js';

const observer = new Observer();
observer.on('call-added', ({ observedCall }) => {
  console.log('Observed call:', observedCall.callId);
});

// Your handler has authenticated and validated this decoded sample.
observer.accept(sample);
```

The first sample for a new call creates its live call state and emits the call event. Subsequent samples update the existing client. Follow the [quick start](/docs/observer-js/quick-start/) to connect browser telemetry and [backend integration](/docs/observer-js/recipes/) to define the ingestion boundary.

## Integration decisions

Your service authenticates senders, validates payloads, checks allowed identities, and preserves per-client sample order. Decode optional codec streams before calling Observer. Do not rely on the library as an HTTP server or an authentication layer.

Choose [timeouts and factories](/docs/observer-js/configuration/) to match your sampling cadence and reconnect behavior. Register [server detectors](/docs/observer-js/detectors/) explicitly: a new Observer has none. Configure [SFU correlation](/docs/observer-js/sfu/) if analysis needs publisher/receiver relationships; browser IDs alone do not supply those links.

## State, timing, and persistence

[Calls, clients, and tracks](/docs/observer-js/entities/) explains ownership and identifier scopes. Client-level rate calculations in the documented baseline use server arrival intervals, so rapidly replaying historical samples is not equivalent to live cadence.

[Events](/docs/observer-js/event-bus/) provide ancestry for handlers. Use [sinks](/docs/observer-js/sinks/) for raw sample history and [call summaries](/docs/observer-js/call-summaries/) for selected completed-call results. Your application remains responsible for durability and persistence errors.

## Boundaries and cleanup

Observer does not rerun browser-side collection or endpoint detectors. Correlated evidence can narrow an investigation without proving an infrastructure fault. Missing resolver links and disabled analysis must not be interpreted as healthy results.

Call `observer.close()` during service shutdown. Make timeouts deliberate: closing a client too early can split a participant's history, while retaining abandoned clients too long affects counts and memory.

The current installation guidance uses **1.1.0** through `npm install @observertc/observer-js`. Detailed older references remain labeled in [version coverage](/docs/reference/versions/); [known implementation differences](/docs/reference/known-differences/) applies to its pinned baseline.

[Observer implementation reference](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts).
