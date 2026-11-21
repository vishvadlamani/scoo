import { redirect } from '@sveltejs/kit';
import type { Handle } from '@sveltejs/kit/hooks';

// The old static site's file names, still in links and bookmarks.
const OLD_PATHS: Record<string, string> = {
	'/index.html': '/',
	'/request.html': '/request',
	'/pros.html': '/pros'
};

// www.scoo.app → scoo.app is handled ahead of SvelteKit (tools/embed-assets.ts), since
// prerendered pages never reach this hook.
export const handle: Handle = async ({ event, resolve }) => {
	const moved = OLD_PATHS[event.url.pathname];
	if (moved) redirect(301, moved + event.url.search);
	return resolve(event);
};
