// What a public pro profile and an exchange page show. Built on the server, from the database for
// real pages and from examples.ts for the example ones.
/** [longitude, latitude] */
export type LonLat = [number, number];

/** Numbers Scoo counts from real calls. Absent until there are calls to count. */
export type TrackRecord = {
	jobsWon: number;
	/** share of offered calls the pro picked up, 0 to 1 */
	answerRate: number;
	/** average seconds to pick up */
	answerSecs: number;
};

export type ServiceArea = { name: string; outline: LonLat[] };

/** The short form, used on cards in an exchange's member list. */
export type ProCard = {
	slug: string;
	business: string;
	trade: string;
	/** "Dallas, TX" */
	place: string | null;
	premium: boolean;
	/** joined before Scoo opened in their area */
	founding: boolean;
	/** ISO date */
	memberSince: string;
	record: TrackRecord | null;
};

export type ProProfile = ProCard & {
	about: string | null;
	services: string[];
	area: ServiceArea | null;
	exchanges: { slug: string; name: string }[];
	example: boolean;
};

export type Activity = { when: string; text: string };

export type Exchange = {
	slug: string;
	name: string;
	org: string;
	tagline: string | null;
	about: string | null;
	trades: string[];
	area: ServiceArea | null;
	rules: string[];
	members: ProCard[];
	/** live numbers, once the exchange is open */
	numbers: { members: number; sources: number; answerSecs: number; jobsThisWeek: number } | null;
	activity: Activity[];
	/** ISO date */
	openedAt: string;
	example: boolean;
};
