import psycopg2
import json
import sys
from datetime import datetime
import datetime as pants
from psycopg2 import pool
import functools
import time
import threading
import requests
from waitress import serve
from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory, send_file
import os
# [U:1:88677982]
from steamid_converter import Converter
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import threading
import initsql


try:
    pgpool = pool.ThreadedConnectionPool(20, 200, dsn="postgresql://pguserm:hiddenpassword@postgres:3452/realdb")
except:
    pgpool = pool.ThreadedConnectionPool(20, 200, dsn="postgresql://pguserm:hiddenpassword@localhost:3449/realdb")
root = "https://logs.tf/api/v1"
app = Flask(__name__)








    

def cachestats():
    conn = pgpool.getconn()
    c = conn.cursor()
    print("caching stats")
    stats = {"totalmatches":0,"totalmessages":0,"badmessages":0,"uniquepeople":0,"flaggedplayers":0,"timestampcached":int(time.time())}
    with open("./statscache.json", "w") as f:
        f.write(json.dumps(stats,indent=4))
    c.execute("SELECT COUNT(*) FROM logs_raw")
    if output := c.fetchone():
        stats["totalmatches"] = output[0]
    c.execute("SELECT COUNT(*) FROM messages")
    if output := c.fetchone():
        stats["totalmessages"] = output[0]
    c.execute("SELECT COUNT(*) FROM messages WHERE flagged = true")
    if output := c.fetchone():
        stats["badmessages"] = output[0]
    c.execute("SELECT COUNT(DISTINCT sender) FROM messages")
    if output := c.fetchone():
        stats["uniquepeople"] = output[0]
    c.execute("SELECT COUNT(DISTINCT sender) FROM messages WHERE flagged = true")
    if output := c.fetchone():
        stats["flaggedplayers"] = output[0]
    print("done caching stats")
    pgpool.putconn(conn)
    with open("./statscache.json", "w") as f:
        f.write(json.dumps(stats,indent=4))

    

@app.route("/stats",methods=["GET"])
def stats():
    now = int(time.time())

    print("pulling stats at",now)
    stats = {"totalmatches":0,"totalmessages":0,"badmessages":0,"uniquepeople":0,"timestampcached":0,"flaggedplayers":0}
    if os.path.exists("./statscache.json"):
        with open("./statscache.json", "r") as f:
            stats = json.load(f)
    if now - 21600 > stats["timestampcached"]:
        threading.Thread(target=cachestats, daemon=True).start()
    del(stats["timestampcached"])
    return stats,200
            

