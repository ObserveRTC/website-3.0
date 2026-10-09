---
slug: "known-differences"
title: "Known implementation differences"
description: "Verified discrepancies to account for when building integrations."
lead: "Verified discrepancies to account for when building integrations."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "Markdown"]
weight: 30
toc: true
---

## Delta reset semantics

`DERIVED_METRICS` says zero; `positiveDelta` returns undefined. Source wins. Other consumers can explicitly coalesce; do not overgeneralize either direction.

## Outdated metric names

`DERIVED_METRICS` examples use `InboundRtpMonitor.fractionLost`, `isFreezed`, and `OutboundRtpMonitor.encodeTimePerFrameInMs`; the current relevant names are `deltaFractionLost`/`totalFractionLost`, track flow state, and `avgEncodeTimePerFrameInMs`. See field inventory.

## Pixelation explanation

`ClientMonitorConfig` prose still says `bitPerPixel`, while `PixelatedVideoDetector` uses `normalizedQp`.

## Audio synthesis taxonomy

The stable taxonomy describes `AudioPlayoutSynthesis` as event-only/missing issue; actual constructor binds an `InboundTrackMonitor` and raises synthesized-audio using playout counters through that track.

## Scoring prose

“open issues and nothing else,” “healthy/no issues always 5,” and root score becomes undefined with nothing measurable do not describe all actual paths. Continuous ramps and root early-return/default behavior contradict those statements.

## Observer AcceptContext comment

The comment says merged into `appData`; actual factories can consume it at creation, and it is otherwise transient event context. Current changelog/config text correctly explains the distinction.

## Observer middleware contract

Omitting `next()` does not stop ingestion; throwing logs “dropping” but still ingests; `next(newPayload)` does not replace the object dispatched. `Observer.accept` proceeds after `process()`, and no final callback controls dispatch. The existing middleware tests cover ordering/mutation/removal, not these advertised cases.

## On-change ICE compatibility

Client Monitor sends static ICE metadata first/on change by default; `ObservedIceTransport.update()` assigns absent metadata to undefined. Thus roles, certificate IDs and crypto fields disappear on ordinary later samples. This needs a receiver-side retention contract or explicit sender setting, not documentation alone.

## Zero score history

`ObservedClient` accepts score 0, but `if (this.calculatedScore.value)` skips its cumulative score measurement count. Current instantaneous score remains 0; historical counters omit that measurement.

{{< details "Source references" >}}

- [client-monitor-js/docs/DERIVED_METRICS.md](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/docs/DERIVED_METRICS.md)
- [client-monitor-js/src/utils/common.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/common.ts)
- [client-monitor-js/src/ClientMonitorConfig.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitorConfig.ts)
- [client-monitor-js/src/detectors/AudioPlayoutSynthesisDetector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/AudioPlayoutSynthesisDetector.ts)
- [client-monitor-js/docs/DETECTOR_TAXONOMY.md](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/docs/DETECTOR_TAXONOMY.md)
- [client-monitor-js/src/scores/DefaultScoreCalculator.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/scores/DefaultScoreCalculator.ts)
- [observer-js/src/Observer.ts · accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts#L710)
- [observer-js/src/common/Middleware.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/common/Middleware.ts)
- [observer-js/src/ObservedIceTransport.ts · update](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedIceTransport.ts#L53)
- [observer-js/src/ObservedClient.ts · accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts#L217)

{{< /details >}}

[Focused execution results](/reference/verification-results.json). These are source-snapshot findings, not claims about unexamined later releases.
