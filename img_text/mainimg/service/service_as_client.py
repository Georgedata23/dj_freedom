

import requests

from img_text.settings import MEDIA_ROOT
from mainimg.service.variables import FASTAPI_URL


def send_image_to_fastapi(id_doc):
    url = f"{FASTAPI_URL}/upload_doc/"
    with open(f'{MEDIA_ROOT}/{id_doc}.webp', 'rb+') as img_file:
        file = {'file': img_file}
        data = {"id_doc": id_doc}
        requests.post(url, files=file, data=data)  # Отправка POST-запроса


def delete_to_fastapi(id_doc):
    url = f"{FASTAPI_URL}/delete_doc"
    params = {"id_doc": str(id_doc)}
    requests.delete(url, params=params)


def analyse_to_fastapi(id_doc):
    url = f"{FASTAPI_URL}/doc_analyse/"
    data = {"id_doc": str(id_doc)}
    requests.post(url, params=data)



def get_text_to_fastapi(id_doc):
    url = f"{FASTAPI_URL}/get_text"
    params = {"id_doc": str(id_doc)}
    response = requests.get(url, params=params)
    return response.json()   # decode(encoding="utf-8")
