from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    comitet = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
