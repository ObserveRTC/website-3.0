# ObserveRTC documentation website

Hugo/Doks website for Client Monitor, Observer and the sample schemas. This project is separate from the live example (`webrtc-observer.org`).

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
- `static/reference/`: public library implementation references. They are not loaded by the home page.

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

## Analytics and newsletter REST endpoints

The frontend remains static Hugo/Doks. Configure `[services]` in
`config/_default/params.toml`:

```toml
[services]
analyticsEndpoint = "https://ingest.observertc.org/analytics"
subscribeEndpoint = "https://ingest.observertc.org/subscribe"
analyticsInDevelopment = false
```

An empty URL disables that integration. Development previews do not send analytics.
The subscription form uses JavaScript and sends only when submitted. These public
URLs contain no credentials; object storage access belongs on your server.

Both endpoints accept `POST` with `Content-Type: application/json` and no browser
credentials. Analytics receives one record per page load:

```json
{"version":1,"event":"page_view","path":"/docs/overview/introduction/","timestamp":"2026-10-08T12:00:00.000Z"}
```

No query string, fragment, referrer, email, cookies, or persistent visitor ID is
included. Do Not Track and Global Privacy Control suppress analytics. This measures
page views, not unique people or sessions. Network errors never block the page.

Subscription payload:

```json
{"version":1,"email":"reader@example.com","source":"website","consent":"monthly-newsletter-v1","timestamp":"2026-10-08T12:00:00.000Z"}
```

Return a successful 2xx response **after recording** the subscription; response body
is optional. Non-2xx or network failures show a retry message; requests time out after
15 seconds. Repeated clicks are blocked while a request is pending. Your server
should validate input, deduplicate subscribers, and rate limit requests. Client
timestamps are informational; add your own received time when storing records.

For cross-origin hosting, handle `OPTIONS` preflight and return
`Access-Control-Allow-Origin` for the website origin (including localhost if testing),
`Access-Control-Allow-Methods: POST, OPTIONS`, and
`Access-Control-Allow-Headers: Content-Type`. Return the origin header on error
responses too. Keep storage credentials and access to subscriber exports private.

Store analytics as separate objects and subscribers under deterministic keys to
avoid concurrent overwrites. Sending monthly email and handling removals are server
or manual responsibilities; the website only records signups. The Privacy page has been removed; keep newsletter copy accurate about the
actual subscription behavior.

The sample blog post is excluded from listings via `example: true`. Add real Markdown
posts under `content/blog/`; the homepage automatically displays the newest three.

For articles published elsewhere, set `publication`, `author`, `externalUrl`, and
`layout: external` in the post front matter. Blog and homepage cards link directly
to the original publication; the local page provides a summary for feeds and search.

## Release updates

Release notes and maintainer commentary live under `content/updates/`, separate
from blog articles, and appear newest first at `/updates/`.

Create an update with `hugo new content updates/client-monitor-next.md`.
The archetype includes release notes and maintainer notes sections, plus optional
`project`, `version`, `summary`, and `releaseUrl` metadata. Set the date and title,
write the notes, and change `draft: true` to `draft: false` when ready to publish.
Commentary is Markdown written by maintainers; no visitor comment backend is needed.

For deployment steps, verified limitations, and the browser/privacy assessment,
see [Ingestion migration](docs/ingestion-migration.md). Infrastructure and real
browser/ad-blocker verification must be completed on the service deployment.
