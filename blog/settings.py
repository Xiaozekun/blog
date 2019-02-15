import os, sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    BLOG_POST_PER_PAGE = 10
    BLOG_COMMENT_PER_PAGE = 10

    BLOG_EMAIL = 'xiaozekun2012@gmail.com'

    BLOG_THEMES = {'perfect_blue': 'Perfect Blue',
                   'black_swan': 'Black Swan'}

    BLOG_MANAGE_POST_PER_PAGE = 20
    BLOG_MANAGE_COMMENT_PER_PAGE = 50

    BLOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    BLOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


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
