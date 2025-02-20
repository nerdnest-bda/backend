import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class for Flask"""

    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")  
    DEBUG = os.getenv("DEBUG", "False").lower() == "true" 

    # MongoDB settings
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/flask_api")
    USER_DB = os.getenv("USER_DB", "dev-nerdnest")

    # JWT settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "your_default_jwt_secret")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 7200)) 

    # CORS settings
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "*")  

    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  
