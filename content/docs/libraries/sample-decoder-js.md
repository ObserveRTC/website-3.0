---
title: "sample-decoder-js"
description: "Sample Decoding Library"
lead: "Efficient decoding and validation of monitoring samples"
date: 2023-09-07T16:33:54+02:00
lastmod: 2024-01-15T10:00:00+02:00
draft: false
weight: 30
toc: true
---

## Overview

`@observertc/sample-decoder-js` provides efficient decoding for binary-encoded ObserveRTC monitoring samples. It converts compressed binary data back to JavaScript objects with schema validation.

## Key Capabilities

### High-Performance Decoding
- **Fast decompression** - Optimized algorithms for rapid binary-to-object conversion
- **Schema-aware decoding** - Leverages Avro schemas for efficient type reconstruction
- **Type safety** - Full TypeScript support with proper type reconstruction
- **Memory efficient** - Minimal memory footprint during decoding operations

### Validation & Recovery
- **Automatic schema validation** - Ensures decoded data matches expected structure
- **Version compatibility** - Handles multiple schema versions gracefully
- **Error recovery** - Robust handling of corrupted or malformed data

## Installation

```bash
npm install @observertc/sample-decoder-js
```

## Quick Example

### Basic Sample Decoding

```javascript
import { SampleDecoder } from '@observertc/sample-decoder-js';

// Create decoder
const decoder = new SampleDecoder();

// Decode binary data received from network
const encodedData = receivedFromNetwork(); // Binary data from samples-encoder

// Decode single sample
const decodedSample = decoder.decode(encodedData);

console.log('Decoded sample:', {
    clientId: decodedSample.clientId,
    timestamp: decodedSample.timestamp,
    peerConnections: decodedSample.peerConnectionSamples?.length || 0,
    events: decodedSample.clientEvents?.length || 0
});
```

## What You Can Decode

### Client Sample Data
- **WebRTC Statistics** - Complete peer connection, track, and RTP stream metrics
- **Performance Metrics** - Bitrates, packet loss, RTT, jitter measurements
- **Issue Detection Results** - Congestion events, CPU limitations, video freezes
- **Quality Scores** - Performance scores with detailed reasoning
- **Custom Events** - Application-specific events and metadata

### Server Sample Data
- **SFU Metrics** - Transport states, media routing, participant statistics
- **TURN Statistics** - Relay usage, allocation details, bandwidth metrics

## Real-World Integration

### HTTP Endpoint Processing

```javascript
import express from 'express';
import { SampleDecoder } from '@observertc/sample-decoder-js';

const app = express();
const decoder = new SampleDecoder();

// Process encoded samples from clients
app.post('/api/samples', express.raw({ type: 'application/octet-stream' }), async (req, res) => {
    try {
        const sample = decoder.decode(req.body);

        // Process the sample
        await analytics.store(sample);
        await alerts.checkThresholds(sample);

        res.status(200).json({ processed: 1 });
    } catch (error) {
        console.error('Decoding failed:', error);
        res.status(400).json({ error: 'Invalid sample data' });
    }
});
```

### WebSocket Processing

```javascript
import WebSocket from 'ws';
import { SampleDecoder } from '@observertc/sample-decoder-js';

const wss = new WebSocket.Server({ port: 8080 });
const decoder = new SampleDecoder();

wss.on('connection', (ws) => {
    ws.on('message', async (data) => {
        try {
            const sample = decoder.decode(data);
            await realTimeProcessor.handle(sample);
        } catch (error) {
            console.warn('Invalid data received:', error.message);
        }
    });
});
```

## Integration Examples

### Analytics Pipeline

```javascript
import { SampleDecoder } from '@observertc/sample-decoder-js';

class AnalyticsPipeline {
    constructor() {
        this.decoder = new SampleDecoder();
    }

    async processSample(encodedData) {
        try {
            const sample = this.decoder.decode(encodedData);

            // Extract metrics
            const metrics = this.extractMetrics(sample);
            await this.metricsDb.insert(metrics);

            // Check alerts
            await this.alerting.evaluate(sample);

            // Update dashboards
            await this.dashboards.update(sample);
        } catch (error) {
            console.error('Processing failed:', error);
        }
    }
}
```

### Real-time Monitoring

```javascript
import { SampleDecoder } from '@observertc/sample-decoder-js';

class RealTimeMonitor {
    constructor() {
        this.decoder = new SampleDecoder();
    }

    async handleEncodedSample(encodedData) {
        const sample = this.decoder.decode(encodedData);

        // Update real-time dashboard
        this.dashboard.updateClientMetrics(sample.clientId, {
            timestamp: sample.timestamp,
            score: sample.score,
            issueCount: sample.clientEvents?.filter(e => e.name === 'ISSUE')?.length || 0
        });

        // Trigger alerts for critical issues
        if (sample.score < 2.0) {
            this.alerts.triggerQualityAlert(sample);
        }
    }
}
```

## API Overview

### Core Classes
- `SampleDecoder` - Main decoder for sample decoding

### Key Methods
- `decode(binaryData)` - Decode single sample from binary format

## Related Libraries

- **[@observertc/samples-encoder](./sample-encoder-js)** - Binary encoding for efficient transmission
- **[@observertc/client-monitor-js](./client-monitor-js)** - Generates samples for encoding/decoding
- **[@observertc/observer-js](./observer-js)** - Server-side sample processing and analysis

## Complete Documentation

For comprehensive documentation including detailed configuration options, advanced validation strategies, and complete API reference:

**📦 [NPM Package Documentation](https://www.npmjs.com/package/@observertc/sample-decoder-js)**
