# Working on the ObserveRTC website

These instructions apply throughout this repository. They capture the user's
established preferences; a newer explicit user instruction takes precedence.

## Scope and architecture

- Keep this a simple, fast, self-hostable static Hugo/Doks site. Avoid adding a
  frontend framework, database, CMS, or backend dependency for ordinary changes.
- Use repository templates, SCSS, and small local JavaScript modules. Override
  theme files in `layouts/` or `assets/`; do not edit `node_modules/`.
- Preserve existing uncommitted work. Make focused edits; avoid repository-wide
  formatting, generated-output edits, or unrelated cleanup.
- This repository owns the frontend. DNS, TLS, CORS, object storage credentials,
  subscriber exports, and email delivery belong to the separate server deployment.

## Design and wording

- Keep ObserveRTC's font style, logo, and orange theme. The layout direction is
  inspired by GoReleaser, while retaining ObserveRTC's identity.
- Homepage headline: **Understand Every WebRTC Connection.** Keep the line break
  before “WebRTC Connection.” and its orange emphasis.
- Secondary motto: **From Signals to Insights.**
- Light mode is the default, independent of system preference. A visitor can
  explicitly select dark mode, and that selection is remembered.
- Keep Doks `colorMode = "auto"` and `colorModeToggler = true`: they enable the
  switch and script. Actual default behavior lives in `assets/js/color-mode.js`.
  Setting the Doks option to `light` would remove the switch.
- Theme switching must work across the entire button and through keyboard input.
  Use theme variables for custom surfaces, borders, text, and accent colors.
- Selected and hovered docs links and Updates pagination must be orange in both
  themes, never the stock purple. Check selector specificity against Doks styles.
- The main Docs link stays bold and orange throughout the docs section. Match
  its menu identifier to `.Section`, not the article title or humanized section.
  Keep `identifier = "docs"` on the main menu entry and the explicit section
  match in `layouts/partials/header/header.html`. The active anchor needs the
  `active` class and `aria-current`. Verify both on the quick start, component
  pages, and nested docs routes after changing navigation.
- Scope Bootstrap ScrollSpy to a rendered table of contents. On docs pages without
  `#toc`, omit its body attributes; Bootstrap otherwise falls back to the body
  and removes the main navigation active class. Keep the TOC condition in
  `layouts/_default/baseof.html` aligned with `layouts/partials/docs/page.html`.
- Live example links to `https://webrtc-observer.org/` open in a new tab with
  `target="_blank"` and `rel="noopener noreferrer"`, preserving the website tab.
- Every page includes the shared footer with Contact and ObserveRTC branding.
  Contact remains a standalone page without previous/next article navigation.
  The Privacy page and its navigation/form links were deliberately removed.
- Use the existing ObserveRTC favicon artwork, not stock theme icons.

## Documentation and readability

- `sfu-monitor-js` is deprecated. Do not list it as a current component or
  restore its obsolete license/reference links. SFU integration belongs to
  Observer; verify supported capabilities against Observer source.

- Read `docs/documentation-guidelines.md` when creating or restructuring docs.
- Keep navigation at two levels: section → page. Architecture stays in Overview.
  Component sections retain engineering-oriented implementation details.
- Use `content/docs/concepts/telemetry.md` as the single shared glossary.
- Use sentence-case headings and the page archetypes in `archetypes/docs/` where
  appropriate. Guides include prerequisites, observable outcomes, and diagnostics.
- Ground contracts in public interfaces/implementation, tests, schemas/package
  definitions, and W3C/IETF specifications. Distinguish source review from runtime
  testing and current releases from historical generated snapshots.
- Keep component and problem-oriented discovery connected by links, without
  duplicating contracts. Markdown outputs and the agent index use the same source.


- Write for engineers integrating the libraries, not their internal maintainers.
  Explain purpose, practical steps, and consequences before implementation details.
- Put quick start first, then integration, configuration, live API/metrics, and
  collection/sampling. Give application context, events, and issues separate guides.
