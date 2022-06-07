import simplejpeg
import imagezmq
import configparser
from VideoCapture import VideoCapture
from VideoBufferless import VideoBufferless

config = configparser.ConfigParser()
config.read('config/app.ini')
CAMNAME = config['CAM']['NAME']
CAMURL = config['CAM']['URL']
PORT = int(config['SENDER']['PORT'])
JPEG_QUALITY = int(config['FRAME']['JPEG_QUALITY'])
WIDTH = int(config['FRAME']['WIDTH'])
HEIGHT = int(config['FRAME']['HEIGHT'])

if __name__ == "__main__":

    sender = imagezmq.ImageSender("tcp://*:{}".format(PORT), REQ_REP=False)
    camera = VideoCapture(CAMURL, WIDTH, HEIGHT)

    if camera.isOpened():
        print('Camera is connected')
        cap = VideoBufferless(camera)
        while True:
            frame = cap.read()
            jpg_buffer = simplejpeg.encode_jpeg(
                frame, quality=JPEG_QUALITY, colorspace='BGR')
            sender.send_jpg(CAMNAME, jpg_buffer)
    else:
        print('Camera not connected')
        camera.release()
