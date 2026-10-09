---
title: "Reference"
description: "Source-backed details for integration and development."
lead: "Source-backed details for integration and development."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "RSS", "SITEMAP", "Markdown"]
landingTitle: "Reference index"
weight: 50
toc: true
---

Use this index to find the authoritative contract for the component you are integrating. Installation guidance and historical generated references have different version coverage; check [versions and compatibility](/docs/reference/versions/) before depending on a detail.

## Component contracts

| Area | Authoritative pages |
|---|---|
| Client Monitor | [API and relationships](/docs/client-monitor-js/api-reference/), [configuration](/docs/client-monitor-js/configuration/), [metrics](/docs/client-monitor-js/metrics/). |
| Events and issues | [Monitor events](/docs/client-monitor-js/monitor-events/), [monitor issues](/docs/client-monitor-js/monitor-issues/), [Observer events](/docs/observer-js/event-bus/). |
| Detectors | [Client catalog](/docs/client-monitor-js/detectors/), [server detectors](/docs/observer-js/detectors/). |
| Observer | [Configuration](/docs/observer-js/configuration/), [ingestion](/docs/observer-js/ingestion/), [entities](/docs/observer-js/entities/). |
| Sample and codecs | [Sample fields](/docs/schema/clientsample/), [generation/compatibility](/docs/schema/general/), [codec contracts](/docs/codecs/). |



{{< card-grid >}}
{{< link-card title="Monitor catalog" description="Public properties and accessors, grouped by monitor." href="/docs/reference/monitor-catalog/" >}}
{{< link-card title="Versions" description="Released versions and source revisions." href="/docs/reference/versions/" >}}
{{< link-card title="Known differences" description="Documentation disagreements and reproduced behavior." href="/docs/reference/known-differences/" >}}
{{< link-card title="Contributing" description="Where metrics, detectors, schema and server changes belong." href="/docs/reference/contributing/" >}}
{{< /card-grid >}}

## Complete references

- [Field calculations and serialization source](/reference/monitor-fields-and-formulas.md)
- [Detector source and defaults](/reference/detector-implementation-reference.md)
- [Focused verification results](/reference/verification-results.json)

These are pinned snapshots from 28 September 2026. Source comments are preserved; the known-differences page records verified disagreements.

## Source licenses

The offline references retain source snapshots under their repositories’ licenses.

- [website-3.0](/reference/licenses/website-3.0.txt)
- [observer-js](/reference/licenses/observer-js.txt)
- [schemas](/reference/licenses/schemas.txt)
- [client-monitor-js](/reference/licenses/client-monitor-js.txt)
- [stats-dashboard](/reference/licenses/stats-dashboard.txt)
