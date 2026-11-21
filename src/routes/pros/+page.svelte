<!-- The "I'm a pro" page. Pre-launch, it signs up businesses for their area, the same way the
     request page signs up customers, and says plainly what they get and when. -->
<script lang="ts">
	import { onMount } from 'svelte';
	import type { Attachment } from 'svelte/attachments';
	import Mark from '#lib/brand/Mark.svelte';
	import { TRADES, type Trade } from '#lib/trades.ts';
	import { RECEPTIONIST } from '#lib/art/receptionist.ts';
	import { mountTurnstile, postJson, type Turnstile } from '#lib/pros/signup.ts';

	interface Joined {
		city: string;
		place?: string | null;
		trade: string;
		position: number;
		code: string;
	}

	// The strip under the comparison: every trade but the catch-all, twice over so it loops seamlessly.
	const STRIP = TRADES.filter((t) => t !== 'Other');

	let form = $state({ business: '', trade: TRADES[0] as Trade, zip: '', phone: '', email: '', consent: false, profile: false });
	let ref: string | null = null;
	let tsNeeded = $state(false);
	let tsToken = $state<string | null>(null);
	let sending = $state(false);
	let error = $state('');
	let joined = $state<{ title: string; lead: string; link: string } | null>(null);
	let copied = $state(false);

	let card: HTMLElement;
	let bizInput = $state<HTMLInputElement>();
	let consentSpan = $state<HTMLSpanElement>();
	let tsEl = $state<HTMLDivElement>();
	let turnstile: Turnstile | null = null;

	const ready = $derived(
		form.consent &&
			form.business.trim() !== '' &&
			/^\d{5}$/.test(form.zip.trim()) &&
			form.phone.replace(/\D/g, '').length >= 10 &&
			(!tsNeeded || tsToken !== null)
	);

	onMount(() => {
		// An invite link (/pro/CODE) lands here with ?ref; keep it in case they sign up on a later visit.
		try {
			const q = new URLSearchParams(location.search).get('ref');
			if (q) localStorage.setItem('scoo_pro_ref', q);
			ref = localStorage.getItem('scoo_pro_ref');
		} catch {
			// storage can be blocked; the sign-up still works without a referrer
		}
		if (tsEl) turnstile = mountTurnstile(tsEl, { needed: () => (tsNeeded = true), token: (t) => (tsToken = t) });
		return () => turnstile?.destroy();
	});

	const ordinal = (n: number) => (n % 100 >= 11 && n % 100 <= 13 ? 'th' : ['th', 'st', 'nd', 'rd'][n % 10] || 'th');

	async function submit(e: SubmitEvent) {
		e.preventDefault();
		if (!ready || sending) return;
		sending = true;
		const body = {
			business: form.business.trim(),
			trade: form.trade,
			zip: form.zip.trim(),
			phone: form.phone,
			email: form.email.trim() || null,
			consent: form.consent,
			// optional: they want a public profile page; Scoo publishes it after a check
			profile: form.profile,
			// the exact words they agreed to, as shown, so the record can prove the opt-in
			consentText: consentSpan?.textContent ?? '',
			ref,
			turnstile: tsToken
		};
		try {
			const r = await postJson<Joined>('/api/pros', body);
			const n = r.position;
			joined = {
				title: `You're a founding pro, ${body.business}.`,
				lead: `You're the ${n}${ordinal(n)} ${r.trade.toLowerCase()} to join in ${r.place || r.city}. We'll text you when your AI receptionist is ready.`,
				link: 'scoo.app/pro/' + r.code
			};
		} catch (err) {
			if (tsNeeded) turnstile?.reset();
			error = (err instanceof Error ? err.message : 'Something went wrong') + '. Please try again.';
		} finally {
			sending = false;
		}
	}

	function claim(e: MouseEvent) {
		e.preventDefault();
		card.scrollIntoView({ behavior: 'smooth', block: 'center' });
		setTimeout(() => bizInput?.focus({ preventScroll: true }), 600);
	}

	function copy() {
		if (!joined) return;
		navigator.clipboard?.writeText('https://' + joined.link);
		copied = true;
	}

	// The example call plays line by line once it scrolls into view, and only once.
	let shown = $state(0);
	const CHAT_LINES = 6;
	const playOnView: Attachment<HTMLElement> = (el) => {
		let timers: ReturnType<typeof setTimeout>[] = [];
		const play = () => {
			const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
			for (let i = 0; i < CHAT_LINES; i++) timers.push(setTimeout(() => (shown = i + 1), reduce ? 0 : 300 + i * 850));
		};
		if (!('IntersectionObserver' in window)) {
			play();
			return () => timers.forEach(clearTimeout);
		}
		const io = new IntersectionObserver(
			(es) => {
				if (es.some((x) => x.isIntersecting)) {
					play();
					io.disconnect();
				}
			},
			{ threshold: 0.35 }
		);
		io.observe(el);
		return () => {
			io.disconnect();
			timers.forEach(clearTimeout);
		};
	};
