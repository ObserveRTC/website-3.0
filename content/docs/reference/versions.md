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


## How to read these matrices

**Shared contract** means reviewed sources use the same sample schema. It does not mean the combination passed an end-to-end test. **Documented target** means the consumer explicitly describes that producer range. Unlisted versions are not assessed here. Library versions and sample schema versions are different numbers.

## Client Monitor JS and Observer

| Client Monitor JS | Observer JS | Sample schema | Compatibility evidence |
|---|---|---|---|
| 4.10.1 | 1.2.0 | 3.7.0 on both sides | Shared contract verified in pinned source; end-to-end combination not tested here. |
| Other releases | Other releases | Check both source contracts | Not assessed; do not infer compatibility solely from a major version. |

Observer ingestion requires `clientId` and `callId`. Your backend must authenticate and validate incoming samples and decode codec streams before calling `accept()`. Matching schema versions does not provide transport ordering, authentication, or missing browser fields.

Sources: [Client Monitor 4.10.1 schema](https://github.com/ObserveRTC/client-monitor-js/blob/4ae541eac3305d1cc779ff6dd703211e837a7f7b/src/schema/ClientSample.ts), [Observer 1.2.0 package](https://github.com/ObserveRTC/observer-js/blob/1.2.0/package.json), [Observer schema](https://github.com/ObserveRTC/observer-js/blob/1.2.0/src/schema/ClientSample.ts), and [ingestion implementation](https://github.com/ObserveRTC/observer-js/blob/1.2.0/src/Observer.ts).

## Client Monitor C++ and Observer

| Client Monitor C++ | Observer JS | Sample schema | Compatibility evidence |
|---|---|---|---|
| 0.1.0 | 1.2.0 | 3.7.0 on both sides | Shared contract; native-to-Observer integration not independently tested here. |

C++ 0.1.0 has partial detector coverage and no ported default score calculator. A default score of 5.0 is not a measured healthy-quality verdict. Its optional native bindings are listed as not yet compiled against libwebrtc/libmediasoupclient in the release notes. These limitations remain even when sample contracts match.

Sources: [C++ 0.1.0 release](https://github.com/ObserveRTC/client-monitor-cpp/releases/tag/v0.1.0) and [porting status](https://github.com/ObserveRTC/client-monitor-cpp/blob/v0.1.0/PORTING.md). See [Native C++ integration](/docs/client-monitor-js/native-cpp/).

## Producers, Observer, and Stats Dashboard

| Producer | Observer JS | Stats Dashboard | Evidence and limits |
|---|---|---|---|
| Client Monitor JS 4.10.1 | 1.2.0 | Package 0.1.0, commit `323a1b2` | Shared 3.7.0 contract; JS version falls within the dashboard's documented 4.9.0+ target. Complete pipeline not tested here. |
| Client Monitor C++ 0.1.0 | 1.2.0 | Package 0.1.0, commit `323a1b2` | Shared 3.7.0 contract; native dashboard integration unverified, with missing detector/scoring capabilities. |

The dashboard reads archived JSONL samples, not an Observer process directly. Store streams using its documented layout and preserve the required sample fields. Server/router diagnostics require their own data; matching a client schema does not supply SFU mapping.

Stats Dashboard's package declares 0.1.0, but no published GitHub release was listed on October 13, 2026. Pin the commit for reproducibility until a tagged release is available. Sources: [package](https://github.com/ObserveRTC/stats-dashboard/blob/323a1b28553758edafaa0abd0d4211c9e13de9ea/package.json), [documented schema target](https://github.com/ObserveRTC/stats-dashboard/blob/323a1b28553758edafaa0abd0d4211c9e13de9ea/src/schema/ClientSample.ts), and [fixture tests](https://github.com/ObserveRTC/stats-dashboard/blob/323a1b28553758edafaa0abd0d4211c9e13de9ea/scripts/realFixture.test.ts). Start with the [Stats Dashboard overview](/docs/stats-dashboard/).

## Documentation source baselines

| Component | Examined revision | Package/source version | Meaning |
|---|---|---|---|
| Client Monitor installation/configuration | `4ae541eac3305d1cc779ff6dd703211e837a7f7b` | 4.10.1 | npm latest checked October 9, 2026; configuration verified against release source |
| Client Monitor field/formula catalog | `0f08bd5d110a4e9d53cf0486962e638c5b393c49` | 4.9.1 | Pinned implementation reference; not npm latest |
| Observer | tag `1.2.0` | 1.2.0 | Current release contracts reviewed October 13, 2026; some detailed references retain explicitly pinned sources |
| Schemas | `eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17` | schema 3.7.0; generator package 3.0.0 | `sources/version.txt` is the schema version |

{{< details "Source references" >}}

- [client-monitor-js/package.json](https://github.com/ObserveRTC/client-monitor-js/blob/0f08bd5d110a4e9d53cf0486962e638c5b393c49/package.json)
- [observer-js/package.json](https://github.com/ObserveRTC/observer-js/blob/b4a1ccb85468c94084a89ed2c007708c14ead551/package.json)
- [schemas/sources/version.txt](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/sources/version.txt)
- [schemas/package.json](https://github.com/ObserveRTC/schemas/blob/eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17/package.json)

{{< /details >}}

Client Monitor **4.10.1** was checked on October 9, 2026. Observer **1.2.0** was released October 13, 2026. Install with `npm install @observertc/client-monitor-js` to follow the published `latest` tag.

The table also records older source revisions used to verify detailed formulas, detector evidence, and generated field catalogs. Configuration has been checked against 4.10.1, but the generated field catalog and historical detector references have not been regenerated; do not interpret them as an exhaustive API inventory for that release. See [Updates](/updates/) for newer releases and release notes.

### Feature-level requirements

Schema 3.7.0 compatibility does not guarantee audio echo evidence. `AudioEchoDetector` needs usable audio levels across participants. Receiver-derived publisher levels require a configured remote track resolver. `AUDIO_INPUT_DEVICE` metadata is described by the 1.2.0 release as a Client Monitor JS next capability, so do not assume it is emitted by JS 4.10.1 or C++ 0.1.0. The dashboard's pinned source has not been verified to display every Observer 1.2.0 session-total or echo field.
