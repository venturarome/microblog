from flask import Flask
from config import Config

# Create the application object as an instance of class 'Flask'
app = Flask(__name__)	# This is the 'app' VARIABLE. It is a member of the 'app' PACKAGE.
app.config.from_object(Config)

# Workaround to avoid circular imports. Import those modules which need to import the 'app' variable. Those modules (created by us) come from the 'app' PACKAGE.
from app import routes	# ¿¿valdria tambien from . import routes??

