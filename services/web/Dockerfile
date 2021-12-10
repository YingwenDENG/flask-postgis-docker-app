# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies (it is for running the entrypoint.sh file)
RUN apt-get update && apt-get install -y netcat

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip3 install -r requirements.txt

# copy project
COPY . /usr/src/app/

#CMD ["python3","-m", "flask", "run", "--host=0.0.0.0"]

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]