import os

from mainimg.forms import UploadFileForm



class ForUpload:

    def __init__(self, id_doc, request):
        self.id_doc = id_doc
        self.request = request

    def check_id_message(self):
        message = ''
        while os.path.exists(f"media/{self.id_doc}.webp"):
            self.id_doc += 1
            message = f"Используется другой  id: {self.id_doc}"
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
                print(f"{file.size//1024}Kb")
                self.handle_uploaded_file(file, self.id_doc)
        else:
            form = UploadFileForm()
        return form