---
title: "Architecture"
description: "ObserveRTC system architecture and components"
lead: "Understanding the ObserveRTC monitoring architecture"
date: 2023-09-07T16:33:54+02:00
lastmod: 2023-09-07T16:33:54+02:00
draft: false
weight: 120
toc: true
---

```
┌─────────────────┐    Sample Data    ┌─────────────────┐    Processed Data    ┌─────────────────┐
│                 │   ──────────────▶  │                 │   ──────────────▶    │                 │
│  Client Monitor │                   │    Observer     │                      │   Your System   │
│   (Browser)     │                   │   (Server)      │                      │  (DB/Analytics) │
│                 │                   │                 │                      │                 │
└─────────────────┘                   └─────────────────┘                      └─────────────────┘
        │                                      │                                        │
        │                                      │                                        │
   ┌────▼─────┐                          ┌────▼─────┐                              ┌───▼────┐
   │ Collects │                          │ Analyzes │                              │Reports │
   │WebRTC    │                          │ Samples  │                              │Metrics │
   │Statistics│                          │ Real-time│                              │Alerts  │
   └──────────┘                          └──────────┘                              └────────┘
```

ObserveRTC is an open source, modular toolkit designed to enable deep, real-time insights into WebRTC-based applications. It provides a full end-to-end infrastructure from client-side instrumentation to server-side processing, based on standardized sample schemas.

## Key Components

### Client-Side Monitoring

- Collects real-time WebRTC statistics from browser applications
- Uses libraries to gather performance data with minimal impact
- Encodes and transmits samples efficiently

### Server-Side Processing

- Receives and processes samples from multiple clients
- Uses libraries to analyze data and detect patterns
- Generates insights for monitoring and alerting

### Data Flow

- Standardized schemas ensure compatibility between components
- Modular libraries handle encoding, transport, and analysis
- Extensible architecture supports custom metrics and detectors

## Use Cases

- Monitor thousands of WebRTC clients in real-time
- Detect jitter, packet loss, or performance issues
- Analyze call quality across sessions
- Generate custom metrics and alerts
- Build monitoring dashboards
