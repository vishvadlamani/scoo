<!-- One rounded input with the round coral arrow beside it: the need and the ZIP screens. Enter
     submits, as it would any form; the browser's own validation (required, pattern) runs first. -->
<script lang="ts">
	import type { HTMLInputAttributes } from 'svelte/elements';

	let {
		id,
		label,
		value = $bindable(''),
		form = $bindable(),
		onsubmit,
		...attrs
	}: {
		id: string;
		label: string;
		value?: string;
		form?: HTMLFormElement;
		onsubmit: () => void;
	} & Omit<HTMLInputAttributes, 'id' | 'value' | 'form'> = $props();
</script>

<form
	class="field"
	id="f-{id}"
	bind:this={form}
	onsubmit={(e) => {
		e.preventDefault();
		onsubmit();
	}}
>
	<label class="vh" for={id}>{label}</label>
	<input {id} bind:value {...attrs} />
	<button class="go" aria-label="Continue"><svg viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6" /></svg></button>
</form>

<style>
	.field {
		display: flex;
		align-items: center;
		gap: 6px;
		width: 100%;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 6px 6px 6px 20px;
		margin-top: 6px;
	}
	.field:focus-within {
		box-shadow: 0 0 0 4px var(--soft);
	}
	.field input {
		flex: 1;
		min-width: 0;
		border: 0;
		outline: 0;
		background: transparent;
		color: var(--ink);
		font: 400 18px 'Hanken Grotesk', sans-serif;
		min-height: 48px;
	}
	.go {
		display: grid;
		place-items: center;
		width: 48px;
		height: 48px;
		border-radius: 999px;
		border: 0;
		background: var(--accent);
		color: #fff;
		cursor: pointer;
	}
	.go svg {
		width: 22px;
		height: 22px;
		fill: none;
		stroke: currentColor;
		stroke-width: 2.2;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
</style>
