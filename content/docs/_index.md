---
title: "Documentation"
description: "ObserveRTC Documentation - Complete guide to monitoring WebRTC applications"
lead: "Everything you need to instrument, collect and analyse WebRTC call quality"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 50
toc: true
seo:
  title: ""
  description: "ObserveRTC documentation: client-side monitoring, server-side analysis, and the shared WebRTC monitoring schema."
  canonical: ""
  robots: ""
---

ObserveRTC is an open-source toolkit for monitoring WebRTC applications: a browser library that
turns `getStats()` into actionable verdicts, a Node.js library that correlates those verdicts across
participants, two delta codecs that cut what you upload, and a versioned schema that ties them all
together.

## Start here

{{< card-grid >}}
{{< link-card title="Introduction" description="What ObserveRTC is, what it gives you, and who it is for." href="/docs/overview/introduction/" >}}
{{< link-card title="Architecture" description="How the pieces fit together, and where the client/server line is drawn." href="/docs/overview/architecture/" >}}
{{< /card-grid >}}

## The libraries

{{< card-grid >}}
{{< link-card
  title="Client Monitor"
  description="Browser-side monitoring: derived metrics, quality scores, and 46 detectors that raise and resolve issues with hysteresis. Current: 4.9.0."
  href="/docs/client-monitor-js/" >}}
{{< link-card
  title="Observer"
  description="Server-side analysis: a live model of every call plus cross-participant detection that answers what no single browser can. Current: 1.0.0."
  href="/docs/observer-js/" >}}
{{< /card-grid >}}

## The codecs

{{< card-grid >}}
{{< link-card title="Protobuf Codec" description="Smallest payload. Each message carries only what changed since the previous sample." href="/docs/samples-protobuf-codec/" >}}
{{< link-card title="JSON Codec" description="The same delta codec with zero dependencies, ~2 KB gzipped, and a payload you can read in a log." href="/docs/samples-json-codec/" >}}
{{< /card-grid >}}

## The schema

{{< card-grid >}}
{{< link-card title="Schema overview" description="One contract shared by every component, generated from Avro." href="/docs/schema/" >}}
{{< link-card title="ClientSample reference" description="Every record and field, generated from schema 3.7.0." href="/docs/schema/clientsample/" >}}
{{< link-card title="Version history" description="What changed in each release since 3.0.0, field by field." href="/docs/schema/versions/" >}}
{{< /card-grid >}}

## Quick install

{{< tabs "install" >}}
{{< tab "Browser" >}}
```bash
npm install @observertc/client-monitor-js
```

```javascript
import { ClientMonitor } from "@observertc/client-monitor-js";

const monitor = new ClientMonitor({ clientId, callId, samplingPeriodInMs: 5000 });
monitor.addSource(peerConnection);
monitor.on("sample-created", ({ sample }) => transport.send(sample));
```
{{< /tab >}}
{{< tab "Server" >}}
```bash
npm install @observertc/observer-js
```

```typescript
import { Observer } from "@observertc/observer-js";

const observer = new Observer({ closeClientIfIdleForMs: 60_000 });
observer.on("client-issue-resolved", ({ resolvedIssue }) => log.info(resolvedIssue));

transport.on("sample", (sample) => observer.accept(sample));
```
{{< /tab >}}
{{< tab "Both + a codec" >}}
```bash
npm install @observertc/client-monitor-js @observertc/samples-protobuf-codec   # browser
npm install @observertc/observer-js @observertc/samples-protobuf-codec         # server
```

Or swap in `@observertc/samples-json-codec` on both ends — same semantics, same error codes, no
dependencies.
{{< /tab >}}
{{< /tabs >}}

## Upgrading

{{< card-grid >}}
{{< link-card title="client-monitor-js 4.9" description="27 detector classes became 46, every group config key was retired, and the score is now a reading of the open issues." href="/docs/client-monitor-js/migration-4-9/" >}}
{{< link-card title="observer-js 1.0" description="Detector configuration, the update policy enum and the pluggable Updater are gone; inbound bitrate is now bps." href="/docs/observer-js/migration-1-0/" >}}
{{< link-card title="Schema 3.4 – 3.7" description="Payloads became records and then free-form JSON; scoreReasons became a map of contributions." href="/docs/schema/versions/" >}}
{{< /card-grid >}}
