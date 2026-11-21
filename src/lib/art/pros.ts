// The winged pros, one line-art SVG each. Their CSS classes (wing, wl, wr, wingp, skin, hat, tool…)
// are styled by the page that shows them, so they follow the page's tokens and dark mode.
const files = import.meta.glob('./pros/*.svg', { query: '?raw', import: 'default', eager: true }) as Record<string, string>;

export const PROS: Record<string, string> = Object.fromEntries(
	Object.entries(files).map(([path, svg]) => [path.replace(/^.*\/(.+)\.svg$/, '$1'), svg])
);

/** The pro's SVG positioned inside a larger SVG (adds x, y, width and height to its root). */
export const placePro = (name: string, x: number, y: number, w: number, h: number) =>
	PROS[name].trim().replace(/^<svg /, `<svg x="${x}" y="${y}" width="${w}" height="${h}" `);
