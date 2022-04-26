---
contributors: {'Balázs Kreith'}
title: "Object hierarchy"
date: 2021-07-09 06:27:48
lastmod: 2022-04-25
draft: false
images: []
menu:
  docs:
    parent: "observer"
weight: 4020
toc: false
images: ["object-hierarchy.png"]
---

{{< img-simple src="object-hierarchy.png" alt="Object hierarchy" >}}

The elements of the object hierarchy are the following:

 * **Service** is the top level object identify the owner the provided media service belongs to.
 * **Room** is a virtual place clients share to exchange media contents. 
   Clients are in the same Room under the same Service participating in the same call. 
 * **Call** identifies a group of clients exchange media contents at the same time in the same room under the same service.
 * **MediaUnit** hold information clients and SFUs can arbitrary add in the samples. 
   For example, it can be the webrtc app version in the client side, 
   and the geographic region and availability zone in the SFUs side.
 * **Client** uses the WebRTC app provides the ClientSamples
 * **PeerConnection**s are established by the client to another client or to an SFU.
 * **MediaTrack**s are used by the peer connection to send out or receive in media contents.
 * **SFU** or Selective Forwarding Units are server side components to compound and distribute media contents between 
   several participants.
 * **SfuTransport** are the peer connection established by the SFU with either a client or with another SFU / media service.
 * **SfuRtpPad**s are used by the SfuTransports to send out or receive in media contents using RTP transport protocol.
