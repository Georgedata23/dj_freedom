import os

from django.http import HttpResponse

from img_text import settings
from mainimg.models import Cart, Docs, UsersToDocs


class ForIndex:

    @staticmethod
    def files_upload():
        images_dir = os.path.join(settings.MEDIA_ROOT)
        # Получение списка файлов в папке
        images = [{
            'url': os.path.join(settings.MEDIA_URL, f),
            'title': os.path.splitext(f)[0],
        }
        for f in os.listdir(images_dir)
        if os.path.isfile(os.path.join(images_dir, f))
        ]
        return images

class ForDelete:

    @staticmethod
    def db_delete_data(id_doc, request):
        Cart.objects.get(docs_id=id_doc).delete()
        doc = Docs.objects.get(pk=id_doc)
        UsersToDocs.objects.get(username=request.user).docs_id.remove(doc)
        doc.delete()


    @classmethod
    def file_delete(cls, id_doc, request):
        os.remove(f'media/{id_doc}.webp')
        cls.db_delete_data(id_doc, request)

