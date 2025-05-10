import psycopg2
import os

# Local environment variables setup
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connect to local PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
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

def create_embeddings_table():
    if table_exists("exercise_embeddings"):
        print("Table 'exercise_embeddings' already exists. Skipping creation.")
    else:
        cur.execute("""
            CREATE TABLE exercise_embeddings (
                id SERIAL PRIMARY KEY,
                chunk_text TEXT,
                embedding VECTOR(1536)
            );
        """)
        conn.commit()
        print("Table 'exercise_embeddings' created successfully.")

try:
    ensure_vector_extension()
    create_embeddings_table()
    print("✅ Local database setup complete!")
except Exception as e:
    print(f"❌ ERROR during setup: {e}")
finally:
    cur.close()
    conn.close()
