---
title: "FAQ"
description: "Answers to frequently asked questions."
lead: "Answers to frequently asked questions."
date: 2021-04-01
lastmod: 2021-04-01
draft: false
images: []
menu:
  docs:
    parent: "help"
weight: 9010
toc: false
---

### What is the license of ObserveRTC components?

Apache-2.0

### How can I contribute to the source code?

Find the repository you want to work on, and work.

### I want to send reports to my database. How can I do it?

If the database type is supported by the Observer, then configure it to forward.
Or else you need to add your Sink implementation.
 * if you want to add as a general sink, then open a PR in observer repository.
 * if you want to develop it in your private realm, then develop and compile the observer by yourself.
 * additionally you can forward it to kafka as it is integrated and you can use one of a kafka connector to forward Reports into yor database.
