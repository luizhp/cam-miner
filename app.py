import simplejpeg
import imagezmq

from Config import Config
from VideoCapture import VideoCapture
from VideoBufferless import VideoBufferless

if __name__ == "__main__":

    config = Config()
    sender = imagezmq.ImageSender(
        "tcp://*:{}".format(config.get('SENDER', 'PORT')), REQ_REP=False)
    camera = VideoCapture(config.get('CAM', 'URL'), config.get(
        'FRAME', 'WIDTH'), config.get('FRAME', 'HEIGHT'))

    if camera.isOpened():
        print('Camera is connected')
        camname = config.get('CAM', 'NAME')
        jpeg_quality = config.get('FRAME', 'JPEG_QUALITY')
        cap = VideoBufferless(camera)
        while True:
            frame = cap.read()
            jpg_buffer = simplejpeg.encode_jpeg(
                frame, quality=jpeg_quality, colorspace='BGR')
            sender.send_jpg(camname, jpg_buffer)
    else:
        print('Camera not connected')
        camera.release()
