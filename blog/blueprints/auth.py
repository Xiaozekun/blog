from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user, login_required

from blog.models import Admin
from blog.utils import redirect_back
from blog.forms import LoginForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form['username'].data
        password = form['password'].data
        remember = form['remember'].data
        admin = Admin.query.first()
        if admin:
            if admin.username == username and admin.check_password(password):
                flash('Login successfully', 'info')
                login_user(user=admin, remember=remember)
                return redirect_back()
            else:
                flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()

