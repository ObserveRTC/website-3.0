---
contributors: {'Balázs Kreith'}
title: "observer-js"
date: 2023-04-10
lastmod: 2023-04-10
draft: false
images: []
menu:
  docs:
    parent: "api"
weight: 2030
toc: true
images: ["observer.png"]
---

The documentation is created for `observer-js` version 1.x.y

#### Install

```
npm i @observertc/observer-js
```

#### Source code

[https://github.com/ObserveRTC/observer-js](https://github.com/ObserveRTC/observer-js)




## Top-level exported components

```javascript
// Using ES6 import.
import * as ObserveRTC from '@observertc/observer-js';

// Using CommonJS.
const ObserveRTC = require("@observertc/observer-js");

// Using destructuring assignment:
import {
  /**
   * Configuration for the Observer class. 
   */
  ObserverConfig,
  /**
   * Configuration for sources providing Samples for the observer.
   */
  SourcesConfig,
  /**
   * Observer sink class providing API for getting reports.
   */
  ObserverSink,
  /**
   * Observer storage type for data stored while an observed client or SFU provide samples.
   * This is not equivalent to a sink, which emits reports for saving; storages are 
   * responsible for maintaining the object hierarchy and, optionally, the last samples
   * from clients or SFUs.
   */
  ObserverStorage,
  /**
   * Storage Provider type gives the possibility to provide 
   * custom-developed storages for the observer.
   */
  StorageProvider,
  /**
   * Types for observed call source and its configuration.
   */
  ObservedCallSource,
  ObservedClientSourceConfig,
  /**
   * Types for observed client source and its configuration.
   */
  ObservedClientSource,
  ObservedCallSourceConfig,
  /**
   * Evaluator configuration and process types.
   */
  EvaluatorConfig,
  EvaluatorProcess,
  /**
   * Types for evaluator context and middleware.
   */
  EvaluatorContext,
  EvaluatorMiddleware,

  /**
   * Creates an observer
   */
  createObserver,

  /**
   * Provide access to objects stored in storages.
   */
  Models,

  /**
   * Provide access to schema for samples
   */
  SampleSchema,

  /**
   * Provide access to schema for reports
   */
  ReportSchema,

} from '@observertc/observer-js';

```

### createObserver

Creates a new Observer instance with the specified configuration.

```javascript
import * as ObserveRTC from '@observertc/observer-js';

// Create with default config
const observer = ObserveRTC.createObserver();
```

```javascript
// OR provide the config
const config: Partial<ObserverConfig> | undefined = {
  /**
   * serviceId is the top-level object identifier for the owner of the provided media service.
   * It can be the name of the organization/company developing the service or the customer 
   * using the provided service.
   * 
   */
  defaultServiceId: 'my-webrtc-service-id',
  /**
   * mediaUnitId holds information clients and SFUs can arbitrarily add in the samples. 
   * For example, it can be the *webrtc app version on the client-side, 
   * and the geographic region and availability zone on the SFU side.
   * 
   */ 
  defaultMediaUnitId: 'my-webapp',

  /**
   * Configuration for sources providing samples for the observer.
   * This, among other things, determines when samples are processed by the observer.
   */
  sources: {
    /**
     * The maximum number of samples that can be collected before an event is emitted 
     * to process the buffered samples.
     */
    maxSamples: 1000,
    /**
     * The time the samples should be collected in the sources buffer and emitted 
     * for processing.
     */
    maxTimeInMs: 10000,
  },

  /**
   * Configuration for the observer to evaluate the samples.
   */
  evaluator: {
    /**
     * Indicates if the evaluator process samples can store the latest sample 
     * in storages or not.
     * 
     * True by default.
     */
    fetchSamples: true,
  },

  /**
   * Sets a storage provider for the observer. If this is given, the application 
   * must provide all internal storage for the observer to store data 
   * to maintain its object hierarchy. Useful for providing a distributed object storage 
   * system if it is required for the developed application.
   * 
   * By default, it uses a simple map-based observer storage to store data in memory.
   */
  storages: customStorageProvider,

  /**
   * Sets the semaphore provider for the observer evaluation process. It is useful if the application 
   * maintains a distributed storage for several observers across the grid. In this case, the semaphore 
   * gives the ability to lock a segment in evaluation to avoid concurrent modification.
   * 
   * By default the observer does not lock any segment in evaluation.
   */
  semaphores: customSemaphores,
  /**
   * Sets the logging level for the instantiated observer.
   * 
   * Possible values are 'trace', 'debug', 'info', 'warn', 'error', 'silent'.
   * 
   * 'info' by default.
   */
  logLevel: 'warn'

};

const observer = ObserveRTC.createObserver(config);
```


## Observer

The `Observer` class manages media events, sources, and evaluations.

```javascript
import * as ObserveRTC from '@observertc/observerr-js';

const observer = ObserveRTC.createObserver();

```

### Properties

#### closed

Indicates whether the observer instance is closed.

```javascript

if (!observed.closed) {
  observer.close();
}

```

#### sink

Access to observer sink emit reports

```javascript

// Subscribe to sink events to get the reports
// and save them into your favorite database / warehouse
observer.sink.on('inbound-audio-track', ({ reports }) => {
  
});
```

### Storages

Observer storage stores data while an observed client or SFU provide samples.
This is not equivalent to sinks, which emits reports for saving; storages are 
responsible for maintaining the object hierarchy and, optionally, the last samples
from clients or SFUs.

#### Calls

```javascript
// Retrieves a call by its ID.
const callId = 'unique-call-id';
const call = await observer.getCall(callId);

// Retrieves all calls with the specified IDs.
const callIds = ['callId-1', 'callId-2'];
for await (const call of observer.getAllCalls(callIds)) {
  
}

// Iterates through all calls. 
for await (const call of observer.calls()) {

}
```

#### Clients

```javascript
// Retrieves a client by its ID.
const clientId = 'unique-client-id';
const client = await observer.getClient(clientId);

// Retrieves all clients with the specified IDs.
const clientIds = ['clientId-1', 'clientId-2'];
const clients = await observer.getAllClients(clientIds);

// Iterates through all clients.
for await (const client of observer.clients()) {

}
```

#### Peer Connections

```javascript
// Retrieves a peer connection by its ID.
const peerConnectionId = 'unique-peer-connection-id';
const peerConnection = await observer.getPeerConnection(peerConnectionId);

// Retrieves all peer connections with the specified IDs.
const peerConnectionIds = ['peerConnectionId-1', 'peerConnectionId-2'];
const peerConnections = await observer.getAllPeerConnections(peerConnectionIds);

// Iterates through all peer connections.
for await (const peerConnection of observer.peerConnections()) {

}
```

#### Inbound Tracks

```javascript
// Retrieves an inbound track by its ID.
const inboundTrackId = 'unique-inbound-track-id';
const inboundTrack = await observer.getInboundTrack(inboundTrackId);

// Retrieves all inbound tracks with the specified IDs.
const inboundTrackIds = ['inboundTrackId-1', 'inboundTrackId-2'];
const inboundTracks = await observer.getAllInboundTracks(inboundTrackIds);

// Iterates through all inbound tracks.
for await (const inboundTrack of observer.inboundTracks()) {

}

```

#### Outbound Tracks

```javascript
// Retrieves an outbound track by its ID.
const outboundTrackId = 'unique-outbound-track-id';
const outboundTrack = await observer.getOutboundTrack(outboundTrackId);

// Retrieves all outbound tracks with the specified IDs.
const outboundTrackIds = ['outboundTrackId-1', 'outboundTrackId-2'];
const outboundTracks = await observer.getAllOutboundTracks(outboundTrackIds);

// Iterates through all outbound tracks.
for await (const outboundTrack of observer.outboundTracks()) {

}
```

#### SFUs

```javascript
// Retrieves an SFU by its ID.
const sfuId = 'unique-sfu-id';
const sfu = await observer.getSfu(sfuId);

// Retrieves all SFUs with the specified IDs.
const sfuIds = ['sfuId-1', 'sfuId-2'];
const sfus = await observer.getAllSfus(sfuIds);

// Iterates through all SFUs.
for await (const sfu of observer.sfus()) {

}
```

#### SFU Transports

```javascript
// Retrieves an SFU transport by its ID.
const sfuTransportId = 'unique-sfu-transport-id';
const sfuTransport = await observer.getSfuTransport(sfuTransportId);

// Retrieves all SFU transports with the specified IDs.
const sfuTransportIds = ['sfuTransportId-1', 'sfuTransportId-2'];
const sfuTransports = await observer.getAllSfuTransports(sfuTransportIds);

// Iterates through all SFU transports.
for await (const sfuTransport of observer.sfuTransports()) {

}
```

#### SFU Inbound RTP Pads


```javascript
// Retrieves an SFU inbound RTP pad by its ID.
const sfuInboundRtpPadId = 'unique-sfu-inbound-rtp-pad-id';
const sfuInboundRtpPad = await observer.getSfuInboundRtpPad(sfuInboundRtpPadId);

// Retrieves all SFU inbound RTP pads with the specified IDs.
const sfuInboundRtpPadIds = ['sfuInboundRtpPadId-1', 'sfuInboundRtpPadId-2'];
const sfuInboundRtpPads = await observer.getAllSfuInboundRtpPads(sfuInboundRtpPadIds);

// Iterates through all SFU inbound RTP pads.
for await (const sfuInboundRtpPad of observer.sfuInboundRtpPads()) {

}
```

#### SFU Outbound RTP Pads


```javascript
// Retrieves an SFU outbound RTP pad by its ID.
const sfuOutboundRtpPadId = 'unique-sfu-outbound-rtp-pad-id';
const sfuOutboundRtpPad = await observer.getSfuOutboundRtpPad(sfuOutboundRtpPadId);

// Retrieves all SFU outbound RTP pads with the specified IDs.
const sfuOutboundRtpPadIds = ['sfuOutboundRtpPadId-1', 'sfuOutboundRtpPadId-2'];
const sfuOutboundRtpPads = await observer.getAllSfuOutboundRtpPads(sfuOutboundRtpPadIds);

// Iterates through all SFU outbound RTP pads.
for await (const sfuOutboundRtpPad of observer.sfuOutboundRtpPads()) {

}
```

#### SFU SctpChannels


```javascript
// Retrieves an SFU SCTP channel by its ID.
const sctpChannelId = 'unique-sfu-sctp-channel-id';
const sfuSctpChannel = await observer.getSfuSctpChannel(sctpChannelId);

// Retrieves all SFU SCTP channels with the specified IDs.
const sctpChannelIds = ['sctpChannelId-1', 'sctpChannelId-2'];
const sfuSctpChannels = await observer.getAllSfuSctpChannels(sctpChannelIds);

// Iterates through all SFU SCTP channels.
for await (const sfuSctpChannel of observer.sfuSctpChannels()) {

}
```

### createCallSource

Creates a new observed call source. An Observed call

```javascript
const config: ObservedCallSourceConfig = {
  /**
   * Overrides the default serviceId given in the ObserverConfig and sets the 
   * serviceId for all samples provided by ClientSources created from this observed call.
   * 
   * This is an optional setting; if it is not provided, the serviceId will be the one 
   * provided by the ObserverConfig.
   */
  serviceId: 'my-webrtc-service-id',
  /**
   * Overrides the default media unit id given in the ObserverConfig and sets it  
   * for all samples provided by ClientSources created from this observed call.
   * 
   * This is an optional setting; if it is not provided, the mediaUnitId will be the one 
   * provided by the ObserverConfig.
   */
  mediaUnitId: 'my-supercool-webapp-id',
  /**
   * Sets the roomId for the observed call.
   * 
   * Required setting.
   */
  roomId: 'observed-room-id',
  /**
   * Sets the callId for the observed call.
   * 
   * Required setting.
   */
  callId: 'observed-room-unique-session-id',

}
const callSource = observer.createCallSource(config);

const clientSource = callSource.createClientSource({
  /**
   * a unique identifier for clients providing samples for the observer
   */
  clientId: 'unique-client-id',

  /**
   * Optional config to set a human readable userId for each client.
   */
  userId: 'John Davis',
  /**
   * Optional config to set a timezone of the client providing a config.
   * All report timestamps are in UTC. With this config, a client's timezone can be noted and
   * taken into account in reports.
  */
  timeZoneId: 'EET',
  /**
   * Optional config to mark all reports provided by this client.
   */
  marker: 'my-experimental-development',
  /**
   * Optional config to set a human-readable userId for each client.
   */
  userId: 'John Davis',

  /**
   * Optional config to set the timestamp (epoch) for the client.
   * If it is not given the timestamp will be assigned at the moment the client 
   * source is created.
   */
  joined: 123456789,
});

```

### createClientSource

```javascript
const config: ObservedCallSourceConfig = {
  /**
   * Overrides the default serviceId given in the ObserverConfig and sets the 
   * serviceId for all samples provided by ClientSources created from this observed call.
   * 
   * This is an optional setting; if it is not provided, the serviceId will be the one 
   * provided by the ObserverConfig.
   */
  serviceId: 'my-webrtc-service-id',
  /**
   * Overrides the default media unit id given in the ObserverConfig and sets it  
   * for all samples provided by ClientSources created from this observed call.
   * 
   * This is an optional setting; if it is not provided, the mediaUnitId will be the one 
   * provided by the ObserverConfig.
   */
  mediaUnitId: 'my-supercool-webapp-id',
  /**
   * Sets the roomId for the observed call.
   * 
   */
  roomId: 'observed-room-id',
  /**
   * Sets the callId for the observed call.
   * 
   */
  callId: 'observed-room-unique-session-id',

  /**
   * A unique identifier for clients providing samples for the observer.
   */
  clientId: 'unique-client-id',

  /**
   * Optional config to set a human-readable userId for each client.
   */
  userId: 'John Davis',
  /**
   * Optional config to set a timezone for the client providing a config.
   * All report timestamps are in UTC. With this config, a client's timezone can be noted and
   * taken into account in reports.
   */
  timeZoneId: 'EET',
  /**
   * Optional config to mark all reports provided by this client.
   */
  marker: 'my-experimental-development',
  /**
   * Optional config to set a human-readable userId for each client.
   */
  userId: 'John Davis',

  /**
   * Optional config to set the timestamp (epoch) for the client.
   * If it is not given, the timestamp will be assigned at the moment the client 
   * source is created.
   */
  joined: 123456789,
}

const clientSource = observer.createClientSource(config);

```


### evaluator processes

Evaluators are async processes to evaluate the observed calls or SFUs after samples 
are processed and changes are made in storages, but before reports are emitted.

For each evaluator the evaluator context is given holds information about the changes 
has happened since the last run.

```javascript

async function evaluateEndedCalls(context: EvaluatorContext) {

  const { endedCalls } = context;

  // log call durations
  for (const endedCall of endedCalls) {
    const elapsedTimeInMins = (endedCall.ended -  Number(endedCall.started)) / (60 * 1000);
    console.log(`Call ${endedCall.callId} duration was ${elapsedTimeInMins} minutes`);
  }
}

// Adds an evaluator process
observer.addEvaluator(evaluateEndedCalls);

// removes the evaluator 10s later
setTimeout(() => {
  observer.removeEvaluator(evaluateEndedCalls);
}, 10000)
```



### close

Closes the observer instance.

```javascript

observer.close();

```

## ClientSource

The `ClientSource` accept samples from a client or signalize a client detaches from a call.

```javascript
// see for config options above
const config = {

}
const clientSource = observer.createClientSource(config);
setTimeout(() => {
  clientSource.close();
}, 1000);

```

### accept

Accept a [ClientSample](docs/overview/schemas/#client-application-provided-samples) will be processed by the observer.

```javascript
const clientSource = observer.createClientSource(config);

socket.on('client-sample-received', clientSample => {
  clientSource.accept(clientSample);
});

```

### close

Close the `ClientSource` object providing samples. When this method is called 
it indicate to the observer that the client is detached, which may trigger to end an 
observed call, if the closed client was the last client in a call.

```javascript
const clientSource = observer.createClientSource(config);

// ...

socket.on('close', () => {
  clientSource.close();
});

```

## SfuSource

## StorageProvider

The `StorageProvider` interface defines the various storage instances used by the Observer.

```typescript
export interface StorageProvider {
  readonly callStorage: ObserverStorage<string, Models.Call>;
  readonly clientStorage: ObserverStorage<string, Models.Client>;
  readonly peerConnectionStorage: ObserverStorage<string, Models.PeerConnection>;
  readonly inboundTrackStorage: ObserverStorage<string, Models.InboundTrack>;
  readonly outboundTrackStorage: ObserverStorage<string, Models.OutboundTrack>;
  readonly sfuStorage: ObserverStorage<string, Models.Sfu>;
  readonly sfuTransportStorage: ObserverStorage<string, Models.SfuTransport>;
  readonly sfuInboundRtpPadStorage: ObserverStorage<string, Models.SfuInboundRtpPad>;
  readonly sfuOutboundRtpPadStorage: ObserverStorage<string, Models.SfuOutboundRtpPad>;
  readonly sfuSctpChannelStorage: ObserverStorage<string, Models.SfuSctpChannel>;
}
```

## ObserverStorage

The `ObserverStorage` interface defines the methods used for managing storage of key-value pairs.

```typescript
interface ObserverStorage<K, V> {

    /**
     * The identifier of the storage
     */
    readonly id: string;

    /**
     * Returns the number of entries the storage has.
     */
    size(): Promise<number>;

    /**
     * Clears the storage and evicts all entries.
     */
    clear(): Promise<void>;

    /**
     * Retrieves the value associated with the given key or returns undefined if the entry is not found.
     *
     * @param key The key to be accessed in the storage.
     * @returns The value or undefined if the entry was not found.
     */
    get(key: K): Promise<V | undefined>;

    /**
     * Retrieves a map filled with key-value pairs found in the storage for the given keys.
     *
     * @param keys A set of keys to be retrieved from the storage.
     * @returns A ReadonlyMap containing the key-value pairs found in the storage.
     */
    getAll(keys: Iterable<K>): Promise<ReadonlyMap<K, V>>;
    
    /**
     * Sets the value for the specified key and returns the previous value or undefined.
     *
     * @param key The key to be set.
     * @param value The value to be set.
     * @returns The previous value or undefined.
     */
    set(key: K, value: V): Promise<V | undefined>;

    /**
     * Sets all the key-value pairs in the provided ReadonlyMap.
     *
     * @param entries A ReadonlyMap containing the key-value pairs to be set.
     * @returns A Promise of the ReadonlyMap containing the key-value pairs.
     */
    setAll(entries: ReadonlyMap<K, V>): Promise<ReadonlyMap<K, V>>;

    /**
     * Inserts a key-value pair only if the key does not already exist and returns the value or undefined.
     *
     * @param key The key to be inserted.
     * @param value The value to be inserted.
     * @returns The value already stored in the storage, or undefined if there was no value stored for the given key.
     */
    insert(key: K, value: V): Promise<V | undefined>;

    /**
     * Inserts all key-value pairs in the provided ReadonlyMap only if the keys do not already exist.
     * Returns a ReadonlyMap containing the values already stored in the storage for the given keys, 
     * or undefined for each key that had no value stored.
     *
     * @param entries A ReadonlyMap containing the key-value pairs to be inserted.
     * @returns A Promise of the ReadonlyMap containing the values already stored in the storage for the given keys,
     *          or undefined for each key that had no value stored.
     */
    insertAll(entries: ReadonlyMap<K, V>): Promise<ReadonlyMap<K, V | undefined>>;

    /**
     * Removes the key-value pair associated with the specified key and returns the removed value or undefined.
     *
     * @param key The key to be removed.
     * @returns The removed value or undefined.
     */
    remove(key: K): Promise<V | undefined>;

    /**
     * Removes all key-value pairs associated with the specified keys and returns a ReadonlyMap of the removed pairs.
     *
     * @param keys An iterable of keys to be removed.
     * @returns A Promise of the ReadonlyMap containing the removed key-value pairs.
     */
    removeAll(keys: Iterable<K>): Promise<ReadonlyMap<K, V>>;

    /**
     * Returns an async iterable iterator for the key-value pairs in the storage.
     */
    [Symbol.asyncIterator](): AsyncIterableIterator<[K, V]>;

}
```

## Semaphores

Interface for a `SemaphoreProvider`, an object that provides semaphore instances for different shared resources. SemaphoreProvider is used to manage access to shared resources across multiple processes.

```typescript
export interface SemaphoreProvider {
    /**
     * A Semaphore instance that manages access to the 'call' shared resource.
     * This semaphore ensures that only one process can access the 'call' resource at a time.
     */
    readonly callSemaphore: Semaphore;
}

```

### Semaphore

Interface for a `Semaphore`, a synchronization primitive that provides exclusive access to a shared resource. Semaphores are used to ensure that only one process can access the shared resource at a time.

```typescript
export interface Semaphore {
    /**
     * Acquires the semaphore, blocking until the semaphore is available.
     * When the semaphore is acquired, it prevents other processes from acquiring it.
     * @returns A Promise that resolves when the semaphore is successfully acquired.
     */
    acquire(): Promise<void>;

    /**
     * Releases the semaphore, allowing other processes to acquire it.
     * @returns A Promise that resolves when the semaphore is successfully released.
     */
    release(): Promise<void>;
}

```

