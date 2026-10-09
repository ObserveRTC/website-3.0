---
slug: "detectors"
title: "Server detectors"
description: "Correlate evidence across clients or calls with explicit registration."
lead: "Correlate evidence across clients or calls with explicit registration."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 70
toc: true
---

Server detectors compare evidence across participants or calls. They help answer questions a browser alone cannot answer, such as whether one publisher is failing for several receivers. Register the detectors relevant to your service; they do not run automatically on a new Observer.

| Scope | Classes | Evidence / purpose |
|---|---|---|
| Call | `CallConcurrentIssueDetector` | active issue prevalence and onset bursts within one call |
| Call | `IssueFanOutDetector` | same publisher-associated failure appears across receivers |
| Call | `PublisherFaultCorroborationDetector` | publisher-side issues corroborated by receiver degradation/issues |
| Call | `TrackDeliveryMismatchDetector` | publisher/receiver delivery disagreement with resolved track links |
| Call | `UnconsumedTrackDetector` | outbound track has no known consumer after configured grace; requires a resolver |
| Observer | `ObserverConcurrentIssueDetector` | same issue spans independent calls / synchronized onsets |
| Observer | `SfuCongestionDetector` | correlated infrastructure/SFU degradation, consumes client issues |
| Observer | `ClientPopulationIssueDetector` | group client issues by browser/OS/location or supported axis |
| Observer | `TurnServerHealthDetector` | group current client findings around relays |
| Observer | `TurnServerOutageDetector` | detect relay outage patterns across clients |
| One-shot validation | `SimulcastReceiverValidator` | whether receivers select layers independently |
| One-shot validation | `RemoteTrackResolverValidator` | whether remote publisher/subscriber linkage can be established |
| One-shot validation | `CodecConsistencyValidator` | cross-end codec consistency / deployment behavior |

Exact configs/defaults, state and triggers for all server detector classes are in the [detector reference](/reference/detector-implementation-reference.md). Configurations and defaults are defined in each detector constructor. See [Validators](/docs/observer-js/validators/) for one-shot structural checks.

{{< details "Source references" >}}

- [observer-js/src/validators/Validators.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/validators/Validators.ts)
- [observer-js/src/validators/Validator.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/validators/Validator.ts)
- [observer-js/examples/detectors.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/examples/detectors.ts)

{{< /details >}}

## Registration scope

- `observer.addObserverDetector(...)` registers observer-wide analysis.
- `observer.addCallDetector(...)` registers a factory for future calls.
- `call.addDetector(...)` registers on an existing call.

Constructor configurations belong to each detector. Do not assume a default enabled set or a shared `DetectorsConfig` module.
