---
title: "Observer 1.1.0"
date: "2026-09-29T17:57:12Z"
draft: false
project: "Observer"
version: "1.1.0"
summary: "Public client and peer-connection IP addresses, address-change events, and selected candidate-pair change reporting."
releaseUrl: "https://github.com/ObserveRTC/observer-js/releases/tag/1.1.0"
author: "balazskreith"
---
## Public address of clients and peer connections (new)

The internet-facing IP of a client is now derived from the ICE candidates it already reports.

`ObservedPeerConnection.publicAddress` / `publicAddressUpdatedAt`: taken from the local candidate of the selected pair (address for srflx / prflx / public host, `relatedAddress` for relay), falling back to the local candidates of any reported pair. Only public IP literals count; private, CGNAT, link-local, `mDNS` .local and redacted 0.0.0.0 addresses are skipped.

`ObservedClient.publicAddress` (the most recently changed PC's address) and `ObservedClient.publicAddresses` (distinct addresses of the open PCs).

New events: `peer-connection-public-address-changed` and `client-public-address-changed`, both { `publicAddress`, `previousPublicAddress`? }. Values are sticky: they never change back to undefined, so a closing peer connection does not fire them.

`isPublicIpAddress(address)` is exported.

## selected-candidate-pair-changed now fires

It was declared in `ObserverEvents` but never emitted. It now fires when an ICE transport's `selectedCandidatePairId` changes (first selection, switch, or deselection), after the whole peer-connection sample is applied. The payload gains { `observedIceTransport`, `observedIceCandidatePair`?, `previousCandidatePairId`? }. `ObservedIceTransport` exposes `selectedCandidatePairChanged` and `previousSelectedCandidatePairId`.

## Event fixes (from an audit of every event in ObserverEvents)

- `peer-connection-closed` now fires when the client closes a peer connection. A `PEER_CONNECTION_CLOSED` client event used to set only `closedAt`; the peer connection stayed open (and counted, and registered on its TURN server) until the whole client closed. It is now closed once the sample that carried the event is applied. Stats that arrive later for the same id are ignored and do not re-create it.

- `certificate-removed` was never emitted when a certificate stopped being reported. It is now.

- `certificate-updated` now fires on every tick the certificate is reported, the first one included, like every other sub-stat -updated event.

- `client-event` fired twice for events that had to wait for a peer connection created in the same sample (`PEER_CONNECTION_OPENED`, `MEDIA_TRACK_ADDED`, …). It now fires once.

- `inbound-track-muted` / outbound-track-muted / -unmuted were dropped silently when the peer connection existed but the track arrived in the same sample as the event. The event now waits for the track like the others do.

- `call-empty` no longer fires while the call itself is closing. It also no longer re-arms the empty-call timer on a call that is already closed.

- `client-extension-stats` is no longer emitted by `addExtensionStats()` on a closed client.

## Other fixes

`ObservedPeerConnection.deltaDataChannelMessagesSent` / `deltaDataChannelMessagesReceived` were never reset per tick and grew without bound. They are now per-tick deltas as documented.

---

Source: [GitHub release 1.1.0](https://github.com/ObserveRTC/observer-js/releases/tag/1.1.0). Published at 2026-09-29T17:57:12Z (UTC).
