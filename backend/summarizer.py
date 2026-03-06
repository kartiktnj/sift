from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from semantic_extractor import extract_important_sentences
from preprocessor import clean_text
import torch
import time

MODEL_NAME = "google/pegasus-xsum"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def summarize_chunk(chunk, max_summary_length, min_summary_length):
    inputs = tokenizer(
        chunk,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )
    print("max Length", max_summary_length)

    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=max_summary_length,
        min_length=min_summary_length,
        num_beams=4,
        no_repeat_ngram_size=3
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


def summarize_text(text: str, max_summary_length: int = 150, min_summary_length: int = 60, top_ratio: float = 0.6) -> str:
    start_time = time.time()

    text = clean_text(text)
    # Extract important content first
    text = extract_important_sentences(text, top_ratio=top_ratio)

    # Split into sentences first
    sentences = text.split(". ")

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        test_chunk = current_chunk + sentence + ". "

        token_count = len(tokenizer.tokenize(test_chunk))

        if token_count < 450:
            current_chunk = test_chunk
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk)

    summaries = []

    for chunk in chunks:
        summaries.append(summarize_chunk(chunk, max_summary_length, min_summary_length))

    combined = " ".join(summaries)

    # Final summarization pass (if not too large)
    if len(tokenizer.tokenize(combined)) > 1024 and max_summary_length < 300:
        combined = summarize_chunk(combined, max_summary_length, min_summary_length)

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