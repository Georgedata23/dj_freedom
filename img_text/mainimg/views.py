from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Страница приложения mainimg!")

def upload(request, id_doc):
    return HttpResponse(f"<h2>Страница загрузки файла</h2><p>id: {id_doc}</p>")

def upload_slug(request, id_doc):
    return HttpResponse(status=422, content="Uncorrected id, use integer!")