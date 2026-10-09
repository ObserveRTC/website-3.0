---
slug: "results"
title: "Inspect monitoring results"
description: "Read the first measurements without confusing unavailable data with a healthy call."
lead: "Read the first measurements without confusing unavailable data with a healthy call."
draft: false
outputs: ["HTML", "Markdown"]
weight: 20
toc: true
---

Your goal is to identify which endpoint and media direction a measurement describes. First run the [connection quick start](/docs/overview/introduction/) with active media.

## Read an updated measurement

1. Read live metrics inside the `stats-collected` callback so you see the latest update.
2. Identify the direction: outbound is what this client sends; inbound is what this client receives.
3. Allow successive collections before expecting an interval rate such as bitrate.
4. Compare the affected track with its peer connection and transport when investigating a change.

`receivingVideoBitrate` is an aggregate received-video rate in bits per second. A change can reflect application choices, sender adaptation, or network/media behavior; the rate alone does not diagnose the cause.

## Use scores and issues together

A score summarizes measured penalties; an issue describes a particular evaluated condition. Read the component's score reasons and related metrics to explain a low score. No active issues does not mean every measurement is available or that every user experiences perfect media.

## Expected result

You can identify the endpoint, direction, and unit of the values in your diagnostics, and distinguish a reported zero from an unavailable field. Continue with [metrics](/docs/client-monitor-js/metrics/), [quality scores](/docs/client-monitor-js/scoring/), and [missing-statistics diagnosis](/docs/guides/missing-statistics/).
