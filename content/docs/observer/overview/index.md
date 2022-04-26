---
contributors: {'Balázs Kreith'}
title: "Observer"
date: 2021-07-09 06:27:48
lastmod: 2022-04-25
draft: false
images: []
menu:
  docs:
    parent: "observer"
weight: 4010
toc: true
images: ["observer.png"]
---

{{< img-simple src="observer.png" alt="Observer" >}}

[Observer](https://github.com/ObserveRTC/observer) collects [samples](/docs/overview/schemas/#samples) from [monitors](/docs/overview/monitors).
Based on the received samples, the observer:
 * Identify calls
 * Create events (call started, call ended, client joined, client left, etc.)
 * Match clients' inbound-rtp sessions with remote clients' outbound-rtp sessions
 * Match SFUs RTP sessions with browser-side clients' in-, and outbound-rtp sessions.

The Observer creates [reports](/docs/overview/schemas/#reports) and forwards them for further processing.


## Scaling

Observer instances can share data through their [hazelcast](https://hazelcast.com/)
in-memory database grid. To scale observer horizontally you need to
configure the underlying hazelcast so that observer instances can see each other.

## Deployments

See [deployments](/docs/overview/deployments).

### Upgrade Observer

Since observer uses IMDG to store its [object-hierarchy](/docs/observer/object-hierarchy) you need to 
to ensure a gradual upgrading process. The upgrading process should not shut down more 
instances at one time than a number of backup configured for the IMDG to keep. In kubernetes 
this can be achieved by a a [rolling update](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/).

## Configuration

The description for observer configuration can be found [here](https://github.com/ObserveRTC/observer#configurations).