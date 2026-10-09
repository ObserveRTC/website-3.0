---
title: "Observer"
description: "Turn client samples into live calls, participants, tracks and server analysis."
lead: "Turn client samples into live calls, participants, tracks and server analysis."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 30
toc: true
---

`@observertc/observer-js` runs in your backend and receives samples from the browsers in a call. It brings those separate views together so you can inspect participants, follow their tracks, see active issues, and compare what a sender and its receivers experience. Your application chooses which analysis to run and which records to keep.

Your application supplies transport, authentication, validation and storage. A new Observer has **no detectors registered**.

The current npm release is **1.1.0**. Install without a version suffix to follow `latest`.

## Start here

Follow the [Observer quick start](/docs/observer-js/quick-start/), connect it to your ingestion handler, and choose a [configuration](/docs/observer-js/configuration/). The [source reference](/docs/reference/versions/) identifies the revisions used for implementation details.

{{< card-grid >}}
{{< link-card title="Ingestion & lifecycle" description="Understand accept(), timing and automatic cleanup." href="/docs/observer-js/ingestion/" >}}
{{< link-card title="Entities & events" description="Navigate server state and the central event bus." href="/docs/observer-js/entities/" >}}
{{< link-card title="Server detectors" description="Explicitly register cross-client and cross-call analysis." href="/docs/observer-js/detectors/" >}}
{{< link-card title="SFU integration" description="Join publishers and subscribers using signaling identifiers." href="/docs/observer-js/sfu/" >}}
{{< link-card title="Summaries & sinks" description="Persist samples and summarize a completed call." href="/docs/observer-js/call-summaries/" >}}
{{< link-card title="Known differences" description="Reproduced behavior to account for during integration." href="/docs/reference/known-differences/" >}}
{{< /card-grid >}}
