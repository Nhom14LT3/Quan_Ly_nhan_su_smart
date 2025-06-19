from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.user import User
from app.decorators.role_required import role_required
from app.utils.render_with_role_layout import render_with_role
from app.models import Attendance,EmployeeInfo
employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/')
def list_employee():
    users = User.query.all()
    return render_with_role('employee/list.html', users=users)

@employee_bp.route('/add', methods=['GET', 'POST'])
@role_required('admin', 'manager') 
def add_employee():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if User.query.filter_by(username=username).first():
            flash('Username đã tồn tại.')
        else:
            new_user = User(
                username=username,
                role=role,
                employee_code=User.generate_employee_code()  # ✅ sinh mã tự động
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Thêm nhân viên thành công. Mã nhân viên là {new_user.employee_code}')
            return redirect(url_for('employee.list_employee'))
    return render_with_role('employee/form_add.html')

@employee_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit_employee(id):
    u = User.query.get_or_404(id)
    if request.method=='POST':
        u.username = request.form['username']
        if request.form['password']:
            u.set_password(request.form['password'])
        u.role = request.form['role']
        db.session.commit()
        flash('Cập nhật thành công.')
        return redirect(url_for('employee.list_employee'))
    return render_with_role('employee/form_update.html', user=u)

@employee_bp.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    u = User.query.get_or_404(id)
    Attendance.query.filter_by(user_id=id).delete()
    user = EmployeeInfo.query.filter_by(employee_code= EmployeeInfo.MaNV).first()
    if EmployeeInfo.user:
        db.session.delete(EmployeeInfo.user)

    db.session.delete(EmployeeInfo)
    db.session.commit()
    flash('Xóa thành công.')
    return redirect(url_for('employee.list_employee'))
