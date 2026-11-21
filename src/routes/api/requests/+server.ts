import { createRequest } from '#lib/server/waitlist.ts';
import { env } from 'cloudflare:workers';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = ({ request }) => createRequest(request, env);
