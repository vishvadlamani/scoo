// The example exchange and its example members: what a living exchange will look like, for demos
// and for the "see an example" links. Every name and number here is invented. The pages say so on
// screen and tell search engines not to index them, and their slugs ("example", "example-…") are
// reserved so no real exchange or pro can ever be given one.
import { AREAS, type LonLat } from './geo/geo.ts';
import type { Exchange, ProCard, ProProfile, ServiceArea } from '#lib/profiles/types.ts';

export const EXAMPLE_EXCHANGE = 'example';
export const isExampleSlug = (slug: string) => slug === EXAMPLE_EXCHANGE || slug.startsWith('example-');

const area = (key: string, name: string): ServiceArea | null => (AREAS[key] ? { name, outline: AREAS[key].h } : null);

// Dallas and Fort Worth are separate launch areas; the example exchange spans both, so its outline
// is the convex hull of the two.
function hull(points: LonLat[]): LonLat[] {
	const pts = [...points].sort((a, b) => a[0] - b[0] || a[1] - b[1]);
	const cross = (o: LonLat, a: LonLat, b: LonLat) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
	const half = (list: LonLat[]) => {
		const out: LonLat[] = [];
		for (const p of list) {
			while (out.length >= 2 && cross(out[out.length - 2], out[out.length - 1], p) <= 0) out.pop();
			out.push(p);
		}
		return out.slice(0, -1);
	};
	return [...half(pts), ...half([...pts].reverse())];
}
const dfw = (): ServiceArea | null =>
	AREAS['dallas'] && AREAS['fort-worth']
		? { name: 'Dallas–Fort Worth', outline: hull([...AREAS['dallas'].h, ...AREAS['fort-worth'].h]) }
		: area('dallas', 'Dallas–Fort Worth');

type Example = ProCard & { about: string; services: string[]; areaKey: string; areaName: string };

const PROS: Example[] = [
	{
		slug: 'example-rivera-plumbing',
		business: 'Rivera Plumbing',
		trade: 'Plumber',
		place: 'Dallas, TX',
		premium: true,
		founding: true,
		memberSince: '2026-11-03',
		record: { jobsWon: 142, answerRate: 0.98, answerSecs: 9 },
		about:
			'Family-run since 2009. Leaks, water heaters, drains and repipes across Dallas. Licensed and insured, and we answer the phone, even at 9pm.',
		services: ['Leak repair', 'Water heaters', 'Drain cleaning', 'Repipes', 'Emergency call-outs'],
		areaKey: 'dallas',
		areaName: 'Dallas and nearby'
	},
	{
		slug: 'example-cool-front-hvac',
		business: 'Cool Front HVAC',
		trade: 'HVAC',
		place: 'Plano, TX',
		premium: true,
		founding: true,
		memberSince: '2026-11-05',
		record: { jobsWon: 96, answerRate: 0.95, answerSecs: 14 },
		about: 'AC repair and installs for North Dallas homes. Same-day diagnostics in summer.',
		services: ['AC repair', 'Furnace repair', 'New systems', 'Maintenance plans'],
		areaKey: 'dallas',
		areaName: 'Plano and North Dallas'
	},
	{
		slug: 'example-wirewise-electric',
		business: 'Wirewise Electric',
		trade: 'Electrician',
		place: 'Irving, TX',
		premium: false,
		founding: true,
		memberSince: '2026-11-08',
		record: { jobsWon: 77, answerRate: 0.97, answerSecs: 11 },
		about: 'Panels, outlets, lighting and EV chargers. Master electrician on every job.',
		services: ['Panel upgrades', 'EV chargers', 'Lighting', 'Outlets and switches'],
		areaKey: 'dallas',
		areaName: 'Irving and Las Colinas'
	},
	{
		slug: 'example-kettle-creek-roofing',
		business: 'Kettle Creek Roofing',
		trade: 'Roofer',
		place: 'Arlington, TX',
		premium: false,
		founding: true,
		memberSince: '2026-11-10',
		record: { jobsWon: 41, answerRate: 0.91, answerSecs: 22 },
		about: 'Storm damage, leaks and full replacements. Free roof checks after hail.',
		services: ['Roof repair', 'Storm damage', 'Replacements', 'Gutters'],
		areaKey: 'fort-worth',
		areaName: 'Arlington and Mid-Cities'
	},
	{
		slug: 'example-fixwell-handyman',
		business: 'Fixwell Handyman',
		trade: 'Handyman',
		place: 'Fort Worth, TX',
		premium: false,
		founding: true,
		memberSince: '2026-11-12',
		record: { jobsWon: 63, answerRate: 0.99, answerSecs: 7 },
		about: 'The small jobs list: doors, drywall, fixtures, assembly. No job too small.',
		services: ['Drywall', 'Doors', 'Fixtures', 'Furniture assembly'],
		areaKey: 'fort-worth',
		areaName: 'Fort Worth'
	},
	{
		slug: 'example-mesquite-drain',
		business: 'Mesquite Drain & Sewer',
		trade: 'Plumber',
		place: 'Mesquite, TX',
		premium: false,
		founding: false,
		memberSince: '2026-11-18',
		record: null,
		about: 'Drains and sewer lines, camera inspections included.',
		services: ['Drain cleaning', 'Sewer lines', 'Camera inspections'],
		areaKey: 'dallas',
		areaName: 'Mesquite and East Dallas'
	}
];

const card = ({ slug, business, trade, place, premium, founding, memberSince, record }: Example): ProCard => ({
	slug,
	business,
	trade,
	place,
	premium,
	founding,
	memberSince,
	record
});

const EXCHANGE: Exchange = {
	slug: EXAMPLE_EXCHANGE,
	name: 'DFW Home Pros',
	org: 'North Texas Trades Network',
	tagline: 'Licensed home pros across Dallas–Fort Worth, passing on the calls they can’t take.',
	about:
		'A referral group of independent plumbers, HVAC techs, electricians and roofers. When one of us is booked up, the call goes to another member instead of a stranger off a lead site. Every member is licensed, insured and answers their phone.',
	trades: ['Plumbing', 'HVAC', 'Electrical', 'Roofing', 'Handyman'],
	area: dfw(),
	rules: [
		'Emergency calls go first to members who answered 9 in 10 calls this month.',
		'Members take up to 8 calls a day, 7am to 9pm.',
		'New members get one call a day for their first week.',
		'Calls under 60 seconds are free for the member.'
	],
	members: PROS.map(card),
	numbers: { members: PROS.length, sources: 3, answerSecs: 12, jobsThisWeek: 37 },
	activity: [
		{ when: '4 min ago', text: 'Rivera Plumbing took an emergency call in Uptown' },
		{ when: '22 min ago', text: 'Cool Front HVAC booked an AC repair in Plano' },
		{ when: '1 hr ago', text: 'Mesquite Drain & Sewer joined the exchange' },
		{ when: '2 hr ago', text: 'Kettle Creek Roofing passed a call to Fixwell Handyman' },
		{ when: 'Yesterday', text: 'The exchange matched 9 jobs' }
	],
	openedAt: '2026-11-01',
	example: true
};

export function exampleExchange(slug: string): Exchange | null {
	return slug === EXAMPLE_EXCHANGE ? EXCHANGE : null;
}

export function examplePro(slug: string): ProProfile | null {
	const p = PROS.find((x) => x.slug === slug);
	if (!p) return null;
	return {
		...card(p),
		about: p.about,
		services: p.services,
		area: area(p.areaKey, p.areaName),
		exchanges: [{ slug: EXCHANGE.slug, name: EXCHANGE.name }],
		example: true
	};
}
