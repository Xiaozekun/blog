import os
import click

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
from flask_login import current_user

from blog.blueprints.admin import admin_bp
from blog.blueprints.blog import blog_bp
from blog.blueprints.auth import auth_bp
from blog.extensions import db, csrf, bootstrap, ckeditor, moment, mail, login_manager, migrate
from blog.settings import config
from blog.models import Admin, Category, Comment
from blog.fakes import fake_admin, fake_categories, fake_posts, fake_comments


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLAKS_ENV', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_template_context(app)
    register_errors(app)
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
    login_manager.init_app(app)
    migrate.init_app(app, db)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete teh database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

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

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    # @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
    #               help='The password used to login.')
    @click.password_option()
    def init(username, password):
        click.echo('Initializing the database...')
        db.create_all()
        admin = Admin.query.first()
        if admin:
            click.echo('The admin already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary admin account...')
            admin = Admin(
                username='admin',
                name='Xiaozekun',
                about='编程工程师',
                blog_title='我的BLOG',
                blog_sub_title='lihfts'
            )
            admin.set_password(password)
            db.session.add(admin)
        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='default')
            db.session.add(category)
        db.session.commit()
        click.echo('Done')


def register_template_context(app):
    @app.context_processor
    def make_template_contest():
        admin = Admin.query.first()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, unread_comments=unread_comments)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400
