// https://vike.dev/data

import type { PageContextServer } from "vike/types";
import { useConfig } from "vike-react/useConfig";
import type { Stats } from "./types.ts";
import { API_URL } from "../../components/config";

export type Data = Awaited<ReturnType<typeof data>>;

export async function data(pageContext: PageContextServer) {
  // https://vike.dev/useConfig
  const config = useConfig();

  const response = await fetch(
      `${API_URL}/stats`
  );
    let stats = {} as Stats
    if (response.status == 200) {
      stats = (await response.json());
      

      config({
        description: `Tracking bad words in ${stats.totalmessages.toLocaleString()} messages`
      })
          
    }
  
  
  


  // We remove data we don't need because the data is passed to
  // the client; we should minimize what is sent over the network.

  return { stats, statuscode:response.status};
}
