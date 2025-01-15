import os

from mainimg.forms import UploadFileForm




def check_id_message(id_doc):
    message = ''
    while os.path.exists(f"media/{id_doc}.webp"):
        id_doc += 1
        message = f"Используется другой  id: {id_doc}"
    return message, id_doc


def handle_uploaded_file(f, id_doc: int):
    with open(f"media/{id_doc}.webp", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def for_upload_form(request, id_doc):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            print(file.content_type.split("/")[1])
            handle_uploaded_file(file, id_doc)
    else:
        form = UploadFileForm()
    return form