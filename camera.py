from time import sleep
from measure import get_measures
from picamera import PiCamera
from datetime import datetime
from send_img import send_img, send_img_data
import asyncio

camera = PiCamera()


def get_date_str() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d") + "_T" + now.strftime("%H:%M:%S")


async def make_photo():
    try:
        current_date = get_date_str()
        img_name = f"img-{current_date}.jpg"
        path_tmp = "tmp/"
        camera.capture(path_tmp + img_name, resize=(640, 480))
        print("Photo has been made")
        await send_img(path_tmp, img_name, current_date)
        await asyncio.sleep(5)
        await make_photo()

    except:
        await asyncio.sleep(2)
        await make_photo()


async def start_camera():
    try:
        resolution = {"width": 2592, "height": 1944}
        camera.resolution = (resolution["width"], resolution["height"])
        camera.start_preview()
        # Camera warm-up time
        await asyncio.sleep(2)
        await make_photo()

    except:
        asyncio.sleep(2)
        await start_camera()


async def main() -> None:
    task_camera = asyncio.create_task(start_camera())
    task_measures = asyncio.create_task(get_measures())

    await task_camera
    await task_measures


if __name__ == "__main__":
    asyncio.run(main())
