<!-- An exchange's page: the network's own corner of Scoo, with its members, rules and area. -->
<script lang="ts">
	import SiteHeader from '#lib/profiles/SiteHeader.svelte';
	import ExampleBar from '#lib/profiles/ExampleBar.svelte';
	import ProCard from '#lib/profiles/ProCard.svelte';
	import AreaOutline from '#lib/profiles/AreaOutline.svelte';
	import Seo from '#lib/profiles/Seo.svelte';
	import { initials, monthYear } from '#lib/profiles/format.ts';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
	const x = $derived(data.exchange);
	const where = $derived(x.area?.name ?? null);
	const description = $derived(
		x.tagline ?? `${x.name} is an exchange of local pros on Scoo${where ? ` serving ${where}` : ''}.`
	);
	const jsonLd = $derived(
		x.example
			? null
			: {
					'@context': 'https://schema.org',
					'@type': 'Organization',
					name: x.name,
					url: `https://scoo.app/x/${x.slug}`,
					description,
					...(where ? { areaServed: where } : {}),
					...(x.members.length ? { member: x.members.map((m) => ({ '@type': 'LocalBusiness', name: m.business, url: `https://scoo.app/p/${m.slug}` })) } : {})
				}
	);
</script>

<Seo title="{x.name}{where ? ` · ${where}` : ''} · Scoo" {description} path="/x/{x.slug}" index={!x.example} {jsonLd} />

