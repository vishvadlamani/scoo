<!-- A pro's public profile: who they are, where they work, and the track record Scoo counts for
     them. Numbers come from real calls only, so a new pro shows none rather than a zero. -->
<script lang="ts">
	import SiteHeader from '#lib/profiles/SiteHeader.svelte';
	import ExampleBar from '#lib/profiles/ExampleBar.svelte';
	import AreaOutline from '#lib/profiles/AreaOutline.svelte';
	import Seo from '#lib/profiles/Seo.svelte';
	import { initials, monthYear, percent, tradeNoun } from '#lib/profiles/format.ts';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
	const p = $derived(data.pro);
	const town = $derived(p.place?.replace(/, [A-Z]{2}$/, '') ?? null);
	const title = $derived(`${p.business} · ${p.trade}${p.place ? ` in ${p.place}` : ''} · Scoo`);
	const description = $derived(
		p.about ?? `${p.business} is ${tradeNoun(p.trade)}${p.place ? ` in ${p.place}` : ''} on Scoo. Request them in 60 seconds.`
	);
	const ask = $derived(`/request?q=${encodeURIComponent(`I need ${tradeNoun(p.trade)}`)}`);
	const jsonLd = $derived(
		p.example
			? null
			: {
					'@context': 'https://schema.org',
					'@type': 'LocalBusiness',
					name: p.business,
					url: `https://scoo.app/p/${p.slug}`,
					description,
					...(p.place ? { address: { '@type': 'PostalAddress', addressLocality: town, addressRegion: p.place.slice(-2), addressCountry: 'US' } } : {}),
					...(p.area ? { areaServed: p.area.name } : {})
				}
	);
	let copied = $state(false);
	async function share() {
		const url = `https://scoo.app/p/${p.slug}`;
		try {
			if (navigator.share) await navigator.share({ title: p.business, url });
			else {
				await navigator.clipboard.writeText(url);
				copied = true;
				setTimeout(() => (copied = false), 2000);
			}
		} catch {
			// cancelled share sheet: nothing to do
		}
	}
</script>

<Seo {title} {description} path="/p/{p.slug}" index={!p.example} {jsonLd} />

