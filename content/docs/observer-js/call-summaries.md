---
slug: "call-summaries"
title: "Call summaries"
description: "Enable a bounded final record for each call."
lead: "Enable a bounded final record for each call."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 80
toc: true
---

Call summaries opt into sections (`clients`, `issues`, `turnServers`, `scores`) and optional event enrichers. Empty include defaults to no built-in sections, not “all.” Caps default to 500 issues/10000 client IDs; truncation is recorded. Collector bus subscriptions span the Observer rather than multiplying per call; final summary emits during call close. Client logger is supplied in ClientMonitor config; server uses its common logger API (`setObserverLogger` etc.). [observer-js/src/summaries/CallSummary.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/summaries/CallSummary.ts), [observer-js/src/summaries/CallSummaryCollector.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/summaries/CallSummaryCollector.ts), [observer-js/src/common/logger.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/common/logger.ts), [observer-js/docs/logging.md](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/docs/logging.md).

## Configure before the call begins

Summaries are disabled when `callSummary` is absent or null. Supplying an object enables collection; its default inclusion list is empty. Choose the sections you need instead of assuming every detail will be captured.

Default caps are 500 issue entries and 10,000 client IDs. Samples and summaries serve different purposes: use a sink for full sample history and a summary for call-level reporting.

[Configuration and lifecycle: Observer](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts) · [Call implementation](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedCall.ts)
