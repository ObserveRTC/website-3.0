---
title: "Monitors"
date: 2021-04-01
lastmod: 2021-04-01
draft: false
images: []
menu:
  docs:
    parent: "overview"
weight: 1050
images: ["monitors.png"]
toc: true
---

{{< img-simple src="monitors.png" alt="Overview" >}}

In ObserveRTC architecture monitors are designed to monitor RTC component and create Samples. 

Typically implemented as a library 
embedded into media units such as webrtc applications running in browser or in a SFU controller.
A monitor collect measurements from a media unit. The collected measurements can be used locally 
on the application the monitor runs, or can send [samples](/docs/overview/schemas/#samples) to the 
observer for further analysis.

## Client Monitor

{{< img-simple src="client-monitor.png" alt="Overview" >}}

Client Monitor is a front-end component runs in browsers. It collects webrtc stats, and metadata from client applications.

**Implementations**:

* [client-monitor-js]() 



## SFU Monitor

{{< img-simple src="sfu-monitor.png" alt="SFU Monitor" >}}

Sfu-Monitor is a backend component runs with the selective forwarding unit. 

### Implementations

[sfu-monitor-js](https://github.com/ObserveRTC/sfu-monitor-js) is a javascript library written 
for monitoring selective forwarding units. 