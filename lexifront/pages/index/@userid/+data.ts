// https://vike.dev/data

import type { PageContextServer } from "vike/types";
import { useConfig } from "vike-react/useConfig";
import type { Userdetails } from "../types.ts";
import { API_URL } from "../../../components/config";

export type Data = Awaited<ReturnType<typeof data>>;

export async function data(pageContext: PageContextServer) {
  // https://vike.dev/useConfig
  const config = useConfig();

  const response = await fetch(
      `${API_URL}/user`, { method: "POST", body: JSON.stringify({ "url": decodeURIComponent(pageContext.routeParams.userid) }) , headers: { "Content-Type": "application/json" }}
  );
    let personresults = {} as Userdetails
    if (response.status == 200) {
        personresults = (await response.json());
      config({
        description: `${personresults.nonowords.length || "No" } Bad words sent`,
            
      image: personresults.avatarurl,
    // Set <title>
    title: personresults.currentusername,
  });
    }
  


  // We remove data we don't need because the data is passed to
  // the client; we should minimize what is sent over the network.

  return { personresults, statuscode:response.status};
}
