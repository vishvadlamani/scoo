// scoo.app: the static site plus a small waitlist API backed by D1.
//
// The pages are bundled into the Worker as text rather than uploaded as static assets: the
// asset-upload API authenticates with its own one-time token, which the deploy environment's
// network proxy replaces, so asset uploads fail from there. The pages are small enough that
// serving them from the Worker costs nothing that matters.
import { openStore } from './store.js';
import { placeForZip, coordsForZip } from './zips.js';
import METROS_JSON from './metros.json';
import { AREAS } from './areas.js';
import INDEX from '../public/index.html';
import REQUEST from '../public/request.html';
import PROS from '../public/pros.html';
import TERMS from '../public/terms.html';
import APP_PAGE from '../public/app.html';
import EXCH_START from '../public/exchanges-start.html';
import PRIVACY from '../public/privacy.html';
import FAVICON from '../public/favicon.svg';
import MARK_LIGHT from '../public/mark-light.svg';
import MARK_DARK from '../public/mark-dark.svg';
import APP_ICON from '../public/app-icon.svg';

const PAGES = {
  '/': [INDEX, 'text/html; charset=utf-8'],
  '/index.html': [INDEX, 'text/html; charset=utf-8'],
  '/request': [REQUEST, 'text/html; charset=utf-8'],
  '/request.html': [REQUEST, 'text/html; charset=utf-8'],
  '/pros': [PROS, 'text/html; charset=utf-8'],
  '/pros.html': [PROS, 'text/html; charset=utf-8'],
  '/terms': [TERMS, 'text/html; charset=utf-8'],
  '/app': [APP_PAGE, 'text/html; charset=utf-8'],
  '/exchanges': [EXCH_START, 'text/html; charset=utf-8'],
  '/exchanges/start': [EXCH_START, 'text/html; charset=utf-8'],
  '/privacy': [PRIVACY, 'text/html; charset=utf-8'],
  '/favicon.svg': [FAVICON, 'image/svg+xml'],
  '/mark-light.svg': [MARK_LIGHT, 'image/svg+xml'],
  '/mark-dark.svg': [MARK_DARK, 'image/svg+xml'],
  '/app-icon.svg': [APP_ICON, 'image/svg+xml'],
};
//
// Every number the page shows a visitor comes from here, counted from real rows. Ads will point
// at this page, and a waitlist count that is not real is a misleading claim, so nothing is seeded
// or padded.

const GOAL = 1000; // sign-ups a city needs before Scoo opens there

// Launch areas by 3-digit ZIP prefix. A prefix not listed here still counts: it becomes its own
// area, named after the prefix, so demand outside these metros shows up in the data rather than
// being dropped.
const METROS = METROS_JSON;
const PREFIX = new Map(METROS.flatMap(([name, ps]) => ps.map(p => [p, name])));

// Where a ZIP is, two ways. `place` is the town people recognise ("Plano, TX"), from the ZIP
// table; it is what the page says back to them. `key` and `name` are the launch area the sign-up
// counts toward: a tracked metro (Plano counts toward Dallas), or else its 3-digit ZIP prefix.
function area(zip) {
  const p = zip.slice(0, 3);
  const metro = PREFIX.get(p) || null;
  const place = placeForZip(zip);
  const town = place ? place.replace(/, [A-Z]{2}$/, '') : null;
  return {
    key: metro ? metro.toLowerCase().replace(/\s+/g, '-') : 'zip-' + p,
    name: metro || town || 'your area',            // the launch area, for counts and positions
    place: place || (metro ? metro : null),        // "Plano, TX", said back to them
    town: town || metro || null,                   // "Plano"
    label: metro ? `the ${metro} area` : town ? `the ${town} area` : 'your area',
  };
}

// The homepage badge names the visitor's own area, from Cloudflare's IP location: a metro we track
// by postal code, else the city Cloudflare reports. It is approximate (an IP, not a GPS fix), so it
// says "near you" when there is nothing usable, and never asks for location permission.
function visitorArea(cf) {
  if (!cf || cf.country !== 'US') return null;
  const zip = /^\d{5}/.test(cf.postalCode || '') ? cf.postalCode.slice(0, 5) : null;
  if (zip) { const a = area(zip); if (a.town) return a.town; }
  return cf.city || null;
}
const escapeHtml = s => s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function homepage(request) {
  const place = visitorArea(request.cf);
  const res = new Response(INDEX, { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'private, no-cache', vary: 'cf-ipcity' } });
  if (!place) return res;
  return new HTMLRewriter()
    .on('p.badge', { element(el) { el.setInnerContent(`<i></i>Coming soon to ${escapeHtml(place)}`, { html: true }); } })
    .transform(res);
}

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });

