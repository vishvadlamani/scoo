import { error } from '@sveltejs/kit';
import { env } from 'cloudflare:workers';
import { openStore } from '#lib/server/store.ts';
import { getPro } from '#lib/server/profiles.ts';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, setHeaders }) => {
	const pro = await getPro(openStore(env), params.slug);
	if (!pro) error(404, 'No pro here');
	setHeaders({ 'cache-control': 'public, max-age=60' });
	return { pro };
};
