import random
from nlp.intents import INTENTS
from nlp.preprocess import preprocess

def detect_intent(user_input):

    processed = preprocess(user_input)
    processed_tokens = set(processed.split())

    best_intent = None
    best_score = 0

    for intent_name, intent_data in INTENTS.items():

        for pattern in intent_data["patterns"]:

            pattern_processed = preprocess(pattern)
            pattern_tokens = set(pattern_processed.split())

            if len(pattern_tokens) == 0:
                continue

            # 🔥 improved scoring (recall-friendly)
            overlap = len(pattern_tokens & processed_tokens)
            score = overlap / len(pattern_tokens)

            # bonus boost for partial phrase match
            if processed in pattern_processed or pattern_processed in processed:
                score += 0.3

            if score > best_score:
                best_score = score
                best_intent = intent_data

    # 🔥 LOWER threshold (important fix)
    if best_score >= 0.25:
        return {
            "response": random.choice(best_intent["responses"]),
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

