import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

############################################################

# Add plugins core objects
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')   # The Flask-Login extension flashes a message in English any time it redirects the user to the login page. This message can be overriden, so we make sure that it gets translated using the _l() function for lazy processing.
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()

############################################################


def create_app(config_class=Config):
    # Create the application object as an instance of class 'Flask'
    app = Flask(__name__)	# This is the 'app' VARIABLE. It is a member of the 'app' PACKAGE.
    app.config.from_object(config_class)

    #Init the app on the already instantiated plugins.
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    # Blueprints. Imported here to avoid circular dependencies.
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    
    # Configuration to send email in case of error
    if not app.debug and not app.testing:
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
        
    return app

############################################################
    
# 'localselector' is a decorator included in the Babel class. The decorated function is invoked for each request to select a language translation to use for that request
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

############################################################

# Workaround to avoid circular imports. Import those modules which need to import the 'app' variable. Those modules (created by us) come from the 'app' PACKAGE.
from app import models
