import cv2
import numpy as np
from face_module.models import SCRFD, ArcFace
from face_module.utils.helpers import compute_similarity, draw_bbox_info

def frame_processor(
    frame: np.ndarray,
    detector: SCRFD,
    recognizer: ArcFace,
    targets: list,
    colors: dict,
    var,
    detected_faces=None
) -> tuple:
    """Phát hiện và nhận diện khuôn mặt từ ảnh đầu vào.
    Trả về: (frame có vẽ khung, tên nếu nhận diện được) hoặc (None, None)
    """

    bboxes, kpss = detector.detect(frame, var.max_num)

    best_match_name = None
    best_similarity = 0

    for bbox, kps in zip(bboxes, kpss):
        *bbox_coords, conf_score = bbox.astype(np.int32)
        embedding = recognizer(frame, kps)

        # So sánh với tất cả embedding mẫu
        for target_emb, name in targets:
            similarity = compute_similarity(target_emb, embedding)

            if similarity > best_similarity and similarity > var.similarity_thresh:
                best_similarity = similarity
                best_match_name = name
                best_bbox = bbox_coords

    if best_match_name:
        color = colors[best_match_name]
        draw_bbox_info(frame, best_bbox, similarity=best_similarity, name=best_match_name, color=color)
        return frame, best_match_name  # ✅ Nhận diện thành công

    return None, None  