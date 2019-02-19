import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    BLOG_POST_PER_PAGE = 10
    BLOG_COMMENT_PER_PAGE = 10

    BLOG_EMAIL = os.getenv('BLOG_EMAIL')

    BLOG_THEMES = {'perfect_blue': 'Perfect Blue',
                   'black_swan': 'Black Swan'}

    BLOG_MANAGE_POST_PER_PAGE = 20
    BLOG_MANAGE_COMMENT_PER_PAGE = 50

    BLOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    BLOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = ('Blog Admin', MAIL_USERNAME)


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass


class TestingConfig:
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
