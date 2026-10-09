---
slug: "telemetry"
title: "Telemetry and glossary"
description: "The shared vocabulary for ObserveRTC documentation."
lead: "The shared vocabulary for ObserveRTC documentation."
draft: false
outputs: ["HTML", "Markdown"]
weight: 10
toc: true
---

Telemetry is the data you collect to understand the behavior of a running application. In ObserveRTC, it connects browser observations to endpoint and call-level analysis. Keep the observation separate from the conclusion you draw from it.

| Term | Meaning |
|---|---|
| Raw statistic | A value reported by a browser or WebRTC implementation, such as a byte counter. |
| Adapted statistic | A reported value or relationship normalized to account for browser differences. It is not automatically a direct browser measurement. |
| Derived metric | A calculated value, such as bitrate derived from the change in bytes over elapsed time. |
| Detector | A component that evaluates specified signals to identify a condition. |
| Issue | A record of a detected condition; stateful issues have a raise and resolution lifecycle. |
| Event | A notification from a component, or a recorded application occurrence. Local callbacks and serialized application events are distinct. |
| Quality score | A computed assessment of a component or quality dimension, with defined aggregation and missing-data behavior. |
| Sample | A serializable snapshot of current telemetry plus buffered discrete records. It is not an average of every intervening update. |
| Collection | Reading browser statistics and updating live measurements and detectors. |
| Sampling | Creating the telemetry record that your application may send or store. |
| Client | One monitored endpoint represented by `clientId`; not necessarily a unique human. |
| Call | A group of monitored clients identified by `callId`. |
| Session-level evaluation | Analysis across participants or connections, where the required signals and correlation are available. |
| Track | The audio or video object used by the application. |
| RTP stream | An encoded stream carrying media; one outbound track can have several streams. |

## A practical distinction

A byte counter says how much data has been received. A bitrate says how quickly it arrived over a measured interval. An issue might report a stream that stopped progressing. A score summarizes penalties. These answer different questions and should not be used interchangeably.

## Units and scope

Always identify whether a value belongs to a client, connection, track, or RTP stream. Check units before comparing values: raw WebRTC fields and derived ObserveRTC fields can use different units. Missing data is not zero.

This page is the shared glossary. Exact fields and calculations remain in [metrics](/docs/client-monitor-js/metrics/), [sample fields](/docs/schema/clientsample/), and their versioned source references.
