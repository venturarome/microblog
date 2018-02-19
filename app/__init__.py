import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment


############################################################


# Create the application object as an instance of class 'Flask'
app = Flask(__name__)	# This is the 'app' VARIABLE. It is a member of the 'app' PACKAGE.
app.config.from_object(Config)

# Add plugins core objects
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


############################################################


# Configuration to send email in case of error
if not app.debug:
    # General config
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='MicroBlog Website Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)  # CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
        app.logger.addHandler(mail_handler)

    # Enable a file based log
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10) # Keep in storage a max of 10 logfiles, of a max of 10KB each.
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('MicroBlog startup')


############################################################
    
    
# Workaround to avoid circular imports. Import those modules which need to import the 'app' variable. Those modules (created by us) come from the 'app' PACKAGE.
from app import routes, models, errors    # valdría tambien from . import routes??

