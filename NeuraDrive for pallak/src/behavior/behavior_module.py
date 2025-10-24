# behavior/behavior_module.py

from scipy.spatial import distance as dist
import cv2
import numpy as np

# Dlib's 68-point facial landmark indices for Left and Right Eyes
# (Yeh points aapko dlib documentation se milenge)
EYE_L = list(range(42, 48))
EYE_R = list(range(36, 42))

class BehaviorMonitor:
    def __init__(self, predictor, alert_engine, ear_thresh, ear_consec_frames):
        self.predictor = predictor
        self.alert_engine = alert_engine
        self.EAR_THRESH = ear_thresh
        self.EAR_CONSEC_FRAMES = ear_consec_frames
        self.drowsy_counter = 0 # Frames counter for drowsiness

    def _eye_aspect_ratio(self, eye):
        """Eye Aspect Ratio (EAR) calculate karta hai."""
        # Vertical distances
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        
        # Horizontal distance
        C = dist.euclidean(eye[0], eye[3])
        
        # EAR formula: (|P2-P6| + |P3-P5|) / (2 * |P1-P4|)
        ear = (A + B) / (2.0 * C)
        return ear

    def _shape_to_np(self, shape, dtype="int"):
        """Dlib shape object ko NumPy array mein convert karta hai."""
        coords = np.zeros((68, 2), dtype=dtype)
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        return coords

    def process_frame(self, frame, gray, rects):
        """Har ek frame ko process karta hai aur alerts check karta hai."""
        
        # --- 1. No Face Check ---
        if len(rects) == 0:
            self.alert_engine.trigger_alert("NO_FACE")
            self.drowsy_counter = 0 # Reset counter when face is gone
            self.alert_engine.update_wellness("RED")
            return frame # Return frame as is

        # --- 2. Face is Present (Drowsiness & Distraction Check) ---
        rect = rects[0] # Focus on the first detected face
        shape = self.predictor(gray, rect)
        points = self._shape_to_np(shape)

        # Get Eye Coordinates
        leftEye = points[EYE_L]
        rightEye = points[EYE_R]
        
        # Calculate EAR
        leftEAR = self._eye_aspect_ratio(leftEye)
        rightEAR = self._eye_aspect_ratio(rightEye)
        avg_EAR = (leftEAR + rightEAR) / 2.0

        # --- Drowsiness Logic ---
        if avg_EAR < self.EAR_THRESH:
            self.drowsy_counter += 1
            if self.drowsy_counter >= self.EAR_CONSEC_FRAMES:
                self.alert_engine.trigger_alert("DROWSINESS")
                self.alert_engine.update_wellness("RED")
            else:
                self.alert_engine.update_wellness("YELLOW") # Getting drowsy
        else:
            self.drowsy_counter = max(0, self.drowsy_counter - 1) # Rolling average effect
            self.alert_engine.update_wellness("GREEN") # Fully alert

        # --- Distraction Logic (Simple Head Pose Check) ---
        # TODO: Implement head pose estimation logic here
        # E.g., if head tilt is > 20 degrees for X seconds, trigger "DISTRACTION"
        
        # --- Visual Feedback (Draw landmarks) ---
        # Optional: Draw the 68 points on the face for debugging/demo
        for (x, y) in points:
             cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
        
        # Display EAR on screen
        cv2.putText(frame, f"EAR: {avg_EAR:.2f}", (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"State: {self.alert_engine.wellness_state}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame