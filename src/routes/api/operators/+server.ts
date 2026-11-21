import { createOperator } from '#lib/server/waitlist.ts';
import { env } from 'cloudflare:workers';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = ({ request }) => createOperator(request, env);
