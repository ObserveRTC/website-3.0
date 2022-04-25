---
contributors: {'Balázs Kreith'}
title: "SFU Monitor"
date: 2021-07-09 06:27:48
lastmod: 2021-11-30 07:42:32
draft: false
images: []
menu:
  docs:
    parent: "sfu-monitor"
weight: 3005
toc: false
images: ["sfu-monitor.png"]
---
{{< img-simple src="sfu-monitor.png" alt="SFU Monitor" >}}


SFU Monitor is embedded in the selective forwarding units. Based on the configuration the monitor applied, 
it collects measurements from the SFU and can send Samples to the observer.

## Javascript library

[https://github.com/ObserveRTC/sfu-monitor-js](https://github.com/ObserveRTC/sfu-monitor-js) is a javascript written 
to monitor webrtc applications in the browser. 

### Mediasoup integration

An example of a mediasoup integration can be looked [here](https://github.com/ObserveRTC/full-stack-examples/tree/main/mediasoup-sfu)