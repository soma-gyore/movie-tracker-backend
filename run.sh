#!/usr/bin/env bash
export FLASK_CONFIGURATION=testing
gunicorn --config gunicorn_config.py --reload wsgi:flask_app
