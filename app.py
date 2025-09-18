# app.py
import os
import faiss
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np

INDEX_PATH = os.getenv("INDEX_PATH", "models/faiss.index")
METADATA_PATH = os.getenv("METADATA_PATH", "models/metadata.json")
MODEL_NAME = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")

app = FastAPI(title="Handwritten Notes Search API")
model = SentenceTransformer(MODEL_NAME)

def load_index(index_path=INDEX_PATH):
    if not Path(index_path).exists():
        raise FileNotFoundError("FAISS index not found.")
    idx = faiss.read_index(index_path)
    return idx

def load_metadata(meta_path=METADATA_PATH):
    with open(meta_path, "r", encoding="utf-8") as f:
        return json.load(f)

index = load_index()
metadata = load_metadata()

class SearchResult(BaseModel):
    score: float
    file: str
    text: str

@app.get("/search", response_model=list[SearchResult])
def search(q: str = Query(..., min_length=1), k: int = 5):
    # embed query, search FAISS
    q_emb = model.encode([q], convert_to_numpy=True)
    D, I = index.search(q_emb, k)
    results = []
    for score, idx in zip(D[0], I[0]):
        if idx == -1:
            continue
        meta = metadata[idx]
        results.append(SearchResult(score=float(score), file=meta["file"], text=meta["text"]))
    return results

@app.get("/health")
def health():
    return {"status": "ok"}
