from flask import Blueprint, redirect, url_for
from flask_login import current_user

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.root'))  # nếu đã login → dashboard
    else:
        return redirect(url_for('auth.login'))       # nếu chưa login → login
