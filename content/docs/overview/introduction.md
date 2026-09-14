---
title: "Introduction"
slug: "introduction"
description: "Introduction to the ObserveRTC monitoring toolkit"
lead: "Open-source WebRTC call quality monitoring you own end to end"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 110
toc: true
---

## What is ObserveRTC?

ObserveRTC is an open-source toolkit for monitoring WebRTC applications. It is a set of libraries,
not a service you sign up for: you include what you need, keep your data, and build the parts that
are specific to your product.

The problem it solves is narrow and real. `RTCPeerConnection.getStats()` gives you a flat map of
monotonically increasing counters joined by string ids. Almost every question you actually want to
ask — *what is the bitrate right now? is this video frozen? is the CPU the bottleneck or the
network? is the whole room affected or one person?* — requires differencing those counters,
normalising browser differences, applying hysteresis so you do not alert on one bad tick, and then
correlating across participants.

That is the work these libraries do.

## What you get

{{< card-grid >}}
{{< link-card
  title="Metrics, not counters"
  description="Per-interval bitrates, packet rates, RTT, jitter, loss, frame rates and their volatility — computed for you, on a navigable object graph."
  href="/docs/client-monitor-js/metrics/" >}}
{{< link-card
  title="Verdicts, not thresholds"
  description="Detectors with on/off hysteresis that raise an issue when a condition starts and resolve it when it ends, with a duration attached."
  href="/docs/client-monitor-js/detectors/" >}}
{{< link-card
  title="Correlation across participants"
  description="Server-side detection that separates 'one person's Wi-Fi' from 'this room is broken' from 'our infrastructure is in trouble'."
  href="/docs/observer-js/detectors/" >}}
{{< link-card
  title="A versioned schema"
  description="One typed contract shared by every component, generated into TypeScript, protobuf and documentation from a single Avro source."
  href="/docs/schema/" >}}
{{< /card-grid >}}

## Why ObserveRTC

- **Open source.** No hidden magic and no secret sauce — you can read exactly why a detector fired.
- **You own the data.** It runs in your browser code and on your servers. Nothing is sent anywhere
  you did not send it.
- **Modular.** Take the client library alone for in-call UX. Add the observer when you need
  cross-participant answers. Replace any piece with your own — they agree on a schema, not on an
  implementation.
- **Honest about its boundaries.** It does not ship a database, a dashboard or an alert router,
  because you already have opinions about those. It gives you events and a live model.

## What it is good for

| | |
|---|---|
| **Support triage** | A user says the call was bad at 3 pm. Issues carry a start, an end and a duration — you answer what was wrong, not guess from averages. |
| **In-call UX** | Show a real warning at the moment congestion is detected and take it down when it resolves. |
| **Adaptive behaviour** | Pause screen share on sustained congestion, lower the encoding on CPU limitation, prompt a device check on a dry outbound track — in the client, before the user complains. |
| **Release regression** | Tag samples with your build version and compare issue rates and score distributions between releases. |
| **Infrastructure incidents** | The same symptom across independent calls implicates the servers, because those clients share nothing else. |
| **Deployment validation** | Prove that simulcast adapts per receiver, that track correlation is wired, and that you are on the codec you think you negotiated. |

## Who it is for

- **Application developers** debugging real WebRTC problems in production.
- **Product owners** who want quality trends they can act on rather than a vendor's opaque score.
- **Operations teams** who need to know quickly whether an incident is one user, one room, or the
  fleet.

## Getting started

{{< tabs "start" >}}
{{< tab "Browser" >}}
```bash
npm install @observertc/client-monitor-js
```

```javascript
import { ClientMonitor } from "@observertc/client-monitor-js";

const monitor = new ClientMonitor({
    clientId: "user-42",
    callId: "room-abc",
    collectingPeriodInMs: 5000,
    samplingPeriodInMs: 5000,
});

monitor.addSource(peerConnection);

monitor.on("issue", (issue) => console.warn(issue.type, issue.payload));
monitor.on("sample-created", ({ sample }) => transport.send(sample));
```

[Full documentation →](/docs/client-monitor-js/)
{{< /tab >}}
{{< tab "Server" >}}
```bash
npm install @observertc/observer-js
```

```typescript
import { Observer } from "@observertc/observer-js";

const observer = new Observer({ closeClientIfIdleForMs: 60_000 });

observer.on("client-issue-resolved", ({ observedClient, resolvedIssue }) => {
    analytics.track("quality_episode", {
        clientId: observedClient.clientId,
        type: resolvedIssue.type,
        durationInMs: resolvedIssue.durationInMs,
    });
});

transport.on("sample", (sample) => observer.accept(sample));
```

[Full documentation →](/docs/observer-js/)
{{< /tab >}}
{{< /tabs >}}

## Next steps

{{< card-grid >}}
{{< link-card title="Architecture" description="How the pieces fit together and where the client/server line is drawn." href="/docs/overview/architecture/" >}}
{{< link-card title="Client Monitor" description="The browser library: derived metrics, 46 detectors, quality scores." href="/docs/client-monitor-js/" >}}
{{< link-card title="Observer" description="The Node.js library: a live call model and cross-participant detection." href="/docs/observer-js/" >}}
{{< link-card title="Schema" description="The shared contract, and what changed in each version." href="/docs/schema/" >}}
{{< /card-grid >}}
