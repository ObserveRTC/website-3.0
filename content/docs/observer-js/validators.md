---
slug: "validators"
title: "Validators"
description: "Check structural behavior from observed evidence."
lead: "Check structural behavior from observed evidence."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 75
toc: true
---

A validator checks a specific expectation over a limited period. Use one when your application wants to confirm that an operation worked, rather than continuously watching for a recurring problem. Detectors and validators therefore have different lifetimes.

Validators run on Observer updates until they can produce a report or are cancelled. An absence of evidence is not a successful validation.

## Available validators

| Validator | Question |
|---|---|
| `SimulcastReceiverValidator` | Do receivers independently select layers? |
| `RemoteTrackResolverValidator` | Can publisher/subscriber relationships be resolved? |
| `CodecConsistencyValidator` | Is codec behavior consistent across the observed endpoints? |

## Update lifecycle

Keep validators separate from continuing issue detectors. Ensure Observer updates run when disabling automatic updates.

Sources: [Validator](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/validators/Validator.ts), [available validators](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/src/validators/Validators.ts).
