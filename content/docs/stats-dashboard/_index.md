---
title: "Stats Dashboard"
landingTitle: "What is Stats Dashboard?"
description: "Explore recorded WebRTC calls, participants, and telemetry from object storage."
lead: "Move from a reported call problem to the recorded evidence."
draft: false
outputs: ["HTML", "Markdown"]
weight: 35
toc: false
---

Stats Dashboard is ObserveRTC's interface for investigating recorded WebRTC sessions. Browse a room, choose a call and participant, and inspect quality timelines, transport state, RTP measurements, and reported issues. It reads archived telemetry rather than replacing Client Monitor or Observer.

{{< component-flow from="Collect and analyze" fromText="Client Monitor reports endpoint observations; Observer processes samples." via="Archive telemetry" viaText="Your backend writes ClientSample JSONL files to S3-compatible storage." to="Investigate a call" toText="Stats Dashboard reads the archive and presents the recorded evidence." caption="The dashboard consumes stored telemetry; it does not collect browser statistics." >}}

## Start with your archive

The documented client stream layout is:

```text
<bucket>/<roomId>/<callId>/<clientId>.jsonl
```

Use S3-compatible storage such as AWS S3, MinIO, or Cloudflare R2. Configure access on the dashboard server; storage credentials do not belong in browser code. Follow the repository's [getting-started and storage instructions](https://github.com/ObserveRTC/stats-dashboard/tree/323a1b28553758edafaa0abd0d4211c9e13de9ea#getting-started).

The dashboard is a separate Next.js application. Installing the monitoring libraries does not install or deploy it. Optional mediasoup router data supports additional SFU diagnostics; client samples alone do not provide every server-side relationship.

## Versions and compatibility

The reviewed package declares **0.1.0**, at commit `323a1b28553758edafaa0abd0d4211c9e13de9ea`. As of October 13, 2026, GitHub lists no published releases for the repository. This is a package/source version, not a claim that a release tag exists.

Its schema source documents a target of Client Monitor JS 4.9.0 and later with sample schema 3.7.0, plus normalization of selected older payload/reason representations. This is not a guarantee that every historical schema or native client provides all displayed fields.

See the [compatibility matrices](/docs/reference/versions/) before choosing a producer/Observer/dashboard combination. Native C++ samples share the 3.7.0 contract, but native detector and scoring coverage is partial and dashboard integration is not independently verified here.

Sources: [package version](https://github.com/ObserveRTC/stats-dashboard/blob/323a1b28553758edafaa0abd0d4211c9e13de9ea/package.json), [sample contract](https://github.com/ObserveRTC/stats-dashboard/blob/323a1b28553758edafaa0abd0d4211c9e13de9ea/src/schema/ClientSample.ts), and [fixture tests](https://github.com/ObserveRTC/stats-dashboard/blob/323a1b28553758edafaa0abd0d4211c9e13de9ea/scripts/realFixture.test.ts). These are source references; the dashboard was not run as part of the website checks.
