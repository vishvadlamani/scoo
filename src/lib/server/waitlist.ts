// The pre-launch API: customers asking to be told when Scoo opens near them, pros claiming their
// receptionist, and exchange operators reserving a name.
//
// Every number a page shows a visitor comes from here, counted from real rows. Ads will point at
// these pages, and a waitlist count that is not real is a misleading claim, so nothing is seeded
// or padded.
import { json } from '@sveltejs/kit';
import { AREAS, area, coordsForZip } from './geo/geo.ts';
import { openStore, type Store } from './store.ts';
import { TRADES } from '#lib/trades.ts';
import { freeProSlug, slugify } from './profiles.ts';
import { isExampleSlug } from './examples.ts';

/** Sign-ups a city needs before Scoo opens there. */
export const GOAL = 1000;

type Body = Record<string, unknown>;
const str = (v: unknown) => (v == null ? '' : String(v));
const noStore = { 'cache-control': 'no-store' };
const fail = (error: string, status = 400) => json({ error }, { status, headers: noStore });
const ok = (body: unknown, headers: HeadersInit = {}) => json(body, { headers: { ...noStore, ...headers } });

async function body(request: Request): Promise<Body | null> {
	try {
		const b: unknown = await request.json();
		return b && typeof b === 'object' ? (b as Body) : null;
	} catch {
		return null;
	}
}

// Invite codes: 6 characters from an alphabet without look-alikes (no 0/O, 1/l/I).
const ALPHABET = 'abcdefghjkmnpqrstuvwxyz23456789';
const newCode = () => Array.from(crypto.getRandomValues(new Uint8Array(6)), (x) => ALPHABET[x % ALPHABET.length]).join('');
const newToken = () => Array.from(crypto.getRandomValues(new Uint8Array(24)), (x) => x.toString(16).padStart(2, '0')).join('');
const cleanRef = (v: unknown) => (v ? str(v).toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 12) : null);
const userAgent = (r: Request) => (r.headers.get('user-agent') ?? '').slice(0, 300);
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

/** A mobile number (1 + 10 digits) or an email, from one field. */
function contactOf(raw: string): { phone: string | null; email: string | null } | string {
	if (raw.includes('@')) {
		const email = raw.toLowerCase();
		return EMAIL.test(email) ? { phone: null, email } : 'That email does not look right';
	}
	let phone = raw.replace(/\D/g, '');
	if (phone.length === 10) phone = '1' + phone;
	return /^1\d{10}$/.test(phone) ? { phone, email: null } : 'Add a mobile number or an email';
}

// Turnstile: on whenever TURNSTILE_SECRET is set. Until then the forms work without it, so the site
// never breaks while the widget is being set up.
async function humanCheck(env: Env, token: unknown, ip: string | null): Promise<boolean> {
	if (!env.TURNSTILE_SECRET) return true;
	if (!token) return false;
	const form = new FormData();
	form.append('secret', env.TURNSTILE_SECRET);
	form.append('response', str(token));
	if (ip) form.append('remoteip', ip);
	const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
	const out = (await r.json().catch(() => ({}))) as { success?: boolean };
	return out.success === true;
}
const notHuman = () => fail('Please complete the check that you are not a robot');

const count = async (db: Store, sql: string, params: (string | number)[]) =>
	(await db.first<{ n: number }>(sql, params))?.n ?? 0;
const waitingIn = (db: Store, key: string) => count(db, 'SELECT COUNT(*) AS n FROM requests WHERE city_key = ?', [key]);

/** Inserts with a fresh invite code, retrying on the rare code collision. */
async function insertWithCode(db: Store, sql: string, params: (code: string) => (string | number | null)[]) {
	for (let attempt = 0; attempt < 5; attempt++) {
		const code = newCode();
		try {
			const r = await db.run(sql, params(code));
			if (r.lastRowId != null) return { id: r.lastRowId, code };
		} catch (e) {
			if (!/UNIQUE/i.test(String(e))) throw e;
		}
	}
	return null;
}

export const config = (env: Env) => ok({ turnstileSiteKey: env.TURNSTILE_SITE_KEY ?? null });

export async function city(env: Env, zip: string) {
	if (!/^\d{5}$/.test(zip)) return fail('zip');
	const { key, name, place, town, label } = area(zip);
	return ok({ city: name, place, town, areaLabel: label, waiting: await waitingIn(openStore(env), key), goal: GOAL });
}

