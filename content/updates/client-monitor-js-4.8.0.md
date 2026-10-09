---
title: "Client Monitor 4.8.0"
date: "2026-08-31T10:28:33Z"
draft: false
project: "Client Monitor"
version: "4.8.0"
summary: "Transport observability, DTLS handshake detection, and ClientSample 3.7.0 with nested payloads and metadata sent on change."
releaseUrl: "https://github.com/ObserveRTC/client-monitor-js/releases/tag/4.8.0"
author: "balazskreith"
---
Transport observability. Three themes: the RTP → transport → candidate-pair graph is fully traversable and attributed by one rule, DTLS handshake failure finally has an owner, and samples stop repeating constants (sample schema 3.7.0).

## Wire / payload changes — schema ClientSample 3.7.0

Payloads may nest. `ClientEvent.payload`, `ClientIssue.payload`, `ClientMetaData.payload` and `ExtensionStat.payload` accept nested structures (Record<string, unknown>), not only flat records of primitives — still records on the wire, never pre-serialised JSON strings. `ClientPayload` widened accordingly; `ClientPayloadValue` is removed (it named the flat-only constraint).

`PEER_CONNECTION_ICE_PATH_CHANGED` carries structured from/to. The path evidence travels as records now that the schema allows nesting; before 3.7.0 the two fields were JSON documents in strings. Consumers parsing them with `JSON.parse` must read them as objects instead.

`IceTransportStats` static members ship on change only. `iceRole`, `iceLocalUsernameFragment`, `localCertificateId`, `remoteCertificateId`, `tlsVersion`, `dtlsCipher`, `dtlsRole` and `srtpCipher` are constant after the DTLS handshake, so they appear in a transport's first sample and again only when a value changes — the ufrag changing is exactly an ICE restart, a change worth shipping. Consumers keep the last seen value per transport id; absence means "unchanged", not "unknown". `sendIceTransportMetadataOnChangeOnly`: false restores every-sample emission. Dynamic members (`iceState`, `dtlsState`, `selectedCandidatePairId`, `selectedCandidatePairChanges`, byte/packet counters) are unchanged.

Two new issues: dtls-handshake-failed and dtls-handshake-stalled (see the detector below), in the `ClientMonitorIssue`/`ClientMonitorResolvedIssue` unions and the `isClientMonitorIssue` guard.

`LONG_PC_CONNECTION_ESTABLISHMENT` says where setup is stuck. The event payload gains `stalledStage` ('ice-gathering' | 'ice-checking' | 'dtls' | 'unknown') plus the most severe transport's `iceState`/`dtlsState` and the pc's `iceGatheringState` — `connectionState`: 'connecting' covers ICE and DTLS alike, and until now the event could not tell a STUN desert from a certificate problem.

unstable-ice-path payload gains `nativePairChanges` — how many switches the browser's own counter saw inside the window, which can exceed the observed transition count (see below).

Firefox < 153 reconstructed transport counter is spec-aligned. `selectedCandidatePairChanges` now counts the first selection as 1, matching the native counter's "going from no selected pair to having one also increments" semantics; it previously landed on 0.

## New: DtlsHandshakeDetector

Separates "the network path failed" (the ICE detectors' territory) from "the secure media transport never negotiated", which nothing owned: a certificate fingerprint mismatch, DTLS version intolerance, or a middlebox that passes STUN but eats DTLS all presented as a generically slow connecting. `dtlsState`: 'failed' raises dtls-handshake-failed immediately; ICE proven healthy while DTLS sits in new/connecting past `stalledThresholdInMs` (default 6000) raises dtls-handshake-stalled. ICE health comes from the transport's `iceState` where the browser reports one, and from the selected pair being succeeded where it does not (Safari, and the transport reconstructed for Firefox < 153) — the payload's `iceEvidence` names which proof was used. Never judges a transport on its first observed tick (Firefox 153/154 report pre-negotiation values that only 155 makes trustworthy), never treats closed as a failure, and restarts its stall timer when the ufrag changes. Config: `dtlsHandshakeDetector`, null to disable.

## One attribution rule for RTP → transport

`attributeRtpToTransport` (utils) / `PeerConnectionMonitor.attributeRtpToTransport()` is now the single rule mapping RTP streams onto a transport: exact `transportId` match, and streams carrying no `transportId` belong to a transport only when it is the pc's sole transport — exact under BUNDLE, never double-counted without it.

`BlockedTransportDetector` and `MediaPipelineDetector` both use it. They previously disagreed: the pipeline detector's permissive filter counted a `transportId`-less inbound stream against every transport of a non-BUNDLE connection, so one quiet stream could raise media-pipeline-stalled on two transports at once.

The traversal graph is complete: `getIceTransport()` and `getSelectedCandidatePair()` on all four RTP monitors (only the inbound one could traverse before), and `getSelectedIcePath()` on `IceTransportMonitor` — any stream can now answer "is this on TURN?" in two hops.

## Selected-pair churn is counted from the browser

`IceTransportMonitor.deltaSelectedCandidatePairChanges` differences the native `selectedCandidatePairChanges` counter (Chrome 80+, Firefox 155+; absent on Safari). Counted only once the transport already had a selection, so the first selection is never churn; a backwards counter reads as a reset, not as movement.

unstable-ice-path uses the larger of observed transitions and the native delta. The path diffing in `SelectedIcePath` remains the classifier and the only portable signal, but it is tick-to-tick and structurally blind to a flap that departs and returns within one collecting period — the native counter sees it. An inferred ICE restart clears the native tally and suppresses the next ticks, so a restart's own reselection never counts.

## Fixed

Peer-connection `iceState` is the most severe state across its transports, not whatever transport happened to be listed first — a failed transport is no longer masked by a healthy sibling on a non-BUNDLE connection. Severity: failed > disconnected > checking > new > connected > completed > closed.

The never-established restart recommendation reports the most severe transport instead of the first one, for the same reason.

---

Source: [GitHub release 4.8.0](https://github.com/ObserveRTC/client-monitor-js/releases/tag/4.8.0). Published at 2026-08-31T10:28:33Z (UTC).
