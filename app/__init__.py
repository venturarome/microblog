from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Create the application object as an instance of class 'Flask'
app = Flask(__name__)	# This is the 'app' VARIABLE. It is a member of the 'app' PACKAGE.
app.config.from_object(Config)

# Add plugins core objects
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'tutologin'	# Could this be added to the Config object as well?

# Workaround to avoid circular imports. Import those modules which need to import the 'app' variable. Those modules (created by us) come from the 'app' PACKAGE.
from app import routes, models    # valdría tambien from . import routes??

