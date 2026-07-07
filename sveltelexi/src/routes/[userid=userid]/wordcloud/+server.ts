import { API_URL } from '$lib/morestuff/config';
import type { RequestHandler } from './$types';



const getWordcloud = async (userid: string, fetch: typeof globalThis.fetch) => {
	return fetch(`${API_URL}/wordcloud/${encodeURIComponent(userid)}`);
};

export const GET: RequestHandler = async ({ params, request, url, fetch }) => {

	const response = await getWordcloud(params.userid, fetch);

	const headers = new Headers();
	headers.set('content-type', response.headers.get('content-type') ?? 'image/png');
	headers.set('vary', 'accept');


	return new Response(response.body, {
		status: response.status,
		statusText: response.statusText
	});
};