@app.route("/user", methods=["POST"])
def resolvename(userid = False):
    if not userid:
        userid = request.get_json()["url"]
    now = int(time.time())
    timer = time.time()
    conn = pgpool.getconn()
    c = conn.cursor()
    print("pulling a user at",now)


    if userid.startswith("https://steamcommunity.com/id/") or userid.startswith("steamcommunity.com/id/"):
        vanity =(userid.endswith("/") and userid[:-1] or userid).rsplit("/",1)[1]
        c.execute("SELECT vanity,steamid,lastcheckedtimestamp FROM vanityurls WHERE vanity = %s",(vanity,))
        output = c.fetchone()
        if output and output[2] > now - 86400:
            steam3 = Converter.to_steamID3(output[1])
        else:
            r = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/",params = {"key":os.getenv("STEAMAPIKEY"),"vanityurl":vanity})
            r.raise_for_status()
            if  r.json()["response"]["success"] != 1:
                pgpool.putconn(conn)
                return {}, 404
            steam3 = Converter.to_steamID3(r.json()["response"]["steamid"]) 
            c.execute("INSERT INTO vanityurls (vanity,steamid,lastcheckedtimestamp) VALUES (%s,%s,%s) ON CONFLICT (vanity) DO UPDATE SET steamid = EXCLUDED.steamid, lastcheckedtimestamp = EXCLUDED.lastcheckedtimestamp",(vanity,r.json()["response"]["steamid"],now))
            conn.commit()
        
       

    elif userid.startswith("https://steamcommunity.com/profiles/") or userid.startswith("steamcommunity.com/profiles/"):
        steam3 =  Converter.to_steamID3((userid.endswith("/") and userid[:-1] or userid).rsplit("/",1)[1])
        
    else:
        try:
            steam3 = Converter.to_steamID3(userid)
        except: 
            pgpool.putconn(conn)
            return resolvename(f"https://steamcommunity.com/id/{userid}")
            
    steam64 = Converter.to_steamID64(steam3)
    c.execute("SELECT currentname,timestampcurrentname,avatar,frame FROM currentthings WHERE steamid = %s",(steam64,))
    output = c.fetchone()
    # int(steamid64) - STEAMID64_BASE

    if not output or not any(output) or output[1] < now - 3600:
        # print("pants")
        r = requests.get("https://steamcommunity.com/actions/ajaxresolveusers",params = {"steamids":steam64})
        r.raise_for_status()
        if not len(r.json()):
            pgpool.putconn(conn)
            return {}  , 404
        currentname = r.json()[0]["persona_name"]
        avatarurl = r.json()[0]["avatar_url"]
        r = requests.get(f"https://steamcommunity.com/miniprofile/{int(steam64) - 76561197960265728}",headers = {"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        frame = soup.select_one(".playersection_avatar_frame img")
        if frame: frame = frame.get("src")
        
        c.execute("INSERT INTO currentthings (currentname,avatar,timestampcurrentname,steamid,frame) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (steamid) DO UPDATE SET currentname = EXCLUDED.currentname, timestampcurrentname = EXCLUDED.timestampcurrentname, avatar = EXCLUDED.avatar, frame = EXCLUDED.frame",(currentname,avatarurl,now,steam64,frame))
        conn.commit()
    else:
        currentname = output[0]
        avatarurl = output[2]
        frame = output[3]

    if avatarurl.isdigit() and not int(avatarurl):
        avatarurl = "https://avatars.fastly.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg"
    else:
        avatarurl = f"https://avatars.steamstatic.com/{avatarurl}_full.jpg"
    
    
    c.execute("""SELECT name, message,time,id FROM messages WHERE (sender = %s OR sender = %s) AND flagged = true ORDER BY time DESC""",(steam3,Converter.to_steamID(steam3)))
    
    output = list(map(lambda x: {"name":x[0],"timestamp":x[2],"message":x[1],"matchid":x[3]},c.fetchall()))
    reallogs = []
    for log in output:
        shouldreturn = False
        for logdupe in reallogs:
            if abs(log["timestamp"] - logdupe["timestamp"]) < 600 and abs(logdupe["matchid"] - log["matchid"]) < 10 and log["message"] == logdupe["message"] and logdupe["name"] == log["name"]:
                shouldreturn = True
                break
        if shouldreturn:
            continue
        reallogs.append(log)
    print("this took",time.time()-timer)
    pgpool.putconn(conn)
    return  {"currentusername":currentname,"nonowords":reallogs,"avatarurl":avatarurl,"frame":frame,"steamprofile":f"https://steamcommunity.com/profiles/{steam64}"} , 200





def howlongodesthistake():
    conn = pgpool.getconn()
    c = conn.cursor()
    print("wee")
    c.execute("SELECT json->'names' FROM logs_raw")


    output = c.fetchall()
    print("OUTPUTLEN",len(output))
    for i,thing in enumerate(output):
        if not i % 5000:
            print("done number",i)
            conn.commit()
        for id,name in thing[0].items():

            try:
                id = Converter.to_steamID64(id)
            except:
                continue
            c.execute("INSERT INTO usernames (name,steamid) VALUES (%s,%s) ON CONFLICT (name,steamid) DO NOTHING",(name,id))
    
    print("done")
    pgpool.putconn(conn)






# indexsomecoolmessages()

print("done!")
howlongodesthistake()
CORS(app, resources={r"/*": {"origins": "*"}})
serve(app, host="0.0.0.0", port=3440, threads=40, connection_limit=200)  