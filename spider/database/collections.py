from spider.database.init_db import MongoConn, get_conn


def get_new_songs():
    conn = get_conn()
    return conn['song_list']


def get_index():
    conn = get_conn()
    return conn['index']

def get_comments():
    conn = get_conn()
    return conn['comments']

def get_playlist():
    conn = get_conn()
    return conn['play_list_japanese']
