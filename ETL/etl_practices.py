import psycopg2
import pandas as pd
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

def load_practices():
    conn = connect_db()
    df = pd.read_csv("data/practices.csv").dropna()
    cur = conn.cursor()

    for _, row in df.iterrows():
        fk_team = int(row["fk_team"])
        fk_athlete = int(row["fk_athlete"])
        if not check_foreign_key(conn, "teams", "id", fk_team) or not check_foreign_key(conn, "athletes", "id", fk_athlete):
            continue

        cur.execute(
            "INSERT INTO practices (fk_team, fk_athlete, season) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            (fk_team, fk_athlete, row["season"])
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_practices()
