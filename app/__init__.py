from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config



db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect nếu chưa login
login_manager.login_message = "Vui lòng đăng nhập để tiếp tục."

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Khởi tạo các extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Đăng ký các blueprint
    from app.routes.index import index_bp

    from app.routes.auth import auth_bp
    from app.routes.employee import employee_bp
    from app.routes.attendance import attendance_bp
    from app.routes.face_trigger import face_trigger_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.InforEmployee import infor_employee_bp
    from app.routes.gameboard import gameboard_bp
    from app.routes.settings import settings_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(employee_bp, url_prefix='/nhanvien')
    app.register_blueprint(attendance_bp)
    app.register_blueprint(face_trigger_bp)
    app.register_blueprint(infor_employee_bp)
    app.register_blueprint(gameboard_bp)
    app.register_blueprint(settings_bp)
    # Load user từ database cho Flask-Login
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
