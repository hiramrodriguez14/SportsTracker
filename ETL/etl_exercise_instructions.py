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

def load_exercise_instructions():
    try:
        conn = connect_db()
        cur = conn.cursor()

        print("Loading JSON file...")
        with open("data/exercise_instructions.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        print("File loaded successfully!")

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
