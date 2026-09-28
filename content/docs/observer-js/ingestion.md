---
slug: "ingestion"
title: "Ingestion & lifecycle"
description: "Validate at your boundary, then pass samples to Observer."
lead: "Validate at your boundary, then pass samples to Observer."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 10
toc: true
---

`Observer.accept(sample, context?)` is synchronous. The current implementation invokes acceptMiddlewares, validates nonempty call/client IDs, gets or creates a call/client and calls `ObservedClient.accept()`. It does not perform full Avro validation, automatic codec decoding or client-side detector execution. The middleware implementation has a reproduced drop/replacement bug described below.

`ObservedClient.accept` resets interval aggregates, normalizes score reason wire generations, merges pending injections, processes events/meta/issues/extensions, updates PCs, processes deferred events, sets attachments and sampled client score, emits update events, resets idle timeout and writes the final sample to a sink. Client-level bitrate uses **server wall-clock arrival interval**, so replaying historical samples rapidly is not equivalent to the browser stats cadence. Per-RTP entities retain their own stat processing rules. [observer-js/src/Observer.ts · accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts#L710), [observer-js/src/ObservedClient.ts · accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts#L217), [observer-js/src/common/utils.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/common/utils.ts).

PC accept handles the same stat families as its arrays, creates or updates `Observed*` entities, derives per-interval/cumulative counters, selects transports and cleans unvisited children. RTP maps commonly use SSRC, tracks use track ID, other objects use stat ID. Parent scopes are included on the central Observer bus; local emitters coordinate internals. State is live and removable; it is not a database. [observer-js/src/ObservedPeerConnection.ts · accept](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedPeerConnection.ts#L317), [observer-js/src/ObserverEvents.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObserverEvents.ts), [observer-js/src/ObservedInboundRtp.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedInboundRtp.ts), [observer-js/src/ObservedOutboundRtp.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedOutboundRtp.ts).

`ObservedClient.activeIssues` mirrors keyed client lifecycle records. A raise gets both client-clock `raisedAt` and server-clock `observedAt`; cross-client onset comparisons must use the latter. Same-key re-raise refreshes payload; keyless records are one-shot. A `-resolved` record retires the key and emits resolution. Client close resolves outstanding state. Registries propagate into call and observer scopes, enabling cross-client queries without walking every healthy client. [observer-js/src/issues/ObservedClientIssueRegistry.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/issues/ObservedClientIssueRegistry.ts), [observer-js/src/issues/ActiveIssuesRegistry.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/issues/ActiveIssuesRegistry.ts), [observer-js/src/ObservedClient.ts · addIssue](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts#L534).

Server defaults: automatic observer update on call updates, 60 s idle client timeout, 60 s empty-call timeout. Passing explicit undefined through config disables those timeout defaults because config is spread after defaults. Call summaries are absent unless configured. Detector registries start **empty**. Register observer-wide detectors with `addObserverDetector`, future-call detectors with `addCallDetector`, and an existing call's detector with `call.addDetector`. Removal semantics and duplicate-name instances differ from a unique-name client registry. [observer-js/src/Observer.ts · constructor](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts#L331), [observer-js/src/Observer.ts · addCallDetector](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts#L418), [observer-js/src/detectors/Detectors.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/detectors/Detectors.ts).


## Middleware limitation in 1.0.0

The inspected `accept()` implementation dispatches the original sample after invoking middleware. Not calling `next()`, throwing, or forwarding a replacement object does **not** reliably drop or replace that sample. In-place mutation of the original object is a different case.

Filter and validate **before calling `observer.accept()`**. Do not use its middleware as an authorization boundary. This behavior was reproduced against the pinned source; it disagrees with repository documentation.

[Known differences and reproduction results](/docs/reference/known-differences/)
