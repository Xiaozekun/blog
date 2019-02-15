from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
migrate = Migrate()
loginmanager = LoginManager()
loginmanager.login_view = 'auth.login'


@loginmanager.user_loader
def load_user(user_id):
    from blog.models import Admin
    user = Admin.query.get(int(user_id))
    return user
