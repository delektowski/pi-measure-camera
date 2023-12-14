from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from os import remove,getenv
from dotenv import load_dotenv
import requests

load_dotenv()
server_url = getenv('URL')
server_port= getenv('PORT')
server_user= getenv('SERVER_USER')
server_path_to_pics= getenv('PATH_TO_PICS')

remote={"host": server_url, "user": server_user, "path": server_path_to_pics}
gql_url=f"http://{server_url}:{server_port}"

def send_img_data(img_name:str)-> None:
    variables = {
        "title": img_name
    }

    body = """
    mutation savePhotoData($title: String) {
        savePhotoData(title: $title) {
            code
            message
            }
        }
    """

    response = requests.post(url=gql_url, json={"query": body, "variables": variables})
    print(response.json())

def send_img(path_tmp: str, img_name: str, current_date: str)-> None:
    img_path = path_tmp + img_name
    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname=remote["host"], username=remote["user"])
        scp = SCPClient(ssh.get_transport())
        scp.put(img_path, remote_path=remote["path"])
        print("Photo has been sent")
        send_img_data(current_date)
        remove_img_from_tmp(img_path)

    except Exception as e:
        print("Scp send error", e)
        sleep(2) 
        send_img(img_path)

def remove_img_from_tmp(img_path:str)-> None:
    try:
       remove(img_path) 
       print("File has been removed")
       
    except:
       print("File removal error")  
