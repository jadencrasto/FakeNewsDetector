"""
Configuration settings for the application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-change-this')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    
    # Database Settings
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # API Keys
    VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY')
    GOOGLE_SAFE_BROWSING_KEY = os.getenv('GOOGLE_SAFE_BROWSING_KEY')
    
    # Server Settings
    PORT = int(os.getenv('PORT', 5000))
    HOST = '0.0.0.0'
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_DEFAULT = "100 per day, 20 per hour"
    
    # CORS Settings
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:8000', 
        'http://127.0.0.1:8000',
        'http://localhost:8080',  # ← Add this!
        'http://127.0.0.1:8080',  # ← Add this!
        'http://localhost:5173',
        'http://127.0.0.1:5173'
    ]
    
    # Risk Score Thresholds
    RISK_THRESHOLD_SAFE = 30
    RISK_THRESHOLD_SUSPICIOUS = 60
    
    # Analysis Settings
    MAX_INPUT_LENGTH = 5000  # Maximum characters in input
    CACHE_TIMEOUT = 3600  # Cache results for 1 hour

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Use stronger rate limits in production
    RATELIMIT_DEFAULT = "50 per day, 10 per hour"

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'postgresql://postgres:password@localhost:5432/test_scam_detector'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}