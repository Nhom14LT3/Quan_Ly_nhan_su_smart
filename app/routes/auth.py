from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app.models.user import User
from app import db
from app.utils.render_with_role_layout import render_with_role
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('dashboard.root'))
        else:
            flash('Sai tài khoản hoặc mật khẩu.', 'danger')

    return render_with_role('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đã đăng xuất.', 'info')
    return redirect(url_for('auth.login'))
