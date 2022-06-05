FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update -yq && \
    apt-get -yq install python3-opencv && \
    apt-get -yq upgrade && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ["app.py", "config", "./"]

VOLUME ["/app/config"]

CMD [ "python3", "app.py", "--host=0.0.0.0"]
