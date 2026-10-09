---
slug: "monitor-events"
title: "Monitor events"
description: "Monitor events for engineers integrating ObserveRTC."
draft: false
outputs: ["HTML", "Markdown"]
weight: 65
toc: true
---

Events let your application react while a call is running. Listen for a completed collection to refresh a diagnostics view, for a created sample to forward data, or for an issue to show a warning.

## Listen to local updates

```javascript
monitor.on('stats-collected', () => {
  console.log(monitor.receivingVideoBitrate);
});
monitor.on('sample-created', ({ sample }) => {
  sendSample(sample);
});
```

| Event | Use it for |
|---|---|
| `stats-collected` | Read freshly updated live metrics. |
| `sample-created` | Forward a serializable sample to your backend. |
| `issue` | React to a newly reported problem. |
| `issue-updated` | Refresh details of an ongoing problem. |
| `issue-resolved` | Clear a warning when its problem ends. |
| `score` | Refresh a quality indicator and inspect its reasons. |

Local callbacks can contain live monitor objects. Send a `ClientSample` to your backend rather than serializing arbitrary callback payloads.

## Record an application event

Application events explain what happened in your product, such as a user joining or an application action changing the call. They are distinct from local callbacks. `addEvent()` records a serializable `ClientEvent` for samples.

Automatic sampling normally buffers these records. If you disable automatic sampling and create samples yourself, set `bufferingEventsForSamples: true`. With both mechanisms disabled, `addEvent()` neither buffers the record nor emits `client-event`.

See [application context](/docs/client-monitor-js/application-context/) for attachments and extension measurements, and [monitor issues](/docs/client-monitor-js/monitor-issues/) for problem lifecycles.

[Complete event payload reference](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitorEvents.ts).
