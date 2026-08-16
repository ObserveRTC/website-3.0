---
title: "Documentation"
description: "ObserveRTC Documentation - Complete guide to monitoring WebRTC applications"
lead: "Everything you need to instrument, collect and analyse WebRTC call quality"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
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
turns `getStats()` into actionable verdicts, a Node.js library that correlates those verdicts
across participants, and a versioned schema that ties them together.

## Start here

{{< card-grid >}}
{{< link-card title="Introduction" description="What ObserveRTC is, what it gives you, and who it is for." href="/docs/overview/introduction/" >}}
{{< link-card title="Architecture" description="How the pieces fit together, and where the client/server line is drawn." href="/docs/overview/architecture/" >}}
{{< /card-grid >}}

## The libraries

{{< card-grid >}}
{{< link-card
  title="client-monitor-js"
  description="Browser-side monitoring: derived metrics, quality scores, and detectors that raise and resolve issues with hysteresis."
  href="/docs/libraries/client-monitor-js/" >}}
{{< link-card
  title="observer-js"
  description="Server-side analysis: a live model of every call plus cross-participant detection that answers what no single browser can."
  href="/docs/libraries/observer-js/" >}}
{{< /card-grid >}}

{{< card-grid >}}
{{< link-card title="sample-encoder-js" description="Compress samples before upload." href="/docs/libraries/sample-encoder-js/" >}}
{{< link-card title="sample-decoder-js" description="Decode them on the server." href="/docs/libraries/sample-decoder-js/" >}}
{{< /card-grid >}}

## The schema

{{< card-grid >}}
{{< link-card title="Schema overview" description="One contract shared by every component, generated from Avro." href="/docs/schema/" >}}
{{< link-card title="ClientSample reference" description="Every record and field, generated from schema 3.3.0." href="/docs/schema/clientsample/" >}}
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

const monitor = new ClientMonitor({ clientId, callId, samplingPeriodInMs: 4000 });
monitor.addSource(peerConnection);
monitor.on("sample-created", (sample) => transport.send(sample));
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
{{< tab "Both + binary transport" >}}
```bash
npm install @observertc/client-monitor-js @observertc/samples-encoder   # browser
npm install @observertc/observer-js @observertc/samples-decoder         # server
```
{{< /tab >}}
{{< /tabs >}}
