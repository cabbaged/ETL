FROM python:3.9-slim

# "Exception: you need a C compiler to build uWSGI"
RUN apt-get update -y && apt install -y gcc

COPY requirements /project/
WORKDIR /project

RUN pip3 install -r production.txt

COPY . /project

CMD uwsgi --ini config/uwsgi.ini
