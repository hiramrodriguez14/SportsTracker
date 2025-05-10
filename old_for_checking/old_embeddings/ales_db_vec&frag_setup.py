# import psycopg2
# import os

# # Load DATABASE_URL from environment variables
# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError("ERROR: DATABASE_URL is not set. Make sure you are using Heroku's environment variables.")

# # Connect to the PostgreSQL database
# conn = psycopg2.connect(DATABASE_URL, sslmode="require")
# cur = conn.cursor()

import psycopg2

# Local DB connection settings
DB_NAME = 'sportsdb'
DB_USER = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_PASSWORD = 'Claudio0911'

# Connect to the local PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    host=DB_HOST,
    port=DB_PORT,
    password=DB_PASSWORD
)
cur = conn.cursor()

def ensure_vector_extension():
    try:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()
        print("Extension 'vector' is ready.")
    except Exception as e:
        print(f"ERROR creating 'vector' extension: {e}")
        raise

def table_exists(table_name):
    cur.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = %s
        );
    """, (table_name,))
    return cur.fetchone()[0]

def create_tables():
    tables = {
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
                did INTEGER REFERENCES docs(did),
                content TEXT,
                embedding VECTOR(768)
            );
        """
    }

    results = []
    for table, sql in tables.items():
        if table_exists(table):
            results.append(f"Table '{table}' already exists. Skipping.")
        else:
            cur.execute(sql)
            results.append(f"Table '{table}' created successfully.")

    conn.commit()
    return results

try:
    ensure_vector_extension()
    table_results = create_tables()
    print("\n".join(table_results))
    print(" Local database setup complete!")
except Exception as e:
    print(f" ERROR during setup: {e}")
finally:
    cur.close()
    conn.close()
