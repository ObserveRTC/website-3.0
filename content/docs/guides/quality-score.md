---
slug: "quality-score"
title: "Interpret a quality score"
description: "Use scores to locate an affected component, then explain the evidence."
lead: "Use scores to locate an affected component, then explain the evidence."
draft: false
outputs: ["HTML", "Markdown"]
weight: 60
toc: true
---

Use this guide when a client or call score drops. You need the score's scope, its component measurements, and any reported score reasons.

## Investigate a change

1. Identify whether you are reading a client, track, connection, or call score.
2. For a call score, locate the clients whose scores changed.
3. For a client, inspect receiving, sending, and connection-stability components.
4. Read component reasons and active issues, then compare the associated metrics.
5. Check whether relevant dimensions or inputs were unavailable during the interval.

## Expected result

You can explain which measured component contributed to the score change and which evidence supports it. A score alone does not name a root cause or guarantee what the user heard or saw.

## Common interpretation mistakes

Call and client aggregation differ. Continuous penalties can lower scores without opening an issue. Empty reasons are not proof of perfect media, and a high score does not establish that every dimension was measured.

Use the [score reference](/docs/client-monitor-js/scoring/) for formulas, penalties, and reason-shipping behavior, and [Observer entities](/docs/observer-js/entities/) for call aggregation.
