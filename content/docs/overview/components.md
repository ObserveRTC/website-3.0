---
slug: "components"
title: "Components and responsibilities"
description: "Choose the library that owns the work you need to do."
lead: "Choose the library that owns the work you need to do."
draft: false
outputs: ["HTML", "Markdown"]
weight: 30
toc: true
---

Start with Client Monitor to inspect an endpoint. Add Observer when your backend needs to combine reports from participants. Schemas define their shared sample contract, and codecs optionally reduce the cost of transporting those samples.

| Component | Responsibility | What your application provides |
|---|---|---|
| [Client Monitor](/docs/client-monitor-js/) | Read browser statistics, derive metrics, evaluate endpoint conditions, and create samples. | Existing connections, application context, and any sample transport. |
| [Observer](/docs/observer-js/) | Maintain live call/client state, mirror reported issues, and run registered server analysis. | Authenticated ingestion, validation, identity mapping, and storage. |
| [Schemas](/docs/schema/) | Define the records and types carried by `ClientSample`. | A compatible producer/consumer contract. |
| [Codecs](/docs/codecs/) | Encode and decode changes between successive samples. | Ordered delivery and a separate stateful stream per client. |

## Supporting projects

The [Stats Dashboard](https://github.com/ObserveRTC/stats-dashboard) and [STUNner demo](https://github.com/ObserveRTC/observertc-stunner-demo) provide examples and tools around the libraries. They are not required to embed Client Monitor or Observer. Read their repositories for deployment requirements.

## Keep telemetry separate from media

The monitoring pipeline transports statistics and application records, not audio/video. Your application's signaling and media infrastructure continue to establish and carry the call. See [Architecture](/docs/overview/architecture/) for the integration boundaries.
