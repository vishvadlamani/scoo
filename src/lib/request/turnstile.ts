// Cloudflare Turnstile, loaded only when the site has a key configured (GET /api/config). The
// script is fetched on demand so the page costs nothing extra while it is switched off.

interface Turnstile {
	render(el: HTMLElement, opts: Record<string, unknown>): string;
	reset(id: string): void;
	remove(id: string): void;
}
type TsWindow = Window & { turnstile?: Turnstile; onTs?: () => void };

export interface Widget {
	reset(): void;
	remove(): void;
}

/**
 * Renders the check into `el`. `onNeeded` fires as soon as the site turns out to want one, so the
 * submit button can wait for it before the script has even loaded; `onToken` hears the token, and
 * null when it expires. The returned widget can be reset after a failed submit, since a token is
 * single-use.
 */
export async function mountTurnstile(
	el: HTMLElement,
	onNeeded: () => void,
	onToken: (t: string | null) => void
): Promise<Widget | null> {
	const c = (await fetch('/api/config').then((r) => r.json())) as { turnstileSiteKey?: string | null };
	if (!c.turnstileSiteKey) return null;
	onNeeded();
	const w = window as TsWindow;
	if (!w.turnstile) {
		// Another page may already have loaded it during this visit; its onload would not fire again.
		await new Promise<void>((resolve) => {
			w.onTs = resolve;
			const sc = document.createElement('script');
			sc.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?onload=onTs&render=explicit';
			sc.async = true;
			document.head.appendChild(sc);
		});
	}
	const ts = w.turnstile!;
	const id = ts.render(el, {
		sitekey: c.turnstileSiteKey,
		theme: 'auto',
		callback: (t: string) => onToken(t),
		'expired-callback': () => onToken(null)
	});
	return { reset: () => ts.reset(id), remove: () => ts.remove(id) };
}
