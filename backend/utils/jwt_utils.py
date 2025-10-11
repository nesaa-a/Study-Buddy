import jwt
from flask import request, jsonify

SECRET_KEY = "sekret123"  # must be the same as in auth_routes.py

def verify_token(func):
    def wrapper(*args, **kwargs):
        token = None

        # Take the token from the headers
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "Missing token!"}), 401

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = decoded["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

        return func(*args, **kwargs)
    return wrapper
