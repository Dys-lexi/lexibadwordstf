
import { API_URL } from "$lib/morestuff/config";
import type { LayoutServerLoad } from './$types';
import type { temp as Temp } from "./types.ts";


async function getTemp(
	f: (input: RequestInfo, init?: RequestInit) => Promise<Response>
): Promise<Temp> {
	try {
		const response = await f(`${API_URL}/temp`, { method: "GET" });

		return {
			statuscode: response.status,
			temp: await response.text()
		};
	} catch {
		return {
			statuscode: 500,
			temp: ''
		};
	}
}

export const load: LayoutServerLoad = ({ fetch, cookies }) => {
	
	return {
		temp: getTemp(fetch),
		randomnumber: Math.floor(Math.random() * 1000)
	};
};
