---
title: "observer-js"
description: "Server-side WebRTC Monitoring Library"
lead: "Node.js library for processing WebRTC client samples and monitoring call quality"
date: 2024-01-15T10:00:00+02:00
lastmod: 2024-01-15T10:00:00+02:00
draft: false
weight: 20
toc: true
---

## Overview

Observer-js is a Node.js library for monitoring WebRTC client data. It processes statistical samples from clients, organizes them into calls and participants, tracks a wide range of metrics, detects common issues, and calculates quality scores. This enables real-time insights into WebRTC session performance.

This library is a core component of the ObserveRTC ecosystem, designed to provide robust server-side monitoring capabilities for WebRTC applications.

## Features

- **Hierarchical Data Model** - Organizes data into `Observer` → `ObservedCall` → `ObservedClient` → `ObservedPeerConnection` and streams/data channels
- **Comprehensive Metrics** - Tracks RTT, jitter, packet loss, codecs, ICE states, TURN usage, bandwidth, and more
- **Automatic Entity Management** - Automatically creates and manages call and client entities based on incoming data samples
- **Issue Detection** - Built-in detectors for common WebRTC problems
- **Quality Scoring** - Calculates quality scores for calls and clients (0.0 to 5.0 scale)
- **Event-Driven Architecture** - Emits events for significant state changes, new entities, and detected issues
- **Configurable Update Policies** - Flexible control over how and when metrics are processed and updated
- **TypeScript Support** - Written in TypeScript with full type definitions
- **Extensible** - Supports custom application data (`appData`) and integration with ObserveRTC schemas

## Installation

```bash
npm install @observertc/observer-js
# or
yarn add @observertc/observer-js
```

## Quick Start

```javascript
import { Observer, ObserverConfig } from '@observertc/observer-js';
import { ClientSample } from '@observertc/schemas';

// 1. Configure the Observer
const observerConfig = {
    updatePolicy: 'update-on-interval',
    updateIntervalInMs: 5000, // Update observer every 5 seconds
    defaultCallUpdatePolicy: 'update-on-any-client-updated', // Calls update when any client sends data
};
const observer = new Observer(observerConfig);

// 2. Listen to events
observer.on('newcall', (call) => {
    console.log(`[Observer] New call detected: ${call.callId}`);

    call.on('newclient', (client) => {
        console.log(`[Call: ${call.callId}] New client joined: ${client.clientId}`);

        client.on('issue', (issue) => {
            console.warn(`[Client: ${client.clientId}] Issue: ${issue.type} - ${issue.severity} - ${issue.description}`);
        });
    });

    call.on('update', () => {
        console.log(
            `[Call: ${call.callId}] Metrics updated. Score: ${call.score?.toFixed(1)}, Clients: ${call.numberOfClients}`
        );
    });
});

// 3. Process Client Samples
function processClientStats(rawStats, callId, clientId) {
    // Transform rawStats into the ClientSample format
    const sample = {
        callId,
        clientId,
        timestamp: Date.now(),
        // ...populate with transformed stats from rawStats, adhering to the ClientSample schema
        // from github.com/observertc/schemas
    };
    observer.accept(sample);
}

// 4. Cleanup when done
process.on('SIGINT', () => observer.close());
```

## Core Concepts

### Data Flow

1. **Client-Side**: Your application collects WebRTC statistics (via `RTCPeerConnection.getStats()`)
2. **Transformation**: Raw stats are transformed into the `ClientSample` schema format
3. **Ingestion**: The `ClientSample` is passed to the `observer.accept()` method
4. **Processing**: Observer-js processes the sample, updating or creating relevant entities
5. **Analysis**: Metrics are analyzed for issue detection and quality scoring
6. **Events**: Events are emitted for significant state changes, new issues, or updates

### Entity Hierarchy

```
Observer (Root)
└── ObservedCall (Call Session)
    └── ObservedClient (Individual Participant)
        └── ObservedPeerConnection (WebRTC Connection)
            ├── ObservedInboundRtpStream (Incoming Media)
            ├── ObservedOutboundRtpStream (Outgoing Media)
            └── ObservedDataChannel (Data Channels)

ObservedTURN (Global TURN metrics)
```

### Automatic Entity Creation

