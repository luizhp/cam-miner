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
                frame_current = cv2.resize(frame_current, (WIDTH, HEIGHT))
                jpg_buffer = simplejpeg.encode_jpeg(
                    frame_current, quality=JPEG_QUALITY, colorspace='BGR')
                # ret_code, jpg_buffer = cv2.imencode(
                #    ".jpg", frame_current, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
                sender.send_jpg(CAMNAME, jpg_buffer)
        return True

    while True:
        print('Conecting camera')
        camera = cv2.VideoCapture(CAMURL)
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
