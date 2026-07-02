// https://vike.dev/data

// import type { PageContextServer } from "vike/types";
// import { useConfig } from "vike-react/useConfig";
import type { Userdetails,playedwithitem } from "../types.ts";
import { API_URL } from "$lib/morestuff/config";
import type { PageServerLoad } from './$types';

type PlayedWithResponse = {
  playedwith: Array<playedwithitem>
  biggestplayedwith: number
  totalplayedwith: number
}



async function playedwith(
    steamid: string,
    f: (input: RequestInfo, init?: RequestInit) => Promise<Response>
): Promise<PlayedWithResponse | null> {
  let response
     try {
     response = await f(
      `${API_URL}/playedwith`, { method: "POST", body: JSON.stringify({ "steam64": decodeURIComponent(steamid),"expand":true }), headers: { "Content-Type": "application/json" } }
     );

    if (response.status == 200) {
      return  (await response.json()) as PlayedWithResponse;
    }
  }
  catch {
    return null
  }
  return null
}

export const load: PageServerLoad = async ({ params, fetch }) => {
  // console.log("wqdqwd",params.userid)
  const results = await funcyfunc(params.userid, fetch)
  // console.log("weee",results)
  if (results.statuscode == 200) {
    const playedwithresults = playedwith(results.personresults.steam64, fetch)
    results.personresults.playedwith = playedwithresults.then((data) => data?.playedwith ?? [])
    results.personresults.biggestplayedwith = playedwithresults.then((data) => data?.biggestplayedwith ?? 0)
    results.personresults.totalplayedwith = playedwithresults.then((data) => data?.totalplayedwith ?? 0)
  }
  return results 
  
};
