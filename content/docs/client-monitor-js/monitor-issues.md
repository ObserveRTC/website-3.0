---
slug: "monitor-issues"
title: "Monitor issues"
description: "Monitor issues for engineers integrating ObserveRTC."
draft: false
outputs: ["HTML", "Markdown"]
weight: 70
toc: true
---

An issue describes a problem, such as a stalled media stream or an unhealthy connection. A stateful issue stays active until its evidence recovers; an event simply records that something happened.

## Respond to problems

```javascript
monitor.on('issue', issue => {
  console.log('Problem:', issue.type, issue.payload);
});
monitor.on('issue-resolved', issue => {
  console.log('Resolved:', issue.type);
});
```

Use the type to choose an explanation in your UI, and the payload to understand the evidence. Multiple tracks can have the same kind of problem at once, so track the issue key rather than treating the type as a unique identifier.

## One-off reports and ongoing problems

`addIssue()` records a one-off finding. `raiseIssue()` opens a keyed problem and `resolveIssue()` closes it. Updating an active issue refreshes its local details without creating a new sampled issue on every collection.

## Report lifecycles to the server

`sendResolvedIssuesToServer` defaults to `true`. A stateful raise and its resolution share a key; resolution uses a type ending in `-resolved`. This lets Observer mirror active problems instead of retaining a warning after recovery.

A detector’s `includeIssueInSample: false` keeps local reporting while excluding its issue records from samples. Issue buffering also depends on automatic sampling or `bufferingEventsForSamples`; local issue callbacks are independent of that buffer.

Choose thresholds in [configuration](/docs/client-monitor-js/configuration/) and read the evidence in the [detector catalog](/docs/client-monitor-js/detectors/).

Sources: [client-monitor-js/src/ClientMonitorEvents.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitorEvents.ts), [client-monitor-js/src/ClientMonitorIssues.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitorIssues.ts), [client-monitor-js/src/utils/IssueRegistry.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/utils/IssueRegistry.ts), [client-monitor-js/src/ClientMonitor.ts · _raiseIssue](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1260), [client-monitor-js/src/ClientMonitor.ts · _updateIssue](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1278), [client-monitor-js/src/ClientMonitor.ts · _resolveIssue](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/ClientMonitor.ts#L1286).

