---
contributors: {'Balázs Kreith'}
title: "client-monitor-js"
date: 2023-04-10
lastmod: 2023-04-10
draft: false
images: []
menu:
  docs:
    parent: "api"
weight: 2010
toc: true
images: ["client-monitor.png"]
---

The documentation is created for `client-monitor-js` version 2.x.y

#### Install

```
npm i @observertc/client-monitor-js
```

#### Source code

[https://github.com/ObserveRTC/client-monitor-js](https://github.com/ObserveRTC/client-monitor-js)



## Top-level components

```javascript
// Using ES6 import.
import * as ObserveRTC from '@observertc/client-monitor-js';

// Using CommonJS.
const ObserveRTC = require("@observertc/client-monitor-js");

// Or using destructuring assignment:
import {
  /**
   * An interface for the ClientMonitor.
   */
  ClientMonitor,
  /**
   * Type for ClientMonitorConfig. 
   */
  ClientMonitorConfig,
  /**
   * interface for ClientMonitor events and emitted data types 
   */
  ClientMonitorEvents,

  /**
   * collection of types the client-monitor collect w3c stats 
   */
  W3CStats,

  /**
   * Additional types are imported from the `@observertc/sample-schemas-js` package
   */
  Samples,
	ClientSample,
	SfuSample,
	ExtensionStat,
	PeerConnectionTransport,
	IceCandidatePair,
	MediaSourceStat,
	MediaCodecStats,
	InboundAudioTrack,
	InboundVideoTrack,
	OutboundAudioTrack,
	OutboundVideoTrack,
	IceLocalCandidate,
	IceRemoteCandidate,
  CustomCallEvent,
  /**
   * interface for entries ClientMonitor storage provide
   */
  CodecEntry,
  InboundRtpEntry,
  OutboundRtpEntry,
  RemoteInboundRtpEntry,
  RemoteOutboundRtpEntry,
  MediaSourceEntry,
  ContributingSourceEntry,
  DataChannelEntry,
  TransceiverEntry,
  SenderEntry,
  ReceiverEntry,
  TransportEntry,
  SctpTransportEntry,
  IceCandidatePairEntry,
  LocalCandidateEntry,
  RemoteCandidateEntry,
  CertificateEntry,
  IceServerEntry,
  PeerConnectionEntry,
} from '@observertc/client-monitor-js';

```

### createClientMonitor

Creates a new ClientMonitor instance with the specified configuration.

```javascript
import * as ObserveRTC from '@observertc/client-monitor-js';

// quick start to create a monitor and log the collected stats
const monitor = ObserveRTC.createClientMonitor({
  collectingPeriodInMs: 2000,
});

monitor.on('stats-collected', stats => {
  console.log('The collected stats', stats);
});
```

```javascript
import * as ObserveRTC from '@observertc/client-monitor-js';

// configuration for the client-monitor
const config: ObserveRTC.ClientMontorConfig = {
  /**
   * By setting it, the monitor calls the added statsCollectors periodically
   * and pulls the stats.
   * 
   * DEFAULT: undefined
   */
  collectingPeriodInMs: 5000,
  /**
   * By setting it, the monitor make samples periodically.
   * 
   * DEFAULT: undefined
   */
  samplingPeriodInMs: 10000,

  /**
   * By setting it, the monitor sends the samples periodically.
   * 
   * DEFAULT: undefined
   */
  sendingPeriodInMs: 10000,

  /**
   * By enabling this option, the monitor automatically generates events
   * when a peer connection added to the collector undergoes a change in connection state or when a track on it is added or removed.
   *
   * If this option is set to true, the samples created by the monitor will include the generated events. However, if
   * no sample is created, events will accumulate indefinitely within the monitor. It is recommended to set this option to true
   * if you want to create a sample with events.
   *
   * DEFAULT: false
   */
  createCallEvents: false,

  /**
   * Collector Component related configurations
   * 
   * DEFAULT: configured by the monitor
   */
  collectors: {
    /**
     * Sets the adapter adapt different browser type and version 
     * provided stats.
     * 
     * DEFAULT: configured by the monitor
     */
    adapter: {
      /**
       * the type of the browser, e.g.: chrome, firefox, safari
       * 
       * DEFAULT: configured by the collector
       */
      browserType: "chrome",
      /**
       * the version of the browser, e.g.: 97.xx.xxxxx
       * 
       * DEFAULT: configured by the collector
       */
      browserVersion: "97.1111.111",
    },
  },

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

const monitor = ObserveRTC.createClientMonitor(config);

```


## Integrations

### Mediasoup

```javascript
import { createClientMonitor } from "@observertc/client-monitor-js";
import mediasoup from "mediaousp-client";

const mediasoupDevice = new mediasoup.Device();
const config = {
    collectingPeriodInMs: 5000,
};
const monitor = createClientMonitor(config);

// adds a mediasoup device to the collectors
const mediasoupStatsCollector = monitor.collectors.collectFromMediasoupDevice(mediasoupDevice);

// close the statscollector and remove it from collectors
mediasoupStatsCollector.close();
```

**Important Note**: The created collector is hooked on the device 'newtransport' event, 
and can detect transports automatically when they are created after the device is added.
If you create transports before you add the device to the monitor,  
transports you created before will not be monitored automatically, you need to add them 
to the statscollector, like this:

```javascript
const myTransport = // your transport created before the device is added to the monitor
mediasoupStatsCollector.addTransport(myTransport)
```


## ClientMonitor

The ClientMonitor is the central element for evaluating WebRTC apps running in the browser. It collects stats from peer connections, creates samples, and provides access to storage. This storage organizes the collected stats and allows for structured access.

### Events

ClientMonitor emitted `stats-collected`, `sample-created`, `send` events.

#### stats-collected

Emitted event after each collection period or if the `monitor.collect()` method is called.


```javascript
const subscription = stats => {
  console.log('The follosing stats are collected:', stats);
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

  * `config`: The assigned configuration for the ClientMonitor upon creation.
  * `os`: Information about the operating system from which the observer is obtained.
  * `browser`: Information about the browser from which the observer is obtained.
  * `platform`: Information about the platform from which the observer is obtained.
  * `engine`: Information about the engine from which the observer is obtained.
  * `audioInputs`: Iterable iterator for the audio input devices obtained by the observer.
  * `audioOutputs`: Iterable iterator for the audio output devices obtained by the observer.
  * `videoInputs`: Iterable iterator for the video input devices obtained by the observer.
  * `metrics`: Provides access to the observer's self metrics (last collection time, etc.).
  * `storage`: Provides access to the collected stats.
  * `collectors`: Provides access to built-in integrations for different providers.
  * `closed`: Flag indicating whether the monitor is closed or not.

```javascript
const config = monitor.config;
console.log(
  'The assigned configuration for the ClientMonitor upon creation.',
  config
);

const os = monitor.os;
console.log(
  'Information about the operating system from which the observer is obtained:',
  os
);

const browser = monitor.browser;
console.log(
  'Information about the browser from which the observer is obtained:',
  browser
);

const platform = monitor.platform;
console.log(
  'Information about the platform from which the observer is obtained:',
  platform
);

const audioInputs = monitor.audioInputs;
for (const audioInput of audioInputs) {
  console.log('Audio input device obtained by the observer:', audioInput);
}

const audioOutputs = monitor.audioOutputs;
for (const audioOutput of audioOutputs) {
  console.log('Audio output device obtained by the observer:', audioOutput);
}

const videoInputs = monitor.videoInputs;
for (const videoInput of videoInputs) {
  console.log('Video input device obtained by the observer:', videoInput);
}

const metrics = monitor.metrics;
console.log(
  "Access to the observer's self metrics (last collection time, etc.):",
  metrics
);

const storage = monitor.storage;
console.log('Access to the collected stats:', storage);

const collectors = monitor.collectors;
console.log(
  'Access to built-in integrations for different providers:',
  collectors
);

const closed = monitor.closed;
console.log('Flag indicating whether the monitor is closed or not:', closed);


```

### addTrackRelation

Adds a track relation to bind tracks to produced/published or consumed/subscribed media objects from SFUs.

```javascript
monitor.addTrackRelation({
  /**
   * The identifier of the track the relation is defined for.
   */
  trackId: mediaStreamTrack.id;
  /**
   * The identifier of the media stream published / produced using the above defined track id.
   */
  sfuStreamId: 'outbound-track-sfu-stream-id'

  /**
   * The identifier of the media sink subscribed / consumed for streaming the above defined track id.
   */
  sfuSinkId: 'inbound-track-sfu-sink-id'
});
```

### removeTrackRelation

Removes a track relation associated with the given track id.

```javascript
monitor.removeTrackRelation(mediaStreamTrack.id);
```

### addLocalSDP

Adds the local part of the Session Description Protocol (SDP).
The Monitor adds it to the next sample it creates and sends it to the observer.

```javascript
monitor.addLocalSDP('a=...');
```

### addMediaConstraints

Adds media constraints used to obtain media. Typically, these are the parameters given to MediaDevices.getUserMedia(). Constraints added to the observer are sampled by a sampler when a ClientSample is created.

```javascript
const constraints = {
  audio: true,
  video: true
};
monitor.addMediaConstraints(constraints);
navigator.getUserMedia(constraints);

```

### addUserMediaError

Adds a user media error. Typically, this is an error caught while obtaining getUserMedia from MediaDevices. The obtained user media error is added to the observer and sampled by a sampler when a ClientSample is created.

```javascript

navigator.getUserMedia(constraints, () => {
  // use the stream
}, err => {
  // adds the error to the sample can be send to the server
  monitor.addUserMediaError(err);
})
```


### addMediaTrackAddedCallEvent

Adds a MEDIA_TRACK_ADDED type call event to the sample created next time.

```javascript
monitor.addMediaTrackAddedCallEvent('peerConnectionId', 'mediaTrackId');
```


### addMediaTrackRemovedCallEvent

Adds a MEDIA_TRACK_REMOVED type call event to the sample created next time.

```javascript
monitor.addMediaTrackRemovedCallEvent('peerConnectionId', 'mediaTrackId');
```


### addPeerConnectionOpenedCallEvent

Adds a PEER_CONNECTION_OPENED type call event to the sample created next time.

```javascript
monitor.addPeerConnectionOpenedCallEvent('peerConnectionId');

```


### addPeerConnectionClosedCallEvent

Adds a PEER_CONNECTION_CLOSED type call event to the sample created next time.

```javascript
monitor.addPeerConnectionClosedCallEvent('peerConnectionId');

```

### addIceConnectionStateChangedCallEvent

Adds an ICE_CONNECTION_STATE_CHANGED type call event to the sample created next time.

```javascript
monitor.addIceConnectionStateChangedCallEvent('peerConnectionId', 'connectionState');
```


### addCustomCallEvent

Adds a custom call event that will be sent along with the sample to the observer. The added event will be reported as a CallEvent by the observer.

```javascript
monitor.addCustomCallEvent({
  type: 'custom-event',
  payload: { customData: 'example' },
});
```

### addExtensionStats

Adds an application-provided custom payload object to the observer. This is typically extra information that the application wants to obtain and send to the backend. The added information is obtained by the sampler, and the ClientSample holds and sends this information to the observer. The observer will forward this information along with the call it belongs to.

```javascript
monitor.addExtensionStats({ key: 'customStats', value: 'example' });
```

### setMediaDevices

Sets the media devices used by the WebRTC app. Typically, this is a list of [MediaDevices.getUserMedia()](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia).

The client monitor keeps track of the already added devices, removes the ones not updated,
and in the next sample sent to the observer, only the new devices will be sent

```javascript
monitor.setMediaDevices(device1, device2, device3);

```

### setCollectingPeriod

Sets the collecting period in milliseconds. The Monitor calls its collect method at the specified time interval.

```javascript
monitor.setCollectingPeriod(1000);
```


### setSamplingPeriod

Sets the sampling period in milliseconds. The Monitor calls its sample method at the specified time interval.

```javascript
monitor.setSamplingPeriod(1000);
```


### setSendingPeriod

Sets the sending period in milliseconds. The Monitor calls its send method with a given time period.

```javascript
monitor.setSendingPeriod(1000);
```


### collect

Collect all stats simultaneously and update the storage.

```javascript
monitor.collect().then(() => console.log('stats are collected'));
```


### sample

Make ClientSample from collected stats.

```javascript
monitor.sample();
```

### send

Create Samples from the accumulated ClientSamples (and/or SfuSamples) and emit send event with the created samples.

```javascript
monitor.send();
```

### close

Close the ClientObserver, clear the storage, and stats collectors.

```javascript
monitor.close();
```




## Collectors

The `Collectors` interface represents a collection of `StatsCollector` instances. It provides methods for managing and interacting with these instances.

### hasCollector

Checks if a collector with the given `collectorId` exists in the collection.

```javascript

```

### removeCollector

Removes a collector with the given `collectorId` from the collection.

```javascript

```

### addGetStats

Adds a custom stats collector using a `getStats` function.

```javascript
const collector = monitor.addGetStats(() => myPeerConnection.getStats());
```

### addStatsProvider

Adds a stats collector based on a provided `StatsProvider`.

```javascript
const collector = monitor.addStatsProvider({
  /**
   * A unique id for a peer connection the stats belongs to. 
   */
  peerConnectionId: 'unique-pc-id'

  /**
   * An optional label of the peer collector added as label to the samples as well. 
   */
  label: 'sending-pc',

  /**
   * Set a function called when stats are collected 
   */
  getStats: myPeerConnection.getStats,
});
```

### addRTCPeerConnection

Adds a stats collector for an `RTCPeerConnection`.

```javascript
const collector = monitor.addRTCPeerConnection(peerConnection);
```

### addMediasoupDevice

Adds a stats collector for a Mediasoup device.

```javascript
const collector = monitor.addMediasoupDevice(mediasoupDevice);
```

## Storage

Client Monitor collects [WebRTCStats](https://www.w3.org/TR/webrtc-stats/). The collected stats can be accessed through entries the client monitor storage provides.

### inboundRtps
```javascript
const storage = monitor.storage;

for (const inboundRtp of storage.inboundRtps()) {
    const receiver = inboundRtp.getReceiver();
    const trackId = inboundRtp.getTrackId();
    const ssrc = inboundRtp.getSsrc();
    const remoteOutboundRtp = inboundRtp.getRemoteOutboundRtp();
    const peerConnection = inboundRtp.getPeerConnection();
    const transport = inboundRtp.getTransport();
    const codec = inboundRtp.getCodec();

    console.log(trackId, ssrc, 
        inboundRtp.stats, 
        remoteOutboundRtp.stats, 
        receiver.stats,
        peerConnection.stats,
        transport.stats,
        codec.stats
    );
}
```

### outboundRtps

```javascript
const storage = monitor.storage;

for (const outboundRtp of storage.outboundRtps()) {
    const sender = outboundRtp.getSender();
    const trackId = outboundRtp.getTrackId();
    const ssrc = outboundRtp.getSsrc();
    const remoteInboundRtp = outboundRtp.getRemoteInboundRtp();
    const peerConnection = outboundRtp.getPeerConnection();
    const transport = outboundRtp.getTransport();
    const mediaSource = outboundRtp.getMediaSource();

    console.log(trackId, ssrc, 
        outboundRtp.stats, 
        remoteInboundRtp.stats, 
        sender.stats,
        peerConnection.stats,
        transport.stats,
        mediaSource.stats
    );
}
```

### remoteInboundRtps

```javascript
const storage = monitor.storage;

for (const remoteInboundRtp of storage.remoteInboundRtps()) {
    const ssrc = remoteInboundRtp.getSsrc();
    const outboundRtp = remoteInboundRtp.getOutboundRtp();
    const peerConnection = remoteInboundRtp.getPeerConnection();

    console.log(ssrc, 
        remoteInboundRtp.stats, 
        outboundRtp.stats, 
        peerConnection.stats
    );
}
```

### remoteOutboundRtps

```javascript
const storage = monitor.storage;

for (const remoteOutboundRtp of storage.remoteOutboundRtps()) {
    const ssrc = remoteOutboundRtp.getSsrc();
    const inboundRtp = remoteOutboundRtp.getInboundRtp();
    const peerConnection = remoteOutboundRtp.getPeerConnection();

    console.log(ssrc, 
        remoteOutboundRtp.stats, 
        inboundRtp.stats, 
        peerConnection.stats
    );
}
```

### mediaSources

```javascript
const storage = monitor.storage;

for (const mediaSource of storage.mediaSources()) {
    const peerConnection = mediaSource.getPeerConnection();

    console.log( 
        mediaSource.stats, 
        peerConnection.stats
    );
}
```

### contributingSources

```javascript
const storage = monitor.storage;

for (const cssrc of storage.contributingSources()) {
    const peerConnection = cssrc.getPeerConnection();

    console.log( 
        cssrc.stats, 
        peerConnection.stats
    );
}
```

### dataChannels

```javascript
const storage = monitor.storage;

for (const dataChannel of storage.dataChannels()) {
    const peerConnection = dataChannel.getPeerConnection();

    console.log( 
        dataChannel.stats, 
        peerConnection.stats
    );
}
```

### transceivers

```javascript
const storage = monitor.storage;

for (const transceiver of storage.transceivers()) {
    const receiver = transceiver.getReceiver();
    const sender = transceiver.getSender();
    const peerConnection = transceiver.getPeerConnection();

    console.log( 
        transceiver.stats, 
        receiver.stats,
        sender.stats,
        peerConnection.stats
    );
}
```


### senders

```javascript
const storage = monitor.storage;

for (const sender of storage.senders()) {
    const mediaSource = sender.getMediaSource();
    const peerConnection = sender.getPeerConnection();

    console.log( 
        sender.stats,
        mediaSource.stats,
        peerConnection.stats
    );
}
```


### receivers

```javascript
const storage = monitor.storage;

for (const receiver of storage.receivers()) {
    const peerConnection = receiver.getPeerConnection();

    console.log( 
        receiver.stats,
        peerConnection.stats
    );
}
```

### transports

```javascript
const storage = monitor.storage;

for (const transport of storage.transports()) {
    const contributingTransport = transport.getRtcpTransport();
    const selectedIceCandidatePair = transport.getSelectedIceCandidatePair();
    const localCandidate = transport.getLocalCertificate();
    const remoteCandidate = transport.getRemoteCertificate();
    const peerConnection = transport.getPeerConnection();

    console.log( 
        transport.stats,
        contributingTransport?.stats,
        selectedIceCandidatePair?.stats,
        localCandidate?.stats,
        remoteCandidate?.stats,
        remoteCandidate?.stats
    );
}
```

### sctpTransports

```javascript
const storage = monitor.storage;

for (const sctpTransport of storage.sctpTransports()) {
    const transport = sctpTransport.getTransport();
    const peerConnection = sctpTransport.getPeerConnection();

    console.log( 
        sctpTransport.stats,
        transport?.stats,
        peerConnection?.stats,
    );
}
```


### iceCandidatePairs

```javascript
const storage = monitor.storage;

for (const iceCandidatePair of storage.iceCandidatePairs()) {
    const transport = iceCandidatePair.getTransport();
    const localCandidate = iceCandidatePair.getLocalCandidate();
    const remoteCandidate = iceCandidatePair.getRemoteCandidate();
    const peerConnection = iceCandidatePair.getPeerConnection();

    console.log( 
        iceCandidatePair.stats,
        transport?.stats,
        localCandidate?.stats,
        remoteCandidate?.stats,
        peerConnection?.stats,
    );
}
```

### localCandidates

```javascript
const storage = monitor.storage;

for (const localCandidate of storage.localCandidates()) {
    const transport = localCandidate.getTransport();
    const peerConnection = localCandidate.getPeerConnection();

    console.log( 
        localCandidate.stats,
        peerConnection?.stats,
    );
}
```

### remoteCandidates

```javascript
const storage = monitor.storage;

for (const remoteCandidate of storage.remoteCandidates()) {
    const transport = remoteCandidate.getTransport();
    const peerConnection = remoteCandidate.getPeerConnection();

    console.log( 
        remoteCandidate.stats,
        peerConnection?.stats,
    );
}
```

### certificates

```javascript
const storage = monitor.storage;

for (const certificate of storage.certificates()) {
    const peerConnection = certificate.getPeerConnection();

    console.log( 
        certificate.stats,
        peerConnection?.stats,
    );
}
```

### iceServers

```javascript
const storage = monitor.storage;

for (const iceServer of storage.iceServers()) {
    const peerConnection = iceServer.getPeerConnection();

    console.log( 
        iceServer.stats,
        peerConnection?.stats,
    );
}
```

### peerConnections

```javascript
const storage = monitor.storage;

for (const peerConnection of storage.peerConnections()) {

    for (const codec of peerConnection.getCodecs()) 
        console.log(
            `peerConnection(${peerConnection.id}).codec(${codec.id}).stats: `, 
            codec.stats
        );

    for (const inboundRtp of peerConnection.inboundRtps()) 
        console.log(
            `peerConnection(${peerConnection.id}).inboundRtp(${inboundRtp.id}).stats: `, 
            inboundRtp.stats
        );

    for (const outboundRtp of peerConnection.outboundRtps()) 
        console.log(
            `peerConnection(${peerConnection.id}).outboundRtp(${outboundRtp.id}).stats: `, 
            outboundRtp.stats
        );

    for (const remoteInboundRtp of peerConnection.remoteInboundRtps()) 
        console.log(
            `peerConnection(${peerConnection.id}).remoteInboundRtp(${remoteInboundRtp.id}).stats: `, 
            remoteInboundRtp.stats
        );

    for (const remoteOutboundRtp of peerConnection.remoteOutboundRtps()) 
        console.log(
            `peerConnection(${peerConnection.id}).remoteOutboundRtp(${remoteOutboundRtp.id}).stats: `, 
            remoteOutboundRtp.stats
        );

    for (const mediaSource of peerConnection.mediaSources()) 
        console.log(
            `peerConnection(${peerConnection.id}).mediaSource(${mediaSource.id}).stats: `, 
            mediaSource.stats
        );

    for (const cssrc of peerConnection.contributingSources()) 
        console.log(
            `peerConnection(${peerConnection.id}).cssrc(${cssrc.id}).stats: `, 
            cssrc.stats
        );

    for (const dataChannel of peerConnection.dataChannels()) 
        console.log(
            `peerConnection(${peerConnection.id}).dataChannel(${dataChannel.id}).stats: `, 
            dataChannel.stats
        );

    for (const transceiver of peerConnection.transceivers()) 
        console.log(
            `peerConnection(${peerConnection.id}).transceiver(${transceiver.id}).stats: `, 
            transceiver.stats
        );

    for (const sender of peerConnection.senders()) 
        console.log(
            `peerConnection(${peerConnection.id}).sender(${sender.id}).stats: `, 
            sender.stats
        );

    for (const receiver of peerConnection.receivers()) 
        console.log(
            `peerConnection(${peerConnection.id}).receiver(${receiver.id}).stats: `, 
            receiver.stats
        );

    for (const transport of peerConnection.transports()) 
        console.log(
            `peerConnection(${peerConnection.id}).transport(${transport.id}).stats: `, 
            transport.stats
        );

    for (const sctpTransport of peerConnection.sctpTransports()) 
        console.log(
            `peerConnection(${peerConnection.id}).sctpTransport(${sctpTransport.id}).stats: `, 
            sctpTransport.stats
        );

    for (const iceCandidate of peerConnection.iceCandidatePairs()) 
        console.log(
            `peerConnection(${peerConnection.id}).iceCandidate(${iceCandidate.id}).stats: `, 
            iceCandidate.stats
        );

    for (const localCandidate of peerConnection.localCandidates()) 
        console.log(
            `peerConnection(${peerConnection.id}).localCandidate(${localCandidate.id}).stats: `, 
            localCandidate.stats
        );

    for (const remoteCandidate of peerConnection.remoteCandidates()) 
        console.log(
            `peerConnection(${peerConnection.id}).remoteCandidate(${remoteCandidate.id}).stats: `, 
            remoteCandidate.stats
        );

    for (const certificate of peerConnection.certificates()) 
        console.log(
            `peerConnection(${peerConnection.id}).certificate(${certificate.id}).stats: `, 
            certificate.stats
        );

    for (const iceServer of peerConnection.iceServers()) 
        console.log(
            `peerConnection(${peerConnection.id}).iceServer(${iceServer.id}).stats: `, 
            iceServer.stats
        );

    console.log(`peerConnection(${peerConnection.id}) trackIds:`, 
            Array.from(peerConnection.trackIds())
        );
}
```