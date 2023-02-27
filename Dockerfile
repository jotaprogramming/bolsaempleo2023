FROM python:3.11.2-alpine

RUN python -m pip install --upgrade pip

COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt

COPY ./src /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

