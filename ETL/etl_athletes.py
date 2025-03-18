import psycopg2
import sqlite3
import os
import getpass

DB_NAME = "sportsdb"
DB_USER = "postgres"
DB_HOST = "localhost"

DB_PORT = input("Enter your PostgreSQL port (Default is 5432): ")
DB_PASSWORD = getpass.getpass("Enter your PostgreSQL password: ")
if not DB_PORT:
    DB_PORT = input("Enter your PostgreSQL port (Default is 5432): ")
    os.environ["DB_PORT"] = DB_PORT

if not DB_PASSWORD:
    DB_PASSWORD = getpass.getpass("Enter your PostgreSQL password: ")
    os.environ["DB_PASSWORD"] = DB_PASSWORD

def load_athletes():
    conn_pg = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn_sqlite = sqlite3.connect("data/athletes.db")
    cur_pg = conn_pg.cursor()
    cur_sqlite = conn_sqlite.cursor()
    
    cur_sqlite.execute("SELECT id, name, age, gender, height, weight FROM athletes")
    rows = cur_sqlite.fetchall()
    
    for row in rows:
        if any(v is None or v == "" for v in row):
            continue
        cur_pg.execute(
            "INSERT INTO athletes (id, name, age, gender, height, weight) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            row
        )

    conn_pg.commit()
    cur_pg.close()
    conn_pg.close()
    cur_sqlite.close()
    conn_sqlite.close()

if __name__ == "__main__":
    load_athletes()
