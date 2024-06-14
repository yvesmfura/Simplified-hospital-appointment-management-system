import os

class Config:
    # Load the secret key from environment variables or use a default for development/testing
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')  # Replace 'default-secret-key' with a secure default for local testing

    # Load the database URI from environment variables or use SQLite for local development/testing
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration loaded from environment variables
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.googlemail.com')  # Usually SMTP server
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Convert to integer; 587 is common for TLS
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1']  # Convert to boolean
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Securely fetched from environment
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Securely fetched from environment
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')  # Default sender email
