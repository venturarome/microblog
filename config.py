import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Related to cryptographic signs (cookies and some extensions require this).
    SECRET_KEY = os.environ.get('SECRET_KEY') or '6w_pyHQhb4A-KL%bq7kZAq~sq.H7R/Ya'
    # Database config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABSE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Email config:
    MAIL_SERVER = os.environ.get('MAIL_SERVER')                  # for gmail: smtp.goglemail.com
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)           # for gmail: 587
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None    # for gmail: 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')              # sender email username
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')              # sender email password
    ADMINS = ['contact.rafafdezjr@gmail.com']                    # receiver email

    # 'Remember me' login functionality
    REMEMBER_COOKIE_DURATION = 604800  # Value in seconds (604800s = 1w)
