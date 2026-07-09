from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.chat import  Chat
from routes.auth import auth
from routes.admin import admin
from flask_jwt_extended import JWTManager # type: ignore
import os
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__) 
CORS(
    app,
    origins=[
        "https://chatbot-frontend-lovat-psi.vercel.app",
    ],
    supports_credentials=True
)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# JWT CONFIG
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

app.register_blueprint(Chat, url_prefix="/api/chat")
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(admin, url_prefix="/api/admin")

@app.errorhandler(Exception)
def handle_error(e):
    return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
