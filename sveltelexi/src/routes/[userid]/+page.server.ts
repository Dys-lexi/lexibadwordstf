// https://vike.dev/data

// import type { PageContextServer } from "vike/types";
// import { useConfig } from "vike-react/useConfig";
import type { Userdetails } from "./types.ts";
import { API_URL } from "$lib/morestuff/config";
import type { PageServerLoad } from './$types';


async function funcyfunc(
  userid: string,
  fetch : (input: RequestInfo, init?: RequestInit) => Promise<Response>
) {
  let personresults = {} as Userdetails
  let response
  try {
     response = await fetch(
      `${API_URL}/user`, { method: "POST", body: JSON.stringify({ "url": decodeURIComponent(userid) }), headers: { "Content-Type": "application/json" } }
     );

    if (response.status == 200) {
      personresults = (await response.json());
    }
  }
  catch {
    return {personresults,statuscode:500}
  }

  return { personresults, statuscode:response.status};
}

export const load: PageServerLoad = ({ params, fetch }) => funcyfunc(params.userid, fetch );

