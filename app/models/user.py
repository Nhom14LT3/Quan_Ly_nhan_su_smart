from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):  # ✅ thêm UserMixin
    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(10), unique=True)

    # ✅ Quan hệ ngược lại
    employee_info = db.relationship("EmployeeInfo", back_populates="user", uselist=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(20), default = "default.jpg")
    role = db.Column(db.String(20), default='employee')  # admin / employee

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    @staticmethod
    def generate_employee_code():
        # Tìm mã nhân viên cao nhất đã từng được gán (dù những người trước đó đã bị xóa)
        last_user = User.query.order_by(User.employee_code.desc()).first()
        if last_user and last_user.employee_code.isdigit():
            new_code = str(int(last_user.employee_code) + 1)
        else:
            new_code = '250001'  # hoặc số bắt đầu mà bạn muốn

        return new_code