export async function createRequest(request: Request, env: Env) {
	const b = await body(request);
	if (!b) return fail('That did not look like a request');

	const need = str(b.need).trim().slice(0, 500);
	const category = str(b.category || 'pro').slice(0, 32);
	const answer = b.answer == null ? null : str(b.answer).slice(0, 100);
	const zip = str(b.zip).trim();
	// One field on the page: a mobile number or an email, whichever they prefer to be told on.
	const contact = contactOf(str(b.contact ?? b.phone).trim().slice(0, 160));
	const consentText = str(b.consentText).trim().slice(0, 600);
	const ref = cleanRef(b.ref);

	if (typeof contact === 'string') return fail(contact);
	if (!need) return fail('Tell us what you need');
	if (!/^\d{5}$/.test(zip)) return fail('That ZIP code does not look right');
	// No consent, no contact: we only notify people who have agreed to it.
	if (b.consent !== true || consentText.length < 40) return fail('Please tick the box so we can notify you');
	if (!(await humanCheck(env, b.turnstile, request.headers.get('cf-connecting-ip')))) return notHuman();

	const { key, name, place, town, label } = area(zip);
	const { phone, email } = contact;
	const db = openStore(env);

	// Same number or email, same area: they keep their original place and code.
	const existing = await db.first<{ id: number; code: string; token: string | null }>(
		`SELECT id, code, token FROM requests WHERE ${phone ? 'phone' : 'email'} = ? AND city_key = ?`,
		[phone ?? email, key]
	);
	let saved = existing && { id: existing.id, code: existing.code };
	if (!saved) {
		const referredBy = ref && (await db.first('SELECT 1 AS ok FROM requests WHERE code = ?', [ref])) ? ref : null;
		saved = await insertWithCode(
			db,
			`INSERT INTO requests (need, category, answer, zip, city_key, city_name, phone, email, consent_text, consent_at, code, referred_by, user_agent)
			 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, strftime('%Y-%m-%dT%H:%M:%fZ','now'), ?, ?, ?)`,
			(code) => [need, category, answer, zip, key, name, phone, email, consentText, code, referredBy, userAgent(request)]
		);
		if (!saved) return fail('Could not save your request', 500);
	}

	const position = await count(db, 'SELECT COUNT(*) AS n FROM requests WHERE city_key = ? AND id <= ?', [key, saved.id]);
	const waiting = await waitingIn(db, key);
	// The private session: a secret token in an HttpOnly cookie opens their map (/app). It is
	// separate from `code`, which is public: it is in every invite link they share.
	let token = existing?.token;
	if (!token) {
		token = newToken();
		await db.run('UPDATE requests SET token = ? WHERE id = ?', [token, saved.id]);
	}
	return ok(
		{ city: name, place, town, areaLabel: label, position, waiting, goal: GOAL, code: saved.code, via: phone ? 'text' : 'email' },
		{ 'set-cookie': `scoo_t=${token}; Path=/; Max-Age=31536000; HttpOnly; Secure; SameSite=Lax` }
	);
}

