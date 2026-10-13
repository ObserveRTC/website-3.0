---
title: "Codecs"
description: "Choose JSON, protobuf, or deflate for stateful sample transport."
lead: "Choose JSON, protobuf, or deflate for stateful sample transport."
draft: false
outputs: ["HTML", "RSS", "SITEMAP", "Markdown"]
landingTitle: "Choosing a codec"
weight: 45
toc: false
---

ObserveRTC codecs encode changes between successive `ClientSample` records. Choose JSON for readable messages, protobuf for its binary representation, or Deflate for structural deltas with dictionary coding and platform compression.

{{< component-flow from="A sample stream" fromText="Start with samples from one monitored client." via="Encode and transport" viaText="Use your chosen codec over a transport you control." to="Decoded samples" toText="Restore complete samples before analysis." caption="Optional encoding between collection and backend analysis." >}}

{{< card-grid >}}
{{< link-card title="Protobuf Codec" description="Compact binary deltas with encoding and decoding in one package." href="/docs/codecs/protobuf/" >}}
{{< link-card title="JSON Codec" description="Readable JSON deltas with zero runtime dependencies." href="/docs/codecs/json/" >}}
{{< link-card title="Deflate Codec" description="Dictionary-coded structural deltas with per-message platform compression." href="/docs/codecs/deflate/" >}}
{{< /card-grid >}}

Use one encoder and decoder per client stream. Preserve order and complete delivery; reset at reconnect or snapshot boundaries. Decode samples before passing them to Observer.

## Integration boundaries

A codec compresses sample representation; it does not authenticate, deliver, or
store telemetry. Each encoder/decoder maintains stream state, so do not share a
single decoder between unrelated clients. Handle reconnects and missing messages
according to the selected codec's reset/snapshot contract.

Choose a format using your transport constraints and actual streams. Compression
results documented in the codec pages describe their measured fixtures, not a
guarantee for every deployment. Decode before passing samples to Observer.