- Install examples use unpinned npm package names. Client Monitor 4.10.1 was
  confirmed as npm latest on October 9, 2026. Keep verified older source baselines
  explicit; do not claim generated references cover a newer release without review.

- Docs explain APIs, configuration, and ongoing usage. Release announcements,
  upgrade articles, and release-specific integration notes belong in Updates;
  external authored articles belong in Blog. Avoid duplicating those in Docs.
- Titles and headings must be plain text, without inline-code backticks. In prose,
  format actual method, class, property, field, and configuration identifiers as
  inline code. Preserve readable paragraphs, headings, lists, and code examples.
- JSON Codec and Protobuf Codec belong under `content/docs/codecs/`. Preserve
  aliases when moving published docs and check links and navigation afterward.
- Keep sidebar geometry stable between short/long articles: reserve scrollbar
  space, use consistent link dimensions, and preserve menu scroll/collapse state
  through `assets/js/docs-navigation.js`. Restore after layout/font loading,
  keep the active item visible, and never overwrite saved desktop scroll from
  a hidden sidebar or a separate mobile drawer.
- The desktop sidebar and mobile drawer body must each own their scrolling.
  Override Doks overflow/height on their inner `.section-nav.docs-links`; a second
  scroll container makes saved positions unrelated to the menu the reader scrolls.
- Keep subsection links at the original regular weight (400), with the active
  item at 500 and orange. Do not make every article link heavier to fix scrolling.
- Keep the desktop docs sidebar wide enough for article titles on one line
  (currently 320px), with compact subsection spacing and readable section/article
  fonts. Preserve mobile navigation rather than forcing the desktop layout.
- Successful copying uses green button text and border, with no check icon or
  overlay. Suppress theme pseudo-elements even on focus and active states.
- Code blocks use a plain box and an accessible copy button. Do not add
  decorative window dots, filename/title bars, or captions inside code boxes.
  Keep the render hook override and homepage code box consistent.
- Code samples should retain intentional line breaks. Avoid wrapping a package
  import solely because a code panel is too narrow; use responsive sizing or
  horizontal scrolling when necessary.
- Table identifier columns should fit detector/class names on one line; allow
  descriptions to wrap and use horizontal scrolling on narrow screens.

### Detector catalogs

- Use `detector-table` and `detector-row` shortcodes for the client detector catalogs.
- Collapsed rows show a friendly **Name** and a short **Description**, not a class
  name and detailed trigger/recovery conditions.
- Expanded content spans the full row and starts at the left, with readable
  headings: **Class**, **What it collects**, **What triggers it**, **What resolves
  it**, and **Example**. Use the existing observation/reset headings where a
  detector reports telemetry or lifecycle state rather than a recoverable issue.
- Link the actual class identifier to verified source. Do not invent conditions,
  collected fields, defaults, or API behavior. Examples must match the evidence.
- Expanding a row must not change its summary padding, width, or position. Doks
  applies default `details`/`summary` margins and widths; retain the explicit
  catalog overrides that prevent jumping.
- The monitor catalog generator checks a pinned clean source revision. Do not
  bypass its guard or silently move documentation baselines to newer releases.

## Updates and Blog

- Updates live in `content/updates/`, newest first, with **20 cards per page**.
- Publish major/minor releases, not patch releases. Client Monitor 4.9.1 and
  4.10.1 posts were deliberately removed; do not reintroduce patch cards.
- Schema Updates start at **3.0.0**. Each eligible schema release gets its own card;
  do not restore pre-3.0.0 or beta schema update posts.
- Verify dates from the actual release or version commit. Distinguish repository
  creation dates from release dates, and retain source links for imported notes.
- Project introductions for the STUNner demo and Stats Dashboard belong in Updates.
- The STUNner demo introduction must not claim `webrtc-observer.org` still hosts
  that demo: the page was repurposed. Link the repository deployment instructions.
- Maintainer comments are Markdown in the update article; no visitor comment
  backend is required.
- External Blog cards link directly to the original publication. Use the existing
  `layout: external`, `externalUrl`, `publication`, and `author` metadata, with an
  original summary rather than copying an entire third-party article.

