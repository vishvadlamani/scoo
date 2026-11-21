// See https://svelte.dev/docs/kit/types#app.d.ts
declare global {
	namespace Cloudflare {
		/** The Worker's bindings (`import { env } from 'cloudflare:workers'`), from wrangler.jsonc and `wrangler secret put`. */
		interface Env {
			DB?: D1Database;
			/** libsql://… — when set, the waitlist uses Turso instead of D1 */
			TURSO_URL?: string;
			TURSO_AUTH_TOKEN?: string;
			/** Turnstile is on only when both are set */
			TURNSTILE_SECRET?: string;
			TURNSTILE_SITE_KEY?: string;
		}
	}
	type Env = Cloudflare.Env;
}

export {};
