import psycopg2

# DB_NAME = "usgulalc"
# DB_USER = "usgulalc"
# DB_PASS = "k_vZX18f03Bs0gQSkabkxqvRBGJEHl_O"
# DB_HOST = "rogue.db.elephantsql.com"
# DB_PORT = "5432"
from psycopg2 import extensions

DB_NAME = "SteamParser"
DB_USER = "postgres"
DB_PASS = "123"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
conn = psycopg2.connect(database=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST, port=DB_PORT)

# read_committed = extensions.ISOLATION_LEVEL_READ_COMMITTED
# conn.set_isolation_level(read_committed)
cur = conn.cursor()