When `observer.accept(sample)` is called:
- If an `ObservedCall` for `sample.callId` doesn't exist, it's automatically created
- If an `ObservedClient` for `sample.clientId` within that call doesn't exist, it's created
- Peer connections, streams, and data channels are managed based on IDs in the sample

## API Reference

### Observer

**Configuration (`ObserverConfig`)**

```typescript
type ObserverConfig<AppData = Record<string, unknown>> = {
    updatePolicy?: 'update-on-any-call-updated' | 'update-when-all-call-updated' | 'update-on-interval';
    updateIntervalInMs?: number; // Used if updatePolicy is 'update-on-interval'
    defaultCallUpdatePolicy?: ObservedCallSettings['updatePolicy'];
    defaultCallUpdateIntervalInMs?: number;
    appData?: AppData; // Custom data for this observer instance
};
```

**Key Properties**
- `observedCalls: Map<string, ObservedCall>` - Active calls
- `observedTURN: ObservedTURN` - Aggregated TURN metrics
- `appData: AppData | undefined` - Custom application data
- `closed: boolean` - True if `close()` has been called
- Counters: `totalAddedCall`, `totalRemovedCall`, `totalClientIssues`, `numberOfClients`, etc.

**Key Methods**
- `createObservedCall<T>(settings: ObservedCallSettings<T>): ObservedCall<T>`
- `getObservedCall<T>(callId: string): ObservedCall<T> | undefined`
- `accept(sample: ClientSample): void` - Main method to feed WebRTC stats
- `update(): void` - Manually trigger an update cycle
- `close(): void` - Cleans up resources for the observer and all its calls
- `createEventMonitor<CTX>(ctx?: CTX): ObserverEventMonitor<CTX>` - For contextual event listening

**Events**
- `'newcall' (call: ObservedCall)`
- `'call-updated' (call: ObservedCall)`
- `'client-event' (client: ObservedClient, event: ClientEvent)`
- `'client-issue' (client: ObservedClient, issue: ClientIssue)`
- `'client-metadata' (client: ObservedClient, metadata: ClientMetaData)`
- `'client-extension-stats' (client: ObservedClient, stats: ExtensionStat)`
- `'update' ()`
- `'close' ()`

### ObservedCall

**Configuration (`ObservedCallSettings`)**

```typescript
type ObservedCallSettings<AppData = Record<string, unknown>> = {
    callId: string;
    appData?: AppData;
    updatePolicy?: 'update-on-any-client-updated' | 'update-when-all-client-updated' | 'update-on-interval';
    updateIntervalInMs?: number;
    remoteTrackResolvePolicy?: 'mediasoup-sfu'; // For specific SFU integration
};
```

**Key Properties**
- `callId: string`
- `appData: AppData | undefined`
- `numberOfClients: number`
- `score: number | undefined` - Overall call quality score
- `observedClients: Map<string, ObservedClient>`

**Key Methods**
- `createObservedClient<T>(settings: ObservedClientSettings<T>): ObservedClient<T>`
- `getObservedClient<T>(clientId: string): ObservedClient<T> | undefined`
- `update(): void`
- `close(): void`
- `createEventMonitor<CTX>(ctx?: CTX): ObservedCallEventMonitor<CTX>`

**Events**
- `'newclient' (client: ObservedClient)`
- `'empty' ()` - When the last client leaves
- `'not-empty' ()` - When the first client joins an empty call
- `'update' ()`
- `'close' ()`

### ObservedClient

**Configuration (`ObservedClientSettings`)**

```typescript
type ObservedClientSettings<AppData = Record<string, unknown>> = {
    clientId: string;
    appData?: AppData;
};
```

**Key Properties**
- `clientId: string`
- `call: ObservedCall` - Reference to the parent call
- `appData: AppData | undefined`
- `score: number | undefined` - Client quality score
- `numberOfPeerConnections: number`
- `usingTURN: boolean`
- `observedPeerConnections: Map<string, ObservedPeerConnection>`

**Key Methods**
- `accept(sample: ClientSample): void` - Processes ClientSample data for this client
- `createObservedPeerConnection<T>(settings): ObservedPeerConnection<T>`
- `getObservedPeerConnection<T>(peerConnectionId: string): ObservedPeerConnection<T> | undefined`
- `update(): void`
- `close(): void`
- `createEventMonitor<CTX>(ctx?: CTX): ObservedClientEventMonitor<CTX>`

