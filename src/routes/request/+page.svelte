<!-- The request flow: one step per screen, each with a line-art illustration in the same style as
     the street. Pre-launch, so it ends on the city waitlist and referrals rather than a call.
     need → ZIP → one question → the area lookup, which becomes the contact form → done. -->
<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { page } from '$app/state';
	import Mark from '#lib/brand/Mark.svelte';
	import FieldForm from '#lib/request/FieldForm.svelte';
	import AskStep from '#lib/request/AskStep.svelte';
	import NotifyStep from '#lib/request/NotifyStep.svelte';
	import DoneStep from '#lib/request/DoneStep.svelte';
	import { ART_NEED, ART_ZIP } from '#lib/request/art.ts';
	import {
		ORDER,
		QUESTIONS,
		DEMO_AREA,
		classify,
		wait,
		type Step,
		type Need,
		type Area,
		type Joined,
		type SearchView,
		type Phase
	} from '#lib/request/flow.ts';

	/** Where the flow is. Only the last step carries data of its own: the saved request. */
	type Screen = { step: Exclude<Step, 'done'> } | { step: 'done'; joined: Joined };

	const ENTER = (fwd: boolean) => `rq-${fwd ? 'inR' : 'inL'} .42s cubic-bezier(.3,.8,.3,1)`;

	let screen = $state<Screen>({ step: 'need' });
	const cur = $derived(ORDER.indexOf(screen.step));
	// The step on screen lags `screen` while the old one slides out.
	let shown = $state<Step>('need');
	let anim = $state(ENTER(true));
	let reduceMotion = false;
	const sections: Partial<Record<Step, HTMLElement>> = {};

	let needText = $state('');
	let zipText = $state('');
	let needForm = $state<HTMLFormElement>();
	let zipForm = $state<HTMLFormElement>();
	let notify = $state<ReturnType<typeof NotifyStep>>();

	let need: Need | null = null;
	let zip = $state('');
	let zipLead = $state("We'll find a pro near you.");
	let question = $state<[string, string[]]>(['', []]);
	let emergency = $state(false);
	let answer: string | null = null;

	let area = $state<Area | null>(null);
	let searchedZip: string | null = null;
	let skipSearch = false;
	let searching = $state(false);
	let phase = $state<Phase>('search');
	let view = $state<SearchView>({ title: 'Looking up your area…', marks: ['', '', ''], zip: '', place: null, pros: '', launch: '' });

	const backDisabled = $derived(cur === 0 || cur === ORDER.length - 1 || searching);
	const joined = $derived(screen.step === 'done' ? screen.joined : null);

	function show(next: Screen) {
		const fwd = ORDER.indexOf(next.step) >= cur;
		const prev = shown;
		const target = next.step;
		screen = next;
		const enter = async () => {
			shown = target;
			anim = reduceMotion ? '' : ENTER(fwd);
			scrollTo(0, 0);
			await tick();
			const f = sections[target]?.querySelector<HTMLInputElement>('input:not([hidden])');
			if (f && f.offsetParent) setTimeout(() => f.focus({ preventScroll: true }), 380);
		};
		if (prev !== target && !reduceMotion) {
			anim = `rq-${fwd ? 'outL' : 'outR'} .2s ease-in forwards`;
			setTimeout(enter, 190);
		} else enter();
	}

	const back = () => show({ step: ORDER[Math.max(0, cur - 1)] as Exclude<Step, 'done'> });

	function submitNeed() {
		const text = needText.trim();
		if (!text) return;
		need = classify(text);
		zipLead = `We'll find ${need.noun} near you.`;
		show({ step: 'zip' });
	}

	function submitZip() {
		const z = zipText.trim();
		if (!/^\d{5}$/.test(z) || !need) return;
		zip = z;
		question = QUESTIONS[need.cat];
		emergency = false;
		show({ step: 'q' });
	}

	function pick(choice: string) {
		answer = choice;
		if (need?.cat === 'doctor' && choice === 'Yes') {
			emergency = true;
			return;
		}
		callScreen();
	}

	// The "searching" screen between the question and the contact form. It runs while the real
	// lookup does, and every line it shows is true: the area comes from the API, and while Scoo is
	// not live it says so rather than pretending to have found pros.
	async function search(z: string) {
		view = {
			title: 'Looking up your area…',
			marks: ['', '', ''],
			zip: z,
			place: null,
			pros: `Checking Scoo coverage in ${z}`,
			launch: 'Checking when Scoo opens near you'
		};
		const lookup: Promise<Partial<Area> | null> = fetch('/api/city?zip=' + z)
			.then((r) => r.json() as Promise<Partial<Area>>)
			.catch(() => null);
		const step = async (i: 0 | 1 | 2, ms: number) => {
			view.marks[i] = 'run';
			await wait(ms);
			view.marks[i] = 'ok';
		};
		await step(0, 1100);
		const c = await lookup;
		const a: Area = {
			city: c?.city || 'your area',
			place: c?.place || null,
			town: c?.town || null,
			areaLabel: c?.areaLabel || 'your area',
			waiting: c?.waiting || 0
		};
		area = a;
		view.place = a.place;
		view.title = a.place ? `Found you in ${a.place}` : 'Found your area';
		await step(1, 1200);
		view.launch =
			a.waiting >= 25
				? `${a.waiting.toLocaleString()} neighbours already waiting in ${a.areaLabel}`
				: a.town
					? `Scoo is coming to ${a.town}`
					: 'Scoo is coming to your area';
		await step(2, 1000);
		await wait(650);
	}

	// The search runs once per ZIP; coming back to this screen shows its result straight away.
	async function callScreen() {
		if (searching) return;
		show({ step: 'phone' });
		if (searchedZip !== zip && !skipSearch) {
			phase = 'search';
			searching = true;
			await wait(220);
			await search(zip);
			searchedZip = zip;
			searching = false;
			phase = 'found';
			await wait(reduceMotion ? 0 : 520);
		} else {
			if (searchedZip !== zip) {
				area = area ?? DEMO_AREA;
				searchedZip = zip;
			}
			phase = 'found';
		}
		phase = 'ready';
		setTimeout(() => notify?.focusContact(), 450);
	}

	const body = () => ({ need: need?.text ?? '', category: need?.cat ?? 'pro', answer: answer || null, zip });

	const done = (j: Joined) => show({ step: 'done', joined: j });

	onMount(() => {
		reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
		const params = page.url.searchParams;
		// An invite link (/r/CODE) lands with ?ref; it is sent with the request whenever that is.
		try {
			const rf = params.get('ref');
			if (rf) localStorage.setItem('scoo_ref', rf);
		} catch {
			// storage blocked: no referral, nothing else lost
		}
		(async () => {
			// The homepage hands over what was typed there as ?q, so the flow starts at the ZIP.
			const q = params.get('q');
			if (q) {
				needText = q;
				await tick();
				needForm?.requestSubmit();
			} else show({ step: 'need' });
			// ?step=N jumps for screenshots, with a plumber in Plano and no lookup.
			const step = Number(params.get('step') || 0);
			if (!step) return;
			skipSearch = true;
			need ??= { text: 'My water heater is leaking', cat: 'plumber', noun: 'a plumber' };
			zipText = '75201';
			await tick();
			if (step === 1) show({ step: 'zip' });
			if (step >= 2) zipForm?.requestSubmit();
			if (step >= 3) callScreen();
			if (step >= 4) {
				await tick();
				notify?.demoSubmit('(214) 555-0142');
			}
		})();
	});
