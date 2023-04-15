---
contributors: {'Balázs Kreith'}
title: "sfu-monitor-js"
date: 2023-04-10
lastmod: 2023-04-10
draft: false
images: []
menu:
  docs:
    parent: "api"
weight: 2020
toc: true
images: ["sfu-monitor.png"]
---

The documentation is created for `sfu-monitor-js` version 2.x.y

#### Install

```
npm i @observertc/sfu-monitor-js
```

#### Source code

[https://github.com/ObserveRTC/sfu-monitor-js](https://github.com/ObserveRTC/sfu-monitor-js)


## Top-level components

```javascript
// Using ES6 import.
import * as ObserveRTC from '@observertc/sfu-monitor-js';

// Using CommonJS.
const ObserveRTC = require("@observertc/sfu-monitor-js");

// Or using destructuring assignment:
import {
  /**
   * An interface for the SfuMonitor.
   */
  SfuMonitor, 
  /**
   * Type for SfuMonitorConfig. 
   */
  SfuMonitorConfig,
  /**
   * interface for SfuMonitor events and emitted data types 
   */
  SfuMonitorEventsMap,

  /**
   * interface to define an auxilarity collector and SfuMonitor can use to collect stats
   */
  AuxCollector,

  /**
   * interface for a collector created after mediasoup is added to collect stats from
   */
  MediasoupCollector,

  /**
   * Additional types are imported from the `@observertc/sample-schemas-js` package
   */
  Samples,
  SfuSample,
  SfuTransport,
  SfuInboundRtpPad,
  SfuOutboundRtpPad,
  SfuSctpChannel,
  SfuExtensionStats,
  CustomSfuEvent,
  /**
   * interface for entries SfuMonitor storage provide
   */
  SfuTransportEntry,
  SfuInboundRtpPadEntry,
  SfuOutboundRtpPadEntry,
  SfuSctpChannelEntry,
} from '@observertc/client-monitor-js';

```


### createSfuMonitor

Creates a new SfuMonitor instance with the specified configuration.

```javascript
import * as ObserveRTC from '@observertc/sfu-monitor-js';

// quick start to create a monitor and log the collected stats
const monitor = ObserveRTC.createSfuMonitor({
  collectingPeriodInMs: 2000,
  samplingPeriodInMs: 4000,
});

monitor.on('sample-created', ({ sfuSample }) => {
  console.log('The created sample', sfuSample);
});
```

```javascript
import * as ObserveRTC from '@observertc/sfu-monitor-js';

// configuration for the client-monitor
const config: ObserveRTC.SfuMonitorConfig = {
  /**
  * The identifier of the SFU.
  *
  * DEFAULT: a generated unique value
  */
  sfuId: 'my-sfu-id',

  /**
  * Sets the default logging level for sfu-monitor-js
  * 
  * DEFAULT: warn
  */
  logLevel: LogLevel,

  /**
  * Sets the maximum number of listeners for event emitters
  */
  maxListeners: 1000,
  
  /**
  * Set the ticking time of the timer invokes processes for collecting, sampling, and sending.
  * 
  * DEFAULT: 1000
  */
  tickingTimeInMs: 1000,

  /**
  * By setting it, the observer calls the added statsCollectors periodically
  * and pulls the stats.
  *
  * DEFAULT: undefined
  */
  collectingPeriodInMs: 1000,
  /**
  * By setting it, the observer make samples periodically.
  *
  * DEFAULT: undefined
  */
  samplingPeriodInMs: 1000,

  /**
  * By setting it, the observer sends the samples periodically.
  *
  * DEFAULT: undefined
  */
  sendingPeriodInMs: 1000,

  /**
  * Limits the number of stats polled at once from the collectors. 
  * 
  * DEFAULT: 50
  */
  pollingBatchSize: 50,

  /**
  * Pacing time between polling batches of stats
  * 
  * DEFAULT: undefined
  */
  pollingBatchPaceTimeInMs: 50,

  /**
  * Flag indicating if the monitor creates sfu events.
  * If true, events happening on the collected sources create sfu events such as SFU_TRANSPORT_OPENED, SFU_TRANSPORT_CLOSED.
  * 
  * If this flag is false, the application is responsible for adding sfu events by calling the appropriate SfuMonitor method for the corresponding event.
  * 
  * DEFAULT: false
  */
  createSfuEvents: true,

  /**
  * Configuration for the samples accumulator to balance the transfer the size of the Samples 
  * prepared to be sent to the server
  * 
  */
  accumulator: {
    /**
     * Sets the maximum number of client sample allowed to be in one Sample
     * 
     * DEFAULT: 100
     */
    maxClientSamples: 100,

    /**
     * Sets the maximum number of Samples the accumulator can hold
     * 
     * DEFAULT: 10
     */
    maxSamples: 10,

    /**
     * Forward a Sample to the server even if it is empty
     * 
     * DEFAULT: false
     */
    forwardIfEmpty: false
  }
};

const monitor = ObserveRTC.createSfuMonitor(config);

```

## Integrations

### Mediasoup

You can listen all created workers all routers, transports, etc. by adding mediasoup to the collector

```javascript
import * as mediasoup from 'mediasoup';

const sfuMonitor = createSfuMonitor({
  logLevel: 'info',
  collectingPeriodInMs: 5000,
  samplingPeriodInMs: 15000,
});

const mediasoupCollector = sfuMonitor.createMediasoupCollector({
  mediasoup,
  pollConsumerStats: (consumerId: string) => true,
  pollDataConsumerStats: (dataConsumerId: string) => true,
  pollProducerStats: (producerId: string) => true,
  pollDataProducerStats: (dataProducerId: string) => true,
  pollWebRtcTransportStats: (transportId: string) => true,
});
```

Or you can add specific object to listen for

```javascript
import * as mediasoup from 'mediasoup';

const sfuMonitor = createSfuMonitor({
  logLevel: 'info',
  collectingPeriodInMs: 5000,
  samplingPeriodInMs: 15000,
});

const mediasoupCollector = sfuMonitor.createMediasoupCollector({
  pollConsumerStats: (consumerId: string) => true,
});

const transport = // .. created transport from a router
const consumer = // created consumer from a transport

mediasoupCollector.addConsumer(consumer, transportId);
```

## SfuMonitor

SfuMonitor is responsible for monitoring and collecting SFU-related data.

### Events

SfuMonitor emitted `stats-collected`, `sample-created`, `send` events.

#### stats-collected

Emitted event after each collection period or if the `monitor.collect()` method is called.


```javascript
const subscription = () => {
  console.log('The follosing stats are collected:');
};
monitor.on('stats-collected', subscription);
monitor.once('stats-collected', subscription);
monitor.off('stats-collected', subscription);
```

#### sample-created

Emitted event after each sampling period or if the `monitor.sample()` method is called.

```javascript
const subscription = clientSample => {
  console.log('The ClientSample is created', clientSample);
};
monitor.on('sample-created', subscription);
monitor.once('sample-created', subscription);
monitor.off('sample-created', subscription);
```

#### send

Emitted event after each sending period or if the `monitor.send()` method is called.

```javascript
const subscription = samples =>  {
  console.log('Samples are ready for sending', samples);
};
monitor.on('send', subscription);
monitor.once('send', subscription);
monitor.off('send', subscription);

```

### Properties

  * `config`: The assigned configuration for the SfuMonitor upon creation.
  * `sfuId`: Gets the SFU identifier.
  * `metrics`: Access to the montior's self metrics (last collection time, etc.).
  * `storage`: Access to the collected stats.
  * `closed`: Flag indicating whether the monitor is closed or not.

```javascript
const config = monitor.config;
console.log(
  'The assigned configuration for the SfuMonitor upon creation.',
  config
);

const sfuId = monitor.sfuId;
console.log(
  'the SFU identifier.',
  config
);

const metrics = monitor.metrics;
console.log(
  "Access to the montior's self metrics (last collection time, etc.):",
  metrics
);

const storage = monitor.storage;
console.log('Access to the collected stats:', storage);

const closed = monitor.closed;
console.log('Flag indicating whether the monitor is closed or not:', closed);

```

### createAuxCollector

Creates an auxiliary collector the sfu monitor can collect stats from

```javascript
const collector = monitor.createAuxCollector();

const transportId = ""
collector.addTransportStatsSupplier("myUniqueGeneratedTransportId", async () => {
    const stats: SfuTransport = {

    };
    return stats;
});

collector.addInboundRtpPadStatsSupplier("padId", ...);
collector.addOutboundRtpPadStatsSupplier("padId", ...);
collector.addSctpStreamStatsSupplier("channelId", ...);
```

### createMediasoupCollector

Creates a mediasoup collector with the specified configuration.

### addExtensionStats

Adds an arbitrary stats object that will be sent to the backend observer.

```javascript
monitor.addExtensionStats({ name: 'customStats', value: 'example' });
```

### addTransportOpenedEvent

Adds a transport opened event to the SFU event list.

```javascript
monitor.addTransportOpenedEvent(
  transportId, // The identifier of the opened transport.
  timestamp // Optional timestamp for the event. If not provided, the current date and time will be used.
);
```

### addTransportClosedEvent

Adds a transport closed event to the SFU event list.

```javascript
monitor.addTransportClosedEvent(
  transportId, // The identifier of the closed transport.
  timestamp // Optional timestamp for the event. If not provided, the current date and time will be used.
)
```
### addRtpStreamAdded

Adds an RTP stream added event to the SFU event list.

```javascript
monitor.addRtpStreamAdded(
  transportId, // The identifier of the transport associated with the RTP stream.
  rtpPadId, // The identifier of the RTP pad.
  sfuStreamId, // The identifier of the SFU stream.
  sfuSinkId, // Optional identifier of the SFU sink.
  timestamp // Optional timestamp for the event. If not provided, the current date and time will be used.
);
```
### addRtpStreamRemoved

Adds an RTP stream removed event to the SFU event list.

```javascript
monitor.addRtpStreamRemoved(
  transportId, // The identifier of the transport associated with the RTP stream.
  rtpPadId, // The identifier of the RTP pad.
  sfuStreamId, // The identifier of the SFU stream.
  sfuSinkId, // Optional identifier of the SFU sink.
  timestamp // Optional timestamp for the event. If not provided, the current date and time will be used.
)
```

### setMarker

Marks all of the created samples with a given string.

```javascript
await monitor.setMarker("experimental-stats");
```

### collect

Collects stats.

```javascript
await monitor.collect();
```

### sample

Creates a sfu sample from the collected stats.

```javascript
monitor.sample();
```

#### send

Sends the samples.

```javascript
monitor.send();
```


### close

Closes the monitor and all its used resources.

```javascript
monitor.close();
```


## Storage

Sfu Monitor collects measurements about the following components:
 * **Transport**: Represent a network transport connection between an SFU and an external endpoint
 * **Inbound RTP Pad**: Represents an ingress point for RTP sessions to the SFU.
 * **Outbound RTP Pad**: Represents an eggress point for RTP sessions from the SFU.
 * **SCTP Channel**: Represent an SCTP session

 ### transports

Iterable iterator to list all collected transports.

```javascript
const iterator = statsReader.transports();

```

### getTransportEntry

Gets the monitored object based on identifier.

```javascript
const transportEntry = statsReader.getTransportEntry(transportId);

```

### inboundRtpPads

Iterable iterator to list all collected inbound RTP pads.

```javascript
const iterator = statsReader.inboundRtpPads();

```

### getInboundRtpPad

Iterable iterator to list all collected inbound RTP pads.

```javascript
const inboundRtpPad = statsReader.getInboundRtpPad(rtpPadId);

```

### outboundRtpPads

Iterable iterator to list all collected outbound RTP pads.

```javascript
const inboundRtpPad = statsReader.getInboundRtpPad(rtpPadId);

```

### getOutboundRtpPad

Gets the monitored object based on identifier.

```javascript
const outboundRtpPad = statsReader.getOutboundRtpPad(rtpPadId);

```

### sctpChannels

Iterable iterator to list all collected SCTP channels.

```javascript
const iterator = statsReader.sctpChannels();

```

### getSctpChannel

Gets the monitored object based on identifier.

```javascript
const sctpChannel = statsReader.getOutboundRtpPad(sctpChannelId);
```

## AuxCollector

Interface for auxiliary collectors.

### addTransportStatsSupplier

Adds a transport stats supplier for a given transport ID.

```javascript
auxCollector.addTransportStatsSupplier(transportId, supplier);
```

### removeTransportStatsSupplier

Removes a transport stats supplier for a given transport ID.

```javascript
auxCollector.removeTransportStatsSupplier(transportId);
```

### addInboundRtpPadStatsSupplier

Adds an inbound RTP pad stats supplier for a given inbound RTP pad ID.

```javascript
auxCollector.addInboundRtpPadStatsSupplier(inboundRtpPadId, supplier);
```

### removeInboundRtpPadStatsSupplier

Removes an inbound RTP pad stats supplier for a given inbound RTP pad ID.

```javascript
auxCollector.removeInboundRtpPadStatsSupplier(inboundRtpPadId);
```

### addOutboundRtpPadStatsSupplier
Adds an outbound RTP pad stats supplier for a given outbound RTP pad ID.

```javascript
auxCollector.addOutboundRtpPadStatsSupplier(outboundRtpPadId, supplier);
```

### removeOutboundRtpPadStatsSupplier

Removes an outbound RTP pad stats supplier for a given outbound RTP pad ID.

```javascript
auxCollector.removeInboundRtpPadStatsSupplier(outboundRtpPadId);
```

### addSctpStreamStatsSupplier

Adds an SCTP stream stats supplier for a given SCTP stream ID.

```javascript
auxCollector.addSctpStreamStatsSupplier(sctpChannelId, supplier);
```

### removeSctpStreamStatsSupplier

```javascript
auxCollector.removeSctpStreamStatsSupplier(sctpChannelId);
```

## MediasoupCollector

Interface for Mediasoup collectors.

### addWorker
Adds a Mediasoup worker surrogate.

```javascript
mediasoupCollector.addWorker(worker);
```

### addRouter
Adds a Mediasoup router surrogate.

```javascript
mediasoupCollector.addRouter(worker);
```

### addTransport
Adds a Mediasoup transport surrogate.

```javascript
mediasoupCollector.addTransport(worker, internal);
```

### addProducer
Adds a Mediasoup producer surrogate.

```javascript
mediasoupCollector.addProducer(producer, transportId, internal);
```

### addConsumer
Adds a Mediasoup consumer surrogate.

```javascript
mediasoupCollector.addConsumer(consumer, transportId, internal);
```

### addDataProducer
Adds a Mediasoup data producer surrogate.

```javascript
mediasoupCollector.addDataProducer(dataProducer, transportId, internal);
```

### addDataConsumer
Adds a Mediasoup data consumer surrogate.

```javascript
mediasoupCollector.addDataConsumer(dataConsumer, transportId, internal);
```

## MediasoupCollectorConfig

Configuration options for the MediasoupCollector.

```javascript
const config: MediasoupCollectorConfig = {
  /**
    * The top level mediasoup object to observe events and monitor.
    */
  mediasoup?: MediasoupSurrogate;

  /**
    * Function to indicate if we want to poll the WebRTC transport stats.
    * Default: false
    */
  pollWebRtcTransportStats?: (transportId: string) => boolean;

  /**
    * Function to indicate if we want to poll the plain RTP transport stats.
    * Default: false
    */
  pollPlainRtpTransportStats?: (transportId: string) => boolean;

  /**
    * Function to indicate if we want to poll the pipe transport stats.
    * Default: false
    */
  pollPipeTransportStats?: (transportId: string) => boolean;

  /**
    * Function to indicate if we want to poll the direct transport stats.
    * Default: false
    */
  pollDirectTransportStats?: (transportId: string) => boolean;

  /**
    * Function to indicate if we want to poll the producer stats.
    * Default: false
    */
  pollProducerStats?: (producerId: string) => boolean;

  /**
    * Function to indicate if we want to poll the consumer stats.
    * Default: false
    */
  pollConsumerStats?: (consumerId: string) => boolean;

  /**
    * Function to indicate if we want to poll the dataProducer stats.
    * Default: false
    */
  pollDataProducerStats?: (dataProducerId: string) => boolean;

  /**
    * Function to indicate if we want to poll the data consumer stats.
    * Default: false
    */
  pollDataConsumerStats?: (dataConsumerId: string) => boolean;
}
```