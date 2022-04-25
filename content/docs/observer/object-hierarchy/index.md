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

Observer analyze incoming samples and build an internal object hierarchy stores in its repository. 
Object hierarchy is then used to group the client samples, matching tracks and sfu rtp pads, 
identify tracks' peer connections, SFU transports, etc... The identifiers 
revealed by the object hierarchy for the sample are assigned to the generated reports.
As a result, for example, all client related reports can be identified which call it belongs to.

The basic elements of the object hierarchy are the following:

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


## Use Cases

Let's make an example of how to use observer by following a story. In the example a company named `MyAwesomeTutorialForEveryoneExample` creates a webrtc based media service to provide tutorials all over the world.
The company develop a webrtc app called `my-webrtc-app`, and it is integrated to send samples to an observer.

### Observe peer to peer calls

The company provides `free-tutorials` media service through `my-webrtc-app` clients are actively using. 
The `my-webrtc-app` send [ClientSample]()s to the observer using a websocket endpoint `wss://observer.MyAwesomeTutorialForEveryoneExample.com/free-tutorials/my-webrtc-app-1-0-0`, where the `free-tutorials` is the serviceId, and `my-webrtc-app-1-0-0` is the webrtc app bundled with its current version. 

At 8am until 9am Alice and Bob enter to `cryptography` room using the link `https://www.MyAwesomeTutorialForEveryoneExample.com/cryptography`. While they are in the room `cryptography` observer collects the samples from both client and the generated reports forwarded by the observer contains the same callId. Furthermore Alice's outbound video and audio tracks are matched with Bob's inbound audio and video tracks from Alice, and the generated report contains the trackId which remote client id and track the inbound track belongs to.

### Observe multitenant calls

Your company wants to provide tutorials for a group of people and not just 1:1 sessions. You setup an SFU, with what your comapny is able to do a call with multiple participant. With no changes to the ClientSample creation setup for the p2p calls, the observer is able to match calls in the same room under the same service, but to match the tracks ClientSample Outbound-, and Inbound Audio, and Video calls must set the `rtpStreamId` UUID to match between tracks. this id is provided by the SFU client SDK and you should get it through a signal server. When this information is added observer can match the tracks just before to the p2p calls.


### Observe SFUs

Further going with monitoring, observer is able to accept samples from SFUs integrated to provide [SfuSample]()s. When an SFU sending samples to the observer, the observer is able to match SFU provided samples with client samples and generated reports for the SFU contains the callId an SfuRtpPad is opened for (using the matching `rtpStreamId`).

### Observe multiple services

Your company wants to provide paid tutorials for clients but using the same `my-webrtc-app`. In this case the only difference is the serviceId for the observer reported through the `my-webrtc-app`, which should be different than the previously used `free-tutorials`. 