</script>

<svelte:head>
	<title>Tell Scoo what you need</title>
</svelte:head>

<div class="rq">
	<header>
		<a class="logo" href="/" aria-label="Scoo home"><Mark /><span>scoo</span></a><button
			class="back"
			id="back"
			type="button"
			disabled={backDisabled}
			onclick={back}>Back</button
		>
	</header>
	<div class="dots" aria-hidden="true">
		{#each ORDER as s, k (s)}<i class:on={k <= cur}></i>{/each}
	</div>
	<main aria-live="polite">
		<section class="step" data-step="need" hidden={shown !== 'need'} style:animation={shown === 'need' ? anim : null} bind:this={sections.need}>
			<div class="art">{@html ART_NEED}</div>
			<h1>What do you need?</h1>
			<p class="lead">Describe it in your own words. A leaking pipe, a car insurance quote, a lawyer by Friday.</p>
			<FieldForm
				id="need"
				label="What do you need?"
				bind:value={needText}
				bind:form={needForm}
				onsubmit={submitNeed}
				autocomplete="off"
				placeholder="My water heater is leaking…"
				required
			/>
		</section>
		<section class="step" data-step="zip" hidden={shown !== 'zip'} style:animation={shown === 'zip' ? anim : null} bind:this={sections.zip}>
			<div class="art">{@html ART_ZIP}</div>
			<h1>Where are you?</h1>
			<p class="lead" id="zip-lead">{zipLead}</p>
			<FieldForm
				id="zip"
				label="ZIP code"
				bind:value={zipText}
				bind:form={zipForm}
				onsubmit={submitZip}
				inputmode="numeric"
				autocomplete="postal-code"
				maxlength={5}
				placeholder="ZIP code"
				required
				pattern={'[0-9]{5}'}
			/>
		</section>
		<section class="step" data-step="q" hidden={shown !== 'q'} style:animation={shown === 'q' ? anim : null} bind:this={sections.q}>
			<AskStep title={question[0]} choices={question[1]} {emergency} onpick={pick} />
		</section>
		<section class="step" data-step="phone" hidden={shown !== 'phone'} style:animation={shown === 'phone' ? anim : null} bind:this={sections.phone}>
			<NotifyStep bind:this={notify} {phase} {view} {zip} {area} {body} onjoined={done} />
		</section>
		<section class="step" data-step="done" hidden={shown !== 'done'} style:animation={shown === 'done' ? anim : null} bind:this={sections.done}>
			{#if joined}<DoneStep {joined} />{/if}
		</section>
	</main>
</div>

<style>
	header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 20px clamp(16px, 4vw, 48px);
		max-width: 1200px;
		margin: 0 auto;
	}
	.logo {
		display: inline-flex;
		align-items: center;
		gap: 10px;
		color: var(--ink);
		text-decoration: none;
		font-size: 26px;
		letter-spacing: -0.02em;
	}
	.logo :global(.mark) {
		height: 36px;
		width: auto;
		color: var(--ink);
	}
	.back {
		min-height: 44px;
		padding: 0 16px;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		background: var(--bg);
		color: var(--ink);
		font: 500 15px inherit;
		cursor: pointer;
		font-family: inherit;
	}
	.back[disabled] {
		visibility: hidden;
	}
	.dots {
		display: flex;
		gap: 8px;
		justify-content: center;
		margin: 4px 0 0;
	}
	.dots i {
		width: 28px;
		height: 4px;
		border-radius: 99px;
		background: var(--line);
		transition: background 0.3s;
	}
	.dots i.on {
		background: var(--accent);
	}
	main {
		max-width: 560px;
		margin: 0 auto;
		padding: 12px 20px 48px;
	}
	.step {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		gap: 16px;
		animation: rq-in 0.45s cubic-bezier(0.3, 0.8, 0.3, 1);
	}
	.step[hidden] {
		display: none;
	}

	/* What every step shares, including what its components render: global under .rq so it
	   reaches into them and no further. */
	.rq :global(h1) {
		margin: 4px 0 0;
		font-weight: 300;
		font-size: clamp(32px, 5vw, 46px);
		letter-spacing: -0.03em;
		line-height: 1.05;
	}
	.rq :global(.lead) {
		margin: 0;
		color: var(--muted);
		font-size: 17px;
		line-height: 1.5;
		max-width: 440px;
	}
	.rq :global(.primary) {
		min-height: 54px;
		border: 0;
		border-radius: 999px;
		background: var(--accent);
		color: #fff;
		font: 600 17px 'Hanken Grotesk', sans-serif;
		cursor: pointer;
	}
	.rq :global(.primary:disabled) {
		opacity: 0.4;
		cursor: not-allowed;
	}
	.rq :global(.fine) {
		margin: 0;
		font-size: 12px;
		color: var(--muted);
		text-align: left;
		width: 100%;
	}
	.rq :global(.art) {
		width: min(340px, 86vw);
	}

	/* The line-art: ink strokes with coral and soft fills, drawn into each step with {@html}. The
	   winged pros on the done screen bring their own classes (wing, wingp, skin…), styled here. */
	.rq :global(.ill) {
		width: 100%;
		height: auto;
		overflow: visible;
	}
	.rq :global(.ill *) {
		fill: none;
		stroke: var(--ink);
		stroke-width: 2.2;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.rq :global(.ill .soft),
	.rq :global(.ill .wingp) {
		fill: var(--soft);
	}
	.rq :global(.ill .accent) {
		fill: var(--accent);
		stroke: var(--ink);
	}
	.rq :global(.ill .paper),
	.rq :global(.ill .fillbg),
	.rq :global(.ill .skin),
	.rq :global(.ill .mouth) {
		fill: var(--bg);
	}
	.rq :global(.ill .lit) {
		fill: var(--glow);
	}
	.rq :global(.ill .yellow) {
		fill: #ffc93d;
	}
	.rq :global(.ill .blue) {
		fill: #7fb2ff;
	}
	.rq :global(.ill .shades) {
		fill: var(--ink);
	}
	.rq :global(.ill .eyes) {
		stroke-width: 4;
	}
	.rq :global(.ill .cross) {
		stroke: var(--accent);
		stroke-width: 3;
	}
	.rq :global(.ill .band) {
		stroke: var(--accent);
		stroke-width: 5;
	}
	.rq :global(.ill .thick) {
		stroke-width: 5;
	}
	.rq :global(.ill .dash) {
		stroke-dasharray: 14 14;
	}
	.rq :global(.ill .shadow) {
		fill: var(--line);
		stroke: none;
		animation: rq-shadow 0.9s ease-out both;
	}
	.rq :global(.ill .glow) {
		fill: var(--glow);
	}
	.rq :global(.ill .accent-line),
	.rq :global(.ill .paper-line),
	.rq :global(.ill .spark),
	.rq :global(.ill .rain) {
		stroke: var(--accent);
	}
	.rq :global(.ill .water) {
		stroke: #7fb2ff;
		stroke-width: 3;
	}
	.rq :global(.ill .drop) {
		fill: #9ec9ff;
		animation: rq-drip 1.4s ease-in infinite;
		animation-delay: calc(var(--i, 0) * 0.7s);
	}
	.rq :global(.ill text) {
		stroke: none;
		fill: var(--ink);
		font: 600 14px 'Hanken Grotesk', sans-serif;
	}
	.rq :global(.ill .signtxt) {
		stroke: none;
		fill: var(--accent);
		font: 700 12px 'Hanken Grotesk', sans-serif;
	}
	.rq :global(.ill .wing) {
		transform-box: fill-box;
		animation: rq-flap 0.3s ease-in-out infinite alternate;
	}
	.rq :global(.ill .wl) {
		transform-origin: 100% 50%;
	}
	.rq :global(.ill .wr) {
		transform-origin: 0% 50%;
		animation-name: rq-flapr;
	}
	.rq :global(.ill .pop) {
		animation: rq-pop 0.5s cubic-bezier(0.3, 0.8, 0.3, 1.3) both;
		animation-delay: calc(0.25s + var(--i) * 0.45s);
	}
	.rq :global(.ill .dot) {
		fill: var(--ink);
		stroke: none;
		animation: rq-blink 1s infinite;
		animation-delay: calc(var(--i, 0) * 0.15s);
	}
	.rq :global(.ill .pin) {
		animation: rq-pin 0.9s cubic-bezier(0.3, 0.8, 0.3, 1.4) both;
	}
	.rq :global(.ill .row) {
		animation: rq-pop 0.4s cubic-bezier(0.3, 0.8, 0.3, 1.3) both;
		animation-delay: calc(0.2s + var(--i) * 0.35s);
	}
	.rq :global(.ill .tick) {
		stroke: var(--accent);
		stroke-width: 3;
		stroke-dasharray: 24;
		stroke-dashoffset: 24;
		animation: rq-tick 0.4s ease-out forwards;
		animation-delay: calc(1.2s + var(--i, 0) * 0.5s);
	}
	.rq :global(.ill .row:nth-of-type(2) .tick) {
		animation-delay: 1.7s;
	}
	.rq :global(.ill .pencil) {
		animation: rq-write 1.6s ease-in-out infinite;
		transform-box: fill-box;
		transform-origin: 0 100%;
	}
	.rq :global(.ill .wave) {
		animation: rq-hop 1.6s ease-in-out infinite;
		transform-box: fill-box;
		transform-origin: 50% 100%;
	}
	.rq :global(.ill .bubble-s) {
		animation: rq-pop 0.5s 0.5s cubic-bezier(0.3, 0.8, 0.3, 1.3) both;
	}

	/* Global names: the steps' inline slide animations and the components use them too. */
	@keyframes -global-rq-in {
		from {
			opacity: 0;
			transform: translateY(14px);
		}
	}
	@keyframes -global-rq-inR {
		from {
			opacity: 0;
			transform: translateX(32px);
		}
	}
	@keyframes -global-rq-inL {
		from {
			opacity: 0;
			transform: translateX(-32px);
		}
	}
	@keyframes -global-rq-outL {
		to {
			opacity: 0;
			transform: translateX(-32px);
		}
	}
	@keyframes -global-rq-outR {
		to {
			opacity: 0;
			transform: translateX(32px);
		}
	}
	@keyframes -global-rq-pop {
		from {
			opacity: 0;
			transform: scale(0.6);
		}
	}
	@keyframes -global-rq-pin {
		from {
			transform: translateY(-60px);
			opacity: 0;
		}
	}
	@keyframes -global-rq-shadow {
		from {
			opacity: 0;
			transform: scale(0.3);
		}
	}
	@keyframes -global-rq-tick {
		to {
			stroke-dashoffset: 0;
		}
	}
	@keyframes -global-rq-write {
		50% {
			transform: translate(-6px, 4px) rotate(-4deg);
		}
	}
	@keyframes -global-rq-flap {
		to {
			transform: rotate(-16deg) scaleY(0.85);
		}
	}
	@keyframes -global-rq-flapr {
		to {
			transform: rotate(16deg) scaleY(0.85);
		}
	}
	@keyframes -global-rq-blink {
		50% {
			opacity: 0.2;
		}
	}
	@keyframes -global-rq-drip {
		0% {
			transform: translateY(0);
			opacity: 0;
		}
		20% {
			opacity: 1;
		}
		100% {
			transform: translateY(46px);
			opacity: 0;
		}
	}
	@keyframes -global-rq-hop {
		50% {
			transform: translateY(-8px);
		}
	}
</style>
