import type { Config } from "vike/types";
import vikeReact from "vike-react/config";

// Default config (can be overridden by pages)
// https://vike.dev/config

const config: Config = {
  // https://vike.dev/head-tags
  title: "lexislurs",
  image: "https://lexi.tf/logo.png",
  description: "find bad words and mabye slurs sent by people in tf2",
  server:true,
  extends: [vikeReact],
};

export default config;
