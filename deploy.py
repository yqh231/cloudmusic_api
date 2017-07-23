import os

os.system('gunicorn -c gunicorn_config.py -n spider website.manage:app')