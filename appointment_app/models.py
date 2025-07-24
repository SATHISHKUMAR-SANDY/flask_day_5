from app import db
from datetime import time, date

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Confirmed, Canceled

    def __repr__(self):
        return f"<Appointment {self.name} on {self.date} at {self.time}>"
