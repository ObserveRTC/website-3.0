---
slug: "missing-statistics"
title: "Diagnose missing statistics"
description: "Distinguish unavailable browser fields from missing telemetry delivery."
lead: "Distinguish unavailable browser fields from missing telemetry delivery."
draft: false
outputs: ["HTML", "Markdown"]
weight: 50
toc: true
---

Use this guide when a metric is absent, a rate has no usable value, or expected server state does not appear.

## Confirm where data is missing

First distinguish a missing browser field, a missing derived metric, a missing sample, and a sample your backend never accepted. These occur at different boundaries.

## Diagnose in order

1. Confirm active media and the correct inbound/outbound scope.
2. Check whether the browser reports the raw inputs required by the metric.
3. Allow successive usable observations for interval rates. Check for counter resets and collection gaps.
4. Confirm whether the live metric is part of the sample's serialized projection; samples do not contain every live property.
5. Check the `sample-created` listener and transport when the browser has data but the server does not.
6. For encoded streams, verify ordered delivery and matching decoder state. Check decoding and validation failures before `accept()`.

## Resolve the appropriate boundary

Display unsupported measurements as unavailable. Correct registration, sample timing, or transport issues where evidence identifies them. Do not fill missing fields with zero: that can turn absent evidence into a false healthy or failed result.

A backgrounded tab, sleeping device, omitted browser field, first observation, or delivery failure can each explain different symptoms. Establish which one applies.

[Metric missing-value behavior](/docs/client-monitor-js/metrics/) · [Collection and sampling](/docs/client-monitor-js/sampling/) · [ClientSample fields](/docs/schema/clientsample/) · [Codecs](/docs/codecs/).
