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
from initsql import querywrapper, getbadwords
import threading
import itertools

# from waitress import serve
# from flask_cors import CORS
# from flask import Flask, jsonify, request, send_from_directory, send_file
# [U:1:88677982]
try:
    pgpool = pool.ThreadedConnectionPool(20, 20, dsn="postgresql://pguserm:hiddenpassword@postgres:3452/realdb")
except:
    pgpool = pool.ThreadedConnectionPool(20, 20, dsn="postgresql://pguserm:hiddenpassword@localhost:3449/realdb")
root = "https://logs.tf/api/v1"
chatfilterroot = "./chatfilters/"
print("pants")


def occasionallyrunsomething():
    print("loopies")
    while True:
        # time.sleep(3600)
        pleasedoagainsoon = occasionallyasknicelyiftherearenewlogs()
        if not pleasedoagainsoon:
            time.sleep(3600*5.5)
        time.sleep(30)

def occasionallyasknicelyiftherearenewlogs():
    conn = pgpool.getconn()
    c = conn.cursor()
    c.execute("SELECT id FROM logs_raw ORDER BY id DESC LIMIT 1")
    now = int(time.time())
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
    pleasedoagainsoon = False
    for logid in range(mostrecentstoredlog+1,mostrecentlogid+1):
        print(f"downloading log {logid:,}, {(mostrecentlogid-logid):,} logs left" )
        try:
            log = requests.get(f"{root}/log/{logid}")
        except:
            pleasedoagainsoon = True
            break
        if log.status_code != requests.codes.ok and log.status_code != 404:
            print("PANIC",logid,log.status_code)
            pleasedoagainsoon = True
            break
        elif log.status_code == 404:
            print("^ this log is missing!")
            continue
        # print(getpriority(log.json(),["info","date"]))
        if getpriority(log.json(),["info","date"]) > now - 7200:
            print("stopping download as log is potentially ongoing")
            # pleasedoagainsoon = True
            break
        c.execute("INSERT INTO logs_raw (id,json,time,empty,isduplicate) VALUES (%s, %s, to_timestamp(%s), %s, NULL)",(logid,json.dumps(log.json()),getpriority(log.json(),["info","date"]),not log.json()["success"]))
        conn.commit()
    # c.execute("INSERT INTO logs_raw (id,json,time) VALUES (%s, %s, to_timestamp(%s))",(6_000_000,json.dumps({"pants":"underwear"}),time.time()))
    pgpool.putconn(conn)
    indexsomecoolmessages()
    return pleasedoagainsoon
    


def dumploadsofthings():
    conn = pgpool.getconn()
    c = conn.cursor()
    print("weee")
    c.execute("SELECT ids FROM uploadercounter  ORDER BY cardinality(ids) DESC OFFSET 50")
    print("teee")
    deleteids = (functools.reduce(lambda a,b:  [*a,*b[0]],c.fetchall(),[]),)
    c.execute("DELETE FROM messages WHERE id = ANY(%s)",deleteids)
    print("meee")
    conn.commit()
    pgpool.putconn(conn)


# dumploadsofthings()

def redothatmaterialview():

    print("removing logs from less reputable places")

    conn = pgpool.getconn()
    logthreshold = 500

    c = conn.cursor()

    try:
        c.execute("SELECT COUNT(*) FROM logs_raw WHERE isreuputable IS NULL")
        null_count = c.fetchone()[0]

        if null_count >= 10000:
            print("big refresh!")
            c.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY uploadercounter")

            c.execute(f"SELECT ids FROM uploadercounter WHERE cardinality(ids) > {logthreshold}")

            # print(functools.reduce(lambda a,b:  [*a,*b[0]],c.fetchall(),[]))
            c.execute("UPDATE logs_raw SET isreuputable = TRUE where id = ANY(%s)",(
                functools.reduce(lambda a,b:  [*a,*b[0]], c.fetchall(), []),
            ))

            c.execute(f"SELECT ids FROM uploadercounter  WHERE cardinality(ids) <= {logthreshold}")

            c.execute("UPDATE logs_raw SET isreuputable = FALSE where id = ANY(%s)",(
                functools.reduce(lambda a,b:  [*a,*b[0]], c.fetchall(), []),
            ))
            

        else:
            print(f"only {null_count} unprocessed logs, skipping materialized view refresh")


            c.execute(f"""
                SELECT uploaderid
                FROM uploadercounter
                WHERE cardinality(ids) > {logthreshold}
                
            """)
            

            reputable_uploaders = {row[0] for row in c.fetchall()}
            # print(reputable_uploaders)
            c.execute("""
                SELECT
                    id,
                    (json->'info'->'uploader'->'id')::TEXT AS uploaderid
                FROM logs_raw
                WHERE isreuputable IS NULL
            """)

            reputable_ids = []
            less_reputable_ids = []

            for log_id, uploaderid in c.fetchall():
                if uploaderid in reputable_uploaders:
                    reputable_ids.append(log_id)
                else:
                    less_reputable_ids.append(log_id)

            if reputable_ids:
                c.execute(
                    "UPDATE logs_raw SET isreuputable = TRUE WHERE id = ANY(%s)",
                    (reputable_ids,)
                )

            if less_reputable_ids:
                c.execute(
                    "UPDATE logs_raw SET isreuputable = FALSE WHERE id = ANY(%s)",
                    (less_reputable_ids,)
                )

        conn.commit()
        c.execute("SELECT id, json->'names', json->'info'->'uploader'->'id' FROM logs_raw WHERE isreuputable = FALSE AND empty IS FALSE ORDER BY id DESC")
        c.execute("UPDATE logs_raw SET isreuputable = TRUE WHERE id = ANY(%s)",(list(map(lambda x: x[0],list(filter( lambda x: x[2]   and x[2].isdigit() and int(x[2]) and len(x[2]) == 17 and (Converter.to_steamID3(x[2]) in x[1] or Converter.to_steamID(x[2]) in  x[1]), c.fetchall())))),))
        # c.execute("UPDATE messages AS m SET trusted = r.isreuputable FROM logs_raw AS r WHERE m.id = r.id")
        conn.commit()
    except Exception:
        conn.rollback()
        pgpool.putconn(conn)
        raise

    finally:
        pgpool.putconn(conn)











