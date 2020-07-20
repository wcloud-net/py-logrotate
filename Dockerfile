FROM python:3.6

COPY . /app
WORKDIR /app

ENTRYPOINT ["python", "-u", "./logrotate.py"]