---
slug: "sampling"
title: "Collection & sampling"
description: "Follow the update lifecycle and understand the sample boundary."
lead: "Follow the update lifecycle and understand the sample boundary."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 40
toc: true
---

1. `RtcPeerConnectionStatsCollector.getStats()` calls the real browser API; `convertRTCStatsReport()` keeps reports with id, timestamp and type. Mediasoup has its own collector and bindings. Bind a device before transports are created, or attach existing transports explicitly.
2. PC adapters run before dispatch. Chromium folds legacy fields and infers missing references. Safari additionally normalizes old data-channel IDs and pair-state spellings. Firefox can reconstruct a missing transport from its selected candidate pair, maintaining totals across pair changes. Inferred/reconstructed values must be labeled separately from browser-native measurements.
3. PC accept calculates `deltaTime` from successive maximum stats timestamps, resets PC aggregates, dispatches reports with a retry pass for unresolved ordering, updates references/path state, then runs PC and ICE-transport detectors.
4. Root collection aggregates PCs, feeds its window, updates tracks and their detectors, runs root detectors, updates scores, expires extension monitors, emits `stats-collected`, and possibly emits a sample.
5. Collection defaults to 5000 ms. Sampling defaults to 5000 ms and is collection-count-driven: `max(1, floor(samplingPeriod/collectingPeriod))`. A non-integral ratio warns and floors. Zero disables the relevant automatic mechanism. `createSample()` remains callable manually. A sample contains current stat snapshots and buffered discrete records; it is not a time average of all intervening monitor values.
6. `close()` tears down sources/timers, resolves lifecycle state, optionally records departure and emits a final sample before closing. Opt-in pre-subscriber buffering preserves samples until the first subscriber; it is off by default.
7. Stable 4.9.1 retains live track-associated RTP/source monitors over an omitted report and cleans up ended/pending tracks; the site's 4.9.0 dependency predates those fixes.

Sources: [client-monitor-js/src/collectors/RtcPeerConnectionStatsCollector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/collectors/RtcPeerConnectionStatsCollector.ts), [client-monitor-js/src/collectors/MediasoupTransportStatsCollector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/collectors/MediasoupTransportStatsCollector.ts), [client-monitor-js/src/adapters/ChromeStatsAdapter.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/adapters/ChromeStatsAdapter.ts), [client-monitor-js/src/adapters/FirefoxStatsAdapter.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/adapters/FirefoxStatsAdapter.ts), [client-monitor-js/src/adapters/SafariStatsAdapter.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/adapters/SafariStatsAdapter.ts), [client-monitor-js/src/monitors/PeerConnectionMonitor.ts · _acceptAdaptedStats](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/PeerConnectionMonitor.ts#L618), [client-monitor-js/src/ClientMonitor.ts · _setSamplingTick](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1219), [client-monitor-js/CHANGELOG.md](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/CHANGELOG.md).

## Wire projection

A `createSample()` call drains buffered events, issues, metadata and extension entries. It does not serialize every live property, nor average all collection intervals. [See the schema mapping](/docs/schema/clientsample/).

When automatic sampling is disabled, set `bufferingEventsForSamples: true` if manual samples must include discrete records. Otherwise events and metadata return before buffering; local issue emission is independent.
