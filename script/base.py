import sys,os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.extend([ROOT_PATH])
from spider.database.init_db import config_mongo
from spider.util.conf import conf
config_mongo(conf)