from flask import Blueprint, request, jsonify
from backend.models.user_model import create_user, get_user_by_email
import hashlib

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    # Kontrollo nëse user ekziston
    if get_user_by_email(email):
        return jsonify({"error": "User already exists"}), 400
    
    # Hash password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Ruaj user në DB
    create_user(name, email, password_hash)
    
    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route("/login", methods=["POST"])
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
    
    return jsonify({"message": "Login successful!", "user": user})
