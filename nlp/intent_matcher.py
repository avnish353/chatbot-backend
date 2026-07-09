import random
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from nlp.intents import INTENTS
from nlp.preprocess import preprocess
from nlp.embeddings import encode_texts, encode_single

intent_patterns = []
intent_names = []

for intent_name, intent_data in INTENTS.items():
    for pattern in intent_data["patterns"]:
        intent_patterns.append(preprocess(pattern))
        intent_names.append(intent_name)

intent_embeddings = encode_texts(intent_patterns)

def detect_intent(user_input):

    processed = preprocess(user_input)

    query_embedding = encode_single(processed)

    similarities = cosine_similarity(
        [query_embedding],
        intent_embeddings
    )[0]

    best_idx = np.argmax(similarities)
    best_score = float(similarities[best_idx])
    print("Input:", processed)
    print("Matched Intent:", intent_names[best_idx])
    print("Similarity:", best_score)

    if best_score >= 0.50:

        intent_name = intent_names[best_idx]
        return {
            "response": random.choice(INTENTS[intent_name]["responses"]),
            "score": best_score
        }
        

    return None
def get_intent_suggestions(query):

    query = preprocess(query)

    results = []

    for intent_name, intent_data in INTENTS.items():
        for pattern in intent_data["patterns"]:

            pattern_clean = preprocess(pattern)

            if query in pattern_clean or pattern_clean in query:
                results.append({
                    "question": pattern
                })

    return results

