---
slug: "migration-1-0"
title: "Observer 1.0 integration notes"
description: "Account for current registration, updates and known behavior."
lead: "Account for current registration, updates and known behavior."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 100
toc: true
---

A new Observer starts with empty detector registries. Call updates drive Observer updates by default; disable this only when your application will call `update()` itself.

Idle clients and empty calls each default to a 60-second timeout. An explicit `undefined` in the supplied configuration overrides those defaults.

Call summaries are opt-in. The source currently has important differences from its documentation around middleware, omitted ICE metadata and zero-score history.

[Review known differences](/docs/reference/known-differences/) · [Review ingestion](/docs/observer-js/ingestion/)
