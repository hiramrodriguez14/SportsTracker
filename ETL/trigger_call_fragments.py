import os
import psycopg2
import subprocess
from bug_handling.choose_db import get_db_config

ETL_SCRIPT = "ETL/etl_fragments.py"
TARGET_TABLE = "fragments"

def table_exists(table_name):
    try:
        conn = psycopg2.connect(get_db_config().connection_url)
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table_name,))
            exists = cursor.fetchone()[0]
        conn.close()
        return exists
    except Exception as e:
        print(f"[ERROR] Failed to check table '{table_name}': {e}")
        return False

def run_etl_if_needed():
    if table_exists(TARGET_TABLE):
        print(f"Table '{TARGET_TABLE}' already exists. Skipping fragment ETL.")
        return

    if not os.path.exists(ETL_SCRIPT):
        print(f"{ETL_SCRIPT} not found. Aborting.")
        return

    print(f"Running {ETL_SCRIPT}...")
    try:
        subprocess.run(["python", ETL_SCRIPT], check=True)
        print("Fragment ETL completed successfully!\n")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Fragment ETL failed: {e}")

if __name__ == "__main__":
    run_etl_if_needed()
