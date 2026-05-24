from services.db_client import fetch_faqs, save_chat,update_chat_title
from nlp.preprocess import preprocess
from nlp.embeddings import encode_texts, encode_single
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random
from nlp.intents import INTENTS
from nlp.intent_matcher import detect_intent

# Load FAQs once
faqs = fetch_faqs()
questions = [f["question"] for f in faqs]
answers = [f["answer"] for f in faqs]

processed_questions = [preprocess(q) for q in questions]
faq_embeddings = encode_texts(processed_questions)


# ---------------- MAIN CHAT FUNCTION ----------------
def get_response(user_input, user_id, chat_id):

    # ---------------- TITLE UPDATE ----------------
    chat_title = " ".join(user_input.split()[:5])
    update_chat_title(chat_id, chat_title)
  

    processed_input = preprocess(user_input)
    
    # ---------------- 1. HARD RULES ----------------
    text = user_input.lower().strip()

    if text in ["hi", "hello", "hey", "hii", "good morning", "good evening"]:

        bot_reply = random.choice(INTENTS["greeting"]["responses"])
        save_chat(user_id, chat_id, user_input, bot_reply)
        return bot_reply

    if text in ["bye", "goodbye", "see you"]:
        bot_reply = random.choice(INTENTS["farewell"]["responses"])
        save_chat(user_id, chat_id, user_input, bot_reply)
        return bot_reply

    # ---------------- 2. FAQ MATCHING (PRIORITY 1) ----------------
    user_vec = encode_single(processed_input)
    similarities = cosine_similarity([user_vec], faq_embeddings)[0]
    best_idx = int(np.argmax(similarities))
    best_score = float(similarities[best_idx])

    if best_score >= 0.85:
        bot_reply = answers[best_idx]
        save_chat(user_id, chat_id, user_input, bot_reply)
        return bot_reply

    # ---------------- 3. INTENT MATCHING (PRIORITY 2) ----------------
    intent_result = detect_intent(processed_input)
    if intent_result and intent_result.get("score", 0) >= 0.25:
        bot_reply = intent_result["response"]
        save_chat(user_id, chat_id, user_input, bot_reply)
        return bot_reply

    # ---------------- 4. FALLBACK ----------------
    bot_reply = "I couldn't find a clear answer. Can you provide more details?"
    save_chat(user_id, chat_id, user_input, bot_reply)
    return bot_reply

# ---------------- RELOAD FAQS ----------------

def reload_faqs():

    global faqs, questions, answers, faq_embeddings

    faqs = fetch_faqs()

    questions = [f["question"] for f in faqs]
    answers = [f["answer"] for f in faqs]

    processed_questions = [
        preprocess(q)
        for q in questions
    ]

    faq_embeddings = encode_texts(processed_questions)