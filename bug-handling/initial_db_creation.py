import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def table_exists(conn, table_name):
    cur = conn.cursor()
    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
    exists = cur.fetchone()[0]
    cur.close()
    return exists

def create_tables():
    conn = psycopg2.connect(DATABASE_URL)
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

table_results = create_tables()
print("\n".join(table_results))
