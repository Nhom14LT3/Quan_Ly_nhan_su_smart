from app import db
from datetime import datetime

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    date = db.Column(db.Date, default=datetime.utcnow().date)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)
    total_hours = db.Column(db.Float, default=0)  # số giờ làm trong ngày
    ot_hours = db.Column(db.Float, nullable=True, default=0.0)  # ✅ thêm trường tăng ca
    user = db.relationship('User', backref='attendance_records')
