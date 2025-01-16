import os

from django.contrib.auth.models import User

from mainimg.forms import UploadFileForm
from mainimg.models import Docs, Cart, Price, UsersToDocs


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

    @staticmethod
    def handle_uploaded_file(f, id_doc):
        with open(f"media/{id_doc}.webp", "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)


    def for_upload_form(self):
        if self.request.method == 'POST':
            form = UploadFileForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                print(file.content_type.split("/")[1])
                self.create_to_db(form)
                self.handle_uploaded_file(file, self.id_doc)
                print(self.request.user)
        else:
            form = UploadFileForm()
        return form

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
        d = Docs(id=self.id_doc, file_path=f"../media/{self.id_doc}.webp",
             size=form.cleaned_data['file'].size//1024)
        d.save()

        price_id = self.for_file_type_id(form)
        p = Price.objects.filter(id=price_id)[0]
        u = UsersToDocs.objects.filter(id=1)[0]
        print(p.price)
        print(u.pk)

        Cart(id=self.id_doc, user_id=u , docs_id=d,
             price_id=p, order_price=p.price * d.size, payment=False).save()
