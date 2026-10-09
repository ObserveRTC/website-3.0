---
slug: "specifications"
title: "Specifications and source references"
description: "Separate standard WebRTC behavior from library implementation."
lead: "Separate standard WebRTC behavior from library implementation."
draft: false
outputs: ["HTML", "Markdown"]
weight: 50
toc: true
---

Use a WebRTC standard to establish the meaning of a browser measurement. Use the versioned ObserveRTC implementation to establish how the library adapts, calculates, evaluates, or serializes it. A standard's field definition does not guarantee that a browser reports that field.

## Standard references

- [W3C WebRTC Statistics](https://www.w3.org/TR/webrtc-stats/) defines statistics and their semantics.
- [W3C WebRTC API](https://www.w3.org/TR/webrtc/) defines the browser API and connection behavior.
- [IETF ICE specification](https://www.rfc-editor.org/rfc/rfc8445) defines connectivity establishment.
- [IETF RTP specification](https://www.rfc-editor.org/rfc/rfc3550) defines RTP and RTCP.

## Implementation evidence

Check public interfaces and implementation first, then automated tests, published schemas/package definitions, standards, maintained project docs, and design discussions. A design proposal is not an implemented feature.

Exact versioned sources are linked from the relevant component pages and [version coverage](/docs/reference/versions/). Generated snapshots preserve their original baselines and are not automatically refreshed by installing a newer library.
