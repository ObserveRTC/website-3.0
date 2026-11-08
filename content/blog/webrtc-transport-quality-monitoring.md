---
title: "WebRTC Monitoring: The Packets Must Flow"
slug: "webrtc-transport-quality-monitoring"
date: 2026-11-08
draft: false
description: "Investigate WebRTC transport quality with directional congestion, round-trip time, packet loss, and blocked-delivery detectors."
summary: ""
tags: ["WebRTC", "Monitoring", "Transport quality"]
contributors: []
---

In [Are We Connected?](/blog/webrtc-connectivity-monitoring/), we followed the connection from gathering candidates to keeping an established path alive. Now the participant has joined. ICE is connected, DTLS completed, and the camera preview looks fine. Then someone says, “You're breaking up.”

Are we trying to send more than the path can carry? Are packets missing? Are they taking too long to arrive? Are they arriving steadily or in bursts?

A congestion controller can reduce the video bitrate before packets start disappearing. A longer network path can increase round-trip time without losing packets. A wireless link can lose packets without filling a queue.

{{< blog-figure src="/images/blog/webrtc-transport-quality-monitoring/transport-questions.svg" alt="Bandwidth, delay, delivery, and stability are concurrent questions about an established path." >}}

*Figure 1. Four properties of the same path, measured alongside one another.*

The [Client Monitor taxonomy](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/docs/DETECTOR_TAXONOMY.md) calls this **Transport Quality**. Connectivity asks whether the path exists and holds. Pipeline Disruption compares stages inside the media chain, such as encoded frames and outgoing packets. Perceived Quality watches consequences such as concealed audio or disrupted video. Telemetry records changes—a selected route or simulcast layer, for example—without calling each change a fault.

These categories organize the evidence; individual detectors have their own input requirements. In a call that uses an SFU, these measurements describe the connection between this endpoint and the SFU. Correlate both participants’ connections before drawing conclusions about delivery between them.

## Bandwidth: do we have enough?

### Case 1: I look fine from here

The participant sees a smooth local preview, but everyone else sees their video become choppy, then blurry and pixelated. Their application is still producing video. The useful distinction is whether the device cannot encode the requested video fast enough, or the available bandwidth cannot support the outgoing bitrate. Lowering resolution might help either, but it wouldn't explain which one happened.

The browser's [`qualityLimitationReason`](https://www.w3.org/TR/webrtc-stats/#dom-rtcoutboundrtpstreamstats-qualitylimitationreason) distinguishes bandwidth limitation from CPU limitation. It describes what is limiting outbound video resolution or frame rate. The separate [`availableOutgoingBitrate`](https://www.w3.org/TR/webrtc-stats/#dom-rtcicecandidatepairstats-availableoutgoingbitrate) is the congestion controller's estimate of available outgoing RTP bitrate, not a speed test of the participant's access link. Client Monitor combines the limitation reason with changes in that estimate and local packet buffering.

#### Uplink congestion detector

