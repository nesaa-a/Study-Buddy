# backend/services/summarizer.py
from transformers import pipeline

# Load the model once (takes ~1 min the first time)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text, length="medium"):
    if not text or text.strip() == "":
        return "No text available for summarization."
    
    # Adjust summary length
    if length == "short":
        max_len = 80
    elif length == "medium":
        max_len = 150
    else:
        max_len = 300

    summary = summarizer(
        text,
        max_length=max_len,
        min_length=30,
        do_sample=False
    )
    return summary[0]["summary_text"]
