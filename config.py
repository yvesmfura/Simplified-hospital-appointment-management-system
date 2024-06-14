import os

class Config:
    SECRET_KEY = "fg7rh849984bhdbd9477484gdbdbvxtsbxjdjd994474bbdvssjsk"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587  # Port for TLS
    MAIL_USE_TLS = True  # Use TLS encryption
    MAIL_USERNAME = 'shamssupport@gmail.com'  # email username
    MAIL_PASSWORD = 'Software@2024'  # email password
    MAIL_DEFAULT_SENDER = 'shamssupport@gmail.com'  # Default sender email
