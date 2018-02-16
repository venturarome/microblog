import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Related to cryptographic signs (cookies and some extensions require this).
    SECRET_KEY = os.environ.get('SECRET_KEY') or '6w_pyHQhb4A-KL%bq7kZAq~sq.H7R/Ya'
    # Database config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABSE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 'Remember me' login functionality
    REMEMBER_COOKIE_DURATION = 43200  # Value in seconds (43200s = 12h)
