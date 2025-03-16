import psycopg2
import pandas as pd
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

def load_practices():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
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
