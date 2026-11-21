import { redirect } from '@sveltejs/kit';
import type { Handle } from '@sveltejs/kit/hooks';

export const handle: Handle = async ({ event, resolve }) => {
	// One canonical address: www.scoo.app sends people to scoo.app, keeping the path and query.
	if (event.url.hostname === 'www.scoo.app') {
		const to = new URL(event.url);
		to.hostname = 'scoo.app';
		redirect(301, to.toString());
	}
	return resolve(event);
};
