---
title: "Telemetry detectors"
description: "The facts describing a session, and why none of them raises an issue"
lead: "Not 'is this bad' but 'what was this' — which codec, which path, which layers, which device, and when each stopped being what it started as"
date: 2026-09-13T10:00:00+02:00
lastmod: 2026-09-13T10:00:00+02:00
draft: false
weight: 235
toc: true
---

This is the reference for **category 5**. Nothing here judges the call. What it buys is the missing
column in most investigations: *which* codec the bad calls were using, *when* the layer stopped
being sent, *whether* the path moved just before the complaint.

```text
Session     who, what call, what scope
Endpoint    what machine, browser and devices
Media       what is being encoded, sent and decoded
Transport   what path the media is travelling on
Lifecycle   what happened, and when — including to the instrument itself
```

**Telemetry has no rung in the ladder**, because it never fires. It is the context you read
*alongside* categories 1–4, and the five sub-layers are a vocabulary for what kind of context you
are reading.

**Several of these layers are not carried by detectors at all.** Session and Endpoint are sample
fields, client meta items and peer-connection lifecycle events; Transport is carried half by a
detector and half by `SelectedIcePath`, which is a monitor. They are documented here anyway, because
a reader asking "how do I find out what kind of path this call used" needs the answer regardless of
which mechanism provides it.

## What makes something telemetry

The membership test is deliberately counterfactual:

> **Would raising an issue here *ever* be the right thing to do? If no, it is telemetry.**

Not "does it raise one today". That phrasing is what stops the category becoming a bucket for
detectors nobody got around to finishing. Worked through the members:

- **`IceTraversalDetector`** — a threshold on tuple changes is what `UnstableIcePathDetector`
  already owns, and it is a different claim. What is left is a single path move, which is what
  happens when Wi-Fi hands over to cellular. Reporting a successful handover as a fault would be
  wrong at any threshold.
- **`CodecChangeDetector`** — H264 is not a fault, VP8 is not a fault, and a mid-call switch is
  renegotiation or a hardware encoder falling back to software: both are the system working.
- **`VideoResolutionChangeDetector`** — the adaptation ladder moving *is* the adaptation ladder
  working. A picture genuinely too poor to watch already has an owner in `PixelatedVideoDetector`.
- **`SimulcastLayerDetector`** — layers are *meant* to come and go.
- **`CaptureTrackMutedDetector`** — `track.muted` covers the deliberate system mute and the
  accidental device grab with one flag, and the library cannot tell them apart. Raising would file
  thousands of correct mutes as call failures.
- **`StatsGapDetector`** — the subject is not the call, it is the measurement.
- **`IceRestartDetector` / `IceRestartRecommendationDetector`** — a restart is what a healthy
  application *does*, so an issue would flag the recovery rather than the problem.

{{< callout context="caution" title="'Raises no issue' is not 'is telemetry'" icon="alert-triangle" >}}
Category is decided by the question a class answers, not by whether it raises an issue. Ten classes
in the library emit only events; **eight are telemetry and two are not**:

- `IcePathEstablishmentDetector` is **connectivity**, layer 3 — "establishment is taking a long
  time" is not yet a claim that it *failed*, and that claim is a separate class.
- `AudioPlayoutSynthesisDetector` is **perceived quality** — it fails the counterfactual test,
  because a listener hearing invented speech across a sustained window is a fault worth raising.

Filing either under telemetry would put a genuine finding somewhere nobody looks for findings.
{{< /callout >}}

## The grid

