from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    updated_on = db.Column(
        db.DateTime,
        default=datetime.utcnow,       # Set when item is created
        onupdate=datetime.utcnow       # Auto-update when item is edited
    )

    def __repr__(self):
        return f"<Item {self.name} - Qty: {self.quantity}>"
