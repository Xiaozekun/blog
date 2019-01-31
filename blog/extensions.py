from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_mail import Mail

db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()