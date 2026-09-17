from contextvars import ContextVar
from psycopg2 import pool
from cachetools import cached, LRUCache, TTLCache
import os
import re
import inspect
import random
import threading
from datetime import datetime
try:
    pgpool = pool.ThreadedConnectionPool(5, 300, dsn="postgresql://pguserm:hiddenpassword@postgres:3452/realdb")
except:
    pgpool = pool.ThreadedConnectionPool(5, 300, dsn="postgresql://pguserm:hiddenpassword@localhost:3449/realdb")
chatfilterroot = "./chatfilters/"

def threadedprint(*args):
  
    threading.Thread(target=threadedprintreal, args = args, kwargs = {"line": str(inspect.currentframe().f_back.f_lineno),"func": str(inspect.currentframe().f_back.f_code.co_name)}, daemon=True).start()

def threadedprintreal(*args,**kwargs):
    output = []
    for arg in args:
        if isinstance(arg, list) or  isinstance(arg, tuple):
            # print(arg["func"](*arg.get("args",[])))
            # print("meow",arg[0](*arg[1:]))
            output.append(str(arg[0](*arg[1:])))
        else:
            output.append(str(arg))
    print(" ".join(output),function=kwargs["func"],line=kwargs["line"])
class returningthread(threading.Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return

realprint = print
linecolours = {}
lastfuncline = ""
def print(*message, end="\033[0m\n",function = None,line=None):
    global linecolours, lastfuncline
    message = (
        " ".join([str(i) for i in message])
        .replace("[110m", "[38;2;200;200;200m")
        .replace("[111m", "[38;2;80;229;255m")
        .replace("[112m", "[38;2;213;80;16m")
    )


    function = function or  str(inspect.currentframe().f_back.f_code.co_name)
    line = line or str(inspect.currentframe().f_back.f_lineno)
    if line not in linecolours:
        while True:
            colour = random.randint(0, 255)
            if colour not in DISALLOWED_COLOURS:
                break
        linecolours[line] = colour
    currentfuncline = f"{line},{function}"
    if False:
        realprint(
            f"[0m{(('[' + function[:9].ljust(9) + ']') if currentfuncline != lastfuncline else '⯈'.ljust(11))}{('[' + line.ljust(3) + ']')}[{datetime.now().strftime('%H:%M:%S %d/%m')}] {message}"
        )
    else:
        realprint(
            f"[38;2;215;22;105m{(('[' + function[:9].ljust(9) + ']') if currentfuncline != lastfuncline else '⯈'.ljust(11))}[38;2;126;89;140m{('[' + line.ljust(3) + ']')}[38;2;27;64;152m[{datetime.now().strftime('%H:%M:%S %d/%m')}][38;5;{linecolours[line]}m {(message)}",
            end=end,
        )
    lastfuncline = currentfuncline


DISALLOWED_COLOURS = (
    0,
    52,
    16,
    18,
    17,
    20,
    23,
    25,
    24,
    59,
    60,
    62,
    61,
    58,
    65,
    95,
    61,
    54,
    92,
    102,
    101,
    232,
    233,
    234,
    235,
    236,
    237,
    238,
    239,
    240,
    57,
    56,
    19,
    91,
    89,
    90,
    88,
    96,
    53
)


@cached(cache=TTLCache(maxsize=10, ttl=600))
def getbadwords():
    files = os.listdir(chatfilterroot)
    wordslist = []
    for file in files:
        with open(f"{chatfilterroot}{file}","r") as fing:
            for line in fing.readlines():
                stripped = line.strip()
                if stripped and not stripped.startswith("###") and len(stripped):
                    wordslist.append(stripped)
    return r'\b(' + '|'.join([re.escape(w) for w in [word.replace('\x00', '') for word in wordslist if word.replace('\x00', '') not in  ['%', '_', '']]]) + r')\b'
def getpriority(ditionary, *priority, **kwargs):
    """Gets dictionary value using priority-based key lookup with fallbacks"""
    for route in priority:
        if not route:
            continue
        output = ditionary.copy()
        if isinstance(route, str):
            route = [route]
        for place in route:
            output = output.get(place, {})
        if output != {}:
            return output
    return kwargs.get("nofind", None)


class querywrapper:
    def __init__(self):
        self.pool = pgpool
        self.conn = pgpool.getconn()
        self.c = self.conn.cursor()

    def __enter__(self):
        return self

    def execute(self, *query):
        self.c.execute(*query)

    def fetchall(self):
        return self.c.fetchall()

    def fetchone(self):
        return self.c.fetchone()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cleanup()
        return False  # important: don't suppress exceptions

    def cleanup(self):
        try:
            self.c.close()
            self.pool.putconn(self.conn)
        except Exception as e:
            print("error when closing conn", e)



with querywrapper() as query:
    query.execute("""SELECT tablename   FROM pg_tables""")
    tables = list(map(lambda x: x[0] ,query.fetchall()))
def init():
    print("init")
    conn = pgpool.getconn()

    c = conn.cursor()
    c.execute( # barely used, as overshadowed by currentname
        """CREATE TABLE IF NOT EXISTS vanityurls (
            vanity TEXT PRIMARY KEY,

            lastcheckedtimestamp BIGINT,
            steamid BIGINT


        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS usernames (

            name TEXT,

            steamid BIGINT,
            ids INTEGER[],
            deletedaccount BOOLEAN,
            PRIMARY KEY (name, steamid)

        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS playedwith (

            steamid BIGINT,
            steamid2 BIGINT,
            ids INTEGER[],
            sameteam BOOLEAN,
            UNIQUE NULLS NOT DISTINCT (steamid, steamid2, sameteam)
            
            

        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS logdata (
            id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            timestamp BIGINT,
            ip TEXT,
            path TEXT,
            useragent TEXT,
            cfcountry TEXT,
            isclient BOOLEAN,
            cfray TEXT,
            hostname TEXT
        )"""
    )
    # print("weee")
    c.execute(
        """CREATE TABLE IF NOT EXISTS currentthings (

            steamid BIGINT PRIMARY KEY,

            timestampcurrentname BIGINT,
            frame TEXT,
            avatar TEXT,
            currentname TEXT,
            vanity TEXT

        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS messages (
            id INTEGER,
            idwithinlogs INTEGER,
            message TEXT,
            sender TEXT,
            time BIGINT,
            name TEXT,
            flagged BOOLEAN,
            trusted BOOLEAN,
            PRIMARY KEY (id, idwithinlogs)
        )"""
    )

    c.execute(
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
    # c.execute("DROP MATERIALIZED VIEW uploadercounter")
    c.execute(
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS uploadercounter AS
        SELECT
            (json->'info'->'uploader'->'id')::TEXT AS uploaderid,
            ARRAY_AGG(DISTINCT id) AS ids
        FROM logs_raw
        GROUP BY (json->'info'->'uploader'->'id')::TEXT;
        """
    )

    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS name ON uploadercounter(uploaderid);")

    c.execute("ALTER TABLE messages ADD COLUMN IF NOT EXISTS trusted BOOLEAN")
    # print("teee")
    c.execute("CREATE INDEX IF NOT EXISTS idx_messages_id ON messages (id)")
    # print("a")
    c.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_id ON logs_raw (id)")
    # print("b")
    c.execute("ALTER TABLE currentthings ADD COLUMN IF NOT EXISTS vanity TEXT")

    c.execute("ALTER TABLE logs_raw ADD COLUMN IF NOT EXISTS empty BOOLEAN")
    c.execute("ALTER TABLE logs_raw ADD COLUMN IF NOT EXISTS isduplicate BOOLEAN")
    c.execute("ALTER TABLE logs_raw ADD COLUMN IF NOT EXISTS isreuputable BOOLEAN")
    # c.execute("UPDATE logs_raw SET isduplicate = NULL")
    # print("c")
    c.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_isreuputable ON logs_raw (isreuputable)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_isduplicate ON logs_raw (isduplicate)")

    c.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_empty ON logs_raw (empty)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_isreuputable ON logs_raw (isreuputable)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_playedwith_steamid ON playedwith (steamid)")

    c.execute("CREATE INDEX IF NOT EXISTS idx_playedwith_steamid2 ON playedwith (steamid2)")
    # print("d")
    c.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_isduplicate ON logs_raw (isduplicate)")
    # print("e")
    # c.execute("DROP INDEX idx_messages_flagged")
    c.execute("CREATE INDEX IF NOT EXISTS idx_messages_flagged ON messages(sender) WHERE flagged = true AND trusted IS NOT false")
    c.execute("CREATE INDEX IF NOT EXISTS idx_messages_flaggedstuff ON messages (flagged)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_messages_time ON messages (time)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_messages_flaggedtrusted ON messages (trusted)")
    # print("veee")

    c.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    c.execute("CREATE INDEX IF NOT EXISTS idx_usernames_name_trgm ON usernames USING GIN (name gin_trgm_ops)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_usernames_steamid ON usernames (steamid)")
    conn.commit()
    pgpool.putconn(conn)
if "messages" not in tables:
    init()
# init()