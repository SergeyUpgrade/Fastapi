FROM python:latest

WORKDIR /app app

COPY req.txt req.txt

RUN pip install --no-cache-dir --upgrade -r req.txt

COPY . .