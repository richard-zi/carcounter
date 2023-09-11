from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8m.pt')

# Open the video file
cap = cv2.VideoCapture(0)

# Store the track history
track_history = defaultdict(lambda: [])

# Defining counters for vehicles moving in and out of the city
in_counter = 0
out_counter = 0

# Defining the x-coordinate for the vertical line
x_line = int(cap.get(3) * 0.5)  # Placing the line in the middle of the frame

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, classes=[2], tracker="bytetrack.yaml")

        # Draw the vertical line on the frame
        cv2.line(frame, (x_line, 0), (x_line, int(cap.get(4))), (0, 0, 255), 2)

        if results and hasattr(results[0].boxes, 'id') and results[0].boxes.id is not None:
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            annotated_frame = results[0].plot()

            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))

                if len(track) > 2:  # Checking movement direction based on the last 2 positions
                    dx = track[-1][0] - track[-2][0]
                    if dx > 0 and track[-2][0] < x_line and track[-1][0] > x_line:
                        out_counter += 1
                    elif dx < 0 and track[-2][0] > x_line and track[-1][0] < x_line:
                        in_counter += 1

                if len(track) > 30:
                    track.pop(0)

                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=2)
                cv2.circle(annotated_frame, (int(x), int(y)), radius=5, color=(0, 255, 0), thickness=-1)

            # Display the in and out counters
            cv2.putText(annotated_frame, f"In: {in_counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Out: {out_counter}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        else:
            annotated_frame = frame

        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
