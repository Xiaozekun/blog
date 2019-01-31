import os

from  flask import Flask

from blog.blueprints.admin import admin_bp
from blog.blueprints.blog import blog_bp
from blog.blueprints.auth import auth_bp
from blog.extensions import db, csrf, bootstrap, ckeditor, moment, mail
from blog.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLAKS_ENV','development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_blueprints(app)
    register_extensions(app)
    return app

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(blog_bp)

def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)