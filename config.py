import os

class Config:
    # Load the secret key from environment variables
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Load the database URI from environment variables or use SQLite for local development/testing
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration loaded from environment variables
    MAIL_SERVER = os.getenv('MAIL_SERVER')  # Usually SMTP server
    MAIL_PORT = int(os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1'] 
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER') 
