---
contributors: {'Balazs Kreith', 'Balázs Kreith'}
title: "Observer Myapp"
date: 2021-11-08 14:49:52
lastmod: 2021-12-01 04:53:04
draft: false
images: []
menu:
  tutorials:
    parent: "docker"
weight: 1030
toc: true
---

Observer + MyApp
===

TBD

Setup an observer sends reports to a [socket.io](http://socket.io) sink.
a custom NodeJS service, [myApp](myapp/) receives reports from the observer 
and calculate the number of calls started, ended and durations to a prometheus 
`/metrics` endpoint at myApp.

### Usage

```shell
    docker-compose up 
```


### Configurations

Observer configuration files (`observer-config/config.yaml`) setup a sink to the kafka.

