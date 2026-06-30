
import { API_URL } from "$lib/morestuff/config";
import type { LayoutServerLoad } from './$types';
import type { temp } from "./types.ts";


async function temp(
  
    f: (input: RequestInfo, init?: RequestInit) => Promise<Response>
) {
    let temp = {} as temp
  let response
     try {
     response = await f(
      `${API_URL}/temp`, { method: "GET"}
     );
     temp.statuscode = response.status
    temp.temp =await response.text()
  }
  catch {
    return {temp}
  }
  return {temp}
}

export const load = ({ fetch }) => {
  let tempw = {} as temp
       tempw.statuscode = 444
    tempw.temp = "bleh"
    // return {
    //   temp: tempw
    // };
  return {
      temp: temp(fetch)
    };
  };