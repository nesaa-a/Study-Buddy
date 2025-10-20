# backend/services/summarizer.py
from transformers import pipeline
import re
import os
from collections import Counter

# Prefer the HF abstractive model unless explicitly disabled
# Allow explicit model selection via env
MODEL_NAME = os.getenv("SUMMARIZER_MODEL", "facebook/bart-large-cnn").strip()
USE_HF = os.getenv("USE_HF_SUMMARIZER", "1") == "1"
summarizer = None

def _get_summarizer():
    global summarizer
    if summarizer is None:
        # If user asks for DistilBERT, we don't use abstractive generation; fall back to extractive.
        if MODEL_NAME.lower() == "distilbert" or not USE_HF:
            return None

        model_id = MODEL_NAME or "facebook/bart-large-cnn"
        summarizer = pipeline("summarization", model=model_id)
        try:
            if hasattr(summarizer, "tokenizer"):
                maxlen = getattr(summarizer.tokenizer, "model_max_length", None)
                if maxlen in (None, float("inf")):
                    # Heuristics for common models
                    if model_id.startswith("facebook/bart-large"):
                        summarizer.tokenizer.model_max_length = 1024
                    elif model_id.startswith("sshleifer/distilbart"):
                        summarizer.tokenizer.model_max_length = 1024
                    elif model_id.startswith("t5-"):
                        summarizer.tokenizer.model_max_length = 512
                    else:
                        summarizer.tokenizer.model_max_length = 1024
        except Exception:
            pass
    return summarizer


def _normalize_whitespace(s: str) -> str:
    # Collapse newlines and extra spaces to ensure a single paragraph
    return " ".join(s.split())


