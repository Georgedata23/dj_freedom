import json

import requests
from django.http import JsonResponse

from img_text.settings import MEDIA_ROOT
from mainimg.service.variables import FASTAPI_URL


def send_image_to_fastapi(request, id_doc):
    image = request.FILES["file"]
    url = f"{FASTAPI_URL}/upload_doc/"
    with open(f'{MEDIA_ROOT}/{id_doc}.webp', 'rb+') as img_file:
        file = {'file': img_file}
    # file_data = image.read()
    # file = {"file": (f"{id_doc}.webp", file_data, image.content_type)}
        data = {"id_doc": str(id_doc)}
        response = requests.post(url, files=file, data=data)  # Отправка POST-запроса

    if response.status_code == 200 or response.status_code == 503:
        return JsonResponse(response.json(), safe=False)
    return JsonResponse({"error": "Failed to process image"}, status=response.status_code)

def delete_to_fastapi(id_doc):
    url = f"{FASTAPI_URL}/delete_doc"
    params = {"id_doc": str(id_doc)}
    response = requests.delete(url, params=params)
    if response.status_code == 200 or response.status_code == 503:
        return JsonResponse(response.json(), safe=False)
    return JsonResponse({"error": "Failed to process image"}, status=response.status_code)

def analyse_to_fastapi(id_doc):
    url = f"{FASTAPI_URL}/doc_analyse/"
    data = {"id_doc": str(id_doc)}
    response = requests.post(url, params=data)
    if response.status_code == 200 or response.status_code == 503:
        return JsonResponse(response.json(), safe=False)
    return JsonResponse({"error": "Failed to process image"}, status=response.status_code)

def get_text_to_fastapi(id_doc):
    url = f"{FASTAPI_URL}/get_text"
    params = {"id_doc": str(id_doc)}
    response = requests.get(url, params=params)
    return JsonResponse(response.json(), safe=False).content.decode(encoding="utf-8")
