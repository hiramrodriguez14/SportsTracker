import psycopg2
import json
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def load_sports():
    try:
        conn = connect_db()
        cur = conn.cursor()

        with open("data/sports_with_exercises.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for row in data:
            if any(v is None or v == "" for v in row.values()):
                continue

            cur.execute(
                "INSERT INTO sports (id, name, gender, venue) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (row["id"], row["name"], row["gender"], row["venue"])
            )

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error loading sports: {e}")

if __name__ == "__main__":
    load_sports()
