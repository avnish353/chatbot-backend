import random


def deduplicate_patterns(intents):

    for intent in intents.values():

        seen = set()
        unique = []

        for p in intent["patterns"]:

            clean = p.strip().lower()

            if clean not in seen:
                unique.append(clean)
                seen.add(clean)

        intent["patterns"] = unique

    return intents


INTENTS = {

    # ---------------- GREETING ----------------

    "greeting": {

        "patterns": [

            "hello there",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "how are you",
            "hey support",
            "hello support team",
            "can you help me"

        ],

        "responses": [

            "Hello! Welcome to Support Central. How can I help you today? 😊",

            "Hi there! I'm your AI support assistant. What can I help you with?",

            "Hey! Great to see you. Tell me how I can assist you today."
        ]
    },

    # ---------------- FAREWELL ----------------

    "farewell": {

        "patterns": [

            "goodbye",
            "bye bye",
            "see you later",
            "talk to you later",
            "thanks goodbye",
            "have a nice day",
            "take care",
            "bye for now"

        ],

        "responses": [

            "Goodbye! Have a wonderful day! 👋",

            "Take care! Feel free to come back anytime you need help.",

            "Bye! It was a pleasure helping you today 😊"
        ]
    },

    # ---------------- ORDER STATUS ----------------

    "order_status": {

        "patterns": [

            "where is my order",
            "track my order",
            "check my order status",
            "when will my package arrive",
            "i want to track my shipment",
            "delivery status of my order",
            "has my order shipped",
            "track my package",
            "order delivery update",
            "shipping update for my order"

        ],

        "responses": [

            "I can help you track your order! Please provide your order number (e.g., ORD-12345).",

            "Sure! Please share your order ID so I can check the shipping status.",

            "Let me look up your order. Could you provide the order number or email used during purchase?"
        ]
    },

    # ---------------- REFUND ----------------

    "refund": {

        "patterns": [

            "i want a refund",
            "refund my order",
            "can i get my money back",
            "requesting a refund",
            "cancel my order and refund",
            "i need reimbursement",
            "return and refund my purchase",
            "refund for damaged product",
            "how do i request refund",
            "refund my payment"

        ],

        "responses": [

            "I understand you'd like a refund. Please share your order number and reason for the request.",

            "No problem! Refunds are usually processed within 5-7 business days. Please provide your order ID.",

            "I'll help you with the refund process. Kindly share your order number and issue details."
        ]
    },

    # ---------------- PASSWORD RESET ----------------

    "password_reset": {

        "patterns": [

            "i forgot my password",
            "help me reset my password",
            "cannot login to my account",
            "i am locked out of my account",
            "change my account password",
            "password reset help",
            "unable to access my account",
            "login issue with my account",
            "reset my login password",
            "forgot account password"

        ],

        "responses": [

            "You can reset your password by clicking 'Forgot Password' on the login page.",

            "Go to Settings → Security → Reset Password to update your password.",

            "I'll help you regain access. Use the password reset link sent to your email."
        ]
    },

    # ---------------- BILLING ----------------

    "billing": {

        "patterns": [

            "payment failed",
            "i was charged twice",
            "billing issue with my account",
            "problem with my invoice",
            "subscription payment failed",
            "credit card was declined",
            "unable to process payment",
            "issue with billing",
            "incorrect charge on my account",
            "update my payment method"

        ],

        "responses": [

            "I can help with your billing issue. Could you describe the problem in more detail?",

            "Please share the payment date and amount so I can help investigate.",

            "Billing problems are usually resolved by updating payment details in Account → Billing."
        ]
    },

    # ---------------- TECHNICAL SUPPORT ----------------

    "technical_support": {

        "patterns": [

            "website is not working",
            "app keeps crashing",
            "i found a bug",
            "getting an error message",
            "website is loading slowly",
            "unable to access the app",
            "technical issue with website",
            "application is broken",
            "site is down",
            "my page is not loading",
            "system is very slow",
            "something is wrong with the app"

        ],

        "responses": [

            "Let's troubleshoot the issue. Please try refreshing the page or clearing browser cache.",

            "Could you share the exact error message and device/browser you're using?",

            "Please explain what happens when the issue occurs so I can assist further."
        ]
    },

    # ---------------- BOT IDENTITY ----------------

    "bot_identity": {

        "patterns": [

            "who are you",
            "what is your name",
            "tell me about yourself",
            "are you a chatbot",
            "what can you do",
            "who created you"

        ],

        "responses": [

            "I am an AI assistant designed to provide customer support.",

            "I'm your customer support AI assistant. I'm here to help you quickly.",

            "I help answer customer questions related to orders, billing, refunds, and technical issues."
        ]
    },

    # ---------------- PRODUCT INFO ----------------

    "product_info": {

        "patterns": [

            "tell me about your plans",
            "what features are included",
            "compare your pricing plans",
            "how does this product work",
            "product specifications",
            "difference between premium and basic",
            "explain your subscription plans",
            "what are the product features",
            "pricing details for your service",
            "compare available plans"

        ],

        "responses": [

            "Could you specify which product or plan you'd like information about?",

            "I'd be happy to explain the features and pricing. Which product interests you?",

            "I can help compare plans and features. Tell me what you'd like to know."
        ]
    },

    # ---------------- COMPLAINT ----------------

    "complaint": {

        "patterns": [

            "i am very disappointed",
            "this service is terrible",
            "i had a horrible experience",
            "i am frustrated with your service",
            "this is unacceptable",
            "worst customer support experience",
            "i am angry about my order",
            "very bad experience",
            "i want to complain",
            "this is ridiculous"

        ],

        "responses": [

            "I'm truly sorry about your experience. Please share more details so I can help resolve this.",

            "I understand your frustration and apologize for the inconvenience.",

            "Thank you for your feedback. I'll do my best to help make this right."
        ]
    },

    # ---------------- HUMAN AGENT ----------------

    "human_agent": {

        "patterns": [

            "i want to speak to a human",
            "connect me to live agent",
            "i need a real person",
            "transfer me to support agent",
            "talk to customer service representative",
            "escalate this issue",
            "i want to speak with manager",
            "connect me to supervisor"

        ],

        "responses": [

            "Of course! Connecting you to a live support agent now.",

            "I'll transfer your request to a human support representative shortly.",

            f"Your support ticket #{random.randint(10000,99999)} has been created. A human agent will assist you soon."
        ]
    },

    # ---------------- THANKS ----------------

    "thanks": {

        "patterns": [

            "thank you very much",
            "thanks for your help",
            "i appreciate your support",
            "you were very helpful",
            "thanks a lot",
            "great help thank you",
            "thanks for assisting me",
            "you are awesome"

        ],

        "responses": [

            "You're very welcome! 😊",

            "Happy to help! Let me know if you need anything else.",

            "Glad I could help! Have a great day ✨"
        ]
    }
}


# ---------------- FALLBACK RESPONSES ----------------

FALLBACK_RESPONSES = [

    "I want to make sure I give you the right answer. Could you provide more details?",

    "I'm not fully sure I understood. Could you explain your issue a little more?",

    "Could you clarify whether your issue is related to orders, billing, refunds, or technical support?",

    "I need a bit more information to help properly. Please describe the issue in detail."
]

INTENTS = deduplicate_patterns(INTENTS)