// https://vike.dev/data

import type { PageContextServer } from "vike/types";
import { useConfig } from "vike-react/useConfig";
import type { Userdetails } from "../types.ts";
import { API_URL } from "../../../components/config";

export type Data = Awaited<ReturnType<typeof data>>;

export async function data(pageContext: PageContextServer) {
  // https://vike.dev/useConfig
  const config = useConfig();
  let personresults = {} as Userdetails
  let response
  try {
     response = await fetch(
      `${API_URL}/user`, { method: "POST", body: JSON.stringify({ "url": decodeURIComponent(pageContext.routeParams.userid) }), headers: { "Content-Type": "application/json" } }
    );
    
    if (response.status == 200) {
      personresults = (await response.json());
      config({
        description: `${personresults.nonowords.length || "No"} Bad words sent`,
            
        image: personresults.avatarurl,
        // Set <title>
        title: personresults.currentusername,
      });
    }
  }
  catch {
    return {personresults,statuscode:500}
  }
    
  // let personresults = {} as Userdetails
  // personresults.avatarurl = "pants"
  // personresults.nonowords = []
  // personresults.currentusername = "underwear"
  // personresults.frame = "wdqodwq"
  // personresults.steamprofile = "wqdwqdq"

  // We remove data we don't need because the data is passed to
  // the client; we should minimize what is sent over the network.

  return { personresults, statuscode:response.status};
}
