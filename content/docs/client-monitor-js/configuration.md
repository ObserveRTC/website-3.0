---
slug: "configuration"
title: "Configuration"
description: "Use verified defaults and complete detector overrides."
lead: "Use verified defaults and complete detector overrides."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 50
toc: true
---

Version 4.9.1 has **46 detector classes**. Class files, not historical table counts, define availability. Categories describe the condition being judged, not necessarily the registry/owner. `IceTraversal`, `IceRestart`, and `IceRestartRecommendation` are Telemetry even though their subject is connectivity. `IcePathEstablishment` is event-only Connectivity. `AudioPlayoutSynthesis` currently raises an issue despite stale event-only descriptions in stable taxonomy prose.

Each config key is lowerCamelCase class name; undefined selects the default object, null prevents registration, an object replaces that detector's default object. **Nested detector defaults are not deep-merged by ClientMonitor's `detectorDefault` helper.** Passing `{}` to a detector requiring thresholds can leave required values undefined; do not advertise `{}` as generic “use defaults.” Top-level type permits partial root config, not arbitrary partial nested configs. `BlockedInboundMediaDetector` is disabled by default because its evidence premise is not generally usable with browser RTCP mux. Deprecated `CongestionDetector` remains enabled by default.

Default shared windows: detection 3/recovery 3 values for client, PC, inbound and outbound tracks; inbound flow detection 4/flow recovery 3. Max allowed gap defaults to four times a positive collecting period (fallback period 5000 ms). Default flags: integrate media devices/watch visibility/join event/left event true; buffering events and pre-subscriber samples false; resolved issue shipping, score reason shipping and on-change ICE metadata true. See [client-monitor-js/src/ClientMonitor.ts · constructor](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L146), [client-monitor-js/src/ClientMonitorConfig.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitorConfig.ts), [client-monitor-js/src/detectors/Detectors.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/Detectors.ts).

The following summaries identify the main trigger and recovery. **Exact comparison operators, missing-input paths, state variables, payload types and event names are preserved per class in the [detector reference](/reference/detector-implementation-reference.md).** A time threshold alone is insufficient to reproduce a detector.


## Common setup

```javascript
const monitor = new ClientMonitor({
  clientId: 'participant-42',
  callId: 'room-123',
  collectingPeriodInMs: 5000,
  samplingPeriodInMs: 5000,
  congestionDetector: null, // disable the deprecated detector
});
```

To change a detector threshold, use that detector's complete configuration type. A nested object replaces the constructor's default object; it is not a deep partial override.

[Browse all default objects and detector configuration types](/reference/detector-implementation-reference.md).
