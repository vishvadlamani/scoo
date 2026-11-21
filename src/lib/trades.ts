// The trades a pro can sign up under. Shared by the pros form and the API that validates it.
export const TRADES = [
	'Plumber',
	'Electrician',
	'HVAC',
	'Roofer',
	'Handyman',
	'Cleaner',
	'Mover',
	'Locksmith',
	'Pest control',
	'Landscaper',
	'Mechanic',
	'Lawyer',
	'Insurance agent',
	'Real estate agent',
	'Doctor or clinic',
	'Tutor',
	'Other'
] as const;

export type Trade = (typeof TRADES)[number];
