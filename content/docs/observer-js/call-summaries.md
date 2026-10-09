---
slug: "call-summaries"
title: "Call summaries"
description: "Enable a bounded final record for each call."
lead: "Enable a bounded final record for each call."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "Markdown"]
weight: 90
toc: true
---

A call summary is a compact record of a completed call. Use it for support and reporting when you need the important participants, issues, and outcomes without reading every raw sample. Enable it before calls start so it observes their full lifecycle.

Call summaries capture selected call-level results when a call closes. Persist full samples through a [sink](/docs/observer-js/sinks/) when you need detailed history.

## Configure before the call begins

Summaries are disabled when `callSummary` is absent or null. Supplying an object enables collection; its default inclusion list is empty. Choose the sections you need instead of assuming every detail will be captured.

Default caps are 500 issue entries and 10,000 client IDs. Samples and summaries serve different purposes: use a sink for full sample history and a summary for call-level reporting.

{{< details "Source references" >}}

- [Configuration and lifecycle: Observer](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts)
- [Call implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedCall.ts)

{{< /details >}}

## Save a completed-call record

```javascript
const observer = new Observer({
  callSummary: {
    include: ['clients', 'issues', 'scores'],
  },
});
observer.on('call-summary', ({ summary }) => {
  archive(summary);
});
```

`archive` is your application’s persistence function. The summary is emitted when the call closes, including closure after its empty-call grace period. Decide how to store it and how to handle persistence failures in your service.

## Sections and collection

Choose from `clients`, `issues`, `turnServers` and `scores`, with optional event enrichers. Truncation is recorded when configured caps are reached.

Collector subscriptions span the Observer. The final summary emits during call close.

Sources: [CallSummary](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/summaries/CallSummary.ts), [CallSummaryCollector](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/summaries/CallSummaryCollector.ts).
