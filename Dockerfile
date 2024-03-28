FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "/app/django.sh"]
