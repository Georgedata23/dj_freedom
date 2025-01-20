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
        utd = UsersToDocs.objects.get(username=request.user)
        utd.docs_id.remove(doc)
        doc.delete()


    @classmethod
    def file_delete(cls, id_doc, request):
        os.remove(f'media/{id_doc}.webp')
        cls.db_delete_data(id_doc, request)


class ForGetText:

    @classmethod
    def text_image_db(self, id_doc):
        text = "sflkhnfgmgfg"
        image = {
            'url': os.path.join(settings.MEDIA_URL, f"{id_doc}.webp"),
            'id': id_doc,
        }
        Cart.objects.filter(docs_id=id_doc).update(payment=True)
        return text, image
