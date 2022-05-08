---
contributors: {'Balázs Kreith', 'Chad Hart'}
title: "Architecture"
date: 2021-11-27 18:00:13
lastmod: 2021-01-02
draft: false
menu:
  docs:
    parent: "overview"
weight: 1020
toc: false
images: ["superficial-overview.png"]
---

{{< img-simple src="superficial-overview.png" alt="Overview" >}}

ObserveRTC is a full stack monitoring solution for WebRTC applications. The solution can be divided into two parts: 
 * [Monitors](/docs/overview/monitors/) to collect measurements from a media component such as a front-end WebRTC application, or a server-side Selective Forwarding Units (SFUs).
 * [Observer](/docs/observer/overview/) to analyse Monitors provided [samples](/docs/overview/schemas/#samples). As a result the observer create [reports](/docs/overview/schemas/#reports). 

Samples and reports are part of a communication [schemas](/docs/overview/schemas/) describe the structure of the messages between services.

Monitors are co-existing with media components typically integrated through a library 
 such as [client-monitor-js](https://github.com/ObserveRTC/client-monitor-js) for front-end applications, or [sfu-monitor-js](https://github.com/ObserveRTC/sfu-monitor-js) for SFUs. When a monitor is integrated it collect measurements of a monitored media component. The collected measurements can be used locally by the application, 
and can be send to the [observer](https://github.com/ObserveRTC/observer) for further analysis.

The observer analyse the monitors provided [samples](/docs/overview/schemas/#samples). Based on the analysis it can:
 * Identify calls
 * Create events (call started, call ended, client joined, client left, etc.)
 * Match clients' inbound-rtp sessions with remote clients' outbound-rtp sessions
 * Match SFUs RTP sessions with browser-side clients' in-, and outbound-rtp sessions.

Observer create [reports](schemas/#reports). Reports have different types. The type of the report indicate the information it carries.
Currently the following type of reports are created:
 * **Call Event Reports**: Call related events (call started, call ended, client joined, client left, etc.)
 * **Call Meta Reports**: Descriptive information about calls or clients (Client codecs, media devices, ICE candidates, etc.)
 * **Client DataChannel Reports**: Measurements of data channels of a peer connection belongs to a client
 * **Client Extension Reports**: Arbitrary information provided by a client-side application
 * **Client Transport Reports**: Measurements of peer connection belogns to a client
 * **Inbound AudioTrack Reports**: Measurements of a Media Track receives audio content from a remote client
 * **Inbound VideoTrack Reports**: Measurements of a Media Track receives video content from a remote client
 * **Outbound AudioTrack Reports**: Measurements of a Media Track sending audio content to a remote client
 * **Outbound VideoTrack Reports**: Measurements of a Media Track sending video content to a remote client
 * **Sfu Event Reports**: SFU related events (SFU joined, SFU detached, Transport opened, Transport closed, etc.)
 * **Sfu InboundRtpPad Reports**: Measurements of an incoming RTP session traffics
 * **Sfu OutboundRtpPad Reports**:  Measurements of an outgoing RTP session traffics
 * **Sfu SctpStream Reports**: Measurements of an SCTP session traffics
 * **Sfu Transport Reports**: Measurements of network traffic between an SFU and an endpoint
 <!-- * [Sfu Meta Reports](): Descriptive information about SFUs () -->
 <!-- * [Observer Event Reports](): Observer detected events. -->

Reports can be sent for further processing. 
Currenly the following integration is implemented in Observer to send Reports forward:
 * [KafkaSink](https://github.com/ObserveRTC/observer#kafkasink): Apache Kafka Integration
 * [MongoSink](https://github.com/ObserveRTC/observer#mongosink): Mongo Database integration
