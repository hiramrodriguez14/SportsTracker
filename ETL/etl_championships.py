import psycopg2
import sqlite3
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def check_foreign_key(conn, table, column, value):
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM {table} WHERE {column} = %s", (value,))
    exists = cur.fetchone()
    cur.close()
    return exists

def load_championships():
    conn_pg = connect_db()
    conn_sqlite = sqlite3.connect("data/championships.db")
    
    cur_pg = conn_pg.cursor()
    cur_sqlite = conn_sqlite.cursor()
    
    cur_sqlite.execute("SELECT id, name, winner_team, winner_year FROM championships")
    rows = cur_sqlite.fetchall()
    
    for row in rows:
        winner_team = int(row[2])
        
        # ✅ Corrected the any() function
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
