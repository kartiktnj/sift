from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load embedding model (very strong general-purpose model)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_important_sentences(text: str, top_ratio: float = 0.35) -> str:
    # Split into sentences
    sentences = [s.strip() for s in text.split(". ") if len(s.strip()) > 20]

    if len(sentences) < 5:
        return text  # not enough content to filter

    # Generate embeddings
    sentence_embeddings = embedding_model.encode(sentences)
    document_embedding = np.mean(sentence_embeddings, axis=0).reshape(1, -1)

    # Compute similarity
    similarities = cosine_similarity(sentence_embeddings, document_embedding)

    # Rank sentences
    ranked_indices = np.argsort(similarities.flatten())[::-1]

    # Select top sentences
    top_n = int(len(sentences) * top_ratio)
    selected_indices = sorted(ranked_indices[:top_n])

    selected_sentences = [sentences[i] for i in selected_indices]

    return ". ".join(selected_sentences)