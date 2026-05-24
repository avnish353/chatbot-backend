from flask import Blueprint, request, jsonify
from services.db_client import get_connection
from difflib import SequenceMatcher
from services.auth_utils import admin_required
from nlp.chatbot import reload_faqs
from mysql.connector import IntegrityError
from difflib import SequenceMatcher
from nlp.intents import INTENTS

admin = Blueprint('admin', __name__)

@admin.route('/add-faq', methods=['POST'])
@admin_required
def add_faq():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 422

    question = data.get("question").strip().lower()
    answer = data.get("answer")
    category = data.get("category", "general")

    if not question or not answer:
        return jsonify({"error": "question and answer required"}), 422

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO faq (question, answer, category) VALUES (%s, %s, %s)",
            (question, answer, category)
        )
        conn.commit()

    except IntegrityError:
        return jsonify({"error": "FAQ already exists"}), 409

    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "FAQ added"})

@admin.route('/faqs', methods=['GET'])
def get_faqs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM faq")
    data = cursor.fetchall()

    return jsonify(data)

@admin.route('/update-faq/<int:id>', methods=['PUT'])
def update_faq(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    question = data.get("question")
    answer = data.get("answer")
    category = data.get("category", "general")

    if not question or not answer:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE faq 
        SET question=%s, answer=%s, category=%s 
        WHERE id=%s
    """, (question, answer, category, id))

    conn.commit()
    reload_faqs()
    cursor.close()
    conn.close()

    return jsonify({"message": "Updated"})

@admin.route('/delete-faq/<int:id>', methods=['DELETE'])
def delete_faq(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM faq WHERE id=%s", (id,))
    conn.commit()
    reload_faqs()
    return jsonify({"message": "Deleted"})

@admin.route('/search-faq', methods=['POST'])
def search_faq():
    data = request.json
    user_question = data['question']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT question, answer
    FROM faq
    WHERE question LIKE %s
    """

    cursor.execute(query, ("%" + user_question + "%",))
    result = cursor.fetchall()

    return jsonify(result)


def find_best_faq(user_question, faqs):
    best_match = None
    highest_score = 0

    for faq in faqs:
        score = SequenceMatcher(None, user_question.lower(), faq['question'].lower()).ratio()

        if score > highest_score:
            highest_score = score
            best_match = faq

    return best_match if highest_score > 0.5 else None

@admin.route("/suggest-faq", methods=["GET"])
def suggest_faq():

    q = request.args.get("q", "").lower()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # ---------------- DB FAQs ----------------
    cursor.execute("""
        SELECT question FROM faq
        WHERE question LIKE %s
        LIMIT 5
    """, ("%" + q + "%",))

    db_results = cursor.fetchall()

    # ---------------- INTENTS ----------------
    intent_results = []

    for intent_name, intent_data in INTENTS.items():
        for pattern in intent_data["patterns"]:
            if q in pattern:
                intent_results.append({
                    "question": pattern
                })

    # ---------------- MERGE + LIMIT ----------------
    final_results = (db_results + intent_results)[:7]

    return jsonify(final_results)

def is_duplicate(new_q, existing_faqs):
    for faq in existing_faqs:
        score = SequenceMatcher(None, new_q.lower(), faq["question"].lower()).ratio()
        if score > 0.85:
            return True
    return False