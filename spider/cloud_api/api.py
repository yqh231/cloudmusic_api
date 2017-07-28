from spider.cloud_api.verify import (
    generate_secret_key)

BASE_URL = 'http://music.163.com/'


def api_song_url(song_id, rate=192000):
    url = "http://music.163.com/weapi/song/enhance/player/url?csrf_token="
    TEXT = {"ids": "[{}]".format(song_id), "br": rate, "csrf_token": ""}
    return generate_secret_key(TEXT), url


def api_comment(song_id, offset, limit):
    url = BASE_URL + 'weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(song_id)
    TEXT = {"rid": song_id, "offset": offset, "total": "true", "limit": limit, "csrf_token": ""}
    return generate_secret_key(TEXT), url


def api_search(key_word, type, offset, limit):
    """
    1: 单曲
    10: 专辑
    100: 歌手
    1000: 歌单
    1002: 用户
    1004: MV
    1006: 歌词
    1009: 电台
    """
    url = BASE_URL + 'weapi/search/suggest/web?csrf_token='
    TEXT = {'s': key_word, 'type': type, 'offset': 0, 'limit': 5}
    return generate_secret_key(TEXT), url


def api_lyric(offset, limit):
    url = BASE_URL + 'weapi/artist/list?csrf_token='
    TEXT = {'cat':'全部','limit':50, 'offset':0,'csrf_token':""}
    import requests
    text = generate_secret_key(TEXT)
    import json
    res = requests.post(url, data=text)
    print(json.loads(res.text))


api_lyric(0, 10)
