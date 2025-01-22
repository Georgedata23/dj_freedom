from mainimg.service.service_as_client import analyse_to_fastapi, get_text_to_fastapi
from mainimg.service.service_for_upload import ForUpload
from mainimg.service.service_full import ForIndex, ForAnalyse
from mainimg.service.variables import menu_index


data_analyse_get = {'title': 'Страница анализа изображения!',
                    'menu': menu_index}

data_get_text_get = {'title': 'Страница получения текста!',
        'menu': menu_index}

data_delete = {"title": "Страница удаления изображения!", 'menu': menu_index}

def for_data_upload(id_doc, request):
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
    return data

def for_data_index():

    images = ForIndex.files_upload()

    data = {'title': 'Главная страница',
            'menu': menu_index,
            'images': images
            }
    return data


def for_data_analyse_post(id_doc):
    image = ForAnalyse.text_image_db(id_doc)
    print(analyse_to_fastapi(id_doc))
    text = get_text_to_fastapi(id_doc)
    data = {'title': 'Страница результата анализа изображения!',
            'text': text,
            'menu': menu_index,
            'image': image}
    return data


def for_data_get_text_post(request):
    id_doc = request.POST['field_id']
    text = get_text_to_fastapi(id_doc)
    data = {'title': 'Страница результата анализа изображения!',
            'text': text,
            'menu': menu_index,
            'id': id_doc}
    return data
