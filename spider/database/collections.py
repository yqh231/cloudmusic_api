from spider.database.init_db import MongoConn


def get_new_songs():
    return MongoConn['new_songs']

def get_index():
    return MongoConn['index']