| Layer | What carries it | Class or mechanism | Event | Config key |
|---|---|---|---|---|
| Session | Sample fields | `createSample()` — `clientId`, `callId`, `attachments`, `timestamp` | *(none)* | `clientId`, `callId` |
| Session | Client events | `addClientJoinEvent()` / `addClientLeftEvent()` | `CLIENT_JOINED`, `CLIENT_LEFT` | `addClientJointEventOnCreated`, `addClientLeftEventOnClose` |
| Endpoint | Client meta items | `fetchUserAgentData()` | `USER_AGENT_DATA` *(meta)* | *(always, on creation)* |
| Endpoint | Client meta items | `watchMediaDevices()` | `MEDIA_DEVICE`, `MEDIA_DEVICES_SUPPORTED_CONSTRAINTS`, `USER_MEDIA_ERROR` *(meta)* | `integrateNavigatorMediaDevices` |
| Media | Detector | `CodecChangeDetector` | `codec-changed` / `CODEC_CHANGED` | `codecChangeDetector` |
| Media | Detector | `VideoResolutionChangeDetector` | `video-resolution-changed` / `VIDEO_RESOLUTION_CHANGED` | `videoResolutionChangeDetector` |
| Media | Detector | `SimulcastLayerDetector` | `simulcast-layer-changed` / `SIMULCAST_LAYER_CHANGED` | `simulcastLayerDetector` |
| Transport | Detector | `IceTraversalDetector` | `ice-tuple-changed` *(monitor event only)* | `iceTraversalDetector` |
| Transport | Monitor | `SelectedIcePath` | `ice-path-changed` / `PEER_CONNECTION_ICE_PATH_CHANGED` | *(always)* |
| Transport | Detector | `IceRestartDetector` | `ice-restart` / `ICE_RESTART` | `iceRestartDetector` |
| Transport | Detector | `IceRestartRecommendationDetector` | `ice-restart-recommended` / `ICE_RESTART_RECOMMENDED` | `iceRestartRecommendationDetector` |
| Transport | Sample fields | `IceTransportMonitor.createSample()` — roles, ciphers, ufrag | *(none)* | `sendIceTransportMetadataOnChangeOnly` |
| Lifecycle | Detector | `CaptureTrackMutedDetector` | `capture-track-muted` / `CAPTURE_TRACK_MUTED` | `captureTrackMutedDetector` |
| Lifecycle | Detector | `StatsGapDetector` | `stats-collection-gap` / `STATS_COLLECTION_GAP` | `statsGapDetector` |
| Lifecycle | Source binding | `watchTabVisibility()` | `TAB_VISIBILITY_CHANGED` | `watchTabVisibility` |
| Lifecycle | Source bindings | peer connection and track bindings | `PEER_CONNECTION_OPENED`, `MEDIA_TRACK_ADDED`, `ICE_CANDIDATE_ERROR`, … | *(per binding)* |

**Every detector row now names a key of its own.** Two used to be awkward and no longer are:
`IceTraversalDetector` was the one detector registered unconditionally, silenceable only by name,
and `CaptureTrackMutedDetector` used to come and go with the two capture detectors that *do* raise
issues — which is rarely what an application silencing mute noise actually wants.

## The shape they share: first observation is a baseline

Every change-reporting class treats the first value it sees as a baseline and reports nothing for
it. Without that, **every session would report a change in its first seconds**, for every track, for
nothing. A codec that was VP8 from the first tick did not change to VP8.

{{< callout context="caution" title="What that costs, stated plainly" icon="alert-triangle" >}}
A change stream tells you every transition and never tells you the starting state. A consumer
reading only `codec-changed` events cannot answer "what codec was this call using" for the
overwhelming majority of calls, because most calls change codec zero times.

| Fact | Change event | Where the initial state is |
|---|---|---|
| Codec | `codec-changed` | `PeerConnectionSample.codecs`, via `inboundRtps[].codecId` / `outboundRtps[].codecId` |
| Resolution | `video-resolution-changed` | `inboundRtps[]` / `outboundRtps[]` `frameWidth` / `frameHeight` |
| Simulcast layers | `simulcast-layer-changed` | `outboundRtps[]` — one row per encoding, with `rid`, `active`, `scalabilityMode` |
| Selected ICE path | `ice-tuple-changed` | `iceCandidatePairs[]` + `iceCandidates[]`, via `iceTransports[].selectedCandidatePairId` |
| Muted capture | `capture-track-muted` | `MEDIA_TRACK_ADDED`'s `muted` field, plus `MEDIA_TRACK_MUTED` / `_UNMUTED` |

**Sample plus events is the complete picture; either alone is not.**
{{< /callout >}}

One further caveat: `addEvent()` returns immediately when the monitor is not sampling and
`bufferingEventsForSamples` is false (the default). With `samplingPeriodInMs` unset or zero, **no
client event is recorded at all** — while the detector's own monitor event still fires. A monitor
configured to collect but not sample therefore has working telemetry on the event emitter and an
empty client-event stream, which is easy to mistake for a detector that is not working.

## Session

Session identity is carried by the sample itself: `clientId`, `callId`, `timestamp`, and
`attachments` — a free-form `Record<string, unknown>` for what the library cannot know, typically
`roomId`, `userId` and `displayName`.

