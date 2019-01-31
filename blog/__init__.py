from  flask import Flask

from blog.settings import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    return app