</script>

<svelte:head>
	<title>Scoo for pros: never miss a customer again</title>
	<meta
		name="description"
		content="Scoo's AI receptionist answers the calls you can't, books the job and texts you the details. Free for founding pros."
	/>
</svelte:head>

<header>
	<div class="hin">
		<a class="logo" href="/" aria-label="Scoo home"><Mark /><span>scoo</span></a>
		<nav class="nav" aria-label="Pros">
			<a class="n" href="#product">Product</a>
			<a class="n" href="#compare">Why Scoo</a>
			<a class="n" href="/exchanges/start">Exchanges</a>
			<a class="pill alt" href="/">I need a pro</a>
			<a class="pill cta-s" href="#join" onclick={claim}>Claim free</a>
		</nav>
	</div>
</header>
<main>
	<div class="top">
		<section class="intro">
			<p class="badge"><i></i>For pros and local businesses</p>
			<h1>Never miss a <span>customer again.</span></h1>
			<p class="lead">
				Scoo's AI receptionist answers every call you can't, books the job and texts you the details. Free for founding pros.
			</p>
			<ul class="perks">
				<li>
					<span>Answers 24/7, in your business name<small>Nights, weekends, while you're on a job. Callers never hit voicemail.</small></span>
				</li>
				<li>
					<span>Books the job and texts you<small>Name, address, what's wrong and when suits them, straight to your phone.</small></span>
				</li>
				<li>
					<span
						>New customers when Scoo opens<small>Neighbours who need your trade get connected to you. Take only the work you want.</small></span
					>
				</li>
			</ul>
		</section>
		<div class="art">{@html RECEPTIONIST}</div>
		<section class="card" aria-labelledby={joined ? undefined : 'join-title'} bind:this={card}>
			{#if joined}
				<div class="done" aria-live="polite">
					<h2>{joined.title}</h2>
					<p class="sub">{joined.lead}</p>
					<p style="margin:0">Know another pro who misses calls? Send them your link so they can claim theirs.</p>
					<div class="link"><span>{joined.link}</span><button type="button" onclick={copy}>{copied ? 'Copied' : 'Copy'}</button></div>
				</div>
			{:else}
				<div id="join">
					<h2 id="join-title">Claim your free receptionist</h2>
					<p class="sub">Founding pros get it free. Takes a minute, no card needed.</p>
					<form onsubmit={submit}>
						<label class="f"
							>Business name<input
								bind:this={bizInput}
								bind:value={form.business}
								autocomplete="organization"
								required
								maxlength="120"
								placeholder="Rivera Plumbing"
							/></label
						>
						<div class="row">
							<label class="f"
								>Your trade<select bind:value={form.trade} required>
									{#each TRADES as t (t)}<option>{t}</option>{/each}
								</select></label
							>
							<label class="f"
								>ZIP you work in<input
									bind:value={form.zip}
									inputmode="numeric"
									autocomplete="postal-code"
									maxlength="5"
									pattern={'[0-9]{5}'}
									required
									placeholder="75201"
								/></label
							>
						</div>
						<div class="row">
							<label class="f"
								>Mobile number<input bind:value={form.phone} type="tel" autocomplete="tel" required placeholder="(555) 555-0100" /></label
							>
							<label class="f"
								>Email<input bind:value={form.email} type="email" autocomplete="email" maxlength="160" placeholder="Optional" /></label
							>
						</div>
						<label class="consent opt"
							><input type="checkbox" bind:checked={form.profile} /><span
								>Also give my business a free public profile on Scoo, like <a href="/p/example-rivera-plumbing" target="_blank" rel="noopener">this example</a>. We'll check the details with you before it goes live.</span
							></label
						>
						<label class="consent"
							><input type="checkbox" bind:checked={form.consent} required /><span bind:this={consentSpan}
								>I agree to Scoo's <a href="/terms" target="_blank" rel="noopener">terms</a>, and that Scoo may call or text me about joining and connect customer calls to this number. Calls may be recorded. Reply STOP to opt out.</span
							></label
						>
						<div bind:this={tsEl}></div>
						{#if error}<p class="err" role="alert">{error}</p>{/if}
						<button class="primary" disabled={!ready || sending}>{sending ? 'Joining…' : 'Claim it free'}</button>
						<p class="fine">Your receptionist switches on when Scoo opens in your area. We'll text you first.</p>
					</form>
				</div>
			{/if}
		</section>
	</div>

	<section class="sec" id="product" aria-labelledby="feat-title">
		<p class="eyebrow">One app for your business</p>
		<h2 id="feat-title">Everything you need to win the job. <span>Nothing you don't.</span></h2>
		<div class="bento">
			<article class="tile t-recep">
				<div class="tx">
					<h3>AI receptionist</h3>
					<p>Picks up in your business name, asks the questions your trade needs, and books a time that suits the customer and you.</p>
					<span class="tag"><i></i>Free for founding pros</span>
				</div>
				<div class="ui chat" aria-label="Example call, answered by the AI receptionist" {@attach playOnView}>
					<div class="ui-top"><span class="dot"></span>Answering for Rivera Plumbing</div>
					<p class="b them" class:on={shown > 0}>Hi, my water heater is leaking.</p>
					<p class="b us" class:on={shown > 1}>Sorry to hear that. You've reached Rivera Plumbing. Is it still running, or just dripping?</p>
					<p class="b them" class:on={shown > 2}>Just dripping. I'm in 75204.</p>
					<p class="b us" class:on={shown > 3}>We can be there today at 3pm. Shall I book that?</p>
					<p class="b them" class:on={shown > 4}>Yes please.</p>
					<div class="sum" class:on={shown > 5}>✓ Booked today, 3:00 pm. Details texted to you.</div>
				</div>
			</article>
			<article class="tile t-opps">
				<div class="tx">
					<h3>Opportunities</h3>
					<p>When neighbours ask Scoo for your trade, the job lands here with the price up front. Take it or pass. No bidding wars.</p>
				</div>
				<div class="ui inbox" aria-label="Example opportunities">
					<div class="ui-top">Opportunities</div>
					<div class="op new">
						<div><b>Water heater leak</b><small>Uptown · 1.4 mi · now</small></div>
						<span class="price">$34</span>
						<div class="why">Matches your rules: plumbing, within 10 mi, weekdays</div>
						<div class="acts"><span class="take">Take call</span><span>Pass</span></div>
					</div>
					<div class="op">
						<div><b>Toilet replacement</b><small>Highland Park · 4.8 mi · today</small></div>
						<span class="price">$29</span>
					</div>
					<div class="op">
						<div><b>Drain cleaning</b><small>Oak Lawn · 2.0 mi · tomorrow</small></div>
						<span class="price">$22</span>
					</div>
				</div>
			</article>
			<article class="tile t-rules">
				<div class="tx">
					<h3>Your rules, in plain English</h3>
					<p>Say what work you want. Scoo sends only that.</p>
				</div>
				<div class="ui rules" aria-label="Example rules">
					<div class="rl"><span>Only within 10 miles of 75201</span><i class="sw"></i></div>
					<div class="rl"><span>Weekdays, 7am to 6pm</span><i class="sw"></i></div>
					<div class="rl"><span>No more than $40 a call</span><i class="sw"></i></div>
					<div class="rl"><span>Weekend emergencies</span><i class="sw off"></i></div>
				</div>
			</article>
			<article class="tile t-prof">
				<div class="tx">
					<h3>A profile that earns trust</h3>
					<p>Jobs won and calls answered, counted by Scoo, not self-reported.</p>
					<a class="more" href="/p/example-rivera-plumbing">See an example profile →</a>
				</div>
				<div class="ui prof" aria-label="Example pro profile">
					<div class="ph">
						<span class="av">RP</span>
						<div><b>Rivera Plumbing</b><small>Plumber · Dallas</small></div>
						<span class="prem">Premium pro</span>
					</div>
					<div class="stats">
						<div><b>142</b><small>Jobs won</small></div>
						<div><b>98%</b><small>Calls answered</small></div>
						<div><b>2026</b><small>Member since</small></div>
					</div>
				</div>
			</article>
			<article class="tile t-exch">
				<div class="tx">
					<h3>Join exchanges</h3>
					<p>Networks of pros who pass work to each other, each with its own page and rules.</p>
				</div>
				<div class="chips">
					<a class="chip" href="/x/example">DFW Home Pros</a><span class="chip">North Texas Roofers</span><span class="chip">Uptown Trades</span><a
						class="chip add"
						href="/exchanges/start">+ Start your own</a
					>
				</div>
			</article>
			<article class="tile t-pay">
				<div class="tx">
					<h3>No monthly fee</h3>
					<p>No subscription, no contract. New customer calls are optional, and you see the price before you take one.</p>
				</div>
				<div class="big">$0<small>a month</small></div>
			</article>
		</div>
		<p class="note">Product previews use example names and numbers.</p>
	</section>

	<section class="sec" id="compare" aria-labelledby="cmp-title">
		<p class="eyebrow">Why Scoo</p>
		<h2 id="cmp-title">Lead sites sell the same customer to several pros. <span>Scoo connects one.</span></h2>
		<div class="cmp">
			<table>
				<thead>
					<tr><th scope="col"><span class="vh">Compare</span></th><th scope="col">Typical lead sites</th><th scope="col" class="us">Scoo</th></tr>
				</thead>
				<tbody>
					<tr><th scope="row">Who gets the customer</th><td>Often shared with several pros at once</td><td class="us">One pro at a time</td></tr>
					<tr>
						<th scope="row">What you pay for</th><td>A name and number, whether they pick up or not</td><td class="us">A live call, price shown first</td>
					</tr>
					<tr>
						<th scope="row">Calls you miss</th><td>Go to voicemail, then to a competitor</td><td class="us">Answered and booked by your AI receptionist</td>
					</tr>
					<tr><th scope="row">Monthly fees</th><td>Common</td><td class="us">None</td></tr>
					<tr><th scope="row">Your reputation</th><td>Lives on their site</td><td class="us">Your profile, your name, your exchanges</td></tr>
				</tbody>
			</table>
		</div>
	</section>

	<div class="trades" aria-label="Trades on Scoo">
		<p>Built for every local business</p>
		<div class="track">
			{#each [...STRIP, ...STRIP] as t, i (i)}<span class="chip">{t}</span>{/each}
		</div>
	</div>

	<section class="how sec" aria-labelledby="how-title">
		<h2 id="how-title">How it works</h2>
		<ol>
			<li><b>1</b><h3>A call comes in</h3><p>You're under a sink, up a ladder, or it's 9pm. Your missed calls forward to Scoo.</p></li>
			<li><b>2</b><h3>Scoo answers for you</h3><p>In your business name. It asks what's wrong, where they are and when suits them.</p></li>
			<li><b>3</b><h3>You get the job</h3><p>A text with everything you need. Call them back, or just show up at the time they booked.</p></li>
		</ol>
	</section>

	<section class="network" aria-labelledby="net-title">
		<div>
			<h2 id="net-title">Run a network or referral group?</h2>
			<p>Turn it into an exchange on Scoo. Your own page, your rules in plain English, and you earn on every match.</p>
		</div>
		<a class="pill net" href="/exchanges/start">Start an exchange →</a>
	</section>

	<section class="faq" aria-labelledby="faq-title">
		<h2 id="faq-title">Questions</h2>
		<details>
			<summary>Is the AI receptionist really free?</summary>
			<p>
				Yes, for founding pros: everyone who claims it before Scoo opens in their area. A fair-use limit covers normal call volumes for a local
				business, and we'll tell you what it is before it switches on.
			</p>
		</details>
		<details>
			<summary>What does it cost?</summary>
			<p>
				The AI receptionist is free for founding pros. When Scoo opens in your area, you can also choose to receive new customer calls from Scoo.
				Those are pay-per-call: you'll see the price before you take one, and you set your own limits.
			</p>
		</details>
		<details>
			<summary>Do I need a new phone number?</summary>
			<p>No. Keep your number. You forward the calls you can't answer to Scoo, and it picks up from there.</p>
		</details>
		<details>
			<summary>When does Scoo start in my area?</summary>
			<p>City by city, once enough customers and pros in an area have signed up. You'll hear from us before it opens near you.</p>
		</details>
		<details>
			<summary>Are these leads shared with other pros?</summary>
			<p>Each call goes to one pro at a time. If you don't pick up, it moves to the next pro, so the customer still gets help fast.</p>
		</details>
		<details>
			<summary>Can I choose my hours and area?</summary>
			<p>Yes. You set the ZIP codes you cover and when you're available, and you can pause any time.</p>
		</details>
	</section>

	<section class="final" aria-labelledby="fin-title">
		<Mark class="mark mk" />
		<h2 id="fin-title">Stop losing jobs to voicemail.</h2>
		<p>Claim your free AI receptionist now. It switches on when Scoo opens in your area.</p>
		<a href="#join" onclick={claim}>Claim your free receptionist</a>
	</section>
</main>
<footer class="foot"><a href="/exchanges/start">Start an exchange</a><a href="/terms">Terms</a><a href="/privacy">Privacy</a></footer>

<style>
	header {
		position: sticky;
		top: 0;
		z-index: 20;
		padding: 14px clamp(16px, 4vw, 48px);
		background: color-mix(in srgb, var(--bg) 86%, transparent);
		backdrop-filter: saturate(1.4) blur(12px);
		-webkit-backdrop-filter: saturate(1.4) blur(12px);
	}
	.hin {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
		max-width: 1120px;
		margin: 0 auto;
		width: 100%;
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
	.pill {
		display: inline-flex;
		align-items: center;
		min-height: 44px;
		padding: 0 18px;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		color: var(--ink);
		text-decoration: none;
		font-weight: 500;
	}
	.nav {
		display: flex;
		align-items: center;
		gap: 6px;
	}
	.nav a.n {
		color: var(--ink);
		text-decoration: none;
		font-size: 15px;
		padding: 10px 12px;
		border-radius: 999px;
	}
	.nav a.n:hover {
		background: var(--tile);
	}
	.cta-s {
		background: var(--accent);
		border-color: var(--accent) !important;
		color: #fff !important;
		margin-left: 6px;
	}
	@media (max-width: 880px) {
		.nav a.n,
		.nav .pill.alt {
			display: none;
		}
	}
	main {
		max-width: 1120px;
		margin: 0 auto;
		padding: 8px clamp(16px, 4vw, 48px) 64px;
	}

	/* hero */
	.top {
		display: grid;
		grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
		grid-template-areas: 'intro card' 'art card';
		column-gap: clamp(24px, 5vw, 64px);
		row-gap: 0;
		align-items: center;
	}
	.top > .intro {
		grid-area: intro;
	}
	.top > .art {
		grid-area: art;
	}
	.top > .card {
		grid-area: card;
	}
	@media (max-width: 880px) {
		.top {
			grid-template-columns: 1fr;
			grid-template-areas: 'intro' 'card' 'art';
			row-gap: 28px;
		}
	}
	.badge {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 7px 14px;
		font-size: 14px;
		font-weight: 500;
		margin: 0;
	}
	.badge i {
		width: 8px;
		height: 8px;
		border-radius: 99px;
		background: var(--accent);
	}
	h1 {
		margin: 16px 0 0;
		font-weight: 300;
		font-size: clamp(40px, 5.4vw, 72px);
		line-height: 1.02;
		letter-spacing: -0.035em;
	}
	h1 span {
		color: var(--accent);
	}
	.lead {
		margin: 16px 0 0;
		font-size: 19px;
		line-height: 1.5;
		color: var(--muted);
		max-width: 520px;
	}
	.perks {
		list-style: none;
		margin: 22px 0 0;
		padding: 0;
		display: grid;
		gap: 12px;
	}
	.perks li {
		display: flex;
		gap: 12px;
		align-items: flex-start;
		font-size: 17px;
		line-height: 1.4;
	}
	.perks li::before {
		content: '';
		flex: 0 0 auto;
		width: 22px;
		height: 22px;
		margin-top: 1px;
		border-radius: 99px;
		background: var(--accent)
			url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M6 12.5l4 4 8-9' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")
			center/16px no-repeat;
	}
	.perks small {
		display: block;
		color: var(--muted);
		font-size: 14px;
	}

	/* the receptionist illustration, injected as markup, so its rules reach in with :global */
	.art {
		width: min(440px, 100%);
		margin: 28px auto 0;
	}
	.art :global {
		.ill {
			width: 100%;
			height: auto;
			overflow: visible;
		}
		.ill * {
			fill: none;
			stroke: var(--ink);
			stroke-width: 2.2;
			stroke-linecap: round;
			stroke-linejoin: round;
		}
		.ill .soft,
		.ill .wingp {
			fill: var(--soft);
		}
		.ill .accent {
			fill: var(--accent);
		}
		.ill .paper,
		.ill .fillbg,
		.ill .skin,
		.ill .mouth,
		.ill .sign,
		.ill .bib,
		.ill .tool,
		.ill .win {
			fill: var(--bg);
		}
		.ill .hat {
			fill: var(--accent);
		}
		.ill .eyes {
			stroke-width: 4;
		}
		.ill .dash {
			stroke-dasharray: 14 14;
		}
		.ill text {
			stroke: none;
			fill: var(--ink);
			font: 600 13px var(--font);
		}
		.ill .signtxt {
			font: 600 11px var(--font);
			letter-spacing: 2px;
		}
		.ill .t {
			font: 500 8.5px var(--font);
			fill: var(--ink);
		}
		.ill .tw {
			font: 600 9px var(--font);
			fill: #fff;
		}
		.ill .busy {
			font: 500 11px var(--font);
			fill: var(--muted);
		}
		.ill .msg {
			animation: pop 0.4s cubic-bezier(0.3, 0.8, 0.3, 1.3) both;
			animation-delay: calc(0.6s + var(--i) * 0.9s);
		}
		.ill .wing {
			transform-box: fill-box;
			animation: flap 0.3s ease-in-out infinite alternate;
		}
		.ill .wl {
			transform-origin: 100% 50%;
		}
		.ill .wr {
			transform-origin: 0% 50%;
			animation-name: flapr;
		}
		.ill .phone {
			transform-box: fill-box;
			transform-origin: 50% 50%;
		}
		.ill .buzz {
			stroke: var(--accent);
			animation: buzz 1.4s ease-in-out 3;
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
	@keyframes buzz {
		0%,
		60%,
		100% {
			opacity: 0;
		}
		10%,
		50% {
			opacity: 1;
		}
	}
	@keyframes pop {
		from {
			opacity: 0;
			transform: scale(0.7);
		}
	}

	/* sign-up card */
	.card {
		border: 1.5px solid var(--ink);
		border-radius: 24px;
		padding: clamp(18px, 3vw, 28px);
		background: var(--bg);
	}
	.card h2 {
		margin: 0;
		font-size: 24px;
		font-weight: 500;
		letter-spacing: -0.01em;
	}
	.card .sub {
		margin: 6px 0 0;
		color: var(--muted);
	}
	form {
		display: grid;
		gap: 12px;
		margin-top: 18px;
	}
	label.f {
		display: grid;
		gap: 6px;
		font-size: 14px;
		font-weight: 500;
	}
	.f input,
	.f select {
		min-height: 50px;
		border: 1.5px solid var(--ink);
		border-radius: 14px;
		padding: 0 14px;
		font: 400 17px var(--font);
		background: var(--bg);
		color: var(--ink);
		width: 100%;
	}
	.f input:focus,
	.f select:focus {
		outline: none;
		box-shadow: 0 0 0 4px var(--soft);
	}
	.row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 12px;
	}
	@media (max-width: 420px) {
		.row {
			grid-template-columns: 1fr;
		}
	}
	.consent {
		display: flex;
		gap: 10px;
		font-size: 13px;
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
	.consent a {
		color: inherit;
	}
	.consent.opt {
		color: var(--ink);
		font-size: 14px;
	}
	.more {
		display: inline-block;
		margin-top: 8px;
		color: var(--ink);
		font-weight: 600;
		font-size: 14px;
	}
	.primary {
		min-height: 54px;
		border: 0;
		border-radius: 999px;
		background: var(--accent);
		color: #fff;
		font: 600 17px var(--font);
		cursor: pointer;
	}
	.primary:disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}
	.err {
		margin: 0;
		color: #c0392b;
		font-size: 14px;
	}
	.fine {
		margin: 0;
		font-size: 12px;
		color: var(--muted);
	}
	.done {
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.done h2 {
		font-size: 28px;
		font-weight: 400;
	}
	.link {
		display: flex;
		align-items: center;
		gap: 8px;
		border: 1.5px dashed var(--ink);
		border-radius: 14px;
		padding: 8px 12px;
	}
	.link span {
		flex: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.link button {
		flex: 0 0 auto;
		min-height: 38px;
		border-radius: 999px;
		border: 1.5px solid var(--ink);
		background: var(--bg);
		color: var(--ink);
		padding: 0 14px;
		font: 600 14px var(--font);
		cursor: pointer;
	}

	/* product */
	.eyebrow {
		margin: 0;
		color: var(--accent);
		font-weight: 600;
		font-size: 14px;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}
	.sec {
		margin-top: clamp(56px, 9vw, 112px);
	}
	.sec > h2 {
		margin: 10px 0 0;
		font-weight: 300;
		font-size: clamp(34px, 4.6vw, 58px);
		line-height: 1.04;
		letter-spacing: -0.035em;
		max-width: 820px;
	}
	.sec > h2 span {
		color: var(--muted);
	}
	.bento {
		margin-top: 28px;
		display: grid;
		grid-template-columns: repeat(6, minmax(0, 1fr));
		gap: 16px;
	}
	.tile {
		background: var(--tile);
		border: 1.5px solid var(--line);
		border-radius: 28px;
		padding: clamp(20px, 2.6vw, 28px);
		display: flex;
		flex-direction: column;
		gap: 18px;
		overflow: hidden;
		position: relative;
	}
	.tile h3 {
		margin: 0;
		font-size: 22px;
		font-weight: 500;
		letter-spacing: -0.01em;
	}
	.tile p {
		margin: 6px 0 0;
		color: var(--muted);
		line-height: 1.5;
	}
	.t-recep {
		grid-column: span 4;
		flex-direction: row;
		align-items: stretch;
	}
	.t-recep .tx {
		flex: 1 1 40%;
		display: flex;
		flex-direction: column;
	}
	.t-recep .ui {
		flex: 1 1 60%;
	}
	.t-opps {
		grid-column: span 2;
		grid-row: span 2;
	}
	.t-rules,
	.t-prof {
		grid-column: span 2;
	}
	.t-exch,
	.t-pay {
		grid-column: span 3;
	}
	@media (max-width: 1000px) {
		.bento {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
		.tile,
		.t-recep,
		.t-opps {
			grid-column: span 2;
			grid-row: auto;
		}
		.t-rules,
		.t-prof,
		.t-exch,
		.t-pay {
			grid-column: span 1;
		}
	}
	@media (max-width: 640px) {
		.t-recep {
			flex-direction: column;
		}
		.t-recep .tx,
		.t-recep .ui {
			flex: none;
		}
		.t-recep .tag {
			margin-top: 14px;
		}
		.t-rules,
		.t-prof,
		.t-exch,
		.t-pay {
			grid-column: span 2;
		}
	}
	.tag {
		align-self: flex-start;
		margin-top: auto;
		display: inline-flex;
		align-items: center;
		gap: 6px;
		background: var(--bg);
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 6px 12px;
		font-size: 13px;
		font-weight: 600;
	}
	.tag i {
		width: 7px;
		height: 7px;
		border-radius: 9px;
		background: var(--green);
	}
	.ui {
		background: var(--bg);
		border: 1.5px solid var(--line);
		border-radius: 20px;
		padding: 14px;
		box-shadow: 0 18px 40px -24px rgba(0, 0, 0, 0.25);
		font-size: 14px;
	}
	.ui-top {
		display: flex;
		align-items: center;
		gap: 8px;
		color: var(--muted);
		font-size: 12px;
		font-weight: 600;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		margin-bottom: 4px;
	}
	.dot {
		width: 8px;
		height: 8px;
		border-radius: 9px;
		background: var(--green);
		animation: pulse 1.8s infinite;
	}
	@keyframes pulse {
		50% {
			opacity: 0.35;
		}
	}
	.chat {
		display: flex;
		flex-direction: column;
		gap: 8px;
		min-height: 330px;
	}
	.b {
		margin: 0;
		max-width: 84%;
		padding: 9px 12px;
		border-radius: 16px;
		line-height: 1.35;
		opacity: 0;
		transform: translateY(6px);
		transition:
			opacity 0.35s,
			transform 0.35s;
	}
	.b.them {
		align-self: flex-start;
		background: var(--tile);
		border-bottom-left-radius: 6px;
	}
	.b.us {
		align-self: flex-end;
		background: var(--soft);
		border-bottom-right-radius: 6px;
	}
	.sum {
		margin-top: 4px;
		padding: 10px 12px;
		border-radius: 14px;
		background: var(--accent);
		color: #fff;
		font-weight: 600;
		opacity: 0;
		transform: translateY(6px);
		transition:
			opacity 0.35s,
			transform 0.35s;
	}
	.chat .on {
		opacity: 1;
		transform: none;
	}
	.inbox {
		display: flex;
		flex-direction: column;
		gap: 10px;
		margin-top: auto;
	}
	.op {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 4px 10px;
		align-items: center;
		border: 1.5px solid var(--line);
		border-radius: 16px;
		padding: 12px;
	}
	.op b {
		font-weight: 600;
	}
	.op small {
		display: block;
		color: var(--muted);
		font-size: 13px;
		margin-top: 2px;
	}
	.price {
		font-size: 20px;
		font-weight: 600;
		letter-spacing: -0.02em;
	}
	.op .acts {
		grid-column: 1/-1;
		display: flex;
		gap: 8px;
		margin-top: 6px;
	}
	.op .acts span {
		flex: 1;
		text-align: center;
		border-radius: 999px;
		padding: 7px 0;
		font-size: 13px;
		font-weight: 600;
		border: 1.5px solid var(--ink);
	}
	.op .acts .take {
		background: var(--ink);
		color: var(--bg);
	}
	.op.new {
		border-color: var(--accent);
		box-shadow: 0 0 0 3px var(--soft);
	}
	.op .why {
		grid-column: 1/-1;
		font-size: 12px;
		color: var(--muted);
	}
	.rules {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.rl {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
	}
	.rl span {
		line-height: 1.35;
	}
	.sw {
		flex: 0 0 auto;
		width: 38px;
		height: 22px;
		border-radius: 99px;
		background: var(--accent);
		position: relative;
	}
	.sw::after {
		content: '';
		position: absolute;
		top: 3px;
		right: 3px;
		width: 16px;
		height: 16px;
		border-radius: 9px;
		background: #fff;
	}
	.sw.off {
		background: var(--line);
	}
	.sw.off::after {
		right: auto;
		left: 3px;
	}
	.prof {
		display: grid;
		gap: 12px;
	}
	.ph {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	.av {
		flex: 0 0 auto;
		width: 46px;
		height: 46px;
		border-radius: 99px;
		background: var(--soft);
		display: grid;
		place-items: center;
		font-weight: 600;
		border: 1.5px solid var(--ink);
	}
	.ph b {
		display: block;
	}
	.ph small {
		color: var(--muted);
	}
	.prem {
		margin-left: auto;
		background: var(--glow);
		border-radius: 999px;
		padding: 4px 10px;
		font-size: 12px;
		font-weight: 600;
		white-space: nowrap;
	}
	.stats {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 6px;
		text-align: center;
	}
	.stats div {
		background: var(--tile);
		border-radius: 12px;
		padding: 8px 4px;
	}
	.stats b {
		display: block;
		font-size: 18px;
		font-weight: 600;
	}
	.stats small {
		color: var(--muted);
		font-size: 11px;
	}
	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
	}
	.chip {
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 7px 12px;
		font-size: 13px;
		font-weight: 500;
		background: var(--bg);
		color: var(--ink);
		text-decoration: none;
	}
	.chip.add {
		border-style: dashed;
		color: var(--muted);
		border-color: var(--muted);
	}
	.big {
		margin-top: auto;
		font-size: clamp(54px, 6vw, 76px);
		font-weight: 300;
		letter-spacing: -0.05em;
		line-height: 1;
	}
	.big small {
		font-size: 16px;
		letter-spacing: 0;
		color: var(--muted);
		margin-left: 6px;
	}
	.note {
		margin: 14px 0 0;
		color: var(--muted);
		font-size: 13px;
	}

	/* comparison */
	.cmp {
		margin-top: 28px;
		border: 1.5px solid var(--ink);
		border-radius: 28px;
		overflow: hidden;
	}
	.cmp table {
		width: 100%;
		border-collapse: collapse;
		font-size: 16px;
	}
	.cmp th,
	.cmp td {
		padding: 16px clamp(12px, 2vw, 24px);
		text-align: left;
		vertical-align: top;
		border-top: 1.5px solid var(--line);
	}
	.cmp thead th {
		border-top: 0;
		font-size: 14px;
		font-weight: 600;
		color: var(--muted);
	}
	.cmp thead th.us {
		color: var(--accent);
	}
	.cmp td {
		color: var(--muted);
	}
	.cmp td.us {
		background: color-mix(in srgb, var(--soft) 45%, transparent);
		font-weight: 500;
		color: var(--ink);
	}
	.cmp th[scope='row'] {
		font-weight: 500;
		width: 26%;
	}
	@media (max-width: 640px) {
		.cmp table {
			font-size: 14px;
		}
		.cmp th[scope='row'] {
			width: 30%;
		}
	}

	/* trades strip */
	.trades {
		margin-top: clamp(48px, 7vw, 80px);
		overflow: hidden;
		-webkit-mask: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
		mask: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
	}
	.trades p {
		text-align: center;
		color: var(--muted);
		margin: 0 0 14px;
	}
	.track {
		display: flex;
		gap: 10px;
		width: max-content;
		animation: slide 40s linear infinite;
	}
	.track .chip {
		white-space: nowrap;
	}
	@keyframes slide {
		to {
			transform: translateX(-50%);
		}
	}

	/* how it works */
	.how ol {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 16px;
	}
	.how li {
		border: 1.5px solid var(--ink);
		border-radius: 20px;
		padding: 22px;
	}
	.how b {
		display: inline-grid;
		place-items: center;
		width: 32px;
		height: 32px;
		border-radius: 99px;
		background: var(--accent);
		color: #fff;
		font-weight: 600;
	}
	.how h3 {
		margin: 12px 0 6px;
		font-size: 20px;
		font-weight: 500;
	}
	.how p {
		margin: 0;
		color: var(--muted);
		line-height: 1.5;
	}

	/* network band */
	.network {
		margin-top: clamp(40px, 7vw, 72px);
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 16px 32px;
		border: 1.5px solid var(--ink);
		border-radius: 24px;
		padding: clamp(20px, 3vw, 32px);
		background: repeating-linear-gradient(135deg, transparent 0 14px, var(--soft) 14px 15px);
	}
	.network h2 {
		margin: 0;
		font-weight: 400;
		font-size: clamp(24px, 3vw, 32px);
		letter-spacing: -0.02em;
	}
	.network p {
		margin: 6px 0 0;
		color: var(--muted);
		max-width: 560px;
	}
	.network > div {
		background: var(--bg);
		padding: 4px 8px;
		border-radius: 12px;
	}
	.net {
		background: var(--bg);
		font-weight: 600;
	}

	/* FAQ */
	.faq {
		margin-top: clamp(40px, 7vw, 72px);
		max-width: 760px;
	}
	.faq h2 {
		font-weight: 300;
		font-size: clamp(28px, 3.2vw, 40px);
		letter-spacing: -0.03em;
		margin: 0 0 12px;
	}
	.faq details {
		border-top: 1.5px solid var(--line);
		padding: 16px 0;
	}
	.faq summary {
		cursor: pointer;
		font-size: 18px;
		font-weight: 500;
		list-style: none;
	}
	.faq summary::-webkit-details-marker {
		display: none;
	}
	.faq summary::after {
		content: '+';
		float: right;
		color: var(--accent);
		font-size: 22px;
		line-height: 1;
	}
	.faq details[open] summary::after {
		content: '–';
	}
	.faq p {
		margin: 10px 0 0;
		color: var(--muted);
		line-height: 1.55;
	}

	/* final call to action */
	.final {
		margin-top: clamp(56px, 9vw, 112px);
		background: var(--ink);
		color: var(--bg);
		border-radius: 32px;
		padding: clamp(36px, 6vw, 72px) clamp(20px, 5vw, 64px);
		text-align: center;
		position: relative;
		overflow: hidden;
	}
	.final h2 {
		margin: 0 auto;
		font-weight: 300;
		font-size: clamp(36px, 5vw, 64px);
		line-height: 1.02;
		letter-spacing: -0.035em;
		max-width: 760px;
	}
	.final p {
		margin: 14px auto 0;
		opacity: 0.75;
		max-width: 520px;
		font-size: 18px;
		line-height: 1.5;
	}
	.final a {
		margin-top: 26px;
		display: inline-flex;
		align-items: center;
		min-height: 56px;
		padding: 0 28px;
		border-radius: 999px;
		background: var(--accent);
		color: #fff;
		text-decoration: none;
		font-weight: 600;
		font-size: 17px;
	}
	.final :global(.mk) {
		position: absolute;
		height: auto;
		width: 220px;
		opacity: 0.12;
		right: -30px;
		bottom: -40px;
		color: var(--bg);
	}

	.foot {
		max-width: 1120px;
		margin: 0 auto;
		padding: 0 clamp(16px, 4vw, 48px) 40px;
		font-size: 14px;
	}
	.foot a {
		color: var(--muted);
		margin-right: 16px;
	}
</style>
