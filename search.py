from gevent import monkey
monkey.patch_all()

import json
import sys
from datetime import datetime
import datetime as pants
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
from psycogreen.gevent import patch_psycopg
patch_psycopg()
from initsql import querywrapper
from tempurature import recalltemp
from cachetools import cached, LRUCache, TTLCache
load_dotenv() 
root = "https://logs.tf/api/v1"
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='gevent')




    

def cachestats():
    print("caching stats")
    stats = {"totalmatches":0,"totalmessages":0,"badmessages":0,"uniquepeople":0,"flaggedplayers":0,"timestampcached":int(time.time())}
    if os.path.exists("./statscache.json"):
        with open("./statscache.json", "r") as f:
            stats = json.load(f)
    stats["timestampcached"] = int(time.time())
    with open("./statscache.json", "w") as f:
        f.write(json.dumps(stats,indent=4))
    with querywrapper() as query:
        query.execute("SELECT COUNT(*) FROM logs_raw")
        if output := query.fetchone():
            stats["totalmatches"] = output[0]
        query.execute("SELECT COUNT(*) FROM messages")
        if output := query.fetchone():
            stats["totalmessages"] = output[0]
        query.execute("SELECT COUNT(*) FROM messages WHERE flagged = true")
        if output := query.fetchone():
            stats["badmessages"] = output[0]
        query.execute("SELECT COUNT(DISTINCT sender) FROM messages")
        if output := query.fetchone():
            stats["uniquepeople"] = output[0]
        query.execute("SELECT COUNT(DISTINCT sender) FROM messages WHERE flagged = true")
        if output := query.fetchone():
            stats["flaggedplayers"] = output[0]
        print("done caching stats")
    with open("./statscache.json", "w") as f:
        f.write(json.dumps(stats,indent=4))



@app.route("/temp",methods=["GET"])
def temp():
    print("getting temp")
    return recalltemp()

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


@app.route("/playedwith",methods=["POST","GET"])
def playedwithwrapper():
    # print(request.get_json())
    return playedwith(int(request.get_json()["url"]),request.get_json().get("expand"))

@cached(cache=TTLCache(maxsize=10, ttl=1800))
def playedwith(steam64,expand):
    offset = 25
    with querywrapper() as query:
        if not expand:
            query.execute(f"SELECT steamid2, steamid, cardinality(ids) FROM playedwith WHERE (steamid = %s OR steamid2 = %s) AND sameteam != false ORDER BY cardinality(ids) DESC  LIMIT {offset}",(steam64,steam64))
        else:
            query.execute(f"SELECT steamid2, steamid, cardinality(ids) FROM playedwith WHERE (steamid = %s OR steamid2 = %s) AND sameteam != false OFFSET {0}",(steam64,steam64))
        playedwith = dict(sorted((map(lambda x: (x[0] == steam64 and x[1] or x[0],x[2]),query.fetchall())),key = lambda x: x[1], reverse = True))
        query.execute("SELECT  steamid ,(array_agg(name ORDER BY (SELECT MAX(x) FROM unnest(ids) AS x) DESC))[1] FROM usernames WHERE steamid = ANY(%s) GROUP BY steamid",(list(playedwith.keys()),))
        logname = dict(query.fetchall())
        query.execute("SELECT steamid,currentname,avatar,frame FROM currentthings WHERE steamid = ANY(%s)",(list(playedwith.keys()),))
        logsteamdetails = query.fetchall()
        logsteamdetails = dict(map(lambda x: (x[0],x[1:]),logsteamdetails))
        # print(logsteamdetails)
        playedwith = dict(map(lambda x: (x[0],{"commonmatches":x[1],"currentname":logsteamdetails.get(x[0],[logname[x[0]]])[0],"avatar":(  "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb" if (not logsteamdetails.get(x[0],[None] * 2)[1]) or ( logsteamdetails.get(x[0],[None] * 2)[1].isdigit() and not int(logsteamdetails.get(x[0],[None] * 2)[1])) else logsteamdetails.get(x[0],[None] * 2)[1]),"frame":logsteamdetails.get(x[0],[None]*3)[2],"backupusername":logname[x[0]]}) ,playedwith.items()))
        

        query.execute(f"SELECT COUNT(*) FROM playedwith WHERE (steamid = %s OR steamid2 = %s) AND sameteam != false",(steam64,steam64))
        total = query.fetchone()[0]
    # return (json.dumps(playedwith,indent=4))
    # print({"playedwith":list(map(lambda x: {"steam64":str(x[0]),**x[1]},playedwith.items())),"biggestplayedwith": (playedwith or 0) and list(playedwith.values())[0]["commonmatches"]})
    # print(len(list(map(lambda x: {"steam64":str(x[0]),**x[1]},playedwith.items()))))
    return {"playedwith":list(map(lambda x: {"steam64":str(x[0]),**x[1]},playedwith.items())),"biggestplayedwith": (playedwith or 0) and list(playedwith.values())[0]["commonmatches"],"totalplayedwith":total}


