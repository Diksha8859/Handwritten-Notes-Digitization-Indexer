# utils.py
import re
import json
from typing import List
from pathlib import Path

def clean_text(raw: str) -> str:
    # Basic cleaning for OCRed handwritten text
    if not raw:
        return ""
    s = raw.replace("\r", " ").replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # optional: more normalization
    return s

def save_metadata(metadata: List[dict], path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

def load_metadata(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