// Everything their map shows, for the signed-in person only. Counts are by area, never points:
// nothing here places another person anywhere finer than a launch area.
export async function me(token: string | undefined, env: Env) {
	if (!token || !/^[0-9a-f]{48}$/.test(token)) return fail('not signed in', 401);
	const db = openStore(env);
	const r = await db.first<{ id: number; zip: string; city_key: string; code: string }>(
		'SELECT id, zip, city_key, code FROM requests WHERE token = ?',
		[token]
	);
	if (!r) return fail('not signed in', 401);
	const a = area(r.zip);
	const shape = AREAS[r.city_key];
	const position = await count(db, 'SELECT COUNT(*) AS n FROM requests WHERE city_key = ? AND id <= ?', [r.city_key, r.id]);
	const waiting = await waitingIn(db, r.city_key);
	const invited = await count(
		db,
		'SELECT (SELECT COUNT(*) FROM requests WHERE referred_by = ?) + (SELECT COUNT(*) FROM pros WHERE referred_by = ?) AS n',
		[r.code, r.code]
	);
	const pros = await db.all('SELECT trade, COUNT(*) AS n FROM pros WHERE city_key = ? GROUP BY trade ORDER BY n DESC', [r.city_key]);

	// Nearby launch areas, by distance between centres, with their real counts.
	const c = shape?.c ?? null;
	const near = c
		? Object.entries(AREAS)
				.filter(([k]) => k !== r.city_key)
				.map(([k, v]) => ({ k, v, d: Math.hypot((v.c[0] - c[0]) * Math.cos((c[1] * Math.PI) / 180), v.c[1] - c[1]) }))
				.filter((x) => x.d < 2.2)
				.sort((x, y) => x.d - y.d)
				.slice(0, 8)
		: [];
	const counts = near.length
		? Object.fromEntries(
				(
					await db.all<{ city_key: string; n: number }>(
						`SELECT city_key, COUNT(*) AS n FROM requests WHERE city_key IN (${near.map(() => '?').join(',')}) GROUP BY city_key`,
						near.map((x) => x.k)
					)
				).map((x) => [x.city_key, x.n])
			)
		: {};
	const nearby = near.map(({ k, v }) => ({ key: k, name: v.n, center: v.c, outline: v.h, waiting: counts[k] ?? 0 }));
	return ok({
		zip: r.zip,
		place: a.place,
		town: a.town,
		areaLabel: a.label,
		area: a.name,
		pin: coordsForZip(r.zip),
		outline: shape?.h ?? null,
		center: c,
		position,
		waiting,
		goal: GOAL,
		code: r.code,
		invited,
		pros,
		nearby
	});
}

const TRADE_SET = new Set<string>(TRADES);

export async function createPro(request: Request, env: Env) {
	const b = await body(request);
	if (!b) return fail('That did not look like a sign-up');
	const business = str(b.business).trim().replace(/\s+/g, ' ').slice(0, 120);
	const trade = str(b.trade);
	const zip = str(b.zip).trim();
	let phone = str(b.phone).replace(/\D/g, '');
	if (phone.length === 10) phone = '1' + phone;
	const email = b.email ? str(b.email).trim().slice(0, 160) : null;
	const consentText = str(b.consentText).trim().slice(0, 600);
	const ref = cleanRef(b.ref);
	// Optional, unticked by default: a public profile at scoo.app/p/<slug>. Ticking it asks for one;
	// Scoo publishes it after a check, so the form alone never puts a business on Google.
	const wantsProfile = b.profile === true;

	if (business.length < 2) return fail('Add your business name');
	if (!TRADE_SET.has(trade)) return fail('Pick your trade');
	if (!/^\d{5}$/.test(zip)) return fail('That ZIP code does not look right');
	if (!/^1\d{10}$/.test(phone)) return fail('That phone number does not look right');
	if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return fail('That email does not look right');
	if (b.consent !== true || consentText.length < 40) return fail('Please tick the box so we can reach you');
	if (!(await humanCheck(env, b.turnstile, request.headers.get('cf-connecting-ip')))) return notHuman();

	const a = area(zip);
	const db = openStore(env);
	let saved = await db.first<{ id: number; code: string }>('SELECT id, code FROM pros WHERE phone = ? AND trade = ? AND city_key = ?', [
		phone,
		trade,
		a.key
	]);
	if (saved && wantsProfile) {
		await db.run('UPDATE pros SET profile_ok = 1 WHERE id = ?', [saved.id]);
	}
	if (!saved) {
		// A pro can be invited by a customer (requests.code) or by another pro (pros.code).
		// Reserved now so the address can be shown and kept; the page stays dark until published.
		const slug = await freeProSlug(db, slugify(business, a.town));
		const known =
			ref &&
			((await db.first('SELECT 1 AS ok FROM requests WHERE code = ?', [ref])) ||
				(await db.first('SELECT 1 AS ok FROM pros WHERE code = ?', [ref])));
		saved = await insertWithCode(
			db,
			`INSERT INTO pros (business, trade, zip, city_key, city_name, phone, email, consent_text, consent_at, code, referred_by, user_agent, profile_ok, slug)
			 VALUES (?, ?, ?, ?, ?, ?, ?, ?, strftime('%Y-%m-%dT%H:%M:%fZ','now'), ?, ?, ?, ?, ?)`,
			(code) => [business, trade, zip, a.key, a.name, phone, email, consentText, code, known ? ref : null, userAgent(request), wantsProfile ? 1 : 0, slug]
		);
		if (!saved) return fail('Could not save your sign-up', 500);
	}
	const position = await count(db, 'SELECT COUNT(*) AS n FROM pros WHERE city_key = ? AND trade = ? AND id <= ?', [a.key, trade, saved.id]);
	return ok({ city: a.name, place: a.place, town: a.town, areaLabel: a.label, trade, position, code: saved.code });
}

