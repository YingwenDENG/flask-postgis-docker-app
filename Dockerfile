# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /myApp

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

#COPY App App

ENV FLASK_APP="App/main.py"

ENV FLASK_ENV="development"

CMD ["python3","-m", "flask", "run", "--host=0.0.0.0"]