---
title: "Overview"
description: "Overview of ObserveRTC"
lead: "Open source WebRTC monitoring and analytics platform"
date: 2023-09-07T16:33:54+02:00
lastmod: 2023-09-07T16:33:54+02:00
draft: false
weight: 100
toc: true
---

ObserveRTC is a comprehensive monitoring solution designed specifically for WebRTC applications. This section provides an overview of the system architecture, components, and key concepts.

## Key Components

### Monitors

Monitors coexist with media components and are typically integrated through a library, such as client-monitor-js for front-end applications or sfu-monitor-js for SFUs. When a monitor is integrated, it collects measurements of a monitored media component.

### Observer

The observer accepts and evaluates the provided samples and can:

- Aggregate or analyze calls, clients, peer connections, tracks, sfus, etc.
- Create Reports for each provided sample for savings
- Emit events in the server application to do further actions (call started, call ended, client joined, client left, etc.)

### Communication Schemas

Samples and reports are part of communication schemas that describe the structure of the messages between services.
