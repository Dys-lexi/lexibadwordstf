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
    # time.sleep(10)  

    return tempreading()
@cached(cache=TTLCache(maxsize=1024, ttl=60))
def tempreading():
    re = requests.get("https://allusive.me/temp/",timeout = 3)
    if re.ok:
        return f"{float(re.text):.2f}",200
    else:
        return "idk",500

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
    return playedwith(int(request.get_json()["steam64"]),request.get_json().get("expand"))

@cached(cache=TTLCache(maxsize=10, ttl=1800))
def playedwith(steam64,expand):
    offset = 250
    with querywrapper() as query:
        if not expand:
            query.execute(f"SELECT steamid2, steamid, cardinality(ids) FROM playedwith WHERE (steamid = %s OR steamid2 = %s) AND sameteam != false ORDER BY cardinality(ids) DESC  LIMIT {offset}",(steam64,steam64))
        else:
            query.execute(f"SELECT steamid2, steamid, cardinality(ids) FROM playedwith WHERE (steamid = %s OR steamid2 = %s) AND sameteam != false OFFSET {offset}",(steam64,steam64))
        playedwith = dict(sorted((map(lambda x: (x[0] == steam64 and x[1] or x[0],x[2]),query.fetchall())),key = lambda x: x[1], reverse = True))
        query.execute("SELECT  steamid ,(array_agg(name ORDER BY (SELECT MAX(x) FROM unnest(ids) AS x) DESC))[1] FROM usernames WHERE steamid = ANY(%s) GROUP BY steamid",(list(playedwith.keys()),))
        logname = dict(query.fetchall())
        query.execute("SELECT steamid,currentname,avatar,frame FROM currentthings WHERE steamid = ANY(%s)",(list(playedwith.keys()),))
        logsteamdetails = query.fetchall()
        logsteamdetails = dict(map(lambda x: (x[0],x[1:]),logsteamdetails))
        # print(logsteamdetails)
        playedwith = dict(map(lambda x: (x[0],{"commonmatches":x[1],"currentname":logsteamdetails.get(x[0],[logname[x[0]]])[0],"avatar":(  "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb" if (not logsteamdetails.get(x[0],[None] * 2)[1]) or ( logsteamdetails.get(x[0],[None] * 2)[1].isdigit() and not int(logsteamdetails.get(x[0],[None] * 2)[1])) else logsteamdetails.get(x[0],[None] * 2)[1]),"frame":logsteamdetails.get(x[0],[None]*3)[2],"backupusername":logname[x[0]]}) ,playedwith.items()))
        

    

    # return (json.dumps(playedwith,indent=4))
    # print({"playedwith":list(map(lambda x: {"steam64":str(x[0]),**x[1]},playedwith.items())),"biggestplayedwith": (playedwith or 0) and list(playedwith.values())[0]["commonmatches"]})
    return {"playedwith":list(map(lambda x: {"steam64":str(x[0]),**x[1]},playedwith.items())),"biggestplayedwith": (playedwith or 0) and list(playedwith.values())[0]["commonmatches"]}



@app.route("/user", methods=["POST"])
def resolvename():
    return resolvename_cache(request.get_json()["url"])

