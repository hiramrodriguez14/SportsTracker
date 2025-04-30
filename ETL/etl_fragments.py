import os
import json
from sentence_transformers import SentenceTransformer
from fragmentsDAO import FragmentDAO
from docsDAO import DocumentDAO
from bug_handling.choose_db import get_db_config

def load_fragments():
    fragment = FragmentDAO()
    document = DocumentDAO()
    model = SentenceTransformer("all-mpnet-base-v2")

    with open("data/exercise_documents.jsonl", "r", encoding="utf-8") as file:
        for line in file:
            obj = json.loads(line.strip())
            docname = obj.get("id", "")
            content = obj.get("text", "").strip()

            if not content:
                continue

            embedding = model.encode(content)
            did = document.insertDocument(docname)
            fragment.insertFragment(did, content, embedding.tolist())

    print("✅ Fragments inserted successfully!")

if __name__ == "__main__":
    load_fragments()
