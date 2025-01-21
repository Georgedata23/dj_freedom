import os
import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
from django.views import View

from img_text import settings
from mainimg.models import Cart
from mainimg.service.service_for_delete_index import ForIndex, ForDelete, ForAnalyse
from mainimg.service.service_for_upload import ForUpload
from mainimg.service.variables import menu_index, data_df


class TextImg:

    def __init__(self, text: str, id_doc: int):
        self.text = text
        self.id = id_doc


@login_required
def index(request):

    images = ForIndex.files_upload()

    data = {'title': 'Главная страница',
            'menu': menu_index,
            'posts': data_df,
            'images': images
    }
    return render(request, 'mainimg/index.html', context=data)


@login_required
def upload(request, id_doc):

    up = ForUpload(id_doc, request)
    message, id_doc = up.check_id_message()
    form, message_form = up.for_upload_form()
    data = {
        'title': 'Загрузка документа',
        'for_image': 'Файл успешно загружен!',
        'id': id_doc,
        'menu': menu_index,
        'form': form,
        'message': message,
        'message_form': message_form,
    }
    return render(request, 'mainimg/upload.html', context=data)

def upload_slug(request, id_doc_slug):
    return HttpResponse(status=422, content="Uncorrected id, use integer!")


@login_required
def analyse(request):
    if request.method == 'GET':
        data = {'title': 'Страница анализа изображения!',
                'menu': menu_index}
        return render(request, 'mainimg/analyse.html', data)

    elif request.method == 'POST':
        id_doc = request.POST['field_id']
        if os.path.exists(f"media/{id_doc}.webp"):
            image = ForAnalyse.text_image_db(id_doc)
            text = "dfgnadfkljgkldfgj"
            data = {'title': 'Страница результата анализа изображения!',
                    'text': text,
                    'menu': menu_index,
                    'image': image}
            return render(request, 'mainimg/analyse_response.html', data)
        else:
            return HttpResponse("<h1> Файл с данным id не найден! </h1>")


@login_required
def get_text(request):
    if request.method == 'GET':
        data = {'title': 'Страница получения текста!',
                'menu': menu_index}
        return render(request, 'mainimg/get_text.html', data)

    elif request.method == 'POST':
        id_doc = request.POST['field_id']
        text = "sflkhnfgmgfg"
        data = {'title': 'Страница результата анализа изображения!',
                'text': text,
                'menu': menu_index,
                'id': id_doc}
        return render(request, 'mainimg/get_text_response.html', data)


class DeleteFormView(PermissionRequiredMixin, TemplateView):
    template_name = 'restricted_form.html'
    permission_required = 'app_name.some_permission'
    raise_exception = True

    data = {"title": "Страница удаления изображения!", 'menu': menu_index}

    def get(self, request):
        return render(request, 'mainimg/delete.html', self.data)

    def post(self, request):
        id_doc = request.POST['field_id']
        try:
            ForDelete.file_delete(id_doc, request)
            return HttpResponse(f"<h1>Файл {id_doc}.webp успешно удалён.</h1>")
        except FileNotFoundError:
            return HttpResponse(f"<h1>Файл {id_doc}.webp не найден.</h1>")


def forbidden(request, exception):
    return HttpResponse("<h1>вам сюда нельзя, kiss!</h1>")


def page_not_found(request, exception):
    return redirect('home', permanent=True)