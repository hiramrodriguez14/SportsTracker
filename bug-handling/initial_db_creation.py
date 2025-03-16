import psycopg2
import getpass
import sys
import os

DB_NAME = "sportsdb"
DB_USER = "postgres"
DB_HOST = "localhost"

DB_PORT = os.getenv("DB_PORT")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PORT:
    DB_PORT = input("Enter your PostgreSQL port (Default is 5432): ")
    os.environ["DB_PORT"] = DB_PORT

if not DB_PASSWORD:
    DB_PASSWORD = getpass.getpass("Enter your PostgreSQL password: ")
    os.environ["DB_PASSWORD"] = DB_PASSWORD
    
def get_postgres_credentials():
    attempts = 3
    while attempts > 0:
        password = getpass.getpass("Enter your PostgreSQL password: ")
        port = input("Enter your PostgreSQL port (Default is 5432): ") or "5432"

        try:
            conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=password, host=DB_HOST, port=port)
            conn.close()
            return password, port
        except psycopg2.OperationalError:
            print(f"Wrong password or incorrect port. Attempts left: {attempts - 1}")
            attempts -= 1

    print("Too many failed attempts. Exiting.")
    sys.exit(1)

def database_exists():
    conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone()
    cur.close()
    conn.close()
    return exists is not None

def create_database():
    if database_exists():
        return "Database already exists. Skipping creation."

    conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER}")
    cur.close()
    conn.close()
    return "Database created successfully."

def table_exists(conn, table_name):
    cur = conn.cursor()
    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
    exists = cur.fetchone()[0]
    cur.close()
    return exists

def create_tables():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    results = []

    tables = {
        "sports": """
            CREATE TABLE sports (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                gender CHAR(1),
                venue VARCHAR(50)
            )
        """,
        "exercises": """
            CREATE TABLE exercises (
                id SERIAL PRIMARY KEY,
                alter_id VARCHAR(50),
                name VARCHAR(255) NOT NULL,
                force VARCHAR(50),
                level VARCHAR(50),
                mechanic VARCHAR(50),
                equipment VARCHAR(50),
                category VARCHAR(50)
            )
        """,
        "athletes": """
            CREATE TABLE athletes (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT,
                gender CHAR(1),
                height DECIMAL(5,2),
                weight DECIMAL(5,2)
            )
        """,
        "teams": """
            CREATE TABLE teams (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                sport_id INT REFERENCES sports(id) ON DELETE CASCADE
            )
        """,
        "championships": """
            CREATE TABLE championships (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                winner_team INT REFERENCES teams(id) ON DELETE CASCADE,
                winner_year INT
            )
        """,
        "practices": """
            CREATE TABLE practices (
                fk_team INT REFERENCES teams(id) ON DELETE CASCADE,
                fk_athlete INT REFERENCES athletes(id) ON DELETE CASCADE,
                season VARCHAR(50),
                PRIMARY KEY (fk_team, fk_athlete)
            )
        """,
        "exercise_instructions": """
            CREATE TABLE exercise_instructions (
                id SERIAL PRIMARY KEY,
                exercise_id INT REFERENCES exercises(id) ON DELETE CASCADE,
                instruction_number INT,
                instruction TEXT NOT NULL
            )
        """,
        "exercise_primary_muscles": """
            CREATE TABLE exercise_primary_muscles (
                id SERIAL PRIMARY KEY,
                exercise_id INT REFERENCES exercises(id) ON DELETE CASCADE,
                muscle VARCHAR(255) NOT NULL
            )
        """,
        "exercise_secondary_muscles": """
            CREATE TABLE exercise_secondary_muscles (
                id SERIAL PRIMARY KEY,
                exercise_id INT REFERENCES exercises(id) ON DELETE CASCADE,
                muscle VARCHAR(255) NOT NULL
            )
        """,
        "exercise_images": """
            CREATE TABLE exercise_images (
                id SERIAL PRIMARY KEY,
                exercise_id INT REFERENCES exercises(id) ON DELETE CASCADE,
                image_path VARCHAR(255)
            )
        """,
        "sport_exercises": """
            CREATE TABLE sport_exercises (
                sport_id INT REFERENCES sports(id) ON DELETE CASCADE,
                exercise_id INT REFERENCES exercises(id) ON DELETE CASCADE,
                PRIMARY KEY (sport_id, exercise_id)
            )
        """
    }

    for table, sql in tables.items():
        if table_exists(conn, table):
            results.append(f"Table '{table}' already exists. Skipping creation.")
        else:
            cur.execute(sql)
            results.append(f"Table '{table}' created successfully.")

    conn.commit()
    cur.close()
    conn.close()
    return results

db_result = create_database()
table_results = create_tables()

print("\n".join([db_result] + table_results))
