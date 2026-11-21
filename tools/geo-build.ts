// Builds the ZIP and launch-area tables from GeoNames' US postal codes (CC BY 4.0):
//
//   src/lib/server/geo/zips.json   ZIP -> "City, ST" and centroid, packed (see geo.ts)
//   src/lib/server/geo/areas.json  every launch area: name, centre [lon, lat] and an outline
//
//   curl -LO https://download.geonames.org/export/zip/US.zip && unzip US.zip US.txt
//   npm run geo -- path/to/US.txt
//
// Launch areas are the metros in metros.json (by 3-digit ZIP prefix), and every other prefix is an
// area of its own, so demand outside the metros still shows up. An outline is the padded convex
// hull of the area's ZIP centroids: honest about being approximate, and small enough to ship.
import { readFileSync, writeFileSync } from 'node:fs';

type Metro = [name: string, prefixes: string[]];
type Row = { city: string; st: string; lat: number; lon: number };
type Pt = [number, number];

const src = process.argv[2];
if (!src) throw new Error('usage: npm run geo -- path/to/US.txt');
const dir = 'src/lib/server/geo';
const metros = JSON.parse(readFileSync(`${dir}/metros.json`, 'utf8')) as Metro[];
const prefixMetro = new Map(metros.flatMap(([name, ps]) => ps.map((p) => [p, name] as const)));
const slug = (name: string) => name.toLowerCase().replace(/\s+/g, '-');

const rows = new Map<string, Row>();
for (const line of readFileSync(src, 'utf8').split('\n')) {
	const f = line.split('\t');
	const [z, city, st, lat, lon] = [f[1], f[2], f[4], f[9], f[10]];
	if (z?.length === 5 && /^\d{5}$/.test(z) && st && lat && lon && !rows.has(z)) {
		rows.set(z, { city, st, lat: Number(lat), lon: Number(lon) });
	}
}
const zs = [...rows.keys()].sort();
const placeOf = (r: Row) => `${r.city}, ${r.st}`;
const places = [...new Set([...rows.values()].map(placeOf))].sort();
const placeIndex = new Map(places.map((p, i) => [p, i]));
const r = (z: string) => rows.get(z)!;
// Python's round(): halves go to the even neighbour. Kept so a rebuild reproduces the shipped data.
const roundEven = (n: number) => {
	const f = Math.floor(n);
	return n - f === 0.5 ? (f % 2 === 0 ? f : f + 1) : Math.round(n);
};

writeFileSync(
	`${dir}/zips.json`,
	JSON.stringify({
		zips: zs.join(''),
		idx: zs.map((z) => placeIndex.get(placeOf(r(z)))!.toString(36)).join(','),
		places,
		coords: zs.map((z) => `${roundEven(r(z).lat * 100)}:${roundEven(r(z).lon * 100)}`).join(',')
	})
);

function hull(input: Pt[]): Pt[] {
	const pts = [...new Map(input.map((p) => [p.join(','), p])).values()].sort((a, b) => a[0] - b[0] || a[1] - b[1]);
	if (pts.length < 3) return pts;
	const cross = (o: Pt, a: Pt, b: Pt) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
	const half = (list: Pt[]) => {
		const out: Pt[] = [];
		for (const p of list) {
			while (out.length >= 2 && cross(out[out.length - 2], out[out.length - 1], p) <= 0) out.pop();
			out.push(p);
		}
		return out.slice(0, -1);
	};
	return [...half(pts), ...half([...pts].reverse())];
}

const groups = new Map<string, string[]>();
for (const z of zs) {
	const m = prefixMetro.get(z.slice(0, 3));
	const key = m ? slug(m) : 'zip-' + z.slice(0, 3);
	groups.set(key, [...(groups.get(key) ?? []), z]);
}
const round3 = (n: number) => Number(n.toFixed(3));
const PAD = 0.05; // degrees: keeps a lone ZIP or a thin hull visible on the map
const areas: Record<string, { n: string; c: Pt; h: Pt[] }> = {};
for (const [key, members] of groups) {
	const pts = members.map((z): Pt => [r(z).lon, r(z).lat]);
	const cx = pts.reduce((s, p) => s + p[0], 0) / pts.length;
	const cy = pts.reduce((s, p) => s + p[1], 0) / pts.length;
	let h = hull(pts);
	h =
		h.length < 3
			? Array.from({ length: 12 }, (_, i): Pt => [cx + PAD * 1.3 * Math.cos((i * Math.PI) / 6), cy + PAD * Math.sin((i * Math.PI) / 6)])
			: h.map(([x, y]): Pt => [cx + (x - cx) * 1.08 + Math.sign(x - cx || 1) * PAD * 0.6, cy + (y - cy) * 1.08 + Math.sign(y - cy || 1) * PAD * 0.5]);
	let name: string;
	if (key.startsWith('zip-')) {
		const counts = new Map<string, number>();
		for (const z of members) counts.set(r(z).city, (counts.get(r(z).city) ?? 0) + 1);
		name = [...counts].reduce((best, c) => (c[1] > best[1] ? c : best))[0];
	} else {
		name = metros.find(([n]) => slug(n) === key)![0];
	}
	areas[key] = { n: name, c: [round3(cx), round3(cy)], h: h.map(([x, y]): Pt => [round3(x), round3(y)]) };
}
writeFileSync(`${dir}/areas.json`, JSON.stringify(areas));
console.log(`${zs.length} zips, ${Object.keys(areas).length} areas`);
