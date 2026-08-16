---
title: "Libraries"
description: "The ObserveRTC library set"
lead: "Four packages that take you from RTCPeerConnection.getStats() to a live, correlated view of every call"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 300
toc: true
---

ObserveRTC is a set of independent libraries, not a platform you deploy. Take the ones you need.

```text
Browser                                Server
┌──────────────────────┐               ┌──────────────────────┐
│  client-monitor-js   │               │     observer-js      │
│                      │               │                      │
│  getStats() polling  │               │  live call model     │
│  derived metrics     │  ClientSample │  cross-client        │
│  detectors → issues  │──────────────►│  detectors           │
│  quality scores      │               │  publisher↔subscriber│
│                      │               │  correlation         │
└──────────┬───────────┘               └──────────▲───────────┘
           │                                      │
           │  samples-encoder      samples-decoder│
           └──────────────────────────────────────┘
                     binary transport
```

## The two you will actually integrate

{{< card-grid >}}
{{< link-card
  title="client-monitor-js"
  description="Runs in the browser. Turns raw getStats() counters into derived metrics, 0–5 quality scores, and issue verdicts with a start and an end. Works standalone — no server required."
  href="./client-monitor-js/" >}}
{{< link-card
  title="observer-js"
  description="Runs in Node.js. Maintains a live model of every call from the samples clients send, and answers the questions no single browser can: is it the room, the publisher, or our infrastructure?"
  href="./observer-js/" >}}
{{< /card-grid >}}

### `@observertc/client-monitor-js`

**Current: 4.3.2**

- Monitors `RTCPeerConnection`, mediasoup `Device` and mediasoup transports
- Per-interval bitrates, RTT, jitter, loss, frame rates and their volatility
- Seven built-in detectors with hysteresis, raising and resolving stateful issues
- Quality scores with a machine-readable penalty breakdown, and a replaceable calculator
- Extension points: custom detectors, stats adapters, extension stats providers, logger

```bash
npm install @observertc/client-monitor-js
```

[Documentation →](./client-monitor-js/)

### `@observertc/observer-js`

**Current: 1.0.0-beta.16** · Node.js ≥ 22 · dual ESM + CommonJS

- One ingestion method, one typed event bus, lazily created entities
- Counter-reset-safe deltas, RTCP correlation, ICE vs RTCP RTT kept distinct
- Ten cross-participant detectors and three one-shot deployment validators
- Publisher ↔ subscriber track correlation for any SFU topology
- mediasoup router observation for the server's own ground truth
- Per-client sinks for archival and offline replay

```bash
npm install @observertc/observer-js
```

[Documentation →](./observer-js/)

## Transport helpers

{{< card-grid >}}
{{< link-card
  title="sample-encoder-js"
  description="Compresses a ClientSample into the protobuf representation before upload. Same information, far fewer bytes."
  href="./sample-encoder-js/" >}}
{{< link-card
  title="sample-decoder-js"
  description="Decodes it again on the server, with schema validation and batch processing."
  href="./sample-decoder-js/" >}}
{{< /card-grid >}}

{{< callout context="caution" title="Version them together" icon="alert-triangle" >}}
The encoder and decoder are released in lockstep with the [schema](/docs/schema/). Protobuf field
numbers derive from field order, so a mismatched pair can misread a sample without erroring.
{{< /callout >}}

## Choosing what to use

| You want to… | Use |
|---|---|
| Show a network-quality indicator in your call UI | `client-monitor-js` alone |
| React in the browser — pause screen share on congestion, lower encoding on CPU pressure | `client-monitor-js` alone |
| Answer "what went wrong in this user's call at 3 pm?" | `client-monitor-js` + your own storage |
| Answer "was the whole room affected, or one person?" | add `observer-js` |
| Answer "is our SFU forwarding, or is the publisher's camera off?" | `observer-js` with a `RemoteTrackResolver` |
| Answer "is this concentrated on one browser version?" | `observer-js` with `ClientPopulationIssueDetector` |
| Cut telemetry upload cost | add the encoder / decoder pair |
| Replay past incidents against new detector settings | `observer-js` sinks + offline replay |

## They share one contract

Everything above speaks the same [schema](/docs/schema/). `client-monitor-js` produces a
`ClientSample`, `observer-js` consumes one, and the encoder/decoder pair moves one across the wire.
If you replace any single component with your own, the rest keeps working — which is the point of
having a versioned schema at all.
