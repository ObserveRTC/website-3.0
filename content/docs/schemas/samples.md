---
contributors: {'Balázs Kreith', 'Balazs Kreith'}
title: "Samples"
date: 2021-06-08 08:11:43
lastmod: 2022-02-14 15:10:26
draft: false
images: []
menu:
  docs:
    parent: "schemas"
weight: 5040
toc: true
---
## Samples
---


A compound message object from the observed client to the observer
holds various samples, control flags and attachments.


Field | Type | Required | Description 
--- | --- | --- | ---
meta | SamplesMeta | No | Additional meta information about the carried payloads
clientSamples | array | No | array of client samples
sfuSamples | array | No | array of sfu samples
controlFlags | ControlFlags | No | Additional control flags indicate various operation has to be performed

## References
 * [Java Class](https://github.com/ObserveRTC/schemas-2.0/blob/main/generated-schemas/samples/v2/Samples.java)
 * [Schemas](https://github.com/ObserveRTC/schemas-2.0/tree/main/generated-schemas/samples/v2)
