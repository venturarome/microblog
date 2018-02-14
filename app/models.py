from datetime import datetime
from app import db

# Check documentation: http://flask-sqlalchemy.pocoo.org/2.3/

# NOTE: do not forget to add the new model to rafafdez.py!!!

class User(db.Model):
    # Table name:
    __tablename__ = 'user'

    # Table columns:
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Relationships with other tables:
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    # How a row will be printed:
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.id)

