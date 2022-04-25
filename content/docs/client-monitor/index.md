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

Client Monitor is embedded to the front-end application runs in the browser. Based on the configuration the monitor applied, 
it polls [webrtc stats](https://www.w3.org/TR/webrtc-stats/) periodically and provide interfaces to process the stats.

### Javascript library

[https://github.com/ObserveRTC/client-monitor-js](https://github.com/ObserveRTC/client-monitor-js) is a javascript written 
to monitor webrtc applications in the browser. An example of the integration of the library can be look [here](https://github.com/ObserveRTC/full-stack-examples/tree/main/my-webrtc-app)