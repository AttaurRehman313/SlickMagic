from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, primary_key=True)
    video_link = db.Column(db.String(100), nullable=True)
    count = db.Column(db.String(100), nullable=True)
    script = db.Column(db.String(500), nullable=False)
