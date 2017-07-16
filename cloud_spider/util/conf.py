import importlib
import sys
import os.path

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.extend([ROOT_PATH])

conf = importlib.import_module('spider_settings')
