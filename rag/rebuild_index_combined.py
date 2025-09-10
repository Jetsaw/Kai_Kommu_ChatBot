import os
import json
import pickle
from typing import List

import numpy as np
import faiss

from fastembed import TextEmbedding  
from config import FAISS_DIR, SOP_JSON_PATH

MODEL_NAME = "intfloat/multilingual-e5-base"


def _normalize(v: np.ndarray) -> np.ndarray:
    """L2-normalize row-wise for cosine similarity with FAISS IndexFlatIP."""
    n = np.linalg.norm(v, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return v / n


def _embed_texts(texts: List[str], model_name: str = MODEL_NAME) -> np.ndarray:
    """Embed a list of texts with FastEmbed and return float32, L2-normalized."""
    if not texts:
        return np.zeros((0, 384), dtype="float32")

    embedder = TextEmbedding(model_name=model_name)
   
    rows = list(embedder.embed(texts))
    X = np.vstack(rows).astype("float32")

    # L2-normalize to use cosine sim with IndexFlatIP
    X = _normalize(X)
    return X


def rebuild():
    os.makedirs(FAISS_DIR, exist_ok=True)

    # Load SOP JSON
    try:
        with open(SOP_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise SystemExit(f"[ingest] Cannot read {SOP_JSON_PATH}: {e}")

    # Keep your original entry structure
    entries = [
        {"question": d["question"], "answer": d["answer"], "source": "SOP"}
        for d in data
        if d.get("question") and d.get("answer")
    ]
    if not entries:
        raise SystemExit("[ingest] No SOP entries to index.")

    # Same corpus construction as yours
    corpus = [f"Q: {e['question']}\nA: {e['answer']}" for e in entries]

    print(f"[ingest] Embedding {len(corpus)} entries with {MODEL_NAME} (FastEmbed)...")
    embs = _embed_texts(corpus, model_name=MODEL_NAME)  # float32, normalized
    dim = embs.shape[1] if embs.size else 384  # default fallback

    # Cosine similarity using Inner Product on normalized vectors
    index = faiss.IndexFlatIP(dim)
    if embs.size:
        index.add(embs)

    # Persist FAISS + metadata (keeps your original filenames)
    faiss.write_index(index, os.path.join(FAISS_DIR, "index.faiss"))
    with open(os.path.join(FAISS_DIR, "index.pkl"), "wb") as f:
        pickle.dump({"data": entries, "model": MODEL_NAME}, f)

    print(f"[ingest] Indexed {len(entries)} items → {FAISS_DIR}")


if __name__ == "__main__":
    rebuild()
    