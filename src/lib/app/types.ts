// What GET /api/me returns: everything the map home shows, for the signed-in person only. Mirrors
// the object built by `me()` in #lib/server/waitlist.ts; counts are by area, never points.

/** [longitude, latitude], the order MapLibre and GeoJSON use. */
export type LonLat = [number, number];

/** How many pros of one trade have joined the area. */
export type ProCount = { trade: string; n: number };

/** A launch area near theirs, with its real count. */
export type NearbyArea = {
	key: string;
	name: string;
	center: LonLat;
	outline: LonLat[];
	waiting: number;
};

export type Me = {
	zip: string;
	/** "Plano, TX", said back to them */
	place: string | null;
	/** "Plano" */
	town: string | null;
	/** "the Dallas area" */
	areaLabel: string;
	/** the launch area their sign-up counts toward, e.g. "Dallas" */
	area: string;
	/** their ZIP's centroid as [lat, lon]: note the order, unlike every other coordinate here */
	pin: [number, number] | null;
	outline: LonLat[] | null;
	center: LonLat | null;
	position: number;
	waiting: number;
	goal: number;
	/** public invite code, in every link they share */
	code: string;
	invited: number;
	pros: ProCount[];
	nearby: NearbyArea[];
};
