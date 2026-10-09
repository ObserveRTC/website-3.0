---
slug: "backend"
title: "Send samples to your backend"
description: "Connect browser monitoring to server-side call analysis."
lead: "Connect browser monitoring to server-side call analysis."
draft: false
outputs: ["HTML", "Markdown"]
weight: 30
toc: true
---

Use this path when you need to compare participants or retain call diagnostics. Prerequisites are a working browser monitor and an authenticated backend transport you control.

## Connect the pipeline

1. Assign `callId` and `clientId` in Client Monitor from your application's identity model.
2. Attach a `sample-created` listener before samples begin. Forward its `sample` through your transport.
3. Authenticate and validate requests at your backend. Check that the sender may report for those identities.
4. If you use a codec, decode its ordered stream before processing the resulting sample.
5. Pass the decoded sample to `observer.accept(sample)`.
6. Register the [server detectors](/docs/observer-js/detectors/) you need and choose a [sink](/docs/observer-js/sinks/) if you require history.

## Confirm the result

The first accepted sample creates live call/client state. Subsequent samples update that state. Listen to `call-added` and `client-issue` as shown in the [Observer quick start](/docs/observer-js/quick-start/).

If no call appears, confirm that the sample reached your handler, validation succeeded, and both identifiers are present. Observer does not create your endpoint or decode a codec stream automatically.

See [backend integration](/docs/observer-js/recipes/) and [ingestion behavior](/docs/observer-js/ingestion/) for the authoritative implementation boundaries.
