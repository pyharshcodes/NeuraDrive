# alert_engine.py

import time
from datetime import datetime
import pyttsx3 # Assuming ovttsx3 is pyttsx3

class AlertEngine:
    def __init__(self, tts_engine, log_file_path):
        self.tts_engine = tts_engine # Text-to-Speech engine
        self.log_file = log_file_path
        self.alert_on = False # State to prevent overlapping alerts
        self.wellness_state = "GREEN" # GREEN, YELLOW, RED
        
        # Configure TTS voice (Optional)
        self.tts_engine.setProperty('rate', 150)

    def log_alert(self, alert_type, message):
        """Alert ko log file mein record karta hai."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{alert_type}] {message}\n"
        print(f"[ALERT] {alert_type}: {message}")
        
        with open(self.log_file, "a") as f:
            f.write(log_entry)

    def trigger_alert(self, alert_type):
        """Voice aur beep alert deta hai."""
        if self.alert_on:
            return

        self.alert_on = True
        
        if alert_type == "DROWSINESS":
            self.log_alert("DROWSINESS", "Severe Drowsiness Detected. Take a break!")
            self.speak("Warning! Please wake up and take a rest now.")
            # Beep sound ke liye ek separate function ya OS command use kar sakte hain
        
        elif alert_type == "DISTRACTION":
            self.log_alert("DISTRACTION", "Distraction Detected. Focus on the road!")
            self.speak("Focus on the road!")
        
        elif alert_type == "NO_FACE":
            self.log_alert("NO_FACE", "Driver not visible.")
            self.speak("Driver not visible.")
        
        self.alert_on = False

    def speak(self, text):
        """Text ko bolta hai."""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")

    def update_wellness(self, state):
        """Real-time wellness state update karta hai."""
        self.wellness_state = state
        # Logic to display color coded meter goes here (usually in main loop/vision)

    def cleanup(self):
        """Cleanup resources, jaise ki TTS engine."""
        # pyttsx3 doesn't usually need a cleanup but good practice.
        pass