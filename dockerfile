FROM m.docker-registry.ir/python:3.11-rc-alpine

ENV PYTHONUNBUFFERED=1


ADD /other_module /other_module
ADD ./requirements.txt /requirements.txt

RUN python -m pip install mongoengine
RUN pip install pyjwt==v1.7.1
RUN pip install other_module/mango-jwt

RUN pip install -r /requirements.txt

WORKDIR /code
COPY . /code

EXPOSE 8080

CMD [ "python", "manage.py", "runserver", "8080"]
