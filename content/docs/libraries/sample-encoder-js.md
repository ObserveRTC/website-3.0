---
title: "samples-encoder-js"
description: "Binary encoding utilities for ObserveRTC samples"
lead: "Efficient encoding and serialization of WebRTC monitoring samples for transmission"
date: 2023-09-07T16:33:54+02:00
lastmod: 2024-01-15T10:00:00+02:00
draft: false
weight: 20
toc: true
---

## Overview

`@observertc/samples-encoder` provides efficient binary encoding for ObserveRTC monitoring samples. It converts JavaScript monitoring data into compact binary formats optimized for network transmission.

## Key Capabilities

### Binary Encoding & Compression
- **Optimized serialization** - Convert JavaScript objects to compact binary formats using Avro schemas
- **Built-in compression** - Automatic gzip compression for maximum efficiency
- **Type-safe encoding** - Full TypeScript support with schema validation
- **Cross-platform compatibility** - Works in browsers, Node.js, and WebWorker environments

### Sample Type Support
- **ClientSample encoding** - WebRTC client-side statistics from `@observertc/client-monitor-js`
- **SfuSample encoding** - SFU (Selective Forwarding Unit) server metrics
- **TurnSample encoding** - TURN server statistics and relay information

### Performance Benefits
- **60-80% size reduction** - Significantly smaller than equivalent JSON data
- **Fast encoding** - Optimized algorithms for real-time performance
- **Transport agnostic** - Compatible with WebSocket, HTTP, WebRTC DataChannel, and custom transports

## Installation

```bash
npm install @observertc/samples-encoder
```

## Quick Example

### Basic Sample Encoding

```javascript
import { ClientSampleEncoder } from '@observertc/samples-encoder';

// Create encoder
const encoder = new ClientSampleEncoder();

// Encode client monitoring sample
const clientSample = {
    clientId: 'client-123',
    callId: 'call-456',
    timestamp: Date.now(),
    samples: [
        // PeerConnection samples from client-monitor-js
        { /* peer connection stats */ }
    ]
};

// Encode to binary format (60-80% smaller than JSON)
const encodedData = encoder.encode(clientSample);

// Send to analytics backend
fetch('/api/samples', {
    method: 'POST',
    headers: { 'Content-Type': 'application/octet-stream' },
    body: encodedData
});
```

## What You Can Encode

### Client Monitoring Data
- **WebRTC Statistics** - Complete peer connection, track, and RTP stream metrics
- **Issue Detection** - Congestion, CPU performance, audio desync events
- **Performance Scores** - Quality scores with detailed reasoning
- **Custom Events** - Application-specific events and metadata

### Server-Side Metrics
- **SFU Statistics** - Transport states, media routing, participant metrics
- **TURN Server Data** - Relay statistics, allocation details, bandwidth usage

## Real-World Integration

### Client Monitor Integration
```javascript
import { ClientMonitor } from '@observertc/client-monitor-js';
import { ClientSampleEncoder } from '@observertc/samples-encoder';

const monitor = new ClientMonitor({ /* config */ });
const encoder = new ClientSampleEncoder();

// Automatically encode and send samples
monitor.on('sample-created', async (sample) => {
    const encoded = encoder.encode(sample);

    // Send to analytics server
    await fetch('/api/analytics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/octet-stream' },
        body: encoded
    });
});
```

### WebSocket Streaming

```javascript
import { ClientSampleEncoder } from '@observertc/samples-encoder';

const encoder = new ClientSampleEncoder();
const websocket = new WebSocket('wss://analytics.example.com');

// Encode and stream samples
monitor.on('sample-created', (sample) => {
    const encoded = encoder.encode(sample);
    websocket.send(encoded);
});
```

## Integration with Other Libraries

### Server-Side Processing
```javascript
// Server receives and processes encoded samples
import { SampleDecoder } from '@observertc/sample-decoder-js';

app.post('/api/samples', async (req, res) => {
    const decoder = new SampleDecoder();
    const sample = decoder.decode(req.body);

    await processMonitoringData(sample);
    res.status(200).send('OK');
});
```

## API Overview

### Core Classes
- `ClientSampleEncoder` - Encode client monitoring samples
- `SfuSampleEncoder` - Encode SFU server metrics
- `TurnSampleEncoder` - Encode TURN server statistics

### Key Methods
- `encode(sample)` - Encode single sample to binary format

## Related Libraries

- **[@observertc/client-monitor-js](./client-monitor-js)** - Generates samples for encoding
- **[@observertc/sample-decoder-js](./sample-decoder-js)** - Decodes encoded samples
- **[@observertc/observer-js](./observer-js)** - Server-side sample processing

## Complete Documentation

For comprehensive documentation including detailed configuration options, advanced encoding strategies, and complete API reference:

**📦 [NPM Package Documentation](https://www.npmjs.com/package/@observertc/samples-encoder)**
