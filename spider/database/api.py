from datetime import datetime
from spider.database.collections import *


def generate_index():
    """
    这个函数用来建立index表
    :return:
    """
    conn = get_index()
    data = {
        'music_index': 0,
        'comment_index': 0,
        'update_time': datetime.now(),
        'create_time': datetime.now()
    }
    conn.insert(data)


