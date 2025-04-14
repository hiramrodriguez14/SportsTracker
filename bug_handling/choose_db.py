import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env if available
load_dotenv()

class DBConfig:
    def __init__(self):
        self.connection_url = None
        self._prompt_user()
        
    def _prompt_user(self):
        choice = os.getenv("DB_CHOICE", "1")  # Default to "1" if not set
        print("\n🔌 Choosing database to connect to:")
        print(f"Selected option from ENV: {choice}")

        if choice == "1":
            self.connection_url = self._local_db_url()
            print("✅ Connected to LOCAL PostgreSQL.")
        elif choice == "2":
            self.connection_url = self._heroku_db_url()
            print("✅ Connected to HEROKU PostgreSQL.")
        else:
            print("❌ Invalid input. Defaulting to LOCAL PostgreSQL.")
            self.connection_url = self._local_db_url()

    def _local_db_url(self):
        db_name = os.getenv('DB_NAME', 'sportsdb')
        db_user = os.getenv('DB_USER', 'postgres')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = input("Enter local PostgreSQL port [default 5432]: ").strip() or "5432"
        db_password = input("Enter local PostgreSQL password: ").strip()

        return f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"

    def _heroku_db_url(self):
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print("❌ DATABASE_URL not found in environment.")
            sys.exit(1)
        return db_url

# Singleton logic
_db_instance = None

def get_db_config():
    global _db_instance
    if _db_instance is None:
        _db_instance = DBConfig()
    return _db_instance
