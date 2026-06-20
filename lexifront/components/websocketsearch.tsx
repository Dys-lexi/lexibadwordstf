import { create } from "zustand";

import { io, Socket } from "socket.io-client";

type wsstore = {
  socket: Socket | null;
  isConnected: boolean;
  matches: match[];
  avatarstore: Record<number, string>;
  connect: () => void;
  disconnect: () => void;
  sendsearch: (query: string) => void;
};

type match = {
  n: string;
  id: number;
  avatar: string;
};

export const usewsstore = create<wsstore>()((set, get) => ({
  avatarstore: {},
  socket: null,
  isConnected: false,
  matches: [],
  connect: () => {
    const SOCKETIOURL =
      (import.meta.env.VITE_API_URL && `${window.location.origin}`) ||
      "http://localhost:3440";
    const SOCKETIOURLpath =
      (import.meta.env.VITE_API_URL && `/api/socket.io/`) || "/socket.io/";

    if (get().socket?.connected) return;
    console.log("ws urL", SOCKETIOURL);
    const newSocket = io(SOCKETIOURL, { path: SOCKETIOURLpath });

    newSocket.on("connect", () => {
      set({ isConnected: true });
    });

    newSocket.on("disconnect", () => {
      set({ isConnected: false });
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
      set({ matches: data });
    });

    set({ socket: newSocket });
  },

  disconnect: () => {
    get().socket?.disconnect();
    set({ socket: null, isConnected: false });
  },

  sendsearch: (query: string) => {
    get().socket?.emit("s", query);
  },
}));
