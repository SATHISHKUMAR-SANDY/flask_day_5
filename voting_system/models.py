from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100), nullable=False)
    votes = db.relationship('Vote', backref='candidate', lazy=True)

    def __repr__(self):
        return f'<Candidate {self.name} ({self.party})>'

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_name = db.Column(db.String(100), nullable=False, unique=True)  # prevent duplicate voter by unique voter_name
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)

    def __repr__(self):
        return f'<Vote by {self.voter_name} for candidate {self.candidate_id}>'
