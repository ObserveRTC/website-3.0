---
slug: "native-cpp"
title: "Native C++ integration"
description: "Bring Client Monitor telemetry to applications using libwebrtc or libmediasoupclient."
lead: "Monitor native WebRTC endpoints alongside your browser clients."
draft: false
outputs: ["HTML", "Markdown"]
weight: 15
toc: false
---

If your application uses native WebRTC rather than a browser connection, [Client Monitor C++](https://github.com/ObserveRTC/client-monitor-cpp) provides a C++17 port of Client Monitor with optional bindings for libwebrtc and libmediasoupclient. It collects statistics, maintains live monitors, evaluates supported detectors, and produces `ClientSample` records for backend analysis.

This is a native implementation, rather than a binding that runs the JavaScript library. Your application keeps ownership of its connections and sample transport.

{{< component-flow from="Native connection" fromText="Your application uses libwebrtc or libmediasoupclient." via="Client Monitor C++" viaText="Collect statistics, calculate metrics, and evaluate supported detectors." to="Your backend" toText="Deliver ClientSample records for Observer analysis or storage." caption="Native and browser clients participate in the same sample-based monitoring architecture." >}}

The first tagged release is [v0.1.0](https://github.com/ObserveRTC/client-monitor-cpp/releases/tag/v0.1.0), published October 13, 2026. Pin that tag when evaluating the native integration.

## Add it to your application

The project is a source-built CMake library. Its documented requirements are C++17, CMake 3.14 or later, threads, and `nlohmann::json`. Enable the binding appropriate to your application's WebRTC stack and compile against compatible libwebrtc headers and build settings.

Follow the repository's [installation and binding instructions](https://github.com/ObserveRTC/client-monitor-cpp/tree/v0.1.0#add-it-to-your-application), then its [API guide](https://github.com/ObserveRTC/client-monitor-cpp/blob/v0.1.0/docs/USAGE.md). The native API uses PascalCase methods and `ClientMonitor::Listener` interfaces in place of JavaScript event listeners. Do not copy the browser quick start unchanged into a C++ application.

## Check coverage before choosing detectors

The v0.1.0 source identifies Client Monitor JS 4.11.0 and sample schema 3.7.0 as its porting baselines. It lists five ported detectors: `StatsGapDetector`, `IceDisconnectedDetector`, `TransportDelayDetector`, `DryInboundTrackDetector`, and `DryOutboundTrackDetector`. Other detector and browser-specific capabilities are not all ported.

Read the [porting status](https://github.com/ObserveRTC/client-monitor-cpp/blob/v0.1.0/PORTING.md) before assuming parity with the JavaScript library. The release notes state that the optional libwebrtc and libmediasoupclient bindings have not yet been compiled against either dependency. Treat native integration compatibility as something to verify in your application build.

The default score calculator and MOS scoring are not ported. Without a custom score calculator, the client score stays at 5.0; that value is not evidence of healthy media quality. Selected ICE path tracking and SDP monitoring are also not ported.

The release includes an API guide and `examples/api_tour.cpp`, which the release notes describe as compiled and run in CI.

Continue with [Observer](/docs/observer-js/) when you need a backend view across clients, or [Send samples to your backend](/docs/getting-started/backend/) for the collection/delivery/analysis boundaries.
