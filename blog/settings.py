import os, sys


class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BLOG_POST_PER_PAGE = 10
    BLOG_COMMENT_PER_PAGE = 10

    BLOG_EMAIL = 'xiaozekun2012@gmail.com'

    BLOG_THEMES = {'perfect_blue': 'Perfect Blue',
                   'black_swan': 'Black Swan'}

    BLOG_MANAGE_POST_PER_PAGE = 20
    BLOG_MANAGE_COMMENT_PER_PAGE = 50


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig():
    pass


class TestingConfig():
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
