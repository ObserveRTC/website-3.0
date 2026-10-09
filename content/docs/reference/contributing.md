---
slug: "contributing"
title: "Where to implement a change"
description: "Follow a field or behavior through its owning layers."
lead: "Follow a field or behavior through its owning layers."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "Markdown"]
weight: 40
toc: true
---

## Choose the owning layer

| Change | Implementation and verification path |
|---|---|
| New browser field | W3C/schema definitions if appropriate → schema generation → synchronized generated types → owner monitor assignment + `createSample` → observer entity update → browser-availability tests |
| New local derived metric | owner monitor accept/update/getter; reset/missing/stale semantics; raw→derived unit/formula metadata; tests for counter reset, no progress and missing input; serialize only if backend needs the value itself |
| New client detector | Detector class with category/layer, config type, constructor defaults, correct owner registration, event payload/type, issue union, source tests/taxonomy test; independently define trigger/recovery and unavailable behavior |
| New score behavior | `DefaultScoreCalculator` and relevant monitor readings; component reasons and root aggregation kept distinct; verify absence/zero/continuous reason visibility |
| New schema field | authoritative Avro/chunk, source version/changelog, generator outputs/packages, both consumer copies, codec roundtrips and compatibility tests |
| New server entity behavior | appropriate Observed*.update/accept, `ObserverEvents` typed scope, lifecycle cleanup, metric reset semantics, focused source tests |
| New server detector | class + `AvailableCallScope`/`ObserverScopeDetectorsConfigs` + appropriate `addDetector` factory switch + index exports; explicit application registration |
| New structural validation | Validator + `AvailableValidatorConfigs` + `Observer.addValidator` switch; evidence-backed positive/negative/inconclusive behavior |
| New SFU integration | application signaling/attachments → `RemoteTrackResolverFactory`; optional server object observer; no guessed publisher linkage |

## Verification

Client Monitor: `tests/monitors/DerivedFields.spec.ts`, `UnreportedRoundRecovery.spec.ts`, `EndedTrackStandDown.spec.ts`, `RemoteRtcpReportStaleness.spec.ts`, detector-specific specs and `DetectorTaxonomy.spec.ts`, scoring specs

Observer: `acceptMiddleware.spec.ts`, `issueLifecycle.spec.ts`, `payloadWireGenerations.spec.ts`, `injection.spec.ts`, `RemoteTrackResolver.spec.ts`, `mediasoupRouter.spec.ts`, `callSummary.spec.ts`

Schema: JSON/protobuf codec roundtrip/delta/nested-payload/error tests.
