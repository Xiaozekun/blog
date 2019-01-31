import os
import click

from  flask import Flask

from blog.blueprints.admin import admin_bp
from blog.blueprints.blog import blog_bp
from blog.blueprints.auth import auth_bp
from blog.extensions import db, csrf, bootstrap, ckeditor, moment, mail, loginmanager, migrate
from blog.settings import config
from blog.models import Admin
from blog.fakes import fake_admin,fake_categories,fake_posts,fake_comments


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLAKS_ENV','development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_template_context(app)
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
    loginmanager.init_app(app)
    migrate.init_app(app,db)

def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate the fake categories, posts and commands."""
        db.drop_all()
        db.create_all()
        click.echo('Generating the admin...')
        fake_admin()
        click.echo('Generating the categories...')
        fake_categories(category)
        click.echo('Generating the posts...')
        fake_posts(post)
        click.echo('Generating the comment...')
        fake_comments(comment)
        click.echo('Done')


def register_template_context(app):
    @app.context_processor
    def make_template_contest():
        admin = Admin.query.first()
        return dict(admin=admin)