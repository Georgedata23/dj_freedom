

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from mainimg.service_for_upload import ForUpload
from mainimg.variables import menu_index, data_df


# class ProtectedPageView(LoginRequiredMixin, TemplateView): # Для классовых view
#     template_name = 'protected_page.html'

class TextImg:

    def __init__(self, text: str, id_doc: int):
        self.text = text
        self.id = id_doc


@login_required
def index(request):
    data = {'title': 'Главная страница',
            'menu': menu_index,
            'posts': data_df
    }
    return render(request, 'mainimg/index.html', context=data)




@login_required
def upload(request, id_doc):

    up = ForUpload(id_doc, request)
    message, id_doc = up.check_id_message()
    form = up.for_upload_form()
    data = {
        'title': 'Загрузка документа',
        'for_image': 'Файл успешно загружен!',
        'id': id_doc,
        'menu': menu_index,
        'form': form,
        'message': message
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
        # Логика получения анализа документа
        id_doc = request.POST['field_id']
        print(id_doc)
        data = {'title': 'Страница анализа изображения!'}
        return render(request, 'mainimg/analyse.html', data)


def page_not_found(request, exception):
    return redirect('home', permanent=True)