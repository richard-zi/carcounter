import logging
from collections import deque, defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
from streamlit_webrtc import VideoTransformerBase
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class YOLOv8Transformer(VideoTransformerBase):
    """
    Transformer class for vehicle detection and tracking using YOLOv8 model.
    """
    VEHICLE_CLASSES = {
        "car": 2,
        "truck": 7,
        "bus": 5
    }
    CLASS_ID_TO_VEHICLE = {v: k for k, v in VEHICLE_CLASSES.items()}
    MAX_TRACK_LENGTH = 30
    DATA_FILE_PATH = 'data/vehicle_timestamps.txt'
    LINE_RATIO = 0.5
    FONT_SCALE = 0.5
    LINE_SPACING = 25
    VERTICAL_OFFSET = 30

    def __init__(self, model_name: str):
        """
        Initializes the YOLOv8 transformer.

        Args:
            model_name (str): Name of the YOLOv8 model.
        """
        try:
            self.model_path = f'models/{model_name}.pt'
            self.model = YOLO(self.model_path)
            self.track_history = defaultdict(lambda: deque(maxlen=self.MAX_TRACK_LENGTH))
            self.counters = {vehicle: {"in": 0, "out": 0} for vehicle in self.VEHICLE_CLASSES}
            logger.info(f"Initialized YOLOv8Transformer with model {model_name}")
        except Exception as e:
            logger.error(f"Error initializing YOLOv8Transformer: {e}")
            raise

    def _get_current_timestamp(self) -> str:
        """
        Returns the current timestamp in a formatted string.

        Returns:
            str: Current timestamp.
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def save_to_file(self, vehicle: str, direction: str):
        """
        Saves vehicle direction and timestamp to a file.

        Args:
            vehicle (str): Name of the vehicle.
            direction (str): Direction of the vehicle (in or out).
        """
        try:
            timestamp = self._get_current_timestamp()
            with open(self.DATA_FILE_PATH, 'a') as file:
                file.write(f"{vehicle} - {direction} - Timestamp: {timestamp}\n")
            logger.info(f"Saved {vehicle} - {direction} to file")
        except Exception as e:
            logger.error(f"Error saving to file: {e}")

    def _update_counter_and_save(self, vehicle: str, direction: str):
        """
        Updates the vehicle counters and saves the direction to a file.

        Args:
            vehicle (str): Name of the vehicle.
            direction (str): Direction of the vehicle (in or out).
        """
        try:
            self.counters[vehicle][direction] += 1
            self.save_to_file(vehicle, direction)
        except Exception as e:
            logger.error(f"Error updating counter and saving: {e}")

    def _process_tracking_results(self, img, results, x_line):
        """
        Processes tracking results, updates counters, and overlays results on the image.

        Args:
            img (np.ndarray): Image frame.
            results: Tracking results from YOLO model.
            x_line (int): Position of the line on the video feed.
        
        Returns:
            np.ndarray: Processed image frame.
        """
        if not results:
            return img

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
                    vehicle = self.CLASS_ID_TO_VEHICLE.get(detected_class)
                    if vehicle:
                        if dx > 0 and track[-2][0] < x_line and track[-1][0] > x_line:
                            self._update_counter_and_save(vehicle, "out")
                        elif dx < 0 and track[-2][0] > x_line and track[-1][0] < x_line:
                            self._update_counter_and_save(vehicle, "in")

                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(img, [points], isClosed=False, color=(230, 230, 230), thickness=2)
                cv2.circle(img, (int(x), int(y)), radius=5, color=(0, 255, 0), thickness=-1)

        return img

    def transform(self, frame):
        """
        Processes each video frame for vehicle detection and tracking.

        Args:
            frame: Video frame.
        
        Returns:
            np.ndarray: Processed video frame.
        """
        try:
            img = frame.to_ndarray(format="bgr24")
            x_line = int(img.shape[1] * self.LINE_RATIO)
            results = self.model.track(img, persist=True, classes=list(self.VEHICLE_CLASSES.values()), tracker="bytetrack.yaml")
            img = self._process_tracking_results(img, results, x_line)
            
            for idx, (vehicle, counts) in enumerate(self.counters.items()):
                y_position = self.VERTICAL_OFFSET + idx * 2 * self.LINE_SPACING
                cv2.putText(img, f"{vehicle.capitalize()} In: {counts['in']}", (10, y_position), cv2.FONT_HERSHEY_SIMPLEX, self.FONT_SCALE, (0, 255, 0), 2)
                cv2.putText(img, f"{vehicle.capitalize()} Out: {counts['out']}", (10, y_position + self.LINE_SPACING), cv2.FONT_HERSHEY_SIMPLEX, self.FONT_SCALE, (0, 0, 255), 2)
            
            return img
        except Exception as e:
            logger.error(f"Error in transform method: {e}")
            raise

