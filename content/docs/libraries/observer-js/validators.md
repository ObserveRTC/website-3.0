---
title: "Validators"
slug: "validators"
description: "One-shot structural checks for a WebRTC deployment"
lead: "Detectors ask 'is something wrong right now?'. Validators ask 'is this deployment built correctly?' — and answer once."
date: 2024-01-15T10:00:00+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 325
toc: true
---

Every [detector](../detectors/) runs on every tick, because the answer legitimately changes. A
**validator** answers a question that only changes when you deploy. So it is not configured on and
left running: you **start** one, it runs until it can decide, reports once, and the observer drops
it.

```typescript
observer.addValidator("simulcast-receivers", { minChecks: 5 });

observer.on("validation-ready", ({ validator, report }) => {
    if (!report.ready) return;
    if (report.verdict === "layer-decided-lowest-common-denominator") page(validator, report);
});

onDeploy(() => observer.addValidator("simulcast-receivers"));   // check again
```

`observer.validators` is the set currently running — normally empty, since each removes itself on
finishing. There is no revalidation timer: a deploy, not elapsed time, is what makes a structural
verdict stale, so re-checking means starting another.

## The three shipped validators

| Validator | `addValidator` name | Question | Also raises |
|---|---|---|---|
| `SimulcastReceiverValidator` 🔗 | `simulcast-receivers` | Does the SFU pick layers per receiver, or drag the publisher down to the worst one? | `WORST_RECEIVER_CONTAGION` |
| `RemoteTrackResolverValidator` | `remote-track-resolver` | Is the resolver actually linking anything? | `REMOTE_TRACK_LINKS_UNRESOLVED` |
| `CodecConsistencyValidator` | `codec-consistency` | Is everyone on the same codec — and is it the one you think you negotiated? | `CODEC_INCONSISTENCY` |

🔗 requires a [`RemoteTrackResolver`](../sfu/).

### `SimulcastReceiverValidator`

Simulcast (or SVC) exists so one slow participant does not set everyone's quality: with several
encodings the server hands the struggling receiver a lower layer and leaves the rest alone. Without
it — or with a server that relays RTCP end to end, so the publisher's bandwidth estimate collapses
to the slowest receiver — the only way to serve them is to make the *source* send less.

Both causes look identical from outside. What this check establishes is whether per-receiver
adaptation happens at all.

| `verdict` | Meaning |
|---|---|
| `layer-decided-per-receiver` | Verified — a receiver fell far behind and the publisher carried on |
| `layer-decided-lowest-common-denominator` | The publisher followed its worst receiver; everyone gets the slowest participant's quality |
| `inconclusive` | Cancelled, or the observer closed, before it could decide |

{{< callout context="caution" title="Not finishing is not a pass" icon="alert-triangle" >}}
The check only runs when a publisher has 3+ receivers and one is at most half the median; plenty of
healthy deployments never present that. A validator that never sees it simply keeps running and
never reports — it does **not** quietly succeed.

`report.checks` counts the times the check genuinely ran, so an `inconclusive` with `checks: 0`
says plainly that nothing was verified.
{{< /callout >}}

### `RemoteTrackResolverValidator`

This exists because of a specific, nasty failure mode. Four detectors are built on publisher ↔
subscriber links — `IssueFanOutDetector`, `PublisherFaultCorroborationDetector`,
`TrackDeliveryMismatchDetector`, `UnconsumedTrackDetector` (plus `SimulcastReceiverValidator`) —
and every one of them correctly does *nothing* when the links are missing rather than guessing.

So a resolver wired to the wrong id field leaves all of them permanently silent, and **silence is
what a healthy deployment looks like too**. You would conclude your calls were clean when in fact
nothing was ever examined.

Verdicts: `links-resolved` / `no-links-resolved` / `inconclusive`.

Run it at start-up and after changing the resolver or the SFU's id scheme.

```typescript
observer.addValidator("remote-track-resolver");
```

### `CodecConsistencyValidator`

Answers two things at once.

A **split** — participants of one call on different codecs — is a real fault with a confusing
symptom: an SFU that forwards without transcoding cannot serve them all, so some pairs see each
other and some do not, with no error anywhere. Only something holding every participant at once can
see it.

The quieter half is the **silent fallback**: a deployment configured for VP9 or AV1 drops to VP8
whenever one endpoint cannot negotiate the preference, the call keeps working at a higher bitrate
than budgeted, and the team believes it shipped AV1 months ago. Give it `expected` and it says so.

```typescript
observer.addValidator("codec-consistency", {
    expected: { video: "video/VP9", audio: "audio/opus" },
});
```

Verdicts: `codec-consistent` / `codec-split` / `unexpected-codec` / `inconclusive`.

## Cancelling

A check that has not decided can be stopped, by name or by instance:

```typescript
observer.cancelValidator("simulcast-receivers", "sfu redeployed");

// Or one specific instance — observer.validators holds what is running.
for (const validator of observer.validators) {
    observer.cancelValidator(validator, "shutting down");
}
```

{{< callout context="tip" title="Cancelling is not silent discarding" icon="rocket" >}}
The validator finishes `inconclusive` with your reason, emits `validation-ready` like any other
completion, and removes itself. That matters twice over: anything waiting on the verdict would
otherwise wait forever, and *"we stopped asking"* is a materially different outcome from *"we asked
and learned nothing"* — which is exactly what an `inconclusive` carrying a reason records.

Pass a real reason; the default tells the reader nothing they could not already infer.
{{< /callout >}}

`observer.close()` cancels whatever is still running with `'observer closed'`.

## A start-up validation routine

```typescript
const observer = new Observer({
    createRemoteTrackResolver: createDefaultMediasoupRemoteTrackResolverFactory(),
});

function validateDeployment(reason: string) {
    observer
        .addValidator("remote-track-resolver")
        .addValidator("simulcast-receivers", { minChecks: 5 })
        .addValidator("codec-consistency", { expected: { video: "video/VP9", audio: "audio/opus" } });

    log.info("deployment validation started", { reason });
}

observer.on("validation-ready", ({ validator, report }) => {
    log.info("validation settled", { validator, verdict: report.verdict, checks: report.checks });

    switch (report.verdict) {
        case "no-links-resolved":
            // The most important one: every 🔗 detector is silently doing nothing.
            alerting.page("remote track resolver is not linking anything", report);
            break;
        case "layer-decided-lowest-common-denominator":
            alerting.page("one slow receiver is degrading every participant", report);
            break;
        case "codec-split":
        case "unexpected-codec":
            alerting.page("codec negotiation is not what we configured", report);
            break;
        case "inconclusive":
            log.warn("validation could not decide", { validator, checks: report.checks });
            break;
    }
});

validateDeployment("process start");
onDeploy(() => validateDeployment("deploy"));
```

{{< callout context="note" title="Run these in staging too" icon="info-circle" >}}
All three questions — are the links wired, does per-receiver adaptation work, is the negotiated
codec the intended one — are answerable with a handful of synthetic participants. Validating in
staging catches the wiring mistakes before they turn into a month of silent detectors in
production.
{{< /callout >}}
