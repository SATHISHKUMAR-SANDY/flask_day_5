import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'  # Change to PostgreSQL if needed
    SQLALCHEMY_TRACK_MODIFICATIONS = False
