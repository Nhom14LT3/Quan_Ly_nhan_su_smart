from flask import Blueprint
from app.models.attendance import Attendance
from datetime import date
from app.models.user import User
from app.utils.render_with_role_layout import render_with_role
from flask import Blueprint, request, send_file, flash

from flask_login import current_user
from calendar import monthrange
from app import db
from app.decorators.role_required import role_required
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/chamcong')
def bang_cham_cong_ngay():
    today = date.today()

    recs = Attendance.query.filter_by(date=today).all()

    # Chỉ giữ lại bản ghi mà employee_code trùng
    records = []
    for r in recs:
        if r.user and r.user.employee_code == current_user.employee_code:
            records.append({
                'id': r.id,
                'name': r.user.username,
                'date': r.date.strftime('%Y-%m-%d'),
                'check_in': r.check_in.strftime('%H:%M:%S') if r.check_in else '',
                'check_out': r.check_out.strftime('%H:%M:%S') if r.check_out else '',
                'total_hours': r.total_hours or ''
            })

    return render_with_role('attendance/bang_cham_cong_ngay.html', records=records)

@attendance_bp.route('/chamcong/tongket')
def tongket_cham_cong_thang():

    # Nhận tháng/năm từ form GET
    month = int(request.args.get('month', datetime.now().month))
    year = int(request.args.get('year', datetime.now().year))
    total_days = monthrange(year, month)[1]

    summaries = []
    for u in User.query.all():
        recs = Attendance.query.filter_by(user_id=u.id).filter(
            Attendance.date.between(date(year, month, 1), date(year, month, total_days))
        ).all()
        days_worked = len([r for r in recs if r.check_in])
        total_hours = sum([r.total_hours or 0 for r in recs])
        summaries.append({
            'name': u.username,
            'days_worked': days_worked,
            'total_hours': total_hours,
            'days_absent': total_days - days_worked
        })

    return render_with_role('attendance/bang_cham_cong_thang_tong_ket.html', summaries=summaries, month=month, year=year)

@attendance_bp.route('/chamcong/tongket/export')
def export_excel():
    import pandas as pd
    from io import BytesIO
    from flask import send_file

    month = int(request.args.get('month', datetime.now().month))
    year = int(request.args.get('year', datetime.now().year))

    from calendar import monthrange
    total_days = monthrange(year, month)[1]

    data = []
    for u in User.query.all():
        recs = Attendance.query.filter_by(user_id=u.id).filter(
            Attendance.date.between(date(year, month, 1), date(year, month, total_days))
        ).all()
        days_worked = len([r for r in recs if r.check_in])
        total_hours = sum([r.total_hours or 0 for r in recs])
        days_absent = total_days - days_worked
        data.append({
            'Tên nhân viên': u.username,
            'Số ngày làm': days_worked,
            'Số giờ công': total_hours,
            'Số ngày vắng': days_absent
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='TongKet')
    output.seek(0)
    return send_file(output, download_name=f"tongket_{month}_{year}.xlsx", as_attachment=True)
@attendance_bp.route('/chamcong/nam')
@role_required('admin', 'manager')
def tong_hop_nam():
    year = int(request.args.get('year', datetime.now().year))
    users = User.query.all()

    summary = []
    for user in users:
        user_summary = {'name': user.username, 'employee_code': user.employee_code, 'months': []}
        for month in range(1, 13):
            total = Attendance.query.filter(
                Attendance.user_id == user.id,
                Attendance.date.between(date(year, month, 1), date(year, month, monthrange(year, month)[1]))
            ).count()
            user_summary['months'].append({
                'month': month,
                'count': total
            })
        summary.append(user_summary)

    return render_with_role('attendance/tong_hop_nam.html', summary=summary, year=year)


@attendance_bp.route('/chamcong/view-month-detail/<string:employee_code>/<int:month>')
@role_required('admin', 'manager')
def view_month_detail(employee_code, month):
    year = datetime.now().year
    user = User.query.filter_by(employee_code=employee_code).first_or_404()
    days = Attendance.query.filter(
        Attendance.user_id == user.id,
        Attendance.date.between(date(year, month, 1), date(year, month, monthrange(year, month)[1]))
    ).order_by(Attendance.date).all()

    return render_with_role('attendance/chi_tiet_thang.html', user=user, days=days, month=month, year=year)

@attendance_bp.route('/chamcong/chi-tiet/<string:employee_code>/<int:month>')
@role_required('admin', 'manager')
def chi_tiet_cham_cong_thang(employee_code, month):
  

    year = datetime.now().year
    total_days = monthrange(year, month)[1]

    # Lấy thông tin người dùng
    from app.models.user import User
    user = User.query.filter_by(employee_code=employee_code).first_or_404()

    # Lấy danh sách chấm công trong tháng
    from app.models.attendance import Attendance
    records = Attendance.query.filter_by(user_id=user.id).filter(
        Attendance.date.between(date(year, month, 1), date(year, month, total_days))
    ).order_by(Attendance.date.asc()).all()

    return render_with_role('attendance/bang_cham_cong_chi_tiet.html', user=user, records=records, month=month, year=year)
@attendance_bp.route('/chamcong/edit/<int:id>', methods=['GET', 'POST'])
@role_required('admin', 'manager')
def edit_attendance(id):
  

    record = Attendance.query.get_or_404(id)
    user = record.user
    month = record.date.month
    year = record.date.year

    if request.method == 'POST':
        try:
            record.check_in = datetime.strptime(request.form['check_in'], '%Y-%m-%dT%H:%M') if request.form['check_in'] else None
            record.check_out = datetime.strptime(request.form['check_out'], '%Y-%m-%dT%H:%M') if request.form['check_out'] else None
            record.ot_hours = float(request.form['ot_hours']) if request.form['ot_hours'] else 0.0

            if record.check_in and record.check_out:
                duration = record.check_out - record.check_in
                record.total_hours = round(duration.total_seconds() / 3600, 2)
            else:
                record.total_hours = None

            db.session.commit()
            flash("✔️ Cập nhật thành công!")
            return redirect(url_for('attendance.chi_tiet_cham_cong_thang', employee_code=user.employee_code, month=month))

        except Exception as e:
            flash("❌ Lỗi: " + str(e))

    return render_with_role('attendance/form_edit_attendance.html', record=record)
@attendance_bp.route('/chamcong/delete/<int:id>', methods=['POST'])
@role_required('admin', 'manager')
def delete_attendance(id):
    record = Attendance.query.get_or_404(id)
    user = record.user
    month = record.date.month

    try:
        db.session.delete(record)
        db.session.commit()
        flash("🗑️ Xóa bản ghi thành công!")
    except Exception as e:
        flash("❌ Lỗi khi xóa: " + str(e))

    return redirect(url_for('attendance.chi_tiet_cham_cong_thang', employee_code=user.employee_code, month=month))
