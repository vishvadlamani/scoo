// The request flow's data: the steps, what a typed need is matched to, the one follow-up question
// per kind of pro, and the shapes the API answers with. No DOM, no state: the page owns those.

export const ORDER = ['need', 'zip', 'q', 'phone', 'done'] as const;
export type Step = (typeof ORDER)[number];

export type Category = 'plumber' | 'electrician' | 'lawyer' | 'insurance' | 'doctor' | 'mover' | 'pro';

/** What the visitor typed, matched to a kind of pro and the noun the copy uses for it. */
export interface Need {
	text: string;
	cat: Category;
	noun: string;
}

// First match wins, so the order matters: "insurance for my move" is insurance, not movers.
const CATS: [RegExp, Category, string][] = [
	[/plumb|leak|tap|pipe|toilet|drain|water heater/i, 'plumber', 'a plumber'],
	[/lawyer|legal|divorce|attorney|custody|sue/i, 'lawyer', 'a lawyer'],
	[/insur/i, 'insurance', 'an insurance agent'],
	[/electric|power|outlet|spark|breaker|wiring/i, 'electrician', 'an electrician'],
	[/move|moving|sofa|couch|movers/i, 'mover', 'movers'],
	[/doctor|weight|health|glp|clinic|sick/i, 'doctor', 'a doctor']
];

export function classify(text: string): Need {
	const c = CATS.find(([re]) => re.test(text));
	return c ? { text, cat: c[1], noun: c[2] } : { text, cat: 'pro', noun: 'a pro' };
}

export const QUESTIONS: Record<Category, [string, string[]]> = {
	plumber: ['Is water leaking right now?', ["Yes, it's urgent", 'No, it can wait']],
	electrician: ['Is anything sparking or smoking?', ['Yes', 'No']],
	lawyer: ['What kind of help do you need?', ['Divorce or family', 'Injury', 'Business', 'Something else']],
	insurance: ['What do you want to insure?', ['Car', 'Home', 'Life', 'Health']],
	doctor: ['Is this a medical emergency?', ['Yes', 'No']],
	mover: ['When do you need them?', ['Today', 'This week', 'Later']],
	pro: ['How soon do you need help?', ['Right now', 'This week', 'Just planning ahead']]
};

/** A phone number (ten digits, however it is written) or a plausible email address. */
export const validContact = (v: string) =>
	v.includes('@') ? /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) : v.replace(/\D/g, '').length >= 10;

/** GET /api/city: where a ZIP is and how many are already waiting there. */
export interface Area {
	city: string;
	place: string | null;
	town: string | null;
	areaLabel: string;
	waiting: number;
}

/** POST /api/requests on success: the visitor's place in line and their invite code. */
export interface Joined {
	position: number;
	waiting: number;
	goal: number;
	city: string;
	town: string | null;
	areaLabel: string | null;
	code: string;
	via: 'text' | 'email';
}

// ?step=N skips the lookup; the screens then show the area the screenshots were taken with.
export const DEMO_AREA: Area = { city: 'Dallas', place: 'Plano, TX', town: 'Plano', areaLabel: 'the Dallas area', waiting: 0 };

export const wait = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

/** One line of the area lookup: waiting, running (a spinner) or done (a tick). */
export type Mark = '' | 'run' | 'ok';

/** What the map-search screen says while the lookup runs. */
export interface SearchView {
	title: string;
	marks: [Mark, Mark, Mark];
	zip: string;
	/** Set once the lookup has placed the ZIP; the first line then names it. */
	place: string | null;
	pros: string;
	launch: string;
}

/** The lookup screen: search while it runs; found once the area is known and the map is
 * shrinking; ready when the contact form is up. */
export type Phase = 'search' | 'found' | 'ready';
