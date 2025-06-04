---
contributors: {'Balázs Kreith'}
title: "Object hierarchy"
date: 2021-07-09 06:27:48
lastmod: 2022-04-25
draft: false
images: []
menu:
  docs:
    parent: "overview"
weight: 1030
toc: false
images: ["object-hierarchy.png"]
---

{{< img-simple src="object-hierarchy.png" alt="Object hierarchy" >}}

The elements of the object hierarchy are as follows:

 * **Service** is the top-level object that identifies the owner of the provided media service.
 * **Room** is a virtual space where clients share and exchange media content. Clients in the same room under the same service participate in the same call.
 * **Call** identifies a group of clients exchanging media content at the same time in the same room under the same service.
 * **MediaUnit** holds information that clients and SFUs can arbitrarily add in the samples. For example, it can be the WebRTC app version on the client side, and the geographic region and availability zone on the SFUs side.
 * **Client** uses the WebRTC app to provide ClientSamples.
 * **PeerConnection**s are established by the client to another client or to an SFU.
 * **MediaTrack**s are used by the peer connection to send out or receive media content.
 * **SFU** or Selective Forwarding Units are server-side components that compound and distribute media content between several participants.
 * **SfuTransport** are the peer connections established by the SFU with either a client or with another SFU/media service.
 * **SfuRtpPad**s are used by the SfuTransports to send out or receive media content using the RTP transport protocol.

