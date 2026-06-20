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
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory, send_file
import os
# [U:1:88677982]
from steamid_converter import Converter
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import initsql
from cachetools import cached, LRUCache, TTLCache
from psycogreen.gevent import patch_psycopg
patch_psycopg()
load_dotenv() 

try:
    pgpool = pool.ThreadedConnectionPool(20, 200, dsn="postgresql://pguserm:hiddenpassword@postgres:3452/realdb")
except:
    pgpool = pool.ThreadedConnectionPool(20, 200, dsn="postgresql://pguserm:hiddenpassword@localhost:3449/realdb")
root = "https://logs.tf/api/v1"
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='gevent')










    

def cachestats():
    conn = pgpool.getconn()
    c = conn.cursor()
    print("caching stats")
    stats = {"totalmatches":0,"totalmessages":0,"badmessages":0,"uniquepeople":0,"flaggedplayers":0,"timestampcached":int(time.time())}
    if os.path.exists("./statscache.json"):
        with open("./statscache.json", "r") as f:
            stats = json.load(f)
    stats["timestampcached"] = int(time.time())
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
    return stats_cache()
@cached(cache=TTLCache(maxsize=1024, ttl=600))
def stats_cache():
    now = int(time.time())
    
    print("pulling stats at",now)
    stats = {"totalmatches":0,"totalmessages":0,"badmessages":0,"uniquepeople":0,"timestampcached":0,"flaggedplayers":0}
    if os.path.exists("./statscache.json"):
        with open("./statscache.json", "r") as f:
            stats = json.load(f)
    if not stats or now - 86400 > stats["timestampcached"]:
        threading.Thread(target=cachestats, daemon=True).start()
    if not stats: return {}
    if "timestampcached" in stats:
        del(stats["timestampcached"])
    return stats

@app.route("/user", methods=["POST"])
def resolvename():
    userid = request.get_json()["url"]
    return resolvename_cache(userid)

@cached(cache=TTLCache(maxsize=1024, ttl=1800))
def resolvename_cache(userid):
    now = int(time.time())
    print("pulling a user at",now)
    timer = time.time()
    conn = pgpool.getconn()
    c = conn.cursor()
    


    if userid.startswith("https://steamcommunity.com/id/") or userid.startswith("steamcommunity.com/id/"):
        vanity =(userid.endswith("/") and userid[:-1] or userid).rsplit("/",1)[1]
        c.execute("SELECT vanity,steamid,lastcheckedtimestamp FROM vanityurls WHERE vanity = %s",(vanity,))
        output = c.fetchone()
        if output and output[2] > now - 86400:
            steam3 = Converter.to_steamID3(output[1])
        else:
            r = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/",params = {"key":os.getenv("STEAMAPIKEY"),"vanityurl":vanity})
            if r.status_code in [429]:
                return {}, 429
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
            return resolvename_cache(f"https://steamcommunity.com/id/{userid}")
            
    steam64 = Converter.to_steamID64(steam3)
    c.execute("SELECT currentname,timestampcurrentname,avatar,frame FROM currentthings WHERE steamid = %s",(steam64,))
    output = c.fetchone()
    # int(steamid64) - STEAMID64_BASE

    if not output or not all(output) or output[1] < now - 3600:
        # print("pants")
        failed = False
        r = requests.get("https://steamcommunity.com/actions/ajaxresolveusers",params = {"steamids":steam64})
        if r.status_code in [429]:
            currentname = "Unknown (server rate limited)"
            avatarurl = "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb"
            failed = True
        else:
            r.raise_for_status()
            if not len(r.json()):
                pgpool.putconn(conn)
                return {}  , 404
            currentname = r.json()[0]["persona_name"]
            avatarurl = r.json()[0]["avatar_url"]
        r = requests.get(f"https://steamcommunity.com/miniprofile/{int(steam64) - 76561197960265728}",headers = {"User-Agent": "Mozilla/5.0"})
        if r.status_code in [429]:
            return {}, r.status_code
            frame = None
            failed = True
        else:
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            
            frame = soup.select_one(".playersection_avatar_frame img")
            if frame: frame = frame.get("src")
        if not failed:
            c.execute("INSERT INTO currentthings (currentname,avatar,timestampcurrentname,steamid,frame) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (steamid) DO UPDATE SET currentname = EXCLUDED.currentname, timestampcurrentname = EXCLUDED.timestampcurrentname, avatar = EXCLUDED.avatar, frame = EXCLUDED.frame",(currentname,avatarurl,now,steam64,frame))
            conn.commit()
        elif output:
            print("I GOT RATE LIMITED")
            currentname = output[0]
            avatarurl = output[2]
            frame = output[3]

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






