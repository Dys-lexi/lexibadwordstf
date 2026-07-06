import { API_URL } from '$lib/morestuff/config';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params, fetch }) => {
	if (!/^\d+$/.test(params.steam64)) {
		return new Response('Invalid Steam ID', { status: 400 });
	}

	const response = await fetch(`${API_URL}/wordcloud/${encodeURIComponent(params.steam64)}`, {
		method: 'GET'
	});
	const headers = new Headers();

	headers.set('content-type', response.headers.get('content-type') ?? 'image/png');

	const cacheControl = response.headers.get('cache-control');
	if (cacheControl) {
		headers.set('cache-control', cacheControl);
	} else if (response.ok) {
		headers.set('cache-control', 'public, max-age=3600');
	}

	return new Response(response.body, {
		status: response.status,
		statusText: response.statusText,
		headers
	});
};
