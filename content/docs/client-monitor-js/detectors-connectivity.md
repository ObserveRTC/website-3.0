---
slug: "detectors-connectivity"
title: "Connectivity detectors"
description: "Connection establishment, handshake failures and path changes."
lead: "Connection establishment, handshake failures and path changes."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 81
toc: true
---

| Class | Default / trigger | Recovery / state |
|---|---|---|
| [IceReachabilityDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceReachabilityDetector.ts#L49) | gathering complete, no local candidates, never connected; failing state or 6000 ms wait | candidates appear, connected, or closed; remembers prior success |
| [IcePathEstablishmentDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IcePathEstablishmentDetector.ts#L43) | connection stays connecting ≥5000 ms; emits slow-stage event | resets outside connecting; event once per episode |
| [IceEstablishmentFailedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceEstablishmentFailedDetector.ts#L57) | candidates exist, no historical connected/succeeded/nominated path, sustained 15000 ms | established path or closed; distinguishes no-network from failed establishment |
| [DtlsHandshakeFailedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DtlsHandshakeFailedDetector.ts#L38) | dtlsState failed, immediate | connected or transport removed; per-transport raise map |
| [DtlsHandshakeStalledDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DtlsHandshakeStalledDetector.ts#L61) | DTLS new/connecting while real ICE evidence is healthy for 6000 ms | connected/failed/removal; generation and missing-evidence paths reset accumulation |
| [IceDisconnectedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceDisconnectedDetector.ts#L57) | per-transport disconnected for 5000 ms | connected/completed, ICE restart or removal |
| [IceConnectionFailedDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceConnectionFailedDetector.ts#L51) | per-transport failed immediately | connected/completed, restart or removal |
| [IceTransportStalledDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/IceTransportStalledDetector.ts#L65) | succeeded connected path previously received data; sends but no inbound, expected inbound media, 5000 ms | inbound resumes, connectivity lost, restart/removal; send-only/paused situations gated |
| [UnstableIcePathDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/UnstableIcePathDetector.ts#L60) | at least 3 switches in 30000 ms observation window | completed quieter window or transport removal |

Each row links through its named class in [client-monitor-js/src/detectors/Detector.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/Detector.ts) and the [detector implementation reference](/reference/detector-implementation-reference.md); connectivity state machine context is in [client-monitor-js/src/monitors/SelectedIcePath.ts](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/monitors/SelectedIcePath.ts).
