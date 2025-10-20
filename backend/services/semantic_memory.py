import os
import json
from typing import List, Tuple, Optional

INDEX_DIR = os.path.join("uploads", "indexes")
os.makedirs(INDEX_DIR, exist_ok=True)

_model = None
_index_cache = {}
_meta_cache = {}


def _embedder():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            # Small, fast model; you can switch via env SENTENCE_MODEL
            model_name = os.getenv("SENTENCE_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            _model = SentenceTransformer(model_name)
        except Exception:
            return None
    return _model


def _index_paths(user_id: int) -> Tuple[str, str]:
    faiss_path = os.path.join(INDEX_DIR, f"user_{user_id}.faiss")
    meta_path = os.path.join(INDEX_DIR, f"user_{user_id}.meta.json")
    return faiss_path, meta_path


def _load_index(user_id: int):
    try:
        import faiss  # type: ignore
    except Exception:
        return None, None
    if user_id in _index_cache and user_id in _meta_cache:
        return _index_cache[user_id], _meta_cache[user_id]
    faiss_path, meta_path = _index_paths(user_id)
    if os.path.exists(faiss_path) and os.path.exists(meta_path):
        index = faiss.read_index(faiss_path)
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        _index_cache[user_id] = index
        _meta_cache[user_id] = meta
        return index, meta
    return None, None


def _save_index(user_id: int, index, meta: dict):
    try:
        import faiss  # type: ignore
    except Exception:
        return
    faiss_path, meta_path = _index_paths(user_id)
    faiss.write_index(index, faiss_path)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False)
    _index_cache[user_id] = index
    _meta_cache[user_id] = meta


def _split_text(text: str, chunk_size: int = 600, overlap: int = 80) -> List[str]:
    text = (text or "").strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
        if start >= len(text):
            break
    return [c.strip() for c in chunks if c.strip()]


def build_or_update_user_index(user_id: int, fetch_document_callable) -> int:
    """
    Build or update FAISS index for user's documents.
    fetch_document_callable: function (doc_id: int, user_id: int) -> dict with 'content'
    Returns number of chunks indexed.
    """
    try:
        import faiss  # type: ignore
    except Exception:
        return 0

    # Fetch user documents
    from backend.models.document_model import get_user_documents
    docs = get_user_documents(user_id)

    texts = []
    sources = []
    for d in docs:
        try:
            full = fetch_document_callable(d["id"], user_id)
            content = (full or {}).get("content") or ""
            for ch in _split_text(content):
                texts.append(ch)
                sources.append({"document_id": d["id"], "filename": d.get("filename")})
        except Exception:
            continue

    if not texts:
        return 0

    emb = _embedder()
    vecs = emb.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    dim = vecs.shape[1]

    index, meta = _load_index(user_id)
    if index is None:
        index = faiss.IndexFlatIP(dim)
        meta = {"chunks": []}

    # Add vectors
    try:
        import numpy as np  # type: ignore
        index.add(vecs.astype(np.float32))
    except Exception:
        return 0
    for s in sources:
        meta["chunks"].append(s)

    _save_index(user_id, index, meta)
    return len(texts)


def retrieve_context(user_id: int, query: str, k: int = 5) -> List[str]:
    try:
        import faiss  # type: ignore
    except Exception:
        return []
    index, meta = _load_index(user_id)
    if index is None:
        return []
    emb = _embedder()
    if emb is None:
        return []
    try:
        import numpy as np  # type: ignore
        q = emb.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
    except Exception:
        return []
    D, I = index.search(q, k)
    # This simple implementation does not store chunk texts, only metadata; we will return placeholders.
    # For better quality, you can also persist chunk texts. Here we re-hydrate by fetching documents and slicing again.
    contexts: List[str] = []
    try:
        from backend.models.document_model import get_document_by_id
        for idx in I[0]:
            if idx < 0 or idx >= len(meta.get("chunks", [])):
                continue
            doc_id = meta["chunks"][idx]["document_id"]
            doc = get_document_by_id(doc_id, user_id)
            if not doc:
                continue
            content = (doc.get("content") or "")
            if content:
                contexts.append(content[:1000])
    except Exception:
        pass
    return contexts[:k]
