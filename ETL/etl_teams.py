import psycopg2
import pandas as pd
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def check_foreign_key(conn, table, column, value):
    with conn.cursor() as cur:
        cur.execute(f"SELECT 1 FROM {table} WHERE {column} = %s", (value,))
        return cur.fetchone() is not None

def load_teams():
    try:
        conn = connect_db()
        df = pd.read_csv("data/teams_.csv").dropna()

        with conn.cursor() as cur:
            for _, row in df.iterrows():
                sport_id = int(row["sport"])
                if not check_foreign_key(conn, "sports", "id", sport_id):
                    continue

                cur.execute(
                    "INSERT INTO teams (id, name, sport) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (row["id"], row["name"], sport_id)
                )
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error loading teams: {e}")

if __name__ == "__main__":
    load_teams()
