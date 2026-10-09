---
slug: "versions"
title: "Versions and compatibility"
description: "Installation guidance and verified source reference versions."
lead: "Installation guidance and verified source reference versions."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
outputs: ["HTML", "Markdown"]
weight: 20
toc: true
---

| Component | Examined revision | Package/source version | Meaning |
|---|---|---|---|
| Client Monitor installation/configuration | `4ae541eac3305d1cc779ff6dd703211e837a7f7b` | 4.10.1 | npm latest checked October 9, 2026; configuration verified against release source |
| Client Monitor field/formula catalog | `0f08bd5d110a4e9d53cf0486962e638c5b393c49` | 4.9.1 | Pinned implementation reference; not npm latest |
| Observer | `b4a1ccb85468c94084a89ed2c007708c14ead551` | 1.0.0 | Pinned implementation reference; not a claim about npm latest |
| Schemas | `eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17` | schema 3.7.0; generator package 3.0.0 | `sources/version.txt` is the schema version |

{{< details "Source references" >}}

- [client-monitor-js/package.json](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/package.json)
- [observer-js/package.json](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/package.json)
- [schemas/sources/version.txt](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/version.txt)
- [schemas/package.json](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/package.json)

{{< /details >}}

Client Monitor **4.10.1** and Observer **1.1.0** are the current npm releases checked on October 9, 2026. Install with `npm install @observertc/client-monitor-js` to follow the published `latest` tag.

The table also records older source revisions used to verify detailed formulas, detector evidence, and generated field catalogs. Configuration has been checked against 4.10.1, but the generated field catalog and historical detector references have not been regenerated; do not interpret them as an exhaustive API inventory for that release. See [Updates](/updates/) for newer releases and release notes.
