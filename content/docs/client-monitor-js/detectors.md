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

Version 4.9.1 has **46 detector classes**. Class files, not historical table counts, define availability. Categories describe the condition being judged, not necessarily the registry/owner. `IceTraversal`, `IceRestart`, and `IceRestartRecommendation` are Telemetry even though their subject is connectivity. `IcePathEstablishment` is event-only Connectivity. `AudioPlayoutSynthesis` currently raises an issue despite stale event-only descriptions in stable taxonomy prose.

Each config key is lowerCamelCase class name; undefined selects the default object, null prevents registration, an object replaces that detector's default object. **Nested detector defaults are not deep-merged by ClientMonitor's `detectorDefault` helper.** Passing `{}` to a detector requiring thresholds can leave required values undefined; do not advertise `{}` as generic “use defaults.” Top-level type permits partial root config, not arbitrary partial nested configs. `BlockedInboundMediaDetector` is disabled by default because its evidence premise is not generally usable with browser RTCP mux. Deprecated `CongestionDetector` remains enabled by default.

Default shared windows: detection 3/recovery 3 values for client, PC, inbound and outbound tracks; inbound flow detection 4/flow recovery 3. Max allowed gap defaults to four times a positive collecting period (fallback period 5000 ms). Default flags: integrate media devices/watch visibility/join event/left event true; buffering events and pre-subscriber samples false; resolved issue shipping, score reason shipping and on-change ICE metadata true. See [client-monitor-js/src/ClientMonitor.ts · constructor](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L146), [client-monitor-js/src/ClientMonitorConfig.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitorConfig.ts), [client-monitor-js/src/detectors/Detectors.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/Detectors.ts).

The following summaries identify the main trigger and recovery. **Exact comparison operators, missing-input paths, state variables, payload types and event names are preserved per class in the [detector reference](/reference/detector-implementation-reference.md).** A time threshold alone is insufficient to reproduce a detector.


Exact source, state, emitted payloads and resolution paths are in the [implementation reference](/reference/detector-implementation-reference.md).
