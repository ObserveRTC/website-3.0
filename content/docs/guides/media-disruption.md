---
slug: "media-disruption"
title: "Investigate media disruption"
description: "Find where capture, delivery, decoding, or playout stops progressing."
lead: "Find where capture, delivery, decoding, or playout stops progressing."
draft: false
outputs: ["HTML", "Markdown"]
weight: 40
toc: true
---

Use this guide for frozen video, silent audio, or media that unexpectedly stops. Confirm the affected client and track, and whether the application expects that track to be active.

## Trace progress

1. Check pause, mute, track-ended state, and declared application context.
2. For sending media, compare capture progress, encoded frames, and sent bytes/packets.
3. For receiving media, compare incoming bytes, complete frames, decoded frames, and rendered/played output where available.
4. Locate the earliest stage that lacks progress while its preceding stage still advances.
5. Read the matching detector's input requirements, duration thresholds, and recovery rules.

## Interpret the evidence

Incoming bytes without decoded frames differs from decoded frames without playout. A frozen picture alone cannot tell you which stage failed. Audio concealment and interruptions describe different evidence from intentional microphone silence.

## Respond and confirm recovery

Use the narrowed stage to investigate the application's media lifecycle, device behavior, or connection. Choose remedial actions in your application; detection alone does not recreate a consumer or capture device. Confirm progress resumes and any stateful issue resolves.

If the browser lacks required fields, retain that uncertainty and compare application logs or other endpoints.

[Pipeline detectors](/docs/client-monitor-js/detectors-pipeline/) · [Perceived quality detectors](/docs/client-monitor-js/detectors-perceived-quality/) · [Application context](/docs/client-monitor-js/application-context/).
