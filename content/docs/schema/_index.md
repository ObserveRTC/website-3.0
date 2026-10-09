---
title: "Schemas"
description: "ClientSample is the versioned contract between collection and analysis."
lead: "ClientSample is the versioned contract between collection and analysis."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "RSS", "SITEMAP", "Markdown"]
landingTitle: "What is ClientSample?"
weight: 40
toc: true
---

`ClientSample` carries timestamped WebRTC telemetry from Client Monitor to your backend. It includes peer connections, browser statistics, tracks, scores, events, issues and application attachments. Observer requires both `clientId` and `callId` for ingestion.

Start with the field reference when reading samples, or generation and compatibility when changing the contract. The optional JSON and protobuf codecs compress ordered sample streams.

{{< card-grid >}}
{{< link-card title="ClientSample fields" description="Browse the authoritative Avro records." href="/docs/schema/clientsample/" >}}
{{< link-card title="Generation & compatibility" description="Change definitions and regenerate dependent outputs." href="/docs/schema/general/" >}}
{{< link-card title="JSON codec" description="Stateful JSON sample transport." href="/docs/codecs/json/" >}}
{{< link-card title="Protobuf codec" description="Stateful binary sample transport." href="/docs/codecs/protobuf/" >}}
{{< /card-grid >}}

## Engineering boundaries

A sample is the explicit serialization contract, not a dump of every live monitor
property. Events, issues, and application attachments have defined locations; track
context and local DOM objects are not automatically transmitted. Check the field
reference when your backend needs a particular value.

Use [generation and compatibility](/docs/schema/general/) before changing types or
mixing producers and consumers. Historical [schema compatibility notes](/docs/schema/versions/)
remain available for stored streams; release announcements belong in Updates.

[Versioned schema source](https://github.com/ObserveRTC/schemas/tree/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources).
