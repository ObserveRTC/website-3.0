---
title: "Observer 1.2.0"
date: "2026-10-13T19:54:49Z"
draft: false
project: "Observer"
version: "1.2.0"
summary: "Client session totals, RTT and score histograms, call-level audio echo detection, and richer audio evidence."
releaseUrl: "https://github.com/ObserveRTC/observer-js/releases/tag/1.2.0"
author: "balazskreith"
---

## Summarize a client's whole session

`ObservedClient` accumulates RTT and score histograms, issue-raise counts, traffic totals, path sample counts, address changes, and peak bitrates. Totals survive peer connection closure. Cached `rttSummary` and `scoreSummary` expose percentiles and averages. Score measurements now include zero.

**Breaking API change:** `deltaRttLt50Measurements`, `deltaRttLt150Measurements`, `deltaRttLt300Measurements`, and `deltaRttGtOrEq300Measurements` are removed. Use `rttHistogram` instead. `percentileOfHistogram()` supports aggregation across compatible client histograms.

## Detect suspected audio echo

The call-scoped `AudioEchoDetector` raises `AUDIO_ECHO_SUSPECTED` when a participant's outgoing audio follows another participant's voice with sufficient activity overlap and level correlation. Register it through `observer.addCallDetector('audio-echo-detector')` or `call.addDetector('audio-echo-detector')`.

The payload carries track/client identities, evidence, capture-device context when available, and the related loopback-input issue state. Sampling granularity limits faint/intermittent echo detection; this finding remains a suspicion to investigate.

## Inspect audio levels and capture context

Inbound RTP audio level, energy, and sample-duration fields are populated, with per-tick deltas and RMS levels. Media sources expose matching deltas; outbound tracks provide source/receiver-derived levels and capture-device context. `AUDIO_INPUT_DEVICE` metadata populates `ObservedClient.audioInputDevices`. The release describes this metadata producer as Client Monitor JS next; older clients need not supply it.

See [session and audio evidence](/docs/observer-js/entities/), [server detectors](/docs/observer-js/detectors/), and the [compatibility matrices](/docs/reference/versions/) for current integration guidance.

Source: [Observer 1.2.0 release notes](https://github.com/ObserveRTC/observer-js/releases/tag/1.2.0). Date is GitHub's release publication timestamp.
