---
title: "Overview"
description: "Understand ObserveRTC and choose the parts your application needs."
lead: "Understand ObserveRTC and choose the parts your application needs."
draft: false
outputs: ["HTML", "RSS", "SITEMAP", "Markdown"]
weight: 10
toc: true
landingTitle: "What is ObserveRTC?"
---

ObserveRTC helps you investigate WebRTC calls using measurements from their endpoints. Client Monitor runs beside your browser connections; Observer combines endpoint reports in your backend. You can use the browser library alone or add server analysis when you need a call-wide view.

## What problem does it solve?

A connected peer connection does not tell you whether video is being captured, packets are arriving, frames are being decoded, or audio is playing continuously. ObserveRTC brings these signals together so you can locate a symptom and examine the evidence behind it.

It complements your existing media and signaling infrastructure. It does not route calls or replace an SFU, TURN server, or your application's backend.

## Choose your starting point

- To add monitoring, follow [Getting started](/docs/getting-started/).
- To understand the data flow, read [Architecture](/docs/overview/architecture/).
- To choose packages, read [Components and responsibilities](/docs/overview/components/).
- To investigate a symptom, use the [engineering guides](/docs/guides/).

[Client Monitor source](https://github.com/ObserveRTC/client-monitor-js/blob/4ae541eac3305d1cc779ff6dd703211e837a7f7b/src/ClientMonitor.ts) · [Observer source](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts).
