import { city } from '#lib/server/waitlist.ts';
import { env } from 'cloudflare:workers';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = ({ url }) => city(env, url.searchParams.get('zip') ?? '');
