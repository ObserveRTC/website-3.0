---
title: "Client Monitor C++ 0.3.0"
date: "2026-10-19T07:21:01Z"
draft: false
project: "Client Monitor C++"
version: "0.3.0"
summary: "Correct libwebrtc timestamp units, client-level stats adapters, and outbound track tracking fixes. Includes breaking API and sample timestamp changes."
releaseUrl: "https://github.com/ObserveRTC/client-monitor-cpp/releases/tag/v0.3.0"
author: "balazskreith"
---

## Correct timestamp units

`LibWebRtcStatsAdapter` now converts libwebrtc's microsecond stats timestamps to milliseconds. Previously, elapsed times were interpreted as 1,000 times too long, calculated rates were 1,000 times too low, and time-based detector thresholds could be crossed after a single collection.

**Change for sample consumers:** stats-object timestamps inside `peerConnections[]` now use epoch milliseconds, matching browser-produced samples. Sample-level timestamps and the timestamps of client events, issues, and metadata remain in milliseconds, as before. Consumers handling both older and newer C++ clients need to account for the different units; see the release notes' **Sample timestamps** migration guidance.

## Move stats adapters to the client monitor

**Breaking API change:** `PeerConnectionMonitor::AddStatsAdapter()`, `RemoveStatsAdapter()`, and `Collect()` are removed. Manage adapters through `ClientMonitor::AddStatsAdapter()`, `RemoveStatsAdapter()`, and `GetStatsAdapter()`, and collect through `ClientMonitor::Collect()`. The adapter signature is now `Adapt(peerConnectionId, stats)`.

Collection reports raw stats through the new `Listener::OnRawStats()` callback before applying adapters. The client monitor includes a `LibWebRtcStatsAdapter` by default.

## Keep outbound tracks attached to current streams

Outbound tracks refresh their stream associations on every report, including reports with repeated timestamps. A new `DetachedSenderStatsAdapter` clears stale media-source references for senders without a track; the mediasoupclient binding supplies the sender state for send transports.

These changes prevent a sending track from being associated with a closed sender's streams and incorrectly raising `dry-outbound-track`. Reusing an ended track's ID also creates a fresh monitor instead of retaining the ended track's state.

Source: [Client Monitor C++ 0.3.0 release notes](https://github.com/ObserveRTC/client-monitor-cpp/releases/tag/v0.3.0). Date is GitHub's release publication timestamp.
