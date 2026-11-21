<script lang="ts">
	import { onMount } from 'svelte';
	import Mark from '#lib/brand/Mark.svelte';
	import street from '#lib/art/street.svg?raw';
	import { startStreet, type Street } from '#lib/home/fallers.ts';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	// The headline's rotating word, and the pro on the street who hops when it names their trade.
	const WORDS: [string, string | null][] = [
		['an expert', null],
		['a plumber', 'plumber'],
		['a lawyer', 'lawyer'],
		['an electrician', 'electrician'],
		['a doctor', 'doctor'],
		['an insurance agent', 'insurance'],
		['movers', 'mover']
	];
	// Example requests cycled through the empty search box.
	const EXAMPLES = [
		'My AC just died…',
		'Need a lawyer by Friday…',
		'Cheaper car insurance…',
		'Someone to move a sofa…',
		'Help losing weight…',
		'A plumber, now…'
	];

	let word = $state(WORDS[0][0]);
	let leaving = $state(false);
	let entered = $state(false);
	let rotWidth = $state<string>();
	let need = $state('');
	let placeholder = $state(EXAMPLES[0]);

	let hero: HTMLElement;
	let sky: HTMLDivElement;
	let streetBox: HTMLDivElement;
	let form: HTMLFormElement;
	let input: HTMLInputElement;
	let rot: HTMLSpanElement;
	let meas: HTMLSpanElement;

	// The search box hands what was typed to the request page, which carries on from there. A full
	// navigation, as before: the request page starts its own flow from ?q. Without JS the form's own
	// GET to /request does the same.
	function ask(e: SubmitEvent) {
		e.preventDefault();
		const v = need.trim();
		location.assign('/request' + (v ? '?q=' + encodeURIComponent(v) : ''));
	}

	onMount(() => {
		const params = new URLSearchParams(location.search);
		try {
			const rf = params.get('ref');
			if (rf) localStorage.setItem('scoo_ref', rf);
		} catch {
			// storage blocked (private mode): the invite is lost, the page still works
		}

		const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
		const fast = /fast/.test(location.search) ? 8 : 1;
		const timers: ReturnType<typeof setInterval>[] = [];
		let st: Street | undefined;
		let i = 0;
		let gone = false;

		// The word's box animates its width, so it is sized to the text measured in the word's own font.
		const fit = (t: string) => {
			if (reduce) return;
			const cs = getComputedStyle(rot);
			meas.style.font = cs.font;
			meas.style.letterSpacing = cs.letterSpacing;
			meas.style.fontVariationSettings = cs.fontVariationSettings;
			meas.textContent = t;
			rotWidth = meas.getBoundingClientRect().width + 'px';
		};
		const refit = () => {
			if (gone) return;
			fit(WORDS[i][0]);
			st?.layout();
		};
		fit(WORDS[0][0]);
		addEventListener('resize', refit);
		// Re-measure once Hanken Grotesk has actually arrived: until then the browser lays the headline
		// out in a narrower fallback font, and a width measured then clips the word.
		if (document.fonts) {
			document.fonts.addEventListener('loadingdone', refit);
			document.fonts.load('300 64px "Hanken Grotesk"').then(refit, refit);
			document.fonts.load('400 64px "Hanken Grotesk"').then(refit, refit);
			document.fonts.ready.then(refit);
		}

		// The street measures its doors and the search box, so it starts once the page has loaded.
		const begin = () => {
			if (gone) return;
			const scene = streetBox.querySelector('svg.scene');
			if (scene instanceof SVGSVGElement) st = startStreet(sky, hero, scene, form, { fast, reduce });
			refit();
		};
		if (document.readyState === 'complete') begin();
		else addEventListener('load', begin, { once: true });

		if (!reduce) {
			timers.push(
				setInterval(() => {
					i = (i + 1) % WORDS.length;
					const [t, name] = WORDS[i];
					leaving = true;
					setTimeout(() => {
						if (gone) return;
						word = t;
						leaving = false;
						entered = true;
						fit(t);
					}, 300);
					if (name) st?.hop(name);
				}, 2200)
			);
			let ei = 0;
			timers.push(
				setInterval(() => {
					if (document.activeElement !== input && !need) {
						ei = (ei + 1) % EXAMPLES.length;
						placeholder = EXAMPLES[ei];
					}
				}, 2600)
			);
		}

		// scripted walk-through for recordings: ?demo types a request and hands it off
		if (/[?&]demo/.test(location.search)) {
			const wait = (ms: number) => new Promise((r) => setTimeout(r, ms));
			(async () => {
				await wait(6500);
				input.focus();
				for (const ch of 'My water heater is leaking') {
					if (gone) return;
					need += ch;
					await wait(55);
				}
				await wait(400);
				if (!gone) form.requestSubmit();
			})();
		}

		return () => {
			gone = true;
			timers.forEach(clearInterval);
			removeEventListener('resize', refit);
			removeEventListener('load', begin);
			document.fonts?.removeEventListener('loadingdone', refit);
			st?.destroy();
		};
	});
