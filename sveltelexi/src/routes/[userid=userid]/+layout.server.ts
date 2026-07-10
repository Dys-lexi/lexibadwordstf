// https://vike.dev/data

// import type { PageContextServer } from "vike/types";
// import { useConfig } from "vike-react/useConfig";
import type { Userdetails } from "$lib/morestuff/types";
import { API_URL } from "$lib/morestuff/config";
import type { PageServerLoad } from './$types';
import { getprofile } from '$lib/remote/data.remote';






export const load: PageServerLoad = async ({ params, fetch,url }) => {
  // console.log("wqdqwd",params.userid)
  // console.log(params)
  // console.log(url.searchParams)
 
  
  const { profile:personresults,statuscode } =await getprofile({ steam64: decodeURIComponent(params.userid), recall: 3600 })


  return { personresults, statuscode }
  }
  

