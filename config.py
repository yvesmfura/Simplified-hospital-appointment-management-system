import os

class Config:
    SECRET_KEY = "fg7rh849984bhdbd9477484gdbdbvxtsbxjdjd994474bbdvssjsk"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587  # Port for TLS
    MAIL_USE_TLS = True  # Use TLS encryption
    MAIL_USERNAME = 'your-email@example.com'  # Your email username
    MAIL_PASSWORD = 'your-email-password'  # Your email password
    MAIL_DEFAULT_SENDER = 'your-email@example.com'  # Default sender email