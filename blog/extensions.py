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
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = u'请先登录'


@login_manager.user_loader
def load_user(user_id):
    from blog.models import Admin
    user = Admin.query.get(int(user_id))
    return user
