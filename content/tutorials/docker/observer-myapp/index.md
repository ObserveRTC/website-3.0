---
contributors: {'Balázs Kreith', 'Balazs Kreith'}
title: "Observer Myapp"
date: 2021-11-08 16:49:52
lastmod: 2021-11-10 15:06:48
draft: false
images: []
menu:
  tutorials:
    parent: "docker"
weight: 1010
toc: true
---

Observer + MyApp
===

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

