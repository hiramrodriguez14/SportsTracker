import psycopg2
import json
import os
import getpass

DB_NAME = "sportsdb"
DB_USER = "postgres"
DB_HOST = "localhost"

DB_PORT = input("Enter your PostgreSQL port (Default is 5432): ") or "5432"
DB_PASSWORD = getpass.getpass("Enter your PostgreSQL password: ")

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

def load_exercise_instructions():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        print("Loading JSON file...")
        with open("data/exercise_instructions.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        print(" File loaded successfully!")

        for row in data:
            exercise = int(row["exercise_id"])
            
            if any(v is None or v == "" for v in row.values()) or not check_foreign_key(conn, "exercises", "id", exercise):
                print(f"Skipping row: {row}")
                continue

            cur.execute(
                "INSERT INTO exercise_instructions (id, exercise_id, instruction_number, instruction) "
                "VALUES (%s, %s, %s, %s) "
                "ON CONFLICT (id) DO UPDATE SET instruction = EXCLUDED.instruction",
                (row["id"], exercise, row["instruction_number"], row["instruction"])
            )

        conn.commit()
        print(" Data Inserted Successfully!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error loading exercise instructions: {e}")

if __name__ == "__main__":
    load_exercise_instructions()
