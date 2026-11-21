// A customer's invite link. The homepage remembers the code and sends it with their request.
import { error, redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = ({ params }) => {
	if (!/^[a-z0-9]{4,12}$/i.test(params.code)) error(404, 'Not found');
	redirect(302, `/?ref=${params.code.toLowerCase()}`);
};