// Invite codes: 6 characters from an alphabet without look-alikes (no 0/O, 1/l/I).
const ALPHABET = 'abcdefghjkmnpqrstuvwxyz23456789';
function newCode() {
  const b = crypto.getRandomValues(new Uint8Array(6));
  return Array.from(b, x => ALPHABET[x % ALPHABET.length]).join('');
}

function newToken() {
  const b = crypto.getRandomValues(new Uint8Array(24));
  return Array.from(b, x => x.toString(16).padStart(2, '0')).join('');
}
const cookie = (req, name) => (req.headers.get('cookie') || '').split(/;\s*/).map(c => c.split('=')).find(([k]) => k === name)?.[1] || null;

// Everything their map shows, for the signed-in person only. Counts are by area, never points:
// nothing here places another person anywhere finer than a launch area.
async function me(request, env) {
  const token = cookie(request, 'scoo_t');
  if (!token || !/^[0-9a-f]{48}$/.test(token)) return json({ error: 'not signed in' }, 401);
  const db = openStore(env);
  const r = await db.first('SELECT id, zip, city_key, code, category FROM requests WHERE token = ?', [token]);
  if (!r) return json({ error: 'not signed in' }, 401);
  const a = area(r.zip);
  const shape = AREAS[r.city_key];
  const position = (await db.first('SELECT COUNT(*) AS n FROM requests WHERE city_key = ? AND id <= ?', [r.city_key, r.id])).n;
  const waiting = await cityStats(db, r.city_key);
  const invited = (await db.first('SELECT (SELECT COUNT(*) FROM requests WHERE referred_by = ?) + (SELECT COUNT(*) FROM pros WHERE referred_by = ?) AS n', [r.code, r.code])).n;
  const pros = (await db.all('SELECT trade, COUNT(*) AS n FROM pros WHERE city_key = ? GROUP BY trade ORDER BY n DESC', [r.city_key]));
  // Nearby launch areas, by distance between centres, with their real counts.
  const c = shape ? shape.c : null;
  const near = c ? Object.entries(AREAS).filter(([k]) => k !== r.city_key)
    .map(([k, v]) => [k, v, Math.hypot((v.c[0] - c[0]) * Math.cos(c[1] * Math.PI / 180), v.c[1] - c[1])])
    .filter(x => x[2] < 2.2).sort((x, y) => x[2] - y[2]).slice(0, 8) : [];
  const counts = near.length ? Object.fromEntries((await db.all(
    `SELECT city_key, COUNT(*) AS n FROM requests WHERE city_key IN (${near.map(() => '?').join(',')}) GROUP BY city_key`, near.map(x => x[0]))).map(x => [x.city_key, x.n])) : {};
  const nearby = near.map(([k, v]) => ({ key: k, name: v.n, center: v.c, outline: v.h, waiting: counts[k] || 0 }));
  return json({
    zip: r.zip, place: a.place, town: a.town, areaLabel: a.label, area: a.name,
    pin: coordsForZip(r.zip), outline: shape ? shape.h : null, center: c,
    position, waiting, goal: GOAL, code: r.code, invited, pros, nearby,
  });
}

async function cityStats(db, key) {
  return (await db.first('SELECT COUNT(*) AS n FROM requests WHERE city_key = ?', [key])).n;
}

// Turnstile: on whenever TURNSTILE_SECRET is set. Until then the form works without it, so the
// site never breaks while the widget is being set up.
async function humanCheck(env, token, ip) {
  if (!env.TURNSTILE_SECRET) return true;
  if (!token) return false;
  const form = new FormData();
  form.append('secret', env.TURNSTILE_SECRET);
  form.append('response', token);
  if (ip) form.append('remoteip', ip);
  const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
  const out = await r.json().catch(() => ({}));
  return out.success === true;
}

