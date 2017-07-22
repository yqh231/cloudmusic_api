from flask import Flask

from website.app.api import api
from spider.database.init_db import config_mongo
from spider.util.conf import conf


def create_app():
    app = Flask(__name__)
    config_mongo(conf)
    app.register_blueprint(api)
    app.config['JSON_AS_ASCII'] = False
    app.config['ensure_ascii'] = False
    return app
