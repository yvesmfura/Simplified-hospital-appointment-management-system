import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fg7rh849984bhdbd9477484gdbdbvxtsbxjdjd994474bbdvssjsk')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Ensure to convert to the appropriate type (int, str, etc.)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True) in ['True', 'true', '1']  # Convert string to boolean if needed
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'your-email@example.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your-email-password')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'your-email@example.com')
