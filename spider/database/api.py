from datetime import datetime

from pymongo.operations import InsertOne
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
    conn = get_janpanese_playlist()
    conn.insert_one(data)


def insert_chinese_playlist(data):
    conn = get_chinese_playlist()
    conn.insert_one(data)

def insert_single_comments(hot_comments, nor_comments):
    conn = get_single_comments()
    requests = [InsertOne(item) for item in hot_comments+nor_comments]
    if requests:
        conn.bulk_write(requests)

def search_song_list_by_filter(filters, offset, limit, cols=None):
    conn = get_new_songs()
    if cols:
        return conn.find(filters, cols).skip(offset).limit(limit)
    else:
        return conn.find(filters).skip(offset).limit(limit)

def search_chinese_lists_by_filter(filters, offset, limit, cols=None):
    conn = get_chinese_playlist()
    if cols:
        return conn.find(filters, cols).skip(offset).limit(limit)
    else:
        return conn.find(filters).skip(offset).limit(limit)

def search_janpanese_lists_by_filter(filters, offset, limit, cols=None):
    conn = get_janpanese_playlist()
    if cols:
        return conn.find(filters, cols).skip(offset).limit(limit)
    else:
        return conn.find(filters).skip(offset).limit(limit)


def search_by_comment_id(filter):
    conn = get_comments()
    return conn.find(filter)
