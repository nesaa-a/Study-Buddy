import re
from typing import List, Dict

def split_sentences(text: str) -> List[str]:
    if not text:
        return []
    text = re.sub(r"\s+", " ", text)
    # naive sentence split
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p and len(p.strip()) > 20]

def extract_keywords(text: str, limit: int = 8) -> List[str]:
    words = re.findall(r"[A-Za-z][A-Za-z\-]{3,}", text)
    stop = set([
        'this','that','with','from','have','which','their','about','your','into','will','they','were','been','also','some','more','such','than','most','many','like','when','what','where','how','why','then','them','these','those','over','under','between','using','based','within','without','through','only','other','very','each','much','make','made','after','before','because','while','there','here','into','onto','across','upon','even'
    ])
    freq = {}
    for w in words:
        lw = w.lower()
        if lw in stop:
            continue
        freq[lw] = freq.get(lw, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w,_ in ranked[:limit]]

def build_multiple_choice(question_text: str, correct: str) -> Dict:
    # naive distractors: small variations
    distractors = [correct + ' concept', 'unrelated term', 'none of the above']
    options = [correct] + distractors
    return {
        'id': None,
        'question': question_text,
        'options': options,
        'correct_answer': 0,
        'type': 'multiple_choice',
    }

def generate_quiz_from_text(text: str) -> List[Dict]:
    sentences = split_sentences(text)
    if not sentences:
        # fallback, return generic
        return [
            {
                'id': None,
                'question': 'What is the main topic discussed in the document?',
                'options': ['Topic A', 'Topic B', 'Topic C', 'Topic D'],
                'correct_answer': 0,
                'type': 'multiple_choice',
            },
            {
                'id': None,
                'question': 'Summarize the document in one sentence.',
                'options': [],
                'correct_answer': None,
                'type': 'open_ended',
            },
        ]

    keywords = extract_keywords(text, limit=6)
    questions: List[Dict] = []

    if keywords:
        k = keywords[0]
        questions.append(
            build_multiple_choice(f"Which concept is central in the document?", k.capitalize())
        )

    # Use first informative sentence as open-ended
    questions.append({
        'id': None,
        'question': f"Explain: {sentences[0][:120]}...",
        'options': [],
        'correct_answer': None,
        'type': 'open_ended',
    })

    if len(sentences) > 2:
        questions.append({
            'id': None,
            'question': f"What is the key point of: {sentences[1][:120]}?",
            'options': [],
            'correct_answer': None,
            'type': 'open_ended',
        })

    return questions


