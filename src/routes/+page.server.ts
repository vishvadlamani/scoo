// The homepage badge names the visitor's own area from Cloudflare's IP location. It is approximate
// (an IP, not a GPS fix) and never asks for location permission; with nothing usable the page keeps
// its default badge. The answer differs per visitor, so it must not be cached as one page.
import { visitorTown } from '#lib/server/waitlist.ts';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = ({ request, setHeaders }) => {
	setHeaders({ 'cache-control': 'private, no-cache', vary: 'cf-ipcity' });
	// adapter-cloudflare puts the cf object on the request itself, in dev and in production
	const cf = (request as Request & { cf?: IncomingRequestCfProperties }).cf;
	return { town: visitorTown(cf) };
};
