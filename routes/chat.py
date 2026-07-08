from flask import Blueprint, request, jsonify,Response
from database.db import get_connection
from nlp.chatbot import get_response
from services.db_client import delete_chat_from_db,get_chat_history
from flask_jwt_extended import jwt_required, get_jwt_identity 

Chat = Blueprint("chat", __name__)

@Chat.route("/", methods=["POST"])
@jwt_required()
def chat_api():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    user_message = data["message"]

    if not user_message or user_message.strip() == "":
        return jsonify({"error": "Empty message"}), 400

    user_id = get_jwt_identity()
    chat_id = data.get("chat_id")
    
    reply = get_response(user_message, user_id,chat_id)
    return jsonify({"reply": reply})

@Chat.route('/stream', methods=['POST'])
@jwt_required()
def stream():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    user_message = data.get("message", "")
    chat_id = data.get("chat_id")

    user_id = get_jwt_identity()

    def generate():
        try:
            reply = get_response(
                user_message,
                user_id,
                chat_id
            )

            yield reply

        except Exception as e:
            yield f"Error: {str(e)}"

    return Response(
        generate(),
        mimetype="text/event-stream"
    )

@Chat.route("/create", methods=["POST"])
@jwt_required()
def create_chat():

    user_id = get_jwt_identity()

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO chats (user_id, title)
        VALUES (%s, %s)
    """

    cursor.execute(query, (user_id, "New Chat"))
    conn.commit()

    chat_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "chat_id": chat_id,
        "title": "New Chat"
    })

@Chat.route("/history/<int:user_id>")
@jwt_required()
def history(user_id):
    chats = get_chat_history(user_id) 
    return jsonify(chats)

@Chat.route("/<int:chat_id>", methods=["DELETE"])
@jwt_required()
def delete_chat(chat_id):

    user_id = get_jwt_identity()

    try:
        # delete only user's chat
        deleted = delete_chat_from_db(user_id, chat_id)

        if not deleted:
            return jsonify({"error": "Chat not found"}), 404

        return jsonify({"message": "Chat deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
