from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# --------- ENCODING ---------

def encode_texts(texts):
    """
    Batch encoding (FAST)
    """
    return model.encode(texts, normalize_embeddings=True)


def encode_single(text):
    """
    Single text encoding
    """
    return model.encode([text], normalize_embeddings=True)[0]


# --------- SIMILARITY ---------

def get_similarity(vec1, vec2):
    return cosine_similarity([vec1], [vec2])[0][0]


def get_best_match(query_vec, corpus_vecs):
    scores = cosine_similarity([query_vec], corpus_vecs)[0]
    best_idx = int(np.argmax(scores))
    return best_idx, float(scores[best_idx])