def indexsomecoolmessages(firsttime = False):
    redothatmaterialview()
    biglogsdedupe(False) 
    conn = pgpool.getconn()
    cursor = conn.cursor()
    print("Indexing logs")


    if firsttime:
        cursor.execute("UPDATE logs_raw SET empty = TRUE where (json->'success')::BOOLEAN = FALSE OR jsonb_array_length(json->'chat') = 0")
        conn.commit()
        howlongodesthistake()
    
    
        
        
    cursor.execute("""
        SELECT l.id
        FROM logs_raw l
        LEFT JOIN (SELECT DISTINCT id FROM messages) m ON l.id = m.id
        WHERE m.id IS NULL AND l.empty IS FALSE AND l.isduplicate IS NOT TRUE AND isreuputable IS TRUE
        ORDER BY l.id""")

    todologs = list(map(lambda x: x[0], cursor.fetchall()))
    print(f"Indexing {len(todologs):,} logs")
    initplayedwith(todologs)
    usernamesync(todologs)
    messagesync(todologs)
    print("done!")




def coolfunctionthatreturnslotsoids(thingtoreturn,todologs = None):
    conn = pgpool.getconn()
    cursor = conn.cursor()
    if todologs == None: 
        cursor.execute(f"""SELECT id FROM logs_raw WHERE empty = false AND isduplicate IS NOT TRUE AND  isreuputable IS TRUE ORDER BY id DESC""")
        todologs = list(map(lambda x: x[0], cursor.fetchall()))
    todologs = functools.reduce(lambda a, b: [*a[:-1],[*a[-1],b]] if a and len(a[-1]) < 10000 else [*a,[b]] ,todologs,[])
    for i,block in enumerate(todologs):
        cursor.execute(f"SELECT id,  {thingtoreturn} FROM logs_raw WHERE id = ANY(%s)  ORDER BY id",(block,))
        print("doing block",i+1,"out of",len(todologs))
        for log in cursor.fetchall():
            yield {"log":log[0],"data":log[1:]}
    pgpool.putconn(conn)

def initplayedwith(todologs = None):
    print("Updating people played with")

    for log in coolfunctionthatreturnslotsoids("json->'players'", todologs):
        setplayedwith(log["log"],[{"players":log["data"][0],"length":1}] )
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


def messagesync(todologs = None):
    print("Updating messages")
    # print(todologs)
    pattern = getbadwords()
    conn = pgpool.getconn()
    c = conn.cursor()
    for log in coolfunctionthatreturnslotsoids("json->'chat' as chat_array, json->'info'->'date' as log_date", todologs):
        
        logid = log["log"]
        chatarray = log["data"][0]
        log_date = log["data"][1]
        for idwithinlogs, message in enumerate(chatarray):
            # if re.search(pattern, message["msg"], re.IGNORECASE):
            #     print("found a bad word",message["name"].ljust(20)+":",message["msg"])
            c.execute("INSERT INTO messages (id,idwithinlogs, message,sender,time,name,flagged) VALUES (%s, %s, %s, %s, %s, %s ,%s) ON CONFLICT DO NOTHING",(logid,idwithinlogs,message["msg"],message["steamid"],log_date,message["name"],bool(re.search(pattern, message["msg"], re.IGNORECASE))))
    
        conn.commit()
    pgpool.putconn(conn) 




