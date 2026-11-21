// Public pro profiles (/p/<slug>) and exchange pages (/x/<slug>). A real page exists only once it is
// published; until then its slug answers 404, exactly like a slug nobody has.
import { AREAS, area } from './geo/geo.ts';
import type { Store } from './store.ts';
import { examplePro, exampleExchange, isExampleSlug } from './examples.ts';
import type { Exchange, ProCard, ProProfile } from '#lib/profiles/types.ts';

/** "Rivera Plumbing", "Dallas" → "rivera-plumbing-dallas". Never an example slug. */
export function slugify(...parts: (string | null)[]): string {
	const s = parts
		.filter(Boolean)
		.join(' ')
		.normalize('NFKD')
		.replace(/[̀-ͯ]/g, '')
		.toLowerCase()
		.replace(/&/g, ' and ')
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/^-+|-+$/g, '')
		.slice(0, 60)
		.replace(/-+$/, '');
	return isExampleSlug(s) || s.length < 3 ? `pro-${s}`.replace(/-+$/, '') : s;
}

/** A slug no other pro has: the plain one, else with -2, -3… */
export async function freeProSlug(db: Store, base: string): Promise<string> {
	for (let n = 1; n < 50; n++) {
		const s = n === 1 ? base : `${base}-${n}`;
		if (!(await db.first('SELECT 1 AS t FROM pros WHERE slug = ?', [s]))) return s;
	}
	return `${base}-${crypto.randomUUID().slice(0, 6)}`;
}

type ProRow = {
	id: number;
	slug: string;
	business: string;
	trade: string;
	zip: string;
	city_key: string;
	about: string | null;
	premium: number;
	created_at: string;
};

// Every pro who signed up before Scoo opened is a founding pro: that is what the pros page offers.
// Track records stay null until calls are counted; nothing is typed in.
const toCard = (r: ProRow): ProCard => ({
	slug: r.slug,
	business: r.business,
	trade: r.trade,
	place: area(r.zip).place,
	premium: r.premium === 1,
	founding: true,
	memberSince: r.created_at.slice(0, 10),
	record: null
});

const PRO_COLS = 'p.id, p.slug, p.business, p.trade, p.zip, p.city_key, p.about, p.premium, p.created_at';

export async function getPro(db: Store, slug: string): Promise<ProProfile | null> {
	if (isExampleSlug(slug)) return examplePro(slug);
	const r = await db.first<ProRow>(`SELECT ${PRO_COLS} FROM pros p WHERE p.slug = ? AND p.published_at IS NOT NULL`, [slug]);
	if (!r) return null;
	const exchanges = await db.all<{ slug: string; name: string }>(
		`SELECT o.slug, o.org AS name FROM exchange_members m JOIN operators o ON o.id = m.operator_id
		 WHERE m.pro_id = ? AND o.published_at IS NOT NULL ORDER BY m.joined_at`,
		[r.id]
	);
	const a = AREAS[r.city_key];
	return {
		...toCard(r),
		about: r.about,
		services: [r.trade],
		area: a ? { name: area(r.zip).label.replace(/^the /, ''), outline: a.h } : null,
		exchanges,
		example: false
	};
}

type OperatorRow = {
	id: number;
	slug: string;
	name: string;
	org: string;
	trades: string | null;
	zip: string;
	city_key: string;
	tagline: string | null;
	about: string | null;
	rules: string | null;
	published_at: string;
};

export async function getExchange(db: Store, slug: string): Promise<Exchange | null> {
	if (isExampleSlug(slug)) return exampleExchange(slug);
	const o = await db.first<OperatorRow>(
		'SELECT id, slug, name, org, trades, zip, city_key, tagline, about, rules, published_at FROM operators WHERE slug = ? AND published_at IS NOT NULL',
		[slug]
	);
	if (!o) return null;
	const members = await db.all<ProRow>(
		`SELECT ${PRO_COLS} FROM exchange_members m JOIN pros p ON p.id = m.pro_id
		 WHERE m.operator_id = ? AND p.published_at IS NOT NULL ORDER BY m.joined_at`,
		[o.id]
	);
	const a = AREAS[o.city_key];
	return {
		slug: o.slug,
		// `name` on an application is the applicant's own name; the exchange is known by its org
		name: o.org,
		org: o.org,
		tagline: o.tagline,
		about: o.about,
		trades: (o.trades ?? '').split(',').filter(Boolean),
		area: a ? { name: area(o.zip).label.replace(/^the /, ''), outline: a.h } : null,
		rules: (o.rules ?? '')
			.split('\n')
			.map((s) => s.trim())
			.filter(Boolean),
		members: members.map(toCard),
		// Live numbers need call data, which does not exist before launch.
		numbers: null,
		activity: [],
		openedAt: o.published_at.slice(0, 10),
		example: false
	};
}

/** Every published page, for the sitemap. */
export async function publishedPages(db: Store): Promise<{ path: string; updated: string }[]> {
	const pros = await db.all<{ slug: string; published_at: string }>(
		'SELECT slug, published_at FROM pros WHERE published_at IS NOT NULL AND slug IS NOT NULL'
	);
	const exchanges = await db.all<{ slug: string; published_at: string }>(
		'SELECT slug, published_at FROM operators WHERE published_at IS NOT NULL'
	);
	return [
		...exchanges.map((x) => ({ path: `/x/${x.slug}`, updated: x.published_at.slice(0, 10) })),
		...pros.map((p) => ({ path: `/p/${p.slug}`, updated: p.published_at.slice(0, 10) }))
	];
}
