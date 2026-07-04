import { query } from '$app/server';
import { API_URL } from "$lib/morestuff/config";
import type { Userdetails } from "$lib/morestuff/types";
import * as v from 'valibot';


export const getprofile = query(v.string(), async (steam64) => {
	let profile = {} as Userdetails
	const response = await fetch(`${API_URL}/profile`, { method: "POST", body: JSON.stringify({ "url": steam64, "expand": true }), headers: { "Content-Type": "application/json" } })



	if (response.ok) {
		profile = await response.json()
	}
	

	return { profile, statuscode: response.status };
});
