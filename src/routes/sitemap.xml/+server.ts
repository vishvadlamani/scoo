// The pages search engines should know about: the fixed ones, plus every published exchange and pro
// profile. Example pages are left out (and carry noindex), as are /app and the API.
import { env } from 'cloudflare:workers';
import { openStore } from '#lib/server/store.ts';
import { publishedPages } from '#lib/server/profiles.ts';
import type { RequestHandler } from './$types';

const FIXED = ['/', '/request', '/pros', '/exchanges/start', '/terms', '/privacy'];
const xml = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

export const GET: RequestHandler = async () => {
	const pages = [...FIXED.map((path) => ({ path, updated: null as string | null })), ...(await publishedPages(openStore(env)))];
	const body =
		'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
		pages.map((p) => `<url><loc>https://scoo.app${xml(p.path)}</loc>${p.updated ? `<lastmod>${p.updated}</lastmod>` : ''}</url>`).join('\n') +
		'\n</urlset>\n';
	return new Response(body, { headers: { 'content-type': 'application/xml; charset=utf-8', 'cache-control': 'public, max-age=3600' } });
};
