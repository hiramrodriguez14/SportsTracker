import os
import subprocess
import getpass

DB_PORT = os.getenv("DB_PORT")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PORT:
    DB_PORT = input("Enter your PostgreSQL port (Default is 5432): ")
    os.environ["DB_PORT"] = DB_PORT

if not DB_PASSWORD:
    DB_PASSWORD = getpass.getpass("Enter your PostgreSQL password: ")
    os.environ["DB_PASSWORD"] = DB_PASSWORD


ETL_FOLDER = r"C:\Users\proli\source\repos\db-try2\ETL" 

ETL_SCRIPTS = [
    "etl_exercises.py",
    "etl_teams.py",
    "etl_athletes.py",
    "etl_exercise_primary_muscles.py",
    "etl_exercise_secondary_muscles.py",
    "etl_exercise_instructions.py",
    "etl_exercise_images.py",
    "etl_sports_with_exercises.py",
    "etl_championships.py",
    "etl_practices.py"
]

def run_etl_script(script):
    script_path = os.path.join(ETL_FOLDER, script)
    
    if not os.path.exists(script_path):
        print(f"❌ {script} not found. Skipping.")
        return

    print(f"🚀 Running {script}...")
    try:
        subprocess.run(
            ["python", script_path, DB_PASSWORD, DB_PORT],  # ✅ Pass DB credentials once
            check=True
        )
        print(f"✅ {script} completed successfully!\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Data injection failed for {script}: {e}\n")

def main():
    print("🔄 Starting ETL process...\n")
    
    for script in ETL_SCRIPTS:
        run_etl_script(script)

    print("🎯 All ETL scripts executed!\n")

if __name__ == "__main__":
    main()
