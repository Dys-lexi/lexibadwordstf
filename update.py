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
from steamid_converter import Converter
import initsql
import threading
import itertools

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
        time.sleep(3600)
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

        c.execute("INSERT INTO logs_raw (id,json,time,empty,isduplicate) VALUES (%s, %s, to_timestamp(%s), %s, NULL)",(logid,json.dumps(log.json()),getpriority(log.json(),["info","date"]),not log.json()["success"]))
        conn.commit()
    # c.execute("INSERT INTO logs_raw (id,json,time) VALUES (%s, %s, to_timestamp(%s))",(6_000_000,json.dumps({"pants":"underwear"}),time.time()))
    pgpool.putconn(conn)
    generallyupdatethings()
    
    




def generallyupdatethings():
    biglogsdedupe(False) 
    indexsomecoolmessages()
    












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
        howlongodesthistake()
    
    
        
        
    cursor.execute("""
        SELECT l.id
        FROM logs_raw l
        LEFT JOIN (SELECT DISTINCT id FROM messages) m ON l.id = m.id
        WHERE m.id IS NULL AND l.empty IS FALSE AND l.isduplicate != true
        ORDER BY l.id""")

    todologs = list(map(lambda x: x[0], cursor.fetchall()))
    print(f"Indexing {len(todologs):,} logs")
    todologs = functools.reduce(lambda a, b: [*a[:-1],[*a[-1],b]] if a and len(a[-1]) < 500 else [*a,[b]] ,todologs,[])
    initplayedwith(todologs)
    # now = time.time()
    for i,block in enumerate(todologs):
        print(f"indexing block {i+1:,} out of {len(todologs):,}")
        cursor.execute("SELECT id, json->'chat' as chat_array, json->'info'->'date' as log_date,  json->'names' FROM logs_raw WHERE id = ANY(%s)  ORDER BY id",(block,))
        for log in cursor.fetchall():
            logid = log[0]
            chatarray = log[1]
            log_date = log[2]

            for id,name in log[3].items():
                try:
                    cursor.execute("INSERT INTO usernames (name,steamid,ids,deletedaccount) VALUES (%s,%s,%s,false) ON CONFLICT (name,steamid) DO UPDATE SET ids = array_append(usernames.ids, %s) WHERE NOT (usernames.ids @> ARRAY[%s])",(name,Converter.to_steamID64(id),[logid],logid,logid))
                except Exception as e:
                    print("brokey",e)

                

            if chatarray:
                # print("indexing",logid)
                for idwithinlogs, message in enumerate(chatarray):
                    if re.search(pattern, message["msg"], re.IGNORECASE):
                        print("found a bad word",message["msg"])
                    cursor.execute("INSERT INTO messages (id,idwithinlogs, message,sender,time,name,flagged) VALUES (%s, %s, %s, %s, %s, %s ,%s) ON CONFLICT DO NOTHING",(logid,idwithinlogs,message["msg"],message["steamid"],log_date,message["name"],bool(re.search(pattern, message["msg"], re.IGNORECASE))))
        conn.commit()
    print("Done index")
    pgpool.putconn(conn)
    # print(f"that took {(time.time() - now):,} seconds")



def initplayedwith(todologs = False):
    print("Updating people played with")
    conn = pgpool.getconn()
    cursor = conn.cursor()
    if not todologs:
        cursor.execute(f"""
            SELECT id FROM logs_raw WHERE empty = false AND isduplicate != true  ORDER BY id""")
        todologs = list(map(lambda x: x[0], cursor.fetchall()))
        todologs = functools.reduce(lambda a, b: [*a[:-1],[*a[-1],b]] if a and len(a[-1]) < 500 else [*a,[b]] ,todologs,[])

    for i,block in enumerate(todologs):
        print(f"doing played with for block {i+1:,} out of {len(todologs):,}")
        cursor.execute("SELECT id,  json->'players' FROM logs_raw WHERE id = ANY(%s)  ORDER BY id",(block,))
        for log in cursor.fetchall():
            setplayedwith(log[0],[{"players":log[1],"length":1}] )
        # cursor.execute("SELECT id,  json->'rounds', json->'info'->'rounds' FROM logs_raw WHERE id = ANY(%s)  ORDER BY id",(block,))
        # for log in cursor.fetchall():
        #     setplayedwith(log[0],log[1] or log[2])

    pgpool.putconn(conn)



