import torch
import onnxruntime
from face_module.c.cConst import Const
from face_module.models.arcface import ArcFace
from face_module.models.scrfd import SCRFD
import os
var = Const()

def load_model():
    print("📂 Loading model from:", var.det_weight)
    print("📂 File exists?", os.path.exists(var.det_weight))
    # Sử dụng GPU với ONNX Runtime
    detector_session = onnxruntime.InferenceSession(var.det_weight, providers=['CPUExecutionProvider'])
    recognizer_session = onnxruntime.InferenceSession(var.rec_weight, providers=['CPUExecutionProvider'])
    
    detector = SCRFD(session=detector_session, model_path=var.det_weight, input_size=(640, 640), conf_thres=var.confidence_thresh)
    recognizer = ArcFace(session=recognizer_session)
    

    return detector, recognizer
