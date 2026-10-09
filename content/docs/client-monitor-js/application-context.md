---
slug: "application-context"
title: "Application context"
description: "Application context for engineers integrating ObserveRTC."
draft: false
outputs: ["HTML", "Markdown"]
weight: 60
toc: true
---

Application context tells the monitor what your application expects. A paused camera and a camera that unexpectedly stops sending may produce similar statistics, but they should lead to different conclusions.

## Describe a track

```javascript
monitor.setOutboundTrackContext(track.id, {
  contentType: 'screenshare',
  paused: false,
});
```

Use the actual media track identifier. Keep context up to date when your application changes its intent, such as pausing or resuming a track. Context can be supplied before the monitor discovers the track.

## Available context

| Direction | Context fields | Why you would supply them |
|---|---|---|
| Inbound | `contentType`, `paused`, `remoteOutboundTrackPaused` | Tell the monitor what kind of media this is and whether either side intentionally paused it. |
| Inbound video | `motionType`, `presentedResolution`, `videoTag` | Describe the expected motion and displayed video so detectors can evaluate what the user sees. |
| Inbound audio | `linkedVideoTrackId` | Identify the corresponding video track for audio/video synchronization checks. |
| Outbound | `contentType`, `paused` | Describe what you are sending and whether sending is intentionally paused. Capture settings provide additional evidence. |

Context updates merge with existing values. Pass `undefined` for a field to clear it. Supply the actual paired video track identifier rather than guessing from another participant. A `videoTag` is a local element reference, not something to serialize to your backend.

{{< details "Source references" >}}

- [client-monitor-js/src/monitors/InboundTrackMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/InboundTrackMonitor.ts)
- [client-monitor-js/src/monitors/OutboundTrackMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/OutboundTrackMonitor.ts)
- [client-monitor-js/src/ClientMonitor.ts · setInboundTrackContext](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1154)

{{< /details >}}

## Local state and attachments

`appData` is local arbitrary working state. `attachments` is the explicit serializable envelope. Track `createSample()` sends `id`, `kind`, `timestamp`, `attachments`, `score` and reasons; it does not automatically send the context object, HTML element, flags or all derived metrics. Put required backend application context into an appropriate serializable contract explicitly.

## Application measurements

Use `addExtensionStats({ type, payload, id })` when you have application measurements beyond browser WebRTC stats. It updates an identified local `ExtensionStatsMonitor`; providers can also supply measurements during collection.

When automatic sampling or `bufferingEventsForSamples` is enabled, the measurement is buffered for a sample and `extension-stats` is emitted. The sample entry contains `type` and `payload`; the optional local monitor `id` is not included in that entry. Put any identifier your backend needs into your explicit payload contract.

These local monitors expire as measurements become stale. They do not provide historical storage. `getExtensionStatsPayload<T>` gives a TypeScript type assertion, so validate externally supplied data yourself. Observer receives these records through `client-extension-stats` events rather than reconstructing the browser's local extension-monitor registry.

{{< details "Source references" >}}

- [client-monitor-js/src/ClientMonitor.ts · addExtensionStats](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L983)
- [client-monitor-js/src/monitors/ExtensionStatsMonitor.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/ExtensionStatsMonitor.ts)
- [observer-js/src/ObservedClient.ts · addExtensionStats](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObservedClient.ts#L570)

{{< /details >}}


