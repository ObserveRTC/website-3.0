---
title: "Libraries"
description: "ObserveRTC Client Libraries"
lead: "ObserveRTC libraries for integrating WebRTC call quality monitoring into client applications"
date: 2023-09-07T16:33:54+02:00
lastmod: 2023-09-07T16:33:54+02:00
draft: false
weight: 300
toc: true
---

ObserveRTC provides several specialized libraries to help you implement comprehensive monitoring in your WebRTC applications:

## Available Libraries

### [client-monitor-js](/docs/libraries/client-monitor-js/)
**Client-Side Monitoring Library**
- Injected into browser-based WebRTC applications
- Collects real-time statistics and performance data
- Supports custom detectors and event triggering

### [sample-encoder-js](/docs/libraries/sample-encoder-js/)
**Sample Encoding Library**
- Compress and encode samples efficiently
- Optimized to reduce bandwidth and prevent congestion
- Handles sample encoding with strict schema compliance

### [sample-decoder-js](/docs/libraries/sample-decoder-js/)
**Sample Decoding Library**
- Decode received samples for processing
- Schema validation and error handling
- Efficient batch processing capabilities

### [Observer.js](/docs/libraries/observer-js/)
**Server-Side Processing Library**
- Aggregates and analyzes samples across multiple clients
- Real-time anomaly detection and trend analysis
- Supports custom metrics, alerting, and reporting

## Getting Started

Choose the libraries that fit your use case:
- Use `client-monitor-js` for browser-side monitoring
- Use `Observer.js` for server-side analysis
- Use `sample-encoder-js` for encoding data before transmission
- Use `sample-decoder-js` for decoding received data
