from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
from streamlit_webrtc import VideoTransformerBase, VideoFrame

class YOLOv8Transformer(VideoTransformerBase):
    VEHICLE_CLASSES = {
        "car": 2,
        "motorcycle": 3,
        "truck": 7,
        "bus": 5
    }
    
    # Erstellen Sie ein umgekehrtes Wörterbuch, um Klassen-IDs schneller zuzuordnen.
    CLASS_ID_TO_VEHICLE = {v: k for k, v in VEHICLE_CLASSES.items()}

    def __init__(self, model_name):
        self.model_path = f'models/{model_name}.pt'
        self.model = YOLO(self.model_path)
        self.track_history = defaultdict(lambda: [])
        self.counters = {
            vehicle: {"in": 0, "out": 0} for vehicle in self.VEHICLE_CLASSES
        }

    def recv(self, frame: VideoFrame) -> VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        
        x_line = int(img.shape[1] * 0.5)
        
        results = self.model.track(img, persist=True, classes=list(self.VEHICLE_CLASSES.values()), tracker="bytetrack.yaml")
        
        if results:
            img = results[0].plot()

            cv2.line(img, (x_line, 0), (x_line, img.shape[0]), (0, 0, 255), 2)

            if hasattr(results[0].boxes, 'id') and results[0].boxes.id is not None:
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id.int().cpu().tolist()
                detected_classes = results[0].boxes.cls.int().cpu().tolist()

                for box, track_id, detected_class in zip(boxes, track_ids, detected_classes):
                    x, y, w, h = box
                    track = self.track_history[track_id]
                    track.append((float(x), float(y)))

                    if len(track) > 2:
                        dx = track[-1][0] - track[-2][0]
                        # Verwenden Sie das umgekehrte Wörterbuch, um das Fahrzeug zuzuordnen.
                        vehicle = self.CLASS_ID_TO_VEHICLE.get(detected_class)
                        if vehicle:
                            if dx > 0 and track[-2][0] < x_line and track[-1][0] > x_line:
                                self.counters[vehicle]["out"] += 1
                            elif dx < 0 and track[-2][0] > x_line and track[-1][0] < x_line:
                                self.counters[vehicle]["in"] += 1

                    if len(track) > 30:
                        track.pop(0)

                    points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(img, [points], isClosed=False, color=(230, 230, 230), thickness=2)
                    cv2.circle(img, (int(x), int(y)), radius=5, color=(0, 255, 0), thickness=-1)

            font_scale = 0.5
            line_spacing = 25
            vertical_offset = 30

            for idx, (vehicle, counts) in enumerate(self.counters.items()):
                y_position = vertical_offset + idx * 2 * line_spacing
                cv2.putText(img, f"{vehicle.capitalize()} In: {counts['in']}", (10, y_position), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), 2)
                cv2.putText(img, f"{vehicle.capitalize()} Out: {counts['out']}", (10, y_position + line_spacing), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), 2)

        # Erstellen Sie einen neuen VideoFrame und geben Sie ihn zurück
        return VideoFrame.from_ndarray(img, format="bgr24")
