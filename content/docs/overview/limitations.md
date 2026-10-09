---
slug: "limitations"
title: "Capabilities and limitations"
description: "Understand what the measurements can establish and where evidence ends."
lead: "Understand what the measurements can establish and where evidence ends."
draft: false
outputs: ["HTML", "Markdown"]
weight: 40
toc: true
---

ObserveRTC helps you inspect endpoint behavior and compare reports across a call. Its conclusions depend on what the browsers report, what your application declares, and which analysis you enable.

## Browser evidence varies

Browsers expose different fields and can omit measurements. A rate needs successive usable observations. Background tabs and sleeping devices can interrupt collection. A missing value is unavailable evidence, not zero and not proof of healthy media.

[Metrics and missing values](/docs/client-monitor-js/metrics/) describes these distinctions.

## Detection is not a confirmed root cause

A detector evaluates a defined condition. An ICE failure does not by itself identify a particular firewall; degradation shared by several receivers does not by itself prove an SFU outage. Compare related signals and signaling context before choosing a remediation.

## Your application owns integration boundaries

Neither library provides your ingestion endpoint, authentication policy, durable storage, or alert delivery. Client Monitor creates samples; your transport delivers them. Observer receives decoded samples and maintains live state; sinks and your application decide what history to retain.

## Versions and optional analysis matter

Observer has no server detectors registered by default. Track correlation requires the appropriate resolver and identifiers. Optional or unavailable analysis is not a clean bill of health.

Read [versions and compatibility](/docs/reference/versions/) and [known implementation differences](/docs/reference/known-differences/) before depending on historical behavior.
