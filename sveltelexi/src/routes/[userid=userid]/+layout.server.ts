// https://vike.dev/data

// import type { PageContextServer } from "vike/types";
// import { useConfig } from "vike-react/useConfig";
import type { Userdetails } from '$lib/morestuff/types';
import { API_URL } from '$lib/morestuff/config';
import type { LayoutServerLoad } from './$types';
import { getprofile } from '$lib/remote/data.remote';

export const load: LayoutServerLoad = async ({ params, fetch, url, cookies }) => {
	// console.log("wqdqwd",params.userid)
	// console.log(params)
	// console.log(url.searchParams)

	if (cookies.get('client')) {
		return   {profile: getprofile({ steam64: decodeURIComponent(params.userid), recall: 3600 }),promise:true}

	}
		return   {profile: await getprofile({ steam64: decodeURIComponent(params.userid), recall: 3600 }),promise:false}

	
};
