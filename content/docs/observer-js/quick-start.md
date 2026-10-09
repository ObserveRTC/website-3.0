---
slug: "quick-start"
title: "Quick start"
description: "Quick start for engineers integrating ObserveRTC."
draft: false
outputs: ["HTML", "Markdown"]
weight: 5
toc: true
---

Observer runs in your backend. It receives samples from Client Monitor and keeps an up-to-date view of calls, participants, tracks, and their issues. Add it when you need to compare participants or keep call-level diagnostics.

## Install

```bash
npm install @observertc/observer-js
```

## Create an Observer

```javascript
import { Observer } from '@observertc/observer-js';

const observer = new Observer();

observer.on('call-added', ({ observedCall }) => {
  console.log('Call:', observedCall.callId);
});
observer.on('client-issue', ({ observedClient, issue }) => {
  console.log('Client:', observedClient.clientId, issue.type);
});
```

## Accept a sample

```javascript
// Inside your authenticated and validated ingestion handler:
observer.accept(sample);
```

`sample` is a decoded `ClientSample` with a nonempty `callId` and `clientId`. Observer creates the corresponding call and client when it first sees their identifiers, then updates them as more samples arrive.

Your application supplies the endpoint and transport. Authenticate the sender, check that it may report for those identifiers, and validate the payload before accepting it. `accept()` is synchronous and does not decode JSON/Protobuf codec streams for you.

## Add analysis and history

A new Observer has no server detectors registered. Choose [server detectors](/docs/observer-js/detectors/) for cross-participant analysis. Add [sinks](/docs/observer-js/sinks/) for sample history or [call summaries](/docs/observer-js/call-summaries/) for a record of a completed call; live entities alone are not historical storage.

Call `observer.close()` during service shutdown. Continue with [backend integration](/docs/observer-js/recipes/) and [configuration](/docs/observer-js/configuration/).
