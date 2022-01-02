---
title: "Get Started"
description: "Get started with ObserveRTC in just a few minutes"
lead: "Let's get started with ObserveRTC"
date: 2021-04-01
lastmod: 2021-01-02
draft: false
images: ["superficial-overview.png"]
menu:
  docs:
    parent: "overview"
weight: 1011
toc: true
---

# Quick start

### 1. Integrate your WebRTC client application

To integrate your client application, it must provide [ClientSample](/docs/schemas/client-sample/) the observer can accept.
You can write your own integration (example to write your own is [here]()), or you can
use an existing client integration:
* [Mediasoup](https://mediasoup.org)
* [Janus](https://janus.conf.meetecho.com/)
* [PeerJS](https://peerjs.com/)
* [Vonage TokBox](https://www.vonage.com/communications-apis/video/)
* [Jitsi](https://jitsi.org)

### 2. Run Observer

In your terminal, type:


    docker run observertc/observer:1.0.0-beta


This will spin up an observer instance with the default configuration print reports to the terminal.


### 3. Analyze reports

Once your application start sending [ClientSample]() to the observer, you should see the generated reports in your console.

*NOTE*: The default configuration have around 30-60s collecting time periods for the incoming samples, thus
the reports are generated with that expected delay.


