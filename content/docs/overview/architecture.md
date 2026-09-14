---
title: "Architecture"
slug: "architecture"
description: "ObserveRTC system architecture and where responsibility is drawn"
lead: "How the pieces fit together — and why the client/server line sits where it does"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 120
toc: true
---

```text
   BROWSER                                    SERVER                            YOUR SYSTEM
┌───────────────────────┐              ┌────────────────────────┐          ┌──────────────────┐
│  client-monitor-js    │              │      observer-js       │          │                  │
│                       │              │                        │          │  Metrics         │
│  • poll getStats()    │ ClientSample │  • live call model     │  events  │  Alerting        │
│  • derive metrics     │─────────────►│  • cross-client        │─────────►│  Dashboards      │
│  • run detectors      │  (JSON or    │    detectors           │          │  Storage         │
│  • score quality      │   protobuf)  │  • publisher↔subscriber│          │  Post-call       │
│  • emit samples       │              │    correlation         │          │    reports       │
└───────────────────────┘              └───────────┬────────────┘          └──────────────────┘
                                                   │
                                          ┌────────▼────────┐
                                          │   mediasoup     │
                                          │   Router        │  ← optional: the SFU's own
                                          │   observation   │    ground truth
                                          └─────────────────┘
```

## The organising principle

{{< callout context="tip" title="If a condition is detectable on the client, the client's verdict is the source of truth" icon="rocket" >}}
This one rule explains most of ObserveRTC's design.

The browser has information the server never gets: whether an ICE `disconnected` persisted or
healed in 200 ms, whether `concealedSamples` rose during speech or during silence, whether the
jitter buffer grew *and* NetEQ is time-stretching or grew and succeeded. A server re-deriving those
from raw counters sees less and guesses more.

So `client-monitor-js` decides **what is wrong with this endpoint**, and `observer-js` never
repeats that work. It answers the orthogonal question: **who else is in this state, what do they
share, and where does the fault begin?**
{{< /callout >}}

## Client side

`client-monitor-js` polls `getStats()` on a configurable period and does four things with the
result:

| Step | Output |
|---|---|
| **Adapt** | Browser-specific differences normalised away |
| **Derive** | Counters differenced into bitrates, rates, deltas, smoothed and volatility metrics |
| **Detect** | Detectors raise and resolve stateful issues with hysteresis |
| **Score** | 0–5 quality per track, per connection and per client, with reasons |

On the sampling period it snapshots all of it — plus events, issues, metadata and your own
extension stats — into a [`ClientSample`](/docs/schema/clientsample/).

Nothing here requires a server. A monitor with no `sample-created` handler is a perfectly good
in-browser diagnostics tool.

[client-monitor-js →](/docs/client-monitor-js/)

## Transport

`ClientSample` is plain JSON, so any transport works: `fetch`, `sendBeacon`, a WebSocket, a message
queue. For volume, two **delta codecs** send only what changed since the previous sample — which is
where nearly all of the saving is, because a sample mostly repeats itself from one interval to the
next:

| Codec | Take it when |
|---|---|
| [`samples-protobuf-codec`](/docs/samples-protobuf-codec/) | Bytes on the wire are the binding constraint |
| [`samples-json-codec`](/docs/samples-json-codec/) | The transport already compresses, and you would rather have zero dependencies (~2 KB) and a payload you can read in a log |

Both are stateful: **one encoder per client, one decoder per client stream, fed in order**, over an
ordered lossless transport.

The library does not ship a transport, and does not want to — the right choice depends on your
existing telemetry pipeline.

## Server side

`observer-js` accepts samples through one method and maintains a live in-memory tree:

```text
Observer → ObservedCall → ObservedClient → ObservedPeerConnection → sub-stats
```

Entities are created lazily by id and garbage-collected when they stop appearing. Everything is
reachable from one typed event bus, where each payload carries its full ancestry.

On top of that model sit two kinds of analysis:

- **Detectors** run every tick and answer *"is something wrong right now?"* — across the
  participants of a call, or across the calls of a fleet.
- **Validators** run once and answer *"is this deployment built correctly?"* — is the resolver
  wired, does the SFU adapt layers per receiver, is everyone on the codec you configured.

[observer-js →](/docs/observer-js/)

## What the server adds that a browser cannot

| Question | Mechanism |
|---|---|
| Is this the room or this person? | Concurrent-issue detection across participants of one call |
| Is this our infrastructure? | The same symptom across **independent** calls — they share only the servers |
| Is this the publisher or the receiver? | Publisher ↔ subscriber track links from a `RemoteTrackResolver` |
| Is the SFU forwarding, or did the camera stop? | Publisher's outbound RTP versus every subscriber's dry-track verdict |
| Is this one kind of client? | Grouping by browser / engine / platform / OS, gated on relative risk |
| Is a TURN server down? | Population collapse plus a healthy control group elsewhere |
| Is anyone even subscribed to this track? | The resolver's silence — an empty subscriber set |

## Optional: the SFU's own view

When you run mediasoup, `observer-js` can attach to a live `Router` and passively record the
server's ground truth — transports, producers, consumers, their exact lifetimes and state
transitions — into a `MediasoupRouterSample`, completely independent of the client pipeline.

Peer connections and mediasoup WebRTC transports share ids, so the observer can tell you when a
client's peer connection corresponds to one of the router's transports. It emits that as an event
and steps back: how you associate the two is application-specific.

[SFU integration →](/docs/observer-js/sfu/)

## Where your system takes over

ObserveRTC deliberately stops at the event boundary. It does not ship a database, a dashboard, an
alert router or a retention policy, because those are exactly the parts every organisation already
has opinions about.

What it gives you instead:

- **Events** to feed your alerting and metrics pipeline
- **A live model** to query for real-time views
- **Sinks** that persist the exact samples that were accepted — which means past incidents can be
  replayed through a fresh observer with different detector settings, offline, in seconds

## Deployment shapes

{{< tabs "shapes" >}}
{{< tab "Client only" >}}
No server component. The monitor drives in-call UX and adaptive behaviour directly.

- Network quality indicator
- Pause screen share on congestion, lower encoding on CPU pressure
- Prompt a device check on a dry outbound track

Nothing leaves the browser.
{{< /tab >}}
{{< tab "Client + storage" >}}
Samples are uploaded and archived; no live analysis.

- Per-user support triage: what was wrong, when, and for how long
- Release comparison via `attachments`
- Replay archives through `observer-js` later, whenever you want the correlation

The cheapest path to answering "what happened in this call?".
{{< /tab >}}
{{< tab "Full stack" >}}
Samples flow into a live `observer-js` instance alongside archival.

- Real-time cross-participant and cross-call detection
- Publisher ↔ subscriber correlation
- Deployment validation at start-up and after each deploy
- Post-call reports built on [`call-summary`](/docs/observer-js/call-summaries/)

This is where the questions a browser cannot answer get answered.
{{< /tab >}}
{{< /tabs >}}
