# Importieren von benötigten Bibliotheken
from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO

# Laden des YOLOv8-Modells
model = YOLO('models/yolov8l.pt')

# Öffnen der Videodatei (in diesem Fall wird die Webcam verwendet)
cap = cv2.VideoCapture(0)

# Speicher für die Verlaufsinformationen der erkannten Objekte
track_history = defaultdict(lambda: [])

# Zähler, um Fahrzeuge zu zählen, die in die Stadt hinein- und herausfahren
in_counter = 0
out_counter = 0

# Festlegen des x-Koordinatenwertes für eine vertikale Linie in der Mitte des Videobildes
x_line = int(cap.get(3) * 0.5)  # Platzierung der Linie in der Mitte des Frames

# Loop, um jedes Frame des Videos zu verarbeiten
while cap.isOpened():
    # Ein Frame aus dem Video lesen
    success, frame = cap.read()

    if success:
        # Ausführen des YOLOv8-Trackings auf dem Frame und Verfolgen von Objekten zwischen Frames
        results = model.track(frame, persist=True, classes=[2], tracker="bytetrack.yaml")

        # Zeichnen der vertikalen Linie im Frame
        cv2.line(frame, (x_line, 0), (x_line, int(cap.get(4))), (0, 0, 255), 2)

        # Anzeigen der In- und Out-Zähler im Frame
        cv2.putText(frame, f"Towards town: {in_counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Out of town: {out_counter}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Überprüfen, ob Ergebnisse vorhanden sind und ob die erkannten Objekte IDs haben
        if results and hasattr(results[0].boxes, 'id') and results[0].boxes.id is not None:
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            annotated_frame = results[0].plot()

            # Für jedes erkannte Objekt
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))

                # Überprüfen der Bewegungsrichtung basierend auf den letzten 2 Positionen
                if len(track) > 2:
                    dx = track[-1][0] - track[-2][0]
                    if dx > 0 and track[-2][0] < x_line and track[-1][0] > x_line:
                        out_counter += 1
                    elif dx < 0 and track[-2][0] > x_line and track[-1][0] < x_line:
                        in_counter += 1

                # Beschränken der Länge des Verlaufs auf 30
                if len(track) > 30:
                    track.pop(0)

                # Zeichnen der Verlaufslinie und der aktuellen Position
                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=2)
                cv2.circle(annotated_frame, (int(x), int(y)), radius=5, color=(0, 255, 0), thickness=-1)

            # Überschreiben des aktuellen Frames mit der annotierten Version
            frame = annotated_frame

        # Anzeigen des Frames mit den Tracking-Ergebnissen
        cv2.imshow("YOLOv8 Tracking", frame)

        # Beenden der Schleife, wenn die Taste "q" gedrückt wird
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

# Freigeben von Ressourcen und Schließen von Fenstern
cap.release()
cv2.destroyAllWindows()
