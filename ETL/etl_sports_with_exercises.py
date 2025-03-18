import psycopg2
import json
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def check_foreign_key(conn, table, column, value):
    with conn.cursor() as cur:
        cur.execute(f"SELECT 1 FROM {table} WHERE {column} = %s", (value,))
        return cur.fetchone() is not None

def load_sports_with_exercises():
    conn = connect_db()
    
    with open("data/sports_with_exercises.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    with conn.cursor() as cur:
        for row in data:
            sport_id = row["id"]
            exercises = row["exercises"]
            
            for exercise_id in exercises:
                if not check_foreign_key(conn, "sports", "id", sport_id):
                    continue
                if not check_foreign_key(conn, "exercises", "id", exercise_id):
                    continue

                cur.execute(
                    "INSERT INTO sport_exercises (sport, exercise) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (sport_id, exercise_id)
                )
    
    conn.commit()
    conn.close()
    print("Data inserted successfully!")

if __name__ == "__main__":
    load_sports_with_exercises()