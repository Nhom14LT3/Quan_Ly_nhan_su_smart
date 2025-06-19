
from flask import Blueprint, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.decorators.role_required import role_required
from app.utils.render_with_role_layout import render_with_role
from app.models.employee import EmployeeInfo, PendingEmployeeInfo
from datetime import datetime
from app import db
from io import BytesIO
import pandas as pd
from flask import send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from io import BytesIO

infor_employee_bp = Blueprint('infor_employee', __name__, url_prefix='/ttnhanvien')


@infor_employee_bp.route('/')
@login_required
def thong_tin_nhan_vien():
    ma_nv = current_user.employee_code
    thong_tin = EmployeeInfo.query.filter_by(MaNV=ma_nv).first()
    return render_with_role('employee/thongtinnhanvien.html', thong_tin=thong_tin)


@infor_employee_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_employee_info():
    if request.method == 'POST':
        existing_pending = PendingEmployeeInfo.query.filter_by(MaNV=current_user.employee_code).first()
        if existing_pending:
            flash("Bạn đã gửi yêu cầu trước đó, vui lòng chờ phê duyệt.")
            return redirect(url_for('infor_employee.thong_tin_nhan_vien'))

        pending = PendingEmployeeInfo(
            MaNV=current_user.employee_code,
            TenNV=request.form['TenNV'],
            SDT=request.form['SDT'],
            Email=request.form['Email'],
            NgaySinh=datetime.strptime(request.form['NgaySinh'], '%Y-%m-%d').date(),
            Gioitinh=request.form['Gioitinh'],
            NoiSinh=request.form['NoiSinh'],
            QuocTich=request.form['QuocTich'],
            MAHD=request.form.get('MAHD'),
            MaPB=request.form.get('MaPB'),
            MaCV=request.form.get('MaCV'),
            Luong=request.form.get('Luong')
        )
        db.session.add(pending)
        db.session.commit()
        flash("Thông tin đã được gửi, chờ phê duyệt.")
        return redirect(url_for('infor_employee.thong_tin_nhan_vien'))

    return render_with_role('employee/form_add_employee.html', thong_tin=None)


@infor_employee_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update_employee_info():
    existing = EmployeeInfo.query.filter_by(MaNV=current_user.employee_code).first()
    if not existing:
        flash("Chưa có thông tin nhân viên.")
        return redirect(url_for('infor_employee.add_employee_info'))

    if request.method == 'POST':
        existing_pending = PendingEmployeeInfo.query.filter_by(MaNV=current_user.employee_code).first()
        if existing_pending:
            flash("Bạn đã gửi yêu cầu cập nhật trước đó, vui lòng chờ phê duyệt.")
            return redirect(url_for('infor_employee.thong_tin_nhan_vien'))

        pending = PendingEmployeeInfo(
            MaNV=current_user.employee_code,
            TenNV=request.form['TenNV'],
            SDT=request.form['SDT'],
            Email=request.form['Email'],
            NgaySinh=datetime.strptime(request.form['NgaySinh'], '%Y-%m-%d').date(),
            Gioitinh=request.form['Gioitinh'],
            NoiSinh=request.form['NoiSinh'],
            QuocTich=request.form['QuocTich'],
            MAHD=request.form.get('MAHD'),
            MaPB=request.form.get('MaPB'),
            MaCV=request.form.get('MaCV'),
            Luong=request.form.get('Luong')
        )
        db.session.merge(pending)  # nếu đã gửi rồi thì cập nhật
        db.session.commit()
        flash("Thông tin cập nhật đã được gửi và chờ duyệt.")
        return redirect(url_for('infor_employee.thong_tin_nhan_vien'))

    return render_with_role('employee/form_update_employee.html', thong_tin=existing)


@infor_employee_bp.route('/pending')
@login_required
@role_required('admin', 'manager')
def pending_approval():
    danh_sach = PendingEmployeeInfo.query.all()
    return render_with_role('employee/pending_list.html', danh_sach=danh_sach)


@infor_employee_bp.route('/approve/<string:MaNV>', methods=['POST'])
@login_required
@role_required('admin', 'manager')
def approve_employee(MaNV):
    pending = PendingEmployeeInfo.query.filter_by(MaNV=MaNV).first()
    if pending:
        existing = EmployeeInfo.query.filter_by(MaNV=MaNV).first()
        if existing:
            db.session.delete(existing)
        approved = EmployeeInfo(
            MaNV=pending.MaNV,
            TenNV=pending.TenNV,
            SDT=pending.SDT,
            Email=pending.Email,
            NgaySinh=pending.NgaySinh,
            Gioitinh=pending.Gioitinh,
            NoiSinh=pending.NoiSinh,
            QuocTich=pending.QuocTich,
            MAHD=pending.MAHD,
            MaPB=pending.MaPB,
            MaCV=pending.MaCV,
            Luong=pending.Luong
        )
        db.session.add(approved)
        db.session.delete(pending)
        db.session.commit()
        flash(f"Đã phê duyệt thông tin cho {approved.TenNV}")
    return redirect(url_for('infor_employee.pending_approval'))


@infor_employee_bp.route('/reject/<string:MaNV>', methods=['POST'])
@login_required
@role_required('admin', 'manager')
def reject_employee(MaNV):
    pending = PendingEmployeeInfo.query.filter_by(MaNV=MaNV).first()
    if pending:
        db.session.delete(pending)
        db.session.commit()
        flash(f"Đã từ chối thông tin của {pending.TenNV}")
    return redirect(url_for('infor_employee.pending_approval'))


