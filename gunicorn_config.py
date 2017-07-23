import multiprocessing
import os

bind = '0.0.0.0:8888'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
chdir = os.path.dirname(os.path.realpath(__file__))
raw_env = ["DJANGO_SETTINGS_MODULE=distributor.settings"]
accesslog = "./logs/gunicorn-access.log"
errorlog = "./logs/gunicorn.log"
reload = True
daemon = False
