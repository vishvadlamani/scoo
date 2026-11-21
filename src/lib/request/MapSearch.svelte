<!-- The lookup's checklist under the map. Each line turns on as that part of the lookup runs and
     ticks when it is done; the words come from the real answer, never a stand-in. -->
<script lang="ts">
	import type { SearchView } from './flow.ts';

	let { view }: { view: SearchView } = $props();
</script>

<div class="searchbox" id="searchbox">
	<h1 id="s-title">{view.title}</h1>
	<ul class="checks" id="s-checks" aria-live="polite">
		<li class={view.marks[0]} data-k="area">
			<i></i>{#if view.place}<span>Found <b>{view.zip}</b> · {view.place}</span>{:else}<span
					>Finding <b id="s-zip">{view.zip}</b> on the map</span
				>{/if}
		</li>
		<li class={view.marks[1]} data-k="pros"><i></i><span id="s-pros">{view.pros}</span></li>
		<li class={view.marks[2]} data-k="launch"><i></i><span id="s-launch">{view.launch}</span></li>
	</ul>
</div>

<style>
	.searchbox {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 16px;
		width: 100%;
		max-height: 420px;
		overflow: hidden;
		transition:
			max-height 0.6s cubic-bezier(0.5, 0, 0.3, 1),
			opacity 0.3s ease;
	}
	/* The page's notify state folds the checklist away once the area is known. */
	:global(.notify) .searchbox {
		max-height: 0;
		opacity: 0;
		margin-top: -16px;
	}
	.searchbox h1 {
		font-size: clamp(28px, 4vw, 38px);
	}
	.checks {
		list-style: none;
		margin: 4px 0 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 12px;
		width: 100%;
		max-width: 360px;
		text-align: left;
	}
	.checks li {
		display: flex;
		align-items: center;
		gap: 12px;
		font-size: 16px;
		color: var(--muted);
		opacity: 0.35;
		transition: opacity 0.3s;
	}
	.checks li.run,
	.checks li.ok {
		opacity: 1;
		color: var(--ink);
	}
	.checks i {
		flex: 0 0 auto;
		width: 22px;
		height: 22px;
		border-radius: 99px;
		border: 2px solid var(--line);
		position: relative;
	}
	.checks li.run i {
		border-color: var(--line);
		border-top-color: var(--accent);
		animation: spin 0.7s linear infinite;
	}
	.checks li.ok i {
		border-color: var(--accent);
		background: var(--accent);
	}
	.checks li.ok i::after {
		content: '';
		position: absolute;
		left: 6px;
		top: 3px;
		width: 5px;
		height: 9px;
		border: solid #fff;
		border-width: 0 2px 2px 0;
		transform: rotate(45deg);
	}
	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}
</style>
