import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://username:password@localhost:5432/event_db'  # Change to your PG settings
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
