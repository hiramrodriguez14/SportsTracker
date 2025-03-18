import psycopg2
import json
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def load_exercises():
    try:
        conn = connect_db()
        cur = conn.cursor()

        with open("data/exercises.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for row in data:
            if any(v is None or v == "" for v in row.values()): 
                continue

            cur.execute(
                "INSERT INTO exercises (id, alter_id, name, force, level, mechanic, equipment, category) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (row["id"], row["alter_id"], row["name"], row["force"], row["level"], row["mechanic"], row["equipment"], row["category"])
            )

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error loading exercises: {e}")

if __name__ == "__main__":
    load_exercises()
