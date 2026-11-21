// There is no exchange directory yet; the only exchanges page is the operator application.
import { redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = () => redirect(307, '/exchanges/start');
