from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Danh sách user mặc định
    default_users = [
        {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
        {'username': 'hoangnguyen', 'password': 'hoang123', 'role': 'manager'},
        {'username': 'ngoc2106', 'password': 'ngoc123', 'role': 'employee'},
    ]

    for index, user_data in enumerate(default_users, start=1):
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if not existing_user:
            user = User(
                username=user_data['username'],
                role=user_data['role'],
                employee_code=f"25{index:04d}",
                avatar="default.jpg"
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            print(f"✅ Tạo tài khoản {user_data['username']} thành công.")
        else:
            # ✅ Cập nhật nếu thiếu mã hoặc avatar
            updated = False
            if not existing_user.employee_code:
                existing_user.employee_code = f"25{index:04d}"
                updated = True
            if not existing_user.avatar:
                existing_user.avatar = "default.jpg"
                updated = True
            if updated:
                print(f"🔄 Cập nhật tài khoản {existing_user.username} (mã hoặc avatar).")
            else:
                print(f"⚠️ Tài khoản {user_data['username']} đã tồn tại đầy đủ.")

    db.session.commit()
