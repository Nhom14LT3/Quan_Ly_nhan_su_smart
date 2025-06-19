import os
import sys
import cv2
import random
from PIL import Image
import numpy as np

from face_module.load_model import load_model
from face_module.c.cConst import Const
from face_module.service.processing import build_targets
from face_module.service.frame_processor import frame_processor


def process_from_webcam_persistent(output_directory, allowed_code):
    """
    Mở webcam, phát hiện và nhận diện khuôn mặt.
    Trả về True nếu nhận diện đúng `allowed_code`, False nếu sai hoặc lỗi.
    """
    var = Const()
    detector, recognizer = load_model()
    targets = build_targets(detector, recognizer, var.faces_dir)
    colors = {name: tuple(random.randint(0, 255) for _ in range(3)) for _, name in targets}

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Không thể mở webcam.")
        return False

    result_flag = False
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Không đọc được frame.")
            break

        bboxes, _ = detector.detect(frame)
        if bboxes.shape[0] > 0:
            print(f"✅ Phát hiện {bboxes.shape[0]} khuôn mặt. Đang xử lý...")
            processed_img, detected_name = frame_processor(
                frame, detector, recognizer, targets, colors, var, output_directory
            )
            if detected_name == allowed_code:
                cv2.putText(frame, f"✅ {detected_name}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                result_flag = True
            else:
                cv2.putText(frame, "❌ Sai mã nhân viên", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            break

        cv2.imshow("Camera - Nhận diện khuôn mặt", frame)
        if cv2.waitKey(1) == 27:  # ESC để thoát
            break

    cap.release()
    cv2.destroyAllWindows()
    return result_flag


def recognize_face_from_image(image, allowed_username):
    from PIL import Image
    import numpy as np
    import cv2

    from app.services.face_state import detector, recognizer, targets, colors, var

    # Chuyển ảnh PIL sang numpy
    if isinstance(image, Image.Image):
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    else:
        frame = image

    processed_img, detected_name = frame_processor(
        frame, detector, recognizer, targets, colors, var, var.output_images_dir
    )
    print(f"[DEBUG] Mong đợi: {allowed_username} - Nhận diện: {detected_name}")
    return detected_name == allowed_username


def main():
    if len(sys.argv) != 2:
        print("⚠️ Vui lòng truyền mã nhân viên: python run.py <employee_code>")
        sys.exit(1)

    employee_code = sys.argv[1]
    var = Const()
    output_dir = var.output_images_dir
    os.makedirs(output_dir, exist_ok=True)

    success = process_from_webcam_persistent(output_dir, employee_code)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
