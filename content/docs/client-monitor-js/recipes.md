---
slug: "recipes"
title: "Integration patterns"
description: "Choose a small implementation path for your use case."
lead: "Choose a small implementation path for your use case."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "Markdown"]
weight: 90
toc: true
---

{{< card-grid >}}
{{< link-card title="Local quality UI" description="Read live monitor values after stats-collected." href="/docs/overview/introduction/" >}}
{{< link-card title="Custom application metrics" description="Use extension stats and declared context." href="/docs/client-monitor-js/events-and-issues/" >}}
{{< link-card title="Backend telemetry" description="Send a ClientSample over your transport." href="/docs/client-monitor-js/sampling/" >}}
{{< link-card title="Call analysis" description="Reconstruct participants and correlate their issues." href="/docs/observer-js/" >}}
{{< /card-grid >}}

Do not interpret missing stats as zero. Display unavailable values explicitly, and avoid consuming internal `visited` bookkeeping getters in a diagnostic UI.
