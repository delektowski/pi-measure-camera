from paramiko import SSHClient, AutoAddPolicy
from os import remove, getenv, path
from dotenv import load_dotenv
import requests
import asyncio
import asyncssh
import logging

logging.basicConfig(filename='./logs/errors.log', encoding='utf-8', level=logging.ERROR)

load_dotenv()
server_url = getenv("URL")
server_port = getenv("PORT")
server_path_to_pics = getenv("PATH_TO_PICS")


gql_url = f"{server_url}:{server_port}"



async def send_img_data(img_name: str) -> None:
    variables = {"title": img_name}

    body = """
    mutation savePhotoData($title: String) {
        savePhotoData(title: $title) {
            code
            message
            }
        }
    """

    response = requests.post(
        url=f"http://{gql_url}", json={"query": body, "variables": variables}
    )
    print(response.json())
    await asyncio.sleep(1)


async def send_img(path_tmp: str, img_name: str, current_date: str, attempt = 0) -> None:
    img_path = path_tmp + img_name
   
    try:
        send_img_process = await asyncio.create_subprocess_exec('scp', img_path, server_path_to_pics)
        await asyncio.sleep(2)
        print("Photo has been sent.")
        await remove_img_from_tmp(path_tmp,img_name)
        await send_img_data(current_date)
    
    except Exception as err:
        print("Img send error: ", err)
        await asyncio.sleep(2)
        logging.error()('LOG ERROR in send_img: ')
        if attempt < 10:
            await send_img(img_path, img_name, current_date, attempt + 1)


async def remove_img_from_tmp(path_tmp: str,img_name: str ) -> None:
    try:
        file_path = path.join(path_tmp, img_name)
        remove(file_path)
        print("File has been removed: " + file_path)
        await asyncio.sleep(1)

    except Exception as err:
        print("Remove file error: ", err)
