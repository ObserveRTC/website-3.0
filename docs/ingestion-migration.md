# Ingestion hostname migration

Verified on October 9, 2026. This repository owns a static Hugo/Doks frontend only.
There are no backend, DNS, TLS, reverse proxy, ingress, Kubernetes, or server CORS
configuration files here. Those changes must be applied in the server's repository
or infrastructure control plane.

## Implementation and contracts

Configure both URLs centrally in `config/_default/params.toml`:

- `POST https://ingest.observertc.org/analytics`
- `POST https://ingest.observertc.org/subscribe`

The existing paths and version-1 envelope are preserved (see README). Analytics
now has optional browser/device/language fields and a random `visitorId`; update
backend validation to accept these before deploying. Subscription is unchanged. Do not
switch to `/v1/events` or `/v1/subscriptions` without coordinating backend support.
The existing routes already separate analytics from explicit signups.

`assets/js/site-services.js` is bundled locally and uses standard JSON `fetch`
requests. Analytics sends one page view per page load with `keepalive: true`, no
retry and no fallback transport. No query strings, referrers, email,
cookies, or browser credentials are included. A random localStorage visitor ID
and coarse browser context are included when available. DNT and GPC suppress analytics;
development analytics is disabled by default. Existing behavior does not implement
an explicit consent UI. If a deployment requires opt-in, disable the configured
analytics URL until a consent gate is implemented; do not treat absence of DNT/GPC
as explicit consent.

Subscriptions remain available regardless of DNT/GPC, disabled analytics, or an
analytics network error, including a synchronous fetch error. They use a separate
request, a 15-second timeout, meaningful failure feedback, and a pending-submission
lock. No automatic retry is introduced. The backend must deduplicate email addresses:
a timeout can happen after persistence, and a user may then retry manually.

On `https://observertc.org` the ingestion subdomain is same-site but cross-origin.
Localhost and deployments on another domain are cross-site. JSON Content-Type
requires CORS preflight even when both hosts share a registrable domain.

## Compatibility assessment — not browser test results

There is no third-party tracking library, pixel, fingerprint, renamed tracking
script, alternate hostname fallback, or blocker bypass. The transparent `/analytics`
route and the host or bundled script can still match block rules. Sharing the
frontend script does not make optional analytics a dependency of subscription
logic; if a blocker blocks the entire JavaScript bundle, however, signup cannot run.
The native form action is not a JSON fallback: the current endpoint contract
requires JavaScript, as the form's noscript message explains.

| Protection | Assessment | Actual test status |
|---|---|---|
| uBlock Origin / EasyPrivacy | URL, hostname, request-type and origin-dependent rules may block analytics or the bundle. Same-site does not guarantee allowance. | Not tested with extension/filter engine. |
| Brave Shields | Uses filter lists and additional protections; standard/aggressive modes can behave differently. | Not tested in Brave. |
| Firefox ETP | Classified tracking content may be blocked; no dependence on third-party cookies or storage. | Not tested in Firefox Standard/Strict. |
| Safari ITP / content blockers | Cookie/storage restrictions do not supply a delivery guarantee; content blockers may block requests separately. | Not tested in Safari. |
| AdGuard | Network rules can match hosts, paths, request types and origins. | Not tested with AdGuard. |
| Chrome with blocking extensions | Results depend on the installed extension, filter list and settings. | Not tested in Chrome with extensions. |

These are inferences from the documented protection mechanisms, not evidence that
this hostname is allowed. No naming convention guarantees delivery. Respect
intentional blocking; do not ask users to disable privacy protections to collect
analytics. A legitimate subscription failure should remain visible to the user.

Sources: [uBlock syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax),
[EasyPrivacy](https://easylist.to/), [Brave Shields](https://brave.com/shields/),
[Firefox tracking protection](https://developer.mozilla.org/en-US/docs/Web/Privacy/Guides/Firefox_tracking_protection),
[WebKit tracking prevention](https://webkit.org/tracking-prevention/),
[AdGuard filter rules](https://adguard.com/kb/general/ad-filtering/create-own-filters/).

## Actual infrastructure checks

Read-only DNS lookups on October 9, 2026 failed for both the new ingestion hostname
and the previous hostname with a name-resolution error from this machine's resolver.
That prevents this environment from checking certificates, OPTIONS responses or
live ingestion. This is not proof that public DNS is absent everywhere. No live
subscriber records were created, and no production analytics were posted.

Local automated tests verify exact configured URLs, unchanged payload fields,
privacy suppression, subscription independence, successful/failed requests and
pending-submission protection. The Hugo build/link checks verify rendered pages.
These mocks do not prove real CORS, delivery or object storage persistence.

## Manual deployment steps

1. Create DNS A/AAAA records pointing the new host at your existing server, or a
   CNAME to its existing stable ingress hostname. Do not add a new storage/database.
2. Add the host to your reverse proxy/ingress and provision a valid TLS certificate.
   Route the existing two POST paths to the current acceptor implementation.
3. Allow intended website origins explicitly. Preflight responses must allow
   `POST, OPTIONS` and `Content-Type`; emit `Access-Control-Allow-Origin` on POST
   success and errors. Use `Vary: Origin` when responding from an origin allowlist.
   Credentials are omitted. Add localhost only where development testing is intended.
4. Keep the prior hostname serving the same routes temporarily if old site builds
   are deployed. Serve requests directly there; avoid depending on cross-origin
   POST redirects. Retire it after cached clients/builds have expired.
5. Rebuild and deploy Hugo after the new service is ready. If the host is not ready,
   leave the integrations disabled rather than deploying nonfunctional signup.
6. Check DNS from public resolvers, TLS certificate coverage, both JSON preflights,
   and POST responses from the actual deployed website origin. Verify storage
   persistence in a staging environment using controlled test records.
7. Test standard and strict privacy settings in the browsers above, recording
   versions/filter-list versions and results. Verify signup with analytics blocked,
   GPC/DNT enabled, and network failures. Do not change endpoints to evade a block.
