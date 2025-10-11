from flask import Blueprint, request, jsonify
import bcrypt
from backend.models.user_model import create_user, get_user_by_email
from backend.utils.jwt_utils import verify_token

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    """User registration endpoint"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400
    
    # Check if user already exists
    if get_user_by_email(email):
        return jsonify({"error": "User already exists"}), 400
    
    # Hash password securely using bcrypt
    try:
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        create_user(name, email, password_hash)
        return jsonify({"message": "User registered successfully!"}), 201
        
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@user_bp.route("/profile", methods=["GET"])
@verify_token()
def get_profile():
    """Get user profile - requires authentication"""
    try:
        user = get_user_by_email(request.user_id)  # This might need adjustment based on your user model
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get profile: {str(e)}"}), 500
