# scoo.app

The pre-launch site: homepage, the request flow, and a waitlist API on Cloudflare D1.

- `public/` — `index.html` (homepage) and `request.html` (the step-by-step request flow), plus logo SVGs.
  These are generated; the generators are in `build/` (`gen.py` → street, `post.py` → pros and logo,
  `prelaunch.py` → fonts, `flowpage.py` → request page and homepage hand-off).
- `src/worker.js` — serves the pages and the API:
  - `POST /api/requests` saves a request (need, category, answer, ZIP, phone, the exact consent
    wording shown) and returns `{city, position, waiting, goal, code}`. A repeat phone number in the
    same area keeps its original place.
  - `GET /api/city?zip=` returns the real count for that area.
  - `/r/CODE` and `/pro/CODE` redirect to the homepage with the referral code, which the page
    remembers and sends with the request.
- `src/store.js` — the storage layer: `first(sql, params)` and `run(sql, params)`, with a D1
  implementation and a Turso implementation (Turso's HTTP `/v2/pipeline` API, plain `fetch`, no
  client library). Both are SQLite, so `schema.sql` and every query run unchanged on either.
- `schema.sql` — the `requests` table.

## Database: D1 now, Turso for production

The Worker uses Turso whenever `TURSO_URL` is set, otherwise the D1 binding `DB`. To switch:

```bash
turso db create scoo-waitlist && turso db shell scoo-waitlist < schema.sql
# in wrangler.jsonc: "vars": { "TURSO_URL": "libsql://scoo-waitlist-<org>.turso.io" }
npx wrangler secret put TURSO_AUTH_TOKEN      # a token from `turso db tokens create scoo-waitlist`
npx wrangler deploy
```

Copy any existing D1 rows across before switching if they should be kept.

## Bot check (Cloudflare Turnstile)

On whenever the Worker has `TURNSTILE_SECRET` (secret) and `TURNSTILE_SITE_KEY` (var); without
them the form works unprotected, so the site never breaks mid-setup. The page reads the site key
from `/api/config` and the Worker verifies the token on every `POST /api/requests`.

## www

`www.scoo.app` is a second custom domain on the same Worker; it 301s to `scoo.app`, keeping the
path and query.

The pages are bundled into the Worker as text (not static assets) because asset uploads fail
through the cloud session's network proxy. Deploy:

```bash
CLOUDFLARE_API_TOKEN=... npx wrangler@4.45.0 deploy
```

Every number on the page is counted from real rows. Nothing is seeded.
