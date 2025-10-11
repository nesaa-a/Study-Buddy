import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from backend.config.env_config import Config

def generate_access_token(user_id):
    """Generate JWT access token"""
    try:
        payload = {
            'user_id': user_id,
            'token_type': 'access',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_ACCESS_TOKEN_EXPIRE_HOURS),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, Config.get_jwt_secret_key(), algorithm="HS256")
    except Exception as e:
        raise ValueError(f"Failed to generate access token: {str(e)}")

def generate_refresh_token(user_id):
    """Generate JWT refresh token"""
    try:
        payload = {
            'user_id': user_id,
            'token_type': 'refresh',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=Config.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, Config.get_jwt_secret_key(), algorithm="HS256")
    except Exception as e:
        raise ValueError(f"Failed to generate refresh token: {str(e)}")

def verify_token(token_type='access'):
    """Decorator to verify JWT tokens"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = None

            # Extract token from Authorization header
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

            if not token:
                return jsonify({"error": "Missing token!"}), 401

            try:
                # Decode and verify token
                decoded = jwt.decode(
                    token, 
                    Config.get_jwt_secret_key(), 
                    algorithms=["HS256"]
                )
                
                # Verify token type
                if decoded.get('token_type') != token_type:
                    return jsonify({"error": f"Invalid token type. Expected {token_type}"}), 401
                
                # Add user info to request context
                request.user_id = decoded["user_id"]
                request.token_payload = decoded
                
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired!"}), 401
            except jwt.InvalidTokenError as e:
                return jsonify({"error": f"Invalid token: {str(e)}"}), 401
            except Exception as e:
                return jsonify({"error": f"Token verification failed: {str(e)}"}), 401

            return func(*args, **kwargs)
        return wrapper
    return decorator

def refresh_access_token(refresh_token):
    """Generate new access token from refresh token"""
    try:
        # Verify refresh token
        decoded = jwt.decode(
            refresh_token, 
            Config.get_jwt_secret_key(), 
            algorithms=["HS256"]
        )
        
        if decoded.get('token_type') != 'refresh':
            raise ValueError("Invalid token type")
        
        # Generate new access token
        return generate_access_token(decoded['user_id'])
        
    except jwt.ExpiredSignatureError:
        raise ValueError("Refresh token expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid refresh token: {str(e)}")
    except Exception as e:
        raise ValueError(f"Token refresh failed: {str(e)}")
