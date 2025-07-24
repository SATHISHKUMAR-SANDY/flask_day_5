from flask import Flask
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def index():
    return 'Flask Model Project - All Models Created'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database and tables created.")
    app.run(debug=True)
