<!-- A service area drawn as line art: the launch area's outline, projected flat (longitude scaled
     by the cosine of the latitude, so shapes are not stretched) and fitted to the box. -->
<script lang="ts">
	import type { LonLat } from './types.ts';

	let { outline, label }: { outline: LonLat[]; label: string } = $props();

	const W = 320;
	const H = 200;
	const PAD = 18;

	const path = $derived.by(() => {
		if (outline.length < 3) return '';
		const lat0 = outline.reduce((s, p) => s + p[1], 0) / outline.length;
		const k = Math.cos((lat0 * Math.PI) / 180);
		const pts = outline.map(([lon, lat]) => [lon * k, -lat]);
		const xs = pts.map((p) => p[0]);
		const ys = pts.map((p) => p[1]);
		const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
		const s = Math.min((W - 2 * PAD) / (x1 - x0 || 1), (H - 2 * PAD) / (y1 - y0 || 1));
		const ox = (W - (x1 - x0) * s) / 2;
		const oy = (H - (y1 - y0) * s) / 2;
		return pts.map(([x, y], i) => `${i ? 'L' : 'M'}${(ox + (x - x0) * s).toFixed(1)} ${(oy + (y - y0) * s).toFixed(1)}`).join(' ') + 'Z';
	});
</script>

<svg class="area" viewBox="0 0 {W} {H}" role="img" aria-label="Service area: {label}">
	<defs>
		<pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" /></pattern>
	</defs>
	<rect class="grid" width={W} height={H} fill="url(#dots)" />
	<path class="fill" d={path} />
	<path class="edge" d={path} />
</svg>

<style>
	.area {
		width: 100%;
		height: auto;
		display: block;
	}
	.grid {
		opacity: 0.5;
	}
	pattern circle {
		fill: var(--line);
	}
	.fill {
		fill: var(--soft);
		opacity: 0.7;
	}
	.edge {
		fill: none;
		stroke: var(--accent);
		stroke-width: 2.2;
		stroke-linejoin: round;
	}
</style>
