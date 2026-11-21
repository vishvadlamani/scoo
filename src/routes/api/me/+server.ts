import { me } from '#lib/server/waitlist.ts';
import { env } from 'cloudflare:workers';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = ({ cookies }) => me(cookies.get('scoo_t'), env);
