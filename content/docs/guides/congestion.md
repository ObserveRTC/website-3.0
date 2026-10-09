---
slug: "congestion"
title: "Investigate congestion"
description: "Compare sending and receiving evidence before choosing a network diagnosis."
lead: "Compare sending and receiving evidence before choosing a network diagnosis."
draft: false
outputs: ["HTML", "Markdown"]
weight: 30
toc: true
---

Use this guide when media quality drops alongside apparent network pressure. You need successive measurements for the affected client, its media direction, and the relevant detector findings.

## Confirm the affected direction

Outbound describes media this client sends; inbound describes what it receives. A low bitrate can also reflect a paused track or sender adaptation, so start with application intent and active media.

## Compare evidence

1. Identify the affected track and its connection/transport.
2. Compare bitrate, loss, round-trip time, and adaptation evidence over the affected interval.
3. Read uplink or downlink detector inputs and gates before interpreting the finding.
4. Check other participants when server-side correlation is available. Establish publisher/receiver links before comparing their tracks.
5. Check capture/encode/decode progress to distinguish network pressure from an endpoint pipeline bottleneck.

## Expected evidence and response

Look for related signals that change together, not a single low bitrate. Adaptation and loss can support a network-pressure hypothesis, but a congestion finding does not prove which link or device is responsible.

Choose your application's response after confirming the affected direction and comparing its baseline. If evidence is missing, report that limitation instead of assuming the network is healthy.

[Transport quality detectors](/docs/client-monitor-js/detectors-transport-quality/) · [Metrics](/docs/client-monitor-js/metrics/) · [Server detectors](/docs/observer-js/detectors/).
