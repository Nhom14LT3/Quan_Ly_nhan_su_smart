
from app import db
class PendingEmployeeInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # MaNV = db.Column(db.String(10), db.ForeignKey('user.employee_code'))
    MaNV = db.Column(db.String(10))
    TenNV = db.Column(db.String(100))
    SDT = db.Column(db.String(20))
    Email = db.Column(db.String(100))
    NgaySinh = db.Column(db.String(20))
    GioiTinh = db.Column(db.String(10))
    NoiSinh = db.Column(db.String(100))
    QuocTich = db.Column(db.String(50))
    TrangThai = db.Column(db.String(20), default='cho_duyet')  # 'cho_duyet', 'da_duyet', 'tu_choi'
