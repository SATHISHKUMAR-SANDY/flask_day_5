from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    job_title = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='applied')  # applied, shortlisted, rejected

    def __repr__(self):
        return f'<Application {self.name} - {self.job_title} - {self.status}>'
