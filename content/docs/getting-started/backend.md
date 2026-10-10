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

A browser can tell you what happened at one endpoint. Sending its observations to your backend lets you connect that evidence to a call: which participants were affected, what they were sending or receiving, and how the problem developed.

You do not need to study the schema or generate code to begin. Client Monitor creates the samples; your application delivers them. Start with a [working browser monitor](/docs/client-monitor-js/quick-start/) and a backend transport you control.

{{< component-flow from="Collect in the browser" fromText="Client Monitor creates a sample of the endpoint's observations." via="Deliver to your backend" viaText="Your application authenticates the sender and transports the sample." to="Build the call picture" toText="Observer updates live state; your storage retains history when needed." caption="Collection, delivery, and analysis have separate responsibilities." >}}

## Decide what you need

- **Browser diagnostics only:** stay with [Client Monitor](/docs/client-monitor-js/). Sending samples is optional.
- **Compare participants:** use [Observer](/docs/observer-js/) to organize accepted samples into live calls and clients.
- **Keep diagnostic history:** connect your own storage through an [Observer sink](/docs/observer-js/sinks/).
- **Reduce payload size later:** explore [Codecs](/docs/codecs/) after the basic delivery path works.

## What is a sample?

A `ClientSample` is the record Client Monitor prepares for transport. It carries timestamped observations and identifiers that let the backend associate them with a client and call. It is not a recording of the media, and it does not contain every property available in the live monitor.

For a first integration, consume the sample the library provides. The detailed [field reference](/docs/schema/clientsample/) is useful when you need a specific field or write a custom consumer. [Code generation](/docs/schema/general/) is for working on the schema contract, rather than a setup step for sending samples.

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
