// The AI receptionist at work: the plumber is busy at the van, the phone answers for them and the
// conversation plays out on its screen. Styled by the pros page (classes ill, msg, buzz, phone…).
import svg from './receptionist.svg?raw';
import { placePro } from './pros.ts';

export const RECEPTIONIST = svg.replace('{plumber}', placePro('plumber', 140, 104, 110, 142));
