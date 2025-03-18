import psycopg2
import json
import os
import getpass

DB_NAME = "sportsdb"
DB_USER = "postgres"
DB_HOST = "localhost"

DB_PORT = input("Enter your PostgreSQL port (Default is 5432): ")
DB_PASSWORD = getpass.getpass("Enter your PostgreSQL password: ")

if not DB_PORT:
    DB_PORT = input("Enter your PostgreSQL port (Default is 5432): ")
    os.environ["DB_PORT"] = DB_PORT

if not DB_PASSWORD:
    DB_PASSWORD = getpass.getpass("Enter your PostgreSQL password: ")
    os.environ["DB_PASSWORD"] = DB_PASSWORD

def load_sports():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
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
