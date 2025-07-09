FROM python:3.11-alpine3.21

ENV PYTHONUNBUFFERED 1
WORKDIR app/
COPY . .

RUN pip install -r requirements.txt
RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

USER my_user