def usernamesync(todologs = None):
    print("Updating usernames")
    conn = pgpool.getconn()
    c = conn.cursor()
    for log in coolfunctionthatreturnslotsoids("json->'names'", todologs):
        for id,name in log["data"][0].items():
            try:
                id = Converter.to_steamID64(id)
            except:
                continue
            c.execute("INSERT INTO usernames (name,steamid,ids,deletedaccount) VALUES (%s,%s,%s,false) ON CONFLICT (name,steamid) DO UPDATE SET ids = array_append(usernames.ids, %s) WHERE NOT (usernames.ids @> ARRAY[%s])",(name,id,[log["log"]],log["log"],log["log"]))


    conn.commit()
    pgpool.putconn(conn)



def biglogsdedupe(all = True):
    conn = pgpool.getconn()
    c = conn.cursor()
    print("deduping logs")
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


# def removedupesfromusernames():
#     conn = pgpool.getconn()
#     c = conn.cursor()
#     print("removing duplicate ids from usernames")
#     c.execute("""
#         UPDATE usernames u
#         SET ids = ARRAY(
#             SELECT x
#             FROM unnest(u.ids) AS x
#             WHERE NOT EXISTS (
#                 SELECT 1 FROM logs_raw l WHERE l.id = x AND l.isduplicate IS TRUE
#             )
#         )
#         WHERE EXISTS (
#             SELECT 1
#             FROM unnest(u.ids) AS x
#             JOIN logs_raw l ON l.id = x
#             WHERE l.isduplicate IS TRUE
#         )
#     """)
#     print(f"updated {c.rowcount} username rows")
#     conn.commit()
#     pgpool.putconn(conn)
#     print("done")


def slowlypullpeoplesavatars(): # DO NOT INCREASE LIMIT, FUNC NO LONGER WORKS WITHOUT IT (also the steam api no support)
    laststatuses = 0
    while True:
        with querywrapper() as query:
            now = int(time.time())
            query.execute("SELECT l.steamid FROM usernames AS l LEFT JOIN currentthings AS r ON l.steamid = r.steamid WHERE deletedaccount = false AND r.timestampcurrentname IS NULL OR r.timestampcurrentname < %s GROUP BY l.steamid ORDER BY SUM(cardinality(l.ids)) DESC LIMIT 100",(604800*10,))
            output1 = list(map(lambda x: x[0], query.fetchall()))
            if not output1:
                print("pulling names thinks it is done")
                query.execute("SELECT * FROM usernames AS l LEFT JOIN currentthings AS r ON l.steamid = r.steamid WHERE r.timestampcurrentname IS NULL OR r.timestampcurrentname < %s GROUP BY l.steamid ORDER BY SUM(cardinality(l.ids)) DESC LIMIT 1",(604800*10,))
                print(query.fetchall())
                time.sleep(3600)
                continue
            for output in output1:
                output = [output,]

                # print("pulling",output)
                r = requests.get("https://steamcommunity.com/actions/ajaxresolveusers",params={"steamids":",".join(list(map(str,output)))},headers = {"User-Agent": "Mozilla/5.0"})
                if r.ok:
                    laststatuses = 0
                    if not r.json():
                        print("could not find profile for",output)
                        query.execute("UPDATE usernames SET deletedaccount = true WHERE steamid = %s",(output[0],))
                        continue
                    # print("pulled avatar for",r.json()[0].get("persona_name", "UNKNWON PERSONA NAME"))
                    if not r.json()[0].get("persona_name"):
                        print(json.dumps(r.json(),indent = 4))
                        print("COULD NOT FIND PERSONA NAME")
                        continue
                    query.execute("INSERT INTO currentthings (steamid, timestampcurrentname, avatar, currentname, vanity) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (steamid) DO UPDATE SET timestampcurrentname = EXCLUDED.timestampcurrentname, avatar = EXCLUDED.avatar, currentname = EXCLUDED.currentname, vanity = EXCLUDED.vanity", (int(r.json()[0]["steamid"]), now, r.json()[0]["avatar_url"], r.json()[0]["persona_name"], r.json()[0]["profile_url"] or None))
                    query.commit()
                else:
                    # print(r.status_code)
                    if r.status_code == 429:
                        laststatuses += 1
                        time.sleep(laststatuses*20)
                time.sleep(2)



if False: # first time stuff, otherwise is incremental (but tbh incremental will get it)
    biglogsdedupe()
    indexsomecoolmessages(True)
    removedupesfromusernames() #not needed
    initplayedwith()

# initplayedwith()
# time.sleep(8640000)
# threading.Thread(target=occasionallyrunsomething, daemon=True).start()
threading.Thread(target=slowlypullpeoplesavatars, daemon=True).start()
# indexsomebadwords()

occasionallyrunsomething()
# debug_indexsomebadwords()

# slowlypullpeoplesavatars()
