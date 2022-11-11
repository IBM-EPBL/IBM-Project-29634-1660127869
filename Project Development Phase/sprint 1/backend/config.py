from dotenv import load_dotenv
load_dotenv()

import os

basedir = os.path.abspath(os.path.dirname(__file__))

CONFIG_OBJECT_NAME = os.getenv('CONFIG_OBJECT_NAME', 'config.DevelopmentConfig')

class Config():
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_VERSION_PREFIX = os.getenv('API_VERSION_PREFIX', '/api/v1/')


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "app.db")}'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')
