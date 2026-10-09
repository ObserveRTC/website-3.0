---
slug: "configuration"
title: "Configuration"
description: "Configuration for engineers integrating ObserveRTC."
draft: false
outputs: ["HTML", "Markdown"]
weight: 20
toc: true
---
Observer settings control how long live calls remain in memory, when analysis runs, and how your application enriches and stores data. They do not configure your HTTP endpoint or authentication.

## Start with a lifecycle policy

```javascript
const observer = new Observer({
  closeClientIfIdleForMs: 60000,
  closeCallIfEmptyForMs: 60000,
  autoUpdateOnCallUpdate: true,
});
```

At a five-second client sampling cadence, a 60-second idle timeout tolerates several missed samples. Choose a timeout that covers normal reconnects and background-tab delays. An overly short timeout can close and recreate the same participant; an overly long one retains abandoned clients and affects aggregate counts.

## Lifecycle and update options

| Option | Default | What it controls |
|---|---|---|
| `closeClientIfIdleForMs` | `60000` | How long a client can stop sending samples before it closes. |
| `closeCallIfEmptyForMs` | `60000` | How long an empty call stays open to allow reconnects. |
| `autoUpdateOnCallUpdate` | `true` | Run Observer-wide updates when a call changes. If disabled, drive `observer.update()` yourself. |
| `appData` | Application supplied | Local application state on the Observer. |

The defaults apply when options are omitted. In the verified baseline, explicitly supplying `undefined` for a timeout disables that timeout; it is different from omitting the key. Use a deliberate lifecycle policy and close abandoned entities yourself if automatic cleanup is disabled.

## Application factories

| Option | Use it to |
|---|---|
| `createCallAppData` | Attach application state when a call is first created. |
| `createClientAppData` | Attach participant/client state at creation. |
| `createClientSink` | Choose a per-client destination for accepted samples. |
| `createRemoteTrackResolver` | Match a received track to its publisher using signaling identifiers. |

Factories let you use call/client identity and creation context instead of pre-creating every entity. Request context passed to `accept()` is temporary; application state and sampled attachments serve different purposes.

## Track degradation thresholds

`inboundTrackDegradationThresholds` and `outboundTrackDegradationThresholds` mark tracks using measured values. These flags help compare receivers and publishers; they are separate from client detector issues and their sustained-evidence rules.

| Configuration | Available fields |
|---|---|
| `inboundTrackDegradationThresholds` | `deltaFreezeCount`, `framesDroppedRatio`, `jitterBufferDelayInMs`, `concealmentRatio`, `rttInMs` |
| `outboundTrackDegradationThresholds` | `fractionLost`, `rttInMs` |

Thresholds are exclusive upper bounds: a value must be greater than the configured threshold. Ratios are fractions, and delay/RTT fields here are milliseconds. Choose values from observed sessions rather than copying one universal threshold for all regions and devices. Inbound threshold flags are off unless configured. Outbound tracks can still report encoder quality limitation or no packets sent independently of these thresholds.

## Call summaries and detectors

`callSummary` is off when omitted or `null`. Supply an object to enable it from construction, and select the sections you want through `include`; an empty object does not automatically include every section. Read [call summaries](/docs/observer-js/call-summaries/) for the supported sections and enrichment hooks.

Server detectors are registered separately, at call or Observer scope. Configure them for the question you want to answer, such as whether several participants share a failing publisher. See [server detectors](/docs/observer-js/detectors/).

[Verified Observer configuration source](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/Observer.ts).