`clientId` and `callId` are settable at any time (`monitor.clientId = …`), which matters for the
common shape where the monitor is constructed before the application knows which room the user is
joining. Samples created before they are set carry `undefined` and a server-side correlation has to
stitch them.

`close()` creates one final sample after adding the leave event, so `CLIENT_LEFT` ships rather than
dying in the buffer.

## Endpoint

`fetchUserAgentData()` runs once on construction and adds a `USER_AGENT_DATA` meta item with the
parsed browser, engine, OS, device and CPU records. The same call sets `monitor.browser`, which is
**not merely descriptive**: setting it installs the per-browser stats adapters on every peer
connection, so what the endpoint *is* changes what the library can *see*. Browsers outside the
recognised set are set to `unknown` rather than guessed at.

`watchMediaDevices()` reports `MEDIA_DEVICE` per enumerated device,
`MEDIA_DEVICES_SUPPORTED_CONSTRAINTS` once, and `USER_MEDIA_ERROR` when a `getUserMedia` call
rejects. The last is the one worth noticing: a permission denial or an `OverconstrainedError` is the
reason a great many "nothing worked" sessions have no media at all, and it is invisible in
`getStats()` because no track was ever created to have stats about.

## Media

### `CodecChangeDetector` → `codec-changed`

Which codec a track is using, and when that changes. The codec in use is the missing column in
nearly every aggregate quality question — why the bad calls cluster on H264, whether AV1 is being
negotiated anywhere at all, whether a hardware encoder quietly fell back to software mid-call.

**A change is a difference in either `mimeType` or `sdpFmtpLine`.** Comparing the mime type alone
would miss an H264 `profile-level-id` switch, which is a real codec change with real consequences —
a different profile is a different decoder path and a different bitrate efficiency — and would
otherwise be completely invisible.

```javascript
codecChangeDetector: { createEvent: true }
```

The cost is genuinely negligible, which is why this is on by default: a codec changes once or twice
in a call if it changes at all, unlike a per-tick metric.

### `VideoResolutionChangeDetector` → `video-resolution-changed`

Direction is classified by pixel count: `upgrade` when it rises, `downgrade` when it falls, and
`reshape` when the count is unchanged but the dimensions are not — an orientation change on mobile,
typically. A zero or absent frame size is a stream that has not produced a frame yet rather than a
downgrade to nothing, and is refused.

**`qualityLimitationReason` is the point of the event.** From the resolution alone, "the encoder
dropped resolution because of bandwidth or CPU" and "the application changed its constraints" are
identical, and confusing them sends an investigation in exactly the wrong direction. The field is
only meaningful outbound; on the receive side a resolution change usually means the SFU switched
which simulcast layer it forwards.

On an outbound simulcast track only the highest layer is followed, since the track legitimately
carries several resolutions at once.

{{< callout context="note" title="Two payloads, one confusing field name" icon="info-circle" >}}
The monitor event's field is `direction` (the `upgrade`/`downgrade`/`reshape` classification), while
the client event calls that field `change` and uses `direction` for `inbound`/`outbound`. They are
different names for different things in the two payloads, and reading one shape into the other is a
mistake the naming invites.
{{< /callout >}}

### `SimulcastLayerDetector` → `simulcast-layer-changed`

When the set of simulcast layers an outbound video track is *actually sending* changes. This is a
fact about encoder behaviour under bandwidth and CPU pressure, and it is otherwise completely
invisible: an SFU-side "why is this participant blurry" investigation has no client-side record that
the high layer stopped being produced at all.

**A layer counts as active only when the encoding is not explicitly disabled *and* it actually sent
bytes in the interval.** Trusting `active` alone would hide exactly the transition worth reporting:
`active: true` with no bytes is the common real-world shape of a layer the encoder has quietly given
up on.

Layers are named by `rid` where the application sets one and by SSRC otherwise. **While the producer
is paused the baseline is discarded entirely**, so resuming re-establishes it rather than reporting
the pause and the resume as two layer changes — this is the only member of the category with a pause
gate, and it is there because a paused producer sends no bytes on any layer.

`scalabilityMode` rides along in the per-layer snapshot and is worth having — it separates true
simulcast from SVC, and L1T3 from L3T3 — but it is **absent on Safari**. Treat `undefined` as "not
reported" rather than as "no scalability mode configured".

