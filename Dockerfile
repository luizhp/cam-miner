FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -yq && \
    apt-get -yq install python3-opencv && \
    apt-get -yq upgrade && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ["app.py", "config", "VideoBufferless.py", "VideoCapture.py", "Config.py", "./"]

VOLUME ["/app/config"]

CMD [ "python3", "-u", "app.py", "--host=0.0.0.0"]
