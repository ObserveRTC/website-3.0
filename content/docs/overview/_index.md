---
title: "Overview"
description: "Overview of ObserveRTC"
lead: "Open-source WebRTC monitoring and analytics, from the browser to your backend"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 100
toc: true
---

ObserveRTC is a monitoring toolkit built specifically for WebRTC applications. This section covers
what it is, what it gives you, and how the pieces fit together.

## The three parts

### Monitors

A monitor lives next to the media stack and collects measurements from it. In the browser that is
[`client-monitor-js`](/docs/libraries/client-monitor-js/), which polls
`RTCPeerConnection.getStats()`, derives per-interval metrics, runs detectors, scores quality, and
periodically emits a [`ClientSample`](/docs/schema/clientsample/).

Crucially, a monitor **decides**. It does not just forward counters — it reports that congestion
started at this moment and ended fourteen seconds later, because only the endpoint has the
information needed to say that reliably.

### The observer

[`observer-js`](/docs/libraries/observer-js/) accepts those samples and maintains a live in-memory
model of every call, client, peer connection and stream. On top of it, it:

- derives and aggregates metrics at every level
- correlates a publisher's track with every subscriber of it
- runs cross-participant and cross-call detectors
- emits one typed event stream your application reacts to

It deliberately does **not** re-derive per-endpoint verdicts. Its job is the question a browser
cannot answer: who else is in this state, what do they share, and where does the fault begin?

### The schema

Samples are described by a versioned [schema](/docs/schema/) generated from Avro sources into
TypeScript, protobuf and documentation. It is what lets you replace any single component with your
own and keep the rest working.

## Where to go next

{{< card-grid >}}
{{< link-card title="Introduction" description="What ObserveRTC is, what it gives you, and who it is for." href="./introduction/" >}}
{{< link-card title="Architecture" description="The data flow, the client/server boundary, and deployment shapes." href="./architecture/" >}}
{{< /card-grid >}}