def setplayedwith(id,rounds):
    # print(rounds)
    conn = pgpool.getconn()
    cursor = conn.cursor()
    trueteams = {}
    for round in rounds:
        length = round["length"]
        for player,data in round["players"].items():
            trueteams.setdefault(data.get("team",None),{}).setdefault(player,0) 
            trueteams[data.get("team",None)][player] += length
    truerteams = {}
    for person in functools.reduce(lambda a,b: list({*a,*list(map(lambda x: x,b[1].keys()))}) ,trueteams.items(),[]):
        counter = (0,0)
        for team, data in trueteams.items():
            if data.get(person,0) > counter[1]:
                counter = [team,data.get(person,0)]
        truerteams[person] = counter[0]
    namesdone = []
    for person,team in truerteams.items():
        namesdone.append(person)
        try:
            person = Converter.to_steamID64(person)
        except:
            continue
        for person2, team2 in filter(lambda x: x[0] not in namesdone,truerteams.items()):

            try:
                person2 = Converter.to_steamID64(person2)
            except:
                continue
            if person == person2:
                print("ono")
                break

            cursor.execute("INSERT INTO playedwith (steamid,steamid2,ids,sameteam) VALUES (%s,%s,%s,%s) ON CONFLICT (steamid,steamid2,sameteam) DO UPDATE SET ids = array_append(playedwith.ids, %s) WHERE NOT (playedwith.ids @> ARRAY[%s])",(*sorted([person,person2]),[id],team and (team == team2) ,id,id))

    conn.commit()
    pgpool.putconn(conn)



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







def howlongodesthistake():
    conn = pgpool.getconn()
    c = conn.cursor()
    print("wee")

    last_id = 0
    batch_num = 0
    while True:
        c.execute("SELECT id, json->'names' FROM logs_raw WHERE empty = false AND id > %s AND isduplicate != true ORDER BY id LIMIT 5000", (last_id,))
        output = c.fetchall()

        if not output:
            break

        batch_num += 1
        print(f"Processing batch {batch_num}, rows {len(output)}")

        for thing in output:
            logid = thing[0]
            last_id = logid
            for id,name in thing[1].items():
                try:
                    id = Converter.to_steamID64(id)
                except:
                    continue
                c.execute("INSERT INTO usernames (name,steamid,ids,deletedaccount) VALUES (%s,%s,%s,false) ON CONFLICT (name,steamid) DO UPDATE SET ids = array_append(usernames.ids, %s) WHERE NOT (usernames.ids @> ARRAY[%s])",(name,id,[logid],logid,logid))

        conn.commit()
        print(f"Batch {batch_num} committed")

    print("done")
    pgpool.putconn(conn)


def biglogsdedupe(all = True):
    conn = pgpool.getconn()
    c = conn.cursor()
    print("deduping")
    c.execute(f"""
    WITH logdata AS (
        SELECT
            id,
            (json->'info'->>'date')::BIGINT          AS timestamp,
            json->'info'->'map'                      AS map,
            (json->'info'->>'total_length')::INTEGER AS total_length
        FROM logs_raw WHERE empty = FALSE AND (json->'success')::BOOLEAN = TRUE {"AND id >= COALESCE((SELECT id FROM logs_raw WHERE isduplicate = FALSE ORDER BY id DESC LIMIT 1),0)" if not all else ""}
    ),
    flagged AS (
        -- 1 = starts a new group, 0 = belongs to the previous row's group
        SELECT *,
            CASE
                WHEN timestamp - LAG(timestamp) OVER w <= 120 THEN 0
                ELSE 1
            END AS is_new_group
        FROM logdata
        WINDOW w AS (PARTITION BY map, total_length ORDER BY timestamp)
    ),
    grouped AS (
        SELECT *,
            SUM(is_new_group) OVER (PARTITION BY map, total_length ORDER BY timestamp) AS grp
        FROM flagged
    )
    SELECT array_agg(id ORDER BY timestamp) AS duplicate_ids
    FROM grouped
    GROUP BY map, total_length, grp
    HAVING COUNT(*) > 1""")
    output = c.fetchall()
    print(f"found {len(output)} dupes")
    duplicate_groups = [row[0] for row in output]
    
    c.execute("UPDATE logs_raw SET isduplicate = true WHERE id = ANY(%s) AND isduplicate IS NULL",(list(itertools.chain.from_iterable(list(map(lambda x: x[1:],(duplicate_groups))))),))
    c.execute("UPDATE logs_raw SET isduplicate = false WHERE id = ANY(%s) AND isduplicate IS NULL",(list(map(lambda x: x[0],duplicate_groups)),))
    conn.commit()
    pgpool.putconn(conn)
    print("set dupes")
    # print("\n".join(list(map(str,duplicate_groups))))
    print(len(duplicate_groups),"duplicates found")


