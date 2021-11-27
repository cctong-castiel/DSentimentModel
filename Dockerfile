FROM python:3.8.2

WORKDIR /app

ADD . /app

RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install --no-cache-dir -r /app/lib/requirements.txt

EXPOSE 721

WORKDIR /app/src

CMD gunicorn -c /app/gunicorn.conf main:app
