---
slug: "detection"
title: "Detector evaluation and issue lifecycles"
description: "Understand when evidence becomes an active condition."
lead: "Understand when evidence becomes an active condition."
draft: false
outputs: ["HTML", "Markdown"]
weight: 30
toc: true
---

A detector checks a particular condition using available measurements and state. Some detectors report observations; others open an issue and later resolve it. Their output is evidence about that condition, not a universal diagnosis of the call.

## Evaluate sustained evidence

Many conditions need several observations to distinguish a persistent problem from a short fluctuation. Detection windows collect recent values; recovery windows help determine when a condition has settled. Other detectors use explicit elapsed-time thresholds or immediate state transitions.

Changing collection cadence changes how much time a window covers. It does not necessarily change every detector's independent timer. See [configuration](/docs/client-monitor-js/configuration/) for window sizes and tuning consequences.

## Follow a stateful issue

```text
Eligible observations → condition confirmed → keyed issue raised
                                             ↓
                                      evidence updated
                                             ↓
                                      recovery confirmed
                                             ↓
                                        issue resolved
```

The issue key identifies the active occurrence. Several tracks can have the same issue type, so the type alone is not a unique key. One-off issue records do not have this ongoing lifecycle.

## Distinguish absent evidence

If required statistics are unavailable, or the application intentionally pauses a track, evaluation can be gated. An inactive detector or missing input is not equivalent to a healthy measurement. Read each detector's guards and limitations before treating its output as a guarantee.

Use [monitor issues](/docs/client-monitor-js/monitor-issues/) for lifecycle handling and [server ingestion](/docs/observer-js/ingestion/) for mirrored client issues.
