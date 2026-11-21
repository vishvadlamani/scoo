<!-- The map-search screen and what it turns into: while the lookup runs, a map zooms in on the ZIP
     under a checklist; once the area is known the map shrinks, the checklist folds away and the
     contact form rises in its place. -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { ART_SEARCH } from './art.ts';
	import MapSearch from './MapSearch.svelte';
	import { validContact, type Area, type Joined, type Phase, type SearchView } from './flow.ts';
	import { mountTurnstile, type Widget } from './turnstile.ts';

	let {
		phase,
		view,
		zip,
		area,
		body,
		onjoined
	}: {
		phase: Phase;
		view: SearchView;
		zip: string;
		area: Area | null;
		/** The request so far, sent with the contact details. */
		body: () => { need: string; category: string; answer: string | null; zip: string };
		onjoined: (j: Joined) => void;
	} = $props();

	let contact = $state('');
	let ok = $state(false);
	let saving = $state(false);
	let error = $state<string | null>(null);
	// Turnstile, when the site has it switched on: the button waits for the check as well.
	let tsNeeded = $state(false);
	let tsToken = $state<string | null>(null);
	let widget: Widget | null = null;

	let form: HTMLFormElement;
	let tel: HTMLInputElement;
	let consent: HTMLSpanElement;
	let tsEl: HTMLDivElement;

	const ready = $derived(ok && validContact(contact) && (!tsNeeded || tsToken !== null));
	const town = $derived(area?.town ?? null);
	const waiting = $derived(area?.waiting ?? 0);

	onMount(() => {
		let gone = false;
		mountTurnstile(
			tsEl,
			() => (tsNeeded = true),
			(t) => (tsToken = t)
		)
			.then((w) => {
				if (gone) w?.remove();
				else widget = w;
			})
			.catch(() => {});
		return () => {
			gone = true;
			widget?.remove();
		};
	});

	export function focusContact() {
		tel.focus({ preventScroll: true });
	}

	/** ?step=4: fill the form as a visitor would and send it. */
	export function demoSubmit(value: string) {
		contact = value;
		ok = true;
		// The bound values reach the DOM on the next flush; the submit should see them as typed.
		queueMicrotask(() => form.requestSubmit());
	}

	async function save(e: SubmitEvent) {
		e.preventDefault();
		if (saving || !ready) return;
		saving = true;
		let ref: string | null = null;
		try {
			ref = localStorage.getItem('scoo_ref');
		} catch {
			// storage blocked: the request still goes, just without the referral
		}
		// The exact words the visitor agreed to, as rendered, are stored with the request.
		const payload = {
			...body(),
			contact: contact.trim(),
			consent: ok,
			consentText: consent.textContent,
			ref,
			turnstile: tsToken
		};
		try {
			const res = await fetch('/api/requests', {
				method: 'POST',
				headers: { 'content-type': 'application/json' },
				body: JSON.stringify(payload)
			});
			const r = (await res.json()) as Joined & { error?: string };
			if (!res.ok) throw new Error(r.error || 'Something went wrong');
			onjoined(r);
		} catch (err) {
			saving = false;
			if (tsNeeded && widget) {
				widget.reset();
				tsToken = null;
			}
			error = (err instanceof Error ? err.message : String(err)) + '. Please try again.';
		}
	}
</script>

