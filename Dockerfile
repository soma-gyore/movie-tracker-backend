FROM python:3.6-slim

EXPOSE 5001

COPY . /opt/movie-tracker

WORKDIR /opt/movie-tracker

RUN pip install -r requirements.txt

CMD if [ ! -d migrations ]; then python3 manage.py db init; python3 manage.py db migrate; fi; \
    python3 manage.py db upgrade; \
    gunicorn --config gunicorn_config.py --reload wsgi:flask_app
