---
title: "Schema & transport"
description: "ClientSample is the versioned contract between collection and analysis."
lead: "ClientSample is the versioned contract between collection and analysis."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
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
