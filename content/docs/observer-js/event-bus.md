---
slug: "event-bus"
title: "Event bus"
description: "Subscribe centrally and retain the entity ancestry."
lead: "Subscribe centrally and retain the entity ancestry."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 50
toc: true
---
Subscribe on `Observer` to receive typed lifecycle, update, issue and analysis events. Payloads include the relevant parent entities so handlers can identify a call and participant without attaching listeners to every node.

```javascript
observer.on('call-added', ({ observedCall }) => {
  console.log('Call:', observedCall.callId);
});
observer.on('client-issue', ({ observedClient, issue }) => {
  console.log(observedClient.clientId, issue.type);
});
observer.on('sample-rejected', ({ reason }) => {
  console.warn(reason);
});
```

## Issue timing

A client issue raise carries client-clock `raisedAt` and server-clock `observedAt`. Use the server observation time for cross-client onset comparisons. Keyed resolution records close the corresponding issue; keyless issues are one-shot.

## Request context and application state

`context` passed to `accept()` is request-scoped. `appData` belongs to the application and persists on an entity. Neither is a substitute for schema attachments you intend to transmit.

[Complete event names and payload types: ObserverEvents](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/ObserverEvents.ts).
