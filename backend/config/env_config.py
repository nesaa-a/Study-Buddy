import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_HOURS', '2'))
    JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRE_DAYS', '30'))
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'mysql://username:password@localhost:3306/study_buddy')
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    @classmethod
    def get_jwt_secret_key(cls):
        """Get JWT secret key with validation"""
        if cls.JWT_SECRET_KEY == 'fallback-secret-key-change-in-production':
            raise ValueError(
                "JWT_SECRET_KEY not set in environment variables. "
                "Please set a strong secret key in your .env file."
            )
        return cls.JWT_SECRET_KEY
