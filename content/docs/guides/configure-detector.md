---
slug: "configure-detector"
title: "Configure a detector"
description: "Tune one condition without changing unrelated analysis."
lead: "Tune one condition without changing unrelated analysis."
draft: false
outputs: ["HTML", "Markdown"]
weight: 10
toc: true
---

Your goal is to tune or disable one Client Monitor detector. Start with a working monitor and identify the condition in the [detector catalog](/docs/client-monitor-js/detectors/).

## Choose a change

1. Read the detector's inputs, trigger, recovery behavior, and limitations.
2. Find its option and complete default object in [configuration](/docs/client-monitor-js/configuration/).
3. Decide whether you need a different threshold, additional application context, or to disable the detector.
4. Supply the complete replacement configuration. Nested objects are not deep-merged.
5. Observe normal and affected sessions at your chosen collection cadence before deploying the change.

```javascript
import { ClientMonitor } from '@observertc/client-monitor-js';

const monitor = new ClientMonitor({
  iceReachabilityDetector: { thresholdInMs: 10000 },
});
monitor.addSource(peerConnection);
monitor.on('issue', issue => console.log(issue.type, issue.payload));
```

This example changes the no-usable-network wait threshold from the documented 6000 ms default to 10000 ms. It does not change the other connectivity detectors. A threshold alone does not guarantee an exact notification time: required evidence and collection cadence still apply.

## Confirm and troubleshoot

Confirm that ordinary sessions do not generate misleading findings and that the intended affected case produces the expected evidence. If no issue appears, check input availability, detector gates, and application intent. Use `null` to disable a detector; do not use an empty object as a general replacement for required settings.