// Exchange names: the slug in scoo.app/x/<slug>. Reserved words keep paths and the brand safe.
const RESERVED = new Set(
	'app api pros pro p request terms privacy exchanges exchange x r admin scoo example sitemap robots www help support login signup settings about blog jobs careers press legal security status'.split(
		' '
	)
);
const SLUG = /^[a-z0-9](?:[a-z0-9-]{1,30}[a-z0-9])$/;

async function nameCheck(db: Store, s: string): Promise<{ available: true } | { available: false; reason: string }> {
	if (!SLUG.test(s)) return { available: false, reason: 'Use 3 to 32 lowercase letters, numbers and dashes.' };
	if (RESERVED.has(s) || isExampleSlug(s)) return { available: false, reason: 'That name is reserved. Try another.' };
	const taken = await db.first('SELECT 1 AS t FROM operators WHERE slug = ?', [s]);
	return taken ? { available: false, reason: 'That name is taken. Try another.' } : { available: true };
}

export const exchangeName = async (env: Env, s: string) => ok(await nameCheck(openStore(env), s.toLowerCase()));

export async function createOperator(request: Request, env: Env) {
	const b = await body(request);
	if (!b) return fail('That did not look like an application');
	const slug = str(b.slug).trim().toLowerCase();
	const name = str(b.name).trim().replace(/\s+/g, ' ').slice(0, 80);
	const org = str(b.org).trim().replace(/\s+/g, ' ').slice(0, 120);
	const trades = (Array.isArray(b.trades) ? b.trades : [])
		.map((t) => str(t).slice(0, 40))
		.slice(0, 20)
		.join(',');
	const zip = str(b.zip).trim();
	const size = str(b.size).slice(0, 30);
	const volume = str(b.volume).slice(0, 30);
	const contact = contactOf(str(b.contact).trim().slice(0, 160));
	const consentText = str(b.consentText).trim().slice(0, 600);

	if (typeof contact === 'string') return fail(contact);
	if (name.length < 2) return fail('Add your name');
	if (org.length < 2) return fail('Add your company or network');
	if (!/^\d{5}$/.test(zip)) return fail('That ZIP code does not look right');
	if (b.consent !== true || consentText.length < 40) return fail('Please tick the box so we can reach you');
	if (!(await humanCheck(env, b.turnstile, request.headers.get('cf-connecting-ip')))) return notHuman();

	const db = openStore(env);
	const n = await nameCheck(db, slug);
	if (!n.available) return fail(n.reason.replace(/\.$/, ''), 409);
	const a = area(zip);
	try {
		await db.run(
			`INSERT INTO operators (slug, name, org, trades, zip, city_key, city_name, size, volume, phone, email, consent_text, consent_at, referred_by, user_agent)
			 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, strftime('%Y-%m-%dT%H:%M:%fZ','now'), ?, ?)`,
			[slug, name, org, trades, zip, a.key, a.name, size, volume, contact.phone, contact.email, consentText, cleanRef(b.ref), userAgent(request)]
		);
	} catch (e) {
		if (/UNIQUE/i.test(String(e))) return fail('That name was just taken. Try another', 409);
		throw e;
	}
	return ok({ slug, place: a.place, areaLabel: a.label });
}

// The homepage badge names the visitor's own area from Cloudflare's IP location: a metro we track
// by postal code, else the city Cloudflare reports. It is approximate (an IP, not a GPS fix), so it
// gives nothing when there is nothing usable, and never asks for location permission.
export function visitorTown(cf: IncomingRequestCfProperties | undefined): string | null {
	if (!cf || cf.country !== 'US') return null;
	const postal = typeof cf.postalCode === 'string' ? cf.postalCode : '';
	if (/^\d{5}/.test(postal)) {
		const t = area(postal.slice(0, 5)).town;
		if (t) return t;
	}
	return typeof cf.city === 'string' ? cf.city : null;
}
