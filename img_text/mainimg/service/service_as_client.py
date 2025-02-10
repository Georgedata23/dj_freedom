"""
Здесь хранятся функции для отправки запросов к fastapi
"""

import requests

from img_text.settings import MEDIA_ROOT
from mainimg.service.variables import FASTAPI_URL

DRF_URL = "http://127.0.0.1:8002"
def send_image_to_fastapi(id_doc):
    url = f"{DRF_URL}/api/v1/upload/"
    with open(f'{MEDIA_ROOT}/{id_doc}.webp', 'rb+') as img_file:
        file = {'file': img_file}
        data = {"id_doc": id_doc}
        requests.post(url, files=file, data=data)  # Отправка POST-запроса


def delete_to_fastapi(id_doc):
    url = f"{DRF_URL}/api/v1/delete/"
    params = {"id_doc": str(id_doc)}
    requests.delete(url, params=params)


def analyse_to_fastapi(id_doc):
    url = f"{DRF_URL}/api/v1/analyse/"
    data = {"id_doc": str(id_doc)}
    requests.post(url, data=data)



def get_text_to_fastapi(id_doc):
    url = f"{DRF_URL}/api/v1/get_text/"
    params = {"id_doc": str(id_doc)}
    response = requests.get(url, params=params)
    return response.json()   # decode(encoding="utf-8")
