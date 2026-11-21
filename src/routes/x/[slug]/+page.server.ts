import { error } from '@sveltejs/kit';
import { env } from 'cloudflare:workers';
import { openStore } from '#lib/server/store.ts';
import { getExchange } from '#lib/server/profiles.ts';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, setHeaders }) => {
	const exchange = await getExchange(openStore(env), params.slug);
	if (!exchange) error(404, 'No exchange here');
	// Public and the same for everyone: a short shared cache keeps the database out of most hits.
	setHeaders({ 'cache-control': 'public, max-age=60' });
	return { exchange };
};