@cached(cache=TTLCache(maxsize=1024, ttl=1800))
def resolveavatarandname(steam64,moreinfo = False,timeout = 3600):
    print(steam64)
    moreinfodict = {}
    now = int(time.time())
    with querywrapper() as query:
        query.execute("SELECT currentname,timestampcurrentname,avatar,frame FROM currentthings WHERE steamid = %s",(steam64,))
        output = query.fetchone()
        if not output or not all(output) or output[1] < now - (timeout or now):
            if timeout:
                failed = False
                r = requests.get("https://steamcommunity.com/actions/ajaxresolveusers",params = {"steamids":steam64})
                currentname = None
                frame = None
                avatarurl = None
                if r.status_code in [429]:
                    print("I GOT RATE LIMITED")
                    query.execute("SELECT  name  FROM usernames WHERE steamid = %s", (steam64,) )
                    name2 = query.fetchone()
                    currentname = name2 and name2[0] or "Unknown"
                    avatarurl = None
                    failed = True
                else:
                    r.raise_for_status()
                    if not len(r.json()):
                        query.rollback()
                        return {}  , 404
                    currentname = r.json()[0]["persona_name"]
                    avatarurl = r.json()[0]["avatar_url"]
                    profilevanity = r.json()[0]["profile_url"]
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
                    query.execute("INSERT INTO currentthings (currentname,avatar,timestampcurrentname,steamid,frame,vanity) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (steamid) DO UPDATE SET currentname = EXCLUDED.currentname, timestampcurrentname = EXCLUDED.timestampcurrentname, avatar = EXCLUDED.avatar, frame = EXCLUDED.frame, vanity = EXCLUDED.vanity",(currentname,avatarurl,now,steam64,frame,profilevanity or None))
                    query.commit()
                elif output:
                    print("I GOT RATE LIMITED")
                    currentname = currentname or output[0]
                    avatarurl = avatarurl or output[2]
                    frame = frame or output[3]
            
            else:
                query.execute("SELECT  (array_agg(name ORDER BY (SELECT MAX(x) FROM unnest(ids) AS x) DESC))[1] FROM usernames WHERE steamid = %s GROUP BY steamid",(steam64,))
                # query.execute("SELECT  name  FROM usernames WHERE steamid = %s ORDER BY ", (steam64,) )
                output = query.fetchone()
                currentname = output and output[0] or "Unknown"
                avatarurl = "0"
                frame = None
        else:
            currentname = output[0]
            avatarurl = output[2]
            frame = output[3]
        if moreinfo:
            query.execute("""SELECT COUNT(*) FROM messages WHERE (sender = %s OR sender = %s) AND flagged = true""",(Converter.to_steamID3(steam64),Converter.to_steamID(steam64)))
            moreinfodict["badwords"] = query.fetchone()[0]
            query.execute("""SELECT SUM(cardinality(ids)) FROM usernames WHERE steamid = %s GROUP BY steamid""",(steam64,))
            moreinfodict["logs"] = query.fetchone()
            moreinfodict["logs"] = moreinfodict["logs"] and moreinfodict["logs"][0]
            query.execute("""SELECT cardinality(array_agg(name ORDER BY (SELECT MAX(x) FROM unnest(ids) AS x) DESC)) FROM usernames WHERE steamid = %s GROUP BY steamid""",(steam64,))
            moreinfodict["aliases"] = query.fetchone()
            moreinfodict["aliases"] = moreinfodict["aliases"] and moreinfodict["aliases"][0]


    if not avatarurl or  (avatarurl.isdigit() and not int(avatarurl)):
        avatarurl = "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb"
    else:
        avatarurl = avatarurl
    return {"avatar":avatarurl,"frame":frame,"currentusername":currentname,**moreinfodict}

# @cached(cache=TTLCache(maxsize=30, ttl=1800))
def resolvelotsofavatars(steam64s):
    avatars = dict(zip(steam64s,["fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb"]*len(steam64s),strict = True))
    with querywrapper() as query: 
        query.execute("SELECT steamid, avatar FROM currentthings WHERE steamid = ANY(%s)",(steam64s,))
        avatars.update( dict(query.fetchall() ))
        for steamid ,avatarurl in avatars.items():
            if avatarurl.isdigit() and not int(avatarurl):
                avatars[steamid] = "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb"
    return avatars
