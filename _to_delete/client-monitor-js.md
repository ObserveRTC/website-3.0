---
title: "client-monitor-js"
description: "Client-Side WebRTC Monitoring Library"
lead: "JavaScript library to monitor WebRTC applications with comprehensive statistics collection and real-time anomaly detection"
date: 2023-09-07T16:33:54+02:00
lastmod: 2024-01-15T10:00:00+02:00
draft: false
weight: 10
toc: true
---

## Overview

`@observertc/client-monitor-js` is a comprehensive client-side library for monitoring WebRTC applications. It provides real-time statistics collection, automatic anomaly detection, performance scoring, and seamless integration with both native WebRTC and MediaSoup applications.

## Key Features

### Comprehensive Monitoring
- **Multi-source monitoring** - Supports RTCPeerConnection, MediaSoup devices and transports
- **Automatic stats collection** - Periodically collects WebRTC statistics with configurable intervals
- **Real-time anomaly detection** - Built-in detectors for common issues (congestion, CPU performance, audio desync, video freezes, dry tracks)
- **Performance scoring** - Calculates quality scores (0.0-5.0) for connections and tracks with detailed reasoning
- **Event generation** - Automatically emits events for WebRTC state changes and issues

### Advanced Analytics
- **Derived metrics** - Calculates meaningful insights like bitrates, packet loss, RTT, jitter from raw WebRTC statistics
- **Sample compression** - Integration with `@observertc/samples-encoder` for efficient data transmission
- **Sampling system** - Creates periodic snapshots containing complete client state
- **Cross-browser compatibility** - Handles browser-specific differences transparently

### Integration & Customization
- **MediaSoup native support** - Automatic device and transport detection with `newtransport` event hooking
- **Custom detectors** - Extensible framework for application-specific monitoring and issue detection
- **Stats adapters** - Customizable statistics preprocessing pipeline with pre/post processing hooks
- **Score calculators** - Custom performance scoring algorithms with configurable thresholds
- **Logger integration** - Configurable logging with custom logger support

## Installation

```bash
npm install @observertc/client-monitor-js
```

## Quick Example

### Basic Monitoring with Issue Detection

```javascript
import { ClientMonitor } from "@observertc/client-monitor-js";

// Create monitor with automatic sampling and issue detection
const monitor = new ClientMonitor({
    clientId: "my-client-id",
    callId: "my-call-id",
    collectingPeriodInMs: 2000,    // Collect stats every 2 seconds
    samplingPeriodInMs: 4000,      // Create samples every 4 seconds

    // Configure built-in detectors
    congestionDetector: { sensitivity: "medium" },
    cpuPerformanceDetector: { disabled: false },
    videoFreezesDetector: { disabled: false },
});

// Add peer connection to monitor
const peerConnection = new RTCPeerConnection();
monitor.addSource(peerConnection);

// Listen for real-time metrics
monitor.on("stats-collected", () => {
    console.log("Current metrics:", {
        sendingVideo: monitor.sendingVideoBitrate,
        receivingVideo: monitor.receivingVideoBitrate,
        avgRtt: monitor.avgRttInSec * 1000,
        score: monitor.score
    });
});

// Handle automatic issue detection
monitor.on("issue", (issue) => {
    console.log("Issue detected:", issue.type, issue.payload);
    // Types: 'congestion', 'cpu-limitation', 'video-freeze',
    //        'dry-inbound-track', 'audio-desync', etc.
});

// Handle samples for backend transmission
monitor.on("sample-created", (sample) => {
    // Send compressed sample to analytics backend
    fetch("/analytics", {
        method: "POST",
        body: JSON.stringify(sample),
        headers: { "Content-Type": "application/json" },
    });
});

// Cleanup when done
monitor.close();
```

### MediaSoup Integration

```javascript
import mediasoup from "mediasoup-client";

const device = new mediasoup.Device();
await device.load({ routerRtpCapabilities });

// Add device - automatically detects new transports
monitor.addSource(device);

// All transports and producers/consumers are automatically monitored
const transport = device.createSendTransport(/* ... */);
const producer = await transport.produce({ track: videoTrack });
```

