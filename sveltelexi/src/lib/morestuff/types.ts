export type Userdetails = {
    currentusername: string
    nonowords: Promise<Array<Badmessage>>
    avatar: string
    frame?: string
    steam64: string
    playedwith: Promise<Array<playedwithitem>>
    biggestplayedwith: Promise<number>
    totalplayedwith: Promise<number>
    badwords: number
    logs: number
    aliases: Array<string>
    stats: Array<string>
    mostrecentmatchtimestamp: number

};

export type Badmessage = {
    matchid: number
    message: string
    timestamp: number
    name: string
}

export type playedwithitem = {
    commonmatches: number
    currentusername: string
    avatar: string | null
    frame: string | null
    backupusername: string
    steam64: string

}

export type Stats = {
    totalmatches: number
    totalmessages: number
    badmessages: number
    uniquepeople: number
    flaggedplayers: number
}

