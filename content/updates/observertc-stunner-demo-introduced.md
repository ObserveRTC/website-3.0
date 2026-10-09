---
title: "Introducing the ObserveRTC STUNner demo"
date: "2026-10-01T19:22:18Z"
draft: false
project: "STUNner demo"
summary: "A working mediasoup deployment on Kubernetes, reached through one public TURN endpoint and monitored with ObserveRTC."
sourceUrl: "https://github.com/ObserveRTC/observertc-stunner-demo"
sourceLabel: "Explore project on GitHub ↗"
---

## WebRTC media through one public endpoint

The ObserveRTC STUNner demo is a working example of a mediasoup SFU running inside Kubernetes. STUNner acts as a TURN ingress gateway: browsers reach the media servers through one public IP and UDP port, while the servers remain ordinary pods behind a ClusterIP service.

The demo combines a call application, deployment configuration and monitoring so you can explore both the network architecture and its effect on media quality.

## What you can explore

- Browser diagnostics from Client Monitor and server-side call analysis from Observer.
- A Solid-based call interface and a page displaying STUNner metrics through Grafana.
- Helm configuration for the media servers, STUNner, Envoy Gateway, certificates and monitoring.
- A Puppeteer load generator for exercising the deployment.

## Run it yourself

Use the repository’s [deployment instructions](https://github.com/ObserveRTC/observertc-stunner-demo/blob/main/charts/webrtc-observer-org/README.md) to run your own instance.

The architecture is described in [One Port to Rule Them All](https://medium.com/l7mp-technologies/one-port-to-rule-them-all-turn-webrtc-media-servers-into-a-single-kubernetes-service-e564c2d5327c), which also discusses measuring the additional latency.


---

Source: [STUNner demo repository](https://github.com/ObserveRTC/observertc-stunner-demo). Dated from GitHub’s repository creation timestamp (2026-10-01T19:22:18Z); this is a project introduction, not a tagged release.