async function createRequest(request, env) {
  let b;
  try { b = await request.json(); } catch { return json({ error: 'That did not look like a request' }, 400); }

  const need = String(b.need || '').trim().slice(0, 500);
  const category = String(b.category || 'pro').slice(0, 32);
  const answer = b.answer == null ? null : String(b.answer).slice(0, 100);
  const zip = String(b.zip || '').trim();
  // One field on the page: a mobile number or an email, whichever they prefer to be notified on.
  const contact = String(b.contact ?? b.phone ?? '').trim().slice(0, 160);
  let phone = null, email = null;
  if (contact.includes('@')) {
    email = contact.toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return json({ error: 'That email does not look right' }, 400);
  } else {
    phone = contact.replace(/\D/g, '');
    if (phone.length === 10) phone = '1' + phone;
    if (!/^1\d{10}$/.test(phone)) return json({ error: 'Add a mobile number or an email' }, 400);
  }
  const consentText = String(b.consentText || '').trim().slice(0, 600);
  const ref = b.ref ? String(b.ref).toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 12) : null;

  if (!need) return json({ error: 'Tell us what you need' }, 400);
  if (!/^\d{5}$/.test(zip)) return json({ error: 'That ZIP code does not look right' }, 400);
  // No consent, no contact: we only notify people who have agreed to it.
  if (b.consent !== true || consentText.length < 40) return json({ error: 'Please tick the box so we can notify you' }, 400);

  if (!(await humanCheck(env, b.turnstile, request.headers.get('cf-connecting-ip')))) {
    return json({ error: 'Please complete the check that you are not a robot' }, 400);
  }

  const { key, name, place, town, label } = area(zip);
  const db = openStore(env);

  // Same number or email, same area: keep their original place and code.
  const existing = phone
    ? await db.first('SELECT id, code, token FROM requests WHERE phone = ? AND city_key = ?', [phone, key])
    : await db.first('SELECT id, code, token FROM requests WHERE email = ? AND city_key = ?', [email, key]);
  let id, code;
  if (existing) {
    ({ id, code } = existing);
  } else {
    const referredBy = ref && (await db.first('SELECT 1 AS ok FROM requests WHERE code = ?', [ref])) ? ref : null;
    for (let attempt = 0; attempt < 5 && !id; attempt++) {
      code = newCode();
      try {
        const r = await db.run(
          `INSERT INTO requests (need, category, answer, zip, city_key, city_name, phone, email, consent_text, consent_at, code, referred_by, user_agent)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, strftime('%Y-%m-%dT%H:%M:%fZ','now'), ?, ?, ?)`,
          [need, category, answer, zip, key, name, phone, email, consentText, code, referredBy, (request.headers.get('user-agent') || '').slice(0, 300)]);
        id = r.lastRowId;
      } catch (e) {
        if (!/UNIQUE/i.test(String(e))) throw e; // a code collision: try another
      }
    }
    if (!id) return json({ error: 'Could not save your request' }, 500);
  }

  const position = (await db.first('SELECT COUNT(*) AS n FROM requests WHERE city_key = ? AND id <= ?', [key, id])).n;
  const waiting = await cityStats(db, key);
  // The private session: a secret token in an HttpOnly cookie opens their map (/app). It is separate
  // from `code`, which is public (it is in every invite link they share).
  let token = existing && existing.token;
  if (!token) {
    token = newToken();
    await db.run('UPDATE requests SET token = ? WHERE id = ?', [token, id]);
  }
  const res = json({ city: name, place, town, areaLabel: label, position, waiting, goal: GOAL, code, via: phone ? 'text' : 'email' });
  res.headers.append('set-cookie', `scoo_t=${token}; Path=/; Max-Age=31536000; HttpOnly; Secure; SameSite=Lax`);
  return res;
}


const TRADES = new Set(['Plumber', 'Electrician', 'HVAC', 'Roofer', 'Handyman', 'Cleaner', 'Mover', 'Locksmith', 'Pest control',
  'Landscaper', 'Mechanic', 'Lawyer', 'Insurance agent', 'Real estate agent', 'Doctor or clinic', 'Tutor', 'Other']);

