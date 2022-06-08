import os
import cv2

class VideoCapture:

    def __init__(self, url, width, height):
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

        self.cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
        
        _w  = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        _h  = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        if _w > width:
          self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        
        if _h > height:
          self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        return self.cap.read()

    def release(self):
        return self.cap.release()

    def isOpened(self):
        return self.cap.isOpened()
