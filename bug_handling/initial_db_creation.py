import os
import psycopg2
import urllib.parse as urlparse

url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    dbname=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()

def table_exists(table_name):
    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
    return cur.fetchone()[0]

def create_tables():
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
                alter_id VARCHAR,
                name VARCHAR NOT NULL,
                force VARCHAR,
                level VARCHAR,
                mechanic VARCHAR,
                equipment VARCHAR,
                category VARCHAR
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
                sport INT REFERENCES sports(id) ON DELETE CASCADE
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
                sport INT REFERENCES sports(id) ON DELETE CASCADE,
                exercise INT REFERENCES exercises(id) ON DELETE CASCADE,
                PRIMARY KEY (sport, exercise)
            )
        """,
        "users": """
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(100) NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                memory TEXT NOT NULL
            )
        """,
        "docs": """
            CREATE TABLE docs (
                did SERIAL PRIMARY KEY,
                docname VARCHAR(255),
                content TEXT
            );
        """,
        "fragments": """
            CREATE TABLE fragments (
                fid SERIAL PRIMARY KEY,
                did INTEGER REFERENCES docs(did) ON DELETE CASCADE,
                content TEXT NOT NULL,
                embedding VECTOR(768)
            )
        """,
    }

    results = []
    for table, sql in tables.items():
        if table_exists(table):
            results.append(f"Table '{table}' already exists. Skipping creation.")
        else:
            cur.execute(sql)
            results.append(f"Table '{table}' created successfully.")

    conn.commit()
    return results

try:
    table_results = create_tables()
    print("\n".join(table_results))
    print("Database setup complete!")
except Exception as e:
    print(f"ERROR: Failed to create tables: {e}")
finally:
    cur.close()
    conn.close()
