export type Userdetails = {
    currentusername: string
    nonowords: Array<Badmessage>
    avatar: string
    frame?: string
    steam64: string
    playedwith: Array<playedwithitem>
    biggestplayedwith: number
    totalplayedwith: number
    badwords: number
    logs: number
    aliases: Array<string>
    stats: Array<string>
    mostrecentmatchtimestamp: number

};

export type Aliases = Array<Alias>

export type Alias = {
    name: string
    firstseen: number
    lastseen: number
    firstlog: number
    lastlog: number
}

export type Badmessage = {
    matchid: number
    message: string
    timestamp: number
    name: string
    index?: number
    team?: string,
    original?: boolean
    
}

export type ProfileResponse = {
    avatar: string | null
    badwords: number
    currentusername: string
    frame: string | null
    mostrecentmatchtimestamp: number
    stats: {
        aliases: string
        badwords: string
        logs: string
    }
    steam64: string
}

export type BadWordsResponse = {
    nonowords: Array<Badmessage>
}

export type playedwithitem = {
    commonmatches: number
    currentusername: string
    avatar: string | null
    frame: string | null
    backupusername?: string
    steam64: string

}

export type PlayedWithResponse = {
    playedwith: Array<playedwithitem>
    biggestplayedwith: number
    totalplayedwith: number
}

export type Stats = {
    totalmatches: number
    totalmessages: number
    badmessages: number
    uniquepeople: number
    flaggedplayers: number
}
