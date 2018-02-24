from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from app.search import add_to_index, remove_from_index, query_index


# Check documentation: http://flask-sqlalchemy.pocoo.org/2.3/

# NOTE: do not forget to add the new model to microblog.py!!!

# This is just a table (no data model), as it does not contain more than foreign keys.
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model): # Here, UserMixin is added so the flask-login module can add functionality to the class.
    # Table name:
    __tablename__ = 'user'

    # Table columns:
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(256))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships with other models/tables:
    #     # 'User' is the right side entity
    #     # Condition  that links the left side entity with the association table.
    #     # how the relationship will be accessed from the right side entity.
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    followed = db.relationship('User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic')

    # How a row will be printed:
    def __repr__(self):
        return '<User {}>'.format(self.username)


    # Set password (hashing it before):
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify if a pasword and a hash match:
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Retrieve or create an avatar:
    def avatar(self, size=64):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    # Followers feature:
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # Returns the comments from followed users (+ own), sorted in descending chronological order (newest first)
    def followed_comments(self):
        followed = ( Comment.query.
            join(followers, (followers.c.followed_id == Comment.user_id)).
                filter(followers.c.follower_id == self.id))
        own = Comment.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Comment.timestamp.desc())

    # Reset password. Creates a token.
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # Side note: Static methods are like class methods, but they don receive 'self' as first argument.
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)


# Because Flask-Login knows nothing about databases, it needs the application's help in loading a user. For that reason, the extension expects that the application will configure a user loader function, that can be called to load a user given the ID.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


############################################    
    
# Allows integration with the full-text search feature, and eases synchronization among both.
class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        # Wrapper for the query_index() function from app/search.py. It replaces id's by actual objects.
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total
    
    @classmethod
    def before_commit(cls, session):
        # Triggered thanks to SQLAlchemy events, before a commit is performed.
        session._changes = {
            'add': [obj for obj in session.new if isinstance(obj, cls)],
            'update': [obj for obj in session.dirty if isinstance(obj, cls)],
            'delete': [obj for obj in session.deleted if isinstance(obj, cls)]
        }
        
    @classmethod
    def after_commit(cls, session):
        # Triggered thanks to SQLAlchemy events, after a commit is performed.
        for obj in session._changes['add']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['update']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['delete']:
            remove_from_index(cls.__tablename__, obj)
        session._changes = None
        
    @classmethod
    def reindex(cls):
        # Initialize the index from all the elements of the model currently in the database(ie. Comment.reindex())
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


class Comment(SearchableMixin, db.Model):
    __tablename__ = 'comment'
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))
    
    def __repr__(self):
        return '<Comment {}>'.format(self.id)

# Hooks for listening to events coming from SQLAlchemy:
db.event.listen(db.session, 'before_commit', Comment.before_commit)
db.event.listen(db.session, 'after_commit', Comment.after_commit)    
    
