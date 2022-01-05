---
title: "Introduction"
description: "ObserveRTC is an open-source project provide solutions to monitor your WebRTC Applications"
lead: "ObserveRTC provides open-source tools for monitoring WebRTC Applications"
date: 2021-04-01
lastmod: 2021-04-01
draft: false
images: []
menu:
  docs:
    parent: "overview"
weight: 1010
toc: true
---

Making analytics tools for Real Time Communication (RTC) is challenging.
Technologies like WebRTC generate a tremendous amount statistical data with APIs like `RTCPeerConnection.getStats()`.
One could aggregate this data, but data volumes quickly become overwhelming.
In addition, parsing this data for common queries and exploratory analysis is extremely cumbersome.
Commercial tools are expensive, lack flexibility, and cannot easily be adjusted for specific environments.

### ObserveRTC provides:
* **Client-side libraries** - collect data from your RTC clients with negligible performance impact
* **Server-side integrations** - options to add data from devices like Selective Forwarding Unit (SFU)
* **Flexible Database options** - use your preferred data architectures like Kafka, MongoDB, Hazelcast, RedShift, BigQuery, and others
* **Pre-defined scheme** - start with and expand on the ObserveRTC scheme to simplify data queries

### ObserveRTC benefits

* **Free and Open-source** - No hidden magic, no secret source, it is a transparent monitoring solution for everyone.
* **Own your data** - By deploying it you have full ownership of data from your applications and run further analysis.
* **Easy to scale** - When the size of your memory and compute requirements increase, new resources can be dynamically added to your cluster to scale elastically.

### Use cases

 * **Performance tuning** - Debug/improve your WebRTC applications.
 * **Regression analysis** - Quantify the impact of changes you made.
 * **System operations** - Measure and monitor the performance of your application.
 * **Troubleshooting & debugging** - Investigate technical issues.
 * **Usage trends** - Track/Understand how your app is used.

### Target users

 * **Application developers** - debug your WebRTC applications.
 * **Product Owner** - measure and monitor the performance of your application.
 * **Operations team** - monitor the health and get critical alerts about your application.


