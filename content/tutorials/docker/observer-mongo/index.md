---
contributors: {'Balazs Kreith', 'Balázs Kreith'}
title: "Observer Mongo"
date: 2021-08-26 12:36:40
lastmod: 2021-11-08 18:05:50
draft: false
images: []
menu:
  tutorials:
    parent: "docker"
weight: 1000
toc: true
---

<!---
Observer + Mongo
===
--->

Setup an observer that sends the generated reports to MongoDB.

### Usage

```shell
    docker-compose up
```

Go to mongo express at [http://localhost:8081](http://localhost:8081) and
enter the username and password (root/password). You will find the
reports under the database you set up (default: `ortc_reports`).

### Configurations

Observer configuration files (`observer-config/config.yaml`) set up a sink to the mongo.


