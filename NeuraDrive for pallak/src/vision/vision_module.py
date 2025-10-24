# vision/vision_module.py

from threading import Thread
import cv2

class VideoStream:
    """Class that continuously gets frames from a VideoCapture object
    with a dedicated thread."""
    def __init__(self, src=0):
        # Open the default camera (0)
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()

        # Flag to stop the thread
        self.stopped = False

    def start(self):
        """A new thread start karta hai."""
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """Frame ko continuously grab karta hai."""
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        """Sabse latest frame return karta hai."""
        return self.frame

    def stop(self):
        """Loop aur camera ko stop karta hai."""
        self.stopped = True
        self.stream.release()