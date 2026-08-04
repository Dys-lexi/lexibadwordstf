import type {
    BadWordsResponse,
    PlayedWithResponse,
    ProfileResponse
} from '$lib/morestuff/types';


export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:3440";


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
            "timestamp": Number("1685052644")
        },
        {
            "matchid": Number("0000000"),
            "message": "lore",
            "name": "lorem ipsum dolor",
            "timestamp": Number("1520727299")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum do",
            "name": "lorem ipsum do",
            "timestamp": Number("1681641680")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit ame",
            "name": "lorem ",
            "timestamp": Number("1473988529")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet conse",
            "name": "lorem ips",
            "timestamp": Number("1709275714")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit",
            "name": "lorem ipsum ",
            "timestamp": Number("1455833112")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ip",
            "name": "lor",
            "timestamp": Number("1716586984")
        },
        {
            "matchid": Number("0000000"),
            "message": "elit lorem ipsum",
            "name": "lorem ipsum dolo",
            "timestamp": Number("1566390880")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolo",
            "name": "lorem ipsum ",
            "timestamp": Number("1471116308")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet consec",
            "name": "lorem ",
            "timestamp": Number("1521295089")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolo",
            "name": "lorem ipsum",
            "timestamp": Number("1511390819")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet",
            "name": "lorem ipsum ",
            "timestamp": Number("1493521524")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ip",
            "name": "lorem ipsum ",
            "timestamp": Number("1547543427")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet",
            "name": "lorem ipsum ",
            "timestamp": Number("1620697428")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit a",
            "name": "lorem ipsum ",
            "timestamp": Number("1532196065")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor ",
            "name": "lorem i",
            "timestamp": Number("1733971756")
        },
        {
            "matchid": Number("0000000"),
            "message": "lor",
            "name": "lorem i",
            "timestamp": Number("1511479038")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum",
            "name": "lorem i",
            "timestamp": Number("1769772355")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum do",
            "name": "lorem ",
            "timestamp": Number("1550294234")
        },
        {
            "matchid": Number("0000000"),
            "message": "lore",
            "name": "lorem ",
            "timestamp": Number("1519891387")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ips",
            "name": "lorem ",
            "timestamp": Number("1771462751")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum d",
            "name": "lorem i",
            "timestamp": Number("1455537554")
        },
        {
            "matchid": Number("0000000"),
            "message": "lor",
            "name": "lorem ipsu",
            "timestamp": Number("1646585485")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet conse",
            "name": "lorem ",
            "timestamp": Number("1667582162")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum ",
            "name": "lorem ipsum dolor s",
            "timestamp": Number("1540497112")
        },
        {
            "matchid": Number("0000000"),
            "message": "I eat pizza with my feet",
            "name": "lorem ipsum dolor s",
            "timestamp": Number("1515863486")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor sit amet consecte",
            "name": "lorem ipsum dolor s",
            "timestamp": Number("1639957507")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolor ",
            "name": "lorem ipsum dolor s",
            "timestamp": Number("1619897378")
        },
        {
            "matchid": Number("0000000"),
            "message": "lorem ipsum dolo",
            "name": "lorem ip",
            "timestamp": Number("1696126870")
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
