from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database connected and tables created.")
        except Exception as e:
            print("Database connection failed:", e)
    app.run(debug=True)
