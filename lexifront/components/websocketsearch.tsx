import { create } from "zustand";

import { io, Socket } from "socket.io-client";

type wsstore = {
  socket: Socket | null;
  isConnected: boolean;
  count: number;
  mostrecentcount: number;
  matches: match[];
  connect: () => void;
  disconnect: () => void;
  sendsearch: (query: string) => void;
};

type match = {
  n: Array<string>;
  id: string;
  a: string;
  g: number;
};

export const usewsstore = create<wsstore>()((set, get) => ({
  socket: null,
  mostrecentcount:-1,
  isConnected: false,
  isConnecting: false,
  count: 0,
  matches: [],
  connect: () => {
    const SOCKETIOURL =
      (import.meta.env.VITE_API_URL && `${window.location.origin}`) ||
      "http://192.168.1.39:3440";
    const SOCKETIOURLpath =
      (import.meta.env.VITE_API_URL && `/api/socket.io/`) || "/socket.io/";

    if (get().socket?.connected ) return;


    console.log("ws urL", SOCKETIOURL);
    const newSocket = io(SOCKETIOURL, {
      path: SOCKETIOURLpath,
      transports: ['websocket', 'polling']
    });

    newSocket.on("connect", () => {
      console.log("CONNECTED")
      set({ isConnected: true});
    });

    newSocket.on("disconnect", (reason) => {
      console.log("DISCONNECTED", reason);
      set({ isConnected: false});
    });

    newSocket.on("connect_error", (error) => {
      console.log("CONNECTION ERROR", error);
    });

    newSocket.io.on("error", (error) => {
      console.log("IO ERROR", error);
    });

    newSocket.io.on("reconnect", (attempt) => {
      console.log("RECONNECTED after", attempt, "attempts");
    });

    newSocket.on("m", async (data) => {
      // const todothings = data.filter((id: match) => !(id.id in get().avatarstore))
      // if (todothings.length) {
      //   try {
      //     const response = await fetch(
      //       `https://steamcommunity.com/actions/ajaxresolveusers?steamids=${todothings.map((id: match) => id.id.toString()).join(",")}`,
      //     );
      //     if (response && response.status == 200) {
      //       const tempavatatarstore = { ...get().avatarstore };
      //       (await response.json()).forEach((thing: any, index: number) => {
      //         tempavatatarstore[todothings[index].id] = thing.avatarUrl;
      //       });
      //       set({ avatarstore: tempavatatarstore });
      //     }
      //   } catch { }
      // }
      if (get().mostrecentcount < data[0]) {
        set({ matches: data[1], mostrecentcount: data[0]});
      }
    });
    // console.log("pants")
    set({ socket: newSocket });
  },

  disconnect: () => {
    get().socket?.disconnect();
    set({ socket: null, isConnected: false });
  },

  sendsearch: (query: string) => {
    set({ count: get().count+1 });
    if (query.length > 0) {
      get().socket?.emit("s", [query,get().count]);

    }
    else {
       get().socket?.emit("n",get().count);
      //  set({ matches: [] });
    }
     
  },
}));
