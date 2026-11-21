import { exchangeName } from '#lib/server/waitlist.ts';
import { env } from 'cloudflare:workers';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = ({ url }) => exchangeName(env, url.searchParams.get('s') ?? '');
