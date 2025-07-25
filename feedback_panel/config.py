import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "feedback_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///feedback.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
