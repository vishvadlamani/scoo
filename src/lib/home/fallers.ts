// The winged pros who drift down onto the street and stand between its doors. Imperative on
// purpose: positions change every animation frame, and the rotating headline needs to restart a
// landed pro's hop animation, which only a class toggle around a forced reflow can do.
import { PROS } from '#lib/art/pros.ts';

const DESKTOP = ['plumber', 'lawyer', 'insurance', 'doctor', 'electrician', 'mover'];
const PHONE = ['plumber', 'insurance', 'doctor', 'electrician'];

// The street's viewBox starts at y=160 and is 420 tall; the pavement the pros stand on is y=536.
const FLOOR = (536 - 160) / 420;

type Faller = {
	el: HTMLDivElement;
	name: string;
	slot: number;
	start: number;
	y: number;
	tx: number;
	started: boolean;
	landed: boolean;
	drift: number;
	ph: number;
};

export type Street = {
	/** Re-measure the scene, the search box and the doors; call on resize and once fonts arrive. */
	layout: () => void;
	/** Make a landed pro hop, when the headline names their trade. */
	hop: (name: string) => void;
	destroy: () => void;
};

/**
 * Starts the fallers inside `sky`, landing them on `scene` (the street SVG, which lists its doors in
 * `data-doors`) and spawning them from behind `box` (the search form).
 */
export function startStreet(
	sky: HTMLElement,
	hero: HTMLElement,
	scene: SVGSVGElement,
	box: HTMLElement,
	opts: { fast: number; reduce: boolean }
): Street {
	const phone = innerWidth < 640;
	const cast = phone ? PHONE : DESKTOP;
	const pw = phone ? 64 : 100,
		H = pw * 1.28;
	// evenly spaced slots, shuffled so the order of arrival feels natural
	const slots = cast.map((_, i) => (i + 0.5) / cast.length);
	const order = [...cast.keys()]
		.sort(() => Math.random() - 0.5)
		.sort((a, b) => Number(cast[a] === 'mover') - Number(cast[b] === 'mover'));

	let floorY = 0,
		spawnY = 0,
		last = 0,
		t0 = 0,
		raf = 0;

	const place = (f: Faller, x: number, y: number, r: number) => {
		f.el.style.transform = `translate(${x}px,${y}px) rotate(${r}deg)`;
	};
	const rest = () => floorY - H + pw * 0.18;

	const fallers: Faller[] = order.map((i, k) => {
		const el = document.createElement('div');
		el.className = 'faller';
		el.style.setProperty('--pw', pw + 'px');
		el.innerHTML = PROS[cast[i]];
		sky.appendChild(el);
		return {
			el,
			name: cast[i],
			slot: slots[i],
			start: k * 2.6,
			y: 0,
			tx: 0,
			started: false,
			landed: false,
			drift: (Math.random() < 0.5 ? -1 : 1) * (40 + Math.random() * 60),
			ph: Math.random() * 6
		};
	});

	// Pros appear from behind the search box (never crossing the headline) and land on the pavement
	// between doorways: the street drawing lists its doors, mapped here to screen positions.
	function layout() {
		const sv = scene.getBoundingClientRect(),
			hr = hero.getBoundingClientRect();
		floorY = sv.top - hr.top + sv.height * FLOOR;
		spawnY = box.getBoundingClientRect().bottom - hr.top - H * 0.35;
		const sc = sv.width / (Number(scene.dataset.w) || 1);
		const doors = (JSON.parse(scene.dataset.doors || '[]') as [number, number][]).map(
			([a, b]) => [sv.left - hr.left + a * sc - 8, sv.left - hr.left + b * sc + 8] as const
		);
		const pad = phone ? 10 : Math.max(40, innerWidth * 0.06),
			lo = pad,
			hi = innerWidth - pad - pw;
		const clear = (x: number) => !doors.some(([a, b]) => x + pw * 0.7 > a && x + pw * 0.3 < b);
		const chosen: number[] = [];
		[...fallers]
			.sort((a, b) => a.slot - b.slot)
			.forEach((f) => {
				const ideal = lo + f.slot * (hi - lo);
				let best = ideal;
				// Best: off every doorway and clear of the others. If the visible street has no such spot (a
				// narrow phone), keep them apart anyway: two pros overlapping looks worse than one by a door.
				const apart = (x: number) => chosen.every((o) => Math.abs(o - x) >= pw * 0.85);
				search: for (const ok of [(x: number) => clear(x) && apart(x), apart]) {
					for (let d = 0; d <= hi - lo; d += 2) {
						const c = [ideal - d, ideal + d].find((x) => x >= lo && x <= hi && ok(x));
						if (c !== undefined) {
							best = c;
							break search;
						}
					}
				}
				chosen.push(best);
				f.tx = best;
			});
		fallers.forEach((f) => {
			if (f.landed) place(f, f.tx, rest(), 0);
			else if (!f.started) f.y = spawnY;
		});
	}

	function land(f: Faller) {
		f.landed = true;
		f.started = true;
		f.el.classList.add('on', 'landed', 'bounce');
		place(f, f.tx, rest(), 0);
	}

	function tick(t: number) {
		if (!t0) t0 = t;
		const dt = Math.min(0.05, (t - (last || t)) / 1000) * opts.fast;
		last = t;
		const el = ((t - t0) / 1000) * opts.fast;
		for (const f of fallers) {
			if (f.landed || el < f.start) continue;
			if (!f.started) {
				f.started = true;
				f.y = spawnY;
				f.el.classList.add('on');
			}
			// the mover is carrying a box and drops; the umbrella floats
			const speed = f.name === 'mover' ? 150 : f.name === 'insurance' ? 45 : 60;
			f.y += speed * dt;
			const end = rest(),
				k = Math.min(1, Math.max(0, end - f.y) / 300);
			const x = f.tx + f.drift * k + Math.sin(el * 1.6 + f.ph) * 10 * k,
				r = Math.sin(el * 1.3 + f.ph) * 7 * k;
			if (f.y >= end) {
				land(f);
				continue;
			}
			place(f, x, f.y, r);
		}
		// nothing left to move: stop asking for frames
		if (fallers.every((f) => f.landed)) return;
		raf = requestAnimationFrame(tick);
	}

	layout();
	if (opts.reduce) fallers.forEach(land);
	else raf = requestAnimationFrame(tick);

	return {
		layout,
		hop(name) {
			const f = fallers.find((f) => f.name === name && f.landed);
			if (!f) return;
			f.el.classList.remove('hop');
			void f.el.offsetWidth;
			f.el.classList.add('hop');
		},
		destroy() {
			cancelAnimationFrame(raf);
			fallers.forEach((f) => f.el.remove());
		}
	};
}
