export type Userdetails = {
    currentusername: string
    nonowords: Array<Badmessage>
    avatarurl: string
    frame?: string
    steamprofile: string
    steam64: string
    playedwith: Promise<Record<string, playedwithitem>>

};



export type Badmessage = {
    matchid: number
    message: string
    timestamp: number
    name: string
}

export type playedwithitem = {
    commonmatches: number
    currentname: string
    avatar: string
    frame: string | null
    backupusername: string

}

export type Stats = {
    totalmatches: number
    totalmessages: number
    badmessages: number
    uniquepeople: number
    flaggedplayers: number
}

