<!-- The full-screen line-art map: their area outlined and filling toward the goal, their pin, and
     nearby areas tinted by their real counts. MapLibre touches window, so it is loaded in onMount
     and never during prerender. -->
<script lang="ts">
	import 'maplibre-gl/dist/maplibre-gl.css';
	import { onMount } from 'svelte';
	import type { GeoJSONSource, Map as MlMap, Marker } from 'maplibre-gl';
	import { mapColors, mapStyle } from './mapStyle.ts';
	import { fmt } from './format.ts';
	import type { LonLat, Me } from './types.ts';

	let { data, onready }: { data: Me | null; onready: () => void } = $props();

	let container: HTMLDivElement;
	let map: MlMap | null = $state(null);
	let maplibre: typeof import('maplibre-gl') | null = null;
	let placed = false;
	let markers: Marker[] = [];
	let shown = 0;
	let anim = 0;

	const ring = (p: LonLat[]): LonLat[] => [...p, p[0]];
	const polygon = (p: LonLat[]) => ({ type: 'Feature' as const, properties: {}, geometry: { type: 'Polygon' as const, coordinates: [ring(p)] } });
	const empty = { type: 'FeatureCollection' as const, features: [] };
	const source = (m: MlMap, id: string) => m.getSource<GeoJSONSource>(id);

	// The whole area deepens in colour as it fills toward the launch goal.
	function setFill(m: MlMap, d: Me, p: number) {
		if (!m.getLayer('fill') || !d.outline) return;
		source(m, 'fill')?.setData(polygon(d.outline));
		m.setPaintProperty('fill', 'fill-opacity', 0.06 + 0.38 * Math.max(0, Math.min(1, p)));
	}

	function animateFill(m: MlMap, d: Me, to: number) {
		cancelAnimationFrame(anim);
		const from = shown;
		const t0 = performance.now();
		const dur = matchMedia('(prefers-reduced-motion: reduce)').matches ? 1 : 1600;
		const step = (t: number) => {
			const k = Math.min(1, (t - t0) / dur);
			const e = 1 - Math.pow(1 - k, 3);
			shown = from + (to - from) * e;
			setFill(m, d, shown);
			if (k < 1) anim = requestAnimationFrame(step);
		};
		anim = requestAnimationFrame(step);
	}

	// Pin, labels and framing are placed once, from the first answer; polls only update the
	// shapes and the fill.
	function place(m: MlMap, ml: NonNullable<typeof maplibre>, d: Me) {
		markers.forEach((x) => x.remove());
		markers = [];
		if (d.pin) {
			const el = document.createElement('div');
			el.className = 'me';
			el.setAttribute('aria-label', 'You');
			markers.push(new ml.Marker({ element: el }).setLngLat([d.pin[1], d.pin[0]]).addTo(m));
		}
		for (const n of d.nearby.filter((n) => n.waiting > 0)) {
			const e = document.createElement('div');
			e.className = 'lbl';
			const b = document.createElement('b');
			b.textContent = fmt(n.waiting);
			// Built as nodes rather than markup: the name is data, not HTML.
			e.textContent = `${n.name} · `;
			e.appendChild(b);
			e.appendChild(document.createTextNode(' waiting'));
			markers.push(new ml.Marker({ element: e }).setLngLat(n.center).addTo(m));
		}
		const pts: LonLat[] = (d.outline ?? []).concat(d.pin ? [[d.pin[1], d.pin[0]]] : []);
		if (pts.length) {
			const b = new ml.LngLatBounds(pts[0], pts[0]);
			pts.forEach((p) => b.extend(p));
			// Keep the area clear of the sheet: beside it on wide screens, above it on phones.
			const wide = innerWidth >= 880;
			m.fitBounds(b, {
				padding: wide
					? { top: 90, bottom: 60, left: 460, right: 60 }
					: { top: 90, bottom: Math.min(380, innerHeight * 0.48), left: 24, right: 24 },
				duration: 2200,
				maxZoom: 12
			});
		}
	}

	$effect(() => {
		const m = map;
		const d = data;
		if (!m || !d || !maplibre) return;
		source(m, 'area')?.setData(d.outline ? polygon(d.outline) : empty);
		source(m, 'near')?.setData({
			type: 'FeatureCollection',
			features: d.nearby
				.filter((n) => n.waiting > 0)
				.map((n) => ({ ...polygon(n.outline), properties: { w: n.waiting } }))
		});
		animateFill(m, d, d.waiting / d.goal);
		if (!placed) {
			placed = true;
			place(m, maplibre, d);
		}
	});

	onMount(() => {
		let gone = false;
		let m: MlMap | undefined;
		(async () => {
			const ml = await import('maplibre-gl');
			if (gone) return;
			maplibre = ml;
			const C = mapColors();
			m = new ml.Map({
				container,
				style: mapStyle(C),
				center: [-96.8, 32.9],
				zoom: 8.5,
				attributionControl: { compact: true },
				pitchWithRotate: false,
				dragRotate: false
			});
			m.touchZoomRotate.disableRotation();
			const loaded = m;
			loaded.on('load', () => {
				loaded.addSource('near', { type: 'geojson', data: empty });
				loaded.addLayer({
					id: 'near-fill',
					type: 'fill',
					source: 'near',
					paint: { 'fill-color': C.accent, 'fill-opacity': ['interpolate', ['linear'], ['get', 'w'], 1, 0.04, 1000, 0.22] }
				});
				loaded.addSource('area', { type: 'geojson', data: empty });
				loaded.addSource('fill', { type: 'geojson', data: empty });
				loaded.addLayer({
					id: 'fill',
					type: 'fill',
					source: 'fill',
					paint: { 'fill-color': C.accent, 'fill-opacity': 0.06, 'fill-opacity-transition': { duration: 0 } }
				});
				loaded.addLayer({ id: 'area-line', type: 'line', source: 'area', paint: { 'line-color': C.accent, 'line-width': 2.5 } });
				map = loaded;
				onready();
			});
		})();
		return () => {
			gone = true;
			cancelAnimationFrame(anim);
			m?.remove();
		};
	});
</script>

<div class="map" bind:this={container} role="img" aria-label="Map of your area"></div>

<style>
	.map {
		position: fixed;
		inset: 0;
	}
	.map :global(.me) {
		width: 22px;
		height: 22px;
		border-radius: 99px;
		background: var(--accent);
		border: 3px solid var(--bg);
		box-shadow: 0 0 0 1.5px var(--ink);
	}
	.map :global(.me::after) {
		content: '';
		position: absolute;
		inset: -14px;
		border-radius: 99px;
		border: 2px solid var(--accent);
		animation: pulse 2.2s ease-out infinite;
	}
	@keyframes pulse {
		from {
			transform: scale(0.4);
			opacity: 0.9;
		}
		to {
			transform: scale(1.6);
			opacity: 0;
		}
	}
	.map :global(.lbl) {
		font:
			500 12px 'Hanken Grotesk',
			sans-serif;
		color: var(--ink);
		background: var(--card);
		border: 1px solid var(--line);
		border-radius: 999px;
		padding: 3px 9px;
		white-space: nowrap;
	}
	.map :global(.lbl b) {
		color: var(--accent);
		font-weight: 600;
	}
	.map :global(.maplibregl-ctrl-attrib) {
		font-size: 10px;
	}
</style>
