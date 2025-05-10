import subprocess
import os

initial_db_script = os.path.join("bug_handling", "initial_db_creation.py")
etl_script = os.path.join("ETL", "call_all_etls.py")

print("Running initial_db_creation.py...")
initial_result = subprocess.run(["python", initial_db_script])
if initial_result.returncode != 0:
    print("Failed to run initial_db_creation.py")
    exit(1)
else:
    print("initial_db_creation.py completed successfully.")

print("Running call_all_etls.py...")
etl_result = subprocess.run(["python", etl_script])
if etl_result.returncode != 0:
    print("Failed to run call_all_etls.py")
    exit(1)
else:
    print("call_all_etls.py completed successfully.")