## What You Can Monitor

### Real-time Metrics
- **Bitrates** - Audio/video sending/receiving bitrates with peak tracking
- **Network Quality** - RTT, jitter, packet loss, available bandwidth
- **Connection Health** - ICE state, DTLS state, TURN usage, connection establishment time
- **Media Quality** - Frame rates, resolution changes, codec information
- **Performance** - CPU usage impact, stats collection duration, memory usage

### Automatic Issue Detection
- **Network Congestion** - Bandwidth vs usage analysis with configurable sensitivity
- **CPU Performance** - Frame rate volatility and encoding performance issues
- **Audio Desync** - Audio synchronization problems with correction thresholds
- **Video Freezes** - Frozen video track detection with duration tracking
- **Dry Tracks** - Tracks that stop sending/receiving data
- **Connection Issues** - Long peer connection establishment times

### Performance Scoring
The library calculates quality scores (0.0-5.0) with detailed reasoning:
```javascript
monitor.on("score", ({ clientScore, scoreReasons }) => {
    console.log("Quality Score:", clientScore); // e.g., 3.2
    console.log("Score Breakdown:", scoreReasons);
    // { "high-rtt": 1.0, "high-packetloss": 0.8 }
});
```

## Customization Capabilities

The library provides extensive customization options:

### Custom Detectors
Create application-specific issue detectors by implementing the `Detector` interface with custom logic and thresholds.

### Custom Score Calculators
Implement custom performance scoring algorithms that fit your application's quality requirements.

### Stats Adapters
Customize how WebRTC statistics are processed with pre/post processing hooks for data transformation and correlation.

### Event & Sample Customization
Add custom events, metadata, extension statistics, and application data to enrich monitoring data.

### Configuration Flexibility
Fine-tune all detector thresholds, collection intervals, sampling periods, and integration behaviors.

## Integration Examples

### Production Monitoring Pipeline
```javascript
const monitor = new ClientMonitor({
    collectingPeriodInMs: 3000,     // Reduced frequency for production
    samplingPeriodInMs: 10000,      // Less frequent sampling

    // Optimize for production
    cpuPerformanceDetector: { disabled: true },
    congestionDetector: { sensitivity: "low" },
});

// Handle issues with severity-based routing
monitor.on("issue", (issue) => {
    if (issue.payload?.severity === "critical") {
        sendAlert(issue);
    } else {
        logIssue(issue);
    }
});
```

### Real-time Dashboard
The library provides all metrics needed for building real-time monitoring dashboards with connection-level and track-level granularity.

## API Overview

### Core Methods
- `new ClientMonitor(config)` - Create monitor with comprehensive configuration
- `addSource(source)` - Add RTCPeerConnection, MediaSoup device/transport
- `collect()` - Manual stats collection
- `createSample()` - Manual sample creation
- `close()` - Cleanup and shutdown

### Key Events
- `stats-collected` - Real-time metrics available
- `sample-created` - Complete sample ready for transmission
- `issue` - Automatic issue detection
- `score` - Performance score updates
- `congestion` - Network congestion events

## Related Libraries

- **[@observertc/samples-encoder](./sample-encoder-js)** - Binary encoding for efficient sample transmission
- **[@observertc/sample-decoder-js](./sample-decoder-js)** - Binary decoding for sample processing
- **[@observertc/observer-js](./observer-js)** - Server-side sample processing and analysis

## Complete Documentation

For comprehensive documentation including detailed configuration options, advanced customization examples, best practices, troubleshooting, and complete API reference, visit the official npm package:

**📦 [NPM Package Documentation](https://www.npmjs.com/package/@observertc/client-monitor-js)**

The npm package contains:
- Complete API reference with all configuration options
- Advanced integration examples for React, Vue, Angular
- Custom detector and score calculator implementation guides
- Performance optimization strategies
- Browser compatibility details
- Migration guides and troubleshooting
- TypeScript type definitions and usage examples
