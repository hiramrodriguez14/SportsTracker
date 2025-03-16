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

def check_foreign_key(conn, table, column, value):
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM {table} WHERE {column} = %s", (value,))
    exists = cur.fetchone()
    cur.close()
    return exists

def load_exercise_images():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    with open("data/exercise_images.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for row in data:
        exercise_id = int(row["exercise_id"])
        if any(v is None or v == "" for v in row.values()) or not check_foreign_key(conn, "exercises", "id", exercise_id):
            continue

        cur.execute(
            "INSERT INTO exercise_images (exercise_id, image_path) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (exercise_id, row["image_path"])
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_exercise_images()
