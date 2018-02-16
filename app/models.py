from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Because Flask-Login knows nothing about databases, it needs the application's help in loading a user. For that reason, the extension expects that the application will configure a user loader function, that can be called to load a user given the ID.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))



# Check documentation: http://flask-sqlalchemy.pocoo.org/2.3/

# NOTE: do not forget to add the new model to rafafdez.py!!!

class User(UserMixin, db.Model): # Here, UserMixin is added so the flask-login module can add functionality to the class.
    # Table name:
    __tablename__ = 'user'

    # Table columns:
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Relationships with other tables:
    comments = db.relationship('Comment', backref='author', lazy='dynamic')


    # Set password (hashing it before):
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify if a pasword and a hash match:
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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

