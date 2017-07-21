from spider.cloud_api.verify import (
    generate_secret_key)

BASE_URL = 'http://music.163.com/'

def api_song_url(song_id, rate=192000):
    url = "http://music.163.com/weapi/song/enhance/player/url?csrf_token="
    TEXT = {"ids": "[{}]".format(song_id), "br": rate, "csrf_token": ""}
    return generate_secret_key(TEXT), url

def api_comment(song_id, offset, limit):
    url = BASE_URL + 'weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(song_id)
    TEXT = {"rid":song_id, "offset":offset, "total":"true", "limit":limit, "csrf_token": ""}
    return generate_secret_key(TEXT), url


