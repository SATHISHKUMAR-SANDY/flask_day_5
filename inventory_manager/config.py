import os

class Config:
    # Secret key for form security
    SECRET_KEY = os.getenv('SECRET_KEY', 'inventory_secret')

    # Use remote DB if available (for Render or production), otherwise fallback to local
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',  # Render or remote DB environment variable
        'mysql+pymysql://root:your_local_password@localhost/inventory_db'  # Local fallback
    )

    # Turn off modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
