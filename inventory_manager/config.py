import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'inventory_secret')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost/inventory_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
