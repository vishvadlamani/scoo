<!-- The one follow-up question, so the right pro calls. A "Yes" to the doctor's emergency question
     stops the flow here: Scoo is not for emergencies. -->
<script lang="ts">
	import { ART_ASK } from './art.ts';

	let {
		title,
		choices,
		emergency,
		onpick
	}: { title: string; choices: string[]; emergency: boolean; onpick: (answer: string) => void } = $props();
</script>

<div class="art" id="q-art">{@html ART_ASK}</div>
<h1 id="q-title">{emergency ? 'Please call 911 now.' : title}</h1>
<p class="lead">A quick question so the right pro calls you.</p>
<div class="choices" id="q-choices">
	{#if emergency}
		<p class="lead">Scoo is not for emergencies.</p>
	{:else}
		{#each choices as choice (choice)}
			<button type="button" onclick={() => onpick(choice)}>{choice}</button>
		{/each}
	{/if}
</div>

<style>
	.choices {
		display: grid;
		grid-template-columns: 1fr;
		gap: 10px;
		width: 100%;
	}
	.choices button {
		min-height: 54px;
		border: 1.5px solid var(--ink);
		border-radius: 16px;
		background: var(--bg);
		color: var(--ink);
		font: 500 17px 'Hanken Grotesk', sans-serif;
		cursor: pointer;
		text-align: left;
		padding: 0 18px;
	}
	.choices button:hover {
		background: var(--soft);
	}
</style>
