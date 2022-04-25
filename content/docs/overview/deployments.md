---
contributors: {'Balázs Kreith'}
title: "Deployments"
date: 2021-11-27 18:00:13
lastmod: 2021-01-02
draft: false
menu:
  docs:
    parent: "overview"
weight: 1050
toc: false
images: ["k8s-deployment-overview.png"]
---

[Monitors]() does not require deployments, but they must be integrated into media units such as front-end applications, or backend selective forwarding units.

[Observer]() is published to [dockerhub](https://hub.docker.com/r/observertc/observer/tags). 
It is a stand-alone application can be run with a command `docker run observertc/observer`.

The [full stack example repository](github.com/ObserveRTC/full-stack-examples) uses docker-compose as an example.

## Kubernetes deployment

We maintain a [helm chart repository](https://github.com/ObserveRTC/helm) to deploy Observer through [helm package mananger](https://helm.sh).

