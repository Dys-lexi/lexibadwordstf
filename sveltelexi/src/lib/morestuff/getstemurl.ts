export function getsteamurl(steamid: string,includefirstslash= true as boolean) {
    return `${includefirstslash &&"/"|| ""  }${encodeURIComponent(steamid)}`//?asyncload=1`
    // return `/${steamid}`
}
