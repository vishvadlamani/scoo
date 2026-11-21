// Calls flowing into a hub (the exchange) and out to its members. The dots ride the links with
// animateMotion; their negative begins start them already spread out instead of in a bunch.
import svg from './hub.svg?raw';
import { placePro } from './pros.ts';

const at: Record<string, [number, number]> = { plumber: [30, 16], electrician: [300, 16], lawyer: [30, 176], insurance: [300, 176] };

export const HUB = svg.replace(/\{(\w+)\}/g, (_, name: string) => placePro(name, ...at[name], 70, 90));
