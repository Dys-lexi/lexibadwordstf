
import { API_URL } from "$lib/morestuff/config";
import type { LayoutServerLoad } from './$types';
import type { temp as Temp } from "./types.ts";


async function getTemp(
	f: (input: RequestInfo, init?: RequestInit) => Promise<Response>
): Promise<Temp> {
	try {
		const response = await f(`${API_URL}/temp`, { method: "GET" });
			const stuff = await response.json()
		return {
			statuscode: response.status,
			temp: (stuff).temp,
			lastupdate: (stuff).lastupdate
		};
	} catch {
		return {
			statuscode: 500,
			temp: 0
		};
	}
}

export const load: LayoutServerLoad = ({ fetch, cookies, request }) => {
	// console.log("Meow",request)
	return {
		temp: getTemp(fetch),
		randomnumber: Math.floor(Math.random() * 1000)
	};
};
