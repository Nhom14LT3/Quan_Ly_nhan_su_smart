# app/services/face_state.py

from face_module.load_model import load_model
from face_module.c.cConst import Const
from face_module.service.processing import build_targets

# Load model 1 lần duy nhất
var = Const()
detector, recognizer = load_model()
targets = build_targets(detector, recognizer, var.faces_dir)

# Tạo dictionary màu (optional)
import random
colors = {name: tuple(random.randint(0, 255) for _ in range(3)) for _, name in targets}
