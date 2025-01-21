import os
from pyexpat.errors import messages

from django.contrib.auth.models import User

from img_text import settings
from mainimg.forms import UploadFileForm
from mainimg.models import Docs, Cart, Price, UsersToDocs
from mainimg.service.variables import menu_index


class ForUpload:

    def __init__(self, id_doc, request):
        self.id_doc = id_doc
        self.request = request

    def check_id_message(self):
        message = ''
        while os.path.exists(f"media/{self.id_doc}.webp"):
            self.id_doc += 1
            message = f"Использовался другой  id: {self.id_doc}"
        return message, self.id_doc


    def for_upload_form(self):
        if self.request.method == 'POST':
            form = UploadFileForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                self.create_to_db(form)
                self.handle_uploaded_file(file, self.id_doc)
                message = ''
            else:
                message = 'Используйте изображение, недопустимый формат!'
        else:
            form = UploadFileForm()
            message = ''
        return form, message


    @staticmethod
    def for_file_type_id(form):

        file_type = form.cleaned_data['file'].content_type.split("/")[1]

        if file_type == 'png':
            price_id = 1
        elif file_type == 'jpeg':
            price_id = 2
        elif file_type == 'gif':
            price_id = 3
        elif file_type == 'webp':
            price_id = 4
        elif file_type == 'bmp':
            price_id = 5
        else:
            price_id = 6
        return price_id


    def create_to_db(self, form):

        docs_upload = Docs(id=self.id_doc, file_path=f"../media/{self.id_doc}.webp",
                           size=form.cleaned_data['file'].size // 1024)
        docs_upload.save()

        price_id = self.for_file_type_id(form)
        price_upload = Price.objects.get(pk=price_id)
        user_upload = UsersToDocs.objects.get(username=self.request.user)
        docs_upload.users_to_docs.set([user_upload])
        Cart(id=self.id_doc, user_id=user_upload, docs_id=docs_upload,
             price_id=price_upload, order_price=price_upload.price * docs_upload.size, payment=False).save()


    @staticmethod
    def handle_uploaded_file(f, id_doc):
        with open(f"media/{id_doc}.webp", "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)



