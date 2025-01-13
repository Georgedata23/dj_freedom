from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render

def index(request):
    return HttpResponse("Страница приложения mainimg!")

def upload(request, id_doc):
    if request.POST:
        return HttpResponse(f"<h2>Страница загрузки файла</h2><p>id: {id_doc}</p>")
    else:
        raise Http404()

def upload_slug(request, id_doc_slug):
    return HttpResponse(status=422, content="Uncorrected id, use integer!")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')