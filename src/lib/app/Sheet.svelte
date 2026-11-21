<!-- Their launch area filling up toward the goal: place, position, progress, pros and invites.
     It is in the page from the start, empty and off-screen, so the bar grows when numbers land. -->
<script lang="ts">
	import { fmt, tradeName } from './format.ts';
	import type { Me } from './types.ts';

	let { data, on, onshare, onpro }: { data: Me | null; on: boolean; onshare: () => void; onpro: () => void } = $props();

	let min = $state(false);
	const width = $derived(data ? Math.max(2, Math.min(100, (data.waiting / data.goal) * 100)) : 0);
</script>

<section class="sheet" class:on class:min aria-live="polite">
	<button
		class="handle"
		aria-label={min ? 'Show more' : 'Show less'}
		aria-expanded={!min}
		onclick={() => (min = !min)}><i></i></button
	>
	<span class="chip"
		><svg viewBox="0 0 24 24" aria-hidden="true"
			><path d="M12 21s-7-6.3-7-11.5A7 7 0 0 1 19 9.5C19 14.7 12 21 12 21Z" /><circle cx="12" cy="9.5" r="2.5" /></svg
		><span>{data ? `${data.place || 'Your area'} · ${data.zip}` : ''}</span></span
	>
	<h1>{data ? (data.town ? `Scoo is coming to ${data.town}` : 'Scoo is coming to your area') : ''}</h1>
	<div class="prog">
		<div class="bar"><i style:width="{width}%"></i></div>
		<small
			><span
				>{data
					? `${fmt(data.waiting)} ${data.waiting === 1 ? 'neighbour' : 'neighbours'} waiting · you're #${fmt(data.position)}`
					: ''}</span
			><span>{data ? `${fmt(data.goal)} to open` : ''}</span></small
		>
	</div>
	<div class="more">
		<div class="rows">
			<div class="row">
				<span class="ic"
					><svg viewBox="0 0 24 24"
						><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z" /></svg
					></span
				>
				{#if data}
					{#if data.pros.length}
						<span
							><b
								>{data.pros
									.map((p) => `${p.n} ${tradeName(p.trade, p.n)}`)
									.slice(0, 3)
									.join(' · ')}</b
							>
							joined in {data.areaLabel}<small>More pros means a faster launch.</small></span
						>
					{:else}
						<span
							><b>Pros are joining soon</b><small>Know a great one? Invite them to claim a free AI receptionist.</small></span
						>
					{/if}
				{/if}
			</div>
			<div class="row">
				<span class="ic"
					><svg viewBox="0 0 24 24"
						><circle cx="9" cy="8" r="3" /><path d="M3 20c0-3 3-5 6-5s6 2 6 5M16 11a3 3 0 1 0 0-6M21 20c0-2.4-1.7-4.3-4-4.8" /></svg
					></span
				>
				{#if data}
					{#if data.invited}
						<span
							><b>{data.invited} {data.invited === 1 ? 'person' : 'people'}</b> joined through you<small
								>Every invite moves {data.area} closer.</small
							></span
						>
					{:else}
						<span><b>Invite neighbours to open {data.area} sooner</b><small>You each get $10 credit.</small></span>
					{/if}
				{/if}
			</div>
		</div>
	</div>
	<div class="acts">
		<button class="p" onclick={onshare}>Invite friends</button><button onclick={onpro}>Know a pro?</button>
	</div>
</section>

<style>
	.sheet {
		position: fixed;
		left: 12px;
		right: 12px;
		bottom: max(12px, env(safe-area-inset-bottom));
		z-index: 2;
		background: var(--card);
		border: 1.5px solid var(--ink);
		border-radius: 24px;
		padding: 18px 18px 16px;
		box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);
		display: flex;
		flex-direction: column;
		gap: 12px;
		max-width: 440px;
		transform: translateY(130%);
		transition: transform 0.7s cubic-bezier(0.3, 0.8, 0.3, 1);
	}
	.sheet.on {
		transform: none;
	}
	@media (min-width: 880px) {
		.sheet {
			left: 24px;
			right: auto;
			bottom: 24px;
			width: 400px;
		}
	}
	.chip {
		align-self: flex-start;
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 5px 11px;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		font-size: 13px;
		font-weight: 500;
	}
	.chip svg {
		width: 14px;
		height: 14px;
		fill: var(--accent);
		stroke: var(--ink);
		stroke-width: 1.6;
	}
	.chip circle {
		fill: var(--bg);
	}
	h1 {
		margin: 0;
		font-weight: 400;
		font-size: 26px;
		letter-spacing: -0.02em;
		line-height: 1.15;
	}
	.prog {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.bar {
		height: 10px;
		border-radius: 99px;
		border: 1.5px solid var(--ink);
		overflow: hidden;
	}
	.bar i {
		display: block;
		height: 100%;
		width: 0;
		background: var(--accent);
		transition: width 1.4s cubic-bezier(0.3, 0.8, 0.3, 1);
	}
	.prog small {
		display: flex;
		justify-content: space-between;
		color: var(--muted);
		font-size: 13px;
	}
	.rows {
		display: grid;
		gap: 8px;
		font-size: 15px;
	}
	.row {
		display: flex;
		gap: 10px;
		align-items: flex-start;
		line-height: 1.35;
	}
	.row b {
		font-weight: 600;
	}
	.row .ic {
		flex: 0 0 auto;
		width: 28px;
		height: 28px;
		border-radius: 99px;
		display: grid;
		place-items: center;
		background: var(--soft);
	}
	.row .ic svg {
		width: 16px;
		height: 16px;
		fill: none;
		stroke: var(--ink);
		stroke-width: 2;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.row small {
		display: block;
		color: var(--muted);
		font-size: 13px;
	}
	.handle {
		align-self: center;
		margin: -8px 0 -4px;
		width: 60px;
		height: 22px;
		border: 0;
		background: none;
		cursor: pointer;
		display: grid;
		place-items: center;
	}
	.handle i {
		width: 40px;
		height: 5px;
		border-radius: 99px;
		background: var(--line);
	}
	.more {
		display: grid;
		gap: 12px;
		overflow: hidden;
		max-height: 260px;
		transition:
			max-height 0.45s cubic-bezier(0.3, 0.8, 0.3, 1),
			opacity 0.3s;
	}
	.sheet.min .more {
		max-height: 0;
		opacity: 0;
		margin-top: -12px;
	}
	@media (min-width: 880px) {
		.handle {
			display: none;
		}
	}
	.acts {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 8px;
	}
	.acts button {
		min-height: 46px;
		border-radius: 999px;
		border: 1.5px solid var(--ink);
		background: var(--bg);
		color: var(--ink);
		font:
			600 15px 'Hanken Grotesk',
			sans-serif;
		cursor: pointer;
	}
	.acts .p {
		background: var(--accent);
		border-color: var(--accent);
		color: #fff;
	}
</style>
