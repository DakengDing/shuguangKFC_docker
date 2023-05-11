FROM python:3.10.11-bullseye

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN pip install whitenoise

COPY ./app /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh","/entrypoint.sh" ]