@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('n')
def handle_search(data):
    now = time.time()
    emit("m",[data,defaultthing()])
    print(time.time()-now)
@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def defaultthing():
    conn = pgpool.getconn()
    c = conn.cursor()


    c.execute("SELECT  name, steamid, cardinality(ids) FROM usernames  ORDER BY cardinality(ids) DESC LIMIT 10" )
    
    output = list(map(lambda x: {"n":x[0],"id":str(x[1]),"g":x[2]}, c.fetchall()))
    c.execute("SELECT steamid, avatar FROM currentthings WHERE steamid = ANY(%s)",(list(map(lambda x: int(x["id"]) , output)),))
    avatars = dict(c.fetchall() )
    for steamid ,avatarurl in avatars.items():
        if avatarurl.isdigit() and not int(avatarurl):
            avatarurl = "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb"
            avatars[steamid] = avatarurl
    output = list(map(lambda x: {**x,"a":avatars.get(int(x["id"]))},output))
    pgpool.putconn(conn)

    return output


@socketio.on('s')
def handle_search(data):
    now = time.time()
    # print("PANTS",data)
    emit("m",[data[1],handle_search_helper(data[0])])
    # print(data[0].ljust(10), time.time()-now)
@cached(cache=TTLCache(maxsize=10000, ttl=3600))
def handle_search_helper(data):
    conn = pgpool.getconn()
    c = conn.cursor()
    now = int(time.time())

    # print("meow")
    if not data:
        emit("m",[])
        return 
    escaped = data.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
    c.execute("SELECT  name, steamid, cardinality(ids) FROM usernames WHERE name ILIKE %s AND LENGTH(name) >= LENGTH(%s) ORDER BY cardinality(ids) DESC LIMIT 10", (f'{escaped}%',escaped))
    
    output = sorted(map(lambda x: {"n":x[0],"id":str(x[1]),"g":x[2]}, c.fetchall()), key = lambda x: x["n"] == data, reverse = True)
    if not output:
        c.execute("SELECT  name, steamid, cardinality(ids) FROM usernames WHERE name ILIKE %s AND LENGTH(name) >= LENGTH(%s) ORDER BY cardinality(ids) DESC LIMIT 10", (f'%{escaped}%',escaped))
        output = sorted(map(lambda x: {"n":x[0],"id":str(x[1]),"g":x[2]}, c.fetchall()), key = lambda x: x["n"] == data, reverse = True)

    # print(list(list(map(lambda x: x["id"],output))))
    # c.execute("SELECT steamid, avatar, timestampcurrentname FROM currentthings WHERE steamid = ANY(%s)",(list(map(lambda x: x["id"] , output)),))
    # ids = list(filter(lambda x: x["timestampcurrentname"] > now - 604800, map(lambda x:{"id":x[0],"avatar":x[1],"timestampcurrentname":x[2]}, c.fetchall())))
    # requeststomake = list(filter(lambda x: x not in list(map(lambda x: x["id"],ids)), list(map(lambda x: x["id"] , output))))
    # r = requests.get("https://steamcommunity.com/actions/ajaxresolveusers",params={"steamids":",".join(list(map(str,requeststomake)))})
    # if r.ok:
    #     avatarstore = {}
    #     for thing in r.json():

    #         c.execute("INSERT INTO currentthings (steamid, timestampcurrentname,avatar,currentname) VALUES (%s, %s, %s, %s) ON CONFLICT (steamid) DO UPDATE SET currentname = EXCLUDED.currentname, timestampcurrentname = EXCLUDED.timestampcurrentname, avatar = EXCLUDED.avatar",(int(thing["steamid"]),now,thing["avatar_url"],thing["persona_name"]))
    #         conn.commit()
    #         avatarstore[int(thing["steamid"])] = {"avatar":thing["avatar_url"],"currentname":thing["persona_name"]}
    #     output = list(map(lambda x: {**x,**avatarstore[x]},output))
    # else:
    #     print(r.status_code)

    c.execute("SELECT steamid, avatar FROM currentthings WHERE steamid = ANY(%s)",(list(map(lambda x: int(x["id"]) , output)),))
    avatars = dict(c.fetchall() )
    # print(avatars)
    for steamid ,avatarurl in avatars.items():
        if avatarurl.isdigit() and not int(avatarurl):
            avatarurl = "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb"
            avatars[steamid] = avatarurl
    output = list(map(lambda x: {**x,"a":avatars.get(int(x["id"]))},output))
    # print(list(map(lambda x: (x["id"], x["n"]) , output)))
    pgpool.putconn(conn)
    # print(output)
    return output




# indexsomecoolmessages()
# gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --bind 0.0.0.0:3440 search:app
print("done!")

CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=3440, debug=False, allow_unsafe_werkzeug=True)