## Transport

### `IceTraversalDetector` → `ice-tuple-changed`

That the set of selected ICE candidate pairs changed — the network path underneath the call moved,
which is what a user experiences as the brief cut-out when Wi-Fi hands over to cellular, a VPN comes
up, or a NAT rebinding forces a new pair.

It holds a `Set<string>` of tuples (`localAddress:localPort:remoteAddress:remotePort:protocol`) and
diffs it both ways each tick. Because the tuple is computed in one place — on the candidate pair
monitor — this detector and the connectivity detectors can never disagree about what the selected
path is.

It emits the monitor event only: **this fact does not reach the sample through this detector at
all.** `iceTraversalDetector: {}` enables it, `null` disables it.

{{< callout context="tip" title="One raw signal, two categories" icon="rocket" >}}
The selected candidate pair changing is a single observation. Read once, it is a fact about the
session: the path moved, here is when. Read as a *rate* — three or more switches inside thirty
seconds — it is a claim that the path is oscillating rather than migrating, which is an **issue**
with a threshold and a resolve condition, raised by `UnstableIcePathDetector` from the same stats
independently. Neither reads the other's conclusion. That is not duplication; it is the difference
between recording a fact and judging it.
{{< /callout >}}

### `SelectedIcePath` — the path monitor

Not a detector. One per ICE transport with a selected candidate pair, reachable as
`pcMonitor.selectedIcePaths` (or `selectedIcePath` for the BUNDLE case). It is the single
authoritative interpretation of "what path is this peer connection actually using", and it holds no
copies of candidate data — every descriptive getter reads through the linked monitors, so the path
can never disagree with the stats it was built from.

`IcePathKind` is `direct`, `turn-udp`, `turn-tcp`, `turn-tls` or `turn-unknown`, derived
candidate-type-first. `turn-unknown` means TURN is definitely in use but the browser did not expose
how the endpoint reaches the TURN server.

Each tick it classifies the transition: `initial-selection`, `direct-to-relay`, `relay-to-direct`,
`relay-protocol-changed`, `turn-server-changed`, or a plain `path-changed`. **Unlike
`IceTraversalDetector` it does report the initial selection** — as a transition with no `from` —
which is what makes the event stream able to answer "what path did this call start on" at all.

What it computes and keeps live on the object (none of it reaches the sample):

| Field | What it holds |
|---|---|
| `durations` | Milliseconds spent in each `IcePathKind` |
| `relayDurationInMs` | The four relay kinds' durations summed |
| `timeToFirstRelayInMs` | From path creation to the first relay selection; `undefined` if never |
| `pathSwitches`, `directToRelaySwitches`, `relayToDirectSwitches` | Switch counts after the initial selection |
| `relayProtocolSwitches`, `turnServerSwitches` | Same TURN server on a different transport; a different TURN server |
| `totalBytesSent` / `Received`, `totalPacketsSent` / `Received` | Traffic observed across the path's life |
| `relayBytesSent` / `Received`, `relayBytesRatio` | The portion of that which travelled over a relay |
| `getSwitchCountSince(timestamp)` | Switches at or after a wall-clock instant, from a bounded 64-entry ring |

### The restart classes

