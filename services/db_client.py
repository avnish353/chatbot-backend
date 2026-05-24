from database.queries import get_all_faqs
from database.db import get_connection 

def fetch_faqs():
    """
    Fetches all FAQs from the database.

    Returns:
        list of dicts: [{"question": "...", "answer": "..."}, ...]
    """
    return get_all_faqs()

def save_chat(user_id, chat_id, user_msg, bot_msg):

    if chat_id is None:
        raise ValueError("chat_id is missing")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO chat_history (user_id, chat_id, user_message, bot_reply)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (user_id, chat_id, user_msg, bot_msg))

    conn.commit()

    cursor.close()
    conn.close()
    print("SAVE CHAT → user_id:", user_id, "chat_id:", chat_id)
    
def get_chat_history(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT chat_id, user_message, bot_reply, created_at
    FROM chat_history
    WHERE user_id = %s
    ORDER BY created_at ASC
    """

    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    grouped = {}

    for r in rows:
        cid = r["chat_id"]

        if cid not in grouped:
            grouped[cid] = {
                "id": cid,
                "title": r["user_message"][:30],
                "messages": []
            }

        # USER MESSAGE
        grouped[cid]["messages"].append({
            "text": r["user_message"],
            "sender": "user",
            "time": r["created_at"].isoformat()
                if r["created_at"] else None
        })

        # BOT MESSAGE
        grouped[cid]["messages"].append({
            "text": r["bot_reply"],
            "sender": "bot",
            "time": r["created_at"].isoformat()
                if r["created_at"] else None
        })

    cursor.close()
    conn.close()

    return list(grouped.values())

def delete_chat_from_db(user_id, chat_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    DELETE FROM chat_history
    WHERE user_id = %s AND chat_id = %s
    """

    cursor.execute(query, (user_id, chat_id))
    conn.commit()

    return cursor.rowcount > 0

def update_chat_title(chat_id, title):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE chats
    SET title = %s
    WHERE id = %s
    AND (title IS NULL OR title = 'New Chat')
    """

    cursor.execute(query, (title, chat_id))
    conn.commit()

    cursor.close()
    conn.close()