**Events**
- `'joined' ()`
- `'left' ()`
- `'update' ()`
- `'close' ()`
- `'newpeerconnection' (pc: ObservedPeerConnection)`
- `'issue' (issue: ClientIssue)`

## Configuration Options

### Update Policies

Control how frequently entities re-calculate metrics and emit `update` events.

**Observer Level**
- `'update-on-any-call-updated'` - Observer updates if any of its calls update
- `'update-when-all-call-updated'` - Observer updates after all its calls update (Default)
- `'update-on-interval'` - Observer updates at `updateIntervalInMs`

**Call Level**
- `'update-on-any-client-updated'` - Call updates if any of its clients update
- `'update-when-all-client-updated'` - Call updates after all its clients update
- `'update-on-interval'` - Call updates at its `updateIntervalInMs`

### Application Data (appData)

Associate custom context with entities using generics:

```javascript
interface MyCallAppData {
    meetingTitle: string;
    scheduledAt: Date;
}

const call = observer.createObservedCall({
    callId: 'call1',
    appData: { meetingTitle: 'Team Sync', scheduledAt: new Date() },
});

console.log(call.appData?.meetingTitle); // "Team Sync"
```

### MediaSoup Integration

For SFU scenarios, especially with MediaSoup:

```javascript
const call = observer.createObservedCall({
    callId: 'sfu-room-123',
    remoteTrackResolvePolicy: 'mediasoup-sfu'
});
```

## ClientSample Schema

The primary input data structure passed to `observer.accept()`. Key fields include:

- `callId`, `clientId`, `timestamp`
- `peerConnections: RTCPeerConnectionStats[]`
- `inboundRtpStreams: RTCInboundRtpStreamStats[]`
- `outboundRtpStreams: RTCOutboundRtpStreamStats[]`
- `remoteInboundRtpStreams: RTCRemoteInboundRtpStreamStats[]`
- `remoteOutboundRtpStreams: RTCRemoteOutboundRtpStreamStats[]`
- `dataChannels: RTCDataChannelStats[]`
- `iceLocalCandidates`, `iceRemoteCandidates`, `iceCandidatePairs`
- `mediaSources: RTCAudioSourceStats[] / RTCVideoSourceStats[]`
- `tracks: RTCMediaStreamTrackStats[]`
- `certificates: RTCCertificateStats[]`
- `codecs: RTCCodecStats[]`
- `transports: RTCIceTransportStats[]`
- `browser`, `engine`, `platform`, `os` (client environment metadata)
- `userMediaErrors`, `iceConnectionStates`, `connectionStates`
- `extensionStats` (for custom data)

