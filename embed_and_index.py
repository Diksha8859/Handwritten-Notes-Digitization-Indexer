# embed_and_index.py
import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from utils import save_metadata

MODEL_NAME = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")
INDEX_PATH = os.getenv("INDEX_PATH", "models/faiss.index")
METADATA_PATH = os.getenv("METADATA_PATH", "models/metadata.json")

def build_index(extracted_json: str, index_path=INDEX_PATH, metadata_path=METADATA_PATH):
    with open(extracted_json, "r", encoding="utf-8") as f:
        items = json.load(f)

    # flatten into documents (one doc per file; optionally split into chunks)
    docs = []
    for it in items:
        text = it.get("text", "")
        if not text:
            continue
        docs.append({"text": text, "file": it.get("file")})

    model = SentenceTransformer(MODEL_NAME)
    texts = [d["text"] for d in docs]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    Path(index_path).parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, index_path)

    # Save metadata in same order as vectors
    metadata = [{"id": i, "file": docs[i]["file"], "text": docs[i]["text"]} for i in range(len(docs))]
    save_metadata(metadata, metadata_path)
    print(f"Saved index -> {index_path} and metadata -> {metadata_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--extracted", default="models/extracted.json")
    parser.add_argument("--index", default="models/faiss.index")
    parser.add_argument("--meta", default="models/metadata.json")
    args = parser.parse_args()
    build_index(args.extracted, args.index, args.meta)
