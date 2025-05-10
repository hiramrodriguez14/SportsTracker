import json

def load_and_chunk_documents(file_path, chunk_size=250):
    chunks = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            doc = json.loads(line)
            text = doc.get("content", "")
            words = text.split()
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i:i + chunk_size])
                if chunk.strip():
                    chunks.append(chunk)
    return chunks

chunks = load_and_chunk_documents("app/embeddings/exercise_documents.jsonl")

with open("app/embeddings/processed_chunks.txt", "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(chunk.strip() + "\n")

print(f"Saved {len(chunks)} chunks to app/embeddings/processed_chunks.txt")