def removedupesfromusernames():
    conn = pgpool.getconn()
    c = conn.cursor()
    print("removing duplicate ids from usernames")
    c.execute("""
        UPDATE usernames u
        SET ids = ARRAY(
            SELECT x
            FROM unnest(u.ids) AS x
            WHERE NOT EXISTS (
                SELECT 1 FROM logs_raw l WHERE l.id = x AND l.isduplicate IS TRUE
            )
        )
        WHERE EXISTS (
            SELECT 1
            FROM unnest(u.ids) AS x
            JOIN logs_raw l ON l.id = x
            WHERE l.isduplicate IS TRUE
        )
    """)
    print(f"updated {c.rowcount} username rows")
    conn.commit()
    pgpool.putconn(conn)
    print("done")


def slowlypullpeoplesavatars(): # DO NOT INCREASE LIMIT, FUNC NO LONGER WORKS WITHOUT IT (also the steam api no support)
    conn = pgpool.getconn()
    c = conn.cursor()
    laststatuses = 0
    while True:
        now = int(time.time())
        c.execute("SELECT l.steamid FROM usernames AS l LEFT JOIN currentthings AS r ON l.steamid = r.steamid WHERE deletedaccount = false AND r.timestampcurrentname IS NULL OR r.timestampcurrentname < %s GROUP BY l.steamid ORDER BY SUM(cardinality(l.ids)) DESC LIMIT 1",(604800*10,))
        output = list(map(lambda x: x[0], c.fetchall()))
        output = [output[0],]
        if not output:
            print("pulling names thinks it is done")
            c.execute("SELECT * FROM usernames AS l LEFT JOIN currentthings AS r ON l.steamid = r.steamid WHERE r.timestampcurrentname IS NULL OR r.timestampcurrentname < %s GROUP BY l.steamid ORDER BY SUM(cardinality(l.ids)) DESC LIMIT 1",(604800*10,))
            print(c.fetchall())
            time.sleep(3600)
            continue
        print("pulling",output)
        r = requests.get("https://steamcommunity.com/actions/ajaxresolveusers",params={"steamids":",".join(list(map(str,output)))},headers = {"User-Agent": "Mozilla/5.0"})
        if r.ok:
            laststatuses = 0
            if not r.json():
                print("could not find profile for",output)
                c.execute("UPDATE usernames SET deletedaccount = true WHERE steamid = %s",(output[0],))
                continue
            print("pulled avatar for",r.json()[0].get("persona_name", "UNKNWON PERSONA NAME"))
            if not r.json()[0].get("persona_name"):
                print(json.dumps(r.json(),indent = 4))
                print("COULD NOT FIND PERSONA NAME")
                continue
            c.execute("INSERT INTO currentthings (steamid,timestampcurrentname,avatar,currentname,vanity) VALUES (%s,%s,%s,%s,%s)",(int(r.json()[0]["steamid"]),now,r.json()[0]["avatar_url"],r.json()[0]["persona_name"],r.json()[0]["profile_url"] or None ))
            conn.commit()
        else:
            print(r.status_code)
            if r.status_code == 429:
                laststatuses += 1
                time.sleep(laststatuses*20)
        time.sleep(2)



if False: # first time stuff, otherwise is incremental (but tbh incremental will get it)
    biglogsdedupe()
    indexsomecoolmessages(True)
    removedupesfromusernames() #not needed
    initplayedwith()

initplayedwith()
time.sleep(8640000)
# threading.Thread(target=occasionallyrunsomething, daemon=True).start()
threading.Thread(target=slowlypullpeoplesavatars, daemon=True).start()
# indexsomebadwords()

occasionallyrunsomething()
# debug_indexsomebadwords()

# slowlypullpeoplesavatars()