Client Monitor's [`UplinkCongestionDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/UplinkCongestionDetector.ts) combines the browser's `bandwidth` limitation report with a falling outgoing bitrate estimate and increasing local packet-send delay. Together, these indicate that the sending path is struggling to carry the outgoing traffic, raising **`uplink-congestion`**. Packet-send delay describes [local buffering before packets reach the network socket](https://www.w3.org/TR/webrtc-stats/#dom-rtcoutboundrtpstreamstats-totalpacketsenddelay), rather than delay inside the network.

{{< blog-figure src="/images/blog/webrtc-transport-quality-monitoring/uplink.svg" alt="Watching raises on bandwidth limitation and sufficient severity. Raised returns when sending stops or the bandwidth verdict ends. Missing inputs hold the state." >}}

*Figure 2. Uplink issue resolution follows the browser’s bandwidth-limitation report.*

The issue clears when the browser no longer reports bandwidth limitation or sending stops. Reduced packet-send delay alone doesn't close it while that limitation remains. The detector needs outbound video measurements, so it cannot assess audio-only calls or browsers that omit those inputs; missing measurements don't establish recovery.

### Case 2: the whole room goes blurry

Now the local participant looks fine to everyone else, but several remote videos deteriorate on their screen. I would look at the receiving connection before asking every remote sender to restart its camera. Still, a fall in received bitrate isn't enough: the application might have selected smaller layers or paused off-screen videos. We need evidence that delivery is struggling too.

#### Downlink congestion detector

Client Monitor's [`DownlinkCongestionDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/DownlinkCongestionDetector.ts) combines falling received bitrate with increasing video jitter-buffer delay. Receiving less data alone could reflect a deliberate layer change; frames spending longer in the buffer add evidence of delivery problems. When the combined indication is strong enough, it raises **`downlink-congestion`**. It uses [video jitter-buffer measurements](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay) and works on receive-only video connections.

{{< blog-figure src="/images/blog/webrtc-transport-quality-monitoring/downlink.svg" alt="Congestion detection raises an issue. Sufficiently reduced severity or removal of inbound video clears it. Missing buffer measurements preserve the issue." >}}

*Figure 3. Downlink congestion has a separate, lower recovery threshold.*

The issue clears when the combined indication has eased sufficiently or inbound video is no longer present. It needs video-buffer measurements, so audio-only calls and missing buffer data leave it unable to assess the condition. Buffer delay can also change with synchronization or application buffering targets; the finding doesn't identify a congested network hop.

## Delay: this long-distance thing isn’t working

### Case 1: I thought you’d finished

Nobody is dropping out, but the conversation keeps colliding. A participant finishes speaking, waits, then starts just as the other person answers. We should check round-trip time even if loss is low and the outgoing bitrate estimate looks sufficient. A distant relay is one possible explanation; a queue or a different route is another. The measurement should come before the remedy.

#### Transport delay detector

Client Monitor's [`TransportDelayDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/TransportDelayDetector.ts) watches round-trip time (RTT) over a recent observation window and raises **`transport-delay-degraded`** when the mean is too high. It prefers fresh [RTCP RTT measurements](https://www.w3.org/TR/webrtc-stats/#dom-rtcremoteinboundrtpstreamstats-roundtriptime), falling back to STUN RTT on the selected ICE path. These measure protocol round-trip time, not capture-to-playback latency; the RTCP endpoint may be the SFU rather than the other participant.

{{< blog-figure src="/images/blog/webrtc-transport-quality-monitoring/delay.svg" alt="High mean RTT in a ready detection window raises an issue. The recovery reading or loss of measurable RTT can clear it." >}}

*Figure 4. Delay uses sample windows, with a separate recovery reading.*

Recovery uses a lower threshold and, when available, the preceding observation window to avoid closing the issue on a brief improvement. Losing all usable RTT measurements also clears the finding, but that means it can no longer be assessed—not that delay recovered. Keep the measurement source alongside the finding when comparing RTT over time.

## Delivery: did you get that?

### Case 1: most of it, apparently

The conversation continues, but the audio intermittently cuts out. Some packets are lost while others continue to arrive. This is different from the connection going completely quiet, and different again from an encoder deliberately sending fewer bits. Check which direction lost packets before asking the participant to change anything.

#### Transport loss detector

Client Monitor's [`TransportLossDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/TransportLossDetector.ts) uses local reception statistics and the far end's [RTCP receiver reports](https://datatracker.ietf.org/doc/html/rfc3550#section-6.4.1) to assess inbound and outbound packet loss. It watches the worse available direction and raises **`transport-loss-sustained`** when material loss persists. This describes packet delivery, rather than how much damage the listener or viewer experienced after receiver processing.

{{< blog-figure src="/images/blog/webrtc-transport-quality-monitoring/loss.svg" alt="Loss above the raise threshold accumulates time until an issue is raised. Loss below the recovery threshold resets and resolves. The intermediate band and missing averages preserve state." >}}

*Figure 5. The middle band preserves accumulated loss time.*

Loss must fall below a separate recovery threshold to clear the issue. Intermediate readings preserve its state, so several bad intervals can contribute to one finding. Connection averages can hide a particularly affected stream, and complete silence may leave no usable inbound loss reading. Check the affected stream as well; missing measurements aren't zero loss.

### Case 2: the path stopped responding

The path worked, then stopped answering checks while the endpoint kept asking. This is stronger evidence than an old `connected` label, but weaker than knowing who dropped the packets. A firewall, expired mapping, vanished network, or unresponsive peer could all leave us investigating the same silence.

#### Blocked STUN requests detector

Client Monitor's [`BlockedStunRequestsDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/BlockedStunRequestsDetector.ts) watches each established ICE transport for STUN requests that stop receiving responses. It uses both connectivity-check and [consent-freshness](https://datatracker.ietf.org/doc/html/rfc7675) activity. If responses remain absent beyond the allowed wait while requests have been sent, it raises **`blocked-stun-requests`** and emits **`blocked-transport`**. A quiet interval with no requests isn't evidence of a blocked path.

{{< blog-figure src="/images/blog/webrtc-transport-quality-monitoring/stun.svg" alt="A succeeded pair with unanswered requests raises after a response timeout. A response, loss of the succeeded pair, or missing required counters clears the window and any issue." >}}

*Figure 6. A response timeout requires evidence that STUN requests were sent.*

A new response clears the issue. It also clears when the selected pair no longer qualifies or the required counters become unavailable, because the original condition can no longer be assessed. The finding identifies unanswered STUN traffic, not whether a firewall, expired mapping, network failure, or remote endpoint caused it.

## Reading a call together

Consider this **hypothetical** call using an SFU. The browser reports bandwidth limitation, its outgoing bitrate estimate falls, and local packet-send delay rises. Client Monitor raises uplink congestion. Packet loss remains low and RTT hasn't increased much: the browser can be reducing its sending rate before sustained loss or high RTT develops.

{{< blog-figure src="/images/blog/webrtc-transport-quality-monitoring/worked.svg" alt="A hypothetical outgoing RTP bitrate estimate falls and local packet-send delay rises. The application reduces video demand, then checks transport readings and far-end playback separately." >}}

*Figure 7. Change one demand, then check delivery and playback.*

I would first check whether our application just changed the sending layers or bitrate constraints, then consider reducing video demand while preserving audio. The detector doesn't call `setParameters()` or choose an SFU layer for us. Keep the application action on the same timeline as the findings so we can see what followed it.

Suppose mean packet-send delay returns to its baseline after reducing the video bitrate. If `qualityLimitationReason` remains `bandwidth`, the uplink issue stays open even as severity falls. If that verdict changes, it resolves. Neither outcome tells us that the other participant's video is now rendering smoothly; inspect that receiver's delivery and playback evidence. Successful playback after backing off supports keeping that setting for this call, but doesn't identify which network hop or competing transfer reduced the available bandwidth.

If RTT instead stayed high with no congestion finding, compare routing and relay placement before repeatedly lowering video bitrate. If loss persisted, inspect the affected direction and stream intervals, including repair traffic and receiver consequences. [BlogGeek.me's packet-loss guide](https://bloggeek.me/webrtcglossary/packet-loss/) describes retransmission and redundancy as possible responses; they have bandwidth and deadline costs, so “add more repair” isn't a universal answer either.

For an integration, start with the [Client Monitor guide](/docs/client-monitor-js/integrations/) and [events and issues source reference](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/docs/EVENTS_AND_ISSUES.md). Omitted detector config uses defaults; `null` omits that detector. Keep the issue lifecycle alongside the useful live measurements, application intent, and `inputsUnavailable`. A live event marks an observation; the issue registry tells you whether its finding remains open. All five detectors described here raise issues; route-change telemetry emits events without that issue lifecycle. Read resolution comments as well as timestamps: several stand-down paths clear a claim because it no longer applies or cannot be measured.

## What's next?

Once packets arrive, the job still isn't finished. Next we'll follow the media pipeline: whether capture supplies frames, encoding makes progress, and received media reaches decoding and playback.

<!-- Editorial baseline: source reviewed 2026-10-25 at ecbb77277306c35b32ad0d275e193a9687bf764e, package.json 4.11.0. Tracked source clean; untracked Claude outputs/ excluded. Not an npm-latest or release claim. Research and verification notes: docs/transport-quality-blog-source-notes.md. -->
