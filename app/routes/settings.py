from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.utils.render_with_role_layout import render_with_role

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not check_password_hash(current_user.password, old_password):
            flash("Mật khẩu cũ không đúng.", "danger")
        elif new_password != confirm_password:
            flash("Mật khẩu mới và xác nhận không khớp.", "danger")
        else:
            current_user.password = generate_password_hash(new_password)
            db.session.commit()
            flash("Cập nhật mật khẩu thành công.", "success")
            return redirect(url_for('settings.change_password'))

    return render_with_role('settings/change_password.html')
