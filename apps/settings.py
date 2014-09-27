"""
settings.py

Configuration for Flask app

"""
import os
from datetime import timedelta


class Config(object):
    # Set secret key to use session
    SECRET_KEY = "glouniv"
    debug = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=2)


class Production(Config):
    debug = True
    CSRF_ENABLED = False
    ADMIN = "charmcathy@gmail.com"
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///glouniv?instance=causal-shell-662:mjuexamlikelion2'
    migration_directory = 'migrations'