@cached(cache=TTLCache(maxsize=1024, ttl=1800))
def resolveamessyinputtoaprofile(userid):
    now = int(time.time())
    with querywrapper() as query:
        if userid.startswith("https://steamcommunity.com/id/") or userid.startswith("steamcommunity.com/id/"):
            vanity =(userid.endswith("/") and userid[:-1] or userid).rsplit("/",1)[1]
            query.execute("SELECT vanity,steamid,lastcheckedtimestamp FROM vanityurls WHERE vanity = %s",(vanity,))
            output = query.fetchone()
            if output and output[2] > now - 86400:
                steam3 = Converter.to_steamID3(output[1])
            else:
                r = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/",params = {"key":os.getenv("STEAMAPIKEY"),"vanityurl":vanity})
                if r.status_code in [429]:
                    return 
                r.raise_for_status()
                if  r.json()["response"]["success"] != 1:
                    query.rollback()
                    return
                steam3 = Converter.to_steamID3(r.json()["response"]["steamid"]) 
                query.execute("INSERT INTO vanityurls (vanity,steamid,lastcheckedtimestamp) VALUES (%s,%s,%s) ON CONFLICT (vanity) DO UPDATE SET steamid = EXCLUDED.steamid, lastcheckedtimestamp = EXCLUDED.lastcheckedtimestamp",(vanity,r.json()["response"]["steamid"],now))
                query.commit()

        elif userid.startswith("https://steamcommunity.com/profiles/") or userid.startswith("steamcommunity.com/profiles/"):
            steam3 =  Converter.to_steamID3((userid.endswith("/") and userid[:-1] or userid).rsplit("/",1)[1])
            
        else:
            # print(userid,"pants")
            try:
                steam3 = Converter.to_steamID3(userid)
            except: 
                query.rollback()
                return resolveamessyinputtoaprofile(f"https://steamcommunity.com/id/{userid}")
                
        return( Converter.to_steamID64(steam3))


@app.route("/profile", methods=["POST"])
def resolveprofile():
    steam64 = resolveamessyinputtoaprofile(request.get_json()["url"])
    if not steam64:
        return {}, 404
    return {**resolveavatarandname(steam64,True,request.get_json().get("timeout",3600)),"steam64":steam64}

@app.route("/badwords", methods=["POST"])
def resolvename():
    return resolvename_cache(request.get_json()["url"])

@cached(cache=TTLCache(maxsize=1024, ttl=1800))
def resolvename_cache(userid):
    now = int(time.time())
    print("pulling a user at",now,userid )
    timer = time.time()
    steam64 = userid #resolveamessyinputtoaprofile(userid)

    with querywrapper() as query:
        
        if not steam64:
            return {},404
        steam3 = Converter.to_steamID3(steam64)

        
        
        query.execute("""SELECT name, message,time,id FROM messages WHERE (sender = %s OR sender = %s) AND flagged = true ORDER BY time DESC""",(steam3,Converter.to_steamID(steam3)))
        
        output = list(map(lambda x: {"name":x[0],"timestamp":x[2],"message":x[1],"matchid":x[3]},query.fetchall()))
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
        # print(resolveavatarandname(steam64))
        return  {"nonowords":reallogs} , 200






@socketio.on('connect')
def handle_connect():
    pass
    # print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    pass
    # print('Client disconnected')

@socketio.on('n')
def handle_search(data):
    now = time.time()
    emit("m",[data,defaultthing()])
    print(time.time()-now)
@cached(cache=TTLCache(maxsize=1024, ttl=86400))
def defaultthing():
    top_players_query = ("""
        SELECT  (array_agg(name ORDER BY (SELECT MAX(x) FROM unnest(ids) AS x) DESC))[1:3] ,steamid,  SUM(cardinality(ids))  as pants
        FROM usernames
       -- WHERE name ILIKE %s
        GROUP BY steamid
        ORDER BY pants DESC
        LIMIT 10;
        """)    
    with querywrapper() as query:
        query.execute("SELECT  name, steamid, cardinality(ids) FROM usernames  ORDER BY cardinality(ids) DESC LIMIT 10" )
        # query.execute(top_players_query)
        output = list(map(lambda x: {"n":x[0] if isinstance(x[0],list) else [x[0]],"id":str(x[1]),"g":x[2]}, query.fetchall()))
        avatars = resolvelotsofavatars(list(map(lambda x: int(x["id"]) , output)))
        output = list(map(lambda x: {**x,"a":avatars.get(int(x["id"]))},output))
    # print(output)
    return output


@socketio.on('s')
def handle_search(data):
    now = time.time()
    # print("PANTS",data)
    emit("m",[data[1],handle_search_helper(data[0])])
    print(data[0].ljust(10), time.time()-now)
