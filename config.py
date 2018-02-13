import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or '6w_pyHQhb4A-KL%bq7kZAq~sq.H7R/Ya'

