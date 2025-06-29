"""
PostgreSQL Configuration for Bank Accounts Management System
Usage: Set environment variables or import this configuration
"""

import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration - uses SQLite"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bank_accounts.db'

class ProductionConfig(Config):
    """Production configuration - uses PostgreSQL"""
    DEBUG = False
    
    # PostgreSQL Configuration
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'bankuser')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'bankpass123')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'bank_accounts_db')
    
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_bank_accounts.db'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 