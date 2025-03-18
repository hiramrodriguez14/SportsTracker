import psycopg2
import json
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

def load_exercise_primary_muscles():
    conn = connect_db()
    cur = conn.cursor()

    with open("data/exercise_primary_muscles.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for row in data:
        exercise_id = int(row["exercise_id"])
        if any(v is None or v == "" for v in row.values()) or not check_foreign_key(conn, "exercises", "id", exercise_id):
            continue

        cur.execute(
            "INSERT INTO exercise_primary_muscles (exercise_id, muscle) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (exercise_id, row["muscle"])
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_exercise_primary_muscles()
