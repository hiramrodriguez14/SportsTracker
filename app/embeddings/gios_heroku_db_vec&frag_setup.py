import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Make sure your .env file or Heroku config vars are set.")

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
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
            SELECT 1 FROM information_schema.tables WHERE table_name = %s
        );
    """, (table_name,))
    return cur.fetchone()[0]

def create_tables():
    tables = {
        "docs": """
            CREATE TABLE IF NOT EXISTS docs (
                did SERIAL PRIMARY KEY,
                docname VARCHAR(255)
            );
        """,
        "fragments": """
            CREATE TABLE IF NOT EXISTS fragments (
                fid SERIAL PRIMARY KEY,
                did INTEGER REFERENCES docs(did) ON DELETE CASCADE,
                content TEXT NOT NULL,
                embedding VECTOR(768)
            );
        """,
        "exercise_embeddings": """
            CREATE TABLE IF NOT EXISTS exercise_embeddings (
                id SERIAL PRIMARY KEY,
                chunk_text TEXT,
                embedding VECTOR(768)
            );
        """
    }

    for name, sql in tables.items():
        if not table_exists(name):
            cur.execute(sql)
            print(f"Created table '{name}'.")
        else:
            print(f"Table '{name}' already exists. Skipping.")
    conn.commit()

try:
    ensure_vector_extension()
    create_tables()
    print("Heroku vector tables are ready.")
except Exception as e:
    print(f"ERROR during setup: {e}")
finally:
    cur.close()
    conn.close()
