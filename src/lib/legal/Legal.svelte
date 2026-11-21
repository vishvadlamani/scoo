<!-- The frame for the terms and the privacy policy. Drafts: nothing here is legal advice. -->
<script lang="ts">
	import type { Snippet } from 'svelte';
	import Mark from '#lib/brand/Mark.svelte';

	let { title, description, children }: { title: string; description: string; children: Snippet } = $props();
</script>

<svelte:head>
	<title>{title} · Scoo</title>
	<meta name="description" content={description} />
</svelte:head>

<header>
	<a class="logo" href="/" aria-label="Scoo home"><Mark /><span>scoo</span></a>
	<nav><a href="/terms">Terms</a><a href="/privacy">Privacy</a></nav>
</header>
<main>
	<p class="draft">Draft, pending legal review.</p>
	{@render children()}
</main>
<footer><a href="/">Home</a><a href="/pros">For pros</a><a href="/terms">Terms</a><a href="/privacy">Privacy</a></footer>

<style>
	header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 20px clamp(16px, 4vw, 48px);
		max-width: 1100px;
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
	nav a {
		color: var(--ink);
		margin-left: 18px;
		font-size: 15px;
	}
	main {
		max-width: 720px;
		margin: 0 auto;
		padding: 8px 20px 72px;
		line-height: 1.65;
		font-size: 17px;
	}
	main :global(h1) {
		font-weight: 300;
		font-size: clamp(36px, 5vw, 52px);
		letter-spacing: -0.03em;
		margin: 16px 0 4px;
	}
	main :global(h2) {
		font-weight: 500;
		font-size: 21px;
		margin: 36px 0 8px;
	}
	main :global(.meta) {
		color: var(--muted);
		margin: 0 0 24px;
	}
	.draft {
		border: 1.5px solid var(--accent);
		border-radius: 14px;
		padding: 12px 16px;
		font-size: 15px;
		margin: 0 0 8px;
	}
	main :global(ul) {
		padding-left: 20px;
	}
	main :global(li) {
		margin: 6px 0;
	}
	main :global(a) {
		color: var(--ink);
	}
	footer {
		max-width: 720px;
		margin: 0 auto;
		padding: 24px 20px 48px;
		border-top: 1.5px solid var(--line);
		color: var(--muted);
		font-size: 14px;
	}
	footer a {
		color: var(--muted);
		margin-right: 16px;
	}
</style>