async function createPro(request, env) {
  let b;
  try { b = await request.json(); } catch { return json({ error: 'That did not look like a sign-up' }, 400); }
  const business = String(b.business || '').trim().replace(/\s+/g, ' ').slice(0, 120);
  const trade = String(b.trade || '');
  const zip = String(b.zip || '').trim();
  let phone = String(b.phone || '').replace(/\D/g, '');
  if (phone.length === 10) phone = '1' + phone;
  const email = b.email ? String(b.email).trim().slice(0, 160) : null;
  const consentText = String(b.consentText || '').trim().slice(0, 600);
  const ref = b.ref ? String(b.ref).toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 12) : null;

  if (business.length < 2) return json({ error: 'Add your business name' }, 400);
  if (!TRADES.has(trade)) return json({ error: 'Pick your trade' }, 400);
  if (!/^\d{5}$/.test(zip)) return json({ error: 'That ZIP code does not look right' }, 400);
  if (!/^1\d{10}$/.test(phone)) return json({ error: 'That phone number does not look right' }, 400);
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ error: 'That email does not look right' }, 400);
  if (b.consent !== true || consentText.length < 40) return json({ error: 'Please tick the box so we can reach you' }, 400);
  if (!(await humanCheck(env, b.turnstile, request.headers.get('cf-connecting-ip')))) {
    return json({ error: 'Please complete the check that you are not a robot' }, 400);
  }

  const a = area(zip);
  const { key, name } = a;
  const db = openStore(env);
  const existing = await db.first('SELECT id, code FROM pros WHERE phone = ? AND trade = ? AND city_key = ?', [phone, trade, key]);
  let id, code;
  if (existing) {
    ({ id, code } = existing);
  } else {
    // A pro can be invited by a customer (requests.code) or by another pro (pros.code).
    const known = ref && ((await db.first('SELECT 1 AS ok FROM requests WHERE code = ?', [ref])) || (await db.first('SELECT 1 AS ok FROM pros WHERE code = ?', [ref])));
    for (let attempt = 0; attempt < 5 && !id; attempt++) {
      code = newCode();
      try {
        const r = await db.run(
          `INSERT INTO pros (business, trade, zip, city_key, city_name, phone, email, consent_text, consent_at, code, referred_by, user_agent)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, strftime('%Y-%m-%dT%H:%M:%fZ','now'), ?, ?, ?)`,
          [business, trade, zip, key, name, phone, email, consentText, code, known ? ref : null, (request.headers.get('user-agent') || '').slice(0, 300)]);
        id = r.lastRowId;
      } catch (e) {
        if (!/UNIQUE/i.test(String(e))) throw e;
      }
    }
    if (!id) return json({ error: 'Could not save your sign-up' }, 500);
  }
  const position = (await db.first('SELECT COUNT(*) AS n FROM pros WHERE city_key = ? AND trade = ? AND id <= ?', [key, trade, id])).n;
  return json({ city: name, place: a.place, town: a.town, areaLabel: a.label, trade, position, code });
}

// Exchange names: the slug in scoo.app/x/<slug>. Reserved words keep paths and the brand safe.
const RESERVED = new Set(['app', 'api', 'pros', 'pro', 'request', 'terms', 'privacy', 'exchanges', 'exchange', 'x', 'r', 'admin', 'scoo',
  'www', 'help', 'support', 'login', 'signup', 'settings', 'about', 'blog', 'jobs', 'careers', 'press', 'legal', 'security', 'status']);
const SLUG = /^[a-z0-9](?:[a-z0-9-]{1,30}[a-z0-9])$/;
async function nameCheck(db, s) {
  if (!SLUG.test(s)) return { available: false, reason: 'Use 3 to 32 lowercase letters, numbers and dashes.' };
  if (RESERVED.has(s)) return { available: false, reason: 'That name is reserved. Try another.' };
  const taken = await db.first('SELECT 1 AS t FROM operators WHERE slug = ?', [s]);
  return taken ? { available: false, reason: 'That name is taken. Try another.' } : { available: true };
}

