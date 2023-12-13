from time import sleep
from picamera import PiCamera
from datetime import datetime
from send_img import send_img, send_img_data

camera = PiCamera()

def get_date_str()-> str: 
    now = datetime.now()
    return now.strftime("%Y-%m-%d") + "_T" + now.strftime("%H:%M:%S")    

def make_photo():
    try:
        current_date = get_date_str()
        img_name = f'img-{current_date}.jpg'
        path_tmp="tmp/"
        camera.capture(path_tmp + img_name, resize=(640, 480))
        print("Photo has been made")
        send_img(path_tmp, img_name, current_date)
        sleep(5)
        make_photo()

    except:
        sleep(2)
        make_photo()

def start_camera():
    try:
        resolution = {"width":2592,"height":1944}
        camera.resolution = (resolution["width"], resolution["height"])
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        make_photo()

    except:
        sleep(2)
        start_camera()

if __name__ == "__main__":
    start_camera()


