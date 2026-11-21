// What the two sign-up forms (/pros and /exchanges/start) share: Cloudflare Turnstile and the POST.
// Turnstile is on only when the server has a site key (/api/config says so); without one the forms
// submit with no token and the API does not ask for it. The script loads once per page view.

interface TurnstileOptions {
	sitekey: string;
	theme: 'auto' | 'light' | 'dark';
	callback: (token: string) => void;
	'expired-callback': () => void;
}
interface TurnstileApi {
	render(el: HTMLElement, options: TurnstileOptions): string;
	reset(id: string): void;
	remove(id: string): void;
}
declare global {
	interface Window {
		turnstile?: TurnstileApi;
		scooTurnstileReady?: () => void;
	}
}

let script: Promise<TurnstileApi> | null = null;
const loadScript = () =>
	(script ??= new Promise((resolve) => {
		window.scooTurnstileReady = () => resolve(window.turnstile!);
		const s = document.createElement('script');
		s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?onload=scooTurnstileReady&render=explicit';
		s.async = true;
		document.head.appendChild(s);
	}));

export interface Turnstile {
	/** Throw the current token away and ask again; after a failed submit a token is spent. */
	reset(): void;
	/** Remove the widget when the form unmounts. */
	destroy(): void;
}

/**
 * Renders Turnstile into `el` when the server has a site key. `needed` is called before the widget
 * loads, so the form can hold its submit button until `token` arrives.
 */
export function mountTurnstile(
	el: HTMLElement,
	on: { needed: () => void; token: (token: string | null) => void }
): Turnstile {
	let id: string | null = null;
	let gone = false;
	fetch('/api/config')
		.then((r) => r.json() as Promise<{ turnstileSiteKey: string | null }>)
		.then(async (c) => {
			if (!c.turnstileSiteKey || gone) return;
			on.needed();
			const ts = await loadScript();
			if (gone) return;
			id = ts.render(el, {
				sitekey: c.turnstileSiteKey,
				theme: 'auto',
				callback: (t) => on.token(t),
				'expired-callback': () => on.token(null)
			});
		})
		.catch(() => {});
	return {
		reset() {
			if (id !== null && window.turnstile) {
				window.turnstile.reset(id);
				on.token(null);
			}
		},
		destroy() {
			gone = true;
			if (id !== null) window.turnstile?.remove(id);
		}
	};
}

/** POSTs JSON and returns the reply, or throws the API's own error message. */
export async function postJson<T>(url: string, body: unknown): Promise<T> {
	const res = await fetch(url, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) });
	const j = (await res.json()) as T & { error?: string };
	if (!res.ok) throw new Error(j.error || 'Something went wrong');
	return j;
}
