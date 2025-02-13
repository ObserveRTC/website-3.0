---
contributors: {'Balázs Kreith'}
title: "Observer"
date: 2021-07-09 06:27:48
lastmod: 2022-04-25
draft: false
images: []
menu:
  docs:
    parent: "overview"
weight: 1060
toc: true
images: ["observer.png"]
---

{{< img-simple src="observer.png" alt="Observer" >}}

The observer accept and evaluate the provided [samples](/docs/overview/schemas/#samples) from monitors and can do the followings:
 * Aggregate or analyze calls, clients, peer connections, tracks, sfus, etc.
 * Create Reports for each provided sample for savings
 * Emit events in the server application to do further actions (call started, call ended, client joined, client left, etc.)
