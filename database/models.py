class FAQ:
    def __init__(self, id, question, answer):
        self.id = id
        self.question = question
        self.answer = answer


class ChatHistory:
    def __init__(self, id, user_message, bot_reply):
        self.id = id
        self.user_message = user_message
        self.bot_reply = bot_reply