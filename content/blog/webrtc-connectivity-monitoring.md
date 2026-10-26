---
title: "WebRTC Monitoring: Are We Connected?"
slug: "webrtc-connectivity-monitoring"
date: 2026-10-26
draft: false
description: "Troubleshoot WebRTC connectivity step by step: signaling, ICE candidates, STUN and TURN, DTLS, path changes, and recovery with ObserveRTC detectors."
summary: ""
tags: ["WebRTC", "Monitoring", "Connectivity", "ICE", "TURN"]
contributors: []
---

In [The Bigger Picture](/blog/holistic-webrtc-monitoring/), we separated connectivity from transport quality and the media pipeline. This time, let's work through connectivity: what to check on the client, what each observation means, and how ObserveRTC's detectors help us keep track of it. The [five connectivity layers](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/docs/CONNECTIVITY_DETECTORS.md) are reachability, discovery and traversal, path establishment, secure transport, and path continuity.

A participant clicks Join. Their camera preview works, the room opens, and the application says “Connecting…”

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/connection-boundaries.svg" alt="Application signaling above five connectivity layers: reachability, discovery and traversal, path establishment, secure transport, and path continuity. Signaling requires application logs." >}}

*Figure 1. Follow the connection from signaling through ICE and DTLS, then watch whether the established path stays connected.*

For a failed join, I would start with the last thing we can show actually happened. Did the offer and answer reach both endpoints? Did they exchange ICE candidates? Were connectivity checks getting responses? Was a candidate pair selected, or did a working path disappear later?

## Signaling: an offer you can’t refuse

WebRTC uses an offer and answer to negotiate the session, but your application delivers them. With trickle ICE, it also delivers newly gathered candidates. So the first question we need to ask before investigating the network path: was the offer received and applied, was an answer sent back, and did the candidates reach the right peer connection?

An open WebSocket doesn’t prove SDP offers are accepted and answered. We need to record failures from `setLocalDescription()`, `setRemoteDescription()`, and `addIceCandidate()`.

ObserveRTC doesn't detect signaling delivery failures. Its native binding reads descriptions for media context, but your application logs have to tell us whether the offer, answer, and candidates arrived and were applied. Keep those records alongside the monitor's timeline.

## Reachability: is there anybody out there?