`IceRestartDetector` and `IceRestartRecommendationDetector` are telemetry by category and documented
with the ladder they describe — see
[connectivity detectors](../detectors-connectivity/#restarts-the-telemetry-alongside-the-ladder).
They are listed here so a reader working from the category rather than the subject can find them:
**eight classes are categorised telemetry, six of them documented on this page.**

### What the sample already carries

`IceTransportMonitor.createSample()` ships `iceRole`, `iceLocalUsernameFragment`,
`localCertificateId`, `remoteCertificateId`, `tlsVersion`, `dtlsCipher`, `dtlsRole` and `srtpCipher`
as **static metadata**: under `sendIceTransportMetadataOnChangeOnly` (default `true`) they are
emitted in the first sample and again only when one of them changes — which for the username
fragment is exactly at an ICE restart.

{{< callout context="caution" title="Absence means unchanged, not unknown" icon="alert-triangle" >}}
A consumer must keep the last seen value per transport `id`. Set
`sendIceTransportMetadataOnChangeOnly: false` to restore every-sample emission.
{{< /callout >}}

## Lifecycle

### `CaptureTrackMutedDetector` → `capture-track-muted`

The moment something outside the application took the capture device away: `track.muted` flipped to
true. The OS grabbed the microphone for a system call, another application claimed exclusive camera
access, the lid closed, the privacy shutter moved, the device slept.

This is **not** the application's own mute — that is `track.enabled`, which the application sets and
therefore already knows about. `track.muted` is the browser's statement that the source has stopped
delivering data.

It reads the DOM track object and nothing from the stats, which makes it one of the few detectors
that would still work with no `getStats()` output whatsoever. Only the `false → true` transition is
reported; a track already muted when monitoring began is refused, because it may have been muted
since before the call.

The three capture classes, and why they are three:

| Class | Category | Raises | Because |
|---|---|---|---|
| `CaptureTrackMutedDetector` | Telemetry | *(event only)* | `track.muted` covers the deliberate system mute and the accidental device grab with one flag. Most mutes are correct |
| `CaptureSourceLostDetector` | Pipeline disruption | `capture-source-lost` | `readyState: 'ended'` is terminal and never intentional mid-call |
| `SilentAudioSourceDetector` | Pipeline disruption | `silent-audio-source` | A live, unmuted, enabled microphone producing digital silence for a sustained span is a broken capture chain |

What separates them is not where they sit in the stack — all three watch the same capture stage —
but **whether the observation could ever be the user doing something correct.** Ended and silent
could not; muted routinely is.

The value of the mute event is a **timestamp**: the record of when capture stopped, next to which
the silence and dry-track findings that follow stop looking mysterious.

### `StatsGapDetector` → `stats-collection-gap`

That stats collection itself ran late. This is telemetry about the *instrument*, not the call, and
it is **the only signal in the library that changes how you read the other signals**.

Every rate the library reports is a delta divided by an elapsed time, and all of them assume
collection happened roughly on schedule. When the tab is backgrounded, the device sleeps, or the
main thread is blocked long enough, counters keep advancing while the monitor is not looking, and
the first tick afterwards attributes a large accumulation to a short window — which reads as a
network event that never happened. Rather than trying to correct for it, the gap is reported so a
consumer can discount that interval.

```javascript
statsGapDetector: {
    gapRatioThreshold: 2,  // multiple of collectingPeriodInMs that counts as a gap
    minGapInMs: 5000,      // a single missed short tick is jitter, not a gap
    createEvent: true,
}
```

An overrun must clear **both** the ratio and the absolute floor. With the default 5-second floor and
a 200 ms collecting period, a 500 ms tick is 2.5× over and correctly says nothing.

**It is deliberately the one detector that measures wall-clock time.** Design rule 3 exists so a
backgrounded tab does not credit itself with a minute of watching a condition nobody observed;
applying it here would be meaningless, because **how late the library ran is exactly what this
detector exists to measure**, and stats time is by construction the clock that cannot see it. The
rule and this detector are not in tension: the rule protects verdicts about the *call*, and this
detector reports the monitor's scheduling as its subject.

A `stats-collection-gap` next to a burst of pipeline issues is very often the explanation for the
burst rather than a co-symptom of it.

### The client-event stream

Most of the Lifecycle layer is not detectors at all. The source bindings forward peer-connection and
track events into `addEvent()` as they happen: `PEER_CONNECTION_OPENED` / `CLOSED`,
`MEDIA_TRACK_ADDED` / `REMOVED` / `MUTED` / `UNMUTED`, `ICE_GATHERING_STATE_CHANGED`,
`ICE_CONNECTION_STATE_CHANGED`, `PEER_CONNECTION_STATE_CHANGED`, `SIGNALING_STATE_CHANGE`,
`NEGOTIATION_NEEDED`, `ICE_CANDIDATE`, `ICE_CANDIDATE_ERROR`, the data-channel events, and the
mediasoup producer and consumer events where a mediasoup transport is bound.

`TAB_VISIBILITY_CHANGED` sits with them and does double duty: it keeps `monitor.activeTab` in sync
so the pause-aware detectors can stand down, and it puts every transition in the sample stream so a
reader can see exactly when the tab went to the background and came back. Where no usable `document`
exists — SSR, workers, react-native — the watcher logs and leaves `activeTab` at `true`, because a
missing watcher must never look like a hidden tab.

This stream is telemetry by every part of the definition. It is not a detector because there is
nothing to detect: the browser already said it.
