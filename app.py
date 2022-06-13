import simplejpeg
import imagezmq

from utilities import util
from Config import Config
from VideoCapture import VideoCapture
from VideoBufferless import VideoBufferless

if __name__ == "__main__":

    logger = util.get_logger('cam-miner')
    config = Config()

    while True:
        logger.info('Start imagezmq publisher')
        sender = imagezmq.ImageSender(
            "tcp://*:{}".format(config.get('SENDER', 'PORT')), REQ_REP=False)

        logger.info('Conecting camera')
        camera = VideoCapture(config.get('CAM', 'URL'), config.get(
            'FRAME', 'WIDTH'), config.get('FRAME', 'HEIGHT'))

        if camera.isOpened():
            logger.info('Camera is connected')
            camname = config.get('CAM', 'NAME')
            jpeg_quality = config.get('FRAME', 'JPEG_QUALITY')
            cap = VideoBufferless(camera)
            while True:
                frame = cap.read()
                jpg_buffer = simplejpeg.encode_jpeg(
                    frame, quality=jpeg_quality, colorspace='BGR')
                sender.send_jpg(camname, jpg_buffer)
        else:
            logger.error('Camera not connected')
            camera.release()
            sender.close()
