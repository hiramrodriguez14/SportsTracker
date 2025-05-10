import psycopg2
import os

# Connect to Heroku PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing!")

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
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = %s
        );
    """, (table_name,))
    return cur.fetchone()[0]

def create_embeddings_table():
    if table_exists("exercise_embeddings"):
        print("Table 'exercise_embeddings' already exists. Skipping creation.")
    else:
        cur.execute("""
            CREATE TABLE exercise_embeddings (
                id SERIAL PRIMARY KEY,
                chunk_text TEXT,
                embedding VECTOR(1536) -- important: match your model output dimension
            );
        """)
        conn.commit()
        print("Table 'exercise_embeddings' created successfully.")

try:
    ensure_vector_extension()
    create_embeddings_table()
    print("✅ Heroku database setup complete!")
except Exception as e:
    print(f"❌ ERROR during setup: {e}")
finally:
    cur.close()
    conn.close()
