import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost/jobtrackerdb'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
