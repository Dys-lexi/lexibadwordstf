export type Userdetails = {
    currentusername: string
    nonowords: Array<Badmessage>
    avatarurl: string
};

export type Badmessage = {
    matchid: number
    message: string
    timestamp: Date
    name: string
}