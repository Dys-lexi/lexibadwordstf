// https://vike.dev/data

import type { PageContextServer } from "vike/types";
import { useConfig } from "vike-react/useConfig";
import type { Stats } from "./types.ts";

export type Data = Awaited<ReturnType<typeof data>>;

export async function data(pageContext: PageContextServer) {
  // https://vike.dev/useConfig
  const config = useConfig();

  const response = await fetch(
      `http://localhost:3440/stats`
  );
    let stats = {} as Stats
    if (response.status == 200) {
        stats = (await response.json());
          
    }
  


  // We remove data we don't need because the data is passed to
  // the client; we should minimize what is sent over the network.

  return { stats, statuscode:response.status};
}
