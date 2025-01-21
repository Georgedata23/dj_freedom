import requests
from django.http import JsonResponse

from mainimg.service.variables import FASTAPI_URL


def send_image_to_fastapi(request, id_doc):
    image = request.FILES["file"]
    url = f"{FASTAPI_URL}/upload_doc/"
    print(image.content_type)
    file_data = image.read()
    file = {"file": (f"{id_doc}.webp", file_data, image.content_type)}
    data = {"id_doc": str(id_doc)}
    response = requests.post(url, files=file, data=data)  # Отправка POST-запроса
    if response.status_code == 200 or response.status_code == 503:
        return JsonResponse(response.json(), safe=False)
    return JsonResponse({"error": "Failed to process image"}, status=response.status_code)
