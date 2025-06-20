# Human Resource Management System (HRMS)

## Mô tả dự án

Dự án xây dựng hệ thống quản lý nhân sự tích hợp các tính năng:
- Phân quyền theo vai trò: Admin, Manager, Employee
- Chấm công bằng nhận diện khuôn mặt sử dụng AI
- Gameboard điểm thưởng: theo dõi hiệu suất làm việc
- Giao diện web đơn giản, dễ mở rộng, có thể triển khai trên Render

---

## Tính năng chính

### 1. Phân quyền vai trò
- Admin: toàn quyền quản trị nhân sự, tài khoản, phê duyệt
- Manager: theo dõi nhân sự, duyệt thông tin
- Employee: chấm công, xem thông tin cá nhân và bảng điểm

### 2. Chấm công bằng khuôn mặt
- SCRFD: phát hiện khuôn mặt nhanh, nhẹ
- ArcFace: nhận diện khuôn mặt chính xác bằng embedding vector

### 3. Gameboard (trò chơi hóa hiệu suất)
- Điểm số dựa trên: chuyên cần, KPI, hoàn thành deadline
- Có bảng xếp hạng, level, huy hiệu để tạo động lực làm việc

---

## Yêu cầu hệ thống

- Python ≥ 3.9
- Anaconda hoặc Miniconda (khuyến nghị)
- Webcam (nếu test tính năng chấm công AI)

---

## Cài đặt & chạy

### Bước 1: Cài Anaconda (nếu chưa có)

Tải tại: https://www.anaconda.com/products/distribution

### Bước 2: Tạo môi trường ảo
conda create -n tenbanmuondat python=(bản mà bạn muốn cài)
VD:
```bash
conda create -n hrms python=3.9
conda activate hrms
```

### Bước 3: Tải source code và cài thư viện

```bash
git clone https://github.com/Group15N07/Quan_ly_nhan_su.git
cd Quan_ly_nhan_su
pip install -r requirements.txt
```

### Bước 4: Thêm file AI (nếu sử dụng nhận diện khuôn mặt)

Tải và đặt các file `.onnx` vào `face_module/weights/`:

- det_10g.onnx (SCRFD)
- w600k_r50.onnx (ArcFace)

### Bước 5: Chạy ứng dụng

```bash
# Windows
set FLASK_APP=run.py
set FLASK_ENV=development
flask run

# macOS/Linux
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

Truy cập trình duyệt: http://127.0.0.1:5000

---

## Tài khoản mẫu

| Role     | Username    | Password   |
|----------|-------------|------------|
| Admin    | admin       | admin123   |
| Manager  | manager     | manager123 |
| Employee | phuongbui   | phuong123  |

---

## Cấu trúc thư mục

Quan_ly_nhan_su/
├── app/               # Thư mục chính chứa logic ứng dụng Flask
│   ├── __init__.py    # Hàm create_app() để tạo Flask app
│   ├── routes/        # Các file routes Flask (phân chia module)
│   ├── models/        # Các model ORM (User, Attendance, ...)
│   ├── templates/     # Giao diện HTML (dùng Jinja2)
│   ├── static/        # CSS, JS, ảnh tĩnh
│   ├── decorators/    # Các decorator như @login_required, @role_required
│   ├── utils/         # Các hàm tiện ích (ví dụ xuất Excel, gửi mail)
│   └── services/      # Xử lý AI: nhận diện khuôn mặt, load model
│
├── face_module/       # Module AI nhận diện khuôn mặt
│   ├── load_model.py  # Load model SCRFD & ArcFace (.onnx)
│   └── weights/       # Các model AI dạng .onnx
│
├── config.py          # File cấu hình Flask
├── run.py             # File chạy Flask app
├── seed.py            # Seed dữ liệu mẫu vào database
├── requirements.txt   # Danh sách thư viện cần cài
├── Procfile           # Khai báo command chạy app trên Render/Heroku
├── database.db        # File SQLite database
└── README.md          # Hướng dẫn dự án


---

## Deployment

- Hệ thống có thể deploy dễ dàng trên [Render](https://render.com/)
- Sử dụng gunicorn để chạy production server
- Chỉ cần upload repo + bổ sung model `.onnx`

---

## Tài liệu & trình bày


---

## Liên hệ

Tác giả chính: Bùi Thế Phương 
Email: 23010097@st.phenikaa-uni.edu.vn  
GitHub: https://github.com/Nhom14LT3/Quan_Ly_nhan_su_smart


## Giấy phép

MIT License © Bùi Thế Phương – Phenikaa University
