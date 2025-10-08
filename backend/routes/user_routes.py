from flask import Blueprint, request, jsonify
from backend.models.user_model import create_user, get_user_by_email
import hashlib

user_bp = Blueprint("user_bp", __name__)

# REGISTER
@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    if get_user_by_email(email):
        return jsonify({"error": "User already exists"}), 400
    
    # Hash password (simplified)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    create_user(name, email, password_hash)
    return jsonify({"message": "User registered successfully!"}), 201

# LOGIN
@user_bp.route("/login", methods=["POST"])
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
    
    # Për testim, thjesht kthe user info (pa JWT për momentin)
    return jsonify({"message": "Login successful!", "user": user})
