from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from random import randint
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView



class ProtectedPageView(LoginRequiredMixin, TemplateView): # Для классовых view
    template_name = 'protected_page.html'



random_id = randint(1, 10000)
menu_index = {'analyse': "Проанализировать картинку", 'upload': "Добавить картинку", 'id': random_id}

class TextImg:

    def __init__(self, text: str, id_doc: int):
        self.text = text
        self.id = id_doc

data_df = [
    {'id': 1, 'image': '1.webp'},
    {'id': 2, 'image': '2.webp'},
    {'id': 3, 'image': '3.webp'},
]

@login_required
def index(request):
    data = {'title': 'Главная страница',
            'menu': menu_index,
            'posts': data_df
    }
    return render(request, 'mainimg/index.html', context=data)



def handle_uploaded_file(f, id_doc: int):
    with open(f"media/{id_doc}.webp", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
def upload(request, id_doc):
    if request.method == 'POST':

        data = {
            'title': 'Загрузка документа',
            'for_image': 'Файл успешно загружен!',
            'id': id_doc,
            'menu': menu_index
        }
        handle_uploaded_file(request.FILES['upload'], id_doc)
        # form = UploadFileForm(request.POST, request.FILES)
        # photo = request.POST['upload']
        return render(request, 'mainimg/upload.html', context=data)

    elif request.method == 'GET':
        # Отображение формы загрузки
        data = {
            'title': 'Загрузка документа',
            'for_image': 'Здесь должна быть загрузка картинки!',
            'id': id_doc,
            'menu': menu_index
        }
        return render(request, 'mainimg/upload.html', context=data)

    else:
        raise Http404()


def upload_slug(request, id_doc_slug):
    return HttpResponse(status=422, content="Uncorrected id, use integer!")

@login_required
def analyse(request):
    if request.method == 'GET':
        data = {'title': 'Страница анализа изображения!',
                'menu': menu_index}
        return render(request, 'mainimg/analyse.html', data)
    elif request.method == 'POST':
        # Логика получения анализа документа
        id_doc = request.POST['field_id']
        print(id_doc)
        data = {'title': 'Страница анализа изображения!'}
        return render(request, 'mainimg/analyse.html', data)


def page_not_found(request, exception):
    return redirect('home', permanent=True)
    # return HttpResponseNotFound('<h1>Страница не найдена</h1>')