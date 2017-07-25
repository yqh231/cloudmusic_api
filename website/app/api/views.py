from flask import request

from website.app.api import api
from spider.database import search_song_list_by_filter, search_by_comment_id
from website.app.util import JsonSuccess, JsonError, ParamCheck, Param, error


@api.route('/popular_songs_list', endpoint='get_popular_song_list')
@error
@ParamCheck({'type': Param(int),
             'offset': Param(int, optional=True),
             'limit': Param(int, optional=True)})
def get_popular_song_list(params):
    type_ = params['type']
    offset = request.args.get('offset')
    limit = request.args.get('limit')

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


@api.route('/popular_song_comments', endpoint='get_popular_song_comments')
@error
@ParamCheck({'comment_id': Param(int)})
def get_popular_song_comments(params):
    comment_id = params['comment_id']
    filter = {
        '_id': comment_id
    }
    result = search_by_comment_id(filter)

    return JsonSuccess(result[0])
