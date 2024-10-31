FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y python3-pip

RUN pip3 install -r config/requirements.txt

CMD ["python3", "-m", "api"]

