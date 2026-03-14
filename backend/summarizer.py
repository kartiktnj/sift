from flask import jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from semantic_extractor import extract_important_sentences
from preprocessor import clean_text
import torch
import time

MODEL_NAME = "facebook/bart-large-cnn"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def summarize_text(text: str, max_summary_length: int = 150, min_summary_length: int = 60, top_ratio: float = 0.6) -> str:
    start_time = time.time()

    text = clean_text(text)
    # Extract important content first
    text = extract_important_sentences(text, top_ratio=top_ratio)

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=max_summary_length,
        min_length=min_summary_length,
        num_beams=2,
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    combined = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    print(f"Summarization took {time.time() - start_time:.2f} seconds")

    summary = [s.strip() for s in combined.split(". ") if len(s.strip()) > 20]
    key_points = summary[:5]
    short_summary = " ".join(summary[:2])

    return {
        "Title": summary[0][:60],
        "Key Points": key_points,
        "Short Summary": short_summary,
        "Full Summary": combined
    }