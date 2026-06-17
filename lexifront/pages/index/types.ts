export type Userdetails = {
    currentusername: string
    nonowords: Array<Badmessage>
    avatarurl: string
    frame? :string
};

export type Badmessage = {
    matchid: number
    message: string
    timestamp: number
    name: string
}
