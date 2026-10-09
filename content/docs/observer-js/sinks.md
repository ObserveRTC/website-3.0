---
slug: "sinks"
title: "Sample persistence and enrichment"
description: "Persist the accepted sample and enrich it with application data."
lead: "Persist the accepted sample and enrich it with application data."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "Markdown"]
weight: 80
toc: true
---

Live entities show the current state; a sink keeps the samples that produced it. Choose a sink when you need historical investigation, exports, or replay. Observer does not require a database: the destination is chosen by your application.

Sinks are per-client via `createClientSink`; built-ins are JSONL and in-memory. They persist the final injection-merged sample. During accept, `injectAttachment/Event/Issue/MetaData/ExtensionStat` affects the active sample immediately; between accepts it queues; close flushes pending data before sink teardown. A sink failure is logged, not a substitute for application persistence guarantees.

{{< details "Source references" >}}

- [observer-js/src/sinks/ClientSampleSink.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/sinks/ClientSampleSink.ts)
- [observer-js/src/sinks/JsonlFileSink.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/sinks/JsonlFileSink.ts)
- [observer-js/src/sinks/InMemorySink.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/sinks/InMemorySink.ts)
- [observer-js/src/ObservedClient.ts · _flushPendingInjections](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts#L923)

{{< /details >}}

## Logging

Supply a logger in Client Monitor configuration for browser logs. On the server, use `setObserverLogger` and the common logger API. Route these logs to your existing application logger.

[Observer logger source](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/common/logger.ts).