def _chunk_text(text: str, max_chars: int = 900, overlap_chars: int = 120):
    """Split text into roughly sentence-aligned chunks under max_chars.
    Uses a simple sentence regex to avoid cutting mid-sentence.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks = []
    current = []
    current_len = 0
    for sent in sentences:
        sent_len = len(sent) + 1  # account for space/join
        if current_len + sent_len > max_chars and current:
            chunk_text = " ".join(current)
            chunks.append(chunk_text)
            # add small overlap for coherence
            tail = chunk_text[-overlap_chars:]
            current = [tail, sent]
            current_len = len(tail) + sent_len
        else:
            current.append(sent)
            current_len += sent_len
    if current:
        chunks.append(" ".join(current))
    return chunks if chunks else [text[:max_chars]]


def _clean_text(t: str) -> str:
    # Remove common artifacts: bullets, copyright lines, page numbers
    t = re.sub(r"[\u2022\u2023\u25CF\u25A0\u25E6\u2219\u25C6\u25C7\u2666\u25C8\u25AA\u25AB\u25FE\u25FD\u25CB\u274F\u25A1\u25B8\u25B9\u25AA\u25AB\u25BA\u25C4\u25B6\u25B2\u25BC\u2751\u2752\u25CF\u25CB\u25CC\u25D8\u25D9\u2023\u2043\u2219\u204C\u204D\u25E6\u223C\u2794\u27A4\u27A2\u29BF\u2024\u2027\u2219\u25AA\u25AB\u25CF\u25CB\u25C9\u25CE\u25C7\u25C6\u25C8\u25C9\u142F\u25CF\u25A0\u25CF\u25A1\u25A3\u25A4\u25A9\u25A6\u25A7\u25A8\u25A9\u25AA\u25AB\u25AC\u25AD\u25AE\u25AF\u25B0\u25B1\u25B2\u25B3\u25B4\u25B5\u25B6\u25B7\u25B8\u25B9\u25BA\u25BB\u25BC\u25BD\u25BE\u25BF\u25C0\u25C1\u25C2\u25C3]", " ", t)
    t = t.replace('❑', ' ').replace('▪', ' ').replace('©', ' ')
    # Remove copyright/footer like "2022 UBT 10"
    t = re.sub(r"\b\d{4}\b\s+UBT\b.*", " ", t, flags=re.IGNORECASE)
    # Remove standalone page numbers
    t = re.sub(r"\b\d+\b", lambda m: " " if len(m.group()) <= 3 else m.group(), t)
    # Collapse multiple spaces
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def _extractive_summary(text: str, target_sentences: int) -> str:
    text = _clean_text(text)
    # Split to sentences
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]
    # Filter noisy/too short/too long sentences
    filtered = []
    for s in sentences:
        wc = len(s.split())
        if 8 <= wc <= 40 and re.search(r"[A-Za-zÀ-ÿ]", s):
            filtered.append(s)
    if not filtered:
        filtered = sentences[:]
    # Deduplicate preserving order
    seen = set()
    dedup = []
    for s in filtered:
        key = s.lower()
        if key not in seen:
            seen.add(key)
            dedup.append(s)
    if len(dedup) <= target_sentences:
        return _normalize_whitespace(" ".join(dedup))

    # Build frequency table with English + Albanian common stopwords
    words = re.findall(r"[a-zA-ZÀ-ÿ0-9']+", " ".join(dedup).lower())
    stop = set([
        # English
        'the','is','in','at','of','a','and','to','for','on','with','as','by','an','be','are','it','that','this','from','or','was','were','have','has','had','you','we','they','he','she','i','your','our','their','not','but','if','then','so','also','can','will','may','might',
        # Albanian (basic subset)
        'dhe','një','është','në','me','si','të','për','ose','nga','kjo','ky','ajo','ai','ajo','janë','jemi','jam','ke','kam','ishte','ishin','do','mund','është','edhe','pasi','kur','që','ne','ju','ata','atyre','i','e','te','ti','ka','kaq','këtë','atë','këto','ato'
    ])
    freq = Counter(w for w in words if w not in stop)

    scores = []
    for i, s in enumerate(dedup):
        ws = re.findall(r"[a-zA-ZÀ-ÿ0-9']+", s.lower())
        score = sum(freq.get(w, 0) for w in ws) / (len(ws) + 1e-6)
        # Small boost for early sentences
        score += 0.05 * (1.0 / (i + 1))
        scores.append((score, i, s))

    top = sorted(scores, key=lambda x: (-x[0], x[1]))[:target_sentences]
    top_sorted = [s for _, _, s in sorted(top, key=lambda x: x[1])]
    return _normalize_whitespace(" ".join(top_sorted))


def generate_summary(text, length="medium"):
    if not text or text.strip() == "":
        return "No text available for summarization."

    # Clean source text first to improve model quality
    text = _clean_text(text)

    # Adjust target lengths (a bit longer for better coherence)
    if length == "short":
        max_len = 90
        min_len = 30
    elif length == "medium":
        max_len = 160
        min_len = 60
    else:
        max_len = 260
        min_len = 100

    # If DistilBERT is selected or HF disabled, use extractive summarization
    if MODEL_NAME.lower() == "distilbert" or not USE_HF:
        target = 3 if length == "short" else (5 if length == "medium" else 8)
        return _extractive_summary(text, target)

    chunks = _chunk_text(text, max_chars=900, overlap_chars=120)
    try:
        pipe = _get_summarizer()
        if pipe is None:
            # Safety net: if pipeline couldn't initialize, fall back to extractive
            target = 3 if length == "short" else (5 if length == "medium" else 8)
            return _extractive_summary(text, target)
        if len(chunks) == 1:
            result = pipe(
                chunks[0],
                max_length=max_len,
                min_length=min_len,
                do_sample=False,
                num_beams=4,
                truncation=True,
            )
            return _normalize_whitespace(result[0]["summary_text"])

        partial_summaries = []
        for ch in chunks:
            res = pipe(
                ch,
                max_length=min(max_len, 220),
                min_length=min_len,
                do_sample=False,
                num_beams=4,
                truncation=True,
            )
            partial_summaries.append(res[0]["summary_text"]) 

        combined = _normalize_whitespace(" ".join(partial_summaries))
        final = pipe(
            combined[:2000],
            max_length=max_len,
            min_length=min_len,
            do_sample=False,
            num_beams=4,
            truncation=True,
        )
        return _normalize_whitespace(final[0]["summary_text"])
    except Exception:
        target = 3 if length == "short" else (5 if length == "medium" else 8)
        return _extractive_summary(text, target)