@cached(cache=TTLCache(maxsize=10000, ttl=3600))
def handle_search_helper(data):
    now = int(time.time())

    # print("meow")

    if not data:
        return
    escaped = data.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
    #  bv said no to searching by exact match -> popularity, now we only have popularity :(   c.execute("SELECT  name, steamid, cardinality(ids) FROM usernames WHERE name ILIKE %s   AND LENGTH(name) >= LENGTH(%s) ORDER BY  (LOWER(name) = LOWER(%s)) DESC,  cardinality(ids) DESC LIMIT 10", (f'{escaped}%',escaped,escaped))
    search_query = ("""
    SELECT  (array_agg(name ORDER BY (SELECT MAX(x) FROM unnest(ids) AS x) DESC))[1:3] ,steamid,  SUM(cardinality(ids))  as pants
    FROM usernames
    WHERE name ILIKE %s
    GROUP BY steamid
    ORDER BY pants DESC
    LIMIT 10;
    """)
    with querywrapper() as query:
        query.execute(search_query, (f"{escaped}%",))
        # query.execute("SELECT  name, steamid, cardinality(ids) FROM usernames WHERE name ILIKE %s ORDER BY cardinality(ids) DESC LIMIT 10", (f'{escaped}%',))
        output = sorted(map(lambda x: {"n":x[0],"id":str(x[1]),"g":x[2]}, query.fetchall()), key = lambda x: 1)#x["n"] == data, reverse = True)
        if not output:
            # query.execute("SELECT  name, steamid, cardinality(ids) FROM usernames WHERE name ILIKE %s AND LENGTH(name) >= LENGTH(%s) ORDER BY cardinality(ids) DESC LIMIT 10", (f'%{escaped}%',escaped))
            query.execute(search_query, (f"%{escaped}%",))
            output = sorted(map(lambda x: {"n":x[0],"id":str(x[1]),"g":x[2]}, query.fetchall()), key = lambda x: 1)#, reverse = True)
        if not output: #avatarurl
            try:
                steam64 = f"{Converter.to_steamID64((escaped.endswith("/") and escaped[:-1] or escaped).replace("https://steamcommunity.com/profiles/",""))}"
            except:
                steam64 = False
            # finally:
            # query.execute("SELECT  name, steamid, cardinality(ids) FROM usernames WHERE name ILIKE %s AND LENGTH(name) >= LENGTH(%s) ORDER BY cardinality(ids) DESC LIMIT 10", (f'%{escaped}%',escaped))
            if steam64:
                query.execute(search_query.replace("name ILIKE %s","steamid = %s"), (steam64,))
                output = sorted(map(lambda x: {"n":x[0],"id":str(x[1]),"g":x[2]}, query.fetchall()), key = lambda x: 1)#, reverse = True)
        # print(output,"pants")
        if not output: #vanityurl
            query.execute("SELECT steamid FROM currentthings WHERE vanity = %s LIMIT 1", (f"{(escaped.endswith("/") and escaped[:-1] or escaped).replace("https://steamcommunity.com/id/","")}",))
            # query.execute("SELECT  name, steamid, cardinality(ids) FROM usernames WHERE name ILIKE %s ORDER BY cardinality(ids) DESC LIMIT 10", (f'{escaped}%',))
            
            steamid = query.fetchone()
            # print("HERE",steamid)
            if steamid:
                query.execute(search_query.replace("name ILIKE %s","steamid = %s"), (f"{(steamid[0])}",))

                output = sorted(map(lambda x: {"n":x[0],"id":str(x[1]),"g":x[2]}, query.fetchall()), key = lambda x: 1)#x["n"] == data, reverse = True)
        if not output: #vanityurl
            query.execute("SELECT  steamid,currentname FROM currentthings WHERE currentname ILIKE %s LIMIT 10", (f"%{(escaped.endswith("/") and escaped[:-1] or escaped).replace("https://steamcommunity.com/id/","")}%",))
            # query.execute("SELECT  name, steamid, cardinality(ids) FROM usernames WHERE name ILIKE %s ORDER BY cardinality(ids) DESC LIMIT 10", (f'{escaped}%',))
            
            steamid = dict(query.fetchall())
            # print("HERE",steamid)
            if steamid:
                query.execute(search_query.replace("name ILIKE %s","steamid = ANY(%s)"), (list(steamid.keys()),))

                output = sorted(map(lambda x: {"n":[steamid[x[1]],*x[0][0:2]],"id":str(x[1]),"g":x[2]}, query.fetchall()), key = lambda x: 1)#x["n"] == data, reverse = True)
        avatars = resolvelotsofavatars(list(map(lambda x: int(x["id"]) , output)))
        output = list(map(lambda x: {**x,"a":avatars.get(int(x["id"]))},output))
        # print(list(map(lambda x: (x["id"], x["n"]) , output)))
    
    # print(output)
    return output




# indexsomecoolmessages()
# gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --bind 0.0.0.0:3440 search:app
print("done!")

CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=3440, debug=False, allow_unsafe_werkzeug=True)


