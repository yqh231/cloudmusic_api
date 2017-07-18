from datetime import datetime
from spider.database.collections import *


def generate_index():
    """
    这个函数用来建立index表
    :return:
    """
    conn = get_index()
    data = {
        '_id': 2,
        'music_index': 0,
        'comment_index': 0,
        'update_time': datetime.now(),
        'create_time': datetime.now()
    }
    conn.insert(data)


def generate_music_index():
    conn = get_index()
    filter = {
        '_id': 1
    }

    update_filter = {
        "$inc": {
            "music": 1
        }
    }
    return conn.find_one_and_update(filter, update_filter)


def generate_comment_index():
    conn = get_index()
    filter = {
        '_id': 1
    }

    update_filter = {
        "$inc": {'comment_index': 1}
    }
    return conn.find_one_and_update(filter, update_filter)