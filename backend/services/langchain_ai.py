import os
import json
from typing import List, Dict, Optional

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

def _load_chat_model():
    if not OPENAI_API_KEY:
        return None
    try:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=os.getenv("CHAT_MODEL", "gpt-3.5-turbo-0125"), temperature=0.2, api_key=OPENAI_API_KEY)
    except Exception:
        try:
            from langchain.chat_models import ChatOpenAI  # older langchain
            return ChatOpenAI(model_name=os.getenv("CHAT_MODEL", "gpt-3.5-turbo-0125"), temperature=0.2, openai_api_key=OPENAI_API_KEY)
        except Exception:
            return None


def get_chat_provider() -> str:
    """Return 'openai' if ChatOpenAI is available and key is set, else 'offline'."""
    try:
        llm = _load_chat_model()
        return "openai" if llm is not None else "offline"
    except Exception:
        return "offline"

def _extractive_answer(message: str, context: Optional[str]) -> str:
    """Compose a concise, grounded answer without calling an LLM.
    Strategy: split context into sentences, score by keyword overlap with the query,
    pick top sentences (1-4), and compress into a single paragraph.
    """
    import re
    if not context:
        return (
            "I'm working offline right now and can't call an LLM. "
            "Please ask a more specific question or provide more context."
        )
    q_words = set(re.findall(r"[A-Za-zÀ-ÿ0-9']+", (message or '').lower()))
    sents = re.split(r"(?<=[.!?])\s+|\n+", context)
    scored = []
    for s in sents:
        sw = set(re.findall(r"[A-Za-zÀ-ÿ0-9']+", s.lower()))
        if not sw:
            continue
        overlap = len(q_words & sw) / (len(sw) + 1e-6)
        # Boost for sentences that contain classic summary keywords
        if any(k in s.lower() for k in ["key", "main", "important", "summary", "purpose", "definition"]):
            overlap *= 1.2
        scored.append((overlap, s.strip()))
    if not scored:
        return (
            "I'm working offline and couldn't match your question to the document. "
            "Try asking about key topics, definitions, or sections."
        )
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [s for _, s in scored[:4]]
    # De-duplicate while preserving order
    seen = set()
    unique = []
    for s in top:
        k = s.lower()
        if k not in seen:
            seen.add(k)
            unique.append(s)
    answer = " ".join(unique)
    # Light cleanup
    answer = " ".join(answer.split())
    # Keep it reasonably short
    return answer[:800]


def chat_with_context(message: str, context: Optional[str]) -> str:
    llm = _load_chat_model()
    if llm is None:
        return _extractive_answer(message, context)
    try:
        from langchain.prompts import ChatPromptTemplate
        tmpl = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful study tutor. Use the provided context if relevant. Be concise and clear."),
            ("system", "Context:\n{context}"),
            ("human", "{question}")
        ])
        prompt = tmpl.format_messages(context=(context or "(no context)"), question=message)
        resp = llm.invoke(prompt)
        return resp.content.strip()
    except Exception:
        # Fall back to extractive if LLM fails
        return _extractive_answer(message, context)


def generate_quiz_from_text_langchain(text: str, num_questions: int = 6) -> List[Dict]:
    def _simple_mcq_from_text(t: str, n: int) -> List[Dict]:
        import re, random
        stems = [
            "According to the document, which statement is true?",
            "Which option is best supported by the document?",
            "Which statement best reflects the document's content?",
            "What conclusion is supported by the document?",
        ]
        # Extract sentences
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", (t or "")) if len(s.strip()) > 20]
        if not sents:
            sents = [
                "This document discusses key concepts and definitions.",
                "It presents examples and main ideas.",
                "It concludes with important takeaways.",
                "It introduces important terminology and context.",
            ]
        # Deduplicate
        seen = set(); uniq = []
        for s in sents:
            k = s.lower()
            if k not in seen:
                seen.add(k); uniq.append(s)
        random.shuffle(uniq)
        out = []
        for i in range(max(1, n)):
            correct = uniq[i % len(uniq)]
            pool = [x for x in uniq if x != correct]
            random.shuffle(pool)
            distractors = (pool[:3] if len(pool) >= 3 else (pool + ["None of the above", "All of the above", "Not specified"]))[:3]
            options = [correct] + distractors
            random.shuffle(options)
            correct_index = options.index(correct)
            out.append({
                "id": i+1,
                "question": stems[i % len(stems)],
                "options": options,
                "correct_answer": correct_index,
                "type": "multiple_choice",
            })
        return out

    llm = _load_chat_model()
    if llm is None:
        return _simple_mcq_from_text(text, num_questions)
    try:
        from langchain.prompts import ChatPromptTemplate
        tmpl = ChatPromptTemplate.from_messages([
            ("system", "You generate quizzes as valid JSON. No extra commentary."),
            ("system", "Return a JSON array of objects with: question (string), options (array of 4 strings), correct_index (0-3)."),
            ("system", "Ensure options are plausible and distinct. Focus on key concepts from the text."),
            ("human", "Create {n} multiple-choice questions from this text.\nTEXT:\n{doc}")
        ])
        prompt = tmpl.format_messages(n=num_questions, doc=text[:12000])
        resp = llm.invoke(prompt)
        raw = resp.content.strip()
        # Try direct parse, then attempt to repair by extracting JSON array
        try:
            data = json.loads(raw)
        except Exception:
            import re
            m = re.search(r"\[.*\]", raw, re.S)
            if not m:
                raise ValueError("No JSON array found in LLM output")
            data = json.loads(m.group(0))
        out = []
        for i, q in enumerate(data):
            out.append({
                "id": i+1,
                "question": q.get("question", ""),
                "options": q.get("options", []),
                "correct_answer": q.get("correct_index", 0),
                "type": "multiple_choice",
            })
        # If fewer than requested, pad with simple ones
        if len(out) < num_questions:
            extra = _simple_mcq_from_text(text, num_questions - len(out))
            # Fix IDs to be continuous
            for j, q in enumerate(extra, start=len(out)+1):
                q["id"] = j
            out.extend(extra)
        return out
    except Exception:
        # Fallback to non-LLM MCQ generator using the actual text so it stays relevant
        return _simple_mcq_from_text(text, num_questions)
