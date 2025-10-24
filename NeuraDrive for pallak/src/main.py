# main.py

import cv2
import dlib
import numpy as np
import threading
import time
import os
import pyttsx3 as tts 

from vision.vision_module import VideoStream
from alert_engine import AlertEngine
from behavior.behavior_module import BehaviorMonitor

# --- Global Constants ---
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 48

def main():
    print("[INFO] Loading dlib models...")

    detector = dlib.get_frontal_face_detector()

    # ✅ Fix: Use dynamic absolute path for predictor file
    base_path = os.path.dirname(__file__)
    predictor_path = os.path.join(base_path, "shape_predictor_68_face_landmarks.dat")

    # ✅ Check if file exists, else show clear error
    if not os.path.exists(predictor_path):
        raise FileNotFoundError(
            f"Model file not found: {predictor_path}\n"
            "Please place 'shape_predictor_68_face_landmarks.dat' inside the 'src' folder."
        )

    predictor = dlib.shape_predictor(predictor_path)

    alert_system = AlertEngine(tts.init(), "neuradrive_alerts.log")
    monitor = BehaviorMonitor(predictor, alert_system, EAR_THRESHOLD, CONSEC_FRAMES)

    print("[INFO] Starting video stream...")
    vs = VideoStream().start()
    time.sleep(1.0)

    while True:
        frame = vs.read()
        if frame is None:
            continue

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)
        frame = monitor.process_frame(frame, gray, rects)
        
        cv2.imshow("Neuradrive Wellness Monitor", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    print("[INFO] Shutting down...")
    cv2.destroyAllWindows()
    vs.stop()
    alert_system.cleanup()

if __name__ == "__main__":
    main()
