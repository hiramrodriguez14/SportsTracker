import psycopg2
import sqlite3
import os
import getpass

DB_NAME = "sportsdb"
DB_USER = "postgres"
DB_HOST = "localhost"

DB_PORT = os.getenv("DB_PORT")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PORT:
    DB_PORT = input("Enter your PostgreSQL port (Default is 5432): ")
    os.environ["DB_PORT"] = DB_PORT

if not DB_PASSWORD:
    DB_PASSWORD = getpass.getpass("Enter your PostgreSQL password: ")
    os.environ["DB_PASSWORD"] = DB_PASSWORD

def check_foreign_key(conn, table, column, value):
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM {table} WHERE {column} = %s", (value,))
    exists = cur.fetchone()
    cur.close()
    return exists

def load_championships():
    conn_pg = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn_sqlite = sqlite3.connect("data/championships.db")
    cur_pg = conn_pg.cursor()
    cur_sqlite = conn_sqlite.cursor()
    
    cur_sqlite.execute("SELECT id, name, winner_team, winner_year FROM championships")
    rows = cur_sqlite.fetchall()
    
    for row in rows:
        winner_team = int(row[2])
        if any(v is None or v == "" for v in row) or not check_foreign_key(conn_pg, "teams", "id", winner_team):
            continue
        cur_pg.execute(
            "INSERT INTO championships (id, name, winner_team, winner_year) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
            row
        )

    conn_pg.commit()
    cur_pg.close()
    conn_pg.close()
    cur_sqlite.close()
    conn_sqlite.close()

if __name__ == "__main__":
    load_championships()
