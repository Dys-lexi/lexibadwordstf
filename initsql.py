from psycopg2 import pool

try:
    pgpool = pool.ThreadedConnectionPool(20, 200, dsn="postgresql://pguserm:hiddenpassword@postgres:3452/realdb")
except:
    pgpool = pool.ThreadedConnectionPool(20, 200, dsn="postgresql://pguserm:hiddenpassword@localhost:3449/realdb")

def init():
    print("init")
    conn = pgpool.getconn()

    c = conn.cursor()
    c.execute(
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
    # print("weee")
    c.execute(
        """CREATE TABLE IF NOT EXISTS currentthings (

            steamid BIGINT PRIMARY KEY,

            timestampcurrentname BIGINT,
            frame TEXT,
            avatar TEXT,
            currentname TEXT

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
    # print("teee")
    c.execute("CREATE INDEX IF NOT EXISTS idx_messages_id ON messages (id)")
    # print("a")
    c.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_id ON logs_raw (id)")
    # print("b")
    c.execute("ALTER TABLE currentthings ADD COLUMN IF NOT EXISTS vanity TEXT")
    # c.execute("UPDATE logs_raw SET isduplicate = NULL")
    # print("c")
    c.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_isduplicate ON logs_raw (isduplicate)")

    c.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_empty ON logs_raw (empty)")
    # print("d")
    c.execute("CREATE INDEX IF NOT EXISTS idx_logs_raw_isduplicate ON logs_raw (isduplicate)")
    # print("e")
    c.execute("CREATE INDEX IF NOT EXISTS idx_messages_flagged ON messages(sender) WHERE flagged = true;")
    # print("veee")

    c.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    c.execute("CREATE INDEX IF NOT EXISTS idx_usernames_name_trgm ON usernames USING GIN (name gin_trgm_ops)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_usernames_steamid ON usernames (steamid)")
    conn.commit()
    pgpool.putconn(conn)
init()