@cached(cache=TTLCache(maxsize=1024, ttl=1800))
def resolvename_cache(userid):
    now = int(time.time())
    print("pulling a user at",now)
    timer = time.time()

    # if userid.startswith("https:/steamcommunity.com/id/") or userid.startswith ("https:/steamcommunity.com/profiles/"):
    #     # stupid fucking workaround
    #     userid.replace("https:/","https://")

    # for i in userid:
    #     print("ABC:",i)
    print(userid)
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
                    return {}, 429
                r.raise_for_status()
                if  r.json()["response"]["success"] != 1:
                    query.rollback()
                    return {}, 404
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
                return resolvename_cache(f"https://steamcommunity.com/id/{userid}")
                
        steam64 = Converter.to_steamID64(steam3)
        query.execute("SELECT currentname,timestampcurrentname,avatar,frame FROM currentthings WHERE steamid = %s",(steam64,))
        output = query.fetchone()
        # int(steamid64) - STEAMID64_BASE

        if not output or not all(output) or output[1] < now - 3600:
            # print("pants")
            failed = False
            r = requests.get("https://steamcommunity.com/actions/ajaxresolveusers",params = {"steamids":steam64})
            if r.status_code in [429]:
                currentname = "Unknown (server rate limited) - cannot resolve user pfp or currentname for this request" 
                avatarurl = "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb"
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
        return  {"currentusername":currentname,"nonowords":reallogs,"avatarurl":avatarurl,"frame":frame,"steamprofile":f"https://steamcommunity.com/profiles/{steam64}","steam64":str(steam64)} , 200






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
        query.execute("SELECT steamid, avatar FROM currentthings WHERE steamid = ANY(%s)",(list(map(lambda x: int(x["id"]) , output)),))
        avatars = dict(query.fetchall() )
        for steamid ,avatarurl in avatars.items():
            if avatarurl.isdigit() and not int(avatarurl):
                avatarurl = "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb"
                avatars[steamid] = avatarurl
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
    # c.execute("""
    # WITH steamids AS (
    #     SELECT steamid FROM usernames 

    #     WHERE name ILIKE %s
    # ),
    #  occurences AS (
    # SELECT steamid, name, cardinality(ids) AS amount
    #     FROM usernames
    #     WHERE steamid IN (SELECT steamid FROM steamids)
    # )
    # SELECT 
    #     array_agg(name ORDER BY amount DESC) AS names,
    #     steamid,
    #     SUM(amount) AS total_amount,
    #      (array_agg(name ORDER BY LENGTH(name), name) FILTER (WHERE name ILIKE %s))[1]
        
        
    # FROM occurences
    # GROUP BY steamid ORDER BY total_amount DESC LIMIT 10""",(f'{escaped}%',f'{escaped}%'))

    # print(json.dumps(list(map(lambda x: {"steamid":x[0],"names":x[1],"count":x[2]} ,c.fetchall())),indent=4))
    # things = c.fetchall()
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
      
        # print(list(list(map(lambda x: x["id"],output))))
        # query.execute("SELECT steamid, avatar, timestampcurrentname FROM currentthings WHERE steamid = ANY(%s)",(list(map(lambda x: x["id"] , output)),))
        # ids = list(filter(lambda x: x["timestampcurrentname"] > now - 604800, map(lambda x:{"id":x[0],"avatar":x[1],"timestampcurrentname":x[2]}, query.fetchall())))
        # requeststomake = list(filter(lambda x: x not in list(map(lambda x: x["id"],ids)), list(map(lambda x: x["id"] , output))))
        # r = requests.get("https://steamcommunity.com/actions/ajaxresolveusers",params={"steamids":",".join(list(map(str,requeststomake)))})
        # if r.ok:
        #     avatarstore = {}
        #     for thing in r.json():

        #         query.execute("INSERT INTO currentthings (steamid, timestampcurrentname,avatar,currentname) VALUES (%s, %s, %s, %s) ON CONFLICT (steamid) DO UPDATE SET currentname = EXCLUDED.currentname, timestampcurrentname = EXCLUDED.timestampcurrentname, avatar = EXCLUDED.avatar",(int(thing["steamid"]),now,thing["avatar_url"],thing["persona_name"]))
        #         query.commit()
        #         avatarstore[int(thing["steamid"])] = {"avatar":thing["avatar_url"],"currentname":thing["persona_name"]}
        #     output = list(map(lambda x: {**x,**avatarstore[x]},output))
        # else:
        #     print(r.status_code)

        query.execute("SELECT steamid, avatar FROM currentthings WHERE steamid = ANY(%s)",(list(map(lambda x: int(x["id"]) , output)),))
        avatars = dict(query.fetchall() )
        # print(avatars)
        for steamid ,avatarurl in avatars.items():
            if avatarurl.isdigit() and not int(avatarurl):
                avatarurl = "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb"
                avatars[steamid] = avatarurl
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


# WITH occurences AS (
#     SELECT steamid, name, cardinality(ids) AS amount
#     FROM usernames
# )
# SELECT steamid,
#        string_agg(name, ', ' ORDER BY amount DESC) AS names,
#        SUM(amount) AS total_amount
# FROM occurences
# GROUP BY steamid;
