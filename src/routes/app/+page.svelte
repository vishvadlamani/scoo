<!-- The signed-in home screen: a full-screen line-art map of their area, the request bar floating on
     top, and their launch area filling up toward the goal. Every number comes from /api/me (real,
     counted by area). Updates by polling for now; Durable Objects push later. -->
<script lang="ts">
	import { onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import Mark from '#lib/brand/Mark.svelte';
	import AppMap from '#lib/app/AppMap.svelte';
	import Sheet from '#lib/app/Sheet.svelte';
	import Toast from '#lib/app/Toast.svelte';
	import type { Me } from '#lib/app/types.ts';

	let data: Me | null = $state(null);
	let gate = $state(false);
	let sheetOn = $state(false);
	let q = $state('');
	let toast: ReturnType<typeof Toast>;
	let poll: ReturnType<typeof setInterval> | undefined;
	let reveal: ReturnType<typeof setTimeout> | undefined;

	// null when signed out (and the gate goes up); throws on anything else unexpected.
	async function load(): Promise<Me | null> {
		const r = await fetch('/api/me', { credentials: 'same-origin' });
		if (r.status === 401) {
			gate = true;
			return null;
		}
		if (!r.ok) throw new Error(`/api/me answered ${r.status}`);
		return (await r.json()) as Me;
	}

	const total = (d: Me) => d.pros.reduce((a, p) => a + p.n, 0);

	async function refresh() {
		const d = await load().catch(() => null);
		if (!d || !data) return;
		const was = data;
		if (d.waiting > was.waiting) {
			const n = d.waiting - was.waiting;
			toast.show(`+${n} ${n === 1 ? 'neighbour' : 'neighbours'} just joined in ${d.areaLabel}`);
		} else if (d.invited > was.invited) toast.show('Someone joined through your invite');
		if (total(d) > total(was)) toast.show(`A new pro joined in ${d.areaLabel}`);
		data = d;
	}

	// The map asks for their numbers once it can draw them.
	async function start() {
		const d = await load().catch(() => null);
		if (!d) return;
		data = d;
		reveal = setTimeout(() => (sheetOn = true), 400);
		// Live: poll for now (a Durable Object will push these later). Only real changes are announced.
		const every = Number(new URLSearchParams(location.search).get('poll')) || 20;
		poll = setInterval(refresh, every * 1000);
	}

	onDestroy(() => {
		clearInterval(poll);
		clearTimeout(reveal);
	});

	function ask(e: SubmitEvent) {
		e.preventDefault();
		const v = q.trim();
		goto('/request' + (v ? '?q=' + encodeURIComponent(v) : ''));
	}

	async function share(url: string, text: string) {
		if (navigator.share) {
			try {
				await navigator.share({ text, url });
			} catch {
				// They closed the share sheet: nothing to say.
			}
		} else {
			await navigator.clipboard.writeText(url);
			toast.show('Link copied');
		}
	}

	const invite = () =>
		data &&
		share(
			`https://scoo.app/r/${data.code}`,
			`I'm on the Scoo early list: a pro calls you back in 60 seconds. Join with my link and we both get $10.`
		);
	const knowPro = () =>
		data &&
		share(
			`https://scoo.app/pro/${data.code}`,
			`Thought of you: Scoo gives pros a free AI receptionist that answers the calls you miss and books the job. Claim yours here.`
		);
</script>

<svelte:head>
	<title>Scoo · Your area</title>
</svelte:head>

<AppMap {data} onready={start} />
<div class="top">
	<a class="logo" href="/" aria-label="Scoo home"><Mark /></a>
	<form class="ask" role="search" onsubmit={ask}>
		<label for="q" class="vh">What do you need?</label>
		<input id="q" placeholder="What do you need?" autocomplete="off" bind:value={q} />
		<button aria-label="Ask Scoo"><svg viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6" /></svg></button>
	</form>
</div>
<Toast bind:this={toast} />
<Sheet {data} on={sheetOn} onshare={invite} onpro={knowPro} />
{#if gate}
	<div class="gate">
		<div>
			<h2>Join to see your area</h2>
			<p>Tell Scoo what you need and save your spot.</p>
			<a href="/request">Get started</a>
		</div>
	</div>
{/if}

<style>
	.top {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		display: flex;
		gap: 10px;
		align-items: center;
		padding: max(14px, env(safe-area-inset-top)) 14px 0;
		pointer-events: none;
		z-index: 2;
	}
	.top > * {
		pointer-events: auto;
	}
	@media (min-width: 880px) {
		.top {
			padding: 24px 24px 0;
		}
	}
	.logo {
		display: grid;
		place-items: center;
		width: 50px;
		height: 50px;
		border-radius: 999px;
		background: var(--card);
		border: 1.5px solid var(--ink);
		flex: 0 0 auto;
		color: var(--ink);
	}
	.logo :global(svg) {
		height: 22px;
		width: auto;
	}
	.ask {
		flex: 1;
		display: flex;
		align-items: center;
		gap: 6px;
		min-width: 0;
		max-width: 560px;
		height: 50px;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		background: var(--card);
		padding: 0 5px 0 18px;
		box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
	}
	.ask input {
		flex: 1;
		min-width: 0;
		border: 0;
		outline: 0;
		background: transparent;
		color: var(--ink);
		font:
			400 17px 'Hanken Grotesk',
			sans-serif;
	}
	.ask button {
		display: grid;
		place-items: center;
		width: 40px;
		height: 40px;
		border: 0;
		border-radius: 999px;
		background: var(--accent);
		color: #fff;
		cursor: pointer;
	}
	.ask svg {
		width: 20px;
		height: 20px;
		fill: none;
		stroke: currentColor;
		stroke-width: 2.2;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.gate {
		position: fixed;
		inset: 0;
		display: grid;
		place-items: center;
		z-index: 5;
		background: var(--bg);
		text-align: center;
		padding: 24px;
	}
	.gate h2 {
		font-weight: 400;
		margin: 0;
	}
	.gate p {
		color: var(--muted);
	}
	.gate a {
		display: inline-block;
		margin-top: 14px;
		padding: 14px 22px;
		border-radius: 999px;
		background: var(--accent);
		color: #fff;
		text-decoration: none;
		font-weight: 600;
	}
</style>
