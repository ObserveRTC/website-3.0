---
title: "Client Monitor"
description: "Collect browser stats, inspect live monitors, and detect endpoint problems."
lead: "Collect browser stats, inspect live monitors, and detect endpoint problems."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 20
toc: true
---

`@observertc/client-monitor-js` runs in your browser. It turns the browser’s `getStats()` reports into measurements you can use: sending and receiving bitrates, media quality, connection health, and detected problems. You can inspect these values while a call is running. Use it on its own or send samples to Observer.

The current release used for installation guidance is **4.10.1**. Install without a version suffix to follow npm’s `latest` release. Detailed implementation references identify their [verified source revision](/docs/reference/versions/).

## Start here

Begin with the [Client Monitor quick start](/docs/client-monitor-js/quick-start/), then attach your connections, configure collection, and choose the measurements you need.

{{< card-grid >}}
{{< link-card title="Integrate" description="A short working path for a peer connection or mediasoup transport." href="/docs/client-monitor-js/integrations/" >}}
{{< link-card title="Monitors & metrics" description="Find fields, formulas and missing-value behavior." href="/docs/client-monitor-js/metrics/" >}}
{{< link-card title="Detectors" description="Triggers, thresholds, state and recovery across five categories." href="/docs/client-monitor-js/detectors/" >}}
{{< link-card title="Configuration" description="Defaults, cadence and disabling a detector." href="/docs/client-monitor-js/configuration/" >}}
{{< link-card title="Events & issues" description="Local events and the serialized issue lifecycle." href="/docs/client-monitor-js/monitor-events/" >}}
{{< link-card title="Scoring" description="Component penalties and client aggregation." href="/docs/client-monitor-js/scoring/" >}}
{{< /card-grid >}}