@infor_employee_bp.route('/list')
@login_required
@role_required('admin', 'manager')
def list_all_employees():
    query = request.args.get('query', '').strip()
    if query:
        danh_sach = EmployeeInfo.query.filter(EmployeeInfo.MaNV.contains(query)).all()
    else:
        danh_sach = EmployeeInfo.query.all()

    pending_count = PendingEmployeeInfo.query.count()
    return render_with_role('employee/employee_list.html', danh_sach=danh_sach, pending_count=pending_count)

@infor_employee_bp.route('/detail/<string:MaNV>', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'manager')
def view_employee_detail(MaNV):
    emp = EmployeeInfo.query.filter_by(MaNV=MaNV).first_or_404()
    if request.method == 'POST':
        emp.TenNV = request.form['TenNV']
        emp.SDT = request.form['SDT']
        emp.Email = request.form['Email']
        emp.Gioitinh = request.form['Gioitinh']
        emp.NoiSinh = request.form['NoiSinh']
        emp.NgaySinh = datetime.strptime(request.form['NgaySinh'], '%Y-%m-%d').date()
        emp.QuocTich = request.form['QuocTich']
        emp.MAHD = request.form['MAHD']
        emp.MaPB = request.form['MaPB']
        emp.MaCV = request.form['MaCV']
        emp.Luong = request.form['Luong']
        db.session.commit()
        flash("Cập nhật thành công.")
        return redirect(url_for('infor_employee.list_all_employees'))

    return render_with_role('employee/form_update_employee.html', thong_tin=emp)


@infor_employee_bp.route('/export')
@login_required
@role_required('admin', 'manager')
def export_employees():
    data = EmployeeInfo.query.all()
    df = pd.DataFrame([{
        'MaNV': nv.MaNV,
        'TenNV': nv.TenNV,
        'Email': nv.Email,
        'SDT': nv.SDT,
        'MaCV': nv.MaCV,
        'MaPB': nv.MaPB
    } for nv in data])

    output = BytesIO()
    df.to_excel(output, index=False, sheet_name='DanhSachNhanVien')
    output.seek(0)

    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     download_name='ds_nhanvien.xlsx', as_attachment=True)




@infor_employee_bp.route('/export/pdf')
@login_required
@role_required('admin', 'manager')
def export_employees_pdf():
    buffer = BytesIO()

    # Landscape A4
    c = canvas.Canvas(buffer, pagesize=landscape(A4))

    # Đăng ký font tiếng Việt
    font_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'fonts', 'DejaVuSans.ttf')
    font_path = os.path.abspath(font_path)
    pdfmetrics.registerFont(TTFont('DejaVu', font_path))
    c.setFont("DejaVu", 14)
    
    # Vị trí bắt đầu
    x_start = 40
    y_start = 550

    # Tiêu đề chính
    c.drawCentredString(420, y_start + 60, "DANH SÁCH NHÂN VIÊN")

    # Cấu trúc bảng
    headers = ["Mã NV", "Họ tên", "Email", "SĐT", "Chức vụ", "Phòng ban"]
    col_widths = [70, 140, 220, 100, 90, 90]  # Tổng ~710
    x_positions = [x_start]
    for w in col_widths[:-1]:
        x_positions.append(x_positions[-1] + w)

    # Header
    c.setFont("DejaVu", 12)
    for i, header in enumerate(headers):
        c.drawString(x_positions[i], y_start, header)

    # Dữ liệu
    y = y_start - 30
    c.setFont("DejaVu", 11)
    data = EmployeeInfo.query.all()
    for nv in data:
        row = [
            nv.MaNV,
            nv.TenNV,
            nv.Email,
            nv.SDT,
            nv.MaCV,
            nv.MaPB
        ]
        for i, item in enumerate(row):
            c.drawString(x_positions[i], y, str(item))
        y -= 25
        if y < 50:
            c.showPage()
            y = y_start

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='ds_nhanvien.pdf'
    )


@infor_employee_bp.route('/search')
@login_required
@role_required('admin', 'manager')
def search_employee():
    query = request.args.get('query', '')
    danh_sach = EmployeeInfo.query.filter(EmployeeInfo.MaNV.contains(query)).all()
    return render_with_role('employee/employee_list.html', danh_sach=danh_sach)
@infor_employee_bp.route('/import', methods=['POST'])
@login_required
@role_required('admin', 'manager')
def import_employees():
    file = request.files['file']
    if not file.filename.endswith('.xlsx'):
        flash("Vui lòng chọn file Excel.")
        return redirect(url_for('infor_employee.list_all_employees'))

    df = pd.read_excel(file)
    for _, row in df.iterrows():
        if not EmployeeInfo.query.filter_by(MaNV=row['MaNV']).first():
            nv = EmployeeInfo(
                MaNV=row['MaNV'],
                TenNV=row['TenNV'],
                Email=row['Email'],
                SDT=row['SDT'],
                MaCV=row.get('MaCV'),
                MaPB=row.get('MaPB'),
                MAHD=row.get('MAHD'),
                Luong=row.get('Luong'),
                Da_duyet=True
            )
            db.session.add(nv)
    db.session.commit()
    flash("Import thành công.")
    return redirect(url_for('infor_employee.list_all_employees'))
@infor_employee_bp.route('/delete/<string:MaNV>', methods=['POST'])
@login_required
@role_required('admin', 'manager')
def delete_employee(MaNV):
    nv = EmployeeInfo.query.filter_by(MaNV=MaNV).first()
    if nv:
        db.session.delete(nv)
        db.session.commit()
        flash(f"Đã xóa nhân viên {nv.TenNV}")
    return redirect(url_for('infor_employee.list_all_employees'))
