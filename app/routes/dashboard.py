from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.utils.render_with_role_layout import render_with_role
from datetime import datetime
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def root():
    return render_with_role('dashboard.html')