{#if p.example}<ExampleBar what="An example pro profile." href="/pros" cta="Claim yours free" />{/if}
<SiteHeader />

<main>
	<section class="card head">
		<div class="who">
			<span class="av" aria-hidden="true">{initials(p.business)}</span>
			<div>
				<h1>{p.business}</h1>
				<p class="line">{p.trade}{p.place ? ` · ${p.place}` : ''}</p>
				<ul class="badges">
					{#if p.premium}<li class="prem">Premium pro</li>{/if}
					{#if p.founding}<li>Founding pro</li>{/if}
					<li class="since">On Scoo since {monthYear(p.memberSince)}</li>
				</ul>
			</div>
		</div>
		<div class="btns">
			<a class="btn p" href={ask}>Request {p.business}</a>
			<button class="btn" type="button" onclick={share}>{copied ? 'Link copied' : 'Share'}</button>
		</div>
	</section>

	<section class="record" aria-labelledby="rec">
		<h2 id="rec" class="vh">Track record</h2>
		{#if p.record}
			<div class="stats">
				<div><b>{p.record.jobsWon}</b><small>Jobs won through Scoo</small></div>
				<div><b>{percent(p.record.answerRate)}</b><small>Calls answered</small></div>
				<div><b>{p.record.answerSecs}s</b><small>Average pick-up</small></div>
			</div>
			<p class="note">Counted by Scoo from real calls, not self-reported.</p>
		{:else}
			<p class="note fresh">New on Scoo. Jobs won and calls answered appear here as Scoo counts them from real calls.</p>
		{/if}
	</section>

	<div class="grid">
		<div>
			{#if p.about}
				<section class="block">
					<h2>About</h2>
					<p class="about">{p.about}</p>
				</section>
			{/if}
			<section class="block">
				<h2>Services</h2>
				<ul class="chips">
					{#each p.services as s (s)}<li>{s}</li>{/each}
				</ul>
			</section>
			{#if p.exchanges.length}
				<section class="block">
					<h2>Exchanges</h2>
					<p class="sub">Networks of pros that pass work to each other.</p>
					<ul class="chips">
						{#each p.exchanges as x (x.slug)}<li><a href="/x/{x.slug}">{x.name}</a></li>{/each}
					</ul>
				</section>
			{/if}
		</div>
		{#if p.area}
			<aside class="card area">
				<h2>Service area</h2>
				<AreaOutline outline={p.area.outline} label={p.area.name} />
				<p class="sub">{p.area.name}</p>
			</aside>
		{/if}
	</div>

	<section class="claim">
		<div>
			<h2>Are you a pro{town ? ` in ${town}` : ''}?</h2>
			<p>Get a profile like this, and a free AI receptionist that answers the calls you miss.</p>
		</div>
		<a class="btn p" href="/pros">Claim yours free</a>
	</section>
</main>

<footer class="foot">
	<a href="/">Scoo</a><a href="/pros">For pros</a><a href="/exchanges/start">Start an exchange</a><a href="/terms">Terms</a><a href="/privacy">Privacy</a>
</footer>

<style>
	main {
		max-width: 1000px;
		margin: 0 auto;
		padding: 12px clamp(16px, 4vw, 48px) 64px;
	}
	.card {
		border: 1.5px solid var(--ink);
		border-radius: 28px;
		padding: clamp(20px, 3vw, 32px);
		background: var(--bg);
	}
	.head {
		display: flex;
		flex-wrap: wrap;
		gap: 20px;
		align-items: center;
		justify-content: space-between;
		background:
			radial-gradient(var(--soft) 1.5px, transparent 1.5px) 0 0 / 16px 16px,
			var(--tint);
	}
	.who {
		display: flex;
		gap: 18px;
		align-items: center;
		min-width: 0;
	}
	.av {
		flex: 0 0 auto;
		width: clamp(72px, 10vw, 96px);
		height: clamp(72px, 10vw, 96px);
		border-radius: 99px;
		border: 1.5px solid var(--ink);
		background: var(--soft);
		display: grid;
		place-items: center;
		font: 600 clamp(24px, 3vw, 32px) var(--font);
	}
	h1 {
		margin: 0;
		font-weight: 400;
		font-size: clamp(30px, 4.4vw, 48px);
		letter-spacing: -0.03em;
		line-height: 1.05;
	}
	.line {
		margin: 6px 0 0;
		font-size: 17px;
		color: var(--muted);
	}
	.badges {
		list-style: none;
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		margin: 12px 0 0;
		padding: 0;
	}
	.badges li {
		border: 1.5px solid var(--ink);
		background: var(--bg);
		border-radius: 999px;
		padding: 4px 10px;
		font-size: 12px;
		font-weight: 600;
	}
	.badges .prem {
		background: var(--glow);
		border-color: transparent;
	}
	.badges .since {
		border-color: var(--line);
		font-weight: 500;
		color: var(--muted);
	}
	.btns {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
	}
	.btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-height: 48px;
		padding: 0 20px;
		border-radius: 999px;
		border: 1.5px solid var(--ink);
		background: var(--bg);
		color: var(--ink);
		text-decoration: none;
		font: 600 15px var(--font);
		cursor: pointer;
	}
	.btn.p {
		background: var(--accent);
		border-color: var(--accent);
		color: #fff;
	}
	.record {
		margin-top: 16px;
	}
	.stats {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 12px;
	}
	.stats div {
		background: var(--tile);
		border-radius: 20px;
		padding: clamp(14px, 2vw, 22px);
	}
	.stats b {
		display: block;
		font-weight: 300;
		font-size: clamp(32px, 5vw, 52px);
		letter-spacing: -0.04em;
		line-height: 1;
	}
	.stats small {
		display: block;
		margin-top: 6px;
		color: var(--muted);
		font-size: 13px;
	}
	.note {
		margin: 10px 2px 0;
		color: var(--muted);
		font-size: 13px;
	}
	.note.fresh {
		margin: 0;
		background: var(--tile);
		border-radius: 20px;
		padding: 18px 20px;
		font-size: 15px;
	}
	.grid {
		display: grid;
		grid-template-columns: minmax(0, 1fr) 320px;
		gap: 28px;
		margin-top: 32px;
		align-items: start;
	}
	@media (max-width: 820px) {
		.grid {
			grid-template-columns: 1fr;
		}
		.stats b {
			font-size: 30px;
		}
	}
	.block + .block {
		margin-top: 30px;
	}
	h2 {
		margin: 0;
		font-weight: 500;
		font-size: 21px;
		letter-spacing: -0.01em;
	}
	.sub {
		margin: 6px 0 0;
		color: var(--muted);
		line-height: 1.5;
	}
	.about {
		margin: 10px 0 0;
		font-size: 17px;
		line-height: 1.6;
	}
	.chips {
		list-style: none;
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		margin: 12px 0 0;
		padding: 0;
	}
	.chips li {
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 7px 13px;
		font-size: 14px;
		font-weight: 500;
	}
	.chips a {
		color: var(--ink);
		text-decoration: none;
	}
	.area {
		background: var(--tile);
		border-color: var(--line);
		padding: 20px;
	}
	.area :global(.area) {
		margin-top: 12px;
		border-radius: 14px;
		background: var(--bg);
	}
	.claim {
		margin-top: 48px;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 16px 28px;
		background: var(--ink);
		color: var(--bg);
		border-radius: 28px;
		padding: clamp(22px, 4vw, 36px);
	}
	.claim h2 {
		font-weight: 400;
		font-size: clamp(24px, 3vw, 32px);
	}
	.claim p {
		margin: 6px 0 0;
		opacity: 0.75;
	}
	.foot {
		max-width: 1000px;
		margin: 0 auto;
		padding: 0 clamp(16px, 4vw, 48px) 40px;
		font-size: 14px;
	}
	.foot a {
		color: var(--muted);
		margin-right: 16px;
	}
</style>
