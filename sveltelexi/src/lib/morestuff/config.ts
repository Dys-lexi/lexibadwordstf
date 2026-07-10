export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:3440";
export function getsteamurl(steamid: string,includefirstslash= true as boolean) {
return `${includefirstslash &&"/"|| ""  }${encodeURIComponent(steamid)}`//?asyncload=1`
}