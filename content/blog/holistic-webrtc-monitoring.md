---
title: "WebRTC Monitoring: The Bigger Picture"
slug: "holistic-webrtc-monitoring"
date: 2026-10-16
draft: false
description: "A model for WebRTC monitoring that connects connectivity, transport quality, media pipeline disruption, and perceived quality with session context."
summary: "How can we detect quality issues in WebRTC calls—and understand where they come from?"
tags: ["WebRTC", "Monitoring", "Observability"]
contributors: []
---

Monitoring helps us spot problems and track how calls behave. Observability helps us investigate why, using the measurements and context we have collected—a distinction Tsahi Levent-Levi very nicely pointed out in [What WebRTC observability actually requires](https://rtcstats.com/blog/what-webrtc-observability-requires). The goal is an explanation we can support with evidence.

Why was my video frozen? Why couldn’t I hear the other participant? Why did the picture suddenly become blurry? **Simple questions, non-trivial answers.**

Customers do not care about WebRTC statistics. They have a specific problem and want an answer they can understand. Was it the network? Their device? Something in our application? And what can they do about it?

{{< blog-figure src="/images/blog/webrtc-holistic-monitoring/same-symptom.svg" alt="Several interruption points can produce frozen video" height="445" >}}

*Figure 1. One visible symptom can lead to several different investigations.*

Suppose a customer tells us their video froze. We check the statistics ([WebRTC Statistics specification](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-freezecount)) for that video stream around the time of the complaint and find an increase in `freezeCount`. So the browser recorded a freeze too. Great! But that is probably not the answer the customer is looking for. They want to know why.

To investigate, we can work backward from the receiver. Was it rendering fresh decoded frames? Was the decoder getting complete frames and processing them in time? Were the necessary RTP packets arriving? Were those packets forwarded and delivered through the network and any SFU? Was the sender transmitting successfully? Was the encoder producing output, and was the camera or source supplying fresh frames?

We do not need to follow this as a fixed checklist. The point is to look beyond the place where we noticed the problem. As we go, we need to check the same stream over the same period and ask what the application was supposed to be doing. If it deliberately paused the video, missing frames may be expected.

To explain the call, we need to put those pieces together. Let’s start with four questions that connect the sender, the network, and the receiver.

## Slice and dice

{{< blog-figure src="/images/blog/webrtc-holistic-monitoring/call-overview.svg" alt="Sender, network, and receiver with measurements and context" height="300" >}}

*Follow the media from the sender, through the network, to the receiver.*

We can look at the call from two perspectives. The first follows the media flow: sender, network, receiver. This feels like a horizontal slice, and it is a natural place to start when investigating quality degradation. Congestion may lead to packet loss and incomplete frames. An overloaded receiver may struggle to decode video in time. We can compare what happens along the path with what the participant hears and sees.

These are the problems I enjoy investigating: finding what hurts quality, measuring the effect, and looking for ways to improve it. But much of the actual debugging is about getting media to work at all. Something stalled somewhere. The connection never became ready, a sender stopped producing packets, or video stopped updating. This leads us to the second perspective we need to consider.

First, the client needs to establish and maintain a connection. Once connected, we can check how well the transport carries the traffic. Then we follow the processing on both sides: from camera frames to outgoing packets, and from incoming packets to the display. We check where media stopped or slowed down. If it keeps flowing, we look at the quality of the audio and video the participant received.

Following the media tells us where to look; checking these layers helps us decide what to ask there. ObserveRTC's [detector categories](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/docs/DETECTOR_TAXONOMY.md) organize those questions, with context alongside them: a path change, a codec switch, or an intentional pause can change how we read the measurements. These layers guide the investigation, but they do not prove what caused what. A decoder can stop on a healthy network, and several problems can happen at once.

{{< blog-figure src="/images/blog/webrtc-holistic-monitoring/diagnostic-model.svg" alt="Four diagnostic questions with context alongside each" height="490" >}}

*Figure 2. Look through the layers to ask what worked, what stopped, and what changed around it.*

### Connectivity: are we connected?

Before worrying about picture quality, let’s check whether a connection was possible at all. Could we reach the required infrastructure? Did we gather usable candidates? Did ICE find a working pair, and did secure transport complete? These are the steps separated by the [connectivity model](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/docs/CONNECTIVITY_DETECTORS.md). The details of ICE are in [RFC 8445](https://www.rfc-editor.org/rfc/rfc8445.html); continued consent to send traffic is covered separately in [RFC 7675](https://www.rfc-editor.org/rfc/rfc7675.html).

Your application might say someone has joined before they hear any audio or see a frame. It is worth recording both moments: when the connection was ready and when useful media started.

No usable candidate? That is one investigation. ICE succeeded but secure transport never completed? That is another. Both calls failed to start, but calling them both “connection failure” does not help us decide where to look. And once connected, we still need to watch for lost paths, changes, and recovery attempts.

### Transport quality: packets getting through?

We connected. Good! Now, are the packets actually getting through well enough? They may arrive late, go missing, or arrive in bursts while the connection still looks connected. It may also have too little capacity for the media we want to send. The [transport quality model](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/docs/TRANSPORT_QUALITY_DETECTORS.md) treats these as separate properties. A high delay does not, on its own, prove congestion. A loss counter tells us packets were missing, but not why.

The WebRTC Statistics specification distinguishes [candidate-pair statistics](https://www.w3.org/TR/webrtc-stats/#rtcicecandidatepairstats-dictionary) from [remote inbound RTP statistics](https://www.w3.org/TR/webrtc-stats/#dom-rtcremoteinboundrtpstreamstats). They measure round trips in different ways: STUN transactions on the candidate pair and RTCP feedback for an RTP stream. So before putting either value on a chart labeled “RTT,” it is worth asking: which round trip are we measuring?

Neither RTT tells us how long a frame took to travel from the camera to the screen. RTP interarrival jitter describes variation in transit timing ([RFC 3550](https://www.rfc-editor.org/rfc/rfc3550)), rather than audible interruptions. A buffer may smooth out those arrivals while making the audio or video later. We need to measure both the network timing and what happened during playout.

| What we see | What it tells us | What we still need to ask |
|---|---|---|
| Candidate-pair RTT rises | STUN round trips took longer. | Did queues build up? Did the route change? |
| RTP loss is reported | Packets were missing. | Did repair or concealment help? What reached the participant? |
| Sender reports bandwidth limitation | The encoder reports that bandwidth limited its output. | Did resolution or frame rate drop? How did the picture change? |
| Time in the jitter buffer rises | Samples or frames waited longer before playout. | Did playback get smoother? Did conversation get slower? |

These numbers start to help when we read them together. Take [`qualityLimitationReason`](https://www.w3.org/TR/webrtc-stats/#dom-rtcoutboundrtpstreamstats-qualitylimitationreason): it tells us what the encoder reports as limiting its output. Useful, but it cannot tell us exactly where the network bottleneck is.

### Pipeline disruption: where’s the holdup?

The [pipeline disruption model](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/docs/PIPELINE_DISRUPTION_DETECTORS.md) looks for places where media should be moving but is not. The sending and receiving sides do different work, so let’s look at them separately.

{{< blog-figure src="/images/blog/webrtc-holistic-monitoring/media-boundaries.svg" alt="Two media pipelines: sending moves from capture through encoding to RTP transmission; receiving moves from RTP reception through frame assembly and decoding to presentation. Network delivery connects the two." height="480" >}}

*Figure 3. Follow the media on each side of the network. Browsers let us measure some stages more directly than others.*

#### Sending: camera to packets

Start at the source. Is the camera still producing fresh frames? Is the encoder turning them into encoded frames? Are packets leaving the RTP sender? The network may be working perfectly while the camera or encoder has stopped producing anything.

If the source keeps producing frames but the encoder produces none, that gives us somewhere to look. If encoding continues but packets stop leaving, look further along the sending side. Neither comparison proves the cause yet. And before treating either as a fault, check whether the application paused the track or stopped an encoding on purpose.

#### Receiving: packets to playback

Now follow the other end. Are packets arriving? Do they form complete frames? Is the decoder producing anything new? Does that output make it to the screen? The [`packetsReceived`, `framesReceived`, and `framesDecoded` counters](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats) describe different stages. Packet arrival does not guarantee complete frames, and complete frames do not guarantee decoded output.

Packets are arriving, but decoding has stopped? Check whether complete frames are available before blaming the decoder. Decoding continues, but the picture does not change? Look at presentation and what the application is doing with playback. We cannot see every part of that last step through browser statistics.

On both sides, look at how the counters change for the same stream over time. Thousands of frames processed earlier do not tell us whether anything is moving now. If a stats object changes or a counter resets, start a new comparison.

### Perceived quality: all good?

Everything is moving. Does that mean the call is good? Not necessarily. Audio can cut out, video can stutter, and lips can move out of sync with speech. The [perceived quality model](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/docs/PERCEIVED_QUALITY_DETECTORS.md) looks at these kinds of problems and how long they last.

Take audio. The receiver can keep playing sound while filling in for missing samples. The statistics expose [`concealedSamples` and `silentConcealedSamples`](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-concealedsamples), with silent concealment included in the total. So audio can keep playing even when some original speech is missing. The concealment count still cannot tell us which words the listener understood.

#### Buffering: smooth, but late?

Buffering gives us another example. A jitter buffer can wait for unevenly arriving media and help keep playout steady. How much waiting did it add? Using the [jitter-buffer statistics](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay), divide the change in `jitterBufferDelay` by the change in `jitterBufferEmittedCount`. That gives us the average time emitted samples or frames spent in the buffer during that interval. Only calculate it when the emitted count increased and both counters are available and comparable. It describes time in this buffer, not the full delay from sender to receiver.

Let’s put some numbers to that. Suppose the counters in the same audio report changed by these amounts:

```text
change in jitterBufferDelay        = 480 seconds
change in jitterBufferEmittedCount = 480,000 samples

mean buffer residence time = 480 / 480,000
                           = 0.001 seconds
                           = 1 millisecond
```

480 seconds might look odd at first. The counter adds up the waiting time of every emitted sample; it is not a stopwatch for the call. Dividing by the sample count gives us the average. The numbers here only illustrate the calculation—one millisecond is not a proposed threshold for a good call.

More buffering may stop the audio cutting out, but make people wait longer for each other. Smooth sound, awkward conversation. Another application might prefer that tradeoff. Before calling the audio “healthy,” we need to decide which parts of the experience matter.

## Context matters

The resolution dropped. Is that bad? Perhaps the browser kept the video moving on a struggling uplink. Perhaps the shared text became unreadable. We need to know what changed and what happened afterward. The same goes for a path switch or a pause: the event alone does not tell us whether something went wrong. Interactive media involves tradeoffs between useful throughput and timely delivery ([RFC 8836](https://www.rfc-editor.org/rfc/rfc8836)).

This is why ObserveRTC keeps a [telemetry category](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/docs/TELEMETRY_DETECTORS.md) alongside the four diagnostic categories. It records changes we need to know about without calling each one a problem. Using a relay, switching codecs, or changing resolution can all be normal parts of a call.

Some answers have to come from your application: was the participant publishing, was the subscription active, had playback been paused? A static slide may need much less bitrate than a moving camera. A drop in bitrate alone does not tell us something went wrong.

### Missing measurements

We have no samples for a few seconds. Did media stop? We do not know yet—we stopped seeing it. If collection resumes after both a path change and a bitrate drop, the next sample may show both without telling us which came first. Keep the collection times and intervals. A record reaching your server now does not mean the event happened now.

### No news is good news?

No issues reported. Great—or did the detector have nothing to work with? Maybe the condition never happened. Maybe it did not last long enough to trigger a finding. The detector might also have been disabled or missing an input. The dashboard can look the same in all four cases.

Before trusting a quiet dashboard, I would check which detectors were running and whether they had the inputs they needed. A missing browser statistic needs to remain missing. If we replace it with zero, we may accidentally turn “we could not measure this” into “everything was fine.”

This matters when comparing browsers too. If one reports a signal and another does not, fewer issues on the second browser may simply mean we can see less. Check what was measured before concluding that its calls were better.

## A practical example: Frozen video

Let’s return to that frozen video. Suppose we follow the same incoming video stream over the reported period. The connection stays established and its RTP packet counter keeps increasing, but `framesDecoded` stops. The application still expects video to play; neither participant intentionally paused it.

We have narrowed the investigation, but we have not found the cause. Those packets might include retransmissions, and arriving packets do not necessarily add up to complete, usable frames. I would check the next boundary: is `framesReceived`, which counts complete frames, still increasing?

{{< blog-figure src="/images/blog/webrtc-holistic-monitoring/frozen-video-investigation.svg" alt="Illustrative receiving stream: packets and complete frames keep arriving, but decoded and rendered frames stop. Investigate usable decoder input and decoding without assuming a decoder fault." height="350" >}}

*Figure 4. An illustrative case: complete frames keep arriving, but decoding stops. This narrows where to investigate; it does not tell us why.*

If packets arrive but no complete frames emerge, we need to investigate frame assembly and what arrived: missing or late packets may leave frames incomplete. ObserveRTC’s [frame-assembly-stalled detector](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/FrameAssemblyStalledDetector.ts) looks for this combination over time. It identifies a stalled boundary, not the reason it stalled.

If complete frames keep arriving but decoding stops, as in the figure, I would check whether the decoder has usable input. A complete frame may still depend on an earlier frame that was lost. Waiting for a usable keyframe is one possibility; a decoding problem is another. ObserveRTC’s [stuck-decoder detector](https://github.com/ObserveRTC/client-monitor-js/blob/ecbb77277306c35b32ad0d275e193a9687bf764e/src/detectors/StuckDecoderDetector.ts) brings together incoming traffic, stopped decoding, elapsed time, and recovery requests. Its name does not mean we have proved a decoder fault.

Recovery feedback adds another piece of evidence. An increasing `pliCount` tells us the receiver sent picture-loss indications. It does not prove that the sender received them or that a keyframe came back: [RFC 4585](https://www.rfc-editor.org/rfc/rfc4585.html#section-6.3.1) leaves the response subject to the sender’s circumstances, including congestion. And `keyFramesDecoded` counts successfully decoded keyframes, not keyframes that merely arrived.

If decoding keeps progressing but rendering stops, we would investigate playback and presentation instead. Check the media element, application state, and whether the page is in the background. These comparisons need available counters and valid intervals for the same stream; a missing measurement is not a zero.

Now change one observation: incoming traffic stops too. We need to look upstream. The receiver alone cannot tell us whether the source stopped, a server stopped forwarding, or the network stopped delivering. This is where sender measurements and application events help us connect the receiving symptom to the rest of the call.

What if the connection recovers after a network change, but video stays frozen? Connection recovery and media recovery are different observations. Measure when video actually resumes too. And if a restart fixes it, keep the measurements from before the restart: recovery helps the participant, but it does not explain the original failure.

That is the bigger picture in practice. We use the symptom to start the investigation, compare progress across stages, and bring in evidence from elsewhere in the call when the receiver cannot answer the next question.

## What’s next?

Next, we will look more closely at each category, starting with connectivity. We will also try ObserveRTC’s detectors: how to use them, what they can tell us, and what we still need to check. The plan is a new article roughly every three weeks.
