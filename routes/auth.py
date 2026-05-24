from flask import Blueprint, request, jsonify
from itsdangerous import Serializer
from database.db import get_connection
from flask_jwt_extended import create_access_token  # type: ignore
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import URLSafeTimedSerializer
import os


SECRET_KEY = os.getenv("SECRET_KEY")
serializer = URLSafeTimedSerializer(SECRET_KEY)

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    
    data = request.json

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (data["email"],)
    )

    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    # -------------------------
    # GOOGLE USER BLOCK
    # -------------------------
    if user["auth_provider"] == "google":
        return jsonify({
            "message": "Please login using Google"
        }), 400

    # -------------------------
    # LOCAL LOGIN
    # -------------------------
    if check_password_hash(user["password"], data["password"]):

        token = create_access_token(
            identity=str(user["id"]),
            additional_claims={
                "role": user["role"]
            }
        )

        safe_user = {
           "id": user["id"],
           "name": user["name"],          # ✅ add this
           "username": user["username"],  # ✅ add this
           "email": user["email"],
           "role": user["role"]
}

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": safe_user
        })

    return jsonify({"message": "Invalid credentials"}), 401


@auth.route("/google-login", methods=["POST", "OPTIONS"])
def google_login():

    # ✅ HANDLE PREFLIGHT REQUEST
    if request.method == "OPTIONS":
        return jsonify({"message": "ok"}), 200

    data = request.json
    email = data.get("email")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "User not found"}), 404

    token = create_access_token(
        identity=str(user["id"]),
        additional_claims={"role": user["role"]}
    )

    return jsonify({
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "username": user["username"],
            "role": user["role"]
        }
    })


@auth.route("/register", methods=["POST"])
def register():
    try:
        data = request.json

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (data["email"],)
        )

        if cursor.fetchone():
            return jsonify({
                "message": "Email already exists"
            }), 400

        auth_provider = data.get("auth_provider", "local")

        if auth_provider == "google":
            hashed_password = None
        else:
            hashed_password = generate_password_hash(
                data["password"]
            )

        cursor.execute(
            """
            INSERT INTO users
            (name, email, username, password, auth_provider)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                data["name"],
                data["email"],
                data["username"],
                hashed_password,
                auth_provider
            )
        )

        conn.commit()

        return jsonify({
            "message": "User registered"
        })

    except Exception as e:
        print("REGISTER ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()
        
        
@auth.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get("email")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "User not found"}), 404

    # ✅ generate token properly
    token = serializer.dumps(email, salt="reset-password")

    reset_link = f"http://localhost:5173/reset-password/{token}"

    return jsonify({
         "message": "Reset link generated",
          "reset_link": reset_link
    })
    
@auth.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    try:
        email = serializer.loads(
            token,
            salt="reset-password",
            max_age=600
        )
    except:
        return jsonify({"message": "Invalid or expired token"}), 400

    new_password = request.json.get("password")
    hashed = generate_password_hash(new_password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET password=%s WHERE email=%s",
        (hashed, email)
    )

    conn.commit()

    return jsonify({
    "message": "Password updated successfully",
    "redirect": "/login"
    })