# ObserveRTC documentation website

Hugo/Doks website for Client Monitor, Observer and the sample schemas. This project is separate from the live mediasoup demo (`webrtc-observer.org`).

## Run locally

Requires Node.js 20.11+ and **Hugo Extended** (verified with 0.143.1). Python 3 is used only for the link check.

```sh
npm ci
npm run dev -- --bind 127.0.0.1 --port 1313
```

Open http://localhost:1313. Hugo rebuilds when content, templates or styles change. This documentation preview does not start a WebRTC call or request camera/microphone access.

If Hugo is missing on macOS:

```sh
brew install hugo
```

Production build and internal-link verification:

```sh
npm run build
npm run check
```

## Editing

- `layouts/index.html`: ecosystem home page.
- `assets/scss/common/_custom.scss`: branding and responsive layouts.
- `layouts/partials/docs/page.html`: consistent documentation column, sidebar and table of contents.
- `content/docs/`: guides and references. Explicit slugs keep URLs stable when titles change.
- `data/monitors.json`: generated public field/accessor catalog, including constructor properties.
- `assets/js/monitor-catalog.js`: accessible search/filter controls; native details remain usable without JavaScript.
- `static/reference/`: pinned implementation references and offline source atlas. They are not loaded by the home page.

## Source baseline

Client Monitor 4.9.1 (`0f08bd5d110a4e9d53cf0486962e638c5b393c49`), Observer 1.0.0 (`b4a1ccb85468c94084a89ed2c007708c14ead551`), schemas 3.7.0 (`eb7fe28062b81d6db9dfb7ca565b1fb9c88b5d17`).

Regenerate the monitor catalog from a clean pinned Client Monitor checkout:

```sh
node scripts/generate-monitor-catalog.mjs /path/to/client-monitor-js
npm run build
npm run check
```

The generator uses the TypeScript AST, includes public constructor parameter properties, excludes private/protected members and the destructive `visited` bookkeeping accessor, and rejects an unexpected or locally edited source revision. A schema field is not automatically classified as a native browser statistic. Review provenance and formulas in the metrics guide.

When updating the baseline, refresh the implementation references, verify the differences page, review the generator's revision guard and rerun the build/link checks. Historical schema pages remain available separately from current integration guidance.
