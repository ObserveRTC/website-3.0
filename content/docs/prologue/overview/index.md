---
title: "Overview"
description: "Monitor your WebRTC with ObserveRTC"
date: 2021-11-16
lastmod: 2021-11-16
draft: false
menu:
  docs:
    parent: "prologue"
weight: 1020
toc: true
images: ["observer-overview.png", "observer-users.png"]
---

{{< img-simple src="observer-overview.png" alt="High-level sketch of the observer inputs and outputs" >}}

In a nutshell, Observer is the focuspoint of measurements of media services. Components, like WebRTC client applications, create samples. [Samples]() contain measurements made at a specific time. Observer analyze samples received from clients and matching the ones belong to the same call. A call is a high-level group identifier for clients shares media contents with each other. The observer generates reports. [Reports]() are the product of the observation made by the observer analyzing the samples. All report holds the information which call it belongs to, and also can hold different event types, which can trigger further actions in a consecutive processing unit (Evaluator in the picture).

{{< img-simple src="observer-users.png" alt="High-level sketch of the observer inputs and outputs" >}}

Let's take an example. Alice, and Bob is in a meeting room `letsTalkAboutCrytpography`. Under the hood, they use WebRTC client application 
establishes the real-time communications between their browsers. More preciesly, they might use a SFU (Selective Forwarding Unit) to exchange their media contents.

Observer collect samples from media service components and identify calls. It also signalize when a call is started, when it is ended, when a track is added. The generated reports are a great starting point to build stream analyzer application to evaluate the quality of the media, or creat alarming service for certain (combination) of events, the possibilities are endless. It starts with an open-source continously maintained reliable engine: The observer.

To integrate the observer your webrtc application should provide the samples for it. Here is how integration comes into the picture. 