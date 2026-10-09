---
slug: "scoring"
title: "Quality dimensions and scoring"
description: "Use a quality overview without losing the evidence behind it."
lead: "Use a quality overview without losing the evidence behind it."
draft: false
outputs: ["HTML", "Markdown"]
weight: 40
toc: true
---

A quality score summarizes measured penalties so you can spot affected endpoints and media components. Client Monitor reports values on a 0–5 scale. Use the score to choose where to investigate, then examine component reasons, issues, and metrics.

## Aggregation changes the meaning

The client's default calculator combines available quality dimensions in a way that keeps a severe bad dimension visible. Observer's default call score is a weighted arithmetic mean of client scores. A client score and a call score therefore answer different questions.

## Missing evidence matters

Unavailable dimensions are excluded from the client aggregation. A score does not establish that every browser measurement was available. Some continuous penalties reduce quality without opening an issue or publishing a reason for every small change.

## Practical use

When a call score drops, find the affected client. Then identify whether receiving, sending, or connection stability carries the penalty. Follow the related metrics instead of displaying the aggregate as the root cause.

Exact formulas and reason behavior belong in the [Client Monitor quality-score reference](/docs/client-monitor-js/scoring/) and [Observer entity guide](/docs/observer-js/entities/).
