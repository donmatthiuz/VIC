import cv2
import time
from ultralytics import YOLO
from collections import Counter

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture('video_geek.mp4')

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_input = cap.get(cv2.CAP_PROP_FPS)
if fps_input <= 0:
    fps_input = 30

out = cv2.VideoWriter('output_task3.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps_input, (width, height))

prev_time = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
    prev_time = curr_time

    results = model(frame, conf=0.5, iou=0.45, verbose=False)
    
    class_names = model.names
    detected_classes = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        
        label = class_names[cls_id]
        detected_classes.append(label)
        
        display_text = f"{label} {conf:.2f}"
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        text_size = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        cv2.rectangle(frame, (x1, y1 - text_size[1] - 5), (x1 + text_size[0], y1), (0, 255, 0), -1)
        cv2.putText(frame, display_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    cv2.putText(frame, f"FPS: {fps:.1f}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    counts = Counter(detected_classes)
    y_offset = 90
    cv2.putText(frame, "Detecciones:", (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    for obj, count in counts.items():
        y_offset += 25
        cv2.putText(frame, f"- {obj}: {count}", (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)

    out.write(frame)

cap.release()
out.release()
