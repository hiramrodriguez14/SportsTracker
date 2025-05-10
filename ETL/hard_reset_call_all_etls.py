import os
import subprocess

DATABASE_URL = os.getenv("DATABASE_URL")

ETL_FOLDER = r"ETL"

ETL_SCRIPTS = [
    "etl_sports.py",
    "etl_teams.py",
    "etl_exercises.py",
    "etl_sports_with_exercises.py",
    "etl_championships.py",
    "etl_athletes.py",
    "etl_practices.py",
    "etl_exercise_instructions.py",
    "etl_exercise_primary_muscles.py",
    "etl_exercise_secondary_muscles.py",
    "etl_exercise_images.py",
    "etl_fragments.py"
]

def run_etl_script(script):
    script_path = os.path.join(ETL_FOLDER, script)
    
    if not os.path.exists(script_path):
        print(f" {script} not found. Skipping.")
        return

    print(f" Running {script}...")
    try:
        subprocess.run(
            ["python", script_path], 
            check=True
        )
        print(f" {script} completed successfully!\n")
    except subprocess.CalledProcessError as e:
        print(f" Data injection failed for {script}: {e}\n")

def main():
    print(" Starting ETL process...\n")
    
    for script in ETL_SCRIPTS:
        run_etl_script(script)

    print(" All ETL scripts executed!\n")

if __name__ == "__main__":
    main()
