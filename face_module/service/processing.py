import os
import cv2
import numpy as np
import glob
from typing import List, Tuple

def build_targets(detector, recognizer, faces_dir) -> List[Tuple[np.ndarray, str]]:
    targets = []

    # Duyệt đệ quy toàn bộ ảnh .jpg và .png
    image_paths = glob.glob(os.path.join(faces_dir, '**', '*.jpg'), recursive=True)
    image_paths += glob.glob(os.path.join(faces_dir, '**', '*.png'), recursive=True)

    for image_path in image_paths:
        filename = os.path.basename(image_path)
        name = os.path.splitext(filename)[0]  # ví dụ: 250001 từ 250001.jpg

        image = cv2.imread(image_path)
        if image is None:
            print(f"[!] Lỗi đọc ảnh: {image_path}")
            continue

        bboxes, kpss = detector.detect(image, max_num=1)

        if len(kpss) == 0:
            print(f"[!] Không phát hiện khuôn mặt trong: {image_path}")
            continue

        embedding = recognizer(image, kpss[0])
        targets.append((embedding, name))

    return targets
