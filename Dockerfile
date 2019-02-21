FROM python:3.6-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]

