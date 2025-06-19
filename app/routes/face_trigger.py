from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app.models.attendance import Attendance
from app import db

from face_module.run import recognize_face_from_image
from PIL import Image
import base64
import io
import subprocess
from app.services.face_state import detector, recognizer, targets, colors
from face_module.service.frame_processor import frame_processor

face_trigger_bp = Blueprint('face_trigger', __name__)

@face_trigger_bp.route('/api/face_recognition', methods=['POST'])
@login_required
def api_face_recognition():
    data = request.json
    img_data = data.get('image')
    employee_code = current_user.employee_code  # ✅ sửa ở đây
    user_id = current_user.id

    if not img_data:
        return jsonify({'success': False, 'message': 'No image provided'}), 400

    try:
        img_bytes = base64.b64decode(img_data.split(',')[1])
        img = Image.open(io.BytesIO(img_bytes))

        result = recognize_face_from_image(img, employee_code)  # ✅ so sánh với mã nhân viên
        now = datetime.now().replace(microsecond=0)
        today = now.date()

        if result:
            record = Attendance.query.filter_by(user_id=user_id, date=today).first()
            if not record:
                new_record = Attendance(user_id=user_id, date=today, check_in=now)
                db.session.add(new_record)
                db.session.commit()
                return jsonify({'success': True, 'message': "✅ Check-in thành công!"})
            elif not record.check_out:
                record.check_out = now
                if record.check_in:
                    duration = record.check_out - record.check_in
                    record.total_hours = round(duration.total_seconds() / 3600, 2)
                db.session.commit()
                return jsonify({'success': True, 'message': "✅ Check-out thành công!"})
            else:
                return jsonify({'success': True, 'message': "✅ Đã chấm công đầy đủ hôm nay."})
        else:
            return jsonify({'success': False, 'message': "❌ Nhận diện thất bại. Không ghi chấm công."})

    except Exception as e:
        return jsonify({'success': False, 'message': f"⚠️ Lỗi khi nhận diện: {str(e)}"}), 500

@face_trigger_bp.route('/chamcong/face')
@login_required
def chamcong_face():
    employee_code = current_user.employee_code  # ✅ sửa ở đây
    user_id = current_user.id

    try:
        # Chạy subprocess với employee_code
        result = subprocess.run(
            ['python', 'face_module/run.py', employee_code],
            check=False
        )

        now = datetime.now().replace(microsecond=0)
        today = now.date()

        if result.returncode == 0:
            record = Attendance.query.filter_by(user_id=user_id, date=today).first()

            if not record:
                db.session.add(Attendance(user_id=user_id, date=today, check_in=now))
                db.session.commit()
                flash("✅ Chúc bạn một ngày làm việc hiệu quả!")

            elif not record.check_out:
                record.check_out = now
                if record.check_in:
                    duration = record.check_out - record.check_in
                    record.total_hours = round(duration.total_seconds() / 3600, 2)
                db.session.commit()
                flash("✅ Check-out thành công!")

            else:
                flash("✅ Đã chấm công đầy đủ hôm nay.")

        else:
            flash("❌ Nhận diện thất bại. Không ghi chấm công.")

    except Exception as e:
        flash("⚠️ Lỗi khi gọi AI nhận diện: " + str(e))

    return redirect(url_for('attendance.bang_cham_cong_ngay'))
