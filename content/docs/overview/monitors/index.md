---
title: "Monitors"
date: 2021-04-01
lastmod: 2021-04-01
draft: false
images: []
menu:
  docs:
    parent: "overview"
weight: 1040
images: ["monitors.png"]
toc: false
---

{{< img-simple src="monitors.png" alt="Overview" >}}

Monitors are client-side components in ObserveRTC architecture. Typically implemented as a library 
embedded into media units such as webrtc applications running in browser or in a SFU controller.
A monitor collect measurements from a media unit. The collected measurements can be used locally 
on the application the monitor runs, or can send [samples](/docs/overview/schemas/#samples) to the 
observer for further analysis.

Currently the following Monitor components available:
 * [Client-Monitor](/docs/client-monitor) for webrtc frontend applications running in browsers
 * [Sfu-Monitor](/docs/sfu-monitor) for selective forwarding units
