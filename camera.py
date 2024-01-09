from time import sleep
from measure import get_measures
from picamera import PiCamera
from datetime import datetime
from send_img import send_img
import asyncio
import logging

logging.basicConfig(filename='./logs/make_photo.log', encoding='utf-8', level=logging.DEBUG)

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
        print("Photo has been made.")
        logging.debug('This message should go to the log file')
        await send_img(path_tmp, img_name, current_date)
        await make_photo()

    except Exception as err:
        logging.error()(f'LOG ERROR in make_photo: {err}')
        await asyncio.sleep(2)
        await make_photo()


async def start_camera():
    try:
        resolution = {"width": 2592, "height": 1944}
        camera.resolution = (resolution["width"], resolution["height"])
        camera.start_preview()
        # Camera warm-up time
        await asyncio.sleep(2)
        print("Camera has been turned on.")
        await make_photo()

    except:
        await asyncio.sleep(2)
        await start_camera()


async def cleanup():
    # Add cleanup steps here, e.g., stopping the camera preview
    camera.stop_preview()
    await main()

async def main() -> None:
    task_camera = asyncio.create_task(start_camera())
    task_measures = asyncio.create_task(get_measures())

    try:
        await task_camera
        await task_measures
    except asyncio.CancelledError:
        # Handle the cancellation of tasks (e.g., during cleanup)
        pass
    finally:
        await cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C gracefully
