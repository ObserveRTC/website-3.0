---
slug: "sfu"
title: "SFU & mediasoup integration"
description: "Resolve track relationships from signaling, then add router observation if needed."
lead: "Resolve track relationships from signaling, then add router observation if needed."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 60
toc: true
---

An SFU receives a publisher’s media and forwards it to subscribers. Browser statistics describe each endpoint separately. To relate a receiver’s video to the publisher that sent it, Observer needs identifiers from your signaling layer.

## Publisher and receiver relationships

`RemoteTrackResolver` connects publishers/subscribers across client boundaries. The mediasoup factory reads `producerId`/`consumerId` in track attachments. The P2P factory joins SSRC-derived identifiers and documents its single-encoding assumption. Generic SFUs need an explicit resolver factory based on their signaling IDs; schema IDs alone do not guarantee end-to-end association.

{{< details "Source references" >}}

- [observer-js/src/resolvers/RemoteTrackResolver.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/resolvers/RemoteTrackResolver.ts)
- [observer-js/src/resolvers/RemoteTrackResolverFactories.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/resolvers/RemoteTrackResolverFactories.ts)

{{< /details >}}

## Mediasoup router observation

`ObservedMediasoupRouter` attaches to a real router and accumulates a separate `MediasoupRouterSample`; it observes server transports, producers/consumers and their lifecycle, and correlates a router's transport with client PCs. This is not the archived sfu-monitor-js API and not a `ClientSample` array. The application decides when to persist the growing router sample. [observer-js/src/ObservedMediasoupRouter.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedMediasoupRouter.ts), [observer-js/src/schema/MediasoupRouter.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/schema/MediasoupRouter.ts), [observer-js/examples/sfu-observer.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/examples/sfu-observer.ts).
