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

`RemoteTrackResolver` connects publishers/subscribers across client boundaries. The mediasoup factory reads producerId/consumerId in track attachments. The P2P factory joins SSRC-derived identifiers and documents its single-encoding assumption. Generic SFUs need an explicit resolver factory based on their signaling IDs; schema IDs alone do not guarantee end-to-end association. [observer-js/src/resolvers/RemoteTrackResolver.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/resolvers/RemoteTrackResolver.ts), [observer-js/src/resolvers/RemoteTrackResolverFactories.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/resolvers/RemoteTrackResolverFactories.ts).

`ObservedMediasoupRouter` attaches to a real router and accumulates a separate `MediasoupRouterSample`; it observes server transports, producers/consumers and their lifecycle, and correlates a router's transport with client PCs. This is not the archived sfu-monitor-js API and not a ClientSample array. The application decides when to persist the growing router sample. The demo writes it beside call summaries and client streams, and injects routerId upon matching. [observer-js/src/ObservedMediasoupRouter.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedMediasoupRouter.ts), [observer-js/src/schema/MediasoupRouter.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/schema/MediasoupRouter.ts), [observer-js/examples/sfu-observer.ts](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/examples/sfu-observer.ts), [webrtc-observer.org/src/observer.ts](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/src/observer.ts).
