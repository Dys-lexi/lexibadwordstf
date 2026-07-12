import type {
    BadWordsResponse,
    PlayedWithResponse,
    ProfileResponse
} from '$lib/morestuff/types';


export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:3440";
export function getsteamurl(steamid: string,includefirstslash= true as boolean) {
return `${includefirstslash &&"/"|| ""  }${encodeURIComponent(steamid)}`//?asyncload=1`
}


export const profileResponse: ProfileResponse = {
    "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
    "badwords": Number("00"),
    "currentusername": "lorem ipsum dol",
    "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
    "mostrecentmatchtimestamp": Number("0000000000"),
    "stats": {
        "aliases": "lorem ipsum",
        "badwords": "lorem ipsum ",
        "logs": "lorem ips"
    },
    "steam64": "00000000000000000"
}


export const badwordsResponse: BadWordsResponse = {
    "nonowords": [
        {
            "matchid": Number("0000000"),
            "message": "lorem i",
            "name": "lore",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lore",
            "name": "lorem ipsum dolor",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum do",
            "name": "lorem ipsum do",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit ame",
            "name": "lorem ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet conse",
            "name": "lorem ips",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit",
            "name": "lorem ipsum ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ip",
            "name": "lor",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "elit lorem ipsum",
            "name": "lorem ipsum dolo",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolo",
            "name": "lorem ipsum ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet consec",
            "name": "lorem ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolo",
            "name": "lorem ipsum",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet",
            "name": "lorem ipsum ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ip",
            "name": "lorem ipsum ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet",
            "name": "lorem ipsum ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit a",
            "name": "lorem ipsum ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor ",
            "name": "lorem i",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lor",
            "name": "lorem i",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum",
            "name": "lorem i",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum do",
            "name": "lorem ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lore",
            "name": "lorem ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ips",
            "name": "lorem ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum d",
            "name": "lorem i",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lor",
            "name": "lorem ipsu",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet conse",
            "name": "lorem ",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum ",
            "name": "lorem ipsum dolor s",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "I eat pizza with my feet",
            "name": "lorem ipsum dolor s",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet consecte",
            "name": "lorem ipsum dolor s",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor ",
            "name": "lorem ipsum dolor s",
            "timestamp": Number("0000000000")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolo",
            "name": "lorem ip",
            "timestamp": Number("0000000000")
        }
    ]
}


export const playedwithResponse: PlayedWithResponse = {
    "biggestplayedwith": Number("0000"),
    "playedwith": [
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("0000"),
            "currentusername": "lorem ipsum do",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("0000"),
            "currentusername": "lorem ipsum do",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("0000"),
            "currentusername": "lorem ipsum dolo",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ipsum dolo",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lore",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ip",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ipsum dol",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ipsum do",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lor",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ipsum dolor",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lore",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ipsum dolor",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem i",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ipsum d",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem i",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ipsum dolor",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lor",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ipsum dolor s",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ipsum ",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lore",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        },
        {
            "avatar": "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb",
            "commonmatches": Number("000"),
            "currentusername": "lorem ips",
            "frame": "https://shared.akamai.steamstatic.com/community_assets/images/items/601220/ccaeeda206ea1a561c35c9bc1252e50a9a36e78e.png",
            "steam64": "00000000000000000"
        }
    ],
    "totalplayedwith": Number("0000")
}
