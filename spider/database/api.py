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


def insert_song_list_data(data):
    conn = get_new_songs()
    conn.insert_one(data)


def insert_comments(data):
    conn = get_comments()
    conn.insert_one(data)


def insert_playlist(data):
    conn = get_playlist()
    conn.insert_one(data)


def insert_chinese_playlist(data):
    conn = get_chinese_playlist()
    conn.insert_one(data)


def search_song_list_by_filter(filters, offset, limit, cols=None):
    conn = get_new_songs()
    if cols:
        return conn.find(filters, cols).skip(offset).limit(limit)
    else:
        return conn.find(filters).skip(offset).limit(limit)


def search_by_comment_id(filter):
    conn = get_comments()
    return conn.find(filter)
