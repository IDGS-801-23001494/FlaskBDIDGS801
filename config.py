import os

from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY = "ClaveSecreta"
    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLACHEWMY_DATABASE_URI = 'mysql+pymsql://root:root@127.0.0.1/flaskdb'
    ALCHEMY_TRACK_MODIFICATIONS = False