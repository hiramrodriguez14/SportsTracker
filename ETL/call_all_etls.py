import os
import subprocess
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ETL_FOLDER = "ETL"

# Mapping of ETL scripts to their target tables
ETL_SCRIPTS = {
    "etl_fragments.py": "fragments",
	"etl_sports.py": "sports",
    "etl_teams.py": "teams",
    "etl_exercises.py": "exercises",
    "etl_sports_with_exercises.py": "sport_exercises",
    "etl_championships.py": "championships",
    "etl_athletes.py": "athletes",
    "etl_practices.py": "practices",
    "etl_exercise_instructions.py": "exercise_instructions",
    "etl_exercise_primary_muscles.py": "exercise_primary_muscles",
    "etl_exercise_secondary_muscles.py": "exercise_secondary_muscles",
    "etl_exercise_images.py": "exercise_images"
}


def table_exists(table_name):
    try:
        result = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table_name,))
            exists = cur.fetchone()[0]
        conn.close()
        return exists
    except Exception as e:
        print(f"Failed to check table {table_name}: {e}")
        return False


def run_etl_script(script):
    script_path = os.path.join(ETL_FOLDER, script)

    if not os.path.exists(script_path):
        print(f"{script} not found. Skipping.")
        return

    print(f"Running {script}...")
    try:
        subprocess.run(["python", script_path], check=True)
        print(f"{script} completed successfully!\n")
    except subprocess.CalledProcessError as e:
        print(f"ETL failed for {script}: {e}\n")


def main():
    print("Starting ETL process...\n")

    for script, table in ETL_SCRIPTS.items():
        if table_exists(table):
            print(f"Table '{table}' already exists. Skipping {script}.\n")
        else:
            run_etl_script(script)

    print("All ETL scripts processed!\n")


if __name__ == "__main__":
    main()
