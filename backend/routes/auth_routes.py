from flask import Blueprint, request, jsonify
import hashlib
import jwt
import datetime
from backend.models.user_model import get_user_by_email
from backend.utils.jwt_utils import verify_token

auth_bp = Blueprint("auth_bp", __name__)
SECRET_KEY = "sekret123"  # çelës sekret për JWT

@auth_bp.route("/login", methods=["POST"])
@verify_token
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if password_hash != user["password_hash"]:
        return jsonify({"error": "Incorrect password"}), 401

    # ✅ Këtu krijohet token-i JWT
    token = jwt.encode({
        "user_id": user["id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm="HS256")

    # Kthe tokenin dhe të dhënat e përdoruesit
    return jsonify({
        "message": "Login successful!",
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }), 200
