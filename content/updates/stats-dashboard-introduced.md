---
title: "Introducing the ObserveRTC Stats Dashboard"
date: "2026-08-30T10:08:31Z"
draft: false
project: "Stats Dashboard"
summary: "Browse archived ClientSample data from S3-compatible storage and inspect WebRTC calls, participants, quality timelines and transports."
sourceUrl: "https://github.com/ObserveRTC/stats-dashboard"
sourceLabel: "Explore project on GitHub ↗"
---

## Explore recorded WebRTC calls

The ObserveRTC Stats Dashboard is a diagnostics interface for `ClientSample` data collected by Observer and saved to S3-compatible object storage. It helps you move from a room to a call, then to a participant’s recorded telemetry.

## What you can inspect

- Quality timelines for individual participants.
- ICE candidates and transport state.
- Inbound and outbound RTP statistics.
- Stored samples organized by room, call and client.

Samples use the storage layout:

```text
<bucket>/<roomId>/<callId>/<clientId>.jsonl
```

## Connect your storage

The application supports S3-compatible providers such as AWS S3, MinIO and Cloudflare R2. Storage is configured through environment variables; access credentials stay on the server.

Built with Next.js, React, TypeScript, Zustand and D3, the dashboard can be run locally or deployed against your existing sample archive. The repository includes installation and storage configuration instructions.


---

Source: [Stats Dashboard repository](https://github.com/ObserveRTC/stats-dashboard). Dated from GitHub’s repository creation timestamp (2026-08-30T10:08:31Z); this is a project introduction, not a tagged release.
