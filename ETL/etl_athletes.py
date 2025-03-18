import psycopg2
import sqlite3
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def load_athletes():
    conn_pg = connect_db()
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