ICE gathering finds the local possibilities. The [ICE specification, RFC 8445](https://datatracker.ietf.org/doc/html/rfc8445), distinguishes host addresses, server-reflexive addresses discovered using STUN, relayed addresses allocated through TURN, and peer-reflexive addresses learned during checks.

In the statistics, those candidate types appear as `host`, `srflx`, `relay`, and `prflx`. A host candidate comes from a local interface. STUN helps discover the address mapped by a NAT, while TURN provides a relay address for forwarding traffic when a direct path won't work.

Let's start with what gathering produced. While it's still running, an empty candidate list may simply mean we need to wait. But if gathering is finished and the list is still empty, there are no local candidates to try.

### Case 1: we are alone

The participant is ready to join, but their browser hasn't found a local address it can use for the connection. There may be someone waiting at the other end; we haven't reached the point where we can try a path to them. An unavailable network interface or a restrictive candidate policy could leave us here. If the application allows only relay candidates, a problem obtaining a TURN allocation could do the same—even while ordinary websites still load.

#### Ice Reachability Detector

Client Monitor's [`IceReachabilityDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/IceReachabilityDetector.ts) starts in **Watching**. It raises **`no-available-ice-candidate`** only when gathering is complete, no local candidates exist, and the connection has never been observed connected. It normally waits **6,000 ms**, configured through `iceReachabilityDetector.thresholdInMs`. A disconnected or failed connection bypasses that wait, but still needs completed gathering and an empty candidate list. Missing gathering state or ongoing gathering leaves it watching.

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/reachability-detector.svg" alt="Reachability detector states: Watching, Raised, and Done. Finding a candidate resolves the issue and returns to Watching; connected or closed ends the checks." >}}

*Figure 2. Reachability detection, from watching to a raised issue or completed checks.*

The wait includes stats time before gathering finishes, so an attempt that ends empty can raise immediately at completion. A candidate appearing resets the wait and resolves an open issue; monitoring continues because the connection hasn't necessarily succeeded. Connected or closed ends the checks and resolves any open issue. To investigate the empty inventory, check the application's candidate policy, ICE-server configuration and gathering errors—the finding doesn't identify a faulty server.

## Discovery: which way do we go?

### Case 1: taking the long way

The participant joins successfully, but their traffic goes through a relay. That's a usable route, not a failed call. [TURN](https://datatracker.ietf.org/doc/html/rfc8656) provides an allocated address and forwards traffic when the direct alternatives don't work. The route can also change during the call: Wi-Fi drops, a VPN comes up, or another candidate pair takes over. Before calling that a problem, we need to know what changed and whether the participant noticed an interruption.

#### Ice Traversal Detector

Client Monitor's [`IceTraversalDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/IceTraversalDetector.ts) compares the set of selected network tuples: local address and port, remote address and port, and protocol. If that set changes after a nonempty set was observed, it emits **`ice-tuple-changed`**. It raises no issue and has no timeout or recovery threshold: this is **Telemetry**, recording a change rather than declaring a fault. Enable it with `iceTraversalDetector: {}` or omit it with `null`.

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/traversal-detector.svg" alt="ICE traversal detector compares selected tuples and emits an event when a previously nonempty set changes. It then continues comparing on the next collection." >}}

*Figure 3. Selected-path changes produce telemetry, not a raised issue.*

Growth from an empty set is skipped; losing every selected tuple counts as a change. The related [`SelectedIcePath`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/monitors/SelectedIcePath.ts) model supplies **`ice-path-changed`** events for initial selection, direct-to-relay, relay-to-direct, changes of TURN server or relay protocol, and other path changes. The traversal detector only reports that the tuple set changed.

Path kinds are `direct`, `turn-udp`, `turn-tcp`, `turn-tls`, and `turn-unknown`, classified from the local candidate. Local `direct` doesn't rule out relay use at the remote endpoint. For a relay, `relayProtocol` describes the client-to-TURN leg; candidate `protocol` can still be UDP when that leg uses TCP or TLS. Candidate type takes precedence over a `turn:` URL, and missing candidate details limit the classification.

## Establishment: are we there yet?

Once local and remote candidates are available, ICE sends connectivity checks. A candidate pair's `succeeded` state records a successful check; nomination and selection identify which usable path is chosen. Don't count every successful pair as a separate active route. Follow the transport's selected pair and its candidate references in the [WebRTC statistics](https://www.w3.org/TR/webrtc-stats/#dom-rtctransportstats-selectedcandidatepairid).

The practical approach in [rtcStats' guide to diagnosing ICE failures](https://rtcstats.com/kb/troubleshooting/webrtc-ice-failed) is helpful here: inspect the candidate pairs and check responses alongside the state. The label `failed` gets you to the right part of the timeline; the attempted paths help you investigate it.

### Case 1: still connecting

The participant hasn't joined yet, but the browser is still trying. A slow attempt deserves attention before we call it a failure. The useful next step is to locate the delay: gathering candidates, checking paths, or finishing the secure transport.

#### Ice Path Establishment Detector

Client Monitor's [`IcePathEstablishmentDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/IcePathEstablishmentDetector.ts) times each stretch of peer connection `connecting` and emits **`ice-path-establishment-slow`** once it reaches **5,000 ms** by default. Set `icePathEstablishmentDetector.thresholdInMs` to change that wait. It raises no issue: the event says setup is slow, not that it has failed. Any exit from `connecting` resets the clock and re-arms it, so later attempts are measured separately.

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/slow-establishment.svg" alt="Timing to Notified on Connecting + timeout. Transition conditions are explained in the text." >}}

*Figure 4. A slow-establishment event fires once per connecting attempt; any exit re-arms it.*

The event's `stalledStage` points to the next check: `ice-gathering` when no transport exists and gathering is running; `ice-checking` when a transport reports ICE new/checking; `dtls` when ICE is connected/completed, or a selected pair succeeded where ICE state is absent. Otherwise it's `unknown`. An ICE new/checking transport takes precedence when several transports exist. The event includes `sustainedForInMs`; `createEvent: true` also buffers `LONG_PC_CONNECTION_ESTABLISHMENT` into samples, while false leaves only the live event.

### Case 2: still no winner

The browser has addresses to try, but none of its observed checks has produced a usable winner. The participant stays outside the call. We need to separate this from an empty candidate list—and from a path ICE already established while something later in setup is waiting.

#### Ice Establishment Failed Detector

Client Monitor's [`IceEstablishmentFailedDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/IceEstablishmentFailedDetector.ts) raises **`ice-establishment-failed`** after **15,000 ms** with local candidates but no observed connection success or pair nomination/success. Configure `iceEstablishmentFailedDetector.thresholdInMs`, preferably above the slow-event threshold. It does not require terminal browser `failed`, or even `connecting`. Observing **either** a nominated pair or a succeeded pair latches establishment success for this detector's lifetime; observing connection `connected` does too.

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/establishment-failed.svg" alt="Watching to Raised on Candidates + timeout. Transition conditions are explained in the text." >}}

*Figure 5. Candidates exist, but no establishment success has been observed within the configured wait.*

**Success** resolves an open issue and ends first-establishment checks; closing the peer connection resolves it too. Zero candidates resets accumulation before a finding, but doesn't close an issue already raised. Pair resets and ICE restarts don't erase the success latches: this detector watches first establishment, not each generation.

The payload captures current candidate counts by type, pair states, pair count and accumulated time. Host-only candidates suggest checking whether STUN/TURN were configured and attempted; server-reflexive candidates without relay suggest checking expected TURN allocation. Relay candidates without a winner suggest checking remote candidate delivery and responses. These are investigation leads, not proof of a server outage.

## Transport: do you understand me?

Once ICE finds a working pair, [DTLS-SRTP](https://datatracker.ietf.org/doc/html/rfc5764) uses a DTLS handshake to establish SRTP keying material. If ICE succeeds but setup still doesn't complete, check this handshake. The detectors below distinguish an explicit DTLS failure from a handshake that keeps waiting.

### Case 1: we’re not on speaking terms

The endpoints can reach each other, but they're not on speaking terms yet. The secure hello has ended with a failed DTLS handshake. This is where we look at certificate fingerprints, DTLS roles and endpoint logs to understand why the secure connection couldn't be established.

#### DTLS Handshake Failed Detector

Client Monitor's [`DtlsHandshakeFailedDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/DtlsHandshakeFailedDetector.ts) raises **`dtls-handshake-failed`** and emits the matching event immediately on `dtlsState: 'failed'`. It doesn't require healthy ICE. Configure `dtlsHandshakeFailedDetector` with `{}` to enable it or `null` to omit it.

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/dtls-failed.svg" alt="Watching to Raised on DTLS failed. Transition conditions are explained in the text." >}}

*Figure 6. A reported DTLS failure raises immediately; retrying alone does not resolve it.*

DTLS connected or transport removal resolves the issue; new/connecting doesn't. An ICE restart alone doesn't guarantee a new handshake or repair its configuration.

### Case 2: the silent treatment

The network path is ready, but the secure hello seems to have met with silence. The participant keeps watching the spinner while DTLS remains unfinished, without an explicit failure. Did the handshake packets reach the other endpoint, and did replies come back? We need evidence from both sides before deciding who gave whom the silent treatment.

#### DTLS Handshake Stalled Detector

Client Monitor's [`DtlsHandshakeStalledDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/DtlsHandshakeStalledDetector.ts) raises **`dtls-handshake-stalled`** after **6,000 ms** of DTLS new/connecting over ICE connected/completed. A succeeded selected pair substitutes only when ICE state is absent. It skips the first transport tick; tune the wait through `dtlsHandshakeStalledDetector.stalledThresholdInMs`.

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/dtls-stalled.svg" alt="Watching to Raised on ICE ready + DTLS timeout. Transition conditions are explained in the text." >}}

*Figure 7. Healthy ICE plus a sustained unfinished DTLS handshake raises a stall finding.*

DTLS connected/failed or transport removal resolves the stall. Missing ICE proof, missing/closed DTLS state, or an observed restart resets timing without closing an open finding.

## Continuity: stay with me

Now the participant joined and the call worked. Then the audio cuts out while they walk away from Wi-Fi.

This time, retain the history. Which transport had worked? Did its selected pair change? Did ICE report a loss of connectivity, or do the state fields still look fine?

Established ICE paths also use periodic STUN exchanges for [consent freshness](https://datatracker.ietf.org/doc/html/rfc7675): permission to keep sending. That is separate from proving that useful media reaches playback.

The [WebRTC ICE transport states](https://www.w3.org/TR/webrtc/#rtcicetransportstate) distinguish `disconnected`, a potentially transient loss, from `failed`. ObserveRTC gives them separate findings, with separate recovery behavior.

### Case 1: don’t leave me hanging

The conversation was flowing, then the other person disappeared mid-sentence. Perhaps their Wi-Fi is handing over and they'll be back in a moment. ICE reports disconnected, but hasn't given up. We give the interruption a little time before treating it as a sustained outage.

#### Ice Disconnected Detector

Client Monitor's [`IceDisconnectedDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/IceDisconnectedDetector.ts) raises **`ice-disconnected`** after transport ICE stays `disconnected` for **5,000 ms**, configured through `iceDisconnectedDetector.disconnectedThresholdInMs`. The clock uses transport stats intervals; any exit resets the accumulation. It raises once per open episode, recording transport and pair IDs, DTLS state, disconnected time and the observed ICE generation.

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/ice-disconnected.svg" alt="Watching to Raised on Disconnected + timeout. Transition conditions are explained in the text." >}}

*Figure 8. A sustained disconnection raises once; failure does not count as recovery.*

ICE connected/completed resolves the issue. A changed local username fragment—falling back to the selected local candidate's fragment—resolves it and restarts timing for the new generation. Transport removal resolves it too. Falling to failed resets the timer but leaves the issue open. Tune the threshold against your application's reconnecting experience: a five-second outage can still recover without a restart.

### Case 2: I think we lost them

This time, ICE has given up on the current generation: the transport reports failed. Did we lose someone who was already in the conversation, or did they never make it in? Both can end with the same state, so we need the connection's history before deciding what to investigate.

#### Ice Connection Failed Detector

Client Monitor's [`IceConnectionFailedDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/IceConnectionFailedDetector.ts) raises **`ice-connection-failed`** on the first observation of transport ICE `failed`, without a time threshold. Enable `iceConnectionFailedDetector` with `{}` or omit it with `null`. The payload's `everConnected` distinguishes a transport observed `connected`/`completed` earlier from one that never reached those states under monitoring. Attach early: the monitor cannot reconstruct missing history.

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/ice-failed.svg" alt="Watching to Raised on ICE failed. Transition conditions are explained in the text." >}}

*Figure 9. An ICE failed state raises immediately, with history showing whether the transport worked earlier.*

ICE connected/completed, an observed fragment change, or transport removal resolves the issue. A new generation can fail and raise again. This finding can overlap `ice-establishment-failed` during setup or an earlier `ice-disconnected`; correlate their transport IDs and intervals rather than counting each as a separate outage.

### Case 3: am I talking to myself?

We're still sending, but nothing is coming back. ICE insists we're connected, yet a path that was receiving traffic has gone quiet. Before asking whether we're talking to ourselves, check that the application still expects incoming media—a deliberately paused subscription doesn't owe us a reply.

#### Ice Transport Stalled Detector

Client Monitor's [`IceTransportStalledDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/IceTransportStalledDetector.ts) raises **`ice-transport-stalled`** after **5,000 ms** of guarded receiving-side silence, controlled by `iceTransportStalledDetector.transportStallThresholdInMs`. ICE must be connected/completed, its selected pair succeeded, both byte deltas available, and outgoing bytes positive while incoming bytes make no progress. Earlier inbound traffic must have been observed on the transport, and an inbound RTP report must still be attributed to it. Those guards exclude an entirely idle path, an initially silent path and a send-only SFU uplink.

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/ice-stalled.svg" alt="Watching to Raised on Guarded silence + timeout. Transition conditions are explained in the text." >}}

*Figure 10. Only a previously receiving, still-sending transport with inbound RTP can meet the stall condition.*

Incoming bytes, losing the connected-path condition, a detected restart, or transport removal resolves the issue. Restart also clears the prior-inbound latch. Missing byte deltas pause judgement; sending stopping or inbound RTP reports disappearing resets accumulation without closing an existing issue. The payload carries deltas, stall time, generation, pair ID and available RTT/last-packet time.

Candidate-pair bytes exclude ICE connectivity checks, so this isn't a count of unanswered consent requests. An inbound RTP report also doesn't prove the subscription is still wanted. The taxonomy keeps this asymmetric finding in Connectivity; `BlockedStunRequestsDetector`, `BlockedOutboundMediaDetector` and `BlockedInboundMediaDetector` belong to Transport Quality's delivery-reliability group.

### Case 4: make up your mind

ICE picks a path, then another, then changes its mind again. One switch may keep the conversation going during a network change. Repeated switches deserve a closer look, especially if they line up with interruptions. Is the path causing trouble, or is the browser moving because another path already did?

#### Unstable Ice Path Detector

Client Monitor's [`UnstableIcePathDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/UnstableIcePathDetector.ts) raises **`unstable-ice-path`** at **three selected-pair switches within a 30,000 ms window** by default. Configure `unstableIcePathDetector.pathSwitchThreshold` and `pathSwitchWindowInMs`. Each interval counts the larger of a changed `selectedCandidatePairId` and the native pair-change counter delta, where reported. Taking the larger avoids double-counting; the native counter can catch a path leaving and returning between collections. Losing a previously selected ID can count too.

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/unstable-path.svg" alt="Watching to Raised on Switch threshold. Transition conditions are explained in the text." >}}

*Figure 11. Count switches within each tumbling window; a quieter complete window resolves the finding.*

The stats-time window tumbles rather than slides: reaching the threshold raises, and a closing window below it resolves. Switches split across a boundary may not raise; transport removal resolves, while an ICE restart has no special reset. Without the native counter, between-collection flaps can be missed. Compare the recorded switch count, path identity and path-change events with media progress—the browser may be switching to escape another problem.

## Recovery: let's try that again

**Hypothetical example.** A participant is in a two-way call when their network changes. Video stops and the application still expects the subscription to play. The selected pair keeps sending bytes, but incoming bytes stop. ICE continues to report connected. At five seconds of observed asymmetry, the transport-stalled issue opens. At ten seconds, Client Monitor recommends a restart.

Two detectors help us follow what happens next. [`IceRestartRecommendationDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/IceRestartRecommendationDetector.ts) says when another attempt may be useful. [`IceRestartDetector`](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/IceRestartDetector.ts) records evidence that it began and how ICE responded. Both are **Telemetry**: neither raises an issue or performs recovery.

{{< blog-figure src="/images/blog/webrtc-connectivity-monitoring/recovery-evidence.svg" alt="Hypothetical recovery timeline: incoming traffic stops, the stall issue opens, a restart is recommended and observed, ICE recovers, then media resumes." >}}

*Figure 12. A recommendation, an observed restart, and returning media are separate events. Times illustrate the default thresholds; collection cadence affects when they appear.*

### The application makes the call

The `ice-restart-recommended` event arrives with reason `transport-stalled`, the condition duration, transport identity, observed generation and recommendation count. Before acting, the application checks that the subscription hasn't been paused, signaling is available, and another negotiation isn't running. An [ICE restart](https://datatracker.ietf.org/doc/html/rfc8445#section-9) starts a new ICE generation with new credentials; the application still has to exchange them through its signaling flow.

For this example, suppose `monitor` watches one native `pc`, `signaling` is the application's existing WebSocket, and the normal negotiation handler already creates and exchanges offers and answers. This listener requests at most one restart for the stalled path:

```typescript
let restartRequested = false;

monitor.on('ice-restart-recommended', ({ reason }) => {
  if (reason !== 'transport-stalled' || restartRequested) return;
  if (signaling.readyState !== WebSocket.OPEN) return;
  if (pc.signalingState !== 'stable') return;

  restartRequested = true;
  pc.restartIce(); // The normal negotiation handler exchanges the new offer.
});

monitor.on('ice-restart', ({ iceGeneration, outcome }) => {
  console.log('ICE restart', iceGeneration, outcome);
});
```

This is one bounded recovery attempt, not a complete retry controller. An SFU SDK may own negotiation and expose its own restart API. In either integration, requesting a restart isn't evidence that the new credentials reached the remote endpoint.

### Did it actually restart?

On a later collection, the local ICE username fragment changes. `IceRestartDetector` emits `ice-restart` with `outcome: 'detected'` and an incremented observed generation. It reads the transport's local fragment, falling back to the selected local candidate's fragment. The first observation only establishes a baseline; entering checking alone isn't a restart, and missing fragments leave the detector silent.

Suppose the new generation later reaches ICE connected. The detector emits `recovered`; had it reached failed, the outcome would be `failed`. While it remains checking, no outcome is invented. Pending outcomes are settled before a changed fragment starts another generation, so the state in that first changed-fragment collection doesn't immediately settle the new attempt. Tracking is per transport and is discarded when that transport disappears.

In our example, incoming bytes return, but video takes another two seconds to resume decoding. Record that separately. ICE recovered before media did. If a restart fails, keep its generation and outcome and let the application's retry policy decide what follows. A working retry helps the participant; it doesn't explain why the old path stopped receiving.

### When to recommend another attempt

The recommendation detector also handles three other situations. Transport ICE `failed` recommends immediately with `ice-failed`. Sustained disconnection recommends `ice-disconnected`; it shares the **10,000 ms** default wait with the guarded transport-stall condition. A separate peer-connection branch recommends `never-established` after 10,000 ms in connecting, yielding to transports already failed/disconnected. This includes attempts delayed at DTLS and doesn't use the establishment-failure detector's lifetime-success latch. Each reason is derived from raw evidence, independently of the other detectors' findings.

In `iceRestartRecommendationDetector`, `iceRestartRecommendationThresholdInMs` controls the transport wait and `restartRecommendationThresholdInMs` the connecting wait. Their respective cooldowns, `iceRestartRecommendationCooldownInMs` and `restartRecommendationCooldownInMs`, default to **15,000 ms**. Conditions use stats time; cooldowns use wall time. Transport reasons share per-transport rate limiting; the connecting branch has its own. Recovery clears the incident's cooldown. A fragment change suppresses transport recommendations while the new generation is pending, until connected/completed or failed; missing fragments limit this suppression, and the separate connecting branch remains eligible.

Repeated recommendations don't count actual restarts—the application may not have acted. With `createEvent: true`, the recommendation block also buffers `ICE_RESTART_RECOMMENDED`; `iceRestartDetector.createEvent` similarly buffers `ICE_RESTART`. Both flags are true in their default blocks. Keep the recommendation, observed attempt, ICE outcome and media-return times together so the recovery history doesn't collapse into a single “reconnected” label.

## Put it in the application

The current public API starts with `ClientMonitor` and `addSource()`. Attach it before setup if you want the setup history. The older `createClientMonitor()` examples in [Power-up getStats for Client Monitoring](https://webrtchacks.com/power-up-getstats-for-client-monitoring/) explain the monitoring approach, but aren't the API used by this source baseline.

```typescript
import { ClientMonitor } from '@observertc/client-monitor-js';

const monitor = new ClientMonitor({
  collectingPeriodInMs: 1000,
  samplingPeriodInMs: 5000,
  icePathEstablishmentDetector: { thresholdInMs: 5000, createEvent: true },
  iceEstablishmentFailedDetector: { thresholdInMs: 15000 },
  iceDisconnectedDetector: { disconnectedThresholdInMs: 5000 },
});

// Use the connection your application will negotiate.
const pc = new RTCPeerConnection();

monitor.on('issue', (issue) => {
  console.log('Finding opened', issue.type, issue.payload);
});
monitor.on('issue-resolved', (issue) => {
  console.log('Finding closed', issue.type, issue.payload);
});
monitor.on('ice-path-establishment-slow', (event) => {
  console.log('Setup is slow', event.stalledStage, event.sustainedForInMs);
});
monitor.on('ice-restart-recommended', (event) => {
  // Pass this to your application's recovery controller.
  // It owns signaling, negotiation serialization, and retry limits.
  console.log('Consider recovery', event.reason, event.peerConnectionId);
});
monitor.on('ice-restart', (event) => {
  console.log('Observed restart', event.iceGeneration, event.outcome);
});

monitor.addSource(pc);
// Continue with your normal track setup and offer/answer exchange.
// Call monitor.close() when monitoring the session ends.
```

The empty `RTCPeerConnection` configuration keeps this example focused on monitoring; use your application's real ICE servers and credentials. Monitoring doesn't provide a TURN server or negotiate the connection for you.

A supplied detector block replaces that block's defaults; include every required threshold and any optional flag you want enabled. In particular, omitting `createEvent` from a supplied block stops its buffered client event, while its live monitor event still fires. These twelve connectivity-related classes are enabled by default at this source revision. To omit one, pass `null` for its own config key, for example `unstableIcePathDetector: null`. There is no current `iceConnectivityDetector` group key. Old names don't silently select the replacement classes.

For recovery itself, the browser's [`pc.restartIce()` method](https://www.w3.org/TR/webrtc/#dom-peerconnection-restartice) requests an ICE restart and triggers negotiation as needed. Your application still has to create and exchange the offer/answer through its normal negotiation handling. Don't put an unconditional restart in every issue listener: one outage can produce several findings, and your signaling stack or SFU SDK may own the appropriate restart API.

### Give the clock some respect

These detectors run on collections, not on a timer which fires at exactly five seconds. With a one-second collection period, a five-second condition is reported at a collection that has accumulated enough valid stats time. A five-second collection period is much coarser. Short state changes between observations may be missed.

Most sustain clocks here sum the monitor's `deltaTime`. That avoids treating wall-clock advance alone as evidence, but it doesn't eliminate gaps: a later valid stats timestamp can span a long collection delay. The detector can't reconstruct every transition inside that interval. Keep `stats-collection-gap` telemetry, timestamps, and collection cadence alongside findings. Don't assume all these clocks reset after a gap.

Many resolved payloads add `durationInMs` using wall time since the finding was raised. That isn't necessarily the full outage duration, and it isn't the same quantity as the stats-time sustain included when it opened. Preserve both, and avoid summing overlapping issue durations into participant downtime.

### Keep silence readable

No issue can mean healthy, too brief to trigger, disabled, or unobservable. The implementation doesn't expose a uniform missing-input signal across all these detectors. Missing `iceState` blocks several continuity checks; the DTLS stall detector has a selected-pair fallback, but that doesn't make every detector equally portable. Missing username fragments hide restart detection. Missing candidate fields limit path classification.

Keep raw evidence with its availability. An absent value shouldn't become a zero, and removal of a monitored transport shouldn't become a successful recovery in your dashboard. At session shutdown, retain the terminal application event as well: several transport detectors return early on a closed peer connection, so closing the monitor isn't evidence of protocol recovery.

For each report, the useful record is the peer connection and transport identity, selected pair and candidate details, browser/source coverage, configuration, application intent, and surrounding state changes. An issue gives that investigation a starting point. It doesn't replace it.

## What's next?

Once a path is established, we can ask how well it carries traffic: capacity, delay, loss, and delivery failures. That's transport quality, and it's the next stop in this series.
