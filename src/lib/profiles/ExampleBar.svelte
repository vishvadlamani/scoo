<!-- Shown on every example page, so nobody mistakes an invented business for a real one. -->
<script lang="ts">
	let { what, href, cta }: { what: string; href: string; cta: string } = $props();
</script>

<div class="bar" role="note">
	<span class="tag">EXAMPLE</span>
	<span class="txt">{what} Names and numbers are invented to show what Scoo will look like.</span>
	<a {href}>{cta} →</a>
</div>

<style>
	.bar {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 8px 12px;
		padding: 10px clamp(16px, 4vw, 48px);
		background: var(--tint);
		border-bottom: 1.5px solid var(--line);
		font-size: 14px;
	}
	.tag {
		background: var(--ink);
		color: var(--bg);
		font-size: 11px;
		font-weight: 600;
		letter-spacing: 1.5px;
		padding: 4px 9px;
		border-radius: 999px;
	}
	.txt {
		color: var(--muted);
		flex: 1 1 280px;
	}
	a {
		color: var(--ink);
		font-weight: 600;
	}
</style>
