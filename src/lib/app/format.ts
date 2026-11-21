export const fmt = (n: number) => n.toLocaleString();

// Trades are stored as the pros form names them ("Plumber", "Doctor or clinic"); a sentence wants
// "3 plumbers" and "1 clinic".
const SPECIAL: Record<string, [string, string]> = {
	HVAC: ['HVAC pro', 'HVAC pros'],
	'Pest control': ['pest control pro', 'pest control pros'],
	'Doctor or clinic': ['clinic', 'clinics'],
	Other: ['pro', 'pros']
};

export function tradeName(trade: string, n: number): string {
	const special = Object.hasOwn(SPECIAL, trade) ? SPECIAL[trade] : undefined;
	if (special) return special[n > 1 ? 1 : 0];
	const w = trade.toLowerCase();
	return n > 1 ? (w.endsWith('s') ? w + 'es' : w + 's') : w;
}