</script>

<svelte:head>
	<title>Scoo: get an expert in 60 seconds</title>
	<meta
		name="description"
		content="Plumbers, lawyers, insurance, health and more. Tell Scoo what you need and the right pro calls you back. Launching city by city."
	/>
</svelte:head>

<div class="home">
	<section class="hero" bind:this={hero}>
		<nav aria-label="Main">
			<a class="logo" href="/" aria-label="Scoo home"><Mark /><span>scoo</span></a>
			<div class="navlinks"><a class="pill" href="/pros">I'm a pro</a></div>
		</nav>
		<div class="copy">
			<p class="badge">
				<i></i>{data.town ? `Coming soon to ${data.town}` : 'Launching city by city'}
			</p>
			<h1 aria-label="Get an expert in 60 seconds">
				Get <span class="rot" aria-hidden="true" bind:this={rot} style:width={rotWidth}
					>{#key word}<span class="w" class:in={entered} class:out={leaving}>{word}</span>{/key}</span
				><br aria-hidden="true" /><span class="tail" aria-hidden="true">in 60 seconds.</span><span
					class="meas"
					aria-hidden="true"
					bind:this={meas}
				></span>
			</h1>
			<form class="ask" role="search" action="/request" bind:this={form} onsubmit={ask}>
				<label for="need" class="vh">What do you need?</label>
				<input id="need" name="q" type="text" autocomplete="off" {placeholder} bind:value={need} bind:this={input} />
				<button type="button" class="mic" aria-label="Speak instead"
					><svg viewBox="0 0 24 24" aria-hidden="true"
						><rect x="9" y="3" width="6" height="11" rx="3" /><path d="M5 11a7 7 0 0 0 14 0M12 18v3" /></svg
					></button
				>
				<button type="submit" class="go" aria-label="Ask Scoo"
					><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" /></svg></button
				>
			</form>
		</div>
		<div class="street" bind:this={streetBox}>{@html street}</div>
		<div class="sky" aria-hidden="true" bind:this={sky}></div>
	</section>
</div>

<style>
	/* The homepage's muted grey is a touch darker (light) and lighter (dark) than the site's. */
	.home {
		--muted: #555555;
	}
	@media (prefers-color-scheme: dark) {
		:global(:root:not([data-theme='light'])) .home {
			--muted: #b5b5b5;
		}
	}
	:global(:root[data-theme='dark']) .home {
		--muted: #b5b5b5;
	}

	.hero {
		position: relative;
		height: 100vh;
		height: 100dvh;
		min-height: 560px;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		color: var(--ink);
	}
	nav {
		position: relative;
		z-index: 3;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 20px clamp(16px, 4vw, 48px);
	}
	.logo {
		display: inline-flex;
		align-items: center;
		gap: 10px;
		font-size: 28px;
		color: var(--ink);
		text-decoration: none;
	}
	.logo span {
		font-weight: 400;
		letter-spacing: -0.02em;
	}
	.logo :global(.mark) {
		height: 42px;
		width: auto;
		color: var(--ink);
	}
	.navlinks {
		display: flex;
		gap: 24px;
		align-items: center;
		font-size: 15px;
	}
	.pill {
		color: var(--ink);
		text-decoration: none;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 9px 18px;
		font-weight: 500;
	}

	.copy {
		position: relative;
		z-index: 3;
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: center;
		gap: 26px;
		padding: 16px 20px;
		opacity: 0;
		animation: fade 0.8s ease-out forwards 0.2s;
	}
	.badge {
		/* the original kept a paragraph's default margins, and the layout is balanced around them */
		margin: 1em 0;
		display: inline-flex;
		align-items: center;
		gap: 8px;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 7px 14px;
		font-size: 14px;
		font-weight: 500;
	}
	.badge i {
		width: 8px;
		height: 8px;
		border-radius: 99px;
		background: var(--accent);
		animation: pulse 1.6s ease-in-out infinite;
	}

	h1 {
		margin: 0;
		font-weight: 300;
		font-size: clamp(44px, 6vw, 92px);
		line-height: 1.02;
		letter-spacing: -0.035em;
	}
	.rot {
		/* the measured width is the text's; the padding is extra room for the last glyph's overhang */
		box-sizing: content-box;
		display: inline-block;
		position: relative;
		vertical-align: bottom;
		overflow: hidden;
		color: var(--accent);
		font-weight: 400;
		transition: width 0.45s cubic-bezier(0.3, 0.8, 0.3, 1);
		white-space: nowrap;
		padding: 0 0.14em 0.08em 0;
		margin: 0 -0.1em -0.08em 0;
	}
	.w {
		display: inline-block;
	}
	.w.out {
		animation: wout 0.35s ease-in forwards;
	}
	.w.in {
		animation: win 0.45s cubic-bezier(0.3, 0.8, 0.3, 1.2);
	}
	.tail {
		color: var(--ink);
	}
	.meas {
		position: absolute;
		visibility: hidden;
		white-space: nowrap;
	}

	.ask {
		/* sized as the original: 640px of field plus its padding and border */
		box-sizing: content-box;
		display: flex;
		align-items: center;
		gap: 6px;
		width: min(640px, 100%);
		background: var(--bg);
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 6px 6px 6px 22px;
		margin-top: 8px;
	}
	.ask:focus-within {
		border-color: var(--accent);
		box-shadow: 0 0 0 4px var(--soft);
	}
	.ask input {
		flex: 1;
		min-width: 0;
		border: 0;
		outline: 0;
		background: transparent;
		font: 500 18px var(--font);
		color: var(--ink);
		min-height: 48px;
	}
	.ask input::placeholder {
		color: var(--muted);
	}
	.ask button {
		display: grid;
		place-items: center;
		width: 48px;
		height: 48px;
		border-radius: 999px;
		border: 0;
		cursor: pointer;
		background: transparent;
		color: var(--ink);
	}
	.ask .go {
		background: var(--accent);
		color: #fff;
	}
	.ask svg {
		width: 22px;
		height: 22px;
		fill: none;
		stroke: currentColor;
		stroke-width: 2.2;
		stroke-linecap: round;
		stroke-linejoin: round;
	}

	/* The street drawing is injected markup, so its rules are global under .street. Each element draws
	   itself in with a dash animation, staggered by its own --d. */
	.street {
		position: relative;
		z-index: 1;
		flex-shrink: 0;
		display: flex;
		justify-content: center;
	}
	.street :global(.scene) {
		flex-shrink: 0;
		width: max(100%, 900px);
		height: auto;
		max-height: 46vh;
		display: block;
	}
	.street :global(.scene *) {
		fill: var(--bg);
		stroke: var(--ink);
		stroke-width: 2;
		stroke-linecap: round;
		stroke-linejoin: round;
		stroke-dasharray: 1;
		stroke-dashoffset: 1;
		animation: draw 1.1s ease-out forwards;
		animation-delay: var(--d);
	}
	.street :global(.scene line) {
		fill: none;
	}
	.street :global(.win.lit) {
		animation:
			draw 1.1s ease-out forwards var(--d),
			glow 0.8s ease-out forwards calc(var(--d) + 2.6s);
	}
	.street :global(.cloud) {
		animation:
			draw 1.1s ease-out forwards var(--d),
			drift 18s ease-in-out infinite alternate calc(var(--d) + 1s);
	}
	.street :global(.scene text) {
		stroke: none;
		fill: var(--ink);
		font-family: var(--font);
		font-weight: 500;
		letter-spacing: 0.14em;
		opacity: 0;
		animation: fade 0.6s forwards;
		animation-delay: calc(var(--d) + 0.8s);
	}
	.street :global(.flower) {
		fill: var(--accent);
	}
	.street :global(.pole),
	.street :global(.spine),
	.street :global(.awn) {
		fill: var(--soft);
	}
	.street :global(.leaf) {
		fill: var(--leaf);
	}
	.street :global(.smoke) {
		fill: none;
		animation:
			draw 1s forwards var(--d),
			rise 3s ease-in-out infinite calc(var(--d) + 1s);
	}
	@media (max-width: 640px) {
		.street :global(.scene) {
			width: 1250px;
			max-height: none;
		}
	}
	/* app.css stops every animation here, so whatever an animation would have revealed is shown outright */
	@media (prefers-reduced-motion: reduce) {
		.copy,
		.street :global(.scene text) {
			opacity: 1;
		}
		.street :global(.scene *) {
			stroke-dashoffset: 0;
		}
		.street :global(.win.lit) {
			fill: var(--glow);
		}
	}

	/* The falling pros, created by #lib/home/fallers.ts. */
	.sky {
		position: absolute;
		inset: 0;
		pointer-events: none;
		overflow: hidden;
		z-index: 2;
	}
	.sky :global(.faller) {
		position: absolute;
		left: 0;
		top: 0;
		width: var(--pw);
		will-change: transform;
		opacity: 0;
		transition: opacity 0.5s ease-out;
	}
	.sky :global(.faller.on) {
		opacity: 1;
	}
	.sky :global(.faller svg) {
		width: 100%;
		height: auto;
		overflow: visible;
		display: block;
	}
	.sky :global(.faller svg *) {
		fill: none;
		stroke: var(--ink);
		stroke-width: 2.4;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.sky :global(.faller .fillbg) {
		fill: var(--bg);
	}
	.sky :global(.faller .wingp),
	.sky :global(.faller .soft) {
		fill: var(--soft);
	}
	.sky :global(.faller .accent) {
		fill: var(--accent);
	}
	.sky :global(.faller .yellow) {
		fill: #ffc93d;
	}
	.sky :global(.faller .blue) {
		fill: #7fb2ff;
	}
	.sky :global(.faller .drop) {
		fill: #9ec9ff;
		stroke-width: 1.5;
	}
	.sky :global(.faller .eyes) {
		stroke-width: 4;
	}
	.sky :global(.faller .mouth) {
		fill: var(--bg);
	}
	.sky :global(.faller .shades) {
		fill: var(--ink);
	}
	.sky :global(.faller .cross) {
		stroke: var(--accent);
		stroke-width: 3;
	}
	.sky :global(.faller .band) {
		stroke: var(--accent);
		stroke-width: 5;
	}
	.sky :global(.faller .thick) {
		stroke-width: 5;
	}
	.sky :global(.faller .signtxt) {
		stroke: none;
		fill: var(--accent);
		font: 700 12px var(--font);
		letter-spacing: 1px;
	}
	.sky :global(.faller .wing) {
		transform-box: fill-box;
		animation: flap 0.3s ease-in-out infinite alternate;
	}
	.sky :global(.faller .wl) {
		transform-origin: 100% 50%;
	}
	.sky :global(.faller .wr) {
		transform-origin: 0% 50%;
		animation-name: flapr;
	}
	/* landed: wings fold in */
	.sky :global(.faller.landed .wing) {
		animation: none;
		transform: rotate(-40deg) scale(0.6);
	}
	.sky :global(.faller.landed .wr) {
		transform: rotate(40deg) scale(0.6);
	}
	.sky :global(.faller.bounce svg) {
		animation: squash 0.5s ease-out;
		transform-origin: 50% 100%;
	}
	/* after .bounce, so a hop replaces the landing squash */
	.sky :global(.faller.hop svg) {
		animation: hop 0.6s ease-out;
		transform-origin: 50% 100%;
	}

	@media (max-width: 640px) {
		.logo :global(.mark) {
			height: 36px;
		}
	}

	@keyframes fade {
		to {
			opacity: 1;
		}
	}
	@keyframes pulse {
		50% {
			opacity: 0.25;
		}
	}
	@keyframes wout {
		to {
			transform: translateY(-100%);
			opacity: 0;
		}
	}
	@keyframes win {
		from {
			transform: translateY(100%);
			opacity: 0;
		}
	}
	@keyframes draw {
		to {
			stroke-dashoffset: 0;
		}
	}
	@keyframes glow {
		to {
			fill: var(--glow);
		}
	}
	@keyframes drift {
		to {
			transform: translateX(60px);
		}
	}
	@keyframes rise {
		0% {
			transform: translateY(0);
			opacity: 1;
		}
		100% {
			transform: translateY(-14px);
			opacity: 0;
		}
	}
	@keyframes flap {
		to {
			transform: rotate(-16deg) scaleY(0.85);
		}
	}
	@keyframes flapr {
		to {
			transform: rotate(16deg) scaleY(0.85);
		}
	}
	@keyframes squash {
		30% {
			transform: scale(1.08, 0.88);
		}
		60% {
			transform: scale(0.97, 1.04);
		}
		100% {
			transform: none;
		}
	}
	@keyframes hop {
		30% {
			transform: translateY(-22%) rotate(-4deg);
		}
		55% {
			transform: translateY(0) scale(1.06, 0.92);
		}
		75% {
			transform: scale(0.98, 1.03);
		}
	}
</style>
