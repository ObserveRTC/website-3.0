---
slug: "detectors-transport-quality"
title: "Transport Quality detectors"
description: "Delay, loss, congestion and stalled media transport."
lead: "Delay, loss, congestion and stalled media transport."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 82
toc: true
---

| Class | Default / trigger | Recovery / state |
|---|---|---|
| [CongestionDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/CongestionDetector.ts#L77) | deprecated sensitivity medium; legacy RTT/loss/limitation heuristic | legacy congested flag and max-baseline bookkeeping; not interchangeable with directional detectors |
| [UplinkCongestionDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/UplinkCongestionDetector.ts#L95) | browser bandwidth-limited verdict AND severity≥0.65; severity = sqrt(BWE undershoot × pacer bloat); bloat saturates at 4×median | closes when browser stops reporting bandwidth limitation or send path stands down; decaying max and median baselines |
| [DownlinkCongestionDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DownlinkCongestionDetector.ts#L105) | inbound video; severity≥0.65 = sqrt(receive-bitrate undershoot × video jitter-buffer bloat), 4×median saturation | below half minSeverity (0.325 default), or no inbound video; separate baselines |
| [TransportDelayDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/TransportDelayDetector.ts#L70) | detection-window mean current RTT≥300 ms | recovery-window RTT<200 ms or no measurement; RTCP/ICE source retained |
| [TransportLossDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/TransportLossDetector.ts#L47) | max available inbound/outbound mean loss≥0.05 for 6000 ms | loss<0.01; hysteresis between thresholds |
| [BlockedStunRequestsDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/BlockedStunRequestsDetector.ts#L52) | succeeded pair sends requests/consent checks but no responses for 10000 ms | response arrives/path unverified/no request evidence; separate 10000 ms request timeout; issue is blocked-stun-requests, event remains blocked-transport |
| [BlockedOutboundMediaDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/BlockedOutboundMediaDetector.ts#L50) | actual outgoing RTP, STUN answers, fresh remote receiver reports stop for 10000 ms | reports resume, no sending or no usable path; absent RTCP is evidence with the other gates, not proof of a particular firewall |
| [BlockedInboundMediaDetector](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/BlockedInboundMediaDetector.ts#L58) | **default null**; sender-report evidence advances while inbound media does not, for configured threshold | reception resumes/no sending or no usable path; enable only where evidence is meaningful |

Directional formulas and baseline update order: [client-monitor-js/src/detectors/UplinkCongestionDetector.ts · update](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/UplinkCongestionDetector.ts#L129), [client-monitor-js/src/detectors/DownlinkCongestionDetector.ts · update](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/src/detectors/DownlinkCongestionDetector.ts#L138). The baseline is read before feeding the current observation; medians stop learning while an issue is open. These are not generic packet-loss thresholds.
