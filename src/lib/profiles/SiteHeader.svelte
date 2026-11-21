<!-- The header on public pages that are not part of a flow: logo, the two audiences, and the main ask. -->
<script lang="ts">
	import Mark from '#lib/brand/Mark.svelte';
</script>

<header>
	<div class="in">
		<a class="logo" href="/" aria-label="Scoo home"><Mark /><span>scoo</span></a>
		<nav aria-label="Scoo">
			<a class="n" href="/pros">For pros</a>
			<a class="n" href="/exchanges/start">Exchanges</a>
			<a class="pill" href="/request">Get a pro</a>
		</nav>
	</div>
</header>

<style>
	header {
		position: sticky;
		top: 0;
		z-index: 20;
		padding: 12px clamp(16px, 4vw, 48px);
		background: color-mix(in srgb, var(--bg) 86%, transparent);
		backdrop-filter: saturate(1.4) blur(12px);
		-webkit-backdrop-filter: saturate(1.4) blur(12px);
	}
	.in {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
		max-width: 1120px;
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
		height: 34px;
		width: auto;
		color: var(--ink);
	}
	nav {
		display: flex;
		align-items: center;
		gap: 4px;
	}
	.n {
		color: var(--ink);
		text-decoration: none;
		font-size: 15px;
		padding: 10px 12px;
		border-radius: 999px;
	}
	.n:hover {
		background: var(--tile);
	}
	.pill {
		display: inline-flex;
		align-items: center;
		min-height: 42px;
		padding: 0 18px;
		margin-left: 6px;
		border-radius: 999px;
		background: var(--accent);
		color: #fff;
		text-decoration: none;
		font-weight: 600;
	}
	@media (max-width: 560px) {
		.n {
			display: none;
		}
	}
</style>
