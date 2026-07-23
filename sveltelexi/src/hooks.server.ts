import type { Handle, RequestEvent } from '@sveltejs/kit';
import { API_URL } from '$lib/morestuff/config';
export const handle: Handle = async ({ event, resolve }) => {
	if (!event.isRemoteRequest) {
		sendcooldata(event);
	}

	// const response = await resolve(event);
	return await resolve(event);
	// things
	//  event.url.href
	//  event.url.pathname
	//  headers
};

async function sendcooldata(event: RequestEvent) {
	try {
		await fetch(`${API_URL}/logdata`, {
				method: 'POST',
				body: JSON.stringify({ path: event.url.pathname,headers: Object.fromEntries(event.request.headers), otherip: event.getClientAddress(),hostname: event.url.hostname }),
				headers: { 'Content-Type': 'application/json' }
		})
		// console.log(event.request.headers)
		// console.log(response)
	} catch {
		console.log("Pants")
		}
}
