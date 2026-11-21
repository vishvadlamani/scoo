<!-- A pro on an exchange's member list: who they are, and what Scoo has counted about them. -->
<script lang="ts">
	import type { ProCard } from './types.ts';
	import { initials, monthYear, percent } from './format.ts';

	let { pro }: { pro: ProCard } = $props();
</script>

<a class="card" href="/p/{pro.slug}">
	<div class="top">
		<span class="av" aria-hidden="true">{initials(pro.business)}</span>
		<div class="who">
			<b>{pro.business}</b>
			<small>{pro.trade}{pro.place ? ` · ${pro.place.replace(/, [A-Z]{2}$/, '')}` : ''}</small>
		</div>
		{#if pro.premium}<span class="badge prem">Premium pro</span>{:else if pro.founding}<span class="badge">Founding</span>{/if}
	</div>
	{#if pro.record}
		<div class="stats">
			<div><b>{pro.record.jobsWon}</b><small>Jobs won</small></div>
			<div><b>{percent(pro.record.answerRate)}</b><small>Answered</small></div>
			<div><b>{pro.record.answerSecs}s</b><small>To pick up</small></div>
		</div>
	{:else}
		<p class="new">New on Scoo · since {monthYear(pro.memberSince)}</p>
	{/if}
</a>

<style>
	.card {
		display: grid;
		gap: 12px;
		padding: 16px;
		border: 1.5px solid var(--line);
		border-radius: 20px;
		background: var(--bg);
		color: var(--ink);
		text-decoration: none;
		transition:
			border-color 0.15s,
			transform 0.15s;
	}
	.card:hover {
		border-color: var(--ink);
		transform: translateY(-2px);
	}
	.top {
		display: flex;
		align-items: center;
		gap: 12px;
		min-width: 0;
	}
	.av {
		flex: 0 0 auto;
		width: 44px;
		height: 44px;
		border-radius: 99px;
		background: var(--soft);
		border: 1.5px solid var(--ink);
		display: grid;
		place-items: center;
		font-weight: 600;
		font-size: 15px;
	}
	.who {
		min-width: 0;
	}
	.who b {
		display: block;
		font-weight: 600;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.who small {
		color: var(--muted);
		font-size: 13px;
	}
	.badge {
		margin-left: auto;
		flex: 0 0 auto;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 3px 9px;
		font-size: 11px;
		font-weight: 600;
		white-space: nowrap;
	}
	.badge.prem {
		background: var(--glow);
		border-color: transparent;
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
		font-size: 17px;
		font-weight: 600;
	}
	.stats small {
		color: var(--muted);
		font-size: 11px;
	}
	.new {
		margin: 0;
		color: var(--muted);
		font-size: 13px;
		background: var(--tile);
		border-radius: 12px;
		padding: 10px 12px;
	}
</style>
