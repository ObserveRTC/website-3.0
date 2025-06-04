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
 * [Monitors](/docs/overview/monitors/) to collect measurements from a media component such as a front-end WebRTC application or server-side Selective Forwarding Units (SFUs).
 * [Observer](/docs/observer/overview/) to analyze Monitors provided [samples](/docs/overview/schemas/#samples). As a result, the observer creates [reports](/docs/overview/schemas/#reports).

Samples and reports are part of a communication [schemas](/docs/overview/schemas/) that describe the structure of the messages between services.

Monitors coexist with media components and are typically integrated through a library,
 such as [client-monitor-js](https://github.com/ObserveRTC/client-monitor-js) for front-end applications or [sfu-monitor-js](https://github.com/ObserveRTC/sfu-monitor-js) for SFUs. When a monitor is integrated, it collects measurements of a monitored media component. The collected measurements can be used locally by the application, and can be sent to the [observer](https://github.com/ObserveRTC/observer) for further analysis.

The observer accept and evaluate the provided [samples](/docs/overview/schemas/#samples) and can do the followings:
 * Aggregate or analyze calls, clients, peer connections, tracks, sfus, etc.
 * Create Reports for each provided sample for savings
 * Emit events in the server application to do further actions (call started, call ended, client joined, client left, etc.)

Observer can create [reports](schemas/#reports). Reports have different types. The type of the report indicates the information it carries.
Currently, the following types of reports are created:
 * **Call Event Reports**: Call related events (call started, call ended, client joined, client left, etc.)
 * **Call Meta Reports**: Descriptive information about calls or clients (Client codecs, media devices, ICE candidates, etc.)
 * **Client DataChannel Reports**: Measurements of data channels of a peer connection belonging to a client
 * **Client Extension Reports**: Arbitrary information provided by a client-side application
 * **Client Transport Reports**: Measurements of peer connections belonging to a client
 * **Inbound AudioTrack Reports**: Measurements of a Media Track receiving audio content from a remote client
 * **Inbound VideoTrack Reports**: Measurements of a Media Track receiving video content from a remote client
 * **Outbound AudioTrack Reports**: Measurements of a Media Track sending audio content to a remote client
 * **Outbound VideoTrack Reports**: Measurements of a Media Track sending video content to a remote client
 * **Sfu Event Reports**: SFU related events (SFU joined, SFU detached, Transport opened, Transport closed, etc.)
 * **Sfu InboundRtpPad Reports**: Measurements of incoming RTP session traffic
 * **Sfu OutboundRtpPad Reports**: Measurements of outgoing RTP session traffic
 * **Sfu SctpStream Reports**: Measurements of SCTP session traffic
 * **Sfu Transport Reports**: Measurements of network traffic between an SFU and an endpoint