*Refer to the [observertc/schemas repository](https://github.com/observertc/schemas) for the complete ClientSample structure.*

## Examples

### Basic Setup with Manual Call Creation

```javascript
import { Observer } from '@observertc/observer-js';

const observer = new Observer({
    updatePolicy: 'update-on-interval',
    updateIntervalInMs: 5000,
    defaultCallUpdatePolicy: 'update-on-any-client-updated',
});

// Manually create call and client
const call = observer.createObservedCall({
    callId: 'scheduled-webinar-456',
    updatePolicy: 'update-on-interval',
    updateIntervalInMs: 10000,
});

const client = call.createObservedClient({
    clientId: 'presenter-01'
});

// Process samples
function mapStatsToClientSample(appStats, callId, clientId) {
    return {
        callId,
        clientId,
        timestamp: Date.now(),
        // ... map all relevant stats fields based on ClientSample schema
    };
}

const rawStats = {}; // Your app's getStats() output
const sample = mapStatsToClientSample(rawStats, 'scheduled-webinar-456', 'presenter-01');
observer.accept(sample);
```

### Event Monitors for Contextual Logging

```javascript
const call = observer.getObservedCall('meeting-alpha-123');
if (call) {
    const callMonitor = call.createEventMonitor({
        callId: call.callId,
        started: new Date()
    });

    callMonitor.on('client-joined', (client, context) => {
        console.log(`EVENT_MONITOR (${context.callId}): Client ${client.clientId} joined at ${new Date()}`);
    });

    callMonitor.on('issue-detected', (client, issue, context) => {
        console.error(`EVENT_MONITOR (${context.callId}): Issue on ${client.clientId} - ${issue.description}`);
    });
}
```

### Express.js Integration

```javascript
import express from 'express';
import { Observer } from '@observertc/observer-js';

const app = express();
const observer = new Observer();

app.use(express.json());

// Endpoint to receive client samples
app.post('/api/samples', (req, res) => {
    try {
        const sample = req.body;
        observer.accept(sample);
        res.status(200).send('OK');
    } catch (error) {
        console.error('Failed to process sample:', error);
        res.status(400).json({ error: error.message });
    }
});

// Get call metrics
app.get('/api/calls/:callId', (req, res) => {
    const call = observer.getObservedCall(req.params.callId);
    if (!call) {
        return res.status(404).json({ error: 'Call not found' });
    }

    res.json({
        callId: call.callId,
        numberOfClients: call.numberOfClients,
        score: call.score,
        appData: call.appData
    });
});

app.listen(3000, () => {
    console.log('Observer server running on port 3000');
});
```

## Metrics Tracked

The library aggregates metrics at each level of the hierarchy:

### Global (Observer)
- Total calls added/removed
- Total client issues
- Number of clients using TURN
- RTT distribution buckets
- Global bandwidth metrics

### Call Level
- Number of clients
- Call quality score
- Total issues in the call
- Aggregate bandwidth (audio/video/data)
- Call duration

### Client Level
- Client quality score
- RTT measurements
- Available incoming/outgoing bitrate
- TURN usage status
- Number of issues
- Peer connection count

### Peer Connection Level
- ICE connection state
- DTLS transport state
- Data channel statistics
- Stream statistics

## Issue Detection

Built-in detectors for common WebRTC problems:
- High packet loss
- Low audio levels
- Frozen video
- Connection setup problems
- High RTT/jitter
- Bandwidth limitations
- TURN connectivity issues

Issues are reported with:
- `type` - Issue category
- `severity` - Issue severity level
- `description` - Human-readable description
- Additional metadata specific to the issue type

## Best Practices

### Resource Management
- Always call `observer.close()`, `call.close()`, and `client.close()` when entities are no longer needed
- Properly remove event listeners to prevent memory leaks
- Monitor memory usage in production deployments

### Error Handling
- Wrap calls to library methods in `try...catch` blocks
- Validate `ClientSample` data before passing to `observer.accept()`
- Handle entity creation errors appropriately

### Sample Quality
- Ensure complete and accurate `ClientSample` data
- Map all relevant WebRTC statistics from `getStats()`
- Include client environment metadata when available

### Update Policies
- Choose update policies based on your application's real-time requirements
- Balance update frequency with system performance
- Use interval-based updates for high-scale deployments

## Troubleshooting

### Memory Leaks
- Ensure `close()` is called on all entities
- Check for unremoved event listeners
- Monitor entity counts in long-running applications

### Missing Events/Updates
- Verify `observer.accept()` is called with correctly formatted `ClientSample` data
- Ensure `callId` and `clientId` in samples match expectations
- Check `updatePolicy` and `updateIntervalInMs` configuration

### Debugging
- Use `console.log` within event handlers to trace data flow
- Add correlation IDs via `appData` for easier debugging
- Monitor entity creation and lifecycle events

## TypeScript Support

The library provides full TypeScript support with generics for custom `appData`:

```typescript
interface MyClientAppData {
    userId: string;
    role: 'admin' | 'user';
}

const client = call.createObservedClient<MyClientAppData>({
    clientId: 'user1',
    appData: { userId: 'u-123', role: 'admin' },
});

// client.appData is typed as MyClientAppData | undefined
```

## Related Libraries

- **[@observertc/client-monitor-js](./client-monitor-js)** - Client-side monitoring and sample collection
- **[@observertc/sample-encoder-js](./sample-encoder-js)** - Efficient sample encoding
- **[@observertc/sample-decoder-js](./sample-decoder-js)** - Sample decoding for server-side processing
- **[ObserveRTC Schemas](../schema)** - Official schema definitions

## Resources

- **[NPM Package](https://www.npmjs.com/package/@observertc/observer-js)** - Current version: 1.0.0-beta.1
- **[GitHub Repository](https://github.com/ObserveRTC/observer-js)** - Source code and issues
- **[ObserveRTC Documentation](https://observertc.org/docs/api/observer-js)** - API documentation
- **[Schemas Repository](https://github.com/observertc/schemas)** - ClientSample and other schema definitions
