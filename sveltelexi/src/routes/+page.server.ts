import type { Stats } from "$lib/morestuff/types";
import { API_URL } from '$lib/morestuff/config';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
	let stats = {} as Stats;
	let response;
	try {
		response = await fetch(`${API_URL}/stats`);
		if (response.status == 200) {
			stats = await response.json();
		}
	} catch {
		return { stats, statuscode: 500 };
	}
	return { stats, statuscode: response.status };
};
