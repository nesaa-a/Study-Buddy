#!/usr/bin/env python3
"""
Script to generate a secure JWT secret key for production use.
Run this script to generate a cryptographically secure secret key.
"""

import secrets
import string

def generate_secret_key(length=64):
    """Generate a cryptographically secure secret key"""
    # Use URL-safe base64 characters for the secret key
    alphabet = string.ascii_letters + string.digits + '-_'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_token_safe_key(length=64):
    """Generate a URL-safe token for JWT secret key"""
    return secrets.token_urlsafe(length)

if __name__ == "__main__":
    print("🔐 JWT Secret Key Generator")
    print("=" * 50)
    
    # Generate different types of keys
    print("\n1. URL-safe token (recommended):")
    url_safe_key = generate_token_safe_key(64)
    print(f"JWT_SECRET_KEY={url_safe_key}")
    
    print("\n2. Custom alphabet key:")
    custom_key = generate_secret_key(64)
    print(f"JWT_SECRET_KEY={custom_key}")
    
    print("\n3. Longer key (128 chars):")
    long_key = generate_token_safe_key(128)
    print(f"JWT_SECRET_KEY={long_key}")
    
    print("\n" + "=" * 50)
    print("✅ Copy one of these keys to your .env file")
    print("⚠️  Keep this key secret and never commit it to version control!")
    print("💡 The URL-safe token is recommended for most use cases.")
