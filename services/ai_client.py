from services.db_client import fetch_faqs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_bot_response(user_message):
    faqs = fetch_faqs()

    questions = [faq["question"] for faq in faqs]
    answers = [faq["answer"] for faq in faqs]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(questions + [user_message])

    similarity = cosine_similarity(vectors[-1], vectors[:-1])

    best_match_index = similarity.argmax()
    score = similarity[0][best_match_index]

    if score > 0.3:
        return answers[best_match_index]

    return "Sorry, I couldn't find a good answer. Try rephrasing."