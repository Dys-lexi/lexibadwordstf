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
load_dotenv()

pgpool = pool.ThreadedConnectionPool(20, 200, dsn="postgresql://pguserm:hiddenpassword@localhost:3449/realdb")
root = "https://logs.tf/api/v1"
app = Flask(__name__)
















def indexsomecoolmessages(todologs = []):
    print("e logs")
    conn = pgpool.getconn()
    cursor = conn.cursor()

    cursor.execute("""SELECT name, message,time FROM messages WHERE sender = '[U:1:88677982]' AND flagged = true ORDER BY time""")

    output = list(map(lambda x: f"{datetime.fromtimestamp(x[2], pants.UTC).strftime('%d-%m-%Y %H:%M:%S')} {x[0]}: {x[1]}",cursor.fetchall()))
    print("\n".join(output))
    



@app.route("/user", methods=["POST"])
def resolvename(userid = False):
    if not userid:
        userid = request.get_json()["url"]
    print("meow")
    conn = pgpool.getconn()
    c = conn.cursor()
    

    if userid.startswith("https://steamcommunity.com/id/") or userid.startswith("steamcommunity.com/id/"):
        vanity =(userid.endswith("/") and userid[:-1] or userid).rsplit("/",1)[1]
        c.execute("SELECT vanity,steamid,lastcheckedtimestamp FROM vanityurls WHERE vanity = %s",(vanity,))
        output = c.fetchone()
        if output and output[2] > int(time.time()) - 86400:
            steam3 = Converter.to_steamID3(output[1])
        else:
            r = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/",params = {"key":os.getenv("STEAMAPIKEY"),"vanityurl":vanity})
            r.raise_for_status()
            if  r.json()["response"]["success"] != 1:
                return {}, 404
            steam3 = Converter.to_steamID3(r.json()["response"]["steamid"]) 
            c.execute("INSERT INTO vanityurls (vanity,steamid,lastcheckedtimestamp) VALUES (%s,%s,%s) ON CONFLICT (vanity) DO UPDATE SET steamid = EXCLUDED.steamid, lastcheckedtimestamp = EXCLUDED.lastcheckedtimestamp",(vanity,r.json()["response"]["steamid"],int(time.time())))
            conn.commit()
        
       

    elif userid.startswith("https://steamcommunity.com/profiles/") or userid.startswith("steamcommunity.com/profiles/"):
        steam3 =  Converter.to_steamID3((userid.endswith("/") and userid[:-1] or userid).rsplit("/",1)[1])
        
    else:
        try:
            steam3 = Converter.to_steamID3(userid)
        except: 
            return resolvename(f"https://steamcommunity.com/id/{userid}")
            
    steam64 = Converter.to_steamID64(steam3)
    c.execute("SELECT currentname,timestampcurrentname,avatar FROM currentthings WHERE steamid = %s",(steam64,))
    output = c.fetchone()
    if not output or not any(output) or output[1] < int(time.time()) - 3600:
        r = requests.get("https://steamcommunity.com/actions/ajaxresolveusers",params = {"steamids":steam64})
        r.raise_for_status()
        if not len(r.json()):
            return {}  , 404
        currentname = r.json()[0]["persona_name"]
        avatarurl = r.json()[0]["avatar_url"]
        c.execute("INSERT INTO currentthings (currentname,avatar,timestampcurrentname,steamid) VALUES (%s,%s,%s,%s) ON CONFLICT (steamid) DO UPDATE SET currentname = EXCLUDED.currentname, timestampcurrentname = EXCLUDED.timestampcurrentname, avatar = EXCLUDED.avatar",(currentname,avatarurl,int(time.time()),steam64))
        conn.commit()
    else:
        currentname = output[0]
        avatarurl = output[2]

    if avatarurl.isdigit() and not int(avatar_url):
        avatarurl = "https://avatars.fastly.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg"
    else:
        avatarurl = f"https://avatars.steamstatic.com/{avatarurl}_full.jpg"

    
    c.execute("""SELECT name, message,time,id FROM messages WHERE (sender = %s OR sender = %s) AND flagged = true ORDER BY time""",(steam3,Converter.to_steamID(steam3)))
    output = list(map(lambda x: {"name":x[0],"timestamp":x[2],"message":x[1],"matchid":x[3]},c.fetchall()))
    return  {"currentusername":currentname,"nonowords":output,"avatarurl":avatarurl} , 200










def init():
    print("init")
    conn = pgpool.getconn()

    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS vanityurls (
            vanity TEXT PRIMARY KEY,

            lastcheckedtimestamp BIGINT,
            steamid BIGINT

        )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS currentthings (

            steamid BIGINT PRIMARY KEY,

            timestampcurrentname BIGINT,
            avatar TEXT,
            currentname TEXT

        )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS messages (
            id INTEGER,
            idwithinlogs INTEGER,
            message TEXT,
            sender TEXT,
            time BIGINT,
            name TEXT,
            flagged BOOLEAN,
            PRIMARY KEY (id, idwithinlogs)
        )"""
    )

    cursor.execute(
    """CREATE TABLE IF NOT EXISTS badmessages (
        id INTEGER,
        idwithinlogs INTEGER,
        message TEXT,
        sender TEXT,
        time BIGINT,
        name TEXT,
        PRIMARY KEY (id, idwithinlogs)
    )"""
    )

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_id ON messages (id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_id ON logs_raw (id)")
    cursor.execute("ALTER TABLE logs_raw ADD COLUMN IF NOT EXISTS isduplicate BOOLEAN DEFAULT FALSE")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_empty ON logs_raw (empty)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_isduplicate ON logs_raw (isduplicate)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_flagged ON messages(sender) WHERE flagged = true;")
    conn.commit()
init()


# indexsomecoolmessages()

CORS(app, resources={r"/*": {"origins": "*"}})
serve(app, host="0.0.0.0", port=3440, threads=40, connection_limit=200)  