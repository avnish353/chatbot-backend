from database.db import get_connection

def get_all_faqs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # IMPORTANT

    cursor.execute("SELECT * FROM faq")
    data = cursor.fetchall()

    conn.close()
    return data

def save_chat(user_id, chat_id, user_message, bot_reply):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO chat_history
    (user_id, chat_id, user_message, bot_reply)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (user_id, chat_id, user_message, bot_reply)
    )

    conn.commit()

    cursor.close()
    conn.close()