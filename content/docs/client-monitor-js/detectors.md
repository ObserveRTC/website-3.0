---
slug: "detectors"
title: "Detector catalog"
description: "Start with the symptom, then inspect the evidence and recovery rule."
lead: "Start with the symptom, then inspect the evidence and recovery rule."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 80
toc: true
---

Stable 4.9.1 contains **46 detector classes**. Categories describe the condition; monitor ownership describes where the detector runs. An event does not necessarily open an issue, and an issue does not necessarily lower a score.

{{< card-grid >}}
{{< link-card title="Connectivity" description="Connection establishment, handshake failures and path changes." href="/docs/client-monitor-js/detectors-connectivity/" >}}
{{< link-card title="Transport Quality" description="Delay, loss, congestion and stalled media transport." href="/docs/client-monitor-js/detectors-transport-quality/" >}}
{{< link-card title="Pipeline Disruption" description="Capture, encoding, delivery, decoding and playout failures." href="/docs/client-monitor-js/detectors-pipeline/" >}}
{{< link-card title="Perceived Quality" description="Visible and audible degradation, including synchronization." href="/docs/client-monitor-js/detectors-perceived-quality/" >}}
{{< link-card title="Telemetry" description="State changes and collection-health events." href="/docs/client-monitor-js/detectors-telemetry/" >}}
{{< /card-grid >}}
## Configuration and lifecycle

Detectors run on their owning client, peer connection or track as observations arrive. Their category describes the condition being judged, rather than their owner.

Use [Configuration](/docs/client-monitor-js/configuration/) for defaults and overrides. A detector configuration object replaces its defaults; nested values are not deep-merged. Set a detector to `null` to disable registration.

The category guides describe triggers and recovery. For exact comparison operators, missing-input behavior, emitted payloads and resolution paths, use the [implementation reference](/reference/detector-implementation-reference.md).
