---
slug: "quality-dimensions"
title: "Connectivity, transport, and media quality"
description: "Locate the stage of a call before choosing a diagnosis."
lead: "Locate the stage of a call before choosing a diagnosis."
draft: false
outputs: ["HTML", "Markdown"]
weight: 20
toc: true
---

A call can connect successfully and still deliver poor media. Separate the stages to understand which measurements matter.

| Dimension | Engineering question | Relevant evidence |
|---|---|---|
| Connectivity | Can the endpoints establish and maintain a usable path? | ICE gathering, connection state, selected candidates, DTLS state. |
| Transport quality | Is an established path delivering data well? | Loss, round-trip time, congestion, and path changes. |
| Pipeline disruption | Where does capture, encoding, delivery, decoding, or playout stop progressing? | Frame/counter progress and the relationship between adjacent stages. |
| Perceived quality | Does received media play continuously and with usable fidelity? | Freezes, concealment, playout behavior, and relevant application context. |

## Follow the symptom through the pipeline

For frozen video, first confirm whether bytes arrive, then whether frames decode, then whether frames render. This narrows the stage that lacks progress. Packet loss alone cannot establish whether the user sees a freeze, and successful ICE cannot establish that media is playing.

Context changes interpretation: paused media is different from an unexpected stall, and screen sharing has different content behavior from a camera. Supply [application context](/docs/client-monitor-js/application-context/) rather than guessing intent from counters.

## Endpoint and call-wide evidence

Client Monitor evaluates an endpoint's evidence. Observer can compare reports across participants and link publishers to receivers when signaling identifiers are available. Correlation strengthens an investigation; it does not automatically prove a root cause.

Read the [detector catalog](/docs/client-monitor-js/detectors/) for exact inputs and conditions, or follow a [diagnostic guide](/docs/guides/).
