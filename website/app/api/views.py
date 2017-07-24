from flask import request

from website.app.api import api
from spider.database import search_song_list_by_filter
from website.app.util import JsonSuccess, JsonError


@api.route('/popular_song_list')
def get_popular_song_list():
    type_ = request.args.get('type')
    offset = request.args.get('offset')
    limit = request.args.get('limit')

    if not type_:
        return JsonError('type参数必填')

    if not offset:
        offset = 0

    if not limit:
        limit = 20

    filters = {
        'type': int(type_)
    }
    result = search_song_list_by_filter(filters, int(offset), int(limit))

    data = [{'song_id': item['_id'], 'name': item['song_name'],
             'comment_id': item['comment_id'], 'source_url': item['source_url']} for item in result]
    return JsonSuccess(data)

@api.route('/popular_song_comments')
def get_popular_song_comments():
    comment_id = request.args.get('comment_id')

    if not comment_id:
        pass

