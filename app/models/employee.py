from app import db
from app.models.user import User

class EmployeeInfo(db.Model):
    __tablename__ = 'employee_info'

    MaNV = db.Column(
    db.String(10),
    db.ForeignKey('user.employee_code', name='fk_employee_info_user'),
    primary_key=True
)

    TenNV = db.Column(db.String(100))
    SDT = db.Column(db.String(20))
    Email = db.Column(db.String(100))
    NgaySinh = db.Column(db.Date)
    Gioitinh = db.Column(db.String(10))
    NoiSinh = db.Column(db.String(100))
    QuocTich = db.Column(db.String(50))
    MAHD = db.Column(db.String(50))
    MaPB = db.Column(db.String(50))
    MaCV = db.Column(db.String(50))   # ✅ Sửa lại đúng tên
    Luong = db.Column(db.Float)
    Da_duyet = db.Column(db.Boolean, default=False)

    user = db.relationship("User", back_populates="employee_info", uselist=False)

    
class PendingEmployeeInfo(db.Model):
    __tablename__ = 'pending_employee_info'

    id = db.Column(db.Integer, primary_key=True)
    MaNV = db.Column(db.String(20), nullable=False, unique=True)
    TenNV = db.Column(db.String(100), nullable=False)
    SDT = db.Column(db.String(20))
    Email = db.Column(db.String(100))
    NgaySinh = db.Column(db.Date)
    Gioitinh = db.Column(db.String(10))
    NoiSinh = db.Column(db.String(100))
    QuocTich = db.Column(db.String(50))
    MAHD = db.Column(db.String(20))
    MaPB = db.Column(db.String(20))
    MaCV = db.Column(db.String(20))
    Luong = db.Column(db.Float)
