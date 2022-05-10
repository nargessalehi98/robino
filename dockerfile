FROM m.docker-registry.ir/python:3.8

ENV PYTHONUNBUFFERED=1

ADD ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /code
COPY . /code

EXPOSE 8080

CMD [ "python", "manage.py", "runserver", "8080"]
