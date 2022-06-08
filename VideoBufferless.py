import queue
import threading
from utilities import util

class VideoBufferless:

    def __init__(self, camera):
        self.logger = util.get_logger('cam-miner')
        self.cap = camera
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                self.logger.error("Camera is disconnected!")
                self.cap.release()
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()
