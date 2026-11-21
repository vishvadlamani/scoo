// Small formatters shared by the profile and exchange pages.

/** "Rivera Plumbing" → "RP" */
export const initials = (name: string) =>
	name
		.replace(/&/g, ' ')
		.split(/\s+/)
		.filter((w) => /^[A-Za-z0-9]/.test(w))
		.slice(0, 2)
		.map((w) => w[0].toUpperCase())
		.join('');

/** "2026-11-03" → "Nov 2026" */
export const monthYear = (iso: string) =>
	new Date(iso + 'T12:00:00Z').toLocaleDateString('en-US', { month: 'short', year: 'numeric', timeZone: 'UTC' });

export const percent = (n: number) => `${Math.round(n * 100)}%`;

/** A trade as a noun for "Request a …": "Plumber" → "a plumber", "HVAC" → "an HVAC pro". */
export function tradeNoun(trade: string): string {
	const t = trade === 'HVAC' ? 'HVAC pro' : trade === 'Doctor or clinic' ? 'doctor' : trade.toLowerCase();
	return (/^[aeiou]/i.test(t) || t.startsWith('HVAC') ? 'an ' : 'a ') + t;
}
