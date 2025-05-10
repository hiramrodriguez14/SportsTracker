import os
import json
from sentence_transformers import SentenceTransformer
from app.model.dao.fragmentsDAO import FragmentDAO
from app.model.dao.docsDAO import DocumentDAO
from bug_handling.choose_db import get_db_config
import re
from textwrap import wrap

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)   
    return text.strip()

def chunk_text(text, max_chars=500):
    return wrap(text, max_chars)
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
            
            did = document.insertDocument(docname, content)
            
            content = clean_text(content)
            chunks = chunk_text(content)
            
            for chunk in chunks:
                  embedding = model.encode(chunk)
                  fragment.insertFragment(did, chunk, embedding.tolist())

    print("Fragments inserted successfully!")

if __name__ == "__main__":
    load_fragments()
