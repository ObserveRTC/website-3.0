---
contributors: {'Balázs Kreith'}
title: "Client Monitor"
date: 2021-07-09 06:27:48
lastmod: 2021-11-30 07:42:32
draft: false
images: []
menu:
  docs:
    parent: "client-monitor"
weight: 2005
toc: false
images: ["client-monitor.png"]
---

{{< img-simple src="client-monitor.png" alt="Client Monitor" >}}

Client Monitor is a front-end component runs in browsers. It collects [webrtc stats](https://www.w3.org/TR/webrtc-stats/), 
and metadata from client applications.

### Javascript library

[client-monitor-js](https://github.com/ObserveRTC/client-monitor-js) is a javascript library written 
for monitoring webrtc applications running in browsers. For an example of the integration of the library take a look [here](https://github.com/ObserveRTC/full-stack-examples/tree/main/my-webrtc-app)