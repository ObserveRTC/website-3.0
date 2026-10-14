---
slug: "versions"
title: "Versions and compatibility"
description: "Choose component versions that use the same ClientSample schema."
lead: "Match your sample schema across collection, analysis, and visualization."
draft: false
outputs: ["HTML", "Markdown"]
weight: 20
toc: false
---

The sample schema connects the components. Client Monitor produces samples; Observer processes them; Stats Dashboard reads the archived records. Use the table to choose versions that share that contract.

| Sample schema | Observer JS | Client Monitor JS | Client Monitor C++ | Stats Dashboard |
|---|---|---|---|---|
| 3.5.0 | — | — | — | — |
| 3.6.0 | — | 4.7.0 | — | — |
| 3.7.0 | 1.1.0, 1.2.0 | 4.8.0, 4.9.0, 4.10.0, 4.10.1 | 0.1.0 | 0.1.0 |

Entries identify versions that use or target that schema. **—** means no version is listed for that combination; it does not mean all versions are incompatible. The table lists specific versions rather than promising support for every later release.

For a new integration, choose schema **3.7.0**. Stats Dashboard's documented client target starts at Client Monitor JS 4.9.0. It can normalize selected older record formats, but that is not full support for every older schema.

## Before connecting components

- Include `clientId` and `callId` when sending samples to Observer.
- Decode codec messages into complete samples before analysis or archiving.
- Store dashboard client streams in its [documented JSONL layout](/docs/stats-dashboard/).
- Check [native client capabilities](/docs/client-monitor-js/native-cpp/) if you need detectors or scoring: a matching schema does not give every producer the same features.

See [Updates](/updates/) for release changes and migration notes.

## Source references

- [Client Monitor JS 4.7.0 schema](https://github.com/ObserveRTC/client-monitor-js/blob/4.7.0/src/schema/ClientSample.ts)
- [Client Monitor JS 4.8.0 schema](https://github.com/ObserveRTC/client-monitor-js/blob/4.8.0/src/schema/ClientSample.ts)
- [Client Monitor JS 4.9.0 schema](https://github.com/ObserveRTC/client-monitor-js/blob/4.9.0/src/schema/ClientSample.ts)
- [Client Monitor JS 4.10.0 schema](https://github.com/ObserveRTC/client-monitor-js/blob/4.10.0/src/schema/ClientSample.ts)
- [Client Monitor JS 4.10.1 schema](https://github.com/ObserveRTC/client-monitor-js/blob/4ae541eac3305d1cc779ff6dd703211e837a7f7b/src/schema/ClientSample.ts)
- [Observer JS 1.1.0 schema](https://github.com/ObserveRTC/observer-js/blob/1.1.0/src/schema/ClientSample.ts)
- [Observer JS 1.2.0 schema](https://github.com/ObserveRTC/observer-js/blob/1.2.0/src/schema/ClientSample.ts)
- [Client Monitor C++ 0.1.0 sample contract](https://github.com/ObserveRTC/client-monitor-cpp/blob/v0.1.0/PORTING.md)
- [Stats Dashboard sample contract](https://github.com/ObserveRTC/stats-dashboard/blob/323a1b28553758edafaa0abd0d4211c9e13de9ea/src/schema/ClientSample.ts)
