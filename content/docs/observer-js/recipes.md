---
slug: "recipes"
title: "Backend integration pattern"
description: "Keep decoding, validation, live analysis and persistence explicit."
lead: "Keep decoding, validation, live analysis and persistence explicit."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 90
toc: true
---

1. Authenticate the incoming connection and determine the allowed call/client identities.
2. Decode with the matching codec when using encoded samples. Preserve stream order and decoder state.
3. Validate the payload and filter it in application code before `accept()`.
4. Pass the accepted sample and optional request context to Observer.
5. Subscribe to events and register the detectors your application needs.
6. Persist through a per-client sink; enable call summaries at construction if required.
7. Close Observer during application shutdown.

[Quick start](/docs/overview/introduction/) · [Ingestion limitations](/docs/observer-js/ingestion/) · [Sinks](/docs/observer-js/sinks/)

[Official integration examples](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/examples/)
