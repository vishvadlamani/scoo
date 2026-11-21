// The flow's line-art, one illustration per screen, in the same style as the street. The SVGs live
// in #lib/art/request; their classes are styled by the request page so they follow its tokens.
import need from '#lib/art/request/need.svg?raw';
import zip from '#lib/art/request/zip.svg?raw';
import ask from '#lib/art/request/ask.svg?raw';
import search from '#lib/art/request/search.svg?raw';
import done from '#lib/art/request/done.svg?raw';
import { placePro } from '#lib/art/pros.ts';

export const ART_NEED = need;
export const ART_ZIP = zip;
export const ART_ASK = ask;
export const ART_SEARCH = search;

// Three pros wave from the street between the two houses: the done screen's "see you soon".
export const ART_DONE = done.replace(
	'<!--pros-->',
	placePro('insurance', 72, 86, 78, 100) + placePro('plumber', 118, 82, 84, 108) + placePro('mover', 170, 86, 78, 100)
);