## Newsletter and analytics

- The newsletter is **one email per month** covering releases/improvements,
  guides/articles, and project news. Explain this beside the form and in consent
  text. Do not promise functionality such as unsubscribe that is not implemented.
- Configure public URLs centrally in `config/_default/params.toml`:
  - `POST https://ingest.observertc.org/analytics`
  - `POST https://ingest.observertc.org/subscribe`
- Keep version-1 JSON contracts unchanged unless backend support is coordinated:

```json
{"version":1,"event":"page_view","path":"/docs/overview/introduction/","timestamp":"2026-10-09T12:00:00.000Z"}
```

```json
{"version":1,"email":"reader@example.com","source":"website","consent":"monthly-newsletter-v1","timestamp":"2026-10-09T12:00:00.000Z"}
```

- Use JSON `fetch`, omit credentials and referrers, and keep storage secrets off
  the frontend. Empty endpoint URLs disable the respective integration.
- Analytics is disabled in development and suppressed by DNT/GPC. Send no query
  strings, fragments, email, cookies, persistent IDs, or browser fingerprint.
  This measures page views, not unique visitors or sessions.
- Analytics failures must never prevent rendering or subscription setup, including
  synchronous fetch errors. Do not add retries, WebSocket fallbacks, alternate
  hosts, or ad-blocker evasion. Delivery cannot be guaranteed.
- Subscribe only on explicit form submission, independently of analytics. Preserve
  the 15-second timeout, pending-submission lock, and clear success/error feedback.
  A successful 2xx means the server recorded the subscription; deduplication is a
  backend responsibility because retries after timeouts can repeat a request.
- Browser JavaScript does not provide a trustworthy client IP. If separately
  authorized, the backend can derive it from the request using trusted proxy
  configuration; do not add IP collection to the frontend payload.
- Keep `connect-src` in the hosting CSP (`netlify.toml`, or the deployed server
  equivalent) aligned with `https://ingest.observertc.org`. A same-origin-only
  policy blocks both analytics and subscriptions before CORS is evaluated.
- Override Doks tabs in `assets/js/tabs.js`; match tab attribute values directly,
  since saved labels can contain spaces or punctuation. Ignore absent saved tabs
  and handle unavailable storage without breaking page initialization.
- JSON POSTs to the ingestion subdomain are cross-origin and need CORS preflight.
  Do not claim real DNS/TLS/CORS/storage or ad-blocker compatibility was verified
  solely because local mocks pass. Consult `docs/ingestion-migration.md` and README
  for contracts, deployment responsibilities, and dated infrastructure observations.

## Useful files and verification

- Homepage: `layouts/index.html`.
- Shared visual overrides: `assets/scss/common/_custom.scss`.
- Docs layout/sidebar: `layouts/partials/docs/page.html` and
  `layouts/partials/sidebar/section-menu.html`.
- Newsletter: `layouts/partials/newsletter.html`.
- Service requests: `assets/js/site-services.js`.
- Theme preference/switch: `assets/js/color-mode.js`.
- Favicon override: `layouts/partials/seo/favicons.html`.
- Updates: `layouts/updates/list.html`, `layouts/updates/single.html`.
- Use Node.js 22 for Netlify builds and Agent Runners. Keep `.nvmrc`,
  `netlify.toml`, the package engine, and the lockfile root engine aligned.
- Run `npm run dev` for the Hugo preview, normally at `http://localhost:1313/`.
  If rendered content remains stale after a change, check/restart the existing
  preview process rather than starting another server on the same port.
- Run `npm run build` after site changes. Run `npm run check` for content/link or
  service changes: it checks local links/fragments and frontend service behavior.
  For instruction-only edits, review the Markdown and referenced paths.
- For visual/layout changes, inspect the affected page at desktop/mobile sizes
  and in the relevant themes. Check active navigation, expanded rows, wrapping,
  and contrast. Report actual verification and any limitations plainly.
- Do not add tests that merely repeat a trivial visual edit. Add meaningful tests
  when behavior changes, especially independent analytics/signup failure handling.