<div class="phone" class:notify={phase !== 'search'}>
	<div class="art">{@html ART_SEARCH}</div>
	<p class="placechip" id="placechip" hidden={phase === 'search'}>
		<svg viewBox="0 0 24 24" aria-hidden="true"
			><path d="M12 21s-7-6.3-7-11.5A7 7 0 0 1 19 9.5C19 14.7 12 21 12 21Z" /><circle cx="12" cy="9.5" r="2.5" /></svg
		><span id="pc-text">{area?.place ? `${area.place} · ${zip}` : zip}</span>
	</p>
	<MapSearch {view} />
	<div class="callwrap" id="callwrap" hidden={phase !== 'ready'}>
		<h2 id="n-title">{town ? `Scoo is coming to ${town}` : 'Scoo is coming to your area'}</h2>
		<p class="lead" id="n-lead">
			Get on the early list and be first to get a pro when we open.{waiting >= 25
				? ` Join ${waiting.toLocaleString()} neighbours already waiting.`
				: ''}
		</p>
		<form class="stack" id="f-phone" bind:this={form} onsubmit={save}>
			<label class="vh" for="tel">Mobile number or email</label><input
				id="tel"
				type="text"
				autocomplete="on"
				autocapitalize="off"
				spellcheck="false"
				placeholder="Mobile number or email"
				required
				bind:this={tel}
				bind:value={contact}
			/>
			<label class="consent"
				><input type="checkbox" id="ok" required bind:checked={ok} /><span bind:this={consent}
					>I agree to Scoo's <a href="/terms" target="_blank" rel="noopener">terms</a>. No spam. Unsubscribe anytime.</span
				></label
			>
			<div id="ts" bind:this={tsEl}></div>
			<button class="primary" id="save" disabled={saving || !ready}>{saving ? 'Saving…' : 'Save my spot'}</button>
			{#if error}<p class="err" role="alert">{error}</p>{/if}
		</form>
	</div>
</div>

<style>
	/* A wrapper for the notify state only: the section's flex layout reaches straight through it. */
	.phone {
		display: contents;
	}
	.phone .art {
		width: min(300px, 80vw);
		transition: width 0.75s cubic-bezier(0.3, 0.8, 0.3, 1);
	}
	.phone.notify .art {
		width: 132px;
	}

	/* The map, drawn into the {@html} above, so its parts are reached with :global. These must beat
	   the page's generic line-art rules for the same elements, hence the extra .phone. */
	.phone .art :global(.map .road) {
		stroke: var(--ink);
		stroke-width: 7;
		opacity: 0.14;
	}
	.phone .art :global(.map .lane) {
		stroke: var(--ink);
		stroke-width: 2;
		opacity: 0.12;
	}
	.phone .art :global(.map .water) {
		stroke: #9ec9ff;
		stroke-width: 12;
		opacity: 0.55;
	}
	.phone .art :global(.map .park) {
		fill: #dcefd9;
		stroke: none;
	}
	.phone .art :global(.map .tree-dot) {
		stroke: #7bb37a;
		stroke-width: 9;
	}
	.phone .art :global(.map .blk) {
		fill: var(--bg);
		stroke: var(--ink);
		stroke-width: 1.5;
		opacity: 0.55;
	}
	.phone .art :global(.map .frame) {
		fill: none;
		stroke: var(--ink);
		stroke-width: 2.2;
	}
	.phone .art :global(.map .zoom) {
		transform-box: view-box;
		transform-origin: 180px 90px;
		animation: zoomin 2.6s cubic-bezier(0.3, 0.7, 0.2, 1) both;
	}
	.phone .art :global(.map .pin) {
		animation: rq-pin 0.7s 1.6s cubic-bezier(0.3, 0.8, 0.3, 1.4) both;
	}
	.phone .art :global(.map .ring) {
		stroke: var(--accent);
		stroke-width: 2;
		vector-effect: non-scaling-stroke;
		transform-box: fill-box;
		transform-origin: center;
		animation: radar 2.4s ease-out infinite;
		animation-delay: calc(1.9s + var(--i) * 0.8s);
		opacity: 0;
	}
	.phone .art :global(.map .sweep) {
		transform-box: view-box;
		transform-origin: 180px 104px;
		animation: sweep 2.2s linear infinite;
		animation-delay: 0.3s;
	}
	.phone .art :global(.map .beam) {
		fill: var(--accent);
		stroke: none;
		opacity: 0.12;
	}
	@keyframes zoomin {
		from {
			transform: scale(0.55) translate(-40px, 30px);
		}
		to {
			transform: scale(1.15);
		}
	}
	/* The radar's rings. The old page named this "ring" a second time, which silently replaced a
	   phone-wobble keyframe of the same name; it has a name of its own here. */
	@keyframes radar {
		0% {
			transform: scale(1);
			opacity: 0.9;
		}
		100% {
			transform: scale(8);
			opacity: 0;
		}
	}
	@keyframes sweep {
		to {
			transform: rotate(360deg);
		}
	}

	.placechip {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		margin: -4px 0 0;
		padding: 6px 12px;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		font-size: 14px;
		font-weight: 500;
		animation: rq-pop 0.45s cubic-bezier(0.3, 0.8, 0.3, 1.3) both;
	}
	.placechip[hidden] {
		display: none;
	}
	.placechip svg {
		width: 16px;
		height: 16px;
		fill: var(--accent);
		stroke: var(--ink);
		stroke-width: 1.6;
	}
	.placechip circle {
		fill: var(--bg);
	}

	.callwrap {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 12px;
		animation: rise 0.55s cubic-bezier(0.3, 0.8, 0.3, 1) both;
	}
	.callwrap[hidden] {
		display: none;
	}
	.callwrap h2 {
		margin: 0;
		font-size: clamp(30px, 5vw, 40px);
		font-weight: 400;
		letter-spacing: -0.03em;
	}
	@keyframes rise {
		from {
			opacity: 0;
			transform: translateY(18px);
		}
	}

	.stack {
		display: flex;
		flex-direction: column;
		gap: 12px;
		width: 100%;
		text-align: left;
	}
	.stack #tel {
		min-height: 54px;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 0 20px;
		font: 400 18px 'Hanken Grotesk', sans-serif;
		background: var(--bg);
		color: var(--ink);
	}
	.consent a {
		color: inherit;
	}
	.consent {
		display: flex;
		gap: 10px;
		font-size: 14px;
		color: var(--muted);
		line-height: 1.45;
	}
	.consent input {
		width: 20px;
		height: 20px;
		margin-top: 1px;
		accent-color: var(--accent);
		flex: 0 0 auto;
	}
	.err {
		margin: 0;
		color: #c0392b;
		font-size: 14px;
	}
</style>
