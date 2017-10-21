FROM python:3.6-alpine

EXPOSE 5000

COPY ./requirements.txt /opt/movie-tracker/requirements.txt

WORKDIR /opt/movie-tracker

RUN pip install -r requirements.txt

CMD ["gunicorn", "--config", "gunicorn_config.py", "wsgi:flask_app"]