async function createOperator(request, env) {
  let b;
  try { b = await request.json(); } catch { return json({ error: 'That did not look like an application' }, 400); }
  const slug = String(b.slug || '').trim().toLowerCase();
  const name = String(b.name || '').trim().replace(/\s+/g, ' ').slice(0, 80);
  const org = String(b.org || '').trim().replace(/\s+/g, ' ').slice(0, 120);
  const trades = (Array.isArray(b.trades) ? b.trades : []).map(t => String(t).slice(0, 40)).slice(0, 20).join(',');
  const zip = String(b.zip || '').trim();
  const size = String(b.size || '').slice(0, 30), volume = String(b.volume || '').slice(0, 30);
  const contact = String(b.contact || '').trim().slice(0, 160);
  let phone = null, email = null;
  if (contact.includes('@')) {
    email = contact.toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return json({ error: 'That email does not look right' }, 400);
  } else {
    phone = contact.replace(/\D/g, ''); if (phone.length === 10) phone = '1' + phone;
    if (!/^1\d{10}$/.test(phone)) return json({ error: 'Add a mobile number or an email' }, 400);
  }
  const consentText = String(b.consentText || '').trim().slice(0, 600);
  if (name.length < 2) return json({ error: 'Add your name' }, 400);
  if (org.length < 2) return json({ error: 'Add your company or network' }, 400);
  if (!/^\d{5}$/.test(zip)) return json({ error: 'That ZIP code does not look right' }, 400);
  if (b.consent !== true || consentText.length < 40) return json({ error: 'Please tick the box so we can reach you' }, 400);
  if (!(await humanCheck(env, b.turnstile, request.headers.get('cf-connecting-ip')))) {
    return json({ error: 'Please complete the check that you are not a robot' }, 400);
  }
  const db = openStore(env);
  const n = await nameCheck(db, slug);
  if (!n.available) return json({ error: n.reason.replace(/\.$/, '') }, 409);
  const a = area(zip);
  const ref = b.ref ? String(b.ref).toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 12) : null;
  try {
    await db.run(
      `INSERT INTO operators (slug, name, org, trades, zip, city_key, city_name, size, volume, phone, email, consent_text, consent_at, referred_by, user_agent)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, strftime('%Y-%m-%dT%H:%M:%fZ','now'), ?, ?)`,
      [slug, name, org, trades, zip, a.key, a.name, size, volume, phone, email, consentText, ref, (request.headers.get('user-agent') || '').slice(0, 300)]);
  } catch (e) {
    if (/UNIQUE/i.test(String(e))) return json({ error: 'That name was just taken. Try another' }, 409);
    throw e;
  }
  return json({ slug, place: a.place, areaLabel: a.label });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // One canonical address: www.scoo.app sends people to scoo.app, keeping the path and query.
    if (url.hostname === 'www.scoo.app') {
      url.hostname = 'scoo.app';
      return Response.redirect(url.toString(), 301);
    }
    if (path === '/api/config') return json({ turnstileSiteKey: env.TURNSTILE_SITE_KEY || null });

    if (path === '/api/requests' && request.method === 'POST') return createRequest(request, env);
    if (path === '/api/pros' && request.method === 'POST') return createPro(request, env);
    if (path === '/api/me' && request.method === 'GET') return me(request, env);
    if (path === '/api/operators' && request.method === 'POST') return createOperator(request, env);
    if (path === '/api/exchange-name' && request.method === 'GET') return json(await nameCheck(openStore(env), String(url.searchParams.get('s') || '').toLowerCase()));
    if (path === '/api/city' && request.method === 'GET') {
      const zip = url.searchParams.get('zip') || '';
      if (!/^\d{5}$/.test(zip)) return json({ error: 'zip' }, 400);
      const { key, name, place, town, label } = area(zip);
      return json({ city: name, place, town, areaLabel: label, waiting: await cityStats(openStore(env), key), goal: GOAL });
    }

    // Invite links land with the code, which the page remembers: customer invites on the homepage,
    // pro invites on the pros page.
    const invite = path.match(/^\/(r|pro)\/([a-z0-9]{4,12})\/?$/i);
    if (invite) return Response.redirect(`${url.origin}${invite[1] === 'pro' ? '/pros' : '/'}?ref=${invite[2].toLowerCase()}`, 302);

    if ((path === '/' || path === '/index.html') && request.method === 'GET') return homepage(request);
    const page = PAGES[path];
    if (page && request.method === 'GET') {
      return new Response(page[0], { headers: { 'content-type': page[1], 'cache-control': 'public, max-age=300' } });
    }
    return new Response('Not found', { status: 404, headers: { 'content-type': 'text/plain' } });
  },
};
