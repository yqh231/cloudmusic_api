# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider.database import insert_song_list_data, insert_comments
from spider.cloud_spider.items import CommentItem, SongListItem
from spider.util.error import error

class CloudSpiderPipeline(object):

    @error
    def __process_song_list(self, item):
        data = {
            '_id': item['_id'][0],
            'song_name': item['song_name'][0],
            'type': item['type'][0],
            'source_url': item['source_url'][0],
            'comment_id': item['comment_id'][0],
            'singer': item['singer'][0],
            'update_time': item['update_time'][0],
            'create_time': item['create_time'][0]
        }
        insert_song_list_data(data)

    @error
    def __process_comments(self, item):
        data = {
            '_id': item['_id'][0],
            'hot_comments': item.get('hot_comments'),
            'comments': item.get('comments'),
            'update_time': item['update_time'][0],
            'create_time': item['create_time'][0]
        }
        insert_comments(data)

    @error
    def __process_japanese_playlist(self, item):
        pass

    def process_item(self, item, spider):
        if spider.name == 'song_list':
            if isinstance(item, SongListItem):
                self.__process_song_list(item)
            if isinstance(item, CommentItem):
                self.__process_comments(item)

        if spider.name == 'play_list_janpanese':
            if isinstance(item, SongListItem):
                self.__process_japanese_playlist(item)
            if isinstance(item, CommentItem):
                self.__process_comments(item)


