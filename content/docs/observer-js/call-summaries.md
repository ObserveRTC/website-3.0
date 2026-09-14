---
title: "Call summaries"
description: "The one record that outlives a call"
lead: "Everything else in the library is about now. A summary is what support, billing and the incident note ask about afterwards"
date: 2026-09-13T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 355
toc: true
---

Detectors answer "is something wrong right now", validators answer a structural question once, and
both read state the call throws away when it ends. A **call summary** is the one thing that
outlives the call: who was in it, what was raised against it, how it scored.

```typescript
const observer = new Observer({
    callSummary: {
        include: ['clients', 'issues', 'turnServers', 'scores'],
    },
});

observer.on('call-summary', ({ summary }) => archive(summary));
```

Omit `callSummary`, or set it to `null`, and there are no summaries and **not one extra bus
subscription**. Pass an object — `{}` is valid — and every call this observer creates carries one.

{{< callout context="note" title="Why construction-time, when detectors are added per call?" icon="info-circle" >}}
A summary is a record of what happened, and **a record you can switch on halfway through is a record
with a hole in it**. Calls that started before the switch would carry different sections from calls
that started after, with nothing on either to say which. One shape for every call, or none.
{{< /callout >}}

## Sections are opt-in, and absence means "not collected"

`include` picks from four built-ins, and **the default is `[]`** — none of them:

| Section | Contains |
|---|---|
| `clients` | `clientIds` (join order), `peak`, `joined`, `left`. Identifiers and counts only |
| `issues` | `CallIssue[]`, in the order raised, capped by `maxIssues` |
| `turnServers` | `serverUrls` that carried media, and `clientsRelayed` |
| `scores` | `min` / `max` / `median` of the call score, and `samples` |

{{< callout context="caution" title="A missing section means it was never collected" icon="alert-triangle" >}}
Never "nothing happened". Reading `summary.issues === undefined` as "this call was clean" is the one
misreading this type invites, so **there is no default-empty section to make it easy**. Same rule as
`inconclusive` on a validator: silence is not success.
{{< /callout >}}

The `clients` section is deliberately identifiers and counts. Anything *about* a client — browser,
platform, region — is already on `observedClient` while the call is live, and belongs in
`attachments` via an enricher if you want it kept.

## Enrichers: fold in anything, from any call-scoped event

```typescript
new Observer({
    callSummary: {
        include: ['issues'],
        enrich: {
            'client-joined': (summary, { observedClient }) => {
                // serialisable facts only — the region string, never the live object it came from
                ((summary.attachments.regions ??= []) as string[]).push(String(observedClient.appData.region));
            },
        },
    },
});
```

Each enricher is typed against its own event's payload. **Only call-scoped events are accepted** —
the ones carrying an `observedCall`. An enricher on `observer-issue` or `validation-ready` will not
compile, because there is no single call to attribute a fleet-wide fact to, and quietly writing it
into every open summary would be worse than a type error.

The library never writes to `summary.attachments`, so nothing you put there can collide with a
section added in a future version.

{{< callout context="tip" title="Why attachments and not appData" icon="rocket" >}}
`appData` is live working state hung off an entity for that entity's lifetime, and it may hold things
that cannot be serialised — a mediasoup router, a socket. A summary is the opposite: it exists to be
**shipped**, and it reaches you while the call it describes is being torn down, so an unserialisable
value in it points at something already gone.

Read the live object off `observedCall` / `observedClient` in the enricher, attach what serialises —
the router's `id`, not the router. An enricher that throws is logged and skipped: a summary is a
side-channel, and nothing about a call should break because a field could not be recorded.
{{< /callout >}}

## Caps announce what they dropped

`maxIssues` (default `500`) and `maxClientIds` (default `10_000`) bound the two unbounded lists.
When either bites, `summary.truncated` appears with the shortfall — present **only** when something
was actually dropped.

That is what makes dropping safe: the true count stays recoverable as
`issues.length + (truncated?.issues ?? 0)`. **A silently truncated summary is worse than no
summary**, because someone will count `issues.length` and report it as the issue count.

`issues` is the plain array, with no derived tallies alongside it. A count is `issues.length` and a
per-type count is one `filter` — both cheaper at the call site than kept correct here.

## Reading it

```typescript
observedCall.summary;   // live: read it at any point during the call

observer.on('call-summary', ({ observedCall, summary }) => archive(summary));
```

`call-summary` is emitted **inside `close()`**, while the call is still in `observer.observedCalls` —
after that the call is gone and there is nothing left to ask. `observer.close()` closes its calls
first and its collector afterwards, so every summary still makes it out.

Cost is **one bus listener per subscribed event type, for the whole observer** — not one per call. A
per-call design would be quadratic in concurrent calls: at 500 calls and eight events, 4,000
listeners each doing 500 no-op invocations per event. Percentiles are computed once, at close.

{{< callout context="caution" title="Watch the teardown timeouts" icon="alert-triangle" >}}
`closeCallIfEmptyForMs` set too low **splits one meeting into several calls**, each emitting its own
`call-summary`. `closeClientIfIdleForMs` set too low re-creates a paused participant as a *new*
client, splitting one person into two in the `clients` section.
{{< /callout >}}
