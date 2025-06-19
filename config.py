import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cấu hình dành cho face_module
    FACES_DIR = os.path.join(basedir, 'face_module', 'faces')
    MAX_FACES = 5
    SIMILARITY_THRESH = 0.5

    # Thời gian hết phiên đăng nhập
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
