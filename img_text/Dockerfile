FROM python:3.12

RUN mkdir /src

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /src/for_docker/app.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
