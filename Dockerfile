FROM python:3.9.2-alpine3.13

WORKDIR /app

COPY app.py  .
COPY requirements.app.txt .
COPY templates templates/

RUN pip install -r requirements.app.txt

EXPOSE 8080

CMD ["python", "app.py"]