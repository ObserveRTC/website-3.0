---
slug: "website-audit"
title: "Demo catalog audit"
description: "The live demo and this documentation site are separate projects."
lead: "The live demo and this documentation site are separate projects."
lastmod: 2026-09-28T12:00:00+03:00
draft: false
weight: 50
toc: true
---

The downloaded `webrtc-observer.org` repository is primarily an interactive diagnostics demo. Its design source is `design/Client Monitor.dc.html`; `tools/build-page.py` transforms it into committed `public/index.html`. Browser modules implement pipelines, catalog, scores, journal, sample viewer and hand-authored field/issue explanations. It is a plain JS/esbuild app, not a React site. Separately, `website-3.0` holds the project's documentation site and is relevant to informational content. Those are different products and should not silently be treated as one repository.

Catalog extraction reads **installed** `dist/monitors/*.d.ts`, `dist/ClientMonitor.d.ts`, and `dist/schema/ClientSample.d.ts`. It uses a hard-coded monitor/type map and regex parsing, includes only selected primitive types/getters, and classifies fields by schema membership. It also extracts monitor-event names. It does **not** derive formulas, units, detector configs, state machines, descriptions, or evidence relationships. Hand-authored explanations live in field-notes.js, issue-notes.js and pipeline modules. [webrtc-observer.org/tools/extract-monitors.py](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/tools/extract-monitors.py), [webrtc-observer.org/client/catalog.js](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/client/catalog.js), [webrtc-observer.org/client/field-notes.js](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/client/field-notes.js), [webrtc-observer.org/client/issue-notes.js](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/client/issue-notes.js), [webrtc-observer.org/client/pipeline.js](https://github.com/ObserveRTC/webrtc-observer.org/blob/45c754f784e915c8b0c8f467e6edd3a178f8df64/client/pipeline.js).

Confirmed issues:

| Finding | Why it matters / source of truth |
|---|---|
| Catalog generated from 4.9.0; stable is 4.9.1; next adds/renames audio detection | Show version/channel explicitly; never mix future docs into stable tooltips |
| Only 17 classes/555 primitive fields | Missing ExtensionStatsMonitor and SelectedIcePath; omits structured stats, contexts, arrays/maps and APIs |
| `clientId`, `closed`, `activeTab` labeled derived | These are identity/lifecycle/context, not calculated WebRTC measurements |
| Schema membership used as raw provenance | Firefox reconstructed transport and inferred IDs can share the same stat types; next raw Chromium extras are outside schema and would be falsely called derived |
| Pattern description says counter resets mean “no change” | positiveDelta yields undefined; zero would falsely suggest a stall |
| Pattern `*Rate` means per second | timeStretchRate/discardRate are fractions; naming cannot define units |
| Pattern `total*` means monotonic | available bandwidth totals are gauges, not counters; use explicit metadata |
| transportStability tooltip describes path changes and consent | actual calculation is RTT/jitter/loss MOS normalization |
| PC score tooltip says tracks contribute | getter is calculatedStabilityScore; track scores contribute separately to root dimensions |
| Root score tooltip says subtract weighted faults | actual aggregation is RMSE over dimension shortfalls |
| Uplink/downlink tooltips describe loss/jitter-based heuristics | current directional detectors use baseline undershoot and pacer/jitter-buffer bloat with distinct gating |
| Build does not regenerate catalog/page | an installed upgrade can leave a stale field/event catalog; generation belongs in a controlled build/check step |
| Automatic join on page load | Project documentation visitors are immediately put into demo behavior |

Visual inspection in the app's narrow browser pane reproduced clipped horizontal navigation and a 4+1 score-dimension grid with a large empty region. Source also uses fixed-width subgrids and many inline layout rules. This supports the reported ergonomic concern, but it is not a completed desktop/mobile breakpoint audit. The server's local loopback worked; no website content was rewritten.

Recommended structure preserving the visual language:

1. **Project overview**: one concise explanation, component/data-flow diagram, install entry points, links to client/server/schema references.
2. **Integrate**: browser, mediasoup, transport/backend, storage examples with version badges and copyable tested commands.
3. **Reference**: monitor graph, fields, detectors, events/issues, scoring and schema. Each field gets origin, unit, availability, formula, guards, wire projection and consumer links. Each detector gets inputs, defaults, raise/resolve, unsupported cases, event/issue shape and source.
4. **Live demo**: explicit Start, separate from reading documentation; stable page shell with consistent content alignment and a collapsible media panel.
5. **Migration/version notes**: released versions and 4.9.0→4.9.1 lifecycle fixes.

For the demo, replace the single long tab strip with a compact navigation group, use one shared content grid with `minmax(0,1fr)`, stack panels at explicit breakpoints, keep prose to a one-sentence explanation plus expandable detail, and avoid reflowing five dimensions into an accidental four-plus-one block. Preserve colors, typography, radii, chart style and spacing tokens; restructure page hierarchy and component layout. This is a proposal, not an implemented redesign.
