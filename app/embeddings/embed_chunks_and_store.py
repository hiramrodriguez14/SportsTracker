import os
import psycopg2
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cursor = conn.cursor()

model = SentenceTransformer("all-mpnet-base-v2")

with open("app/embeddings/processed_chunks.txt", "r", encoding="utf-8") as f:
    chunks = [line.strip() for line in f.readlines() if line.strip()]

cursor.execute("SELECT did FROM docs WHERE docname = %s", ("Embedding Upload #1",))
doc = cursor.fetchone()
if not doc:
    cursor.execute("INSERT INTO docs (docname) VALUES (%s) RETURNING did", ("Embedding Upload #1",))
    did = cursor.fetchone()[0]
else:
    did = doc[0]

for chunk in chunks:
    embedding = model.encode(chunk).tolist()

    cursor.execute("""
        INSERT INTO exercise_embeddings (chunk_text, embedding)
        VALUES (%s, %s);
    """, (chunk, embedding))

    cursor.execute("""
        INSERT INTO fragments (did, content, embedding)
        VALUES (%s, %s, %s);
    """, (did, chunk, embedding))

conn.commit()
cursor.close()
conn.close()

print(f"Inserted {len(chunks)} chunks into both 'exercise_embeddings' and 'fragments'.")