{#if x.example}<ExampleBar what="An example exchange." href="/exchanges/start" cta="Start your own" />{/if}
<SiteHeader />

<main>
	<section class="hero">
		<div class="cover" aria-hidden="true"></div>
		<div class="head">
			<div class="av" aria-hidden="true">{initials(x.name)}</div>
			<div class="title">
				<h1>{x.name}</h1>
				<p class="url">scoo.app/x/{x.slug}{where ? ` · ${where}` : ''}</p>
			</div>
			<div class="btns">
				<a class="btn p" href="/pros">Join as a pro</a>
				<a class="btn" href="/request">Get a pro</a>
			</div>
		</div>
		{#if x.tagline}<p class="tagline">{x.tagline}</p>{/if}
		{#if x.trades.length}
			<ul class="chips" aria-label="Trades">
				{#each x.trades as t (t)}<li>{t}</li>{/each}
			</ul>
		{/if}
	</section>

	<div class="grid">
		<div class="main">
			{#if x.about}
				<section class="block">
					<h2>About</h2>
					<p class="about">{x.about}</p>
				</section>
			{/if}

			<section class="block" aria-labelledby="members">
				<div class="h2row">
					<h2 id="members">Members</h2>
					<span class="count">{x.members.length} {x.members.length === 1 ? 'pro' : 'pros'}</span>
				</div>
				{#if x.members.length}
					<div class="members">
						{#each x.members as pro (pro.slug)}<ProCard {pro} />{/each}
					</div>
				{:else}
					<p class="empty">Members appear here as pros join this exchange.</p>
				{/if}
			</section>

			{#if x.rules.length}
				<section class="block">
					<h2>House rules</h2>
					<p class="sub">Set by the exchange, in plain English. Scoo routes every call by them.</p>
					<ol class="rules">
						{#each x.rules as r, i (i)}<li>{r}</li>{/each}
					</ol>
				</section>
			{/if}
		</div>

		<aside class="side">
			<section class="card">
				<h2>This exchange</h2>
				{#if x.numbers}
					<div class="stats">
						<div><b>{x.numbers.members}</b><small>Members</small></div>
						<div><b>{x.numbers.sources}</b><small>Call sources</small></div>
						<div><b>{x.numbers.answerSecs}s</b><small>Avg. pick-up</small></div>
						<div><b>{x.numbers.jobsThisWeek}</b><small>Jobs this week</small></div>
					</div>
				{:else}
					<p class="sub">Live numbers appear here once Scoo opens in this area.</p>
				{/if}
				<p class="meta">On Scoo since {monthYear(x.openedAt)} · run by {x.org}</p>
			</section>

			{#if x.activity.length}
				<section class="card">
					<h2>Recent activity</h2>
					<ul class="feed">
						{#each x.activity as a, i (i)}<li><span class="dot" aria-hidden="true"></span><span>{a.text}<small>{a.when}</small></span></li>{/each}
					</ul>
				</section>
			{/if}

			{#if x.area}
				<section class="card">
					<h2>Where members work</h2>
					<AreaOutline outline={x.area.outline} label={x.area.name} />
					<p class="meta">{x.area.name}</p>
				</section>
			{/if}

			<section class="card cta">
				<h2>Run a network like this?</h2>
				<p class="sub">Your own page, your rules, and you earn on every match.</p>
				<a class="btn p" href="/exchanges/start">Start an exchange</a>
			</section>
		</aside>
	</div>
</main>

<footer class="foot">
	<a href="/">Scoo</a><a href="/pros">For pros</a><a href="/exchanges/start">Start an exchange</a><a href="/terms">Terms</a><a href="/privacy">Privacy</a>
</footer>

<style>
	main {
		max-width: 1120px;
		margin: 0 auto;
		padding: 12px clamp(16px, 4vw, 48px) 64px;
	}
	.hero {
		border: 1.5px solid var(--ink);
		border-radius: 28px;
		overflow: hidden;
		padding-bottom: 22px;
	}
	.cover {
		height: clamp(110px, 16vw, 170px);
		background: var(--tint);
		border-bottom: 1.5px solid var(--ink);
		background-image: radial-gradient(var(--soft) 1.5px, transparent 1.5px);
		background-size: 16px 16px;
	}
	.head {
		display: flex;
		gap: 18px;
		align-items: flex-start;
		flex-wrap: wrap;
		padding: 0 clamp(18px, 3vw, 28px);
	}
	.av {
		/* the avatar alone overlaps the cover; the name sits below it */
		margin-top: -44px;
		width: 88px;
		height: 88px;
		border-radius: 24px;
		border: 1.5px solid var(--ink);
		background: var(--bg);
		display: grid;
		place-items: center;
		font: 600 30px var(--font);
		color: var(--accent);
	}
	.title {
		min-width: 0;
		flex: 1 1 260px;
		padding-top: 14px;
	}
	h1 {
		margin: 0;
		font-weight: 400;
		font-size: clamp(30px, 4vw, 44px);
		letter-spacing: -0.03em;
		line-height: 1.05;
	}
	.url {
		margin: 6px 0 0;
		color: var(--muted);
		font-size: 14px;
	}
	.btns {
		display: flex;
		gap: 8px;
		flex-wrap: wrap;
		padding-top: 16px;
	}
	.btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-height: 44px;
		padding: 0 18px;
		border-radius: 999px;
		border: 1.5px solid var(--ink);
		color: var(--ink);
		text-decoration: none;
		font-weight: 600;
		font-size: 15px;
		background: var(--bg);
	}
	.btn.p {
		background: var(--accent);
		border-color: var(--accent);
		color: #fff;
	}
	.tagline {
		margin: 16px clamp(18px, 3vw, 28px) 0;
		font-size: 18px;
		line-height: 1.5;
		max-width: 720px;
	}
	.chips {
		list-style: none;
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		margin: 14px clamp(18px, 3vw, 28px) 0;
		padding: 0;
	}
	.chips li {
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 6px 12px;
		font-size: 13px;
		font-weight: 500;
	}
	.grid {
		display: grid;
		grid-template-columns: minmax(0, 1fr) 340px;
		gap: 28px;
		margin-top: 28px;
		align-items: start;
	}
	@media (max-width: 900px) {
		.grid {
			grid-template-columns: 1fr;
		}
	}
	.block + .block {
		margin-top: 36px;
	}
	h2 {
		margin: 0;
		font-weight: 500;
		font-size: 22px;
		letter-spacing: -0.01em;
	}
	.h2row {
		display: flex;
		align-items: baseline;
		gap: 10px;
	}
	.count,
	.sub,
	.meta {
		color: var(--muted);
	}
	.count {
		font-size: 15px;
	}
	.sub {
		margin: 6px 0 0;
		line-height: 1.5;
	}
	.meta {
		margin: 12px 0 0;
		font-size: 14px;
	}
	.about {
		margin: 10px 0 0;
		font-size: 17px;
		line-height: 1.6;
		max-width: 680px;
	}
	.members {
		margin-top: 14px;
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
		gap: 12px;
	}
	.empty {
		margin: 12px 0 0;
		padding: 18px;
		border: 1.5px dashed var(--line);
		border-radius: 20px;
		color: var(--muted);
	}
	.rules {
		margin: 14px 0 0;
		padding: 0;
		list-style: none;
		counter-reset: r;
		display: grid;
		gap: 10px;
	}
	.rules li {
		counter-increment: r;
		display: flex;
		gap: 12px;
		align-items: flex-start;
		line-height: 1.45;
		border: 1.5px solid var(--line);
		border-radius: 16px;
		padding: 12px 14px;
	}
	.rules li::before {
		content: counter(r);
		flex: 0 0 auto;
		width: 26px;
		height: 26px;
		border-radius: 99px;
		background: var(--accent);
		color: #fff;
		display: grid;
		place-items: center;
		font-size: 13px;
		font-weight: 600;
	}
	.side {
		display: grid;
		gap: 16px;
	}
	.card {
		background: var(--tile);
		border: 1.5px solid var(--line);
		border-radius: 24px;
		padding: 20px;
	}
	.card h2 {
		font-size: 18px;
	}
	.stats {
		margin-top: 12px;
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 8px;
	}
	.stats div {
		background: var(--bg);
		border-radius: 14px;
		padding: 12px;
	}
	.stats b {
		display: block;
		font-size: 24px;
		font-weight: 500;
		letter-spacing: -0.02em;
	}
	.stats small {
		color: var(--muted);
		font-size: 12px;
	}
	.feed {
		list-style: none;
		margin: 12px 0 0;
		padding: 0;
		display: grid;
		gap: 12px;
	}
	.feed li {
		display: flex;
		gap: 10px;
		align-items: flex-start;
		font-size: 14px;
		line-height: 1.4;
	}
	.feed small {
		display: block;
		color: var(--muted);
		font-size: 12px;
	}
	.dot {
		flex: 0 0 auto;
		width: 8px;
		height: 8px;
		margin-top: 6px;
		border-radius: 9px;
		background: var(--green);
	}
	.card :global(.area) {
		margin-top: 12px;
		border-radius: 14px;
		background: var(--bg);
	}
	.cta {
		background: var(--ink);
		color: var(--bg);
		border-color: var(--ink);
	}
	.cta .sub {
		color: inherit;
		opacity: 0.75;
	}
	.cta .btn {
		margin-top: 14px;
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
