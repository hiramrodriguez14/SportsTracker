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
    DB_PORT = "5432"

if not DB_PASSWORD:
    print("Error: Password is required.")
    exit(1)

def check_foreign_key(conn, table, column, value):
    """Check if a foreign key exists in a table."""
    with conn.cursor() as cur:
        cur.execute(f"SELECT 1 FROM {table} WHERE {column} = %s", (value,))
        return cur.fetchone() is not None  # Return True if exists, False otherwise

def load_sports_with_exercises():
    """Load sports with exercises into the database."""
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

    with open("data/sports_with_exercises.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    with conn.cursor() as cur:
        for row in data:
            sport_id = row["id"]
            exercises = row["exercises"]  # This is a list
            
            for exercise_id in exercises:  # Loop through exercises list
                # Check if sport_id and exercise_id exist in their respective tables
                if not check_foreign_key(conn, "sports", "id", sport_id):
                    print(f"Skipping: Sport ID {sport_id} does not exist.")
                    continue
                if not check_foreign_key(conn, "exercises", "id", exercise_id):
                    print(f"Skipping: Exercise ID {exercise_id} does not exist.")
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