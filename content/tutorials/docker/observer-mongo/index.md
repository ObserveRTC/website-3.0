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

Observer + Mongo
===

Setup an observer, which sends the generated reports to MongoDB.

### Usage

```shell
    docker-compose up 
```

Go to http://localhost:8081 mongo express, enter with the username and password (root/password) and there you will find the reports under the database you setup to save them (`ortc_reports`).

### Configurations

Observer configuration files (`observer-config/config.yaml`) setup a sink to the mongo.


