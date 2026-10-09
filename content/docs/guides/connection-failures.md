---
slug: "connection-failures"
title: "Investigate connection failures"
description: "Separate gathering, traversal, secure transport, and established-path failure."
lead: "Separate gathering, traversal, secure transport, and established-path failure."
draft: false
outputs: ["HTML", "Markdown"]
weight: 20
toc: true
---

Use this guide when a call never connects or loses connectivity. You need the affected peer connection's state, current detector evidence, and your application's connection/signaling logs.

## Confirm the symptom

Check whether the connection ever reached a working state. Establishment problems and failures after prior success require different evidence.

## Investigate in order

1. Check local candidate gathering. No local candidates narrows the investigation to local reachability or gathering; it does not identify a particular firewall.
2. Check whether a candidate pair was selected and whether ICE established a path.
3. If ICE is usable, check DTLS state to separate secure-transport negotiation from path establishment.
4. If the path previously worked, check disconnection/failure state and current path progress.
5. Compare application signaling and ICE-server configuration with the affected interval.

## Interpret and respond

Candidate absence, failure state, or stalled DTLS are different findings. Fix or retry the stage supported by the evidence. If your application uses ICE-restart recommendations, it decides whether to restart; the recommendation does not itself perform recovery.

Possible causes include unusable local networking, unsuccessful traversal, or secure-transport negotiation failure. Confirm these with the corresponding evidence rather than treating every connectivity issue as a TURN outage.

[Connectivity detector reference](/docs/client-monitor-js/detectors-connectivity/) · [Telemetry recommendations](/docs/client-monitor-js/detectors-telemetry/) · [Monitor relationships](/docs/client-monitor-js/api-reference/).
