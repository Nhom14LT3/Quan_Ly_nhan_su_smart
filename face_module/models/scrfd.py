import os
import cv2
import numpy as np
import onnxruntime

from face_module.utils.helpers import distance2bbox, distance2kps
from typing import Tuple

__all__ = ["SCRFD"]


class SCRFD:
    # hàm khởi tạo
    def __init__(
        self,
        model_path: str,
        session=None,
        input_size: Tuple[int] = (640, 640),
        conf_thres: float = 0.5,
        iou_thres: float = 0.4,
        # self,
        # model_path: str,
        # input_size: Tuple[int] = (640, 640),
        # conf_thres: float = 0.5,
        # iou_thres: float = 0.4,
    ) -> None:
        if session is None:
            self.session = onnxruntime.InferenceSession(
                model_path,
                providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
            )
        else:
            self.session = session
        

        """SCRFD initialization

        Args:
            model_path (str): Path model .onnx file.
            input_size (int): Input image size. Defaults to (640, 640)
            conf_thres (float, optional): Confidence threshold. Defaults to 0.5.
            iou_thres (float, optional): Non-max supression (NMS) threshold. Defaults to 0.4.
        """

        self.input_size = input_size
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres

        # self.session = onnxruntime.InferenceSession(
        #     model_path,
        #     providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
        # )


        # SCRFD model params --------------
        self.fmc = 3
        self._feat_stride_fpn = [8, 16, 32]
        self._num_anchors = 2
        self.use_kps = True

        self.mean = 127.5
        self.std = 128.0

        self.center_cache = {}
        # ---------------------------------

        self._initialize_model(model_path=model_path)

    def _initialize_model(self, model_path: str):  #tải mô hình .onnx
        """Initialize the model from the given path.

        Args:
            model_path (str): Path to .onnx model.
        """
        try:
            self.session = onnxruntime.InferenceSession(
                model_path,
                providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
            )
            # Get model info
            self.output_names = [x.name for x in self.session.get_outputs()]
            self.input_names = [x.name for x in self.session.get_inputs()]
        except Exception as e:
            print(f"Failed to load the model: {e}")
            raise

    def forward(self, image, threshold):  #trả về các thông tin cần thiết
        scores_list = []
        bboxes_list = []
        kpss_list = []
        input_size = tuple(image.shape[0:2][::-1])

        blob = cv2.dnn.blobFromImage(
            image,
            1.0 / self.std,
            input_size,
            (self.mean, self.mean, self.mean),
            swapRB=True
        )
        outputs = self.session.run(self.output_names, {self.input_names[0]: blob})

        input_height = blob.shape[2]
        input_width = blob.shape[3]

        fmc = self.fmc
        for idx, stride in enumerate(self._feat_stride_fpn):
            scores = outputs[idx]
            bbox_preds = outputs[idx + fmc]
            bbox_preds = bbox_preds * stride
            if self.use_kps:
                kps_preds = outputs[idx + fmc * 2] * stride

            height = input_height // stride
            width = input_width // stride
            key = (height, width, stride)
            if key in self.center_cache:
                anchor_centers = self.center_cache[key]
            else:
                anchor_centers = np.stack(np.mgrid[:height, :width][::-1], axis=-1).astype(np.float32)
                anchor_centers = (anchor_centers * stride).reshape((-1, 2))
                if self._num_anchors > 1:
                    anchor_centers = np.stack([anchor_centers] * self._num_anchors, axis=1).reshape((-1, 2))
                if len(self.center_cache) < 100:
                    self.center_cache[key] = anchor_centers

            pos_inds = np.where(scores >= threshold)[0]
            bboxes = distance2bbox(anchor_centers, bbox_preds)
            pos_scores = scores[pos_inds]
            pos_bboxes = bboxes[pos_inds]
            scores_list.append(pos_scores)
            bboxes_list.append(pos_bboxes)
            if self.use_kps:
                kpss = distance2kps(anchor_centers, kps_preds)
                kpss = kpss.reshape((kpss.shape[0], -1, 2))
                pos_kpss = kpss[pos_inds]
                kpss_list.append(pos_kpss)
        return scores_list, bboxes_list, kpss_list    #trả về danh sách điểm số , danh sách khung bao,danh sách kpss (point) các điểm đặc trưng trên khuân mặt

    def detect(self, image, max_num=0, metric="max"):
    # Hàm phát hiện đối tượng (ví dụ: khuôn mặt) từ ảnh đầu vào.
    # Tham số:
    # - image: Ảnh đầu vào (numpy array).
    # - max_num: Số lượng đối tượng tối đa cần trả về (nếu > 0).
    # - metric: Tiêu chí sắp xếp kết quả ("max" hoặc theo trung tâm ảnh).
        width, height = self.input_size

        im_ratio = float(image.shape[0]) / image.shape[1]
        model_ratio = height / width
        if im_ratio > model_ratio:
            new_height = height
            new_width = int(new_height / im_ratio)
        else:
            new_width = width
            new_height = int(new_width * im_ratio)

        det_scale = float(new_height) / image.shape[0]
        resized_image = cv2.resize(image, (new_width, new_height))

        det_image = np.zeros((height, width, 3), dtype=np.uint8)
        det_image[:new_height, :new_width, :] = resized_image

        scores_list, bboxes_list, kpss_list = self.forward(det_image, self.conf_thres)

        scores = np.vstack(scores_list)
        scores_ravel = scores.ravel()
        order = scores_ravel.argsort()[::-1]
        bboxes = np.vstack(bboxes_list) / det_scale

        if self.use_kps:
            kpss = np.vstack(kpss_list) / det_scale

        pre_det = np.hstack((bboxes, scores)).astype(np.float32, copy=False)
        pre_det = pre_det[order, :]
        keep = self.nms(pre_det, iou_thres=self.iou_thres)
        det = pre_det[keep, :]
        if self.use_kps:
            kpss = kpss[order, :, :]
            kpss = kpss[keep, :, :]
        else:
            kpss = None
        if 0 < max_num < det.shape[0]:
            area = (det[:, 2] - det[:, 0]) * (det[:, 3] - det[:, 1])
            image_center = image.shape[0] // 2, image.shape[1] // 2
            offsets = np.vstack(
                [
                    (det[:, 0] + det[:, 2]) / 2 - image_center[1],
                    (det[:, 1] + det[:, 3]) / 2 - image_center[0],
                ]
            )
            offset_dist_squared = np.sum(np.power(offsets, 2.0), 0)
            if metric == "max":
                values = area
            else:
                values = (area - offset_dist_squared * 2.0)  # some extra weight on the centering
            bindex = np.argsort(values)[::-1]
            bindex = bindex[0:max_num]
            det = det[bindex, :]
            if kpss is not None:
                kpss = kpss[bindex, :]
        return det, kpss
    # Trả về:
    # - det: Danh sách các khung bao cuối cùng (tọa độ + điểm số).
    # - kpss: Danh sách các keypoints cuối cùng (nếu có).

    def nms(self, dets, iou_thres):
    # Hàm thực hiện Non-Maximum Suppression (NMS).
    # Tham số:
    # - dets: Mảng chứa danh sách các khung bao và điểm số, kích thước (N, 5).
    #         Mỗi hàng có dạng [x1, y1, x2, y2, score].
    # - iou_thres: Ngưỡng IoU để loại bỏ các khung bao trùng lặp.
        x1 = dets[:, 0]
        y1 = dets[:, 1]
        x2 = dets[:, 2]
        y2 = dets[:, 3]
        scores = dets[:, 4]

        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = scores.argsort()[::-1]

        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter)

            indices = np.where(ovr <= iou_thres)[0]
            order = order[indices + 1]

        return keep


if __name__ == "__main__":
    detector = SCRFD(model_path="./weights/det_10g.onnx")
    cap = cv2.VideoCapture(0)

    captured = False  # Trạng thái đã chụp chưa

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Không thể đọc từ webcam.")
            break

        boxes_list, points_list = detector.detect(frame)

        # Nếu có ít nhất 1 khuôn mặt và chưa chụp
        if len(boxes_list) > 0 and not captured:
            print(f"✅ Phát hiện {len(boxes_list)} khuôn mặt. Đang lưu ảnh...")

            # Vẽ khung quanh khuôn mặt
            for box in boxes_list:
                x1, y1, x2, y2, score = box.astype(np.int32)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Lưu ảnh
            os.makedirs("captured", exist_ok=True)
            output_path = os.path.join("captured", "captured_face.jpg")
            cv2.imwrite(output_path, frame)
            print(f"📸 Ảnh đã lưu tại: {output_path}")
            captured = True

        cv2.imshow("FaceDetection - Tự động chụp", frame)

        if cv2.waitKey(1) & 0xFF == ord("q") or captured:
            break

    cap.release()
    cv2.destroyAllWindows()
