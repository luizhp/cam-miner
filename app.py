import os
import cv2
import time
import simplejpeg
import imagezmq
import configparser

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

    def work_with_captured_video(camera, sender):
        while True:
            ret, frame_current = camera.read()

            if not ret:
                print("Camera is disconnected!")
                camera.release()
                return False
            else:
                jpg_buffer = simplejpeg.encode_jpeg(
                    frame_current, quality=JPEG_QUALITY, colorspace='BGR')
                sender.send_jpg(CAMNAME, jpg_buffer)
        return True

    while True:
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        print('Conecting camera')
        camera = cv2.VideoCapture(CAMURL, cv2.CAP_FFMPEG)
        camera.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

        if camera.isOpened():
            print('Camera is connected')
            response = work_with_captured_video(camera, sender)
            if response == False:
                print('Camera Failed')
                time.sleep(2)
            continue
        else:
            print('Camera not connected')
            camera.release()
            time.sleep(2)
            continue
    cv2.destroyAllWindows()
