import os, sys

class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret)key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BLOG_POST_PER_PAGE=10

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig():
    pass

class TestingConfig():
    pass

config ={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production': ProductionConfig
}