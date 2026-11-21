// Where a ZIP is, and which launch area it counts toward. Tables come from GeoNames (CC BY 4.0) via
// tools/geo-build.ts.
//
// zips.json packs 40,979 ZIPs small enough to ship in a Worker: one sorted string of 5-digit ZIPs
// (binary-searched, no index to build), a base-36 index into a list of "City, ST" names, and a
// centroid in hundredths of a degree (~1 km).
import packed from './zips.json';
import areasJson from './areas.json';
import metros from './metros.json';

export type LonLat = [number, number];
export type Area = { n: string; c: LonLat; h: LonLat[] };
export const AREAS = areasJson as unknown as Record<string, Area>;

const IDX = packed.idx.split(',');
let coordList: string[] | null = null;

function find(zip: string): number {
	let lo = 0;
	let hi = packed.zips.length / 5 - 1;
	while (lo <= hi) {
		const mid = (lo + hi) >> 1;
		const z = packed.zips.slice(mid * 5, mid * 5 + 5);
		if (z === zip) return mid;
		if (z < zip) lo = mid + 1;
		else hi = mid - 1;
	}
	return -1;
}

/** "Plano, TX", or null for a ZIP GeoNames does not list. */
export function placeForZip(zip: string): string | null {
	const i = find(zip);
	return i < 0 ? null : packed.places[parseInt(IDX[i], 36)];
}

/** [lat, lon] of the ZIP's centroid. */
export function coordsForZip(zip: string): [number, number] | null {
	const i = find(zip);
	if (i < 0) return null;
	coordList ??= packed.coords.split(',');
	const [la, lo] = coordList[i].split(':');
	return [Number(la) / 100, Number(lo) / 100];
}

// Launch areas by 3-digit ZIP prefix. A prefix not listed still counts: it becomes its own area,
// named after the prefix, so demand outside these metros shows up rather than being dropped.
const PREFIX = new Map((metros as [string, string[]][]).flatMap(([name, ps]) => ps.map((p) => [p, name] as const)));

export type AreaInfo = {
	/** what launch counts are kept against */
	key: string;
	/** the launch area, for counts and positions */
	name: string;
	/** "Plano, TX", said back to them */
	place: string | null;
	/** "Plano" */
	town: string | null;
	/** "the Dallas area" */
	label: string;
};

// Two answers for one ZIP. `place` is the town people recognise, which is what the page says back
// to them; `key` and `name` are the launch area the sign-up counts toward (Plano counts toward
// Dallas).
export function area(zip: string): AreaInfo {
	const p = zip.slice(0, 3);
	const metro = PREFIX.get(p) ?? null;
	const place = placeForZip(zip);
	const town = place ? place.replace(/, [A-Z]{2}$/, '') : null;
	return {
		key: metro ? metro.toLowerCase().replace(/\s+/g, '-') : 'zip-' + p,
		name: metro ?? town ?? 'your area',
		place: place ?? metro,
		town: town ?? metro,
		label: metro ? `the ${metro} area` : town ? `the ${town} area` : 'your area'
	};
}
