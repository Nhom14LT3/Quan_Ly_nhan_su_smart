# c/cConst.py

import os

class Const:
    det_weight = r".\face_module\weights\det_10g.onnx"
    rec_weight = r".\face_module\weights\w600k_r50.onnx"
    faces_dir = r".\app\static\faces"
    output_images_dir = r".\face_module\output_images"
    max_num = 1
    similarity_thresh = 0.5
    confidence_thresh = 0.6