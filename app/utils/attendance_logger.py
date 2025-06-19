from datetime import datetime, date
from app import db
from app.models.attendance import Attendance
from app.models.user import User

def record_attendance(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return False

    today = date.today()
    now = datetime.now()

    rec = Attendance.query.filter_by(user_id=user.id, date=today).first()
    if not rec:
        # first scan → check-in
        rec = Attendance(user_id=user.id, date=today, check_in=now.time())
        db.session.add(rec)
    else:
        # subsequent scans → check-out
        rec.check_out = now.time()
        delta = datetime.combine(today, rec.check_out) - datetime.combine(today, rec.check_in)
        rec.total_hours = round(delta.seconds / 3600, 2)

    db.session.commit()
    return True
