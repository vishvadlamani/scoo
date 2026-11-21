import type { StyleSpecification } from 'maplibre-gl';

/** The map's own palette. Tiles are drawn by MapLibre, not CSS, so it cannot read the page tokens. */
export type MapColors = {
	bg: string;
	water: string;
	park: string;
	road: string;
	minor: string;
	build: string;
	text: string;
	halo: string;
	accent: string;
};

export const LIGHT: MapColors = {
	bg: '#FFFFFF',
	water: '#D6E8FA',
	park: '#E4F2E1',
	road: '#C9C6BD',
	minor: '#E6E3DC',
	build: '#F2F0EA',
	text: '#55595f',
	halo: '#FFFFFF',
	accent: '#FF6B4A'
};

export const DARK: MapColors = {
	bg: '#0E0E10',
	water: '#16233a',
	park: '#14241a',
	road: '#3a3a40',
	minor: '#26262b',
	build: '#1b1b1f',
	text: '#c9cbd1',
	halo: '#0E0E10',
	accent: '#FF7A5C'
};

/** Dark when the system is, unless the page pins data-theme="light" (as the tokens in app.css do). */
export const mapColors = (): MapColors =>
	matchMedia('(prefers-color-scheme: dark)').matches && document.documentElement.dataset.theme !== 'light' ? DARK : LIGHT;

// A line-art style on OpenFreeMap's vector tiles: white ground, thin streets, quiet labels.
export const mapStyle = (C: MapColors): StyleSpecification => ({
	version: 8,
	glyphs: 'https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf',
	sources: {
		omt: {
			type: 'vector',
			url: 'https://tiles.openfreemap.org/planet',
			attribution:
				'<a href="https://openfreemap.org">OpenFreeMap</a> © <a href="https://www.openmaptiles.org/">OpenMapTiles</a> © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
		}
	},
	layers: [
		{ id: 'bg', type: 'background', paint: { 'background-color': C.bg } },
		{ id: 'park', type: 'fill', source: 'omt', 'source-layer': 'park', paint: { 'fill-color': C.park } },
		{
			id: 'green',
			type: 'fill',
			source: 'omt',
			'source-layer': 'landcover',
			filter: ['in', 'class', 'grass', 'wood'],
			paint: { 'fill-color': C.park, 'fill-opacity': 0.6 }
		},
		{ id: 'water', type: 'fill', source: 'omt', 'source-layer': 'water', paint: { 'fill-color': C.water } },
		{ id: 'river', type: 'line', source: 'omt', 'source-layer': 'waterway', paint: { 'line-color': C.water, 'line-width': 1.5 } },
		{
			id: 'build',
			type: 'fill',
			source: 'omt',
			'source-layer': 'building',
			minzoom: 14,
			paint: { 'fill-color': C.build, 'fill-outline-color': C.minor }
		},
		{
			id: 'minor',
			type: 'line',
			source: 'omt',
			'source-layer': 'transportation',
			filter: ['in', 'class', 'minor', 'service', 'track'],
			minzoom: 12,
			paint: { 'line-color': C.minor, 'line-width': ['interpolate', ['linear'], ['zoom'], 12, 0.5, 16, 3] }
		},
		{
			id: 'road',
			type: 'line',
			source: 'omt',
			'source-layer': 'transportation',
			filter: ['in', 'class', 'primary', 'secondary', 'tertiary', 'trunk'],
			paint: { 'line-color': C.road, 'line-width': ['interpolate', ['linear'], ['zoom'], 8, 0.5, 12, 1.2, 16, 5] }
		},
		{
			id: 'motorway',
			type: 'line',
			source: 'omt',
			'source-layer': 'transportation',
			filter: ['==', 'class', 'motorway'],
			paint: { 'line-color': C.road, 'line-width': ['interpolate', ['linear'], ['zoom'], 6, 0.8, 12, 2, 16, 7] }
		},
		{
			id: 'place',
			type: 'symbol',
			source: 'omt',
			'source-layer': 'place',
			filter: ['in', 'class', 'city', 'town', 'suburb', 'neighbourhood'],
			layout: {
				'text-field': ['coalesce', ['get', 'name:en'], ['get', 'name']],
				'text-font': ['Noto Sans Regular'],
				'text-size': ['match', ['get', 'class'], 'city', 14, 'town', 12, 11]
			},
			paint: { 'text-color': C.text, 'text-halo-color': C.halo, 'text-halo-width': 1.5 }
		}
	]
});
