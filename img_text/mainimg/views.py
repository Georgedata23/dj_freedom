from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

menu = [ "проанализировать картинку", "добавить картинку"]

class TextImg:

    def __init__(self, text: str, id_doc: int):
        self.text = text
        self.id = id_doc

data_df = [
    {'id': 1, 'image': '1.webp'},
    {'id': 2, 'image': '1.webp'},
    {'id': 3, 'image': '1.webp'},
]

def index(request):
    data = {'title': 'Главная страница',
            'menu': menu,
            'posts': data_df
    }
    return render(request, 'mainimg/index.html', context=data)


def upload(request, id_doc):
    # if request.POST:
    data = {'title': 'Загрузка документа',
            'menu': menu,
            'for_image': 'Здесь должна быть загрузка картинки!',
            'id': id_doc
            }
    return render(request, 'mainimg/upload.html', context=data)
    # else:
    #     raise Http404()


def upload_slug(request, id_doc_slug):
    return HttpResponse(status=422, content="Uncorrected id, use integer!")


def analyse(request, id_doc):
    text='abcdef'
    data = {'title': 'Страница анализа изображения!',
            'obj': {'id': id_doc, 'text': text},
            'menu': menu
    }
    return render(request, 'mainimg/analyse.html', data)


def page_not_found(request, exception):
    return redirect('home', permanent=True)
    # return HttpResponseNotFound('<h1>Страница не найдена</h1>')