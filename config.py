import os

class Config:
    # Load the secret key from environment variables
    SECRET_KEY = os.getenv('SECRET_KEY') 

    # Load the database URI from environment variables
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration loaded from environment variables
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.googlemail.com')  # Usually SMTP server
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Convert to integer; 587 is common for TLS
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1']  # Convert to boolean
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Securely fetched from environment
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Securely fetched from environment
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')  # Default sender email
