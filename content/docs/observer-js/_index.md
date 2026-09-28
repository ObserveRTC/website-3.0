---
title: "Observer"
description: "Turn client samples into live calls, participants, tracks and server analysis."
lead: "Turn client samples into live calls, participants, tracks and server analysis."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 30
toc: true
---

`@observertc/observer-js` **1.0.0** consumes `ClientSample` records. It maintains live entities, mirrors client issue lifecycles, and supports cross-client analysis, SFU correlation and persistence hooks.

Your application supplies transport, authentication, validation and storage. A new Observer has **no detectors registered**.

{{< card-grid >}}
{{< link-card title="Ingestion & lifecycle" description="Understand accept(), timing and automatic cleanup." href="/docs/observer-js/ingestion/" >}}
{{< link-card title="Entities & events" description="Navigate server state and the central event bus." href="/docs/observer-js/entities/" >}}
{{< link-card title="Server detectors" description="Explicitly register cross-client and cross-call analysis." href="/docs/observer-js/detectors/" >}}
{{< link-card title="SFU integration" description="Join publishers and subscribers using signaling identifiers." href="/docs/observer-js/sfu/" >}}
{{< link-card title="Summaries & sinks" description="Persist samples and summarize a completed call." href="/docs/observer-js/call-summaries/" >}}
{{< link-card title="Known differences" description="Reproduced behavior to account for during integration." href="/docs/reference/known-differences/" >}}
{{< /card-grid >}}
