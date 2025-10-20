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
    llm = _load_chat_model()
    if llm is None:
        # Simple fallback stub
        return [
            {"id": i+1, "question": f"Write a key fact from the document (item {i+1}).", "options": [], "correct_answer": None, "type": "open_ended"}
            for i in range(num_questions)
        ]
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
        data = json.loads(raw)
        out = []
        for i, q in enumerate(data):
            out.append({
                "id": i+1,
                "question": q.get("question", ""),
                "options": q.get("options", []),
                "correct_answer": q.get("correct_index", 0),
                "type": "multiple_choice",
            })
        return out
    except Exception:
        return [
            {"id": 1, "question": "What is the main topic of the document?", "options": ["A","B","C","D"], "correct_answer": 0, "type": "multiple_choice"}
        ]
