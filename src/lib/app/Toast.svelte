<!-- One line at a time, near the top. A new message replaces the one showing and restarts its clock. -->
<script lang="ts">
	let message = $state('');
	let on = $state(false);
	let timer: ReturnType<typeof setTimeout> | undefined;

	export function show(m: string) {
		message = m;
		on = true;
		clearTimeout(timer);
		timer = setTimeout(() => (on = false), 3200);
	}

	$effect(() => () => clearTimeout(timer));
</script>

<div class="toast" class:on role="status">{message}</div>

<style>
	.toast {
		position: fixed;
		left: 50%;
		top: 84px;
		transform: translate(-50%, -20px);
		opacity: 0;
		z-index: 3;
		background: var(--ink);
		color: var(--bg);
		padding: 10px 16px;
		border-radius: 999px;
		font-size: 14px;
		font-weight: 500;
		transition: all 0.4s ease;
		white-space: nowrap;
	}
	.toast.on {
		opacity: 1;
		transform: translate(-50%, 0);
	}
</style>
