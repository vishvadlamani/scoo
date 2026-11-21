# scoo.app

Scoo's pre-launch site: the homepage, the request flow, the map home, the pros page, the exchange
application, terms and privacy, and the waitlist API behind them. SvelteKit and TypeScript on a
Cloudflare Worker, with Cloudflare D1 as the database today and Turso ready to switch to.

## Running it

```bash
npm install
npx wrangler d1 execute scoo-waitlist --local --file schema.sql   # once: a local database
npm run dev                                                       # http://localhost:5173
npm run check                                                     # types, 0 errors and 0 warnings
npm run deploy                                                    # build, then wrangler deploy
```

## Layout

| path | what |
| --- | --- |
| `src/routes/` | one folder per page; `api/*/+server.ts` are the endpoints; `r/[code]` and `pro/[code]` are invite links |
| `src/lib/server/waitlist.ts` | the API: sign-ups, the signed-in map data, exchange names, Turnstile |
| `src/lib/server/store.ts` | the database behind three calls (`first`, `all`, `run`), on D1 or Turso |
| `src/lib/server/geo/` | ZIP → town and centroid, and the launch areas (generated, see below) |
| `src/lib/art/` | line-art SVGs (the street, the winged pros, illustrations), as files |
| `src/lib/brand/` | the logo |
| `src/app.css` | colour tokens (light and dark) and the base styles every page shares |
| `static/` | favicon and logo files at fixed URLs |
| `schema.sql` | the tables: `requests`, `pros`, `operators`, `exchange_members` (a fresh database runs it whole) |
| `migrations/` | changes to apply to an existing database, in order |
| `src/lib/profiles/`, `src/lib/server/profiles.ts` | public pro profiles (`/p/<slug>`) and exchange pages (`/x/<slug>`) |
| `src/lib/server/examples.ts` | the example exchange and pros: invented, labelled, never indexed |
| `brand/` | logo history and exports, not shipped |
| `tools/` | build scripts, TypeScript, run by Node directly |

## Deploying

`npm run deploy` builds, then `tools/embed-assets.ts` bakes the built client files into the Worker
and drops the static-assets section from the deploy config. That is deliberate: Cloudflare's
static-asset upload authenticates with a short-lived token of its own, which the proxy this project
deploys through overwrites, so the upload fails. The client files are small, so serving them from
the Worker costs nothing that matters, and the adapter's Worker is otherwise unchanged. If you
deploy from somewhere without that proxy, drop the embed step from `build` and the normal static
assets work as SvelteKit intends.

The same step writes a small front door (`entry.js`) ahead of SvelteKit that sends
`www.scoo.app` to `scoo.app`: prerendered pages are answered before SvelteKit's hooks run, so a
redirect that must cover every path cannot live in `hooks.server.ts`.

`wrangler.jsonc` holds every binding and route, so a plain deploy never loses configuration that
only lived in the dashboard. Secrets are set with `wrangler secret put` and never committed.

## Database: D1 now, Turso for production

The Worker uses Turso whenever `TURSO_URL` is set, otherwise the D1 binding `DB`. Both are SQLite,
so `schema.sql` and every query run unchanged on either. To switch:

```bash
turso db create scoo-waitlist && turso db shell scoo-waitlist < schema.sql
# wrangler.jsonc: "vars": { "TURSO_URL": "libsql://scoo-waitlist-<org>.turso.io" }
npx wrangler secret put TURSO_AUTH_TOKEN
npm run deploy
```

## Bot checks

Turnstile is built in and off until both `TURNSTILE_SITE_KEY` (a var) and `TURNSTILE_SECRET` (a
secret) are set. The forms read the site key from `/api/config`.

## ZIP data

`src/lib/server/geo/zips.json` and `areas.json` come from GeoNames' US postal codes (CC BY 4.0,
credited in the terms). Launch metros are listed in `metros.json`; every other 3-digit ZIP prefix
is an area of its own. To rebuild after changing the metros:

```bash
curl -LO https://download.geonames.org/export/zip/US.zip && unzip US.zip US.txt
npm run geo -- US.txt
```

## Public pages and search

A pro profile (`/p/<slug>`) or exchange page (`/x/<slug>`) is public only once `published_at` is
set; before that it answers 404. A pro gets one only if they ticked the profile box on the sign-up
form (`profile_ok`) and Scoo has checked the details with them. To publish:

```sql
UPDATE pros SET published_at = strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE slug = '…';
UPDATE operators SET published_at = strftime('%Y-%m-%dT%H:%M:%fZ','now'), tagline = '…', rules = '…' WHERE slug = '…';
INSERT INTO exchange_members (operator_id, pro_id) VALUES (…, …);
```

Published pages are listed in `/sitemap.xml` and carry schema.org data. `/x/example` and
`/p/example-*` are the examples: invented names and numbers, labelled on screen, `noindex`, left out
of the sitemap, and their slugs are reserved. Track-record numbers on real profiles stay empty until
they can be counted from real calls.

## Rules the pages keep

- Every number shown to a visitor is counted from real rows. Nothing is seeded or padded.
- The map shows counts by area, never anyone's location.
- The private session cookie (`scoo_t`) and the public invite code are separate.
- The consent wording a person saw is stored, verbatim, with their sign-up.
