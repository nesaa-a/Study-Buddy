from flask import Blueprint, request, jsonify
import bcrypt
from backend.models.user_model import get_user_by_email
from backend.utils.jwt_utils import verify_token, generate_access_token, generate_refresh_token, refresh_access_token

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    """User login endpoint - generates JWT tokens"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Verify password using bcrypt
    try:
        if not bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": "Authentication failed"}), 401

    try:
        # Generate JWT tokens
        access_token = generate_access_token(user["id"])
        refresh_token = generate_refresh_token(user["id"])

        return jsonify({
            "message": "Login successful!",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Token generation failed: {str(e)}"}), 500

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    """Refresh access token using refresh token"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": "Refresh token is required"}), 400

    try:
        new_access_token = refresh_access_token(refresh_token)
        return jsonify({
            "message": "Token refreshed successfully",
            "access_token": new_access_token
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": f"Token refresh failed: {str(e)}"}), 500

@auth_bp.route("/logout", methods=["POST"])
@verify_token()
def logout():
    """User logout endpoint - client should discard tokens"""
    return jsonify({"message": "Logout successful"}), 200
