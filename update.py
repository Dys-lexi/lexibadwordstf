import psycopg2
import json
import sys
from datetime import datetime
from psycopg2 import pool
import functools
import time
import threading
import os
import re
import requests
# from waitress import serve
# from flask_cors import CORS
# from flask import Flask, jsonify, request, send_from_directory, send_file
# [U:1:88677982]
try:
    pgpool = pool.ThreadedConnectionPool(20, 200, dsn="postgresql://pguserm:hiddenpassword@postgres:3452/realdb")
except:
    pgpool = pool.ThreadedConnectionPool(20, 200, dsn="postgresql://pguserm:hiddenpassword@localhost:3449/realdb")
root = "https://logs.tf/api/v1"
chatfilterroot = "./chatfilters/"
print("pants")


def occasionallyrunsomething():
    print("loopies")
    while True:

        occasionallyasknicelyiftherearenewlogs()
        time.sleep(3600)

def occasionallyasknicelyiftherearenewlogs():
    conn = pgpool.getconn()
    c = conn.cursor()
    c.execute("SELECT id FROM logs_raw ORDER BY id DESC LIMIT 1")
    mostrecentstoredlog = c.fetchone()
    if mostrecentstoredlog: mostrecentstoredlog = mostrecentstoredlog[0]
    # print(mostrecentstoredlog)
    # "http://logs.tf/api/v1/log?limit=N&offset=N"
    mostrecentlog = requests.get(f"{root}/log",params = {"limit":1,"offset":0})
    if mostrecentlog.status_code != requests.codes.ok:
        print("could not parse the most recent log",mostrecentlog.status_code)
        mostrecentlog.raise_for_status()
    # print(json.dumps(mostrecentlog.json(),indent=4))
    mostrecentlogid = mostrecentlog.json()["logs"][0]["id"]
    print(f"Logs downloaded: {mostrecentstoredlog:,} Logs on logs.tf: {mostrecentlogid:,}")
# to_timestamp(1481294792) AT TIME ZONE 'UTC'

    for logid in range(mostrecentstoredlog+1,mostrecentlogid+1):
        print(f"downloading log {logid:,}, {(mostrecentlogid-logid):,} logs left" )
        log = requests.get(f"{root}/log/{logid}")
        if log.status_code != requests.codes.ok and log.status_code != 404:
            print("PANIC",logid,log.status_code)
            break
        elif log.status_code == 404:
            print("^ this log is missing!")
            continue
        # print(getpriority(log.json(),["info","date"]))

        c.execute("INSERT INTO logs_raw (id,json,time,empty) VALUES (%s, %s, to_timestamp(%s), %s)",(logid,json.dumps(log.json()),getpriority(log.json(),["info","date"]),not log.json()["success"]))
        conn.commit()
    # c.execute("INSERT INTO logs_raw (id,json,time) VALUES (%s, %s, to_timestamp(%s))",(6_000_000,json.dumps({"pants":"underwear"}),time.time()))
    indexsomecoolmessages()
    




def generallyupdatethings():
    indexsomecoolmessages()
    indexsomebadwords()












def indexsomecoolmessages(firsttime = False):

    conn = pgpool.getconn()
    cursor = conn.cursor()
    print("Indexing logs")
    files = os.listdir(chatfilterroot)
    wordslist = []
    for file in files:
        with open(f"{chatfilterroot}{file}","r") as fing:
            for line in fing.readlines():
                stripped = line.strip()
                if stripped and not stripped.startswith("###") and len(stripped):
                    wordslist.append(stripped)
    pattern = r'\b(' + '|'.join([re.escape(w) for w in [word.replace('\x00', '') for word in wordslist if word.replace('\x00', '') not in  ['%', '_', '']]]) + r')\b'




    if firsttime:
        cursor.execute("UPDATE logs_raw SET empty = TRUE where (json->'success')::BOOLEAN = FALSE OR jsonb_array_length(json->'chat') = 0")
        conn.commit()
    
    
        
        
    cursor.execute("""
        SELECT l.id
        FROM logs_raw l
        LEFT JOIN (SELECT DISTINCT id FROM messages) m ON l.id = m.id
        WHERE m.id IS NULL AND l.empty IS FALSE
        ORDER BY l.id""")

    todologs = list(map(lambda x: x[0], cursor.fetchall()))
    print(f"Indexing {len(todologs):,} logs")
    todologs = functools.reduce(lambda a, b: [*a[:-1],[*a[-1],b]] if a and len(a[-1]) < 500 else [*a,[b]] ,todologs,[])
    # now = time.time()
    for i,block in enumerate(todologs):
        print(f"indexing block {i+1:,} out of {len(todologs):,}")
        cursor.execute("SELECT id, json->'chat' as chat_array, json->'info'->'date' as log_date FROM logs_raw WHERE id = ANY(%s)  ORDER BY id",(block,))
        for log in cursor.fetchall():
            logid = log[0]
            chatarray = log[1]
            log_date = log[2]
            if chatarray:
                # print("indexing",logid)
                for idwithinlogs, message in enumerate(chatarray):
                    if re.search(pattern, message["msg"], re.IGNORECASE):
                        print("found a bad word",message["msg"])
                    cursor.execute("INSERT INTO messages (id,idwithinlogs, message,sender,time,name,flagged) VALUES (%s, %s, %s, %s, %s, %s ,%s) ON CONFLICT DO NOTHING",(logid,idwithinlogs,message["msg"],message["steamid"],log_date,message["name"],bool(re.search(pattern, message["msg"], re.IGNORECASE))))
        conn.commit()
    print("Done index")
    # print(f"that took {(time.time() - now):,} seconds")









def getpriority(ditionary, *priority, **kwargs):
    """Gets dictionary value using priority-based key lookup with fallbacks"""
    for route in priority:
        output = ditionary.copy()
        if isinstance(route, str):
            route = [route]
        for place in route:
            output = output.get(place, {})
        if output != {}:
            return output
    return kwargs.get("nofind", None)







def init():
    print("init")
    conn = pgpool.getconn()

    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS vanityurls (
            url TEXT,
            steamid BIGINT,
            PRIMARY KEY (steamid)
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


# threading.Thread(target=occasionallyrunsomething,daemon=True).start()

# indexsomecoolmessages(False)
occasionallyrunsomething()
# indexsomebadwords()
# debug_indexsomebadwords()
