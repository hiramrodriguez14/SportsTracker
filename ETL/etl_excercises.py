import psycopg2
import json
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

def load_exercises():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        with open("data/exercises.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for row in data:
            if any(v is None or v == "" for v in row.values()):
                continue

            cur.execute(
                "INSERT INTO exercises (alter_id, name, force, level, mechanic, equipment, category) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (row["alter_id"], row["name"], row["force"], row["level"], row["mechanic"], row["equipment"], row["category"])
            )

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error loading exercises: {e}")

if __name__ == "__main__":
    load_exercises()
