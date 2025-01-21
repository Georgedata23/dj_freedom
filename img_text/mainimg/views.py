import os
import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView

from mainimg.service.service_data import for_data_upload, for_data_index, data_analyse_get, for_data_analyse_post, \
    data_get_text_get, for_data_get_text_post, data_delete
from mainimg.service.service_full import ForDelete, ForAnalyse
from mainimg.service.variables import menu_index

@login_required
def index(request):
    data = for_data_index()
    return render(request, 'mainimg/index.html', context=data)

@login_required
def upload(request, id_doc):
    data = for_data_upload(id_doc=id_doc, request=request)
    return render(request, 'mainimg/upload.html', context=data)

def upload_slug(request, id_doc_slug):
    return HttpResponse(status=422, content="Uncorrected id, use integer!")

@login_required
def analyse(request):

    if request.method == 'GET':
        return render(request, 'mainimg/analyse.html', data_analyse_get)

    elif request.method == 'POST':
        id_doc = request.POST['field_id']
        if os.path.exists(f"media/{id_doc}.webp"):
            data = for_data_analyse_post(id_doc)
            return render(request, 'mainimg/analyse_response.html', data)
        else:
            return HttpResponse("<h1> Файл с данным id не найден! </h1>")


@login_required
def get_text(request):

    if request.method == 'GET':
        return render(request, 'mainimg/get_text.html', data_get_text_get)

    elif request.method == 'POST':
        data = for_data_get_text_post(request)
        return render(request, 'mainimg/get_text_response.html', data)


class DeleteFormView(PermissionRequiredMixin, TemplateView):
    template_name = 'restricted_form.html'
    permission_required = 'app_name.some_permission'
    raise_exception = True

    def get(self, request):
        return render(request, 'mainimg/delete.html', data_delete)

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