from flask import request,jsonify

from website.app.api import api

@api.route('/popular_songs_list')
def get_popular_song_list():
    type = request.args.get('type')
