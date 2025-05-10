import os
import sys
from dotenv import load_dotenv

load_dotenv()

class DBConfig:
    def __init__(self):
        self.connection_url = None
        self._prompt_user()
        
    def _prompt_user(self):
        choice = os.getenv("DB_CHOICE", "1")
        print("\nChoosing database to connect to:")
        print(f"Selected option from ENV: {choice}")

        if choice == "1":
            self.connection_url = self._local_db_url()
            print("Connected to LOCAL PostgreSQL.")
        elif choice == "2":
            self.connection_url = self._heroku_db_url()
            print("Connected to HEROKU PostgreSQL.")
        else:
            print("Invalid input. Defaulting to LOCAL PostgreSQL.")
            self.connection_url = self._local_db_url()

    def _local_db_url(self):
        db_name = os.getenv('DB_NAME', 'sportsdb')
        db_user = os.getenv('DB_USER', 'postgres')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_password = os.getenv('DB_PASSWORD', '0000')

        return f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"

    def _heroku_db_url(self):
        import urllib.parse as urlparse

        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print("DATABASE_URL not found in environment.")
            sys.exit(1)

        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(db_url)

        return f"dbname={url.path[1:]} user={url.username} password={url.password} host={url.hostname} port={url.port}"

_db_instance = None

def get_db_config():
    global _db_instance
    if _db_instance is None:
        _db_instance = DBConfig()
    return _db_instance
